from pathlib import Path

import pandas as pd


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
MERGED_FILE = WORK_DIR / "merged.csv"
CA_TOTAL_FILE = WORK_DIR / "ca_total.txt"


WORK_DIR.mkdir(parents=True, exist_ok=True)
df_merged = pd.read_csv(MERGED_FILE)
ca_total = df_merged["chiffre_affaires"].sum()
CA_TOTAL_FILE.write_text(f"{ca_total:.2f}", encoding="utf-8")