"""doc-reader CLI entry. Runs under the private venv (see `setup`)."""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docread import env  # noqa: E402


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if argv and argv[0] == "setup":
        env.setup()
        return 0
    vpy = env.venv_python()
    if not vpy.exists():
        import importlib.util

        if importlib.util.find_spec("pymupdf4llm") is None:  # not already in a suitable env
            print("doc-reader is not set up. Run: python docread.py setup")
            return 2
    elif Path(sys.executable).resolve() != vpy.resolve():
        e = dict(os.environ, PYTHONUTF8="1")
        return subprocess.call([str(vpy), __file__, *argv], env=e)
    from docread import cli  # noqa: E402

    return cli.run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
