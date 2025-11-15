# Find Bear

Python script that filters Minecraft player activity logs with Polars. You can
configure the dimension, coordinate/time window, watched items, input CSV, and
output path. Matching rows are written with ANSI colors so tools like `bat`
highlight red entries when an item of interest is found.

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (or another tool to install the
  `polars` dependency)

## Quick Start

1. Edit the configuration block near the top of `main.py` to match your
   dimension, coordinate/time ranges, target items, and file paths.
1. Install dependencies and run the script:

   ```bash
   uv run python main.py
   ```

1. Examine the saved output (default `output.txt`). Use `bat` or `less -R` to
   keep the red/blue ANSI colors:

   ```bash
   bat output.txt
   ```

## Output Format

Each line looks like:

```text
2025-11-14 19:12:33 | 玩家:shuiyu3299 | 坐标:(221.30, 64.75, 2610.06) | 物品:...
```

- Red line: at least one target item in the `物品` column.
- Blue line: no target items found.
- The terminal only prints the total number of saved rows, so the detailed log
  is kept solely in the output file.

## Development

- Type checking: `basedpyright`
- Formatting/linting: managed through `uv` and the `pyproject.toml`

## License

This project is released under the [MIT License](LICENSE).
