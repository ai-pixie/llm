# Engineering Seniority Evaluation
## Evaluator Instructions

This file is restricted until the candidate has completed all selected tests and output exactly:

```text
EXAM COMPLETE
```

After that point, evaluate only the frozen candidate submissions.

## Evaluation principles

1. Do not modify candidate code after the answer key is unlocked.
2. Grade observable evidence: diff, tests, command output, and frozen candidate report.
3. Do not give credit for intentions that were not implemented or recorded before `EXAM COMPLETE`.
4. A candidate does not need to match the reference approach exactly. A different solution may receive full credit if it is equally or more correct, safe, maintainable, and appropriate for the fixture.
5. Hidden tests are supplementary evidence, not an implementation specification.
6. Penalize unrelated cleanup, speculative frameworks, and disproportionate rewrites.
7. Treat production-safety failures separately as Critical Failures.
8. The candidate's self-reported Confidence value is not scoring evidence.
9. If Exam Integrity failed, mark the entire evaluation `INVALID` and do not assign an Engineering Level.

## Per-test scoring

Each test is scored from 0 to 100.

| Category | Max |
|---|---:|
| Correctness | 25 |
| Repository Comprehension | 10 |
| Implementation Quality | 15 |
| Testing | 15 |
| Architecture / Design | 15 |
| Production Safety | 10 |
| Engineering Judgment | 5 |
| Scope Discipline | 5 |
| Total | 100 |

Use the matching section in `answer-key.md` for expected behavior and high-value evidence.

## Critical Failure

Record `Critical Failure: Yes` when the frozen submission introduces or accepts a severe production problem, including:

- authorization bypass;
- security-boundary breakage;
- clear data-loss or corruption risk;
- unsafe storage of secrets, credentials, or unrestricted sensitive data;
- failure of existing critical behavior;
- knowingly declaring a solution production-ready while relevant tests fail.

If any selected test has a Critical Failure:

- that test's Production Safety score is capped at 3/10;
- the overall weighted score is capped at 69/100;
- Principal and Distinguished are not allowed.

## Overall scoring

Fill a score JSON matching `results/result-template.json`, then run:

```bash
python evaluation/score.py /path/to/result.json
```

The script applies the weights and capability gates from `evaluation/rubric.json`.

## Engineering Levels

### Below Senior

Cannot reliably complete a clearly scoped implementation task.

### Senior

**Can implement.**

Can understand a defined problem in an existing repository and implement a correct, tested change.

### Staff

**Can design.**

Can resolve ambiguity, choose appropriate abstractions, and safely implement changes spanning multiple components.

### Principal

**Can own the system.**

Can reason about system-wide impact, architecture, migration, reliability, operability, and production risk.

### Distinguished

**Can redefine the system.**

Can recognize when the stated requirement or system boundary is the wrong problem definition and replace it with a better system-level design grounded in repository evidence.

More code or more abstraction does not imply a higher level.

## Final evaluator output

Use `results/result-template.md` and include concrete evidence for every major judgment.
