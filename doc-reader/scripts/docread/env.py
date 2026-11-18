"""Paths and venv bootstrap for doc-reader."""
import os
import subprocess
import sys
from pathlib import Path

PACKAGES = ["pymupdf4llm>=2.1", "pdfplumber>=0.11"]
DEV_PACKAGES = ["pytest>=8"]


def packages(dev: bool = False) -> list[str]:
    return PACKAGES + (DEV_PACKAGES if dev else [])


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


def setup(dev: bool = False) -> None:
    """Create the private venv and install the light dependencies."""
    if not venv_python().exists():
        print(f"creating venv at {venv_dir()}", flush=True)
        home().mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir())], check=True)
    pkgs = packages(dev)
    print("installing: " + " ".join(pkgs), flush=True)
    subprocess.run([str(venv_python()), "-m", "pip", "install", "-q", *pkgs], check=True)
    print("setup done", flush=True)
