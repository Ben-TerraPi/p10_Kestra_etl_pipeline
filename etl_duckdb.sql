CREATE TABLE erp_clean AS
SELECT DISTINCT
    CAST(product_id AS INT) AS product_id,
    price,
    stock_quantity,
    stock_status
FROM raw_erp
WHERE product_id IS NOT NULL;

CREATE TABLE web_clean AS
SELECT DISTINCT
    sku AS id_web,
    total_sales,
    post_title,
    post_type
FROM raw_web
WHERE sku IS NOT NULL
    AND post_type = 'product';

CREATE TABLE liaison_clean AS
SELECT DISTINCT
    CAST(product_id AS INT) AS product_id,
    id_web
FROM raw_liaison
WHERE product_id IS NOT NULL
    AND id_web IS NOT NULL;

SELECT
    e.product_id,
    l.id_web,
    w.post_title AS nom_produit,
    e.price,
    COALESCE(w.total_sales, 0) AS total_sales,
    (e.price * COALESCE(w.total_sales, 0)) AS chiffre_affaires
FROM erp_clean e
INNER JOIN liaison_clean l ON e.product_id = l.product_id
INNER JOIN web_clean w ON l.id_web = w.id_web;