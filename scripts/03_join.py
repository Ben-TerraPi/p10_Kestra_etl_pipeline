from pathlib import Path

import duckdb


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
PIPELINE_DB = WORK_DIR / "bottleneck.duckdb"
SQL_FILE = PROJECT_DIR / "sql" / "jointure.sql"
MERGED_FILE = WORK_DIR / "merged.csv"

WORK_DIR.mkdir(parents=True, exist_ok=True)


# Connexion DuckDB
con = duckdb.connect(str(PIPELINE_DB))

# Jointure avec requête SQL
df_merged = con.execute(
    SQL_FILE.read_text(encoding="utf-8")
).df()

# Création de la table merged dans DuckDB
con.execute("DROP TABLE IF EXISTS merged")
con.register("df_merged", df_merged)
con.execute("""
    CREATE TABLE merged AS
    SELECT * FROM df_merged
""")

# Création du CSV pour les tests et la suite
df_merged.to_csv(MERGED_FILE, index=False)

con.close()