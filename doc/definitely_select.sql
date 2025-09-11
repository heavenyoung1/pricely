-- 1. История цен для конкретного продукта
SELECT 
    p.created_at as "Дата обновления",
    p.with_card as "Цена с картой",
    p.without_card as "Цена без карты",
    p.previous_with_card as "Предыдущая цена с картой",
    p.previous_without_card as "Предыдущая цена без карты",
    p.default as "Базовая цена"
FROM prices p
WHERE p.product_id = 'prod_1'
ORDER BY p.created_at DESC;

-- 2. Актуальная (последняя цена) для продукта
SELECT 
    pr.name as "Название продукта",
    p.with_card as "Актуальная цена с картой",
    p.without_card as "Актуальная цена без карты",
    p.default as "Базовая цена",
    p.created_at as "Дата последнего обновления"
FROM prices p
JOIN products pr ON p.product_id = pr.id
WHERE p.product_id = 'prod_1'
ORDER BY p.created_at DESC
LIMIT 1;

-- 3. Получить все продукты для пользователя с актуальными ценами
SELECT 
    u.username as "Пользователь",
    pr.name as "Название продукта",
    pr.link as "Ссылка",
    pr.rating as "Рейтинг",
    latest_price.with_card as "Цена с картой",
    latest_price.without_card as "Цена без карты",
    latest_price.created_at as "Последнее обновление цены"
FROM users u
JOIN users_products up ON u.id = up.user_id
JOIN products pr ON up.product_id = pr.id
JOIN (
    SELECT DISTINCT ON (product_id) *
    FROM prices
    ORDER BY product_id, created_at DESC
) latest_price ON pr.id = latest_price.product_id
WHERE u.id = 'user_1'
ORDER BY pr.name;

-- 3a. Альтернативный вариант (более эффективный для больших данных)
WITH latest_prices AS (
    SELECT 
        product_id,
        with_card,
        without_card,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY created_at DESC) as rn
    FROM prices
)
SELECT 
    u.username,
    pr.name as product_name,
    pr.link,
    pr.rating,
    lp.with_card,
    lp.without_card,
    lp.created_at as price_update_time
FROM users u
JOIN users_products up ON u.id = up.user_id
JOIN products pr ON up.product_id = pr.id
JOIN latest_prices lp ON pr.id = lp.product_id AND lp.rn = 1
WHERE u.id = 'user_1'
ORDER BY pr.name;

-- Дополнительный запрос: Все пользователи, которые следят за конкретным продуктом
SELECT 
    u.username,
    u.chat_id,
    pr.name as product_name,
    lp.with_card as current_price_with_card,
    lp.without_card as current_price_without_card
FROM users u
JOIN users_products up ON u.id = up.user_id
JOIN products pr ON up.product_id = pr.id
JOIN (
    SELECT DISTINCT ON (product_id) *
    FROM prices
    ORDER BY product_id, created_at DESC
) lp ON pr.id = lp.product_id
WHERE pr.id = 'prod_1'
ORDER BY u.username;