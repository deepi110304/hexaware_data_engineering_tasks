CREATE DATABASE IF NOT EXISTS retail_sales_db;
USE retail_sales_db;
CREATE TABLE products 
(
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL
);
CREATE TABLE stores 
(
    store_id INT PRIMARY KEY AUTO_INCREMENT,
    store_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);
CREATE TABLE employees 
(
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_name VARCHAR(100) NOT NULL,
    store_id INT NOT NULL,
    job_role VARCHAR(50),
    FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
);
CREATE TABLE sales 
(
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    employee_id INT,
    sale_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    FOREIGN KEY (store_id)
        REFERENCES stores(store_id),
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);
SHOW TABLES;
DESCRIBE products;
DESCRIBE stores;
DESCRIBE employees;
DESCRIBE sales;
INSERT INTO products (product_name, category, price, cost) VALUES
('Laptop', 'Electronics', 60000.00, 45000.00),
('Wireless Mouse', 'Accessories', 800.00, 350.00),
('Keyboard', 'Accessories', 1500.00, 700.00),
('Smartphone', 'Electronics', 25000.00, 18000.00),
('Headphones', 'Accessories', 2000.00, 900.00),
('Monitor', 'Electronics', 12000.00, 8500.00),
('Office Chair', 'Furniture', 7500.00, 5000.00),
('Desk', 'Furniture', 10000.00, 7000.00),
('USB Cable', 'Accessories', 300.00, 100.00),
('Printer', 'Electronics', 15000.00, 11000.00);
INSERT INTO stores (store_name, region, city) VALUES
('Chennai Central Store', 'South', 'Chennai'),
('Bengaluru City Store', 'South', 'Bengaluru'),
('Mumbai Retail Store', 'West', 'Mumbai'),
('Delhi Main Store', 'North', 'Delhi'),
('Hyderabad Tech Store', 'South', 'Hyderabad');
INSERT INTO employees (employee_name, store_id, job_role) VALUES
('Arun Kumar', 1, 'Sales Executive'),
('Priya Sharma', 1, 'Store Manager'),
('Rahul Verma', 2, 'Sales Executive'),
('Sneha Patel', 2, 'Cashier'),
('Vikram Singh', 3, 'Store Manager'),
('Ananya Das', 3, 'Sales Executive'),
('Karthik Raj', 4, 'Sales Executive'),
('Meera Nair', 4, 'Cashier'),
('Divya Reddy', 5, 'Store Manager'),
('Sanjay Rao', 5, 'Sales Executive');
INSERT INTO sales(product_id, store_id, employee_id, sale_date,quantity, unit_price, discount_percent) VALUES
(1, 1, 1, '2026-07-01', 2, 60000.00, 5.00),
(2, 1, 1, '2026-07-01', 10, 800.00, 0.00),
(3, 2, 3, '2026-07-02', 5, 1500.00, 2.00),
(4, 2, 4, '2026-07-03', 3, 25000.00, 5.00),
(5, 3, 6, '2026-07-04', 8, 2000.00, 10.00),
(6, 3, 5, '2026-07-05', 2, 12000.00, 0.00),
(7, 4, 7, '2026-08-01', 4, 7500.00, 5.00),
(8, 4, 8, '2026-08-02', 2, 10000.00, 0.00),
(9, 5, 10, '2026-08-03', 20, 300.00, 0.00),
(10, 5, 9, '2026-08-04', 3, 15000.00, 8.00),
(1, 2, 3, '2026-08-10', 1, 60000.00, 0.00),
(2, 3, 6, '2026-08-12', 15, 800.00, 5.00),
(4, 5, 10, '2026-09-01', 2, 25000.00, 3.00),
(5, 1, 2, '2026-09-05', 6, 2000.00, 0.00),
(6, 2, 4, '2026-09-10', 4, 12000.00, 5.00),
(7, 3, 5, '2026-09-15', 3, 7500.00, 0.00),
(8, 5, 9, '2026-09-20', 1, 10000.00, 10.00),
(3, 4, 8, '2026-09-25', 7, 1500.00, 0.00),
(10, 1, 1, '2026-10-01', 2, 15000.00, 5.00),
(9, 2, 4, '2026-10-02', 30, 300.00, 0.00);
SELECT COUNT(*) AS total_products FROM products;
SELECT COUNT(*) AS total_stores FROM stores;
SELECT COUNT(*) AS total_employees FROM employees;
SELECT COUNT(*) AS total_sales FROM sales;
SELECT * FROM products;
SELECT * FROM stores;
SELECT * FROM employees;
SELECT * FROM sales;
SELECT st.store_name,st.region,SUM(s.quantity * s.unit_price *(1 - s.discount_percent / 100)) AS total_revenue
FROM sales s JOIN stores st ON s.store_id = st.store_id GROUP BY st.store_id, st.store_name, st.region
ORDER BY total_revenue DESC;
INSERT INTO sales(product_id, store_id, employee_id, sale_date,quantity, unit_price, discount_percent) VALUES
(1, 1, 1, '2026-10-05', 2, 60000, 5);
SELECT * FROM sales WHERE sale_date = '2026-10-05';
UPDATE sales SET discount_percent = 10 WHERE sale_date = '2026-10-05' AND product_id = 1 AND store_id = 1;
SELECT * FROM sales WHERE sale_date = '2026-10-05' AND product_id = 1 AND store_id = 1;
DELIMITER //
CREATE PROCEDURE GetDailySales
(
    IN p_store_id INT,
    IN p_sale_date DATE
)
BEGIN
    SELECT
        st.store_name,
        s.sale_date,
        SUM(
            s.quantity * s.unit_price *
            (1 - s.discount_percent / 100)
        ) AS daily_revenue,
        SUM(s.quantity) AS total_units_sold,
        COUNT(s.sale_id) AS number_of_sales
    FROM sales s
    JOIN stores st
        ON s.store_id = st.store_id
    WHERE s.store_id = p_store_id
      AND s.sale_date = p_sale_date
    GROUP BY st.store_name, s.sale_date;
END //
DELIMITER ;
CALL GetDailySales(1, '2026-07-01');
SELECT s.sale_id, s.sale_date, s.product_id, p.product_name, p.category, p.cost, s.store_id, st.store_name, st.region, s.employee_id,
s.quantity, s.unit_price, s.discount_percent FROM sales s INNER JOIN products p ON s.product_id = p.product_id
INNER JOIN stores st ON s.store_id = st.store_id ORDER BY s.sale_date;