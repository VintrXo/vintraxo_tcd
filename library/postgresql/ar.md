# @lesson pg-intro
title: مقدمة PostgreSQL
summary: ما هي PostgreSQL، وقاعدة بيانات الشركة التجريبية، وأول استعلام لك.
---
**PostgreSQL** (وتُختصر "Postgres") قاعدة بيانات علائقية مجانية ومفتوحة المصدر، معروفة بالاعتمادية والالتزام بالمعايير وكثرة المزايا: JSON، والبحث في النصوص، ودوال النوافذ، والأنواع المخصصة وغيرها كثير. تستخدمها البنوك والحكومات وشركات الويب على نطاق واسع.

أمثلة هذه الدورة تعمل على **PostgreSQL حقيقية** داخل متصفحك. وكل تشغيل يبدأ بنسخة جديدة من قاعدة بيانات شركة صغيرة:

| الجدول | ماذا يحتوي |
|---|---|
| `departments` | id، name، city |
| `employees` | id، name، department_id، job، salary، hired_on، manager_id، email |
| `customers` | id، name، city، joined_on |
| `products` | id، name، category، price |
| `orders` | id، customer_id، sales_rep_id، ordered_on، status |
| `order_items` | order_id، product_id، qty |

```try html pg
<script type="text/postgresql">
SELECT version();
SELECT name, job, salary FROM employees;
</script>
```

- تنتهي جمل SQL بـ `;`، ويمكنك تشغيل عدة جمل معًا، وتظهر كل نتيجة كجدول.
- يمكن أن يحتوي المثال على عدة كتل `<script type="text/postgresql">`، وكل كتلة تعمل وحدها، فالخطأ في إحداها لا يخفي نتائج الأخرى.
- الكلمات المحجوزة مثل `SELECT` لا تتأثر بحالة الأحرف، لكن كتابتها بحروف كبيرة تجعل الاستعلام أسهل في القراءة.

:::info على جهازك
ثبّت PostgreSQL من postgresql.org (أو عبر Docker: `docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres`)، ثم اتصل بأداة سطر الأوامر `psql` أو بواجهة رسومية مثل pgAdmin أو DBeaver.
:::

```quiz
? ما نوع قاعدة بيانات PostgreSQL؟
* قاعدة بيانات علائقية تستخدم SQL
- برنامج جداول حسابية
- خدمة لتخزين الملفات

? تُعد PostgreSQL مجانية ومفتوحة المصدر.
= true
```

# @lesson pg-select
title: اختيار الصفوف وتصفيتها
summary: SELECT و WHERE و ORDER BY و LIMIT و DISTINCT ومطابقة الأنماط.
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
SELECT a, b FROM t | اختيار الأعمدة | SELECT name, price FROM products
WHERE cond | تصفية الصفوف | WHERE salary > 20000
AND / OR / NOT | دمج الشروط | WHERE city = 'Cairo' AND salary > 1
BETWEEN a AND b | نطاق شامل للطرفين | WHERE hired_on BETWEEN '2020-01-01' AND '2020-12-31'
IN (...) | واحدة من عدة قيم | WHERE status IN ('pending', 'shipped')
LIKE / ILIKE | نمط (ILIKE تتجاهل حالة الأحرف) | WHERE name ILIKE 'sa%'
IS NULL / IS NOT NULL | القيم الناقصة | WHERE email IS NULL
ORDER BY col DESC | الترتيب | ORDER BY salary DESC, name
LIMIT n OFFSET m | التصفح على صفحات | LIMIT 10 OFFSET 20
DISTINCT | حذف التكرار | SELECT DISTINCT city FROM customers
```

:::warning NULL لا تساوي أي شيء
الشرط `email = NULL` لا يكون صحيحًا أبدًا، حتى مع البريد الناقص. افحص القيم الناقصة دائمًا بـ `IS NULL`.
:::

```exercise sql
? اعرض منتجات فئة Software
SELECT name FROM products ___ category = 'Software';
= WHERE | where
```

```quiz
? أي عامل يطابق أنماط النص دون اهتمام بحالة الأحرف؟
* ILIKE
- LIKE
- MATCH

? الشرط WHERE email = NULL يجد الصفوف التي ينقصها البريد.
= false
> استخدم IS NULL؛ فالمقارنة مع NULL لا تعطي "صحيح" أبدًا.
```

# @lesson pg-expressions
title: التعبيرات والدوال و CASE
summary: الأعمدة المحسوبة، ودوال النصوص والتواريخ، و CASE و COALESCE.
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
expr AS name | تسمية عمود محسوب | salary * 12 AS yearly
round / ceil / floor | التقريب | round(price * 1.14, 2)
upper / lower / length | أساسيات النصوص | lower(email)
|| / concat | دمج النصوص | first_name || ' ' || last_name
split_part / substring / replace | أجزاء النص | split_part(name, ' ', 1)
coalesce(a, b) | أول قيمة ليست NULL | coalesce(email, 'n/a')
CASE WHEN ... THEN ... END | شروط داخل الاستعلام | CASE WHEN qty > 10 THEN 'bulk' END
now() / current_date | الوقت / التاريخ الحالي | WHERE ordered_on > current_date - 30
INTERVAL / age() / date_part | حسابات التواريخ | hired_on + INTERVAL '90 days'
to_char | تنسيق التواريخ والأرقام | to_char(now(), 'YYYY-MM')
```

:::tip قسمة الأعداد الصحيحة
ناتج `7 / 2` هو `3` لأن الرقمين صحيحان. اكتب `7 / 2.0` أو حوّل النوع بـ `7::numeric / 2` لتحتفظ بالكسور.
:::

```exercise sql
? اعرض "unknown" عندما تكون المدينة NULL
SELECT name, ___(city, 'unknown') FROM customers;
= coalesce | COALESCE
```

```quiz
? ماذا تفعل CASE في الاستعلام؟
* تختار قيمة حسب شروط، صفًا بصف
- تغيّر حالة الأحرف
- تنشئ جدولًا جديدًا
```

# @lesson pg-aggregate
title: التجميع والدوال التجميعية
summary: COUNT و SUM و AVG و GROUP BY و HAVING و FILTER.
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
count(*) / count(col) | الصفوف / القيم غير الفارغة | count(email)
sum / avg / min / max | المجاميع والقيم القصوى | sum(qty)
GROUP BY col | صف نتيجة لكل مجموعة | GROUP BY category
HAVING cond | تصفية المجموعات (بعد التجميع) | HAVING sum(qty) > 10
agg FILTER (WHERE ...) | تجميع بعض الصفوف فقط | count(*) FILTER (WHERE paid)
string_agg / array_agg | جمع القيم في نص / مصفوفة | string_agg(name, ', ')
```

:::tip WHERE أم HAVING؟
`WHERE` تصفّي الصفوف **قبل** التجميع، و `HAVING` تصفّي المجموعات **بعد** حساب الدوال التجميعية. فسؤال "الأقسام التي يزيد متوسط رواتبها عن 20,000" يحتاج `HAVING avg(salary) > 20000`.
:::

```exercise sql
? أبقِ فقط الفئات التي فيها أكثر من منتج
SELECT category, count(*) FROM products GROUP BY category ___ count(*) > 1;
= HAVING | having
```

```quiz
? أي جزء من الاستعلام يصفّي المجموعات بعد التجميع؟
* HAVING
- WHERE
- ORDER BY

? الدالة count(email) تعدّ فقط الصفوف التي ليس فيها email فارغًا.
= true
```

# @lesson pg-joins
title: ربط الجداول
summary: INNER JOIN و LEFT JOIN وربط عدة جداول وربط الجدول بنفسه.
---
```try html pg
<script type="text/postgresql">
-- ربط داخلي: الموظفون الذين لهم قسم فقط
SELECT e.name, d.name AS department, d.city
FROM employees e
JOIN departments d ON d.id = e.department_id
ORDER BY d.name, e.name;

-- ربط يسار: كل الموظفين، لهم قسم أم لا
SELECT e.name, coalesce(d.name, '-') AS department
FROM employees e
LEFT JOIN departments d ON d.id = e.department_id
WHERE d.id IS NULL;

-- عدة جداول: ماذا اشترى كل عميل
SELECT c.name AS customer, o.id AS order_id, p.name AS product, oi.qty, oi.qty * p.price AS line_total
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status <> 'cancelled'
ORDER BY o.id;

-- ربط الجدول بنفسه: كل موظف مع مديره
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id
ORDER BY manager NULLS FIRST, employee;
</script>
```

| نوع الربط | يرجع |
|---|---|
| `JOIN` (داخلي) | الصفوف المتطابقة في الجدولين فقط |
| `LEFT JOIN` | كل صفوف الجدول الأيسر، مع NULL حيث لا يوجد تطابق في الأيمن |
| `RIGHT JOIN` | عكس LEFT |
| `FULL JOIN` | كل الصفوف من الجهتين |

```exercise sql
? احتفظ بكل العملاء حتى من ليس له طلبات
SELECT c.name, o.id FROM customers c ___ JOIN orders o ON o.customer_id = c.id;
= LEFT | left
```

```quiz
? أي ربط يرجع فقط الصفوف المتطابقة في الجدولين؟
* INNER JOIN
- LEFT JOIN
- FULL JOIN
```

# @lesson pg-subqueries
title: الاستعلامات الفرعية و CTE
summary: استعلامات داخل استعلامات، و EXISTS، وخطوات واضحة باستخدام WITH.
---
```try html pg
<script type="text/postgresql">
-- الموظفون الذين يزيد راتبهم عن متوسط الشركة
SELECT name, salary FROM employees
WHERE salary > (SELECT avg(salary) FROM employees)
ORDER BY salary DESC;

-- العملاء الذين لهم طلب واحد مُسلَّم على الأقل
SELECT name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status = 'delivered');

-- CTE تسمّي كل خطوة من الأعلى إلى الأسفل
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
(SELECT ...) | استعلام فرعي كقيمة أو قائمة | WHERE price > (SELECT avg(price) FROM products)
IN (SELECT ...) | مطابقة أي قيمة من استعلام فرعي | WHERE id IN (SELECT customer_id FROM orders)
EXISTS (SELECT 1 ...) | هل يوجد صف مطابق واحد على الأقل؟ | WHERE EXISTS (SELECT 1 FROM orders o WHERE ...)
WITH name AS (...) | تعبير جدول مشترك (CTE) | WITH totals AS (SELECT ...) SELECT * FROM totals
WITH RECURSIVE | المرور على الأشجار مثل الهيكل التنظيمي | WITH RECURSIVE chain AS (...)
```

:::tip CTE تجعل الاستعلامات الطويلة مقروءة
بدل تداخل الاستعلامات الفرعية ثلاثة مستويات، سمِّ كل خطوة بـ `WITH`، فيتابع أي قارئ الاستعلام من الأعلى إلى الأسفل.
:::

```exercise sql
? ابدأ تعبير جدول مشترك اسمه totals
___ totals AS (SELECT customer_id, count(*) FROM orders GROUP BY customer_id) SELECT * FROM totals;
= WITH | with
```

```quiz
? ماذا يفحص EXISTS؟
* هل يرجع الاستعلام الفرعي صفًا واحدًا على الأقل
- هل الجدول موجود في قاعدة البيانات
- هل العمود خالٍ من NULL
```

# @lesson pg-window
title: دوال النوافذ
summary: الترتيب والمجاميع التراكمية والمقارنات دون دمج الصفوف.
---
**دالة النافذة (window function)** تحسب على مجموعة صفوف مثل الدوال التجميعية، لكنها تُبقي كل صف في النتيجة. وهذا يسهّل الترتيب والمجاميع التراكمية و"المقارنة بالصف السابق".

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

-- عدد الطلبات التراكمي حسب التاريخ، والأيام منذ الطلب السابق
SELECT id, ordered_on,
       count(*) OVER (ORDER BY ordered_on) AS orders_so_far,
       ordered_on - lag(ordered_on) OVER (ORDER BY ordered_on) AS days_since_previous
FROM orders
ORDER BY ordered_on;

-- الأعلى راتبًا في كل قسم
SELECT * FROM (
  SELECT name, department_id, salary,
         row_number() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
  FROM employees WHERE department_id IS NOT NULL
) ranked
WHERE rn = 1;
</script>
```

```reference sql
f() OVER (...) | دالة نافذة | sum(qty) OVER (ORDER BY ordered_on)
PARTITION BY | إعادة بدء النافذة لكل مجموعة | OVER (PARTITION BY department_id)
row_number / rank / dense_rank | الترتيب داخل النافذة | rank() OVER (ORDER BY score DESC)
lag / lead | قيمة الصف السابق / التالي | lag(price) OVER (ORDER BY day)
sum / avg ... OVER | مجاميع تراكمية أو للمجموعة على كل صف | avg(salary) OVER (PARTITION BY dept)
```

```exercise sql
? أعد بدء الترقيم لكل قسم
row_number() OVER (___ BY department_id ORDER BY salary DESC)
= PARTITION | partition
```

```quiz
? بماذا تختلف دالة النافذة عن GROUP BY؟
* تُبقي كل صف وتضيف القيمة المحسوبة لكل منها
- تحذف الصفوف المكررة
- تعمل فقط مع أعمدة النصوص
```

# @lesson pg-ddl
title: إنشاء الجداول والقيود
summary: أنواع البيانات، والمفاتيح الأساسية والخارجية، و CHECK و UNIQUE و DEFAULT و ALTER TABLE.
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
-- هذه تخالف قيد CHECK، فترفضها PostgreSQL
INSERT INTO trainings (title, starts_on, seats) VALUES ('Broken', '2026-03-01', 0);
</script>
```

الكتلة الثانية تفشل عن قصد: فالقيود تحمي البيانات من القيم الخاطئة.

| النوع | يُستخدم لـ |
|---|---|
| `int` و `bigint` | الأعداد الصحيحة والمعرّفات |
| `numeric(p, s)` | المال والكسور الدقيقة (لا تستخدم `float` للمال أبدًا) |
| `text` و `varchar(n)` | النصوص |
| `boolean` | صح / خطأ |
| `date` و `timestamptz` | التواريخ، واللحظات الزمنية مع المنطقة الزمنية |
| `jsonb` | مستندات JSON مرنة |
| `uuid` | معرّفات فريدة عالميًا |

```reference sql
GENERATED ALWAYS AS IDENTITY | معرّف يزيد تلقائيًا | id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY
PRIMARY KEY | معرّف فريد للصف | id int PRIMARY KEY
REFERENCES t(col) | مفتاح خارجي | customer_id int REFERENCES customers(id)
NOT NULL / UNIQUE / CHECK | قواعد على القيم | CHECK (price >= 0)
DEFAULT value | قيمة عند عدم الإدخال | status text DEFAULT 'new'
ALTER TABLE ... ADD COLUMN | تعديل جدول | ALTER TABLE t ADD COLUMN note text
DROP TABLE | حذف جدول | DROP TABLE IF EXISTS tmp
```

```exercise sql
? تأكد أن السعر لا يكون سالبًا أبدًا
price numeric(10,2) ___ (price >= 0)
= CHECK | check
```

```quiz
? أي نوع يجب أن يخزن المبالغ المالية؟
* numeric
- float
- text

? المفتاح الخارجي يضمن وجود الصف المشار إليه.
= true
```

# @lesson pg-dml
title: الإضافة والتعديل والحذف
summary: INSERT ... RETURNING و UPDATE و DELETE والإضافة أو التحديث بـ ON CONFLICT.
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

-- إضافة أو تحديث: أضف الصف، أو حدّث السعر إن كان id موجودًا
INSERT INTO products (id, name, category, price)
VALUES (3, 'Keyboard', 'Accessories', 950), (9, 'Docking station', 'Hardware', 4200)
ON CONFLICT (id) DO UPDATE SET price = EXCLUDED.price
RETURNING id, name, price;

SELECT id, name, price FROM products ORDER BY id;
</script>
```

```reference sql
INSERT INTO t (cols) VALUES (...) | إضافة صفوف | INSERT INTO t (a, b) VALUES (1, 'x')
RETURNING cols | استرجاع ما تغيّر | INSERT ... RETURNING id
UPDATE t SET col = v WHERE ... | تعديل صفوف | UPDATE products SET price = 10 WHERE id = 3
DELETE FROM t WHERE ... | حذف صفوف | DELETE FROM orders WHERE status = 'cancelled'
ON CONFLICT (col) DO UPDATE | إضافة أو تحديث (upsert) | ON CONFLICT (id) DO UPDATE SET qty = EXCLUDED.qty
ON CONFLICT DO NOTHING | تجاهل المكرر | INSERT ... ON CONFLICT DO NOTHING
```

:::danger UPDATE و DELETE بدون WHERE
الجملة `UPDATE products SET price = 0;` تغيّر **كل** الصفوف. اكتب شرط `WHERE` أولًا، وشغّله كـ `SELECT` لترى الصفوف المطابقة، ثم حوّله إلى `UPDATE`.
:::

```exercise sql
? أرجع id الصف الجديد بعد إضافته
INSERT INTO customers (id, name) VALUES (6, 'Red Sea Co') ___ id;
= RETURNING | returning
```

```quiz
? ماذا يعطيك ON CONFLICT (id) DO UPDATE؟
* إضافة الصفوف الجديدة وتحديث الموجودة (upsert)
- طريقة لحذف التعارضات
- SELECT أسرع
```

# @lesson pg-json
title: JSON في PostgreSQL
summary: أعمدة jsonb والعاملان -> و ->> والاحتواء وبناء JSON.
---
تخزن PostgreSQL بيانات JSON في النوع `jsonb` وتتيح الاستعلام داخلها، فتجمع بين الأعمدة الثابتة والبيانات المرنة.

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
jsonb | نوع JSON الثنائي | payload jsonb
-> / ->> | قراءة حقل كـ JSON / كنص | payload->>'user'
#>> '{a,b}' | قراءة مسار متداخل كنص | payload #>> '{device,os}'
@> | يحتوي | WHERE payload @> '{"type": "login"}'
jsonb_build_object / jsonb_agg | بناء JSON | jsonb_build_object('id', id)
jsonb_array_elements | صف لكل عنصر في المصفوفة | SELECT jsonb_array_elements(payload->'items')
```

:::tip الأعمدة أولًا و JSON للباقي
ضع الحقول التي تصفّي بها وتربط وتتحقق منها كثيرًا في أعمدة عادية، واحتفظ بـ JSON للبيانات التي يتغير شكلها فعلًا. وفهرس GIN (`CREATE INDEX ON events USING gin (payload)`) يجعل البحث بـ `@>` سريعًا.
:::

```exercise sql
? اقرأ حقل user كنص
SELECT payload___'user' FROM events;
= ->>
```

```quiz
? ما الفرق بين -> و ->>؟
* العامل -> يرجع JSON، و ->> يرجع نصًا
- العامل -> أسرع
- العامل ->> يعمل مع المصفوفات فقط
```

# @lesson pg-performance
title: الفهارس و EXPLAIN والمعاملات
summary: تسريع الاستعلامات والحفاظ على أمان التغييرات.
---
**الفهرس (index)** بنية مرتبة تتيح لـ PostgreSQL إيجاد الصفوف دون قراءة الجدول كله. و `EXPLAIN` تعرض الخطة التي تختارها PostgreSQL. أما **المعاملة (transaction)** فتجمع التغييرات لتحدث كاملة أو لا تحدث إطلاقًا.

```try html pg
<script type="text/postgresql">
CREATE TABLE visits AS
SELECT g AS id, (g % 500) AS customer_id, DATE '2025-01-01' + (g % 365) AS visited_on
FROM generate_series(1, 20000) AS g;

EXPLAIN SELECT * FROM visits WHERE customer_id = 42;
CREATE INDEX visits_customer_idx ON visits (customer_id);
ANALYZE visits;
EXPLAIN SELECT * FROM visits WHERE customer_id = 42;

-- تحويل يجب أن يتم كاملًا أو لا يتم إطلاقًا
CREATE TABLE accounts (id int PRIMARY KEY, owner text, balance numeric NOT NULL CHECK (balance >= 0));
INSERT INTO accounts VALUES (1, 'Sara', 500), (2, 'Omar', 100);

BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE id = 1;
UPDATE accounts SET balance = balance + 200 WHERE id = 2;
COMMIT;

BEGIN;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
ROLLBACK;                    -- تراجعنا: لا يُحفظ شيء من هذه الكتلة

SELECT * FROM accounts ORDER BY id;
</script>
```

الخطة الأولى تقول **Seq Scan** (قراءة كل الصفوف)، وبعد الفهرس تقول **Index Scan** أو **Bitmap Heap Scan** على `visits_customer_idx`.

```reference sql
CREATE INDEX name ON t (col) | تسريع البحث بالعمود | CREATE INDEX ON orders (customer_id)
UNIQUE INDEX | فهرس يمنع التكرار أيضًا | CREATE UNIQUE INDEX ON users (lower(email))
EXPLAIN / EXPLAIN ANALYZE | عرض الخطة / تشغيلها وقياس وقتها | EXPLAIN ANALYZE SELECT ...
BEGIN / COMMIT / ROLLBACK | المعاملات | BEGIN; ... COMMIT;
generate_series | توليد صفوف للتجربة | SELECT generate_series(1, 10)
```

:::tip افهرس ما تبحث به
أضف فهارس على الأعمدة المستخدمة في `WHERE` و `JOIN` و `ORDER BY` للاستعلامات المتكررة، مثل المفاتيح الخارجية. وكل فهرس يبطئ الإضافة قليلًا ويستهلك مساحة، فلا تفهرس كل شيء.
:::

```exercise sql
? تراجع عن كل التغييرات منذ BEGIN
___;
= ROLLBACK | rollback
```

```quiz
? ماذا تضمن المعاملة؟
* أن تُحفظ تغييراتها كاملة أو لا يُحفظ منها شيء
- أن تعمل الاستعلامات أسرع دائمًا
- ألا يقرأ الآخرون الجداول

? تعرض EXPLAIN كيف تخطط PostgreSQL لتنفيذ الاستعلام.
= true
```

# @lesson pg-views-functions
title: العروض والدوال
summary: حفظ الاستعلامات كعروض (views)، وكتابة دوال SQL و PL/pgSQL.
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

الكتلة الأخيرة تفشل عن قصد: فالدالة تتحقق من مدخلاتها وتُظهر رسالة خطأ واضحة.

```reference sql
CREATE VIEW v AS SELECT ... | حفظ استعلام باسم | CREATE VIEW active_users AS SELECT ...
CREATE OR REPLACE VIEW | تعديل عرض | CREATE OR REPLACE VIEW v AS ...
CREATE FUNCTION ... LANGUAGE sql | دالة من استعلام واحد | RETURNS numeric AS $$ SELECT ... $$
LANGUAGE plpgsql | دالة بمتغيرات و IF وحلقات | DECLARE x int; BEGIN ... END
RAISE EXCEPTION | التوقف برسالة خطأ | RAISE EXCEPTION 'bad value %', v
$$ ... $$ | تنصيص الدولار لجسم الدالة | AS $$ ... $$
```

```exercise sql
? احفظ استعلامًا باسم cheap_products
CREATE ___ cheap_products AS SELECT * FROM products WHERE price < 1000;
= VIEW | view
```

```quiz
? ما هو العرض (view)؟
* استعلام محفوظ يمكن الاختيار منه كأنه جدول
- نسخة من بيانات جدول
- نوع من الفهارس
```

# @lesson pg-reference
title: مرجع PostgreSQL السريع
summary: أكثر الجمل والمزايا استخدامًا في صفحة واحدة.
---
```reference sql
SELECT ... FROM ... WHERE ... | قراءة الصفوف | SELECT name FROM employees WHERE salary > 1
ORDER BY / LIMIT / OFFSET | الترتيب والتصفح | ORDER BY created_at DESC LIMIT 20
JOIN / LEFT JOIN | ربط الجداول | JOIN departments d ON d.id = e.department_id
GROUP BY / HAVING / FILTER | التجميع | count(*) FILTER (WHERE paid)
WITH ... AS (...) | خطوات مقروءة (CTE) | WITH t AS (SELECT ...) SELECT * FROM t
OVER (PARTITION BY ... ORDER BY ...) | دوال النوافذ | rank() OVER (ORDER BY score DESC)
INSERT / UPDATE / DELETE ... RETURNING | تغيير البيانات | UPDATE t SET a = 1 WHERE id = 2 RETURNING *
ON CONFLICT ... DO UPDATE | الإضافة أو التحديث | ON CONFLICT (id) DO UPDATE SET qty = EXCLUDED.qty
CREATE TABLE / constraints | تعريف البيانات | CHECK (price >= 0), REFERENCES t(id)
jsonb / -> / ->> / @> | JSON | WHERE payload @> '{"type": "login"}'
CREATE INDEX / EXPLAIN | الأداء | CREATE INDEX ON orders (customer_id)
BEGIN / COMMIT / ROLLBACK | المعاملات | BEGIN; ...; COMMIT;
CREATE VIEW / CREATE FUNCTION | إعادة الاستخدام | CREATE VIEW v AS SELECT ...
```

:::tip الخطوة التالية
ثبّت PostgreSQL على جهازك، وحمّل بيانات حقيقية بـ `COPY` أو `\copy` من ملف CSV، وأجب عن أسئلة عمل بالربط و CTE ودوال النوافذ. بعدها تعلّم الأدوار والصلاحيات، والنسخ الاحتياطي (`pg_dump`)، والاتصال من Python بمكتبة `psycopg`.
:::

```quiz
? أي ميزة ترجع الصفوف المتغيرة مباشرة من INSERT أو UPDATE؟
* RETURNING
- EXPLAIN
- HAVING
```
