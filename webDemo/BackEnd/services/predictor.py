from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd
from joblib import load

from services.config import settings


class PredictorService:
    """Wraps ML model inference for housing price prediction."""

    FEATURE_ORDER = [
        "chieuDai",
        "chieuNgang",
        "dienTich",
        "Phongngu",
        "SoTang",
        "PhongTam",
        "Loai",
        "GiayTo",
        "TinhTrangNoiThat",
        "Phuong",
    ]

    def __init__(self, model_path: str | None = None) -> None:
        root_dir = Path(__file__).resolve().parents[1]
        resolved_model_path = Path(model_path) if model_path else Path(settings.model_path)
        if not resolved_model_path.is_absolute():
            resolved_model_path = root_dir / resolved_model_path
        self.model = load(resolved_model_path)

    def predict_price(self, facts: Dict[str, Any]) -> float:
        row = {feature: facts.get(feature) for feature in self.FEATURE_ORDER}
        features = pd.DataFrame([row])
        prediction_log = self.model.predict(features)[0]
        prediction_vnd = np.expm1(prediction_log)
        return float(prediction_vnd)
