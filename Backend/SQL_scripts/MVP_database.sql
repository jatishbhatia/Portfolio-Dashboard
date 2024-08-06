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
('GOOG', 'Alphabet Inc.', 'Stock', 5000.00, 25),
('TLT', 'iShares 20+ Year Treasury Bond ETF', 'Bond', 2000.00, 15),
('CASH', 'Cash Fund', 'Cash', 100500.00, NULL),
('Property 101', 'Beachfront Property', 'Real_Estate', 300000.00, 1),
('Gold Necklace', 'Gold and Diamond Necklace', 'Valuables', 10000.00, NULL);

-- Insert data into Transaction table
INSERT INTO Transaction (asset_id, transaction_type, quantity, price, transaction_date) VALUES
(1, 'buy', 10, 150.00, '2024-07-01 10:30:00'),  -- Buying an asset
(2, 'sell', 5, 1000.00, '2024-07-01 11:00:00'), -- Selling an asset
(4, 'cash_in', NULL, 5000.00, '2024-07-01 12:00:00'),  -- Depositing cash
(4, 'cash_out', NULL, 200.00, '2024-07-02 09:00:00'); -- Spending cash