from pathlib import Path
import csv


PROJECT_DIR = Path.cwd()
OUTPUT_DIR = PROJECT_DIR / "output"
REPORT_FILE = OUTPUT_DIR / "rapport_chiffre_affaires.xlsx"
PODIUM_PREMIUM_FILE = OUTPUT_DIR / "vins_premium.csv"
PODIUM_ORDINARY_FILE = OUTPUT_DIR / "vins_ordinaires.csv"


required_files = [REPORT_FILE, PODIUM_PREMIUM_FILE, PODIUM_ORDINARY_FILE]
missing_files = [str(path) for path in required_files if not path.exists()]
if missing_files:
	raise ValueError(f"Missing output files: {missing_files}")

with PODIUM_PREMIUM_FILE.open(newline="", encoding="utf-8") as premium_handle:
	premium_count = sum(1 for _ in csv.reader(premium_handle)) - 1

with PODIUM_ORDINARY_FILE.open(newline="", encoding="utf-8") as ordinary_handle:
	ordinary_count = sum(1 for _ in csv.reader(ordinary_handle)) - 1

if premium_count != 30:
	raise ValueError(f"Expected 30 premium wines, got {premium_count}")

if ordinary_count != 684:
	raise ValueError(f"Expected 684 ordinary wines, got {ordinary_count}")

print(f"Validation OK: premium={premium_count}, ordinaires={ordinary_count}")