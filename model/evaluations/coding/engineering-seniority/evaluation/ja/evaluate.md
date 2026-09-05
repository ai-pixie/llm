# Engineering Seniority Evaluation
## Evaluator Instructions

このファイルは、Candidate が選択された全テストを完了し、次を正確に出力するまで参照禁止です。

```text
EXAM COMPLETE
```

それ以降は、freeze された Candidate submission だけを評価してください。

## 評価原則

1. Answer Key 解禁後に Candidate code を変更しない。
2. Diff、tests、command output、frozen Candidate Report という observable evidence を採点する。
3. `EXAM COMPLETE` より前に実装・記録されていない「意図」には点を与えない。
4. Reference approach と完全一致する必要はない。同等以上に correct、safe、maintainable で fixture に適した別解は満点を認める。
5. Hidden tests は補助 evidence であり、implementation specification ではない。
6. 無関係な cleanup、speculative framework、問題規模に不釣り合いな rewrite は減点する。
7. Production safety の重大問題は Critical Failure として別扱いする。
8. Candidate の Confidence 自己申告値を採点 evidence に使わない。
9. Exam Integrity が FAIL の場合、評価全体を `INVALID` とし Engineering Level を付与しない。

## Test ごとの採点

各 test は 0 から 100 点。

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

期待 behavior と高評価 evidence は `answer-key.md` の該当 TEST_ID を使用してください。

## Critical Failure

Frozen submission が以下のような重大な production problem を導入または容認した場合、`Critical Failure: Yes` とします。

- authorization bypass;
- security boundary の破壊;
- 明確な data loss / corruption risk;
- secret、credential、無制限な sensitive data の unsafe storage;
- 既存 critical behavior の破壊;
- relevant test が失敗していると分かっていながら production-ready と判断。

Selected test のどれかに Critical Failure がある場合:

- その test の Production Safety は最大 3/10;
- overall weighted score は最大 69/100;
- Principal / Distinguished は不可。

## Overall score

`results/result-template.json` に従って score JSON を作り、次を実行します。

```bash
python evaluation/score.py /path/to/result.json
```

Script は `evaluation/rubric.json` の weight と capability gate を適用します。

## Engineering Levels

### Below Senior

明確に scope された implementation task を安定して完了できない。

### Senior

**Can implement.**

既存 repository の明確な問題を理解し、correct で tested な変更を実装できる。

### Staff

**Can design.**

Ambiguity を解消し、適切な abstraction を選び、複数 component にまたがる変更を安全に実装できる。

### Principal

**Can own the system.**

System-wide impact、architecture、migration、reliability、operability、production risk を考慮できる。

### Distinguished

**Can redefine the system.**

Requirement や system boundary 自体が誤った problem definition である場合、それを repository evidence に基づくより良い system-level design に置き換えられる。

コード量や abstraction の多さだけで上位 level にはなりません。

## Final evaluator output

`results/result-template.md` を使用し、主要 judgment には具体的 evidence を示してください。
