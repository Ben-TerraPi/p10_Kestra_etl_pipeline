SELECT COUNT(*)
FROM (
    SELECT
        product_id,
        id_web,
        COUNT(*) AS row_count
    FROM (
        SELECT
            e.product_id,
            l.id_web
        FROM erp_clean e
        INNER JOIN liaison_clean l ON e.product_id = l.product_id
        INNER JOIN web_clean w ON l.id_web = w.id_web
    ) joined_keys
    GROUP BY product_id, id_web
    HAVING COUNT(*) > 1
) duplicated_keys