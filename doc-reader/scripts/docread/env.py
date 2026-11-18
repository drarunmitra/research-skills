"""Paths and venv bootstrap for doc-reader."""
import os
import subprocess
import sys
from pathlib import Path

PACKAGES = ["pymupdf4llm", "pdfplumber", "pytest"]


def home() -> Path:
    override = os.environ.get("DOCREAD_HOME")
    if override:
        return Path(override)
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / ".local" / "share")
    return Path(base) / "doc-reader"


def venv_dir() -> Path:
    return home() / "venv"


def venv_python() -> Path:
    sub = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    return venv_dir() / sub


def setup() -> None:
    """Create the private venv and install the light dependencies."""
    if not venv_python().exists():
        print(f"creating venv at {venv_dir()}", flush=True)
        home().mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir())], check=True)
    print("installing: " + " ".join(PACKAGES), flush=True)
    subprocess.run(
        [str(venv_python()), "-m", "pip", "install", "-q", *PACKAGES], check=True
    )
    print("setup done", flush=True)
