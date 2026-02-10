"""Regression coverage for non-root invocation of README consistency check."""

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Callable, ContextManager, Iterator

ROOT = Path(__file__).resolve().parents[1]
CHECK_SCRIPT = ROOT / "tests" / "check_readme_consistency.py"
SUCCESS_MESSAGE = "README output example matches GREETING constant"
TEMP_DIR_PREFIX = "readme-non-root-"


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


@dataclass(frozen=True)
class NonRootScenario:
    name: str
    cwd_provider: Callable[[], ContextManager[Path]]


def build_non_root_scenarios() -> tuple[NonRootScenario, ...]:
    return (
        NonRootScenario(name="tests subdirectory", cwd_provider=tests_subdirectory_cwd),
        NonRootScenario(
            name="temporary subdirectory",
            cwd_provider=temporary_subdirectory_cwd,
        ),
    )


@contextmanager
def tests_subdirectory_cwd() -> Iterator[Path]:
    yield ROOT / "tests"


@contextmanager
def temporary_subdirectory_cwd() -> Iterator[Path]:
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=TEMP_DIR_PREFIX) as temp_dir:
        temp_dir_name = Path(temp_dir).name
        if not temp_dir_name.startswith(TEMP_DIR_PREFIX):
            raise SystemExit(
                "Temporary directory name does not preserve expected prefix.\n"
                f"temp_dir: {temp_dir}\n"
                f"expected_prefix: {TEMP_DIR_PREFIX}"
            )
        yield Path(temp_dir)


def main() -> None:
    for scenario in build_non_root_scenarios():
        with scenario.cwd_provider() as cwd:
            run_check_from(cwd, scenario.name)


if __name__ == "__main__":
    main()
