from pathlib import Path

import duckdb
import pandas as pd


PROJECT_DIR = Path.cwd()

WORK_DIR = PROJECT_DIR / "work"
DATA_DIR = PROJECT_DIR / "data"
SQL_FILE = PROJECT_DIR / "sql" / "nettoyage.sql"
PIPELINE_DB = WORK_DIR / "bottleneck.duckdb"

WORK_DIR.mkdir(parents=True, exist_ok=True)


# dataframes
df_erp = pd.read_excel(DATA_DIR / "Fichier_erp.xlsx")
df_liaison = pd.read_excel(DATA_DIR / "fichier_liaison.xlsx")
df_web = pd.read_excel(DATA_DIR / "Fichier_web.xlsx")

# connexion duckdb
con = duckdb.connect(str(PIPELINE_DB))

# création tables brutes
con.register("raw_erp", df_erp)
con.register("raw_liaison", df_liaison)
con.register("raw_web", df_web)

# nettoyage avec requête sql
con.execute(SQL_FILE.read_text(encoding="utf-8"))

con.close()