# @lesson sql-intro
title: مقدمة في SQL
summary: ما هي قواعد البيانات ولغة SQL.
---
**قاعدة البيانات** مكان منظم لحفظ البيانات في **جداول**، كل جدول له أعمدة (حقول) وصفوف (سجلات)، مثل جدول بيانات Excel لكن أقوى وأسرع.

**SQL** (تُنطق «سيكول» أو «إس كيو إل») هي اللغة التي نسأل بها قاعدة البيانات ونعدّل بياناتها. تعمل بها أنظمة مثل MySQL وPostgreSQL وSQLite وSQL Server وMariaDB.

## أول استعلام

في هذه الدورة قاعدة بيانات متجر جاهزة. اضغط **تشغيل**:

```try sql shop
SELECT * FROM customers;
```

:::info ماذا يحدث عند التشغيل؟
كل تشغيل يبدأ بنسخة جديدة من قاعدة بيانات المتجر داخل متصفحك. جرّب أي شيء، حتى الحذف؛ لن تخرّب شيئًا.
:::

```quiz
? ما وظيفة SQL؟
- تصميم الصفحات
* التعامل مع قواعد البيانات
- رسم الصور

? البيانات في قاعدة البيانات العلائقية تُحفظ في جداول.
= true
```

# @lesson sql-database
title: قاعدة بيانات المتجر
summary: الجداول الأربعة التي نستخدمها في كل الدروس.
---
قاعدة بيانات الدورة فيها أربعة جداول:

```reference sql
customers | العملاء: id, name, city, country, joined | SELECT * FROM customers;
products | المنتجات: id, name, category, price | SELECT * FROM products;
orders | الطلبات: id, customer_id, order_date | SELECT * FROM orders;
order_items | بنود الطلبات: order_id, product_id, quantity | SELECT * FROM order_items;
```

جرّب عرض كل جدول بتغيير اسمه:

```try sql shop
SELECT * FROM products;
```

## العلاقات بين الجداول

- كل طلب في `orders` يخص عميلًا: `orders.customer_id` يساوي `customers.id`.
- كل بند في `order_items` يربط طلبًا بمنتج وكمية.

```try sql shop
SELECT * FROM order_items WHERE order_id = 1;
```

:::tip المفتاح الأساسي والأجنبي
`id` في كل جدول **مفتاح أساسي**: رقم فريد لكل صف. و`customer_id` **مفتاح أجنبي**: يشير إلى صف في جدول آخر.
:::

```quiz
? أي عمود يربط الطلب بالعميل؟
* orders.customer_id
- orders.order_date
- customers.city

? المفتاح الأساسي قيمة فريدة لكل صف.
= true
```

# @lesson sql-select
title: SELECT
summary: اختيار الأعمدة، والقيم المميزة، والأسماء المستعارة.
---
`SELECT` يحدد الأعمدة، و`FROM` يحدد الجدول:

```try sql shop
SELECT name, city FROM customers;
```

- `*` تعني كل الأعمدة.
- الفاصلة المنقوطة `;` تنهي الاستعلام.

## قيم بلا تكرار

```try sql shop
SELECT DISTINCT country FROM customers;
```

## أسماء مستعارة وحسابات

```try sql shop
SELECT name AS product, price, price * 1.15 AS price_with_tax
FROM products;
```

:::tip الكلمات المفتاحية
`SELECT` و `select` متساويتان؛ لكن كتابة الكلمات المفتاحية بأحرف كبيرة تجعل الاستعلام أوضح.
:::

```exercise sql
? أكمل لعرض الدول بلا تكرار
SELECT ___ country FROM customers;
= DISTINCT
```

```quiz
? ماذا تعني * في SELECT * FROM products؟
* كل الأعمدة
- كل الجداول
- أول صف فقط

? الكلمة AS تعطي العمود اسمًا مستعارًا في النتيجة.
= true
```

# @lesson sql-where
title: WHERE
summary: تصفية الصفوف بالشروط، و AND و OR و NOT.
---
`WHERE` تعيد الصفوف التي تحقق الشرط فقط:

```try sql shop
SELECT name, price FROM products
WHERE price > 500;
```

```reference sql
= | يساوي | WHERE city = 'الرياض'
<> | لا يساوي | WHERE country <> 'مصر'
> < >= <= | المقارنة | WHERE price >= 100
AND | الشرطان معًا | WHERE price > 100 AND category = 'أثاث'
OR | أحد الشرطين | WHERE city = 'دبي' OR city = 'جدة'
NOT | النفي | WHERE NOT country = 'مصر'
```

```try sql shop
SELECT name, city FROM customers
WHERE country = 'السعودية' AND city = 'الرياض';
```

:::warning النصوص بين علامتي تنصيص مفردة
اكتب النص هكذا: `'الرياض'`. الأرقام تُكتب بدون علامات: `price > 500`.
:::

```exercise sql
? أكمل لعرض منتجات قسم الأثاث فقط
SELECT * FROM products
___ category = 'أثاث';
= WHERE
```

```quiz
? أي عامل يعني «لا يساوي» في SQL؟
- !==
* <>
- =/=

? الشرط مع AND يعيد الصف إذا تحقق أحد الشرطين فقط.
= false
> AND تحتاج تحقق الشرطين معًا؛ OR يكفيها أحدهما.
```

# @lesson sql-order-by
title: ORDER BY
summary: ترتيب النتائج تصاعديًا وتنازليًا وبأكثر من عمود.
---
```try sql shop
SELECT name, price FROM products
ORDER BY price DESC;
```

- `ASC` تصاعدي (الافتراضي).
- `DESC` تنازلي.

## الترتيب بأكثر من عمود

```try sql shop
SELECT name, category, price FROM products
ORDER BY category, price DESC;
```

يرتب حسب القسم أولًا، ثم داخل كل قسم حسب السعر من الأعلى.

```exercise sql
? رتّب العملاء حسب تاريخ الانضمام من الأحدث
SELECT name, joined FROM customers
ORDER BY joined ___;
= DESC
```

```quiz
? ما الترتيب الافتراضي في ORDER BY؟
* تصاعدي ASC
- تنازلي DESC
- عشوائي

? يمكن الترتيب بأكثر من عمود.
= true
```

# @lesson sql-like-in-between
title: LIKE و IN و BETWEEN
summary: البحث بنمط، والقوائم، والنطاقات.
---
## LIKE

بحث بنمط: `%` أي عدد من الحروف، و`_` حرف واحد:

```try sql shop
SELECT name FROM customers
WHERE name LIKE '%علي%';
```

## IN

القيمة واحدة من قائمة:

```try sql shop
SELECT name, city FROM customers
WHERE city IN ('الرياض', 'دبي', 'عمّان');
```

## BETWEEN

القيمة ضمن نطاق (يشمل الطرفين):

```try sql shop
SELECT name, price FROM products
WHERE price BETWEEN 100 AND 1000;
```

```reference sql
LIKE 'أ%' | يبدأ بـ أ | WHERE name LIKE 'س%'
LIKE '%ة' | ينتهي بـ ة | WHERE name LIKE '%ة'
LIKE '%x%' | يحتوي x | WHERE name LIKE '%حاسوب%'
IN (…) | ضمن قائمة | WHERE id IN (1, 3, 5)
BETWEEN a AND b | ضمن نطاق | WHERE price BETWEEN 10 AND 50
```

```exercise sql
? اعرض الطلبات في الربع الأول من 2025
SELECT * FROM orders
WHERE order_date ___ '2025-01-01' AND '2025-03-31';
= BETWEEN
```

```quiz
? ماذا يعني الرمز % في LIKE؟
* أي عدد من الحروف
- حرف واحد بالضبط
- رقم فقط

? الشرط BETWEEN 100 AND 1000 يشمل القيمتين 100 و1000.
= true
```

# @lesson sql-null
title: القيم الفارغة NULL
summary: IS NULL و IS NOT NULL، و COALESCE.
---
`NULL` تعني «لا توجد قيمة». العميلة هدى في قاعدة البيانات مدينتها غير مسجلة:

```try sql shop
SELECT name, city FROM customers
WHERE city IS NULL;
```

:::warning لا تستخدم = NULL
`city = NULL` لا يعيد شيئًا أبدًا. استخدم `IS NULL` و `IS NOT NULL`.
:::

```try sql shop
SELECT name, city FROM customers
WHERE city IS NOT NULL;
```

## قيمة بديلة

`COALESCE` تعيد أول قيمة غير فارغة:

```try sql shop
SELECT name, COALESCE(city, 'غير معروفة') AS city
FROM customers;
```

```exercise sql
? اعرض العملاء الذين لا مدينة لهم
SELECT name FROM customers
WHERE city ___ NULL;
= IS
```

```quiz
? كيف تبحث عن القيم الفارغة؟
- WHERE city = NULL
* WHERE city IS NULL
- WHERE city == ''

? الدالة COALESCE تعيد أول قيمة غير فارغة.
= true
```

# @lesson sql-limit
title: LIMIT
summary: تحديد عدد الصفوف، والتخطي بـ OFFSET.
---
```try sql shop
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 3;
```

هذا يعرض أغلى ثلاثة منتجات.

## الصفحات بـ OFFSET

```try sql shop
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 3 OFFSET 3;
```

يتخطى أول ثلاثة ويعرض الثلاثة التالية؛ هكذا تعمل «الصفحة التالية» في المواقع.

:::info أنظمة أخرى
`LIMIT` تعمل في SQLite وMySQL وPostgreSQL. في SQL Server تُكتب `SELECT TOP 3 …`.
:::

```exercise sql
? اعرض أرخص منتجين
SELECT name, price FROM products
ORDER BY price
___ 2;
= LIMIT
```

```quiz
? ماذا يفعل OFFSET 5؟
* يتخطى أول خمسة صفوف
- يعرض خمسة صفوف فقط
- يحذف خمسة صفوف

? لعرض أغلى المنتجات نرتب تنازليًا ثم نستخدم LIMIT.
= true
```

# @lesson sql-aggregates
title: دوال التجميع
summary: COUNT و SUM و AVG و MIN و MAX.
---
دوال التجميع تحسب قيمة واحدة من صفوف كثيرة:

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
COUNT(*) | عدد الصفوف | SELECT COUNT(*) FROM orders;
COUNT(col) | عدد القيم غير الفارغة | SELECT COUNT(city) FROM customers;
SUM(col) | المجموع | SELECT SUM(quantity) FROM order_items;
AVG(col) | المتوسط | SELECT AVG(price) FROM products;
MIN(col) / MAX(col) | الأصغر / الأكبر | SELECT MAX(price) FROM products;
```

```try sql shop
SELECT COUNT(*) AS all_customers, COUNT(city) AS with_city
FROM customers;
```

```exercise sql
? احسب عدد الطلبات
SELECT ___(*) FROM orders;
= COUNT
```

```quiz
? أي دالة تحسب المتوسط؟
- SUM
* AVG
- MEAN

? الدالة COUNT(city) لا تعدّ القيم الفارغة NULL.
= true
```

# @lesson sql-group-by
title: GROUP BY و HAVING
summary: التجميع حسب عمود، وتصفية المجموعات.
---
`GROUP BY` يقسم الصفوف إلى مجموعات، وتحسب دوال التجميع قيمة لكل مجموعة:

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

`WHERE` تصفّي الصفوف **قبل** التجميع، و`HAVING` تصفّي المجموعات **بعده**:

```try sql shop
SELECT country, COUNT(*) AS customers
FROM customers
GROUP BY country
HAVING COUNT(*) > 1;
```

```exercise sql
? أكمل لتصفية المجموعات التي فيها أكثر من منتجين
SELECT category, COUNT(*) FROM products
GROUP BY category
___ COUNT(*) > 2;
= HAVING
```

```quiz
? أين تكتب شرطًا على نتيجة COUNT(*) لكل مجموعة؟
- WHERE
* HAVING
- ORDER BY

? الكلمة GROUP BY تقسم الصفوف إلى مجموعات.
= true
```

# @lesson sql-joins
title: الربط بين الجداول JOIN
summary: INNER JOIN و LEFT JOIN وربط أكثر من جدولين.
---
`JOIN` يجمع صفوفًا من جدولين حسب عمود مشترك:

```try sql shop
SELECT o.id AS order_id, c.name, o.order_date
FROM orders o
JOIN customers c ON c.id = o.customer_id;
```

- `o` و `c` أسماء مختصرة للجداول.
- `ON` تحدد شرط الربط.

## ربط ثلاثة جداول

```try sql shop
SELECT c.name AS customer, p.name AS product, i.quantity, p.price * i.quantity AS line_total
FROM order_items i
JOIN orders o ON o.id = i.order_id
JOIN customers c ON c.id = o.customer_id
JOIN products p ON p.id = i.product_id
ORDER BY customer;
```

## LEFT JOIN

يعيد كل صفوف الجدول الأيسر حتى التي ليس لها مقابل:

```try sql shop
SELECT c.name, COUNT(o.id) AS orders_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id
ORDER BY orders_count;
```

لاحظ هدى: ليس لها طلبات، فتظهر بـ 0. مع `JOIN` العادي لن تظهر أصلًا.

```reference sql
INNER JOIN / JOIN | الصفوف المتطابقة في الجدولين فقط | FROM a JOIN b ON b.a_id = a.id
LEFT JOIN | كل صفوف الأيسر + المتطابق من الأيمن | FROM a LEFT JOIN b ON …
RIGHT JOIN | كل صفوف الأيمن + المتطابق من الأيسر | FROM a RIGHT JOIN b ON …
FULL JOIN | كل الصفوف من الجهتين | FROM a FULL JOIN b ON …
```

```exercise sql
? أكمل لعرض كل العملاء حتى من لا طلب له
SELECT c.name, o.id FROM customers c
___ JOIN orders o ON o.customer_id = c.id;
= LEFT
```

```quiz
? أي ربط يعيد كل صفوف الجدول الأيسر حتى بلا مقابل؟
- INNER JOIN
* LEFT JOIN
- CROSS JOIN

? الكلمة ON تحدد شرط الربط بين الجدولين.
= true
```

# @lesson sql-subqueries
title: الاستعلامات الفرعية
summary: استعلام داخل استعلام، و IN، و EXISTS.
---
الاستعلام الفرعي يُكتب بين قوسين ويُستخدم نتيجته في استعلام آخر:

```try sql shop
SELECT name, price FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

هذا يعرض المنتجات الأغلى من المتوسط.

## مع IN

```try sql shop
SELECT name FROM customers
WHERE id IN (SELECT customer_id FROM orders WHERE order_date >= '2025-04-01');
```

## مع EXISTS

```try sql shop
SELECT name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.product_id = p.id);
```

هل ظهرت نتيجة؟ إذا لم يظهر شيء فكل المنتجات طُلبت مرة على الأقل.

```quiz
? أين يُكتب الاستعلام الفرعي؟
* بين قوسين ( )
- بين علامتي تنصيص
- بعد الفاصلة المنقوطة

? الشرط EXISTS يتحقق إذا أعاد الاستعلام الفرعي صفًا واحدًا على الأقل.
= true
```

# @lesson sql-insert
title: INSERT
summary: إضافة صف أو عدة صفوف.
---
```try sql shop
INSERT INTO products (name, category, price)
VALUES ('شاشة', 'إلكترونيات', 900);

SELECT * FROM products WHERE category = 'إلكترونيات';
```

- اذكر أسماء الأعمدة ثم القيم بنفس الترتيب.
- العمود `id` يأخذ رقمًا جديدًا تلقائيًا لأنه مفتاح أساسي.

## عدة صفوف

```try sql shop
INSERT INTO customers (name, city, country, joined) VALUES
  ('رامي فؤاد', 'بيروت', 'لبنان', '2025-07-01'),
  ('سلمى يوسف', 'الدوحة', 'قطر', '2025-07-03');

SELECT name, country FROM customers ORDER BY id DESC LIMIT 2;
```

```exercise sql
? أكمل لإضافة منتج جديد
___ INTO products (name, category, price)
VALUES ('مسطرة', 'قرطاسية', 5);
= INSERT
```

```quiz
? ما الكلمة التي تأتي قبل قائمة القيم في INSERT؟
* VALUES
- SET
- WITH

? يمكن إضافة عدة صفوف في أمر INSERT واحد.
= true
```

# @lesson sql-update-delete
title: UPDATE و DELETE
summary: تعديل البيانات وحذفها بأمان.
---
## UPDATE

```try sql shop
UPDATE products SET price = price * 0.9
WHERE category = 'أثاث';

SELECT name, price FROM products WHERE category = 'أثاث';
```

## DELETE

```try sql shop
DELETE FROM order_items WHERE quantity > 10;

SELECT * FROM order_items;
```

:::danger لا تنسَ WHERE
`UPDATE products SET price = 0;` بدون `WHERE` يغيّر **كل** الصفوف، و`DELETE FROM customers;` يحذفها **كلها**. اكتب `WHERE` أولًا، وجرّب الشرط بـ `SELECT` قبل التعديل.
:::

```exercise sql
? أكمل لتغيير مدينة العميل رقم 8
UPDATE customers ___ city = 'الكويت'
WHERE id = 8;
= SET
```

```quiz
? ماذا يحدث عند تنفيذ DELETE FROM products; بدون WHERE؟
- لا يحدث شيء
* تُحذف كل الصفوف
- يُحذف الجدول نفسه

? الكلمة SET تحدد الأعمدة الجديدة في UPDATE.
= true
```

# @lesson sql-create-table
title: إنشاء الجداول
summary: CREATE TABLE، وأنواع البيانات، والقيود، و ALTER و DROP.
---
```try sql
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  salary REAL CHECK (salary > 0),
  hired TEXT DEFAULT CURRENT_DATE
);

INSERT INTO employees (name, email, salary) VALUES ('علي', 'ali@example.com', 9000);
SELECT * FROM employees;
```

```reference sql
PRIMARY KEY | معرّف فريد لكل صف | id INTEGER PRIMARY KEY
NOT NULL | قيمة إلزامية | name TEXT NOT NULL
UNIQUE | بلا تكرار | email TEXT UNIQUE
DEFAULT | قيمة افتراضية | status TEXT DEFAULT 'active'
CHECK | شرط على القيمة | CHECK (price >= 0)
FOREIGN KEY | يشير لجدول آخر | FOREIGN KEY (customer_id) REFERENCES customers(id)
ALTER TABLE | تعديل الجدول | ALTER TABLE t ADD COLUMN phone TEXT;
DROP TABLE | حذف الجدول كله | DROP TABLE t;
```

جرّب إضافة موظف بلا اسم أو براتب سالب لترى القيود تمنعك:

```try sql
CREATE TABLE t (name TEXT NOT NULL, salary REAL CHECK (salary > 0));
INSERT INTO t VALUES (NULL, 100);
```

```quiz
? أي قيد يمنع تكرار القيمة في العمود؟
- NOT NULL
* UNIQUE
- DEFAULT

? الأمر DROP TABLE يحذف الجدول وكل بياناته.
= true
```

# @lesson sql-reference
title: مرجع SQL
summary: أهم الأوامر والكلمات مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي أمر.

```reference sql
SELECT | اختيار أعمدة | SELECT name, price FROM products;
DISTINCT | بلا تكرار | SELECT DISTINCT country FROM customers;
WHERE | تصفية الصفوف | WHERE price > 100
AND / OR / NOT | دمج الشروط | WHERE a = 1 AND b = 2
ORDER BY | الترتيب | ORDER BY price DESC
LIMIT / OFFSET | عدد الصفوف | LIMIT 10 OFFSET 20
LIKE | بحث بنمط | WHERE name LIKE '%علي%'
IN | ضمن قائمة | WHERE id IN (1, 2)
BETWEEN | ضمن نطاق | WHERE price BETWEEN 10 AND 50
IS NULL | قيمة فارغة | WHERE city IS NULL
AS | اسم مستعار | SELECT price AS p
COUNT / SUM / AVG | دوال التجميع | SELECT COUNT(*) FROM orders;
MIN / MAX | الأصغر والأكبر | SELECT MAX(price) FROM products;
GROUP BY | التجميع | GROUP BY category
HAVING | تصفية المجموعات | HAVING COUNT(*) > 1
JOIN … ON | الربط | JOIN customers c ON c.id = o.customer_id
LEFT JOIN | ربط مع الإبقاء على الأيسر | LEFT JOIN orders o ON …
INSERT INTO | إضافة | INSERT INTO t (a) VALUES (1);
UPDATE … SET | تعديل | UPDATE t SET a = 2 WHERE id = 1;
DELETE FROM | حذف | DELETE FROM t WHERE id = 1;
CREATE TABLE | إنشاء جدول | CREATE TABLE t (id INTEGER PRIMARY KEY);
ALTER TABLE | تعديل جدول | ALTER TABLE t ADD COLUMN b TEXT;
DROP TABLE | حذف جدول | DROP TABLE t;
COALESCE | أول قيمة غير فارغة | COALESCE(city, '-')
ROUND | التقريب | ROUND(AVG(price), 2)
```

:::tip ماذا بعد؟
تدرّب بكتابة أسئلة من عندك على قاعدة بيانات المتجر: من أكثر عميل طلبًا؟ ما أكثر قسم مبيعًا؟ كم أنفق كل عميل؟
:::
