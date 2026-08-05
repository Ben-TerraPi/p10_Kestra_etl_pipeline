from pathlib import Path
import duckdb
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
SQL_DIR = PROJECT_DIR / "sql_files"
OUTPUT_DIR = PROJECT_DIR / "output"

SQL_NETTOYAGE = SQL_DIR / "nettoyage.sql"
SQL_JOINTURE = SQL_DIR / "jointure.sql"
SQL_DOUBLONS = SQL_DIR / "doublons.sql"

REPORT_FILE = OUTPUT_DIR / "rapport_chiffre_affaires.xlsx"
PODIUM_PREMIUM_FILE = OUTPUT_DIR / "vins_premium.csv"
PODIUM_ORDINARY_FILE = OUTPUT_DIR / "vins_ordinaires.csv"


# dataframes
def create_df():
    """Charge les fichiers Excel bruts dans des DataFrames."""
    df_erp = pd.read_excel(DATA_DIR / "Fichier_erp.xlsx")
    df_liaison = pd.read_excel(DATA_DIR / "fichier_liaison.xlsx")
    df_web = pd.read_excel(DATA_DIR / "Fichier_web.xlsx")
    return df_erp, df_liaison, df_web


# connexion duckdb
def duckdb_raw_tables(df_erp, df_liaison, df_web):
    """Crée la connexion DuckDB et enregistre les tables brutes."""
    con = duckdb.connect(database=":memory:")
    con.register("raw_erp", df_erp)
    con.register("raw_liaison", df_liaison)
    con.register("raw_web", df_web)
    return con


# nettoyage 
def clean_data(con):
    """Exécute la requête SQL de nettoyage et crée les tables intermédiaires."""
    query = SQL_NETTOYAGE.read_text(encoding="utf-8")
    con.execute(query)
    return con


# tests nettoyage
def run_sql_tests(con):
    """Réalise les tests d'unicité sur DuckDB."""
    cnt_erp = con.execute("SELECT COUNT(*), COUNT(DISTINCT product_id) FROM erp_clean").fetchone()
    cnt_web = con.execute("SELECT COUNT(*), COUNT(DISTINCT id_web) FROM web_clean").fetchone()
    
    if cnt_erp[0] != cnt_erp[1]:
        raise ValueError(f"ERREUR TEST: Doublons dans erp_clean ({cnt_erp[0]} != {cnt_erp[1]})")

    if cnt_web[0] != cnt_web[1]:
        raise ValueError(f"ERREUR TEST: Doublons dans web_clean ({cnt_web[0]} != {cnt_web[1]})")

    if cnt_erp[0] != 825:
        raise ValueError(f"ERREUR TEST: Volume erp_clean ({cnt_erp[0]}) != 825")

    if cnt_web[0] != 714:
        raise ValueError(f"ERREUR TEST: Volume web_clean ({cnt_web[0]}) != 714")


# jointures
def merge_data(con):
    """Exécute la requête SQL de jointure et retourne le DataFrame final."""
    query = SQL_JOINTURE.read_text(encoding="utf-8")
    df_merged = con.execute(query).df()

    return df_merged


# tests après jointure
def run_join_tests(con, df_merged):
    """Réalise les tests de cohérence après la jointure finale."""

    # clé orpheline
    erp_orphans = con.execute("""
        SELECT COUNT(*)
        FROM erp_clean e
        LEFT JOIN liaison_clean l ON e.product_id = l.product_id
        WHERE l.product_id IS NULL
    """).fetchone()[0]
    if erp_orphans != 0:
        raise ValueError(f"ERREUR TEST: Clés orphelines dans erp_clean ({erp_orphans})")

    liaison_orphans = con.execute("""
        SELECT COUNT(*)
        FROM liaison_clean l
        LEFT JOIN erp_clean e ON e.product_id = l.product_id
        LEFT JOIN web_clean w ON w.id_web = l.id_web
        WHERE e.product_id IS NULL OR w.id_web IS NULL
    """).fetchone()[0]
    if liaison_orphans != 0:
        raise ValueError(f"ERREUR TEST: Clés orphelines dans liaison_clean ({liaison_orphans})")

    web_orphans = con.execute("""
        SELECT COUNT(*)
        FROM web_clean w
        LEFT JOIN liaison_clean l ON l.id_web = w.id_web
        WHERE l.id_web IS NULL
    """).fetchone()[0]
    if web_orphans != 0:
        raise ValueError(f"ERREUR TEST: Clés orphelines dans web_clean ({web_orphans})")

    # doublons
    query = SQL_DOUBLONS.read_text(encoding="utf-8")
    duplicate_rows = con.execute(query).fetchone()[0]
    if duplicate_rows != 0:
        raise ValueError(f"ERREUR TEST: Doublons détectés après jointure ({duplicate_rows})")

    # volume
    if len(df_merged) != 714:
        raise ValueError(f"ERREUR TEST: Volume table fusionnée ({len(df_merged)}) != 714")


# rapport CA
def export_report(df_merged):
    """Exporte le rapport Excel du chiffre d'affaires."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ca_total = df_merged["chiffre_affaires"].sum()

    with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:
        df_merged[
            ["product_id", "id_web", "nom_produit", "price", "total_sales", "chiffre_affaires"]
        ].to_excel(writer, sheet_name="CA par Produit", index=False)
        
        pd.DataFrame([{"CA_Total_Euros": ca_total}]).to_excel(
            writer, sheet_name="CA Global", index=False
        )

    return ca_total


# classification des vins
def classify_wines(df_merged):
    """Calcule le z-score et sépare les vins premium des vins ordinaires."""
    df_merged = df_merged.copy()
    mean_price = df_merged["price"].mean()
    std_price = df_merged["price"].std()
    df_merged["z_score"] = (df_merged["price"] - mean_price) / std_price

    vins_premium = df_merged[df_merged["z_score"] > 2]
    vins_ordinaires = df_merged[df_merged["z_score"] <= 2]
    return vins_premium, vins_ordinaires


def export_wine_lists(vins_premium, vins_ordinaires):
    """Exporte les listes de vins premium et ordinaires en CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    vins_premium.to_csv(PODIUM_PREMIUM_FILE, index=False)
    vins_ordinaires.to_csv(PODIUM_ORDINARY_FILE, index=False)


# validation finale
def validate_business_logic(df_merged, vins_premium, vins_ordinaires, ca_total):
    """Valide la cohérence globale du CA et de la répartition Z-Score."""

    if df_merged["product_id"].isnull().sum() != 0:
        raise ValueError("ERREUR TEST: product_id nul détecté!")

    if df_merged["id_web"].isnull().sum() != 0:
        raise ValueError("ERREUR TEST: id_web nul détecté!")

    if df_merged["price"].isnull().sum() != 0:
        raise ValueError("ERREUR TEST: Prix nul détecté!")

    ca_attendu = 70568.60
    if abs(ca_total - ca_attendu) >= 0.01:
        raise ValueError(f"ERREUR TEST: CA total ({ca_total:.2f} €) != {ca_attendu} €")

    if len(vins_premium) != 30:
        raise ValueError(f"ERREUR TEST: Vins premium ({len(vins_premium)}) != 30")

    if len(vins_ordinaires) != (len(df_merged) - 30):
        raise ValueError("ERREUR TEST: Nombre incohérent de vins ordinaires!")





