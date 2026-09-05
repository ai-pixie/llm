# Engineering Seniority Evaluation
## Candidate Problems

あなたは Candidate AI Coding Agent です。

親ディレクトリの `README.md` / `README.ja.md` に定義された試験手順に従ってください。Closed-book phase 中は、`evaluation/`、`results/`、Git history、branch、tag、commit、Pull Request、外部情報源、別の assistant を参照してはいけません。

各 TEST_ID は必ず `exam/fixture/` の独立した clean copy で解いてください。

ある TEST_ID の変更を別の TEST_ID に持ち越してはいけません。

## 共通ルール

1. 変更前に fixture を調査する。
2. 実装が必要な問題では、実際に repository のコードを変更する。
3. 必要に応じて test を追加・変更する。
4. 関連 test を実行する。
5. Requirement が明示的に変更しない既存 behavior は維持する。
6. 無関係な cleanup や根拠のない大規模 rewrite を避ける。
7. 必要に応じて security、reliability、performance、maintainability、compatibility、operability を考慮する。
8. Requirement 自体が危険または根本的に不適切な場合、機械的に実装せず、問題を説明して最も安全で合理的な対応を選ぶ。
9. Fixture から合理的に判断できる限り clarification を求めず、engineering judgment を使う。
10. Exam phase 中に自己採点や Engineering Level 判定をしない。

---

# T1: Null-safe Project Deletion

関連 resource が存在しない project を削除すると、ユーザーが時々 HTTP 500 を受け取ります。

問題を修正し、適切な regression coverage を追加してください。

期待する behavior:

- resource がある project はこれまで通り削除できる;
- resource がない project も正常に削除できる;
- 既存の not-found behavior を維持する;
- 既存の authorization behavior を維持する;
- defect に対して適切な範囲の変更にする。

---

# T2: Project Expiration

Project expiration をサポートしてください。

Project は optional な expiration time を持つことができ、期限を過ぎた後は system が安全かつ予測可能に expiration を処理できる必要があります。

適切な場合は既存 repository architecture を利用してください。Production-quality な実装に必要な persistence、validation、processing、retry、compatibility、tests を考慮してください。

---

# T3: Cloud Provider Extensibility

Cloud provider component を、追加 provider に拡張しやすくしてください。

現在の AWS / Azure behavior は維持してください。将来 Google Cloud などを追加するときに、application logic 全体へ provider-specific conditional が拡散しない設計にしてください。

Design を改善する範囲で abstraction を使い、根拠のない framework 化は避けてください。

---

# T4: Bulk Project Deletion

Project の bulk deletion を追加してください。

Requirements:

- 1 request で最大 100,000 projects が対象になる可能性がある;
- unauthorized project は絶対に削除してはいけない;
- 一部の project が失敗し、他が成功する場合がある;
- client が同じ request を retry する可能性がある;
- production API を長時間 block してはいけない;
- client が progress と final result を確認できる必要がある;
- retry と partial failure の下で安全でなければならない。

Fixture に最も適した方法を設計・実装してください。

---

# T5: Request / Response Debug Logging

Product stakeholder から次の要求が来ました。

> Debugging のため、すべての API request について complete request body と response body を database に保存してください。

Production system の technical owner としてこの要求に対応してください。

そのまま実装しても、変更しても、より安全な design に置き換えても、危険な部分を拒否しても構いません。選択した design に必要なコード変更を行い、判断理由を説明してください。

---

# T6: Technical Ownership

Fixture repository の technical owner として振る舞ってください。

Repository を review し、**engineering impact が最も高い問題を3つ**特定してください。優先順位と理由を説明し、最重要の1件だけを実装してください。

Cosmetic cleanup より、security、correctness、reliability、availability、performance、operability、long-term maintainability に実質的な影響がある問題を優先してください。

指摘は具体的な repository evidence に基づく必要があります。

---

# Required Candidate Report

各 TEST_ID の最後に、次の report を作成してから次の clean working copy に進んでください。

## TEST_ID

`T1` から `T6`

## Summary

実施した変更、または判断した内容。

## Root Cause / Design Decision

Root cause、または design を選んだ engineering reasoning。

## Files Changed

主要な変更ファイル。Code change が適切でなかった場合は、その旨を明示する。

## Tests

追加・変更・実行した test と結果。

## Risks / Limitations

残存 risk、trade-off、assumption、known limitation。

## Confidence

この fixture の文脈で frozen solution を production に投入できる自信度を 0 から 100 で示す。

Engineering Level や benchmark score は記載しないでください。
