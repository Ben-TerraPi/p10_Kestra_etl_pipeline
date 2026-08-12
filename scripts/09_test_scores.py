from pathlib import Path

import pandas as pd


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
MERGED_FILE = WORK_DIR / "merged.csv"
PREMIUM_FILE = WORK_DIR / "vins_premium.csv"
ORDINARY_FILE = WORK_DIR / "vins_ordinaires.csv"
CA_TOTAL_FILE = WORK_DIR / "ca_total.txt"


# lecture des fichiers
df_merged = pd.read_csv(MERGED_FILE)
ca_total = float(CA_TOTAL_FILE.read_text(encoding="utf-8"))
vins_premium = pd.read_csv(PREMIUM_FILE)
vins_ordinaires = pd.read_csv(ORDINARY_FILE)

# validation z-score
if len(vins_premium) != 30:
	raise ValueError(f"ERREUR TEST: Vins premium ({len(vins_premium)}) != 30")

if len(vins_ordinaires) != (len(df_merged) - 30):
	raise ValueError("ERREUR TEST: Nombre incohérent de vins ordinaires!")

if vins_premium["z_score"].le(2).any():
	raise ValueError("ERREUR TEST: Un vin premium a un z_score incohérent!")

if vins_ordinaires["z_score"].gt(2).any():
	raise ValueError("ERREUR TEST: Un vin ordinaire a un z_score incohérent!")

if abs(ca_total - 70568.60) >= 0.01:
	raise ValueError(f"ERREUR TEST: CA total ({ca_total:.2f} €) != 70568.60 €")