from utils import (
    create_df,
    duckdb_raw_tables,
    clean_data,
    run_sql_tests,
    merge_data,
    run_join_tests,
    classify_wines,
    export_report,
    export_wine_lists,
    validate_business_logic,
)


def main():
    print("--- Début du pipeline ETL Bottleneck ---")

    # dataframes
    df_erp, df_liaison, df_web = create_df()

    # connexion duckdb
    con = duckdb_raw_tables(df_erp, df_liaison, df_web)

    # nettoyage 
    clean_data(con)

    # tests après nettoyage
    run_sql_tests(con)

    # jointures
    df_merged = merge_data(con)

    # tests après jointure
    run_join_tests(con, df_merged)

    # rapport CA
    ca_total = export_report(df_merged)

    # classification des vins
    vins_premium, vins_ordinaires = classify_wines(df_merged)
    export_wine_lists(vins_premium, vins_ordinaires)

    # validation finale
    validate_business_logic(df_merged, vins_premium, vins_ordinaires, ca_total)

    # rapport terminal
    print(" TESTS REUSSIS : Toutes les données sont conformes aux analyses de Stéphane.")
    print(f"Rapport généré avec succès. CA Total : {ca_total:.2f} €.")
    print(f"Nombre de vins premium identifiés : {len(vins_premium)}.")
    print(f"Nombre de vins ordinaires identifiés : {len(vins_ordinaires)}.")


if __name__ == "__main__":
    main()