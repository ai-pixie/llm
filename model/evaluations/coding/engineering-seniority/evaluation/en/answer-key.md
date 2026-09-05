# Engineering Seniority Evaluation
## Answer Key

This file is restricted until `EXAM COMPLETE`.

The answer key defines expected engineering behavior, not a single mandatory implementation.

## T1: Null-safe Project Deletion

### Planted condition

`ResourceRepository.find_by_project()` returns `None` when no resources exist, while `ProjectService.delete_project()` iterates over the result as if it is always iterable. A resource-less project therefore raises a runtime error before project deletion.

### Strong solution evidence

- identifies the contract mismatch as the root cause;
- treats zero resources as a valid empty-collection case;
- preserves deletion when resources exist;
- preserves not-found behavior;
- preserves authorization behavior;
- adds a regression test for a project with no resources;
- keeps the fix proportionate.

Normalizing the repository contract to return `[]` is a clean reference approach. Defensive handling in the service is also acceptable if consistent with the design.

### Major deductions

- broad exception swallowing;
- authorization bypass;
- converting not-found into success;
- no regression test;
- unrelated refactoring.

## T2: Project Expiration

There is no single required implementation.

### Strong solution evidence

- optional expiration persisted in a clear representation;
- canonical timezone handling, normally UTC;
- validation of invalid or nonsensical values;
- backward compatibility for existing projects;
- deterministic expiration detection;
- idempotent expiration processing;
- retry-safe behavior;
- authorization around changing expiration if exposed to callers;
- tests for absent, future, expired, and invalid values;
- use of the existing scheduler or another fixture-consistent execution mechanism.

### Principal-level evidence

Considers processing lifecycle, failure recovery, concurrent processing, API semantics, migration, observability, and operational behavior.

### Distinguished-level evidence

May generalize expiration into a broader lifecycle policy only if repository evidence supports multiple lifecycle concerns. A speculative framework with no evidence is over-engineering.

## T3: Cloud Provider Extensibility

### Planted condition

`CloudOperations` contains repeated provider-specific conditionals for multiple operations.

### Strong solution evidence

- preserves current AWS and Azure behavior;
- isolates provider-specific behavior behind a small explicit contract or equivalent seam;
- makes dependencies injectable/testable;
- avoids spreading provider selection throughout application logic;
- adding a provider requires localized changes;
- generic contracts do not unnecessarily expose provider-specific details;
- tests preserve current provider behavior and predictable unsupported-provider handling.

### Major deductions

- moving the same conditional chain to another file without improving the design;
- a huge speculative interface;
- breaking current behavior;
- unnecessary framework construction.

## T4: Bulk Project Deletion

A synchronous loop over as many as 100,000 projects inside the request path is not production-safe.

### Strong reference architecture

```text
Request
  -> create durable bulk-delete job
  -> queue/background execution
  -> bounded batches
  -> per-project authorization and deletion
  -> persistent progress/result
  -> client status lookup
```

### Strong solution evidence

- asynchronous/background processing;
- bounded batches or chunks;
- authorization enforced for every affected project or an equally safe query boundary;
- idempotency for client retries;
- retry-safe worker behavior;
- partial-failure representation;
- progress and final status retrieval;
- sensible transaction boundaries;
- bounded memory use;
- observability/auditability.

High-value additions, when proportionate, include idempotency keys, retry policies, dead-letter behavior, concurrency controls, and progress metrics.

### Critical-failure patterns

- unauthorized deletion;
- one giant transaction for the entire request;
- unbounded loading of 100,000 records;
- blocking the API while performing all deletes synchronously.

## T5: Request and Response Debug Logging

Blindly storing every complete request and response body is not an acceptable high-level production design.

### Risks the candidate should identify

- passwords;
- authentication tokens;
- API keys;
- session data;
- personally identifiable information;
- customer confidential data;
- compliance exposure;
- uncontrolled storage growth;
- latency and database load;
- retention and access-control risk.

### Strong replacement design

May combine:

- correlation/trace IDs;
- structured logging;
- distributed tracing;
- allow-listed diagnostic fields;
- sensitive-field redaction;
- configurable retention;
- restricted access;
- encryption;
- sampling;
- narrowly scoped diagnostic capture for exceptional cases.

### Principal-level evidence

Reframes the request into a production-safe observability design.

### Distinguished-level evidence

Reframes the underlying debugging problem and composes logs, metrics, traces, reproducibility, and targeted capture rather than treating body persistence as the goal.

Persisting unrestricted secrets, credentials, or sensitive payloads is a Production Safety failure.

## T6: Technical Ownership

There is no single valid issue list, but the fixture contains several concrete high-impact findings.

### Deliberately planted high-value findings

1. **SQL injection risk** in `ProjectRepository.find_by_name()` because user-controlled input is interpolated directly into SQL.
2. **Deletion correctness failure** in the resource-less project path described in T1.
3. **Provider coupling / extensibility debt** in `CloudOperations`, where provider-specific conditionals are duplicated across operations.

Other evidence-based findings may outrank item 3 if the candidate demonstrates real production impact.

### Expected prioritization

The SQL injection risk is normally the highest-impact issue because it is a security-boundary problem. A strong candidate should parameterize the query and add a regression/security test proving malicious input is treated as data.

### Strong solution evidence

- identifies three concrete issues with file/behavior evidence;
- prioritizes by security/correctness/production impact rather than aesthetics;
- implements only the top issue;
- fixes root cause, not symptoms;
- adds regression coverage;
- runs tests;
- avoids unrelated cleanup.

### Principal-level evidence

Prioritizes based on system-wide and operational consequences.

### Distinguished-level evidence

May identify a common architectural, boundary, platform, or development-process weakness explaining multiple problems, but only when grounded in concrete evidence. Unsupported calls for broad rewrites are Scope Discipline failures.
