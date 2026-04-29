from __future__ import annotations

from typing import Any, Dict


def _resolve_margin_by_risk(risk_level: str | None) -> float:
    """Return margin ratio based on rule-engine risk level."""
    mapping = {
        "low": 0.08,
        "medium": 0.12,
        "high": 0.18,
    }
    return mapping.get((risk_level or "").lower(), 0.12)


def combine_ml_and_rules(ml_price: float, rule_result: Dict[str, Any]) -> Dict[str, Any]:
    adjustment_percent = float(rule_result.get("price_adjustment_percent", 0.0))
    factor = 1.0 + (adjustment_percent / 100.0)
    final_price = ml_price * factor

    # Confidence still depends on number of fired rules.
    fired_count = len(rule_result.get("fired_rules", []))
    system_confidence = min(0.95, 0.55 + fired_count * 0.04)

    # Price range width is controlled by risk level for clearer business explanation.
    risk_level = rule_result.get("risk_level")
    margin = _resolve_margin_by_risk(risk_level)
    min_price = final_price * (1.0 - margin)
    max_price = final_price * (1.0 + margin)

    return {
        "ml_price": round(ml_price, 2),
        "final_price": round(final_price, 2),
        "price_range": {"min": round(min_price, 2), "max": round(max_price, 2)},
        "adjustment_percent": round(adjustment_percent, 4),
        "system_confidence": round(system_confidence, 4),
    }
