"""Regression coverage for non-root invocation of README consistency check."""

from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CHECK_SCRIPT = ROOT / "tests" / "check_readme_consistency.py"
SUCCESS_MESSAGE = "README output example matches GREETING constant"


def run_check_from(cwd: Path, scenario: str) -> None:
    # Run from a non-root cwd and verify the expected success output is preserved.
    result = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "README consistency check failed from non-root working directory.\n"
            f"scenario: {scenario}\n"
            f"cwd: {cwd}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    if SUCCESS_MESSAGE not in result.stdout:
        raise SystemExit(
            "README consistency check did not report expected success output "
            "from non-root working directory.\n"
            f"scenario: {scenario}\n"
            f"cwd: {cwd}"
        )

    print(f"README consistency check succeeds from non-root working directory ({scenario})")


def main() -> None:
    run_check_from(ROOT / "tests", "tests subdirectory")

    with tempfile.TemporaryDirectory(dir=ROOT, prefix="readme-non-root-") as temp_dir:
        temp_dir_name = Path(temp_dir).name
        if not temp_dir_name.startswith("readme-non-root-"):
            raise SystemExit(
                "Temporary directory name does not preserve expected prefix.\n"
                f"temp_dir: {temp_dir}\n"
                f"expected_prefix: readme-non-root-"
            )
        run_check_from(Path(temp_dir), "temporary subdirectory")


if __name__ == "__main__":
    main()
