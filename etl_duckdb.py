import pandas as pd
import duckdb

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;") # or load pandas df into duckdb

df_erp = pd.read_excel('Fichier_erp.xlsx')
df_liaison = pd.read_excel('fichier_liaison.xlsx')
df_web = pd.read_excel('Fichier_web.xlsx')

con.register('raw_erp', df_erp)
con.register('raw_liaison', df_liaison)
con.register('raw_web', df_web)

# Deduplication SQL
con.execute("""
CREATE TABLE clean_erp AS 
SELECT DISTINCT product_id, onsale_web, price, stock_quantity, stock_status 
FROM raw_erp 
WHERE product_id IS NOT NULL;
""")

con.execute("""
CREATE TABLE clean_liaison AS 
SELECT DISTINCT product_id, id_web 
FROM raw_liaison 
WHERE product_id IS NOT NULL AND id_web IS NOT NULL;
""")

con.execute("""
CREATE TABLE clean_web AS 
SELECT DISTINCT sku, total_sales, post_title, post_type 
FROM raw_web 
WHERE post_type = 'product' AND sku IS NOT NULL;
""")

# Merge SQL
con.execute("""
CREATE TABLE merged_data AS
SELECT 
    e.product_id,
    l.id_web,
    w.post_title,
    e.price,
    w.total_sales,
    (e.price * w.total_sales) AS ca_produit
FROM clean_erp e
JOIN clean_liaison l ON e.product_id = l.product_id
JOIN clean_web w ON l.id_web = w.sku;
""")

res = con.execute("SELECT COUNT(*), SUM(ca_produit) FROM merged_data").fetchone()
print("Merged row count and Total CA:", res)