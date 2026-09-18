# Shared retry budget

Limit retry amplification using a fractional token budget earned by original requests.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

Each original request earns a configurable fraction of a retry token. A retry spends one whole token, independently of outcomes. Tokens accumulate only up to capacity; Decimal arithmetic makes fractional accounting repeatable.

## Use in Python

```python
from main import RetryBudget

budget = RetryBudget(capacity=10, ratio='0.2')
for _ in range(5):
    budget.record_original()
assert budget.allow_retry() is True
assert budget.allow_retry() is False
```

## Design limits

This controls aggregate retry volume only. It does not implement timeouts, backoff, per-request attempt limits, or concurrency safety. Call record_original exactly once per original request and allow_retry before each retry. The CLI uses synthetic request events.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
