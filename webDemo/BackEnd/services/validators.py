from __future__ import annotations

import math
from typing import Any, Dict, Tuple


REQUIRED_FIELDS = {
    "chieuDai": (int, float),
    "chieuNgang": (int, float),
    "dienTich": (int, float),
    "Phongngu": (int, float),
    "SoTang": (int, float),
    "PhongTam": (int, float),
    "Loai": (str,),
    "GiayTo": (str,),
    "TinhTrangNoiThat": (str,),
    "Phuong": (str,),
}

TEXT_FIELDS = ("Loai", "GiayTo", "TinhTrangNoiThat", "Phuong")
NUMERIC_FIELDS = ("chieuDai", "chieuNgang", "dienTich", "Phongngu", "SoTang", "PhongTam")

# Frontend aliases mapped to backend canonical feature names.
FIELD_ALIASES = {
    "chieu_dai": "chieuDai",
    "chieu_ngang": "chieuNgang",
    "dien_tich": "dienTich",
    "phong_ngu": "Phongngu",
    "so_tang": "SoTang",
    "phong_tam": "PhongTam",
    "loai": "Loai",
    "giay_to": "GiayTo",
    "tinh_trang_noi_that": "TinhTrangNoiThat",
    "phuong": "Phuong",
}


def normalize_facts(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(data)
    for alias, canonical in FIELD_ALIASES.items():
        if alias in normalized and canonical not in normalized:
            normalized[canonical] = normalized[alias]

    for key in TEXT_FIELDS:
        if key in normalized and isinstance(normalized[key], str):
            normalized[key] = normalized[key].strip()
    return normalized


def validate_predict_payload(data: Dict[str, Any]) -> Tuple[bool, str]:
    for alias, canonical in FIELD_ALIASES.items():
        if alias in data and canonical not in data:
            data[canonical] = data[alias]

    for field, accepted_types in REQUIRED_FIELDS.items():
        if field not in data:
            return False, f"Missing required field: {field}"

        value = data[field]
        if value is None:
            return False, f"Field {field} cannot be null"

        if not isinstance(value, accepted_types):
            return False, f"Field {field} has invalid type"

        if field in TEXT_FIELDS and not str(value).strip():
            return False, f"Field {field} cannot be empty"

        if field in NUMERIC_FIELDS:
            if isinstance(value, bool):
                return False, f"Field {field} has invalid type"
            numeric_value = float(value)
            if not math.isfinite(numeric_value):
                return False, f"Field {field} must be a finite number"
            if numeric_value < 0:
                return False, f"Field {field} must be >= 0"

    return True, ""


def validate_rules_schema(rules: list[dict[str, Any]]) -> Tuple[bool, str]:
    required = {"id", "description", "priority", "weight", "confidence", "if", "then", "enabled"}
    for index, rule in enumerate(rules):
        missing = required - set(rule.keys())
        if missing:
            return False, f"Rule at index {index} missing keys: {', '.join(sorted(missing))}"
        if not isinstance(rule["if"], list):
            return False, f"Rule {rule['id']} field 'if' must be a list"
        if not isinstance(rule["then"], dict):
            return False, f"Rule {rule['id']} field 'then' must be an object"
    return True, ""
