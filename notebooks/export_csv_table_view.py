from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data" / "processed" / "housing_hanoi_clean.csv"
    output_dir = project_root / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)

    # Export full data to Excel for easy filtering/sorting.
    excel_path = output_dir / "housing_hanoi_clean.xlsx"
    df.to_excel(excel_path, index=False)

    # Export a styled HTML preview for quick inspection in browser.
    preview_rows = min(300, len(df))
    html_path = output_dir / "housing_hanoi_clean_preview.html"
    html_table = (
        df.head(preview_rows)
        .style.set_sticky(axis="index")
        .set_table_styles(
            [
                {"selector": "th", "props": [("background-color", "#f3f4f6")]},
                {"selector": "td, th", "props": [("padding", "6px 10px")]},
            ]
        )
        .to_html()
    )

    html_doc = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <title>Housing Hanoi Clean Preview</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1 {{ margin-bottom: 8px; }}
    p {{ color: #4b5563; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid #e5e7eb; border-radius: 8px; }}
    table {{ border-collapse: collapse; width: max-content; min-width: 100%; }}
  </style>
</head>
<body>
  <h1>Housing Hanoi Clean - Preview ({preview_rows} dong)</h1>
  <p>File goc: {csv_path}</p>
  <div class="table-wrap">
    {html_table}
  </div>
</body>
</html>
"""
    html_path.write_text(html_doc, encoding="utf-8")

    print(f"Done. Excel: {excel_path}")
    print(f"Done. HTML preview: {html_path}")


if __name__ == "__main__":
    main()
