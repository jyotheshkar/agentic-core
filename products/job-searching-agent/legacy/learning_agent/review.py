"""Read-only daily evidence review for the Job Search Learning Agent."""
import argparse, hashlib, json, sqlite3
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
GATES=("live","unique","sponsor_entity","role_sponsorship","salary","occupation","mandatory_eligibility")
LONDON=ZoneInfo("Europe/London")

def london_day(value):
    return datetime.fromisoformat(value).astimezone(LONDON).date().isoformat()

def completed_day(value=None):
    return value or (datetime.now(LONDON).date()-timedelta(days=1)).isoformat()

def load_rows(day):
    # This reviewer is strictly observational. Opening immutable/read-only avoids
    # creating a journal beside the queue while the primary agents are writing.
    path=(ROOT/'data'/'jobs.sqlite3').resolve().as_posix()
    db=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True); db.row_factory=sqlite3.Row
    rows=[]
    for item in db.execute("SELECT id, first_seen, updated, status, submission, record FROM jobs"):
        record=json.loads(item['record'])
        observed=(london_day(item['first_seen'])==day or london_day(item['updated'])==day)
        if observed: rows.append({**dict(item),"record":record})
    return rows

def gate_summary(row):
    gates=row['record'].get('gates',{})
    states={g:gates.get(g,{}).get('status','UNKNOWN') for g in GATES}
    return states, [g for g,s in states.items() if s=='FAIL'], [g for g,s in states.items() if s!='PASS']

def action(row):
    states, failed, unresolved=gate_summary(row)
    if failed: return 'NO_ACTION','hard_gate_fail:'+','.join(failed)
    if unresolved: return 'PRIORITIZE_RESEARCH','explicit_unresolved:'+','.join(unresolved)
    return 'KEEP_BASELINE','all_gates_pass_existing_rules'

def review(day):
    rows=load_rows(day); statuses=Counter(r['status'] for r in rows)
    gate_failures=Counter(); unresolved=Counter(); suggestions=[]; submissions=0; outcomes=[]
    for row in rows:
        _, fails, missing=gate_summary(row); gate_failures.update(fails); unresolved.update(missing)
        proposed,reason=action(row)
        suggestions.append({'job_id':row['id'],'action':proposed,'reason':reason,'status':row['status'],
                            'existing_score':row['record'].get('score'), 'url':row['record'].get('url')})
        if row['submission']: submissions+=1
        explicit=row['record'].get('outcome_label')
        if explicit: outcomes.append({'job_id':row['id'],'label':explicit})
    labelled=sum(1 for r in rows if r['submission'] or r['record'].get('outcome_label'))
    positive=sum(1 for x in outcomes if x['label'] in ('INTERVIEW','OFFER','HIRED'))
    negative=sum(1 for x in outcomes if x['label'] in ('REJECTED','WITHDRAWN'))
    sufficient=labelled>=100 and positive>=20 and negative>=20
    return {'schema_version':'1.0','reviewed_london_day':day,'generated_at':datetime.now(timezone.utc).isoformat(),
      'mode':'SHADOW_ONLY','baseline':'hard gates, then existing score descending, then earliest observation',
      'roles_observed':len(rows),'status_counts':dict(sorted(statuses.items())),'gate_failures':dict(sorted(gate_failures.items())),
      'unresolved_evidence':dict(sorted(unresolved.items())),'packs_ready':statuses['APPLICATION PACK READY'],
      'ready_to_submit':statuses['READY TO SUBMIT'],'jyo_confirmed_submissions':submissions,'explicit_outcomes':outcomes,
      'labelled_transitions':labelled,'data_sufficiency':('SUFFICIENT_FOR_OFFLINE_EVALUATION_ONLY' if sufficient else 'INSUFFICIENT_FOR_LEARNED_POLICY'),
      'policy_change':'NO_MODEL_CHANGE','action_mask_enforced':True,'shadow_suggestions':suggestions,
      'approval_required_for_live_influence':True,'rollback_available':True}

def markdown(result):
    s=result['status_counts']; return f'''# Learning Agent daily review: {result['reviewed_london_day']}

| Metric | Count / state |
|---|---:|
| Roles observed | {result['roles_observed']} |
| QUALIFIED | {s.get('QUALIFIED',0)} |
| VERIFY FIRST | {s.get('VERIFY FIRST',0)} |
| SKIP | {s.get('SKIP',0)} |
| Packs ready | {result['packs_ready']} |
| Ready to submit | {result['ready_to_submit']} |
| Jyo-confirmed submissions | {result['jyo_confirmed_submissions']} |
| Explicit outcome labels | {len(result['explicit_outcomes'])} |
| Learned-policy sufficiency | {result['data_sufficiency']} |
| Policy change | {result['policy_change']} |

Deterministic gates remain authoritative. Suggestions are action-masked and shadow-only. No claim was trained from missing evidence, and no live ranking influence is permitted without Jyo approval, a baseline comparison, a frozen ledger, regression evidence and rollback.
'''

def append_ledger(result):
    target=HERE/'evidence-ledger.jsonl'; previous='GENESIS'
    if target.exists():
        previous=json.loads(target.read_text(encoding='utf-8').splitlines()[-1])['entry_hash']
    body={'previous_hash':previous,'reviewed_london_day':result['reviewed_london_day'],'report_hash':hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest(),'policy_change':result['policy_change']}
    body['entry_hash']=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
    with target.open('a',encoding='utf-8',newline='\n') as out: out.write(json.dumps(body,sort_keys=True)+'\n')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--date'); p.add_argument('--dry-run',action='store_true'); a=p.parse_args()
    day=completed_day(a.date); result=review(day); text=markdown(result)
    if not a.dry_run:
        (HERE/'daily-reviews').mkdir(exist_ok=True)
        (HERE/'daily-reviews'/f'{day}.json').write_text(json.dumps(result,indent=2)+"\n",encoding='utf-8')
        (HERE/'daily-reviews'/f'{day}.md').write_text(text,encoding='utf-8')
        append_ledger(result)
    print(text)
if __name__=='__main__': main()
