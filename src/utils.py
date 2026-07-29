from pathlib import Path

import duckdb
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
SQL_DIR = PROJECT_DIR / "sql_files"
OUTPUT_DIR = PROJECT_DIR / "output"

SQL_NETTOYAGE = SQL_DIR / "nettoyage.sql"
SQL_JOINTURE = SQL_DIR / "jointure.sql"

REPORT_FILE = OUTPUT_DIR / "rapport_chiffre_affaires.xlsx"
PODIUM_PREMIUM_FILE = OUTPUT_DIR / "vins_premium.csv"
PODIUM_ORDINARY_FILE = OUTPUT_DIR / "vins_ordinaires.csv"


def create_df():
    """
    Charge les fichiers Excel bruts dans des DataFrames.
    """
    df_erp = pd.read_excel(DATA_DIR / "Fichier_erp.xlsx")
    df_liaison = pd.read_excel(DATA_DIR / "fichier_liaison.xlsx")
    df_web = pd.read_excel(DATA_DIR / "Fichier_web.xlsx")
    return df_erp, df_liaison, df_web


def duckdb_raw_tables(df_erp, df_liaison, df_web):
    """
    Crée la connexion DuckDB et enregistre les tables brutes.
    """
    con = duckdb.connect(database=":memory:")
    con.register("raw_erp", df_erp)
    con.register("raw_liaison", df_liaison)
    con.register("raw_web", df_web)
    return con


def clean_data(con):
    """
    Exécute la requête SQL de nettoyage et crée les tables intermédiaires.
    """
    query = SQL_NETTOYAGE.read_text(encoding="utf-8")
    con.execute(query)
    return con


def merge_data(con):
    """
    Exécute la requête SQL de jointure et retourne le DataFrame final.
    """
    query = SQL_JOINTURE.read_text(encoding="utf-8")
    return con.execute(query).df()


def export_report(df_merged):
    """
    Exporte le rapport Excel du chiffre d'affaires.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ca_total = df_merged["chiffre_affaires"].sum()

    with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:
        df_merged[
            ["product_id", "id_web", "nom_produit", "price", "total_sales", "chiffre_affaires"]
        ].to_excel(
            writer,
            sheet_name="CA par Produit",
            index=False,
        )
        pd.DataFrame([{"CA_Total_Euros": ca_total}]).to_excel(
            writer,
            sheet_name="CA Global",
            index=False,
        )

    return ca_total


def classify_wines(df_merged):
    """
    Calcule le z-score et sépare les vins premium des vins ordinaires.
    """
    df_merged = df_merged.copy()
    mean_price = df_merged["price"].mean()
    std_price = df_merged["price"].std()
    df_merged["z_score"] = (df_merged["price"] - mean_price) / std_price

    vins_premium = df_merged[df_merged["z_score"] > 2]
    vins_ordinaires = df_merged[df_merged["z_score"] <= 2]
    return vins_premium, vins_ordinaires


def export_wine_lists(vins_premium, vins_ordinaires):
    """
    Exporte les listes de vins premium et ordinaires en CSV.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    vins_premium.to_csv(PODIUM_PREMIUM_FILE, index=False)
    vins_ordinaires.to_csv(PODIUM_ORDINARY_FILE, index=False)