# Hidden Tests

These tests are public but exam-restricted. Do not inspect them before `EXAM COMPLETE`.

They are deliberately narrow behavioral checks and do not define the only valid implementation.

Run a test against a frozen candidate working copy with:

```bash
CANDIDATE_ROOT=/absolute/path/to/frozen/T1 python evaluation/hidden-tests/test_t1_no_resources.py
```

Available checks:

- `test_t1_no_resources.py`: verifies the required no-resource deletion behavior through the fixture's existing public classes.
- `test_t3_existing_contract.py`: verifies AWS/Azure behavior remains compatible after provider refactoring.
- `test_t6_sql_injection.py`: verifies a malicious project-name string is treated as data rather than SQL syntax.

T2, T4, and T5 are intentionally judged primarily from design, implementation evidence, and candidate-written tests because forcing one hidden-test interface would reward benchmark-specific implementation choices over engineering judgment.
