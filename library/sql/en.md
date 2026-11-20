# @lesson sql-intro
title: SQL introduction
summary: What databases and SQL are.
---
A **database** is an organized place to keep data in **tables**. Each table has columns (fields) and rows (records), like a spreadsheet, but more powerful and faster.

**SQL** (said "sequel" or "S-Q-L") is the language we use to ask a database questions and change its data. Systems such as MySQL, PostgreSQL, SQLite, SQL Server and MariaDB all speak it.

## Your first query

This course comes with a ready-made shop database. Press **Run**:

```try sql shop
SELECT * FROM customers;
```

:::info What happens when you run it?
Every run starts with a fresh copy of the shop database inside your browser. Try anything, even deleting; you cannot break anything.
:::

```quiz
? What is SQL for?
- Designing pages
* Working with databases
- Drawing pictures

? Data in a relational database is kept in tables.
= true
```

# @lesson sql-database
title: The shop database
summary: The four tables used in every lesson.
---
The course database has four tables:

```reference sql
customers | Customers: id, name, city, country, joined | SELECT * FROM customers;
products | Products: id, name, category, price | SELECT * FROM products;
orders | Orders: id, customer_id, order_date | SELECT * FROM orders;
order_items | Order lines: order_id, product_id, quantity | SELECT * FROM order_items;
```

Try showing each table by changing its name:

```try sql shop
SELECT * FROM products;
```

## How the tables relate

- Every order in `orders` belongs to a customer: `orders.customer_id` equals `customers.id`.
- Every line in `order_items` links an order to a product and a quantity.

```try sql shop
SELECT * FROM order_items WHERE order_id = 1;
```

:::tip Primary and foreign keys
`id` in each table is a **primary key**: a unique number for every row. `customer_id` is a **foreign key**: it points to a row in another table.
:::

```quiz
? Which column links an order to its customer?
* orders.customer_id
- orders.order_date
- customers.city

? A primary key is a unique value for every row.
= true
```

# @lesson sql-select
title: SELECT
summary: Picking columns, distinct values, and aliases.
---
`SELECT` picks the columns and `FROM` names the table:

```try sql shop
SELECT name, city FROM customers;
```

- `*` means every column.
- The semicolon `;` ends the query.

## Values without repeats

```try sql shop
SELECT DISTINCT country FROM customers;
```

## Aliases and calculations

```try sql shop
SELECT name AS product, price, price * 1.15 AS price_with_tax
FROM products;
```

:::tip Keywords
`SELECT` and `select` are the same, but writing keywords in capitals makes the query easier to read.
:::

```exercise sql
? Complete the query to list countries without repeats
SELECT ___ country FROM customers;
= DISTINCT
```

```quiz
? What does * mean in SELECT * FROM products?
* Every column
- Every table
- Only the first row

? AS gives a column another name in the result.
= true
```

# @lesson sql-where
title: WHERE
summary: Filtering rows with conditions, and AND, OR and NOT.
---
`WHERE` returns only the rows that meet the condition:

```try sql shop
SELECT name, price FROM products
WHERE price > 500;
```

```reference sql
= | Equal | WHERE city = 'Riyadh'
<> | Not equal | WHERE country <> 'Egypt'
> < >= <= | Comparison | WHERE price >= 100
AND | Both conditions | WHERE price > 100 AND category = 'Furniture'
OR | Either condition | WHERE city = 'Dubai' OR city = 'Jeddah'
NOT | Negation | WHERE NOT country = 'Egypt'
```

```try sql shop
SELECT name, city FROM customers
WHERE country = 'Saudi Arabia' AND city = 'Riyadh';
```

:::warning Text in single quotes
Write text like this: `'Riyadh'`. Numbers have no quotes: `price > 500`.
:::

```exercise sql
? Complete the query to show only furniture
SELECT * FROM products
___ category = 'Furniture';
= WHERE
```

```quiz
? Which operator means "not equal" in SQL?
- !==
* <>
- =/=

? A condition with AND returns the row if only one of the two conditions holds.
= false
> AND needs both conditions; OR needs only one.
```

# @lesson sql-order-by
title: ORDER BY
summary: Sorting results up and down, and by several columns.
---
```try sql shop
SELECT name, price FROM products
ORDER BY price DESC;
```

- `ASC` ascending (the default).
- `DESC` descending.

## Sorting by several columns

```try sql shop
SELECT name, category, price FROM products
ORDER BY category, price DESC;
```

This sorts by category first, then by price from highest within each category.

```exercise sql
? Sort customers by the date they joined, newest first
SELECT name, joined FROM customers
ORDER BY joined ___;
= DESC
```

```quiz
? What is the default order in ORDER BY?
* Ascending ASC
- Descending DESC
- Random

? You can sort by more than one column.
= true
```

# @lesson sql-like-in-between
title: LIKE, IN and BETWEEN
summary: Pattern search, lists, and ranges.
---
## LIKE

A pattern search: `%` is any number of characters, `_` is one character:

```try sql shop
SELECT name FROM customers
WHERE name LIKE '%Ali%';
```

## IN

The value is one of a list:

```try sql shop
SELECT name, city FROM customers
WHERE city IN ('Riyadh', 'Dubai', 'Amman');
```

## BETWEEN

The value is in a range (both ends included):

```try sql shop
SELECT name, price FROM products
WHERE price BETWEEN 100 AND 1000;
```

```reference sql
LIKE 'S%' | Starts with S | WHERE name LIKE 'S%'
LIKE '%a' | Ends with a | WHERE name LIKE '%a'
LIKE '%x%' | Contains x | WHERE name LIKE '%Laptop%'
IN (…) | In a list | WHERE id IN (1, 3, 5)
BETWEEN a AND b | In a range | WHERE price BETWEEN 10 AND 50
```

```exercise sql
? Show the orders of the first quarter of 2025
SELECT * FROM orders
WHERE order_date ___ '2025-01-01' AND '2025-03-31';
= BETWEEN
```

```quiz
? What does % mean in LIKE?
* Any number of characters
- Exactly one character
- Only a digit

? BETWEEN 100 AND 1000 includes both 100 and 1000.
= true
```

# @lesson sql-null
title: Empty values: NULL
summary: IS NULL and IS NOT NULL, and COALESCE.
---
`NULL` means "there is no value". The customer Huda in the database has no city recorded:

```try sql shop
SELECT name, city FROM customers
WHERE city IS NULL;
```

:::warning Do not use = NULL
`city = NULL` never returns anything. Use `IS NULL` and `IS NOT NULL`.
:::

```try sql shop
SELECT name, city FROM customers
WHERE city IS NOT NULL;
```

## A fallback value

`COALESCE` returns the first value that is not empty:

```try sql shop
SELECT name, COALESCE(city, 'unknown') AS city
FROM customers;
```

```exercise sql
? Show the customers with no city
SELECT name FROM customers
WHERE city ___ NULL;
= IS
```

```quiz
? How do you look for empty values?
- WHERE city = NULL
* WHERE city IS NULL
- WHERE city == ''

? COALESCE returns the first value that is not empty.
= true
```

# @lesson sql-limit
title: LIMIT
summary: Limiting the number of rows, and skipping with OFFSET.
---
```try sql shop
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 3;
```

This shows the three most expensive products.

## Pages with OFFSET

```try sql shop
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 3 OFFSET 3;
```

It skips the first three and shows the next three; this is how "next page" works on websites.

:::info Other systems
`LIMIT` works in SQLite, MySQL and PostgreSQL. In SQL Server you write `SELECT TOP 3 …`.
:::

```exercise sql
? Show the two cheapest products
SELECT name, price FROM products
ORDER BY price
___ 2;
= LIMIT
```

```quiz
? What does OFFSET 5 do?
* Skips the first five rows
- Shows only five rows
- Deletes five rows

? To show the most expensive products, sort descending and then use LIMIT.
= true
```

# @lesson sql-aggregates
title: Aggregate functions
summary: COUNT, SUM, AVG, MIN and MAX.
---
Aggregate functions compute one value from many rows:

```try sql shop
SELECT
  COUNT(*) AS products_count,
  MIN(price) AS cheapest,
  MAX(price) AS most_expensive,
  ROUND(AVG(price), 2) AS average_price,
  SUM(price) AS total
FROM products;
```

```reference sql
COUNT(*) | Number of rows | SELECT COUNT(*) FROM orders;
COUNT(col) | Number of non-empty values | SELECT COUNT(city) FROM customers;
SUM(col) | Total | SELECT SUM(quantity) FROM order_items;
AVG(col) | Average | SELECT AVG(price) FROM products;
MIN(col) / MAX(col) | Smallest / largest | SELECT MAX(price) FROM products;
```

```try sql shop
SELECT COUNT(*) AS all_customers, COUNT(city) AS with_city
FROM customers;
```

```exercise sql
? Count the orders
SELECT ___(*) FROM orders;
= COUNT
```

```quiz
? Which function computes the average?
- SUM
* AVG
- MEAN

? COUNT(city) does not count empty (NULL) values.
= true
```

# @lesson sql-group-by
title: GROUP BY and HAVING
summary: Grouping by a column, and filtering groups.
---
`GROUP BY` splits rows into groups, and aggregate functions compute a value for each group:

```try sql shop
SELECT category, COUNT(*) AS items, ROUND(AVG(price)) AS avg_price
FROM products
GROUP BY category;
```

```try sql shop
SELECT country, COUNT(*) AS customers
FROM customers
GROUP BY country
ORDER BY customers DESC;
```

## HAVING

`WHERE` filters rows **before** grouping; `HAVING` filters groups **after**:

```try sql shop
SELECT country, COUNT(*) AS customers
FROM customers
GROUP BY country
HAVING COUNT(*) > 1;
```

```exercise sql
? Complete the query to keep only categories with more than two products
SELECT category, COUNT(*) FROM products
GROUP BY category
___ COUNT(*) > 2;
= HAVING
```

```quiz
? Where do you put a condition on the COUNT(*) of each group?
- WHERE
* HAVING
- ORDER BY

? GROUP BY splits rows into groups.
= true
```

# @lesson sql-joins
title: Joining tables: JOIN
summary: INNER JOIN, LEFT JOIN, and joining more than two tables.
---
`JOIN` combines rows from two tables on a shared column:

```try sql shop
SELECT o.id AS order_id, c.name, o.order_date
FROM orders o
JOIN customers c ON c.id = o.customer_id;
```

- `o` and `c` are short names for the tables.
- `ON` gives the join condition.

## Joining three tables

```try sql shop
SELECT c.name AS customer, p.name AS product, i.quantity, p.price * i.quantity AS line_total
FROM order_items i
JOIN orders o ON o.id = i.order_id
JOIN customers c ON c.id = o.customer_id
JOIN products p ON p.id = i.product_id
ORDER BY customer;
```

## LEFT JOIN

Returns every row of the left table, even those with no match:

```try sql shop
SELECT c.name, COUNT(o.id) AS orders_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id
ORDER BY orders_count;
```

Notice Huda: she has no orders, so she shows 0. With a plain `JOIN` she would not appear at all.

```reference sql
INNER JOIN / JOIN | Only rows that match in both tables | FROM a JOIN b ON b.a_id = a.id
LEFT JOIN | Every left row + matching right rows | FROM a LEFT JOIN b ON …
RIGHT JOIN | Every right row + matching left rows | FROM a RIGHT JOIN b ON …
FULL JOIN | Every row from both sides | FROM a FULL JOIN b ON …
```

```exercise sql
? Complete the query to show every customer, even those with no order
SELECT c.name, o.id FROM customers c
___ JOIN orders o ON o.customer_id = c.id;
= LEFT
```

```quiz
? Which join returns every row of the left table, even without a match?
- INNER JOIN
* LEFT JOIN
- CROSS JOIN

? ON gives the join condition between the two tables.
= true
```

# @lesson sql-subqueries
title: Subqueries
summary: A query inside a query, IN, and EXISTS.
---
A subquery is written in parentheses and its result is used by another query:

```try sql shop
SELECT name, price FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

This shows the products that cost more than the average.

## With IN

```try sql shop
SELECT name FROM customers
WHERE id IN (SELECT customer_id FROM orders WHERE order_date >= '2025-04-01');
```

## With EXISTS

```try sql shop
SELECT name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.product_id = p.id);
```

Did anything show? If not, every product has been ordered at least once.

```quiz
? Where is a subquery written?
* In parentheses ( )
- In quotes
- After the semicolon

? EXISTS holds if the subquery returns at least one row.
= true
```

# @lesson sql-insert
title: INSERT
summary: Adding one row or several.
---
```try sql shop
INSERT INTO products (name, category, price)
VALUES ('Monitor', 'Electronics', 900);

SELECT * FROM products WHERE category = 'Electronics';
```

- List the column names, then the values in the same order.
- The `id` column gets a new number automatically because it is the primary key.

## Several rows

```try sql shop
INSERT INTO customers (name, city, country, joined) VALUES
  ('Rami Fouad', 'Beirut', 'Lebanon', '2025-07-01'),
  ('Salma Youssef', 'Doha', 'Qatar', '2025-07-03');

SELECT name, country FROM customers ORDER BY id DESC LIMIT 2;
```

```exercise sql
? Complete the statement to add a new product
___ INTO products (name, category, price)
VALUES ('Ruler', 'Stationery', 5);
= INSERT
```

```quiz
? Which keyword comes before the list of values in INSERT?
* VALUES
- SET
- WITH

? You can add several rows with one INSERT statement.
= true
```

# @lesson sql-update-delete
title: UPDATE and DELETE
summary: Changing and deleting data safely.
---
## UPDATE

```try sql shop
UPDATE products SET price = price * 0.9
WHERE category = 'Furniture';

SELECT name, price FROM products WHERE category = 'Furniture';
```

## DELETE

```try sql shop
DELETE FROM order_items WHERE quantity > 10;

SELECT * FROM order_items;
```

:::danger Do not forget WHERE
`UPDATE products SET price = 0;` without `WHERE` changes **every** row, and `DELETE FROM customers;` deletes **all** of them. Write `WHERE` first, and test the condition with `SELECT` before changing anything.
:::

```exercise sql
? Complete the statement to change the city of customer 8
UPDATE customers ___ city = 'Kuwait City'
WHERE id = 8;
= SET
```

```quiz
? What happens when you run DELETE FROM products; without WHERE?
- Nothing happens
* Every row is deleted
- The table itself is deleted

? SET gives the new column values in UPDATE.
= true
```

# @lesson sql-create-table
title: Creating tables
summary: CREATE TABLE, data types, constraints, ALTER and DROP.
---
```try sql
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  salary REAL CHECK (salary > 0),
  hired TEXT DEFAULT CURRENT_DATE
);

INSERT INTO employees (name, email, salary) VALUES ('Ali', 'ali@example.com', 9000);
SELECT * FROM employees;
```

```reference sql
PRIMARY KEY | Unique id for each row | id INTEGER PRIMARY KEY
NOT NULL | A value is required | name TEXT NOT NULL
UNIQUE | No repeats | email TEXT UNIQUE
DEFAULT | Default value | status TEXT DEFAULT 'active'
CHECK | A condition on the value | CHECK (price >= 0)
FOREIGN KEY | Points to another table | FOREIGN KEY (customer_id) REFERENCES customers(id)
ALTER TABLE | Change a table | ALTER TABLE t ADD COLUMN phone TEXT;
DROP TABLE | Delete the whole table | DROP TABLE t;
```

Try adding an employee with no name or a negative salary to see the constraints stop you:

```try sql
CREATE TABLE t (name TEXT NOT NULL, salary REAL CHECK (salary > 0));
INSERT INTO t VALUES (NULL, 100);
```

```quiz
? Which constraint stops a value from repeating in a column?
- NOT NULL
* UNIQUE
- DEFAULT

? DROP TABLE deletes the table and all its data.
= true
```

# @lesson sql-reference
title: SQL reference
summary: The most important statements and keywords with an example for each.
type: Reference
---
Search the table for any statement.

```reference sql
SELECT | Pick columns | SELECT name, price FROM products;
DISTINCT | Without repeats | SELECT DISTINCT country FROM customers;
WHERE | Filter rows | WHERE price > 100
AND / OR / NOT | Combine conditions | WHERE a = 1 AND b = 2
ORDER BY | Sort | ORDER BY price DESC
LIMIT / OFFSET | Number of rows | LIMIT 10 OFFSET 20
LIKE | Pattern search | WHERE name LIKE '%Ali%'
IN | In a list | WHERE id IN (1, 2)
BETWEEN | In a range | WHERE price BETWEEN 10 AND 50
IS NULL | Empty value | WHERE city IS NULL
AS | Alias | SELECT price AS p
COUNT / SUM / AVG | Aggregate functions | SELECT COUNT(*) FROM orders;
MIN / MAX | Smallest and largest | SELECT MAX(price) FROM products;
GROUP BY | Grouping | GROUP BY category
HAVING | Filter groups | HAVING COUNT(*) > 1
JOIN … ON | Join | JOIN customers c ON c.id = o.customer_id
LEFT JOIN | Join keeping the left side | LEFT JOIN orders o ON …
INSERT INTO | Add | INSERT INTO t (a) VALUES (1);
UPDATE … SET | Change | UPDATE t SET a = 2 WHERE id = 1;
DELETE FROM | Delete | DELETE FROM t WHERE id = 1;
CREATE TABLE | Create a table | CREATE TABLE t (id INTEGER PRIMARY KEY);
ALTER TABLE | Change a table | ALTER TABLE t ADD COLUMN b TEXT;
DROP TABLE | Delete a table | DROP TABLE t;
COALESCE | First non-empty value | COALESCE(city, '-')
ROUND | Rounding | ROUND(AVG(price), 2)
```

:::tip What next?
Practise by asking your own questions of the shop database: which customer ordered most? Which category sells most? How much did each customer spend?
:::
