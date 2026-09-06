import json
import tempfile
import unittest
from pathlib import Path
import agent_queue as q

class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name); self.db=q.connect(self.root)
    def tearDown(self):
        self.db.close(); self.temp.cleanup()
    def job(self,n):
        return dict(company='Test fixture',title='Evaluator',location='London',legal_entity='Test Fixture Ltd',job_id=str(n),url='https://example.org/jobs/'+str(n),checked_at=q.now(),score=85,gates={g:dict(status='PASS',source='https://example.org/evidence',checked_at=q.now()) for g in q.GATES})
    def test_five_boundary_dedupe_and_receipt(self):
        for n in range(4): q.upsert(self.db,self.job(n))
        q.stage(self.db); self.assertEqual(q.pending(self.db),[])
        q.upsert(self.db,self.job(4)); q.stage(self.db); self.assertEqual(len(q.pending(self.db)),1)
        for n in range(5): q.upsert(self.db,self.job(n))
        q.stage(self.db); self.assertEqual(len(q.pending(self.db)),1)
        key=q.pending(self.db)[0]['id']; q.notice_state(self.db,key,'SENDING')
        with self.assertRaises(ValueError): q.notice_state(self.db,key,'SENDING')
        with self.assertRaises(ValueError): q.notice_state(self.db,key,'SENT')
        q.notice_state(self.db,key,'SENT','TEST-RECEIPT'); q.stage(self.db)
        self.assertEqual(q.pending(self.db),[])
    def test_unknown_gate_blocks_qualification(self):
        r=self.job(1); r['gates']['salary']['status']='UNKNOWN'; jid=q.upsert(self.db,r)
        self.assertEqual(self.db.execute('SELECT status FROM jobs WHERE id=?',(jid,)).fetchone()[0],'VERIFY FIRST')
    def test_history_not_new(self):
        for n in range(6):
            r=self.job(n); r['historical_import']=True; q.upsert(self.db,r)
        q.stage(self.db); self.assertEqual(q.pending(self.db),[])
    def test_cumulative_export(self):
        for n in range(7): q.upsert(self.db,self.job(n))
        a=q.export(self.db,self.root); self.assertEqual(a,dict(total=7,ready=0))
        q.upsert(self.db,self.job(1)); self.assertEqual(q.export(self.db,self.root)['total'],7)
    def test_pack_is_not_submit_ready(self):
        jid=q.upsert(self.db,self.job(1))
        with self.assertRaises(ValueError): q.prepare(self.db,jid,{'pack':{}},self.root)

    def pack(self):
        folder=self.root/'Job Applications'; folder.mkdir(exist_ok=True)
        pack=dict(pages=2,text_checked=True,visual_checked=True)
        for name in ('cv_pdf','cv_docx','answers','evidence'):
            path=folder/name; path.touch(); pack[name]=str(path)
        return pack

    def test_ready_lifecycle_and_expiry(self):
        jid=q.upsert(self.db,self.job(1)); pack=self.pack()
        self.assertEqual(q.prepare(self.db,jid,{'pack':pack},self.root),'APPLICATION PACK READY')
        q.stage(self.db); self.assertEqual(q.pending(self.db),[])
        form=dict(draft_url='https://example.org/draft',checked_at=q.now(),
                  screenshot_path=pack['evidence'],answers_review_path=pack['answers'],
                  all_required_complete=True,attachments_verified=True,saved_draft_verified=True)
        self.assertEqual(q.prepare(self.db,jid,dict(pack=pack,form=form),self.root),'READY TO SUBMIT')
        q.stage(self.db); notices=q.pending(self.db)
        self.assertEqual([n['kind'] for n in notices],['READY'])
        row=json.loads(self.db.execute('SELECT record FROM jobs WHERE id=?',(jid,)).fetchone()[0])
        row['form']['checked_at']='2020-01-01T00:00:00+00:00'
        self.db.execute('UPDATE jobs SET record=? WHERE id=?',(json.dumps(row),jid))
        self.assertEqual(q.export(self.db,self.root)['ready'],0)
        with self.assertRaises(ValueError): q.notice_state(self.db,notices[0]['id'],'SENDING')

    def test_closed_job_cannot_be_prepared_or_notified(self):
        for n in range(5): jid=q.upsert(self.db,self.job(n))
        q.stage(self.db); key=q.pending(self.db)[0]['id']
        self.db.execute("UPDATE jobs SET status='CLOSED' WHERE id=?",(jid,))
        with self.assertRaises(ValueError): q.prepare(self.db,jid,{'pack':self.pack()},self.root)
        with self.assertRaises(ValueError): q.notice_state(self.db,key,'SENDING')

    def test_daily_ready_cap_blocks_eleventh_new_application(self):
        pack=self.pack()
        def form():
            return dict(draft_url='https://example.org/draft',checked_at=q.now(),
                screenshot_path=pack['evidence'],answers_review_path=pack['answers'],
                all_required_complete=True,attachments_verified=True,saved_draft_verified=True)
        for n in range(q.DAILY_READY_CAP):
            jid=q.upsert(self.db,self.job(n))
            q.prepare(self.db,jid,dict(pack=pack,form=form()),self.root)
        self.assertTrue(q.day_status(self.db)['cap_reached'])
        jid=q.upsert(self.db,self.job(99))
        with self.assertRaisesRegex(ValueError,'Daily READY TO SUBMIT cap'):
            q.prepare(self.db,jid,dict(pack=pack,form=form()),self.root)

if __name__=='__main__': unittest.main()
