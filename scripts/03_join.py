from pathlib import Path

import duckdb


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
PIPELINE_DB = WORK_DIR / "bottleneck.duckdb"
SQL_FILE = PROJECT_DIR / "sql" / "jointure.sql"
MERGED_FILE = WORK_DIR / "merged.csv"

WORK_DIR.mkdir(parents=True, exist_ok=True)


# connexion duckdb
con = duckdb.connect(str(PIPELINE_DB))

# jointure avec requeête SQL
df_merged = con.execute(SQL_FILE.read_text(encoding="utf-8")).df()

# création d'un csv pour test et suite
df_merged.to_csv(MERGED_FILE, index=False)

con.close()