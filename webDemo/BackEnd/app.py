from __future__ import annotations

import json
import logging
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from services.explainer import build_explanations
from services.config import settings
from services.predictor import PredictorService
from services.rule_engine import RuleEngine
from services.scorer import combine_ml_and_rules
from services.validators import normalize_facts, validate_predict_payload, validate_rules_schema

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kbs-backend")

predictor = PredictorService()
rule_engine = RuleEngine()


@app.route("/health", methods=["GET"])
def health() -> tuple[dict, int]:
    return {"status": "ok"}, 200


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True) or {}
    valid, message = validate_predict_payload(payload)
    if not valid:
        return jsonify({"error": message}), 400

    facts = normalize_facts(payload)
    ml_price = predictor.predict_price(facts)
    rule_result = rule_engine.infer(facts)
    ml_result = combine_ml_and_rules(ml_price, rule_result)
    explanation_result = build_explanations(ml_result, rule_result)

    response = {
        "ml_price": ml_result["ml_price"],
        "final_price": ml_result["final_price"],
        "price_range": ml_result["price_range"],
        "system_confidence": ml_result["system_confidence"],
        "adjustment_percent": ml_result["adjustment_percent"],
        "adjustment_breakdown": rule_result["adjustment_breakdown"],
        "risk_level": rule_result["risk_level"],
        "liquidity_level": rule_result["liquidity_level"],
        "warnings": rule_result["warnings"],
        "explanations": explanation_result["explanations"],
        "recommendations": explanation_result["recommendations"],
        "fired_rules": rule_result["fired_rules"],
        "derived_facts": rule_result["derived_facts"],
    }
    return jsonify(response), 200


@app.route("/rules", methods=["GET"])
def get_rules():
    return jsonify({"rules": rule_engine.get_rules()}), 200


@app.route("/rules/validate", methods=["POST"])
def validate_rules():
    payload = request.get_json(silent=True) or {}
    rules = payload.get("rules")
    if rules is None or not isinstance(rules, list):
        return jsonify({"valid": False, "message": "Payload must include 'rules' array."}), 400

    valid, message = validate_rules_schema(rules)
    status = 200 if valid else 400
    return jsonify({"valid": valid, "message": message}), status


@app.route("/rules/reload", methods=["POST"])
def reload_rules():
    try:
        rule_engine.reload_rules()
        logger.info("Rules reloaded successfully.")
        return jsonify({"reloaded": True, "rules_count": len(rule_engine.get_rules())}), 200
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Rule reload failed")
        return jsonify({"reloaded": False, "error": str(exc)}), 500


@app.route("/simulate", methods=["POST"])
def simulate():
    payload = request.get_json(silent=True) or {}
    facts = payload.get("facts", payload)
    valid, message = validate_predict_payload(facts)
    if not valid:
        return jsonify({"error": message}), 400

    normalized = normalize_facts(facts)
    result = rule_engine.infer(normalized)
    return jsonify(result), 200


@app.route("/rules/schema", methods=["GET"])
def get_rule_schema():
    schema_path = Path(__file__).resolve().parent / "knowledge" / "schema.json"
    with open(schema_path, "r", encoding="utf-8") as file:
        schema = json.load(file)
    return jsonify(schema), 200


if __name__ == "__main__":
    app.run(debug=settings.debug)
