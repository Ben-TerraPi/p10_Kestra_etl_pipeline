from pathlib import Path

import pandas as pd


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
OUTPUT_DIR = PROJECT_DIR / "output"
MERGED_FILE = WORK_DIR / "merged.csv"
CA_TOTAL_FILE = WORK_DIR / "ca_total.txt"
REPORT_FILE = OUTPUT_DIR / "rapport_chiffre_affaires.xlsx"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# lecture des fichiers
df_merged = pd.read_csv(MERGED_FILE)
ca_total = float(CA_TOTAL_FILE.read_text(encoding="utf-8"))

# création du rapport .xlxs
with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:
	df_merged[["product_id", "id_web", "nom_produit", "price", "total_sales", "chiffre_affaires"]].to_excel(
		writer,
		sheet_name="CA par Produit",
		index=False,
	)
	pd.DataFrame([{"CA_Total_Euros": ca_total}]).to_excel(writer, sheet_name="CA Global", index=False)