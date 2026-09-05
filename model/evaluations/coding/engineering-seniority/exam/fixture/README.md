# Evaluation Fixture

A deliberately small production-style Python service used by the Engineering Seniority Evaluation.

It uses only the Python standard library and SQLite.

Run the baseline test suite with:

```bash
python -m unittest discover -s tests -v
```

The baseline tests are expected to pass before an evaluation begins. Some important edge cases are intentionally not covered by the baseline tests because discovering and testing them is part of the evaluation.
