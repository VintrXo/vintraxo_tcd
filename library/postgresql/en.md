# @lesson pg-intro
title: PostgreSQL introduction
summary: What PostgreSQL is, the sample company database, and your first query.
---
**PostgreSQL** (often "Postgres") is a free, open-source relational database known for being reliable, standards-compliant and rich in features: JSON, full-text search, window functions, custom types and much more. Banks, governments and web companies run it at large scale.

The examples in this course run on a **real PostgreSQL** inside your browser. Each run starts with a fresh copy of a small company database:

| Table | What it holds |
|---|---|
| `departments` | id, name, city |
| `employees` | id, name, department_id, job, salary, hired_on, manager_id, email |
| `customers` | id, name, city, joined_on |
| `products` | id, name, category, price |
| `orders` | id, customer_id, sales_rep_id, ordered_on, status |
| `order_items` | order_id, product_id, qty |

```try html pg
<script type="text/postgresql">
SELECT version();
SELECT name, job, salary FROM employees;
</script>
```

- SQL statements end with `;`. You can run several at once; each result appears as a table.
- An example can have several `<script type="text/postgresql">` blocks; each runs on its own, so an error in one does not hide the others.
- Keywords like `SELECT` are not case-sensitive, but writing them in capitals makes queries easier to read.

:::info On your own computer
Install PostgreSQL from postgresql.org (or with Docker: `docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres`), then connect with the `psql` command-line tool or a graphical client such as pgAdmin or DBeaver.
:::

```quiz
? What kind of database is PostgreSQL?
* A relational database that uses SQL
- A spreadsheet program
- A file storage service

? PostgreSQL is free and open source.
= true
```

# @lesson pg-select
title: Selecting and filtering rows
summary: SELECT, WHERE, ORDER BY, LIMIT, DISTINCT and pattern matching.
---
```try html pg
<script type="text/postgresql">
SELECT name, salary
FROM employees
WHERE salary >= 15000 AND department_id = 1
ORDER BY salary DESC;

SELECT name, hired_on FROM employees
WHERE hired_on BETWEEN '2020-01-01' AND '2022-12-31'
ORDER BY hired_on;

SELECT name, email FROM employees WHERE email IS NULL;

SELECT name FROM customers WHERE name ILIKE '%tech%' OR city IN ('Giza', 'Sharm');

SELECT DISTINCT category FROM products ORDER BY category;

SELECT name, price FROM products ORDER BY price DESC LIMIT 3 OFFSET 1;
</script>
```

```reference sql
SELECT a, b FROM t | Choose columns | SELECT name, price FROM products
WHERE cond | Filter rows | WHERE salary > 20000
AND / OR / NOT | Combine conditions | WHERE city = 'Cairo' AND salary > 1
BETWEEN a AND b | Inclusive range | WHERE hired_on BETWEEN '2020-01-01' AND '2020-12-31'
IN (...) | One of several values | WHERE status IN ('pending', 'shipped')
LIKE / ILIKE | Pattern (ILIKE ignores case) | WHERE name ILIKE 'sa%'
IS NULL / IS NOT NULL | Missing values | WHERE email IS NULL
ORDER BY col DESC | Sort | ORDER BY salary DESC, name
LIMIT n OFFSET m | Page through results | LIMIT 10 OFFSET 20
DISTINCT | Remove duplicates | SELECT DISTINCT city FROM customers
```

:::warning NULL is not equal to anything
`email = NULL` is never true, not even for missing emails. Always test missing values with `IS NULL`.
:::

```exercise sql
? Find products in the Software category
SELECT name FROM products ___ category = 'Software';
= WHERE | where
```

```quiz
? Which operator matches text patterns without caring about upper or lower case?
* ILIKE
- LIKE
- MATCH

? WHERE email = NULL finds rows where the email is missing.
= false
> Use IS NULL; comparing with NULL never gives true.
```

# @lesson pg-expressions
title: Expressions, functions and CASE
summary: Calculated columns, text and date functions, CASE and COALESCE.
---
```try html pg
<script type="text/postgresql">
SELECT name,
       salary,
       round(salary * 12) AS yearly,
       upper(job) AS job_upper,
       split_part(name, ' ', 1) AS first_name,
       coalesce(email, '(no email)') AS contact,
       hired_on,
       date_part('year', age(DATE '2026-01-01', hired_on)) AS years_at_2026,
       CASE
         WHEN salary >= 25000 THEN 'senior'
         WHEN salary >= 15000 THEN 'mid'
         ELSE 'junior'
       END AS band
FROM employees
ORDER BY salary DESC;

SELECT 7 / 2 AS int_division, 7 / 2.0 AS decimal_division, 7 % 2 AS remainder,
       length('PostgreSQL') AS len, 'Post' || 'gres' AS joined,
       DATE '2026-01-31' + INTERVAL '1 month' AS next_month,
       to_char(DATE '2026-03-05', 'DD Mon YYYY') AS formatted;
</script>
```

```reference sql
expr AS name | Name a calculated column | salary * 12 AS yearly
round / ceil / floor | Rounding | round(price * 1.14, 2)
upper / lower / length | Text basics | lower(email)
|| / concat | Join text | first_name || ' ' || last_name
split_part / substring / replace | Parts of text | split_part(name, ' ', 1)
coalesce(a, b) | First value that is not NULL | coalesce(email, 'n/a')
CASE WHEN ... THEN ... END | Conditions inside a query | CASE WHEN qty > 10 THEN 'bulk' END
now() / current_date | Current time / date | WHERE ordered_on > current_date - 30
INTERVAL / age() / date_part | Date arithmetic | hired_on + INTERVAL '90 days'
to_char | Format dates and numbers | to_char(now(), 'YYYY-MM')
```

:::tip Integer division
`7 / 2` is `3` because both numbers are integers. Write `7 / 2.0` or cast with `7::numeric / 2` to keep decimals.
:::

```exercise sql
? Show "unknown" when city is NULL
SELECT name, ___(city, 'unknown') FROM customers;
= coalesce | COALESCE
```

```quiz
? What does CASE do in a query?
* Chooses a value based on conditions, row by row
- Changes upper and lower case
- Creates a new table
```

# @lesson pg-aggregate
title: Grouping and aggregates
summary: COUNT, SUM, AVG, GROUP BY, HAVING and FILTER.
---
```try html pg
<script type="text/postgresql">
SELECT count(*) AS employees, round(avg(salary)) AS avg_salary,
       min(salary) AS lowest, max(salary) AS highest, sum(salary) AS payroll
FROM employees;

SELECT department_id, count(*) AS people, round(avg(salary)) AS avg_salary
FROM employees
GROUP BY department_id
ORDER BY department_id NULLS LAST;

SELECT status, count(*) AS orders
FROM orders
GROUP BY status
HAVING count(*) >= 2;

SELECT count(*) AS total,
       count(*) FILTER (WHERE status = 'delivered') AS delivered,
       count(*) FILTER (WHERE status = 'cancelled') AS cancelled
FROM orders;

SELECT category, string_agg(name, ', ' ORDER BY name) AS products
FROM products GROUP BY category ORDER BY category;
</script>
```

```reference sql
count(*) / count(col) | Rows / non-NULL values | count(email)
sum / avg / min / max | Totals and extremes | sum(qty)
GROUP BY col | One result row per group | GROUP BY category
HAVING cond | Filter groups (after grouping) | HAVING sum(qty) > 10
agg FILTER (WHERE ...) | Aggregate only some rows | count(*) FILTER (WHERE paid)
string_agg / array_agg | Collect values into text / an array | string_agg(name, ', ')
```

:::tip WHERE or HAVING?
`WHERE` filters rows **before** grouping; `HAVING` filters the groups **after** aggregates are calculated. "Departments whose average salary is above 20,000" needs `HAVING avg(salary) > 20000`.
:::

```exercise sql
? Keep only categories with more than one product
SELECT category, count(*) FROM products GROUP BY category ___ count(*) > 1;
= HAVING | having
```

```quiz
? Which clause filters groups after aggregation?
* HAVING
- WHERE
- ORDER BY

? count(email) counts only rows where email is not NULL.
= true
```

# @lesson pg-joins
title: Joining tables
summary: INNER JOIN, LEFT JOIN, joining several tables and self-joins.
---
```try html pg
<script type="text/postgresql">
-- inner join: only employees that have a department
SELECT e.name, d.name AS department, d.city
FROM employees e
JOIN departments d ON d.id = e.department_id
ORDER BY d.name, e.name;

-- left join: every employee, department or not
SELECT e.name, coalesce(d.name, '-') AS department
FROM employees e
LEFT JOIN departments d ON d.id = e.department_id
WHERE d.id IS NULL;

-- several tables: what each customer bought
SELECT c.name AS customer, o.id AS order_id, p.name AS product, oi.qty, oi.qty * p.price AS line_total
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status <> 'cancelled'
ORDER BY o.id;

-- self join: each employee with their manager
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id
ORDER BY manager NULLS FIRST, employee;
</script>
```

| Join | Returns |
|---|---|
| `JOIN` (inner) | Only rows that match in both tables |
| `LEFT JOIN` | Every row of the left table; NULLs where the right side has no match |
| `RIGHT JOIN` | The opposite of LEFT |
| `FULL JOIN` | Every row from both sides |

```exercise sql
? Keep every customer even if they have no orders
SELECT c.name, o.id FROM customers c ___ JOIN orders o ON o.customer_id = c.id;
= LEFT | left
```

```quiz
? Which join returns only the rows that match in both tables?
* INNER JOIN
- LEFT JOIN
- FULL JOIN
```

# @lesson pg-subqueries
title: Subqueries and CTEs
summary: Queries inside queries, EXISTS, and readable steps with WITH.
---
```try html pg
<script type="text/postgresql">
-- employees paid more than the company average
SELECT name, salary FROM employees
WHERE salary > (SELECT avg(salary) FROM employees)
ORDER BY salary DESC;

-- customers who placed at least one delivered order
SELECT name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status = 'delivered');

-- a CTE names each step, top to bottom
WITH order_totals AS (
  SELECT o.id, o.customer_id, sum(oi.qty * p.price) AS total
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  JOIN products p ON p.id = oi.product_id
  WHERE o.status <> 'cancelled'
  GROUP BY o.id, o.customer_id
),
customer_totals AS (
  SELECT customer_id, count(*) AS orders, sum(total) AS revenue
  FROM order_totals GROUP BY customer_id
)
SELECT c.name, ct.orders, ct.revenue
FROM customer_totals ct JOIN customers c ON c.id = ct.customer_id
ORDER BY ct.revenue DESC;
</script>
```

```reference sql
(SELECT ...) | A subquery used as a value or a list | WHERE price > (SELECT avg(price) FROM products)
IN (SELECT ...) | Match any value from a subquery | WHERE id IN (SELECT customer_id FROM orders)
EXISTS (SELECT 1 ...) | Is there at least one matching row? | WHERE EXISTS (SELECT 1 FROM orders o WHERE ...)
WITH name AS (...) | Common table expression (CTE) | WITH totals AS (SELECT ...) SELECT * FROM totals
WITH RECURSIVE | Walk trees such as org charts | WITH RECURSIVE chain AS (...)
```

:::tip CTEs make long queries readable
Instead of nesting subqueries three levels deep, give each step a name with `WITH`. Anyone reading the query can follow it from top to bottom.
:::

```exercise sql
? Start a common table expression named totals
___ totals AS (SELECT customer_id, count(*) FROM orders GROUP BY customer_id) SELECT * FROM totals;
= WITH | with
```

```quiz
? What does EXISTS check?
* Whether the subquery returns at least one row
- Whether a table exists in the database
- Whether a column has no NULLs
```

# @lesson pg-window
title: Window functions
summary: Rankings, running totals and comparisons without collapsing rows.
---
A **window function** calculates over a group of rows, like an aggregate, but keeps every row in the result. That makes rankings, running totals and "compare with the previous row" easy.

```try html pg
<script type="text/postgresql">
SELECT name, department_id, salary,
       rank() OVER (ORDER BY salary DESC) AS company_rank,
       rank() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank,
       round(avg(salary) OVER (PARTITION BY department_id)) AS dept_avg,
       salary - round(avg(salary) OVER (PARTITION BY department_id)) AS vs_dept_avg
FROM employees
WHERE department_id IS NOT NULL
ORDER BY department_id, dept_rank;

-- running total of orders by date, and the gap since the previous order
SELECT id, ordered_on,
       count(*) OVER (ORDER BY ordered_on) AS orders_so_far,
       ordered_on - lag(ordered_on) OVER (ORDER BY ordered_on) AS days_since_previous
FROM orders
ORDER BY ordered_on;

-- top earner per department
SELECT * FROM (
  SELECT name, department_id, salary,
         row_number() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
  FROM employees WHERE department_id IS NOT NULL
) ranked
WHERE rn = 1;
</script>
```

```reference sql
f() OVER (...) | Window function | sum(qty) OVER (ORDER BY ordered_on)
PARTITION BY | Restart the window per group | OVER (PARTITION BY department_id)
row_number / rank / dense_rank | Position in the window | rank() OVER (ORDER BY score DESC)
lag / lead | Previous / next row's value | lag(price) OVER (ORDER BY day)
sum / avg ... OVER | Running or group totals on every row | avg(salary) OVER (PARTITION BY dept)
```

```exercise sql
? Restart the numbering for each department
row_number() OVER (___ BY department_id ORDER BY salary DESC)
= PARTITION | partition
```

```quiz
? How is a window function different from GROUP BY?
* It keeps every row and adds the calculated value to each
- It removes duplicate rows
- It only works on text columns
```

# @lesson pg-ddl
title: Creating tables and constraints
summary: Data types, primary and foreign keys, CHECK, UNIQUE, DEFAULT and ALTER TABLE.
---
```try html pg
<script type="text/postgresql">
CREATE TABLE trainings (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title       text NOT NULL,
  department_id int REFERENCES departments(id),
  starts_on   date NOT NULL,
  seats       int NOT NULL DEFAULT 20 CHECK (seats > 0),
  fee         numeric(10,2) NOT NULL DEFAULT 0,
  code        text UNIQUE,
  created_at  timestamptz NOT NULL DEFAULT now()
);

INSERT INTO trainings (title, department_id, starts_on, code) VALUES
  ('SQL for analysts', 2, '2026-02-01', 'SQL-101'),
  ('Negotiation', 1, '2026-02-15', 'NEG-201');

ALTER TABLE trainings ADD COLUMN online boolean NOT NULL DEFAULT false;

SELECT id, title, seats, fee, code, online FROM trainings;
</script>
<script type="text/postgresql">
-- this one breaks the CHECK constraint, so PostgreSQL refuses it
INSERT INTO trainings (title, starts_on, seats) VALUES ('Broken', '2026-03-01', 0);
</script>
```

The second block fails on purpose: constraints protect the data from bad values.

| Type | Use for |
|---|---|
| `int`, `bigint` | Whole numbers, ids |
| `numeric(p, s)` | Money and exact decimals (never `float` for money) |
| `text`, `varchar(n)` | Text |
| `boolean` | true / false |
| `date`, `timestamptz` | Dates, moments in time with time zone |
| `jsonb` | Flexible JSON documents |
| `uuid` | Globally unique ids |

```reference sql
GENERATED ALWAYS AS IDENTITY | Auto-increment id | id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY
PRIMARY KEY | Unique row identifier | id int PRIMARY KEY
REFERENCES t(col) | Foreign key | customer_id int REFERENCES customers(id)
NOT NULL / UNIQUE / CHECK | Rules on values | CHECK (price >= 0)
DEFAULT value | Value when none is given | status text DEFAULT 'new'
ALTER TABLE ... ADD COLUMN | Change a table | ALTER TABLE t ADD COLUMN note text
DROP TABLE | Delete a table | DROP TABLE IF EXISTS tmp
```

```exercise sql
? Make sure the price can never be negative
price numeric(10,2) ___ (price >= 0)
= CHECK | check
```

```quiz
? Which type should store money amounts?
* numeric
- float
- text

? A foreign key makes sure a referenced row exists.
= true
```

# @lesson pg-dml
title: Inserting, updating and deleting
summary: INSERT ... RETURNING, UPDATE, DELETE and upserts with ON CONFLICT.
---
```try html pg
<script type="text/postgresql">
INSERT INTO products (id, name, category, price)
VALUES (7, 'Webcam', 'Accessories', 1500), (8, 'Headset', 'Accessories', 1200)
RETURNING id, name;

UPDATE products SET price = price * 1.10
WHERE category = 'Accessories'
RETURNING name, price;

DELETE FROM order_items WHERE order_id = 105 RETURNING *;

-- upsert: insert, or update the price if the id already exists
INSERT INTO products (id, name, category, price)
VALUES (3, 'Keyboard', 'Accessories', 950), (9, 'Docking station', 'Hardware', 4200)
ON CONFLICT (id) DO UPDATE SET price = EXCLUDED.price
RETURNING id, name, price;

SELECT id, name, price FROM products ORDER BY id;
</script>
```

```reference sql
INSERT INTO t (cols) VALUES (...) | Add rows | INSERT INTO t (a, b) VALUES (1, 'x')
RETURNING cols | Get back what was changed | INSERT ... RETURNING id
UPDATE t SET col = v WHERE ... | Change rows | UPDATE products SET price = 10 WHERE id = 3
DELETE FROM t WHERE ... | Remove rows | DELETE FROM orders WHERE status = 'cancelled'
ON CONFLICT (col) DO UPDATE | Upsert | ON CONFLICT (id) DO UPDATE SET qty = EXCLUDED.qty
ON CONFLICT DO NOTHING | Skip duplicates | INSERT ... ON CONFLICT DO NOTHING
```

:::danger UPDATE and DELETE without WHERE
`UPDATE products SET price = 0;` changes **every** row. Write the `WHERE` first, run it as a `SELECT` to see which rows match, then turn it into the `UPDATE`.
:::

```exercise sql
? Return the id of the new row after inserting it
INSERT INTO customers (id, name) VALUES (6, 'Red Sea Co') ___ id;
= RETURNING | returning
```

```quiz
? What does ON CONFLICT (id) DO UPDATE give you?
* An upsert: insert new rows and update existing ones
- A way to delete conflicts
- A faster SELECT
```

# @lesson pg-json
title: JSON in PostgreSQL
summary: jsonb columns, the -> and ->> operators, containment and building JSON.
---
PostgreSQL stores JSON in the `jsonb` type and lets you query inside it, so you can mix fixed columns with flexible data.

```try html pg
<script type="text/postgresql">
CREATE TABLE events (id serial PRIMARY KEY, payload jsonb NOT NULL);
INSERT INTO events (payload) VALUES
  ('{"type": "login", "user": "sara", "device": {"os": "Android", "app": "2.4"}}'),
  ('{"type": "purchase", "user": "omar", "amount": 1200, "items": ["Laptop bag", "Mouse"]}'),
  ('{"type": "login", "user": "lina", "device": {"os": "iOS", "app": "2.5"}}');

SELECT id,
       payload->>'type' AS type,
       payload->>'user' AS "user",
       payload->'device'->>'os' AS os,
       (payload->>'amount')::numeric AS amount,
       jsonb_array_length(coalesce(payload->'items', '[]')) AS items
FROM events;

SELECT payload->>'user' AS "user" FROM events WHERE payload @> '{"type": "login"}';

SELECT jsonb_build_object('department', d.name, 'people', jsonb_agg(e.name ORDER BY e.name)) AS doc
FROM departments d JOIN employees e ON e.department_id = d.id
GROUP BY d.name ORDER BY d.name;
</script>
```

```reference sql
jsonb | Binary JSON type | payload jsonb
-> / ->> | Get a field as JSON / as text | payload->>'user'
#>> '{a,b}' | Get a nested path as text | payload #>> '{device,os}'
@> | Contains | WHERE payload @> '{"type": "login"}'
jsonb_build_object / jsonb_agg | Build JSON | jsonb_build_object('id', id)
jsonb_array_elements | One row per array item | SELECT jsonb_array_elements(payload->'items')
```

:::tip Columns first, JSON for the rest
Put fields you filter, join and validate often in normal columns. Keep JSON for data whose shape really varies. A GIN index (`CREATE INDEX ON events USING gin (payload)`) makes `@>` searches fast.
:::

```exercise sql
? Read the user field as text
SELECT payload___'user' FROM events;
= ->>
```

```quiz
? What is the difference between -> and ->>?
* -> returns JSON, ->> returns text
- -> is faster
- ->> only works on arrays
```

# @lesson pg-performance
title: Indexes, EXPLAIN and transactions
summary: Making queries fast and keeping changes safe.
---
An **index** is a sorted structure that lets PostgreSQL find rows without reading the whole table. `EXPLAIN` shows the plan PostgreSQL chooses. A **transaction** groups changes so they happen completely or not at all.

```try html pg
<script type="text/postgresql">
CREATE TABLE visits AS
SELECT g AS id, (g % 500) AS customer_id, DATE '2025-01-01' + (g % 365) AS visited_on
FROM generate_series(1, 20000) AS g;

EXPLAIN SELECT * FROM visits WHERE customer_id = 42;
CREATE INDEX visits_customer_idx ON visits (customer_id);
ANALYZE visits;
EXPLAIN SELECT * FROM visits WHERE customer_id = 42;

-- a transfer that must happen completely or not at all
CREATE TABLE accounts (id int PRIMARY KEY, owner text, balance numeric NOT NULL CHECK (balance >= 0));
INSERT INTO accounts VALUES (1, 'Sara', 500), (2, 'Omar', 100);

BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE id = 1;
UPDATE accounts SET balance = balance + 200 WHERE id = 2;
COMMIT;

BEGIN;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
ROLLBACK;                    -- changed our mind: nothing from this block is kept

SELECT * FROM accounts ORDER BY id;
</script>
```

The first plan says **Seq Scan** (read every row); after the index it says **Index Scan** or **Bitmap Heap Scan** on `visits_customer_idx`.

```reference sql
CREATE INDEX name ON t (col) | Speed up lookups on col | CREATE INDEX ON orders (customer_id)
UNIQUE INDEX | Index that also forbids duplicates | CREATE UNIQUE INDEX ON users (lower(email))
EXPLAIN / EXPLAIN ANALYZE | Show the plan / run and time it | EXPLAIN ANALYZE SELECT ...
BEGIN / COMMIT / ROLLBACK | Transactions | BEGIN; ... COMMIT;
generate_series | Make test rows | SELECT generate_series(1, 10)
```

:::tip Index what you search by
Add indexes on columns used in `WHERE`, `JOIN` and `ORDER BY` of frequent queries, such as foreign keys. Every index also slows down inserts a little and uses space, so do not index everything.
:::

```exercise sql
? Undo all changes since BEGIN
___;
= ROLLBACK | rollback
```

```quiz
? What does a transaction guarantee?
* Its changes are kept completely or not at all
- Queries always run faster
- Tables cannot be read by others

? EXPLAIN shows how PostgreSQL plans to run a query.
= true
```

# @lesson pg-views-functions
title: Views and functions
summary: Saving queries as views, and writing SQL and PL/pgSQL functions.
---
```try html pg
<script type="text/postgresql">
CREATE VIEW order_summary AS
SELECT o.id, c.name AS customer, o.status, sum(oi.qty * p.price) AS total
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY o.id, c.name, o.status;

SELECT * FROM order_summary WHERE status = 'delivered' ORDER BY total DESC;

CREATE FUNCTION with_vat(amount numeric, rate numeric DEFAULT 0.14)
RETURNS numeric LANGUAGE sql IMMUTABLE
AS $$ SELECT round(amount * (1 + rate), 2) $$;

SELECT name, price, with_vat(price) AS price_with_vat FROM products ORDER BY price DESC LIMIT 3;

CREATE FUNCTION raise_salary(emp int, pct numeric) RETURNS numeric
LANGUAGE plpgsql AS $$
DECLARE new_salary numeric;
BEGIN
  IF pct <= 0 OR pct > 30 THEN
    RAISE EXCEPTION 'raise must be between 0 and 30 percent, got %', pct;
  END IF;
  UPDATE employees SET salary = round(salary * (1 + pct / 100), 2)
  WHERE id = emp RETURNING salary INTO new_salary;
  RETURN new_salary;
END $$;

SELECT raise_salary(2, 10) AS omar_new_salary;
</script>
<script type="text/postgresql">
SELECT raise_salary(2, 50);
</script>
```

The last call fails on purpose: the function checks its input and raises a clear error.

```reference sql
CREATE VIEW v AS SELECT ... | Save a query under a name | CREATE VIEW active_users AS SELECT ...
CREATE OR REPLACE VIEW | Change a view | CREATE OR REPLACE VIEW v AS ...
CREATE FUNCTION ... LANGUAGE sql | Function from one query | RETURNS numeric AS $$ SELECT ... $$
LANGUAGE plpgsql | Function with variables, IF, loops | DECLARE x int; BEGIN ... END
RAISE EXCEPTION | Stop with an error message | RAISE EXCEPTION 'bad value %', v
$$ ... $$ | Dollar quoting for function bodies | AS $$ ... $$
```

```exercise sql
? Save a query under the name cheap_products
CREATE ___ cheap_products AS SELECT * FROM products WHERE price < 1000;
= VIEW | view
```

```quiz
? What is a view?
* A saved query that you can select from like a table
- A copy of a table's data
- A kind of index
```

# @lesson pg-reference
title: PostgreSQL quick reference
summary: The most used statements and features on one page.
---
```reference sql
SELECT ... FROM ... WHERE ... | Read rows | SELECT name FROM employees WHERE salary > 1
ORDER BY / LIMIT / OFFSET | Sort and page | ORDER BY created_at DESC LIMIT 20
JOIN / LEFT JOIN | Combine tables | JOIN departments d ON d.id = e.department_id
GROUP BY / HAVING / FILTER | Aggregate | count(*) FILTER (WHERE paid)
WITH ... AS (...) | Readable steps (CTE) | WITH t AS (SELECT ...) SELECT * FROM t
OVER (PARTITION BY ... ORDER BY ...) | Window functions | rank() OVER (ORDER BY score DESC)
INSERT / UPDATE / DELETE ... RETURNING | Change data | UPDATE t SET a = 1 WHERE id = 2 RETURNING *
ON CONFLICT ... DO UPDATE | Upsert | ON CONFLICT (id) DO UPDATE SET qty = EXCLUDED.qty
CREATE TABLE / constraints | Define data | CHECK (price >= 0), REFERENCES t(id)
jsonb / -> / ->> / @> | JSON | WHERE payload @> '{"type": "login"}'
CREATE INDEX / EXPLAIN | Performance | CREATE INDEX ON orders (customer_id)
BEGIN / COMMIT / ROLLBACK | Transactions | BEGIN; ...; COMMIT;
CREATE VIEW / CREATE FUNCTION | Reuse | CREATE VIEW v AS SELECT ...
```

:::tip Where to go next
Install PostgreSQL locally, load a real dataset with `COPY` or `\copy` from a CSV file, and answer business questions with joins, CTEs and window functions. Then learn about roles and permissions, backups (`pg_dump`), and connecting from Python with `psycopg`.
:::

```quiz
? Which feature returns the changed rows directly from an INSERT or UPDATE?
* RETURNING
- EXPLAIN
- HAVING
```
