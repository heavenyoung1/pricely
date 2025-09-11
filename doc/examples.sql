-- Актуальная цена для продукта (самая свежая по claim):
SELECT price
FROM prices
WHERE product_id = <product_id>  -- Замени на ID продукта
ORDER BY claim DESC
LIMIT 1;

-- История цен для продукта (все цены, отсортированные от новой к старой):

SELECT price, claim
FROM prices
WHERE product_id = <product_id>
ORDER BY claim DESC;

