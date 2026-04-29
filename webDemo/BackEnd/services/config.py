from __future__ import annotations

import os
from pathlib import Path


class Settings:
    def __init__(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.model_path = os.getenv("MODEL_PATH", str(root / "model1.joblib"))
        self.rules_path = os.getenv("RULES_PATH", str(root / "knowledge" / "rules.yaml"))
        self.debug = os.getenv("FLASK_DEBUG", "1") == "1"


settings = Settings()
