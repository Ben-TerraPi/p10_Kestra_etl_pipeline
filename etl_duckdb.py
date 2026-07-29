from pathlib import Path

import duckdb
import pandas as pd


# path pour fichier sql
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "etl_duckdb.sql"

# connection duckdb
con = duckdb.connect(database=":memory:")

# dataframe
df_erp = pd.read_excel(BASE_DIR / "erp.xlsx")
df_liaison = pd.read_excel(BASE_DIR / "liaison.xlsx")
df_web = pd.read_excel(BASE_DIR / "web.xlsx")

# créatrion table duckdb
con.register("raw_erp", df_erp)
con.register("raw_liaison", df_liaison)
con.register("raw_web", df_web)

# requete sql 
query = SQL_FILE.read_text(encoding="utf-8")
df_merged = con.execute(query).df()

# calcul du CA
ca_total = df_merged["chiffre_affaires"].sum()

# ecriture pour fichier xls
with pd.ExcelWriter(BASE_DIR / "rapport_chiffre_affaires.xlsx", engine="openpyxl") as writer:
    df_merged[["product_id", "id_web", "nom_produit", "price", "total_sales", "chiffre_affaires"]].to_excel(
        writer,
        sheet_name="CA par Produit",
        index=False,
    )
    pd.DataFrame([{"CA_Total_Euros": ca_total}]).to_excel(
        writer,
        sheet_name="CA Global",
        index=False,
    )

# calcul des kpi
mean_price = df_merged["price"].mean()
std_price = df_merged["price"].std()
df_merged["z_score"] = (df_merged["price"] - mean_price) / std_price

vins_premium = df_merged[df_merged["z_score"] > 2]
vins_ordinaires = df_merged[df_merged["z_score"] <= 2]

# crétaion des .csv
vins_premium.to_csv(BASE_DIR / "vins_premium.csv", index=False)
vins_ordinaires.to_csv(BASE_DIR / "vins_ordinaires.csv", index=False)

# rapport de fin
print(f"Rapport généré avec succès. CA Total : {ca_total:.2f} €.")
print(f"Nombre de vins premium identifiés : {len(vins_premium)}.")
print(f"Nombre de vins ordinaires identifiés : {len(vins_ordinaires)}.")
