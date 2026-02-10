"""Verify that README output example matches the greeting source of truth."""

from pathlib import Path
import sys

# Keep import behavior consistent for local runs and CI regardless of script path.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from greeting import GREETING


def main() -> None:
    readme = (ROOT / "README.md").read_text()
    expected_block = f"This will output:\n```\n{GREETING}\n```"
    if expected_block not in readme:
        raise SystemExit(
            "README output example does not match greeting source of truth"
        )
    print("README output example matches GREETING constant")


if __name__ == "__main__":
    main()
