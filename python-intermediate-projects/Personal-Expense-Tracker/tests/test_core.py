import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from decimal import Decimal
from expense_tracker.core import Tracker, money

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'data.json'; self.t=Tracker(self.path)
    def add(self): return self.t.record('expense','25.50','Food','2026-11-01')
    def test_persistence(self):
        self.add(); self.assertEqual(len(Tracker(self.path).rows()),1)
    def test_summary(self):
        self.add(); self.assertEqual(self.t.summary('2026-11')[0]['expense'],Decimal('25.50'))
    def test_update(self):
        r=self.add(); self.t.record('expense',30,'Food','2026-11-01',transaction_id=r['id']); self.assertEqual(self.t.rows()[0]['amount'],'30.00')
    def test_delete(self):
        self.t.delete(self.add()['id']); self.assertEqual(self.t.rows(),[])
    def test_invalid(self):
        for v in ['NaN','-1','1.001','0']:
            with self.assertRaises(ValueError): money(v)
    def test_budget(self):
        self.t.budget('2026-11',100); self.assertEqual(self.t.summary('2026-11')[2],100)
    def test_filter(self):
        self.add(); self.assertEqual(self.t.rows('2026-12'),[])
    def test_export(self):
        self.add(); p=self.path.with_suffix('.csv'); self.t.export(p); self.assertIn('25.50',p.read_text());
        with self.assertRaises(FileExistsError): self.t.export(p)
