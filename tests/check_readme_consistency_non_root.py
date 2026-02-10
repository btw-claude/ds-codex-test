"""Regression coverage for non-root invocation of README consistency check."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECK_SCRIPT = ROOT / "tests" / "check_readme_consistency.py"
SUCCESS_MESSAGE = "README output example matches GREETING constant"


def main() -> None:
    # Run from tests/ to ensure behavior is independent of current working dir.
    result = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT)],
        cwd=ROOT / "tests",
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "README consistency check failed from non-root working directory.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    if SUCCESS_MESSAGE not in result.stdout:
        raise SystemExit(
            "README consistency check did not report expected success output "
            "from non-root working directory."
        )

    print("README consistency check succeeds from non-root working directory")


if __name__ == "__main__":
    main()
