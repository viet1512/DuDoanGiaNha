from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

import yaml

from services.config import settings


class RuleEngine:
    def __init__(self, rules_path: str | None = None) -> None:
        root_dir = Path(__file__).resolve().parents[1]
        resolved_path = Path(rules_path) if rules_path else Path(settings.rules_path)
        if not resolved_path.is_absolute():
            resolved_path = root_dir / resolved_path
        self.rules_path = resolved_path
        self.rules: List[Dict[str, Any]] = []
        self.reload_rules()

    def reload_rules(self) -> None:
        with open(self.rules_path, "r", encoding="utf-8") as file:
            parsed = yaml.safe_load(file) or {}
        self.rules = parsed.get("rules", [])

    def get_rules(self) -> List[Dict[str, Any]]:
        return deepcopy(self.rules)

    def _evaluate_condition(self, facts: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        field = condition["field"]
        op = condition["op"]
        value = condition["value"]
        fact_value = facts.get(field)

        if op == "eq":
            return fact_value == value
        if op == "neq":
            return fact_value != value
        if op == "gt":
            return float(fact_value) > float(value)
        if op == "gte":
            return float(fact_value) >= float(value)
        if op == "lt":
            return float(fact_value) < float(value)
        if op == "lte":
            return float(fact_value) <= float(value)
        if op == "in":
            return fact_value in value
        if op == "contains":
            return isinstance(fact_value, str) and str(value) in fact_value
        return False

    def _condition_match(self, facts: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        try:
            return self._evaluate_condition(facts, condition)
        except (TypeError, ValueError):
            return False

    def infer(self, base_facts: Dict[str, Any], max_iterations: int = 5) -> Dict[str, Any]:
        working_memory = dict(base_facts)
        fired_rules: List[Dict[str, Any]] = []
        derived_facts: Dict[str, Any] = {}
        adjustment_events: List[Dict[str, Any]] = []
        warnings: List[str] = []

        available_rules = sorted(
            [rule for rule in self.rules if rule.get("enabled", True)],
            key=lambda item: (item.get("priority", 999), -item.get("confidence", 0.0)),
        )
        fired_ids = set()

        for _ in range(max_iterations):
            changed = False
            for rule in available_rules:
                if rule["id"] in fired_ids:
                    continue

                conditions = rule.get("if", [])
                if all(self._condition_match(working_memory, condition) for condition in conditions):
                    fired_ids.add(rule["id"])
                    fired_rules.append(
                        {
                            "id": rule["id"],
                            "description": rule["description"],
                            "weight": rule.get("weight", 0.0),
                            "confidence": rule.get("confidence", 0.0),
                            "priority": rule.get("priority", 999),
                            "source": rule.get("source", "unknown"),
                        }
                    )

                    then_obj = rule.get("then", {})
                    for key, value in then_obj.items():
                        if key == "price_adjustment_percent":
                            adjustment_events.append(
                                {
                                    "rule_id": rule["id"],
                                    "description": rule["description"],
                                    "weight": float(value),
                                    "confidence": float(rule.get("confidence", 1.0)),
                                }
                            )
                        elif key == "warning":
                            warnings.append(str(value))
                        else:
                            if working_memory.get(key) != value:
                                working_memory[key] = value
                                derived_facts[key] = value
                                changed = True

            if not changed:
                break

        weighted_adjustment = 0.0
        for event in adjustment_events:
            weighted_adjustment += event["weight"] * event["confidence"]

        risk_level = working_memory.get("risk_level", "medium")
        liquidity_level = working_memory.get("liquidity_level", "medium")

        return {
            "fired_rules": fired_rules,
            "derived_facts": derived_facts,
            "price_adjustment_percent": round(weighted_adjustment, 4),
            "adjustment_breakdown": adjustment_events,
            "risk_level": risk_level,
            "liquidity_level": liquidity_level,
            "warnings": warnings,
            "working_memory": working_memory,
        }
