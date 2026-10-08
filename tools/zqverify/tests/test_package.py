"""The verifier runs as the package `zqverify` on the CPython that tools/py pins."""

import sys
from pathlib import Path

import zqverify

HERE = Path(__file__).resolve().parent


def test_runs_on_the_pinned_cpython() -> None:
    pinned = (HERE.parents[1] / "py" / ".python-version").read_text(encoding="utf-8").strip()
    assert sys.implementation.name == "cpython"
    assert ".".join(map(str, sys.version_info[:3])) == pinned


def test_imports_this_directory_as_zqverify() -> None:
    assert zqverify.__name__ == "zqverify"
    assert Path(zqverify.__file__).resolve().parent == HERE.parent
