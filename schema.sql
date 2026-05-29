-- ─────────────────────────────────────────────────
--  NEXUS BI Agent — MySQL Schema
-- ─────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS bi_agent;
USE bi_agent;

-- Drop tables in reverse FK order
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INT           PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(120)  NOT NULL,
    email         VARCHAR(180)  UNIQUE NOT NULL,
    city          VARCHAR(80),
    country       VARCHAR(80),
    created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    product_id      INT           PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(200)  NOT NULL,
    category        VARCHAR(80),
    price           DECIMAL(10,2) NOT NULL,
    stock_quantity  INT           DEFAULT 0
);

-- Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id      INT             PRIMARY KEY AUTO_INCREMENT,
    customer_id   INT             NOT NULL,
    order_date    DATETIME        DEFAULT CURRENT_TIMESTAMP,
    status        ENUM('pending','processing','shipped','delivered','cancelled') DEFAULT 'pending',
    total_amount  DECIMAL(12,2)   NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items
CREATE TABLE IF NOT EXISTS order_items (
    item_id       INT             PRIMARY KEY AUTO_INCREMENT,
    order_id      INT             NOT NULL,
    product_id    INT             NOT NULL,
    quantity      INT             NOT NULL DEFAULT 1,
    unit_price    DECIMAL(10,2)   NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ─── Sample Data ──────────────────────────────────────
INSERT INTO customers (name, email, city, country) VALUES
('Alice Johnson',  'alice@example.com',  'New York',  'USA'),
('Bob Chen',       'bob@example.com',    'London',    'UK'),
('Carlos Ruiz',    'carlos@example.com', 'Madrid',    'Spain'),
('Diana Patel',    'diana@example.com',  'Mumbai',    'India'),
('Eva Müller',     'eva@example.com',    'Berlin',    'Germany'),
('Frank Tanaka',   'frank@example.com',  'Tokyo',     'Japan'),
('Grace Kim',      'grace@example.com',  'Seoul',     'South Korea'),
('Henry Wilson',   'henry@example.com',  'Sydney',    'Australia');

INSERT INTO products (name, category, price, stock_quantity) VALUES
('Laptop Pro 15',      'Electronics',  1299.99,  45),
('Wireless Mouse',     'Electronics',    29.99, 200),
('Office Chair Deluxe','Furniture',     349.99,  20),
('Standing Desk',      'Furniture',     599.99,  15),
('Python Handbook',    'Books',          49.99, 120),
('Data Science Kit',   'Education',     199.99,  60),
('USB-C Hub 7-in-1',  'Electronics',    59.99, 150),
('Ergonomic Keyboard', 'Electronics',    89.99,  80);

INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
(1, '2024-01-15', 'delivered',  1329.98),
(2, '2024-01-22', 'delivered',   349.99),
(3, '2024-02-05', 'delivered',   649.98),
(4, '2024-02-18', 'shipped',     199.99),
(5, '2024-03-01', 'delivered',  1359.97),
(6, '2024-03-14', 'delivered',    89.99),
(7, '2024-04-02', 'processing',  599.99),
(8, '2024-04-20', 'delivered',   249.97),
(1, '2024-05-10', 'delivered',   399.98),
(2, '2024-05-28', 'cancelled',    59.99);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1,  1, 1, 1299.99),
(1,  2, 1,   29.99),
(2,  3, 1,  349.99),
(3,  4, 1,  599.99),
(3,  2, 1,   29.99),
(3,  5, 1,   49.99),
(4,  6, 1,  199.99),
(5,  1, 1, 1299.99),
(5,  2, 2,   29.99),
(6,  8, 1,   89.99),
(7,  4, 1,  599.99),
(8,  5, 2,   49.99),
(8,  7, 2,   59.99),
(9,  3, 1,  349.99),
(9,  2, 1,   29.99),
(10, 7, 1,   59.99);