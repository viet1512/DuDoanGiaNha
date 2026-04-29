from __future__ import annotations

from typing import Any, Dict, List


def build_explanations(ml_result: Dict[str, Any], rule_result: Dict[str, Any]) -> Dict[str, Any]:
    explanations: List[str] = []
    recommendations: List[str] = []

    for event in rule_result.get("adjustment_breakdown", []):
        sign = "tăng" if event["weight"] >= 0 else "giảm"
        explanations.append(
            f"Luật {event['rule_id']} kích hoạt: {event['description']} -> {sign} {abs(event['weight']):.2f}%."
        )

    risk_level = rule_result.get("risk_level", "medium")
    liquidity_level = rule_result.get("liquidity_level", "medium")

    if risk_level == "high":
        recommendations.append("Rủi ro cao: nên kiểm tra pháp lý kỹ trước khi quyết định.")
    elif risk_level == "medium":
        recommendations.append("Rủi ro trung bình: cần xác minh thêm thông tin quy hoạch và giấy tờ.")
    else:
        recommendations.append("Rủi ro thấp: hồ sơ phù hợp cho bước thẩm định tiếp theo.")

    if liquidity_level == "low":
        recommendations.append("Thanh khoản thấp: cân nhắc biên độ đàm phán giá rộng hơn.")
    elif liquidity_level == "high":
        recommendations.append("Thanh khoản cao: có thể ra quyết định nhanh hơn nếu pháp lý rõ ràng.")

    if not explanations:
        explanations.append("Không có luật điều chỉnh đặc biệt, hệ thống giữ gần mức giá ML nền.")

    return {
        "explanations": explanations,
        "recommendations": recommendations,
        "summary": {
            "ml_price": ml_result["ml_price"],
            "final_price": ml_result["final_price"],
            "adjustment_percent": ml_result["adjustment_percent"],
            "risk_level": risk_level,
            "liquidity_level": liquidity_level,
        },
    }
