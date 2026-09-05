# Engineering Seniority Evaluation
## Answer Key

このファイルは `EXAM COMPLETE` まで参照禁止です。

Answer Key は唯一の mandatory implementation ではなく、期待する engineering behavior を定義します。

## T1: Null-safe Project Deletion

### 意図的に仕込まれた状態

`ResourceRepository.find_by_project()` は resource がない場合 `None` を返します。一方 `ProjectService.delete_project()` は結果が常に iterable だと仮定して `for` で処理します。この contract mismatch により resource のない project 削除で runtime error が起きます。

### 高評価 evidence

- contract mismatch を root cause として特定;
- zero resources を正常な empty collection case として扱う;
- resource がある削除 behavior を維持;
- not-found behavior を維持;
- authorization behavior を維持;
- resource なし project の regression test を追加;
- 修正範囲が問題に比例している。

Repository contract を `[]` に normalize するのが clean な reference approach です。Design と整合していれば service 側の defensive handling も正解です。

### 大きな減点

- broad exception swallowing;
- authorization bypass;
- not-found を success に変更;
- regression test なし;
- 無関係な refactoring。

## T2: Project Expiration

唯一の required implementation はありません。

### 高評価 evidence

- optional expiration を明確な形式で persistence;
- canonical timezone、通常 UTC;
- invalid / nonsensical value の validation;
- 既存 project の backward compatibility;
- deterministic な expiration detection;
- idempotent processing;
- retry-safe behavior;
- caller に exposed する場合 expiration 変更の authorization;
- absent / future / expired / invalid の tests;
- existing scheduler など fixture に整合する processing mechanism を利用。

### Principal-level evidence

Processing lifecycle、failure recovery、concurrency、API semantics、migration、observability、production operation まで考慮する。

### Distinguished-level evidence

複数 lifecycle concern を示す repository evidence がある場合に限り、expiration を broader lifecycle policy に generalize してよい。Evidence のない framework 化は over-engineering。

## T3: Cloud Provider Extensibility

### 意図的に仕込まれた状態

`CloudOperations` の複数 operation に provider-specific conditional が重複しています。

### 高評価 evidence

- AWS / Azure の現在 behavior を維持;
- provider-specific behavior を小さな明示 contract または同等 seam の後ろへ分離;
- dependency が injectable / testable;
- provider selection が application logic 全体へ拡散しない;
- provider 追加時の変更が局所化;
- generic contract に provider-specific detail を不要に漏らさない;
- current behavior と unsupported-provider behavior の tests。

### 大きな減点

- 同じ conditional chain を別 file に移しただけ;
- 巨大で speculative な interface;
- current behavior の破壊;
- 不要な framework construction。

## T4: Bulk Project Deletion

最大 100,000 project を request path 内の同期 loop で処理するのは production-safe ではありません。

### Strong reference architecture

```text
Request
  -> durable bulk-delete job 作成
  -> queue / background execution
  -> bounded batch
  -> project ごとの authorization と delete
  -> progress/result persistence
  -> client status lookup
```

### 高評価 evidence

- asynchronous/background processing;
- bounded batch / chunk;
- project ごとの authorization または同等に安全な query boundary;
- client retry の idempotency;
- worker retry-safe behavior;
- partial failure representation;
- progress / final status retrieval;
- 適切な transaction boundary;
- bounded memory use;
- observability / auditability。

適切な範囲で idempotency key、retry policy、dead-letter behavior、concurrency control、progress metrics も高評価。

### Critical Failure の例

- unauthorized deletion;
- 全件を1つの巨大 transaction;
- 100,000 records を無制限に memory 展開;
- API request を全削除完了まで block。

## T5: Request / Response Debug Logging

すべての complete request / response body を無条件に保存するのは、高品質な production design ではありません。

### Candidate が認識すべき risk

- password;
- authentication token;
- API key;
- session data;
- PII;
- customer confidential data;
- compliance exposure;
- uncontrolled storage growth;
- latency / database load;
- retention / access control risk。

### より良い design の例

- correlation / trace ID;
- structured logging;
- distributed tracing;
- allow-listed diagnostic fields;
- sensitive-field redaction;
- configurable retention;
- restricted access;
- encryption;
- sampling;
- exceptional case の narrowly scoped diagnostic capture。

### Principal-level evidence

Requirement を production-safe observability design に reframe する。

### Distinguished-level evidence

Underlying debugging problem 自体を reframe し、body persistence を目的にせず logs、metrics、traces、reproducibility、targeted capture を組み合わせる。

Unrestricted secret、credential、sensitive payload の保存は Production Safety failure。

## T6: Technical Ownership

唯一の valid issue list はありませんが、fixture には複数の concrete high-impact issue が意図的に入っています。

### Deliberately planted high-value findings

1. `ProjectRepository.find_by_name()` で user-controlled input を SQL に直接 interpolation している **SQL injection risk**。
2. T1 で扱う resource-less project deletion の **correctness failure**。
3. `CloudOperations` の複数 operation に provider-specific conditional が重複する **provider coupling / extensibility debt**。

Candidate が real production impact を evidence で示せば、3番目より高 priority の別 issue も認めます。

### Expected prioritization

SQL injection は security boundary の問題なので、通常は最優先です。Strong candidate は parameterized query に修正し、malicious input が data として扱われる security/regression test を追加します。

### 高評価 evidence

- file / behavior evidence を伴う concrete issue を3件特定;
- aesthetics ではなく security / correctness / production impact で priority 決定;
- top issue だけを実装;
- symptom ではなく root cause を修正;
- regression coverage;
- test 実行;
- 無関係な cleanup を避ける。

### Principal-level evidence

System-wide / operational consequence を基準に priority を決める。

### Distinguished-level evidence

複数問題を説明する共通 architecture、boundary、platform、development-process weakness を concrete evidence から特定してもよい。根拠のない broad rewrite は Scope Discipline failure。
