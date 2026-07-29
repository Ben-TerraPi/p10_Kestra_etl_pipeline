import pandas as pd

for f in ['Fichier_erp.xlsx', 'fichier_liaison.xlsx', 'Fichier_web.xlsx']:
    df = pd.read_excel(f)
    print(f"=== {f} ===")
    print("Columns:", df.columns.tolist())
    print(df)
    print()

erp = pd.read_excel('Fichier_erp.xlsx')
liaison = pd.read_excel('fichier_liaison.xlsx')
web = pd.read_excel('Fichier_web.xlsx')

# Test data pipeline logic
erp_clean = erp.dropna(subset=['product_id']).drop_duplicates(subset=['product_id'])
liaison_clean = liaison.dropna(subset=['product_id', 'id_web']).drop_duplicates(subset=['id_web'])
web_clean = web[web['post_type'] == 'product'].dropna(subset=['sku']).drop_duplicates(subset=['sku'])

# Merge
df_merged = erp_clean.merge(liaison_clean, on='product_id', how='inner')
df_merged = df_merged.merge(web_clean, left_on='id_web', right_on='sku', how='inner')

df_merged['ca_produit'] = df_merged['price'] * df_merged['total_sales']
ca_total = df_merged['ca_produit'].sum()

print(f"Merged shape: {df_merged.shape}")
print(f"CA Total: {ca_total:,.2f} €")

# Z-score calculation on price
mean_price = df_merged['price'].mean()
std_price = df_merged['price'].std(ddof=0) # or ddof=1
df_merged['z_score'] = (df_merged['price'] - mean_price) / std_price

vins_premium = df_merged[df_merged['z_score'] > 2]
vins_ordinaires = df_merged[df_merged['z_score'] <= 2]

print(f"Nombre de vins premium (z > 2): {len(vins_premium)}")
print(f"Nombre de vins ordinaires (z <= 2): {len(vins_ordinaires)}")