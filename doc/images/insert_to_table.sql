-- Пользователь
INSERT INTO users (id, username, chat_id)
VALUES ('u1', 'test_user', 123456789);

-- Продукт
INSERT INTO products (id, name, link, image_url, rating, categories)
VALUES (
    'p1',
    'Test Product',
    'https://example.com/product',
    'https://example.com/image.jpg',
    4.7,
    '["electronics", "gadgets"]'::json
);

-- Цена для продукта
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default)
VALUES (
    'p1',
    100,
    120,
    NULL,
    NULL,
    150
);

-- Связь пользователя и продукта
INSERT INTO users_products (user_id, product_id)
VALUES ('u1', 'p1');
