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

    def test_capacity_caps_burst(self):
        b = m.RetryBudget(capacity=2, ratio=1)
        for _ in range(100):
            b.record_original()
        self.assertEqual([b.allow_retry() for _ in range(3)], [True, True, False])

    def test_denials_do_not_spend_fraction(self):
        b = m.RetryBudget(initial='.5')
        self.assertFalse(b.allow_retry())
        self.assertEqual(str(b.tokens), '0.5')

    def test_aggregate_bound(self):
        b = m.RetryBudget(capacity=100, ratio='.2', initial=2)
        for _ in range(100):
            b.record_original()
        self.assertEqual(sum((b.allow_retry() for _ in range(100))), 22)

    def test_invalid_settings(self):
        for args in [{'capacity': 0}, {'ratio': 2}, {'initial': 11}, {'ratio': float('nan')}, {'capacity': True}]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                m.RetryBudget(**args)

if __name__ == '__main__':
    unittest.main()
