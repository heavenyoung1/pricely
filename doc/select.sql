-- Проверим, что пользователь есть
SELECT * FROM users;

-- Проверим продукт
SELECT * FROM products;

-- Проверим цены продукта
SELECT * FROM prices WHERE product_id = 'p1';

-- Проверим, какие продукты привязаны к пользователю
SELECT u.username, p.name, p.link, pr.with_card, pr.without_card
FROM users u
JOIN users_products up ON u.id = up.user_id
JOIN products p ON up.product_id = p.id
JOIN prices pr ON pr.product_id = p.id
WHERE u.id = 'u1';
