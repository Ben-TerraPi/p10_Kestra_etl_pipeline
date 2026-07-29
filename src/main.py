from utils import create_df, duckdb_raw_tables, clean_data, merge_data, export_report, classify_wines, export_wine_lists  

def main():

    # dataframe
    df_erp, df_liaison, df_web = create_df()

    # connection duckdb
    con = duckdb_raw_tables(df_erp, df_liaison, df_web)

    # nettoyage data
    clean_data(con)

    # jointure data
    df_merged = merge_data(con)

    #calcul CA
    ca_total = export_report(df_merged)

    # calcul pour liste des vins différents
    vins_premium, vins_ordinaires = classify_wines(df_merged)
    export_wine_lists(vins_premium, vins_ordinaires)

    # rapport final
    print(f"Rapport généré avec succès. CA Total : {ca_total:.2f} €.")
    print(f"Nombre de vins premium identifiés : {len(vins_premium)}.")
    print(f"Nombre de vins ordinaires identifiés : {len(vins_ordinaires)}.")


if __name__ == "__main__":
    main()
    
