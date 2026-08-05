from pathlib import Path
import shutil


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
OUTPUT_DIR = PROJECT_DIR / "output"


shutil.rmtree(WORK_DIR, ignore_errors=True)
shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)