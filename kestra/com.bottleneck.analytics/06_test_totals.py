from pathlib import Path

import pandas as pd


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
MERGED_FILE = WORK_DIR / "merged.csv"
CA_TOTAL_FILE = WORK_DIR / "ca_total.txt"


df_merged = pd.read_csv(MERGED_FILE)
ca_total = float(CA_TOTAL_FILE.read_text(encoding="utf-8"))

if df_merged["total_sales"].isnull().sum() != 0:
	raise ValueError("ERREUR TEST: total_sales nul détecté avant export du rapport!")

if df_merged["chiffre_affaires"].isnull().sum() != 0:
	raise ValueError("ERREUR TEST: chiffre_affaires nul détecté avant export du rapport!")

ca_attendu = 70568.60
if abs(ca_total - ca_attendu) >= 0.01:
	raise ValueError(f"ERREUR TEST: CA total ({ca_total:.2f} €) != {ca_attendu} €")

ca_recalcule = (df_merged["price"] * df_merged["total_sales"]).sum()
if abs(ca_total - ca_recalcule) >= 0.01:
	raise ValueError(f"ERREUR TEST: Incohérence du total CA ({ca_total:.2f} € != {ca_recalcule:.2f} €)")