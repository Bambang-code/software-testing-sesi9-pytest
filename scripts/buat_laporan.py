"""Jalankan suite dan simpan laporan aktual; exit code mengikuti PyTest."""

from pathlib import Path
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    folder_laporan = root / "laporan"
    folder_laporan.mkdir(exist_ok=True)
    perintah = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--cov=perpustakaan",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=html:laporan/html",
        "--cov-report=json:laporan/coverage.json",
        "--color=no",
    ]
    hasil = subprocess.run(
        perintah,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    (folder_laporan / "hasil-pytest.txt").write_text(hasil.stdout, encoding="utf-8")
    print(hasil.stdout, end="")
    return hasil.returncode


if __name__ == "__main__":
    raise SystemExit(main())
