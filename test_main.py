import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)

class RetryBudgetTests(unittest.TestCase):

    def test_fractional_grants(self):
        b = m.RetryBudget(ratio='.1')
        for _ in range(9):
            b.record_original()
        self.assertFalse(b.allow_retry())
        b.record_original()
        self.assertTrue(b.allow_retry())





if __name__ == '__main__':
    unittest.main()
