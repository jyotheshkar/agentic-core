import importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('review',Path(__file__).with_name('review.py')); review=importlib.util.module_from_spec(spec); spec.loader.exec_module(review)

class ReviewSafetyTests(unittest.TestCase):
 def row(self,states): return {'record':{'gates':{k:{'status':v} for k,v in states.items()}}
 }
 def test_fail_is_no_action(self):
  action,reason=review.action(self.row({'live':'FAIL'})); self.assertEqual(action,'NO_ACTION'); self.assertIn('live',reason)
 def test_unknown_is_research_not_pass(self):
  action,reason=review.action(self.row({'live':'PASS','salary':'UNKNOWN'})); self.assertEqual(action,'PRIORITIZE_RESEARCH'); self.assertIn('salary',reason)
 def test_complete_pass_keeps_existing_baseline(self):
  action,_=review.action(self.row({g:'PASS' for g in review.GATES})); self.assertEqual(action,'KEEP_BASELINE')
 def test_no_fabricated_labels_in_review(self):
  self.assertIn('INSUFFICIENT',review.review('1900-01-01')['data_sufficiency'])
 def test_schema_declares_shadow_only(self):
  schema=json.loads(Path(__file__).with_name('schema.json').read_text()); self.assertEqual(schema['mode'],'SHADOW_ONLY')
if __name__=='__main__': unittest.main()
