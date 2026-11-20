CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT, country TEXT, joined TEXT);
INSERT INTO customers VALUES
 (1, 'Sara Ahmed', 'Riyadh', 'Saudi Arabia', '2024-01-15'),
 (2, 'Omar Khaled', 'Cairo', 'Egypt', '2024-03-02'),
 (3, 'Layla Hassan', 'Dubai', 'UAE', '2024-05-20'),
 (4, 'Nour Mohamed', 'Jeddah', 'Saudi Arabia', '2024-07-11'),
 (5, 'Khaled Ali', 'Alexandria', 'Egypt', '2025-01-08'),
 (6, 'Mona Saeed', 'Amman', 'Jordan', '2025-02-19'),
 (7, 'Youssef Ibrahim', 'Riyadh', 'Saudi Arabia', '2025-04-30'),
 (8, 'Huda Kamal', NULL, 'Kuwait', '2025-06-12');
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES
 (1, 'Laptop', 'Electronics', 3500),
 (2, 'Smartphone', 'Electronics', 2200),
 (3, 'Headphones', 'Electronics', 250),
 (4, 'Office chair', 'Furniture', 600),
 (5, 'Wooden desk', 'Furniture', 1200),
 (6, 'Notebook', 'Stationery', 15),
 (7, 'Colored pens', 'Stationery', 25),
 (8, 'Backpack', 'Accessories', 180);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT);
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-01-12'), (3, 1, '2025-02-03'), (4, 3, '2025-02-15'),
 (5, 4, '2025-03-01'), (6, 5, '2025-03-18'), (7, 2, '2025-04-05'), (8, 7, '2025-04-22'),
 (9, 3, '2025-05-09'), (10, 6, '2025-05-30');
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, quantity INTEGER);
INSERT INTO order_items VALUES
 (1, 1, 1), (1, 3, 2), (2, 2, 1), (3, 6, 10), (3, 7, 5), (4, 4, 2), (4, 5, 1),
 (5, 2, 1), (5, 8, 1), (6, 3, 3), (7, 6, 20), (8, 1, 1), (8, 4, 1), (9, 7, 4), (10, 8, 2);
