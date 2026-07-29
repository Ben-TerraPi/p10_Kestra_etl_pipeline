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