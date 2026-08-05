from utils import (
    create_df,
    duckdb_raw_tables,
    clean_data,
    run_sql_tests,
    merge_data,
    run_join_tests,
    calcul_ca,
    run_total_tests,
    export_report,
    classify_wines,
    valide_z_score,
    export_wine_lists,

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

    # calcul des CA
    ca_total = calcul_ca(df_merged)

    # tests de cohérence des totaux
    run_total_tests(df_merged, ca_total)

    # rapport CA
    export_report(df_merged, ca_total)

    # classification des vins
    vins_premium, vins_ordinaires = classify_wines(df_merged)

    # validation du tri des vins
    valide_z_score(df_merged, vins_premium, vins_ordinaires, ca_total)

    # export csv 
    export_wine_lists(vins_premium, vins_ordinaires)

    # rapport terminal
    print(" TESTS REUSSIS : Toutes les données sont conformes aux analyses de Stéphane.")
    print(f"Rapport généré avec succès. CA Total : {ca_total:.2f} €.")
    print(f"Nombre de vins premium identifiés : {len(vins_premium)}.")
    print(f"Nombre de vins ordinaires identifiés : {len(vins_ordinaires)}.")


if __name__ == "__main__":
    main()