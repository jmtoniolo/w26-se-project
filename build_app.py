import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

def run_pyinstaller():
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "iOSDesktop",

        # hidden imports (adjust if needed)
        "--hidden-import", "django",
        "--hidden-import", "django.core.management",
        "--hidden-import", "django.contrib.sessions",
        "--hidden-import", "django.contrib.messages",
        "--hidden-import", "django.contrib.staticfiles",

        # data files (Windows uses ';')
        "--add-data", "db.sqlite3;.",
        "--add-data", "inventory_optimization_software\\templates;inventory_optimization_software\\templates",

        "run_app.py",
    ]

    print("Running PyInstaller...")
    result = subprocess.run(pyinstaller_cmd, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print("Build failed.")
        sys.exit(result.returncode)

    print("\nBuild complete.")
    print("Output:", PROJECT_ROOT / "dist" / "iOSDesktop.exe")


if __name__ == "__main__":
    run_pyinstaller()