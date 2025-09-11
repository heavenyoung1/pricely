-- ====== Пользователи ======
INSERT INTO users (id, username, chat_id) VALUES
('user_1', 'ivan_petrov', 123456789),
('user_2', 'anna_sidorova', 987654321),
('user_3', 'max_volkov', 555666777),
('user_4', 'olga_ivanova', 111222333),
('user_5', 'sergey_kuznetsov', 444555666);

-- ====== Продукты ======
INSERT INTO products (id, name, link, image_url, rating, categories) VALUES
('prod_1', 'Смартфон Samsung Galaxy S23', 'https://example.com/samsung-s23', 'https://example.com/images/s23.jpg', 4.8, '["electronics", "smartphones", "samsung"]'),
('prod_2', 'Ноутбук ASUS ROG Strix', 'https://example.com/asus-rog', 'https://example.com/images/rog.jpg', 4.6, '["electronics", "laptops", "gaming"]'),
('prod_3', 'Наушники Sony WH-1000XM4', 'https://example.com/sony-xm4', 'https://example.com/images/sony-xm4.jpg', 4.9, '["electronics", "audio", "headphones"]'),
('prod_4', 'Кофемашина DeLonghi', 'https://example.com/delonghi', 'https://example.com/images/delonghi.jpg', 4.5, '["appliances", "kitchen", "coffee"]'),
('prod_5', 'Фитнес-браслет Xiaomi Mi Band 7', 'https://example.com/mi-band-7', 'https://example.com/images/mi-band7.jpg', 4.4, '["electronics", "wearables", "fitness"]'),
('prod_6', 'Монитор LG UltraGear', 'https://example.com/lg-ultragear', 'https://example.com/images/lg-monitor.jpg', 4.7, '["electronics", "monitors", "gaming"]'),
('prod_7', 'Электрическая зубная щетка Oral-B', 'https://example.com/oral-b', 'https://example.com/images/oralb.jpg', 4.3, '["health", "personal_care", "oral_hygiene"]');

-- ====== Цены (несколько цен для каждого продукта с разными датами) ======
-- Продукт 1
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_1', 69990, 74990, 71990, 76990, 79990, '2024-01-15 10:00:00'),
('prod_1', 68990, 73990, 69990, 74990, 79990, '2024-01-20 14:30:00'),
('prod_1', 67990, 72990, 68990, 73990, 79990, '2024-01-25 09:15:00');

-- Продукт 2
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_2', 129990, 139990, NULL, NULL, 149990, '2024-01-10 11:20:00'),
('prod_2', 125990, 135990, 129990, 139990, 149990, '2024-01-18 16:45:00'),
('prod_2', 122990, 132990, 125990, 135990, 149990, '2024-01-26 08:30:00');

-- Продукт 3
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_3', 24990, 27990, 25990, 28990, 29990, '2024-01-12 13:10:00'),
('prod_3', 23990, 26990, 24990, 27990, 29990, '2024-01-19 15:20:00'),
('prod_3', 22990, 25990, 23990, 26990, 29990, '2024-01-27 10:45:00');

-- Продукт 4
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_4', 45990, 49990, NULL, NULL, 54990, '2024-01-14 09:30:00'),
('prod_4', 44990, 48990, 45990, 49990, 54990, '2024-01-22 12:15:00');

-- Продукт 5
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_5', 3990, 4490, 4190, 4690, 4990, '2024-01-16 14:20:00'),
('prod_5', 3890, 4390, 3990, 4490, 4990, '2024-01-24 17:30:00');

-- Продукт 6
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_6', 34990, 37990, NULL, NULL, 39990, '2024-01-17 10:40:00'),
('prod_6', 33990, 36990, 34990, 37990, 39990, '2024-01-25 13:25:00');

-- Продукт 7
INSERT INTO prices (product_id, with_card, without_card, previous_with_card, previous_without_card, default, created_at) VALUES
('prod_7', 5990, 6490, 6190, 6690, 6990, '2024-01-13 15:50:00'),
('prod_7', 5790, 6290, 5990, 6490, 6990, '2024-01-21 11:35:00');

-- ====== Связи пользователей и продуктов ======
INSERT INTO users_products (user_id, product_id) VALUES
('user_1', 'prod_1'),
('user_1', 'prod_3'),
('user_1', 'prod_5'),
('user_2', 'prod_2'),
('user_2', 'prod_4'),
('user_3', 'prod_1'),
('user_3', 'prod_6'),
('user_4', 'prod_3'),
('user_4', 'prod_7'),
('user_5', 'prod_2'),
('user_5', 'prod_5'),
('user_5', 'prod_6');