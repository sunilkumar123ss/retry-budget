"""Fractional retry budgets using exact decimal token accounting."""
import argparse
from decimal import Decimal, InvalidOperation
import json

def amount(value):
    if isinstance(value, bool):
        raise ValueError('Boolean amounts are invalid')
    try:
        n = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError('Invalid amount') from error
    if not n.is_finite() or n < 0:
        raise ValueError('Amount must be finite and nonnegative')
    return n

class RetryBudget:

    def __init__(self, capacity=10, ratio='0.2', initial=0):
        self.capacity = amount(capacity)
        self.ratio = amount(ratio)
        self.tokens = amount(initial)
        if self.capacity < 1 or self.ratio > 1 or self.tokens > self.capacity:
            raise ValueError('Require capacity >=1, ratio <=1, initial <=capacity')
        self.originals = 0
        self.retries = 0

    def record_original(self):
        self.originals += 1
        self.tokens = min(self.capacity, self.tokens + self.ratio)

    def allow_retry(self):
        if self.tokens < 1:
            return False
        self.tokens -= 1
        self.retries += 1
        return True

    def snapshot(self):
        return {'tokens': str(self.tokens), 'original_requests': self.originals, 'allowed_retries': self.retries}

def demo():
    budget = RetryBudget(capacity=3, ratio='0.25')
    for _ in range(12):
        budget.record_original()
    decisions = [budget.allow_retry() for _ in range(5)]
    return {'retry_decisions': decisions, **budget.snapshot()}
if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(demo(), indent=2))
