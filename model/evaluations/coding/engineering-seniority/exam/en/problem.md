# Engineering Seniority Evaluation
## Candidate Problems

You are the candidate AI coding agent.

Follow the examination protocol in the parent `README.md`. During the closed-book phase, do not access `evaluation/`, `results/`, Git history, branches, tags, commits, pull requests, external sources, or other assistants.

Each TEST_ID MUST be solved in an independent clean copy of `exam/fixture/`.

Do not carry changes from one TEST_ID into another.

## General rules

1. Inspect the fixture before changing it.
2. Make actual repository changes when the problem asks for implementation.
3. Add or update tests where appropriate.
4. Run relevant tests.
5. Preserve existing behavior unless the requirement explicitly changes it.
6. Avoid unrelated cleanup and speculative rewrites.
7. Consider security, reliability, performance, maintainability, compatibility, and operability when they are materially relevant.
8. If the stated requirement is unsafe or fundamentally wrong, do not implement it blindly. Explain the issue and choose the safest reasonable response.
9. Do not ask for clarification unless the task is impossible to interpret from the fixture. Use engineering judgment.
10. Do not assign yourself a score or Engineering Level during the exam phase.

---

# T1: Null-safe Project Deletion

Users occasionally receive HTTP 500 when deleting a project that has no associated resources.

Fix the problem and add appropriate regression coverage.

Expected behavior:

- a project with resources can still be deleted;
- a project with no resources can be deleted normally;
- existing not-found behavior is preserved;
- existing authorization behavior is preserved;
- the change should be proportionate to the defect.

---

# T2: Project Expiration

Add support for project expiration.

A project may optionally have an expiration time. After it expires, the system must be able to process the expiration safely and predictably.

Use the existing repository architecture where appropriate. Consider persistence, validation, processing, retries, compatibility, and tests as needed for a production-quality implementation.

---

# T3: Cloud Provider Extensibility

Make the cloud-provider component easier to extend for additional providers.

Current AWS and Azure behavior must continue to work. The design should make adding future providers such as Google Cloud straightforward without spreading provider-specific conditionals through application logic.

Use abstractions only where they improve the design. Avoid speculative framework-building.

---

# T4: Bulk Project Deletion

Add support for bulk deletion of projects.

Requirements:

- a request may target up to 100,000 projects;
- unauthorized projects must never be deleted;
- some project deletions may fail while others succeed;
- clients may retry the same request;
- the production API must not be blocked for a long-running delete operation;
- clients need a way to inspect progress and final results;
- the implementation must be safe under retries and partial failures.

Design and implement the most appropriate solution for the fixture.

---

# T5: Request and Response Debug Logging

A product stakeholder asks for the following feature:

> For debugging purposes, store the complete request body and response body for every API request in the database.

Respond to this requirement as the technical owner responsible for a production system.

You may implement the request, modify it, replace it with a safer design, or refuse unsafe portions of it. Make any code changes that are justified by your chosen design and explain your decision.

---

# T6: Technical Ownership

Act as the technical owner of the fixture repository.

Review the repository and identify the **three highest-impact engineering problems**. Prioritize them, explain why they matter, and implement the single most important improvement.

Prefer issues with real impact on security, correctness, reliability, availability, performance, operability, or long-term maintainability over cosmetic cleanup.

Your findings must be grounded in concrete repository evidence.

---

# Required Candidate Report

For every TEST_ID, finish with the following report before moving to the next clean working copy.

## TEST_ID

`T1` through `T6`

## Summary

What you changed or decided.

## Root Cause / Design Decision

The root cause or the engineering reasoning behind the design.

## Files Changed

List the important changed files. If no code change was appropriate, state that explicitly.

## Tests

List tests added, modified, and executed, including results.

## Risks / Limitations

State remaining risks, trade-offs, assumptions, or known limitations.

## Confidence

A number from 0 to 100 representing confidence that the frozen solution is suitable for production in the context of this fixture.

Do not include an Engineering Level or benchmark score.
