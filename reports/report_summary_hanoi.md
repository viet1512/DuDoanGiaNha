# Bao cao tom tat - Du doan gia nha Ha Noi (Hybrid ML + KBS)

## 1) Muc tieu
- Xay dung he thong du doan gia nha theo huong lai (Hybrid):
  - ML du doan gia co so (`ml_price`)
  - KBS dieu chinh theo luat nghiep vu de tao gia cuoi (`final_price`)

## 2) Du lieu
- Du lieu tho: `data/raw/housing_raw_vn_hanoi_deep.csv`
- Du lieu clean: `data/processed/housing_hanoi_clean.csv`
- Quy mo:
  - Thu thap: 2000 ban ghi tho
  - Sau lam sach (pham vi 1 quan nhieu mau nhat): 258 ban ghi

## 3) Tien xu ly
- Chon 1 quan co nhieu mau nhat de giam nhieu dia ly.
- Xu ly missing:
  - Loai bo mau thieu cot bat buoc (`Gia`, `dienTich`)
  - Dien median cho bien so
  - Dien `Khong ro` cho bien phan loai
- Loc outlier theo mien gia tri hop ly cua gia/dien tich/so phong.

## 4) Huan luyen mo hinh
- Notebook: `notebooks/03_train_model_hanoi.ipynb`
- So sanh model:
  - Linear Regression
  - Random Forest
  - Gradient Boosting
- Tieu chi:
  - MAE
  - RMSE
  - R2
  - CV_RMSE

## 5) Ket qua model
- Model tot nhat: **RandomForest**
- Chi tiet metric: xem file `reports/metrics/model_comparison_hanoi.csv`
- Model luu de suy luan backend:
  - `webDemo/BackEnd/model1.joblib`

## 6) Tich hop Hybrid
- Backend route: `/predict`
- Output chinh:
  - `ml_price`
  - `final_price`
  - `price_range`
  - `adjustment_percent`
  - `fired_rules`
  - `warnings`
  - `recommendations`

## 7) Ghi chu bao ve
- ML tra gia tri diem (point prediction).
- Khoang gia (`price_range`) duoc tinh o lop suy luan hybrid, khong dat o buoc tien xu ly.
- Ly do: khoang gia phu thuoc vao ca ket qua ML va ket qua luat.
