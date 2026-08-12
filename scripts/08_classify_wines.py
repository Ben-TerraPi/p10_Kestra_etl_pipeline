from pathlib import Path

import pandas as pd
import duckdb


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
PIPELINE_DB = WORK_DIR / "bottleneck.duckdb"
MERGED_FILE = WORK_DIR / "merged.csv"
PREMIUM_FILE = WORK_DIR / "vins_premium.csv"
ORDINARY_FILE = WORK_DIR / "vins_ordinaires.csv"
CA_TOTAL_FILE = WORK_DIR / "ca_total.txt"

# lecture des fichiers
df_merged = pd.read_csv(MERGED_FILE).copy()
ca_total = float(CA_TOTAL_FILE.read_text(encoding="utf-8"))

# classification des vins
mean_price = df_merged["price"].mean()
std_price = df_merged["price"].std()
df_merged["z_score"] = (df_merged["price"] - mean_price) / std_price

# Connexion DuckDB
con = duckdb.connect(str(PIPELINE_DB))

# maj table merge
con.execute("DROP TABLE IF EXISTS merged")
con.register("df_merged", df_merged)
con.execute("""
    CREATE TABLE merged AS
    SELECT * FROM df_merged
""")

con.close()

vins_premium = df_merged[df_merged["z_score"] > 2]
vins_ordinaires = df_merged[df_merged["z_score"] <= 2]

# écriture des csv
vins_premium.to_csv(PREMIUM_FILE, index=False)
vins_ordinaires.to_csv(ORDINARY_FILE, index=False)

print(f"Classification calculee avec CA total de reference: {ca_total:.2f} €")
print(f"Vins premium: {len(vins_premium)} | Vins ordinaires: {len(vins_ordinaires)}")