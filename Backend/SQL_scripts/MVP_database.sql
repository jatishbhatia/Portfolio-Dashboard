CREATE DATABASE financial_portfolio;

USE financial_portfolio;

CREATE TABLE Category (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT
);

CREATE TABLE Asset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    category_name VARCHAR(255),
    total_purchase_price DECIMAL(10, 2) DEFAULT 0.00,
    quantity DECIMAL(10, 2) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_name) REFERENCES Category(name)
);

CREATE TABLE Transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT,
    transaction_type ENUM('buy', 'sell', 'cash_in', 'cash_out'),
    quantity DECIMAL(10, 2) DEFAULT NULL,
    price DECIMAL(10, 2) DEFAULT NULL,
    transaction_date DATETIME,
    FOREIGN KEY (asset_id) REFERENCES Asset(id)
);

-- Insert categories into Category table
INSERT INTO Category (name, description) VALUES
('Stock', 'Equities or shares in a company'),
('Bond', 'Debt securities issued by governments or corporations'),
('Cash', 'Physical cash or cash equivalents'),
('Real_Estate', 'Properties and land'),
('Valuables', 'Precious items such as jewelry or collectibles');

-- Insert data into Asset table
INSERT INTO Asset (symbol, name, category_name, total_purchase_price, quantity) VALUES
('AAPL', 'Apple Inc.', 'Stock', 1500.00, 10),
('GOOG', 'Alphabet Inc.', 'Stock', 2500.00, 25);


-- Insert data into Transaction table
INSERT INTO Transaction (asset_id, transaction_type, quantity, price, transaction_date) VALUES
(1, 'buy', 10, 150.00, '2024-07-01 10:30:00'),
(2, 'buy', 20, 100.00, '2024-07-02 10:30:00');
