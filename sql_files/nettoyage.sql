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
