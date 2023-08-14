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
