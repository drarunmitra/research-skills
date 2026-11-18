from pathlib import Path

from docread import env


def test_home_honours_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DOCREAD_HOME", str(tmp_path / "x"))
    assert env.home() == Path(tmp_path / "x")


def test_venv_python_is_scripts_exe():
    assert env.venv_python().as_posix().endswith("venv/Scripts/python.exe")
