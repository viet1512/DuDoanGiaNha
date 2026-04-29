"""Train a minimal sklearn Pipeline and save model1.joblib for local runs when no trained model exists."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

NUM_COLS = ["chieuDai", "chieuNgang", "dienTich", "Phongngu", "SoTang", "PhongTam"]
CAT_COLS = ["Loai", "GiayTo", "TinhTrangNoiThat", "Phuong"]


def main() -> None:
    rng = np.random.default_rng(0)
    n = 300
    X = pd.DataFrame(
        {
            "chieuDai": rng.uniform(5, 25, n),
            "chieuNgang": rng.uniform(3, 10, n),
            "dienTich": rng.uniform(25, 200, n),
            "Phongngu": rng.integers(1, 6, n),
            "SoTang": rng.uniform(1, 5, n),
            "PhongTam": rng.uniform(1, 5, n),
            "Loai": rng.choice(
                ["nhà ngõ, hẻm", "nhà mặt phố, mặt tiền", "nhà phố liền kề"], n
            ),
            "GiayTo": rng.choice(["đã có sổ", "không có sổ", "giấy tờ viết tay"], n),
            "TinhTrangNoiThat": rng.choice(
                ["bàn giao thô", "nội thất đầy đủ", "nội thất cao cấp"], n
            ),
            "Phuong": rng.choice(["phường tân tạo a", "phường khác"], n),
        }
    )
    y = X["dienTich"] * 40.0 + rng.normal(0, 200.0, n)

    num_pipe = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    cat_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value="unknown")),
            (
                "enc",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            ),
        ]
    )
    preprocessor = ColumnTransformer(
        [
            ("num", num_pipe, NUM_COLS),
            ("cat", cat_pipe, CAT_COLS),
        ]
    )
    reg = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=30, random_state=0)),
        ]
    )
    reg.fit(X, y)

    out = Path(__file__).resolve().parents[1] / "model1.joblib"
    dump(reg, out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
