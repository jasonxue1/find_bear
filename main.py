# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import polars as pl

# ---- Configurable section ----
INPUT_FILE = Path("data.csv")
OUTPUT_FILE = Path("output.txt")
DIMENSION = "主世界"
X_RANGE = (-2000.0, 2000.0)
Y_RANGE = (-60.0, 300.0)
Z_RANGE = (-4000.0, 4000.0)
TIME_RANGE = (
    datetime.fromisoformat("2025-11-14 19:12:30"),
    datetime.fromisoformat("2025-11-15 21:14:00"),
)
TARGET_ITEMS = [
    "shulker_box",
]
# ---- End of config ----

RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


def load_data() -> pl.DataFrame:
    df = pl.read_csv(INPUT_FILE, try_parse_dates=False)
    # First column may contain BOM, normalize column name
    first_col = df.columns[0]
    if first_col != "时间":
        df = df.rename({first_col: "时间"})

    return df.with_columns(
        pl.col("时间")
        .cast(pl.Utf8)
        .str.strip_chars()
        .str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S", strict=False),
        pl.col("物品").fill_null("").str.to_lowercase().alias("物品"),
    )


def main():
    df = load_data()
    filtered = df.filter(
        (pl.col("维度") == DIMENSION)
        & pl.col("X").is_between(*X_RANGE, closed="both")
        & pl.col("Y").is_between(*Y_RANGE, closed="both")
        & pl.col("Z").is_between(*Z_RANGE, closed="both")
        & pl.col("时间").is_between(*TIME_RANGE, closed="both")
    ).with_columns(
        # Color logic: row is red if it contains ANY of the target items.
        # Replace pl.any_horizontal with pl.all_horizontal to require all items.
        pl.any_horizontal(
            [
                pl.col("物品").str.contains(item.lower(), literal=True)
                for item in TARGET_ITEMS
            ]
        ).alias("has_target_item")
    )

    output_lines: list[str] = []
    for row in filtered.iter_rows(named=True):
        color = RED if row["has_target_item"] else BLUE
        plain_line = f"{row['时间']} | 玩家:{row['玩家']} | 坐标:({row['X']:.2f}, {row['Y']:.2f}, {row['Z']:.2f}) | 物品:{row['物品']}"
        output_lines.append(f"{color}{plain_line}{RESET}")

    # Persist ANSI-colored text so tools like bat retain red/blue highlighting
    _ = OUTPUT_FILE.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Saved {len(output_lines)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
