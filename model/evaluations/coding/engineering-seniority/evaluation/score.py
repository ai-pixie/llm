from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
RUBRIC = json.loads((ROOT / "rubric.json").read_text())
LEVEL_ORDER = ["Below Senior", "Senior", "Staff", "Principal", "Distinguished"]


def weighted_test_score(tests: dict[str, dict[str, object]]) -> float:
    total = 0.0
    for test_id, weight in RUBRIC["test_weights"].items():
        total += float(tests[test_id]["score"]) * float(weight)
    return total


def weighted_category_score(
    tests: dict[str, dict[str, object]],
    category: str,
) -> float:
    total = 0.0
    for test_id, weight in RUBRIC["test_weights"].items():
        category_scores = tests[test_id]["categories"]
        total += float(category_scores[category]) * float(weight)
    return total


def cap_level(level: str, maximum: str) -> str:
    return LEVEL_ORDER[min(LEVEL_ORDER.index(level), LEVEL_ORDER.index(maximum))]


def initial_level(score: float) -> str:
    if score < 40:
        return "Below Senior"
    if score < 60:
        return "Senior"
    if score < 75:
        return "Staff"
    if score < 90:
        return "Principal"
    return "Distinguished"


def evaluate(data: dict[str, object]) -> dict[str, object]:
    if data.get("exam_integrity") != "PASS":
        return {
            "valid": False,
            "result": "INVALID",
            "reason": "Exam Integrity did not PASS",
            "engineering_level": None,
        }

    tests = data["tests"]
    expected = set(RUBRIC["test_weights"])
    missing = expected - set(tests)
    if missing:
        raise ValueError(f"missing test scores: {', '.join(sorted(missing))}")

    for test_id in sorted(expected):
        test = tests[test_id]
        categories = test["categories"]
        missing_categories = set(RUBRIC["category_max"]) - set(categories)
        if missing_categories:
            raise ValueError(
                f"{test_id} missing categories: {', '.join(sorted(missing_categories))}"
            )
        for category, maximum in RUBRIC["category_max"].items():
            value = float(categories[category])
            if value < 0 or value > float(maximum):
                raise ValueError(
                    f"{test_id}.{category}={value} is outside 0..{maximum}"
                )
        category_total = sum(float(categories[name]) for name in RUBRIC["category_max"])
        reported_score = float(test["score"])
        if abs(category_total - reported_score) > 0.001:
            raise ValueError(
                f"{test_id} score {reported_score} does not equal category total {category_total}"
            )

    raw_score = weighted_test_score(tests)
    critical = any(bool(tests[test_id].get("critical_failure")) for test_id in expected)
    final_score = raw_score
    if critical:
        final_score = min(final_score, float(RUBRIC["critical_failure"]["overall_score_cap"]))

    aggregates = {
        category: weighted_category_score(tests, category)
        for category in RUBRIC["category_max"]
    }

    level = initial_level(final_score)

    if level != "Below Senior":
        if float(tests["T1"]["score"]) < float(RUBRIC["gates"]["senior"]["minimum_t1_score"]):
            level = "Below Senior"

    if LEVEL_ORDER.index(level) >= LEVEL_ORDER.index("Staff"):
        t2_t3_average = (float(tests["T2"]["score"]) + float(tests["T3"]["score"])) / 2
        if t2_t3_average < float(RUBRIC["gates"]["staff"]["minimum_t2_t3_average"]):
            level = "Senior"

    if LEVEL_ORDER.index(level) >= LEVEL_ORDER.index("Principal"):
        gates = RUBRIC["gates"]["principal"]
        t4_t5_t6_average = sum(float(tests[t]["score"]) for t in ("T4", "T5", "T6")) / 3
        principal_ok = (
            aggregates["architecture_design"] >= float(gates["minimum_architecture_design"])
            and aggregates["production_safety"] >= float(gates["minimum_production_safety"])
            and aggregates["engineering_judgment"] >= float(gates["minimum_engineering_judgment"])
            and t4_t5_t6_average >= float(gates["minimum_t4_t5_t6_average"])
            and not critical
        )
        if not principal_ok:
            level = "Staff"

    if level == "Distinguished":
        gates = RUBRIC["gates"]["distinguished"]
        distinguished_ok = (
            aggregates["architecture_design"] >= float(gates["minimum_architecture_design"])
            and aggregates["production_safety"] >= float(gates["minimum_production_safety"])
            and aggregates["engineering_judgment"] >= float(gates["minimum_engineering_judgment"])
            and float(tests["T5"]["score"]) >= float(gates["minimum_t5_score"])
            and float(tests["T6"]["score"]) >= float(gates["minimum_t6_score"])
            and bool(data.get("system_level_insight"))
            and not critical
        )
        if not distinguished_ok:
            level = "Principal"
            principal_gates = RUBRIC["gates"]["principal"]
            t4_t5_t6_average = sum(float(tests[t]["score"]) for t in ("T4", "T5", "T6")) / 3
            principal_ok = (
                aggregates["architecture_design"] >= float(principal_gates["minimum_architecture_design"])
                and aggregates["production_safety"] >= float(principal_gates["minimum_production_safety"])
                and aggregates["engineering_judgment"] >= float(principal_gates["minimum_engineering_judgment"])
                and t4_t5_t6_average >= float(principal_gates["minimum_t4_t5_t6_average"])
                and not critical
            )
            if not principal_ok:
                level = "Staff"

    if critical:
        level = cap_level(level, RUBRIC["critical_failure"]["maximum_level"])

    return {
        "valid": True,
        "raw_weighted_score": round(raw_score, 2),
        "final_weighted_score": round(final_score, 2),
        "engineering_level": level,
        "critical_failure": critical,
        "weighted_category_scores": {key: round(value, 2) for key, value in aggregates.items()},
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python evaluation/score.py /path/to/result.json")

    path = Path(sys.argv[1])
    data = json.loads(path.read_text())
    print(json.dumps(evaluate(data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
