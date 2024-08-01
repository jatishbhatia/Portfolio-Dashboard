CREATE DATABASE financial_portfolio;

USE financial_portfolio;

CREATE TABLE Assets (
asset_id INT AUTO_INCREMENT PRIMARY KEY,
asset_name VARCHAR(255) NOT NULL,
purchase_date DATE,
purchase_price DECIMAL(15, 2),
quantity DECIMAL(15, 2)
);

CREATE TABLE Categories (
category_id INT AUTO_INCREMENT PRIMARY KEY,
category_name VARCHAR(255) NOT NULL,
category_description TEXT
);

CREATE TABLE Asset_Category (
asset_id INT,
category_id INT,
FOREIGN KEY (asset_id) REFERENCES Assets(asset_id),
FOREIGN KEY (category_id) REFERENCES Categories(category_id),
PRIMARY KEY (asset_id, category_id)
);

-- INSERTING EXAMPLE DATA

INSERT INTO Assets (asset_name, purchase_date, purchase_price, quantity)
VALUES
('Apple', '2024-01-01', 150.00, 10),
('ABC', '2024-06-01', 1000.00, 5),
('250 King St. Toronto', '2022-12-10', 50000.00, 1);

INSERT INTO Categories (category_name, category_description)
VALUES
('Stocks', 'Various stock investments'),
('Bonds', 'Different types of bonds'),
('Real Estate', 'Properties and real estate investments'),
('Cash', 'Liquid Funds'),
('Valuables', 'Valuable Items');

INSERT INTO Asset_Category (asset_id, category_id)
VALUES
(1, 1), -- Stock A belongs to Stocks
(2, 2), -- Bond B belongs to Bonds
(3, 3); -- Real Estate C belongs to Real Estate

select * from Assets;
