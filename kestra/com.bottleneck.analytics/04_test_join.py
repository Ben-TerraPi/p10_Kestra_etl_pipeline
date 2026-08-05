from pathlib import Path

import duckdb
import pandas as pd


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
PIPELINE_DB = WORK_DIR / "bottleneck.duckdb"
MERGED_FILE = WORK_DIR / "merged.csv"
SQL_DOUBLONS = PROJECT_DIR / "sql_files" / "doublons.sql"


con = duckdb.connect(str(PIPELINE_DB))
df_merged = pd.read_csv(MERGED_FILE)

if df_merged["product_id"].isnull().sum() != 0:
	raise ValueError("ERREUR TEST: product_id nul détecté après jointure!")

if df_merged["id_web"].isnull().sum() != 0:
	raise ValueError("ERREUR TEST: id_web nul détecté après jointure!")

duplicate_rows = con.execute(SQL_DOUBLONS.read_text(encoding="utf-8")).fetchone()[0]
if duplicate_rows != 0:
	raise ValueError(f"ERREUR TEST: Doublons détectés après jointure ({duplicate_rows})")

if len(df_merged) != 714:
	raise ValueError(f"ERREUR TEST: Volume table fusionnée ({len(df_merged)}) != 714")

con.close()