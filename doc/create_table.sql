-- ====== Таблица пользователей ======
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    chat_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ====== Таблица продуктов ======
CREATE TABLE products (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    rating FLOAT NOT NULL,
    categories JSON NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ====== Таблица цен ======
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    with_card INTEGER NOT NULL,
    without_card INTEGER NOT NULL,
    previous_with_card INTEGER,
    previous_without_card INTEGER,
    default_pr INTEGER NOT NULL, --default нельзя, SQL ругается
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE CASCADE
);

-- ====== Join-таблица пользователей и продуктов ======
CREATE TABLE users_products (
    user_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, product_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_product_user FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE CASCADE
);
