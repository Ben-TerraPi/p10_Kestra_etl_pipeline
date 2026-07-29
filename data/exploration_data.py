import pandas as pd

erp = pd.read_excel('data/Fichier_erp.xlsx')
liaison = pd.read_excel('data/fichier_liaison.xlsx')
web = pd.read_excel('data/Fichier_web.xlsx')

# test logique du pipeline
erp_clean = erp.dropna(subset=['product_id']).drop_duplicates(subset=['product_id'])
liaison_clean = liaison.dropna(subset=['product_id', 'id_web']).drop_duplicates(subset=['id_web'])
web_clean = web[web['post_type'] == 'product'].dropna(subset=['sku']).drop_duplicates(subset=['sku'])

# jointure
df_merged = erp_clean.merge(liaison_clean, on='product_id', how='inner')
df_merged = df_merged.merge(web_clean, left_on='id_web', right_on='sku', how='inner')

#vérification lignes néttoyé
print(f"Merged shape: {df_merged.shape}")

# calcul du CA
df_merged['ca_produit'] = df_merged['price'] * df_merged['total_sales']
ca_total = df_merged['ca_produit'].sum()
print(f"CA Total: {ca_total:,.2f} €")

# z-score 
mean_price = df_merged['price'].mean()
std_price = df_merged['price'].std(ddof=0) # or ddof=1
df_merged['z_score'] = (df_merged['price'] - mean_price) / std_price

# nombres de vin différent
vins_premium = df_merged[df_merged['z_score'] > 2]
vins_ordinaires = df_merged[df_merged['z_score'] <= 2]

#rapport
print(f"Nombre de vins premium (z > 2): {len(vins_premium)}")
print(f"Nombre de vins ordinaires (z <= 2): {len(vins_ordinaires)}")