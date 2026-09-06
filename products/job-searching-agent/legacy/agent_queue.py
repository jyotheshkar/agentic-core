"""Persistent job queue and transactional email outbox. Standard-library only."""
import argparse
import csv
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
GATES = ('live', 'unique', 'sponsor_entity', 'role_sponsorship', 'salary', 'occupation', 'mandatory_eligibility')
DAILY_READY_CAP = 10

def now():
    return datetime.now(timezone.utc).isoformat()

def connect(root=ROOT):
    root = Path(root)
    (root / 'data').mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(root / 'data' / 'jobs.sqlite3', timeout=30)
    db.row_factory = sqlite3.Row
    db.executescript('''
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, fingerprint TEXT UNIQUE, first_seen TEXT,
      updated TEXT, record TEXT NOT NULL, status TEXT NOT NULL, submission TEXT);
    CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, at TEXT, job_id TEXT, kind TEXT, detail TEXT);
    CREATE TABLE IF NOT EXISTS outbox(id TEXT PRIMARY KEY, kind TEXT, job_ids TEXT, state TEXT,
      created TEXT, receipt TEXT);
    CREATE TABLE IF NOT EXISTS notified(job_id TEXT, kind TEXT, PRIMARY KEY(job_id,kind));
    ''')
    return db

def fingerprint(r):
    u = urlsplit(r['url'])
    if u.scheme != 'https' or not u.netloc:
        raise ValueError('Official HTTPS vacancy URL required')
    # Keep query parameters: ATS identifiers may live in the query string.
    r['url'] = urlunsplit((u.scheme,u.netloc.lower(),u.path,u.query,''))
    identity = str(r.get('job_id') or r['url'])
    return '|'.join(('UK',r['legal_entity'].strip().lower(),identity))

def qualified(r):
    return (80 <= r.get('score',0) <= 100 and all(
        r.get('gates',{}).get(g,{}).get('status') == 'PASS' and
        r['gates'][g].get('source') and r['gates'][g].get('checked_at') for g in GATES))

def london_day(value=None):
    """Return the Europe/London calendar date for an ISO timestamp or now."""
    moment = datetime.fromisoformat(value) if value else datetime.now(timezone.utc)
    if moment.tzinfo is None:
        raise ValueError('Timezone-aware timestamp required')
    return moment.astimezone(ZoneInfo('Europe/London')).date().isoformat()

def daily_ready_count(db, day=None):
    day = day or london_day()
    total = 0
    for row in db.execute('SELECT record FROM jobs'):
        stamp = json.loads(row['record']).get('ready_first_at')
        if stamp and london_day(stamp) == day:
            total += 1
    return total

def day_status(db):
    count = daily_ready_count(db)
    return {'london_day': london_day(), 'new_ready_to_submit': count,
            'daily_cap': DAILY_READY_CAP, 'cap_reached': count >= DAILY_READY_CAP}

def expire_readiness(db):
    for row in db.execute("SELECT * FROM jobs WHERE status='READY TO SUBMIT'").fetchall():
        r=json.loads(row['record'])
        try:
            checked=datetime.fromisoformat(r['form']['checked_at'])
            fresh=checked.tzinfo is not None and timedelta(0) <= datetime.now(timezone.utc)-checked < timedelta(minutes=30)
        except (KeyError,ValueError): fresh=False
        if not fresh:
            db.execute("UPDATE jobs SET status='RECHECK REQUIRED',updated=? WHERE id=?",(now(),row['id']))

def upsert(db, r):
    for k in ('company','title','location','legal_entity','url','checked_at'):
        if not r.get(k): raise ValueError('Missing '+k)
    fp = fingerprint(r)
    jid = hashlib.sha256(fp.encode()).hexdigest()[:20]
    old = db.execute('SELECT * FROM jobs WHERE id=?',(jid,)).fetchone()
    status = 'QUALIFIED' if qualified(r) else 'VERIFY FIRST'
    if r.get('rejected_reason'): status = 'SKIP'
    if old:
        previous = json.loads(old['record'])
        for key in ('pack','form'):
            if key in previous: r[key] = previous[key]
        if old['submission']: status = 'SUBMITTED BY JYO'
        elif previous != r and old['status'] == 'READY TO SUBMIT':
            status = 'RECHECK REQUIRED'
        elif previous == r: status = old['status']
    db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET updated=excluded.updated,record=excluded.record,status=excluded.status',
        (jid,fp,old['first_seen'] if old else now(),now(),json.dumps(r),status,None))
    db.execute('INSERT INTO events(at,job_id,kind,detail) VALUES(?,?,?,?)',(now(),jid,'OBSERVED',status))
    return jid

def prepare(db,jid,payload,root=ROOT):
    row = db.execute('SELECT * FROM jobs WHERE id=?',(jid,)).fetchone()
    if not row or row['submission']: raise ValueError('Missing job or already submitted')
    if row['status'] in ('SKIP','CLOSED','ACTION REQUIRED'):
        raise ValueError('Job requires explicit reassessment before preparation')
    r = json.loads(row['record'])
    if not qualified(r): raise ValueError('All qualification gates must pass')
    pack = payload['pack']
    for name in ('cv_pdf','cv_docx','answers','evidence'):
        if not pack.get(name): raise ValueError('Missing artifact: '+name)
        p = Path(pack[name]).resolve()
        if not p.is_relative_to((Path(root)/'Job Applications').resolve()) or not p.is_file():
            raise ValueError('Missing or out-of-scope artifact: '+name)
    if pack.get('pages') != 2 or not pack.get('text_checked') or not pack.get('visual_checked'):
        raise ValueError('Two-page CV must pass text and visual checks')
    r['pack'] = pack
    status = 'APPLICATION PACK READY'
    form = payload.get('form')
    if form:
        for k in ('draft_url','checked_at','screenshot_path','answers_review_path'):
            if not form.get(k): raise ValueError('Missing form evidence: '+k)
        for k in ('screenshot_path','answers_review_path'):
            if not Path(form[k]).is_file(): raise ValueError('Form evidence does not exist: '+k)
        checked = datetime.fromisoformat(form['checked_at'])
        if checked.tzinfo is None or not timedelta(0) <= datetime.now(timezone.utc)-checked < timedelta(minutes=30):
            raise ValueError('Final form evidence must be checked within 30 minutes')
        if form.get('blockers') or not form.get('all_required_complete') or not form.get('attachments_verified'):
            raise ValueError('Form is not ready for final submission')
        if not form.get('saved_draft_verified'):
            raise ValueError('Reopen the saved draft and verify it first')
        if not r.get('ready_first_at'):
            if daily_ready_count(db) >= DAILY_READY_CAP:
                raise ValueError('Daily READY TO SUBMIT cap reached; stop new preparation for London day')
            r['ready_first_at'] = now()
        r['form'] = form
        status = 'READY TO SUBMIT'
    db.execute('UPDATE jobs SET record=?,status=?,updated=? WHERE id=?',(json.dumps(r),status,now(),jid))
    db.execute('INSERT INTO events(at,job_id,kind,detail) VALUES(?,?,?,?)',(now(),jid,'PREPARED',status))
    return status

def stage(db):
    expire_readiness(db)
    reserved = {j for row in db.execute("SELECT job_ids FROM outbox WHERE kind='FOUND' AND state!='CANCELLED'") for j in json.loads(row[0])}
    fresh = [row['id'] for row in db.execute("SELECT * FROM jobs WHERE status IN ('QUALIFIED','APPLICATION PACK READY','READY TO SUBMIT') ORDER BY first_seen,id")
        if row['id'] not in reserved and not json.loads(row['record']).get('historical_import') and not db.execute("SELECT 1 FROM notified WHERE job_id=? AND kind='FOUND'",(row['id'],)).fetchone()]
    for i in range(0,len(fresh)-4,5):
        add_notice(db,'FOUND',fresh[i:i+5])
    for row in db.execute("SELECT * FROM jobs WHERE status='READY TO SUBMIT'").fetchall():
        if not db.execute("SELECT 1 FROM notified WHERE job_id=? AND kind='READY'",(row['id'],)).fetchone():
            add_notice(db,'READY',[row['id']])

def add_notice(db,kind,ids):
    key = kind+'-'+hashlib.sha256('|'.join(ids).encode()).hexdigest()[:16]
    db.execute('INSERT OR IGNORE INTO outbox VALUES(?,?,?,?,?,?)',(key,kind,json.dumps(ids),'PENDING',now(),None))

def pending(db):
    return [dict(r) for r in db.execute("SELECT * FROM outbox WHERE state NOT IN ('SENT','CANCELLED') ORDER BY created")]

def notice_state(db,key,state,receipt=None):
    row = db.execute('SELECT * FROM outbox WHERE id=?',(key,)).fetchone()
    if not row: raise ValueError('Unknown notification')
    if state == 'SENDING' and row['state'] != 'PENDING': raise ValueError('Already claimed; reconcile Outlook before retrying')
    if state == 'SENDING':
        expire_readiness(db)
        for jid in json.loads(row['job_ids']):
            job=db.execute('SELECT * FROM jobs WHERE id=?',(jid,)).fetchone()
            if not job or job['submission'] or not qualified(json.loads(job['record'])):
                raise ValueError('Notification contains an ineligible application')
            if job['status'] in ('SKIP','CLOSED','ACTION REQUIRED','VERIFY FIRST'):
                raise ValueError('Notification contains a blocked application')
            if row['kind']=='READY' and job['status']!='READY TO SUBMIT':
                raise ValueError('Ready notification needs fresh saved-form verification')
    if state == 'SENT':
        if row['state'] not in ('SENDING','UNKNOWN') or not receipt:
            raise ValueError('Confirmed connector receipt required')
        for jid in json.loads(row['job_ids']):
            db.execute('INSERT OR IGNORE INTO notified VALUES(?,?)',(jid,row['kind']))
    db.execute('UPDATE outbox SET state=?,receipt=? WHERE id=?',(state,receipt,key))

def export(db,root=ROOT):
    expire_readiness(db)
    folder = Path(root)/'Job Applications'
    folder.mkdir(exist_ok=True)
    fields = ['application_id','company','role','location','score','status','first_seen','last_verified','official_url','draft_url','cv_pdf','cv_docx','blockers','submitted_at']
    rows = []
    for row in db.execute('SELECT * FROM jobs ORDER BY first_seen,id'):
        r = json.loads(row['record']); p=r.get('pack',{}); f=r.get('form',{})
        rows.append(dict(zip(fields,[row['id'],r['company'],r['title'],r['location'],r.get('score',''),row['status'],row['first_seen'],r['checked_at'],r['url'],f.get('draft_url',''),p.get('cv_pdf',''),p.get('cv_docx',''),r.get('blocker',''),row['submission'] or ''])))
    for name,items in [('applications.csv',rows),('ready_to_submit.csv',[r for r in rows if r['status']=='READY TO SUBMIT'])]:
        target=folder/name; temp=target.with_suffix('.tmp')
        with temp.open('w',newline='',encoding='utf-8-sig') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields); writer.writeheader()
            # Avoid spreadsheet formula execution from employer-controlled text.
            writer.writerows({k:("'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v) for k,v in r.items()} for r in items)
        os.replace(temp,target)
    return {'total':len(rows),'ready':sum(r['status']=='READY TO SUBMIT' for r in rows)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['init','ingest','prepare','list','stage','outbox','claim','sent','unknown','export','status','day-status'])
    parser.add_argument('--file'); parser.add_argument('--id'); parser.add_argument('--receipt')
    parser.add_argument('--status',choices=['SUBMITTED BY JYO','SKIP','CLOSED','ACTION REQUIRED','RECHECK REQUIRED'])
    args=parser.parse_args(); db=connect()
    with db:
        db.execute('BEGIN IMMEDIATE')
        expire_readiness(db)
        if args.command=='ingest':
            data=json.loads(Path(args.file).read_text(encoding='utf-8-sig'))
            result=[upsert(db,r) for r in (data if isinstance(data,list) else [data])]
        elif args.command=='prepare': result=prepare(db,args.id,json.loads(Path(args.file).read_text(encoding='utf-8-sig')))
        elif args.command=='list': result=[dict(r) for r in db.execute('SELECT * FROM jobs')]
        elif args.command=='day-status': result=day_status(db)
        elif args.command=='stage': stage(db); result=pending(db)
        elif args.command=='outbox': result=pending(db)
        elif args.command=='status':
            if not args.status or not args.receipt: raise ValueError('Status and evidence/user instruction required')
            if not db.execute('SELECT 1 FROM jobs WHERE id=?',(args.id,)).fetchone(): raise ValueError('Unknown job')
            db.execute('UPDATE jobs SET status=?,updated=? WHERE id=?',(args.status,now(),args.id))
            if args.status=='SUBMITTED BY JYO': db.execute('UPDATE jobs SET submission=? WHERE id=?',(now(),args.id))
            db.execute('INSERT INTO events(at,job_id,kind,detail) VALUES(?,?,?,?)',(now(),args.id,args.status,args.receipt))
            result='recorded'
        elif args.command in ('claim','sent','unknown'):
            notice_state(db,args.id,{'claim':'SENDING','sent':'SENT','unknown':'UNKNOWN'}[args.command],args.receipt); result='recorded'
        else: result=export(db)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__': main()
