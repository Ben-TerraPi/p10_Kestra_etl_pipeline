from pathlib import Path

import pandas as pd


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
OUTPUT_DIR = PROJECT_DIR / "output"
PREMIUM_FILE = WORK_DIR / "vins_premium.csv"
ORDINARY_FILE = WORK_DIR / "vins_ordinaires.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# lecture des fichiers
vins_premium = pd.read_csv(PREMIUM_FILE)
vins_ordinaires = pd.read_csv(ORDINARY_FILE)

# export csv
vins_premium.to_csv(OUTPUT_DIR / "vins_premium.csv", index=False)
vins_ordinaires.to_csv(OUTPUT_DIR / "vins_ordinaires.csv", index=False)