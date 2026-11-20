# @lesson py-intro
title: مقدمة في Python
summary: ما هي بايثون ولماذا هي من أكثر اللغات استخدامًا.
---
**بايثون** لغة برمجة سهلة القراءة، تُستخدم في تحليل البيانات، والذكاء الاصطناعي، والأتمتة، وتطوير الويب، والتعليم.

## أول برنامج

اضغط **تشغيل** (أول تشغيل يأخذ ثواني لتحميل بايثون في متصفحك):

```try python
print("مرحبًا يا بايثون")
print(3 + 4)
```

## لماذا بايثون؟

- **سهلة القراءة**: كودها قريب من اللغة الإنجليزية.
- **مكتبات ضخمة**: لكل مجال تقريبًا مكتبة جاهزة.
- **تعمل في كل مكان**: ويندوز، ماك، لينكس، والخوادم.

:::info بايثون في هذه المنصة
كل الأمثلة تعمل داخل متصفحك مباشرة، دون تثبيت أي شيء ودون إرسال الكود إلى أي خادم.
:::

```quiz
? أي دالة تطبع النص في بايثون؟
* print()
- echo()
- console.log()

? لغة بايثون تُستخدم في الذكاء الاصطناعي وتحليل البيانات.
= true
```

# @lesson py-syntax
title: صيغة بايثون
summary: المسافات البادئة، والتعليقات، وكتابة عدة أسطر.
---
## المسافات البادئة

بايثون تستخدم **المسافة في بداية السطر** لتحديد الكتل، بدل الأقواس المعقوفة في لغات أخرى:

```try python
age = 20
if age >= 18:
    print("بالغ")
    print("هذا السطر داخل الشرط أيضًا")
print("هذا السطر خارج الشرط")
```

:::warning المسافة إلزامية
نسيان المسافة البادئة بعد `if` أو `for` يسبب خطأ `IndentationError`. استخدم أربع مسافات دائمًا.
:::

## التعليقات

التعليق يبدأ بـ `#`، والمفسّر يتجاهله عند التشغيل:

```try python
# هذا تعليق
print("مرحبا")  # تعليق في نهاية السطر
```

```exercise python
? أكمل علامة بداية التعليق
___ هذا تعليق لا يُنفَّذ
= #
```

```quiz
? بماذا تحدد بايثون الكتل البرمجية؟
- الأقواس المعقوفة {}
* المسافات البادئة
- الكلمة end

? التعليق في بايثون يبدأ بالرمز #.
= true
```

# @lesson py-variables
title: المتغيرات
summary: إنشاء المتغيرات وتسميتها وتعدد الإسناد.
---
المتغير في بايثون يُنشأ بمجرد إسناد قيمة إليه، دون كلمة خاصة:

```try python
name = "سارة"
age = 25
height = 1.65
print(name, age, height)
age = 26
print("العمر الجديد:", age)
```

## إسناد متعدد

```try python
x, y, z = 1, 2, 3
print(x, y, z)
a = b = 0
print(a, b)
x, y = y, x      # تبديل القيمتين
print(x, y)
```

## قواعد التسمية

- يبدأ بحرف أو `_`، ولا يبدأ برقم.
- يفرّق بين الأحرف الكبيرة والصغيرة.
- الأسلوب المعتاد: كلمات صغيرة بينها `_` مثل `total_price`.

```exercise python
? أسند الرقم 10 إلى المتغير count
count ___ 10
= =
```

```quiz
? أي اسم متغير صحيح؟
- 2name
* user_name
- user-name

? في بايثون تحتاج كلمة let لإنشاء متغير.
= false
```

# @lesson py-types
title: أنواع البيانات
summary: str و int و float و bool و None، والدالة type، والتحويل.
---
```reference python
str | نص | "مرحبا"
int | عدد صحيح | 42
float | عدد عشري | 3.14
bool | منطقي | True, False
None | لا قيمة | x = None
list | قائمة | [1, 2, 3]
tuple | صف ثابت | (1, 2)
dict | قاموس | {"a": 1}
set | مجموعة بلا تكرار | {1, 2}
```

```try python
print(type("نص"))
print(type(10))
print(type(2.5))
print(type(True))
print(type(None))
```

## التحويل بين الأنواع

```try python
print(int("42") + 1)
print(float("3.5") * 2)
print(str(100) + " ريال")
print(bool(0), bool(5))
```

:::warning لا يمكن جمع نص ورقم
`"العمر: " + 25` يسبب خطأ. حوّل الرقم إلى نص: `"العمر: " + str(25)`، أو استخدم f-string كما سترى في درس النصوص.
:::

```quiz
? ما نوع القيمة 3.14؟
- int
* float
- str

? القيمة True من النوع bool.
= true
```

# @lesson py-numbers
title: الأرقام والعمليات
summary: العمليات الحسابية، والقسمة الصحيحة، والباقي، والأس، والتقريب.
---
```reference python
+ - * | جمع وطرح وضرب | 7 * 3 → 21
/ | قسمة (دائمًا عشري) | 7 / 2 → 3.5
// | قسمة صحيحة | 7 // 2 → 3
% | باقي القسمة | 7 % 2 → 1
** | الأس | 2 ** 10 → 1024
round() | التقريب | round(3.14159, 2) → 3.14
abs() | القيمة المطلقة | abs(-5) → 5
max() / min() | الأكبر / الأصغر | max(3, 9, 4) → 9
```

```try python
price = 120
discount = 0.15
final = price * (1 - discount)
print("السعر النهائي:", final)
print("مقرّبًا:", round(final, 1))
print("هل الرقم زوجي؟", 10 % 2 == 0)
print(2 ** 10)
```

## العمليات المختصرة

```try python
score = 10
score += 5
score *= 2
print(score)
```

```exercise python
? أكمل لحساب القسمة الصحيحة لـ 17 على 5
print(17 ___ 5)
= //
```

```quiz
? ما ناتج 7 / 2 في بايثون 3؟
- 3
* 3.5
- 4

? العامل % يعطي باقي القسمة.
= true
```

# @lesson py-strings
title: النصوص
summary: f-strings، والتقطيع، والدوال المفيدة.
---
## f-strings

أسهل طريقة لإدراج القيم داخل النص:

```try python
name = "عمر"
score = 92.456
print(f"الطالب {name} حصل على {score:.1f}")
```

## الفهرسة والتقطيع

```try python
word = "Python"
print(word[0])      # أول حرف
print(word[-1])     # آخر حرف
print(word[0:3])    # من 0 إلى 2
print(len(word))
```

## دوال مفيدة

```try python
text = "  Hello Python  "
print(text.strip())
print(text.lower())
print(text.replace("Python", "World"))
print("a,b,c".split(","))
print("-".join(["2026", "11", "20"]))
print("Py" in "Python")
```

```reference python
len() | الطول | len("abc") → 3
upper() / lower() | أحرف كبيرة / صغيرة | "a".upper()
strip() | حذف المسافات من الطرفين | " a ".strip()
replace() | استبدال | "a-b".replace("-", "+")
split() | تقسيم إلى قائمة | "a b".split()
join() | دمج قائمة في نص | ",".join(["a", "b"])
find() | موضع النص | "abc".find("c") → 2
startswith() | يبدأ بـ؟ | "abc".startswith("a")
in | يحتوي؟ | "b" in "abc"
```

```exercise python
? أكمل لإنشاء f-string
name = "ليلى"
print(___"أهلًا {name}")
= f
```

```quiz
? ما ناتج "Python"[0]؟
* "P"
- "y"
- "n"

? الدالة strip تحذف المسافات من طرفي النص.
= true
```

# @lesson py-conditions
title: الشروط
summary: if و elif و else، والعوامل المنطقية، والشرط في سطر واحد.
---
```try python
temperature = 31
if temperature > 35:
    print("حار جدًا")
elif temperature > 25:
    print("دافئ")
else:
    print("معتدل")
```

## العوامل المنطقية

`and` و `or` و `not`:

```try python
age = 22
has_id = True
if age >= 18 and has_id:
    print("مسموح بالدخول")
if not has_id:
    print("أحضر الهوية")
```

## الشرط في سطر واحد

```try python
n = 7
kind = "زوجي" if n % 2 == 0 else "فردي"
print(kind)
```

```exercise python
? أكمل الكلمة التي تعني «وإلا إذا»
x = 0
if x > 0:
    print("موجب")
___ x < 0:
    print("سالب")
else:
    print("صفر")
= elif
```

```quiz
? أي كلمة تكتب للشرط الإضافي في بايثون؟
- else if
* elif
- elseif

? العامل and يعطي True فقط إذا كان الطرفان True.
= true
```

# @lesson py-loops
title: الحلقات
summary: for مع range، و while، و break و continue.
---
## for و range

```try python
for i in range(1, 6):
    print("الرقم", i)
```

`range(start, stop, step)` ينتج أرقامًا من `start` حتى قبل `stop`:

```try python
print(list(range(5)))
print(list(range(2, 10, 2)))
```

## المرور على قائمة

```try python
cities = ["الرياض", "دبي", "القاهرة"]
for index, city in enumerate(cities, start=1):
    print(index, city)
```

## while

```try python
balance = 100
while balance > 0:
    balance -= 30
    print("الرصيد:", balance)
```

## break و continue

```try python
for n in range(1, 10):
    if n == 3:
        continue
    if n == 7:
        break
    print(n)
```

```exercise python
? أكمل لطباعة الأرقام من 0 إلى 4
for i in ___(5):
    print(i)
= range
```

```quiz
? ما آخر رقم ينتجه range(1, 5)؟
- 5
* 4
- 1

? الكلمة continue تتخطى بقية التكرار الحالي وتنتقل للتالي.
= true
```

# @lesson py-lists
title: القوائم
summary: إنشاء القوائم، والإضافة والحذف، والترتيب، والتقطيع.
---
**القائمة** مجموعة مرتبة قابلة للتغيير:

```try python
fruits = ["تفاح", "موز"]
fruits.append("برتقال")
fruits.insert(0, "عنب")
print(fruits)
fruits.remove("موز")
last = fruits.pop()
print(fruits, "| حُذف:", last)
print(len(fruits), fruits[0])
```

## الترتيب والتقطيع

```try python
nums = [5, 2, 9, 1, 7]
print(sorted(nums))
nums.sort(reverse=True)
print(nums)
print(nums[1:3])
print(sum(nums), max(nums), min(nums))
```

```reference python
append() | إضافة في النهاية | lst.append(4)
insert() | إضافة في موضع | lst.insert(0, "a")
remove() | حذف قيمة | lst.remove("a")
pop() | حذف وإرجاع عنصر | lst.pop()
sort() | ترتيب القائمة نفسها | lst.sort()
sorted() | نسخة مرتبة | sorted(lst)
reverse() | عكس الترتيب | lst.reverse()
index() | موضع قيمة | lst.index(9)
count() | عدد التكرار | lst.count(2)
len() / sum() | الطول / المجموع | sum(lst)
```

```exercise python
? أضف 4 في نهاية القائمة
nums = [1, 2, 3]
nums.___(4)
= append
```

```quiz
? ما الفرق بين sort() و sorted()؟
* sort() ترتب القائمة نفسها، و sorted() تعيد نسخة مرتبة
- لا فرق بينهما
- sorted() للنصوص فقط

? الفهرس -1 يشير إلى آخر عنصر في القائمة.
= true
```

# @lesson py-tuples-sets
title: الصفوف والمجموعات
summary: tuple الثابتة، و set بلا تكرار، والعمليات على المجموعات.
---
## الصف (tuple)

مثل القائمة لكنه **لا يتغير** بعد إنشائه:

```try python
point = (10, 20)
x, y = point
print(x, y)
print(point[0])
```

## المجموعة (set)

بلا ترتيب وبلا تكرار، ومفيدة لحذف المكرر والمقارنة:

```try python
tags = {"python", "web", "python", "data"}
print(tags)
emails = ["a@x.com", "b@x.com", "a@x.com"]
print(set(emails))
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)   # التقاطع
print(a | b)   # الاتحاد
print(a - b)   # الفرق
```

```quiz
? أي نوع لا يسمح بتغيير عناصره بعد إنشائه؟
- list
* tuple
- set

? المجموعة set تحذف القيم المكررة تلقائيًا.
= true
```

# @lesson py-dicts
title: القواميس
summary: مفتاح وقيمة، والإضافة والتحديث، والمرور على العناصر، و get.
---
**القاموس** يربط مفاتيح بقيم:

```try python
student = {"name": "نور", "age": 21, "city": "جدة"}
print(student["name"])
student["age"] = 22          # تحديث
student["major"] = "حاسب"    # إضافة
print(student)
print(student.get("phone", "غير موجود"))
```

## المرور على القاموس

```try python
prices = {"قلم": 5, "دفتر": 12, "حقيبة": 90}
for item, price in prices.items():
    print(f"{item}: {price} ريال")
print(list(prices.keys()))
print(sum(prices.values()))
```

## قائمة قواميس

```try python
employees = [
    {"name": "علي", "salary": 8000},
    {"name": "منى", "salary": 9500},
]
top = max(employees, key=lambda e: e["salary"])
print("الأعلى راتبًا:", top["name"])
```

:::tip استخدم get
`d["key"]` يسبب خطأ إذا لم يوجد المفتاح، بينما `d.get("key", default)` يعيد قيمة بديلة.
:::

```exercise python
? اقرأ القيمة بأمان مع قيمة بديلة
age = person.___("age", 0)
= get
```

```quiz
? أي دالة تعيد أزواج المفتاح والقيمة؟
- keys()
- values()
* items()

? القاموس يخزن البيانات على شكل مفتاح وقيمة.
= true
```

# @lesson py-comprehensions
title: الصيغ المختصرة
summary: إنشاء القوائم والقواميس في سطر واحد.
---
**List comprehension** طريقة مختصرة لبناء قائمة من أخرى:

```try python
nums = [1, 2, 3, 4, 5, 6]
squares = [n * n for n in nums]
evens = [n for n in nums if n % 2 == 0]
print(squares)
print(evens)
```

يعادل:

```python
squares = []
for n in nums:
    squares.append(n * n)
```

## قاموس ومجموعة

```try python
names = ["سارة", "عمر", "ليلى"]
lengths = {name: len(name) for name in names}
print(lengths)
unique_lengths = {len(name) for name in names}
print(unique_lengths)
```

:::tip لا تبالغ
الصيغة المختصرة رائعة للتحويل والتصفية البسيطة. إذا أصبحت طويلة ومعقدة، استخدم حلقة عادية لتبقى مقروءة.
:::

```exercise python
? أكمل لإنشاء قائمة بضعف كل رقم
doubled = [n * 2 ___ n in nums]
= for
```

```quiz
? ما ناتج [n for n in range(5) if n > 2]؟
* [3, 4]
- [2, 3, 4]
- [0, 1, 2]

? الصيغة المختصرة يمكنها إنشاء قاموس أيضًا.
= true
```

# @lesson py-functions
title: الدوال
summary: def، والمعاملات الافتراضية والمسماة، والقيمة المرجعة، و lambda.
---
```try python
def greet(name, greeting="أهلًا"):
    return f"{greeting} يا {name}"

print(greet("سارة"))
print(greet("عمر", greeting="مرحبًا"))
```

- `def` تعرّف الدالة.
- المعامل `greeting` له قيمة افتراضية.
- يمكن تمرير المعاملات بالاسم: `greeting="مرحبًا"`.

## إعادة عدة قيم

```try python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

low, high, avg = stats([4, 8, 15, 16])
print(low, high, avg)
```

## عدد غير محدد من المعاملات

```try python
def total(*prices):
    return sum(prices)

print(total(10, 20, 30))
```

## lambda

دالة صغيرة بلا اسم:

```try python
square = lambda x: x * x
print(square(9))
words = ["تفاحة", "موز", "بطيخ أحمر"]
print(sorted(words, key=lambda w: len(w)))
```

```exercise python
? أكمل الكلمة التي تعرّف دالة
___ add(a, b):
    return a + b
= def
```

```quiz
? ما وظيفة return؟
* إعادة نتيجة من الدالة
- طباعة النتيجة
- تكرار الدالة

? يمكن للدالة في بايثون أن تعيد أكثر من قيمة.
= true
```

# @lesson py-modules
title: الوحدات
summary: import، ووحدات math و random و datetime.
---
**الوحدة** ملف فيه دوال جاهزة. تستوردها بـ `import`:

```try python
import math
print(math.sqrt(144))
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))
```

```try python
import random
print(random.randint(1, 6))
print(random.choice(["أحمر", "أزرق", "أخضر"]))
```

```try python
from datetime import date, timedelta
today = date(2026, 11, 20)
print(today + timedelta(days=30))
print(today.strftime("%Y-%m-%d"))
```

## صيغ الاستيراد

```reference python
import math | استيراد الوحدة كاملة | math.sqrt(9)
from math import sqrt | استيراد دالة محددة | sqrt(9)
import math as m | اسم مختصر | m.pi
from datetime import date | صنف من وحدة | date.today()
```

:::info مكتبات بايثون
بالإضافة للوحدات المدمجة، توجد آلاف المكتبات الخارجية مثل `pandas` لتحليل البيانات و `requests` للويب، تُثبَّت بالأمر `pip install`.
:::

```exercise python
? أكمل لاستيراد وحدة math
___ math
print(math.pi)
= import
```

```quiz
? أي وحدة تحتوي الدالة sqrt؟
* math
- random
- datetime

? الصيغة from math import sqrt تسمح باستخدام sqrt مباشرة دون math.
= true
```

# @lesson py-errors
title: معالجة الأخطاء
summary: try و except و else و finally، و raise.
---
```try python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("لا يمكن القسمة على صفر")
        return None
    else:
        return result
    finally:
        print("انتهت المحاولة")

print(safe_divide(10, 2))
print(safe_divide(1, 0))
```

## أخطاء شائعة

```reference python
ValueError | قيمة غير مناسبة | int("abc")
TypeError | نوع غير مناسب | "a" + 1
ZeroDivisionError | قسمة على صفر | 1 / 0
KeyError | مفتاح غير موجود | {}["x"]
IndexError | فهرس خارج القائمة | [1][5]
FileNotFoundError | ملف غير موجود | open("x.txt")
```

## رمي خطأ بنفسك

```try python
def set_age(age):
    if age < 0:
        raise ValueError("العمر لا يكون سالبًا")
    return age

try:
    set_age(-3)
except ValueError as e:
    print("خطأ:", e)
```

```exercise python
? أكمل لالتقاط خطأ التحويل
try:
    n = int("abc")
___ ValueError:
    print("ليس رقمًا")
= except
```

```quiz
? أي خطأ يحدث عند int("abc")؟
* ValueError
- KeyError
- IndexError

? الكلمة raise ترمي خطأ بنفسك.
= true
```

# @lesson py-classes
title: الأصناف والكائنات
summary: class و __init__ و self، والخصائص والدوال، والوراثة.
---
**الصنف** قالب لإنشاء كائنات لها بيانات وسلوك:

```try python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def __str__(self):
        return f"حساب {self.owner}: {self.balance} ريال"

acc = Account("سارة", 100)
acc.deposit(50)
print(acc)
```

- `__init__` تُنفَّذ عند إنشاء الكائن.
- `self` يشير إلى الكائن نفسه.
- `__str__` تحدد كيف يُطبع الكائن.

## الوراثة

```try python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return f"{self.name} يقول: مياو"

print(Cat("مشمش").speak())
```

```exercise python
? أكمل الكلمة التي تعرّف صنفًا
___ Car:
    pass
= class
```

```quiz
? متى تُنفَّذ الدالة __init__؟
* عند إنشاء كائن جديد
- عند حذف الكائن
- عند طباعة الكائن

? الصنف Cat(Animal) يرث من الصنف Animal.
= true
```

# @lesson py-files
title: الملفات
summary: الكتابة والقراءة، و with، وأوضاع فتح الملف.
---
```try python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("السطر الأول\n")
    f.write("السطر الثاني\n")

with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

- `with` تغلق الملف تلقائيًا بعد الانتهاء، حتى لو حدث خطأ.
- `encoding="utf-8"` مهم للنصوص العربية.

```reference python
"r" | قراءة (الافتراضي) | open("a.txt")
"w" | كتابة (يمسح القديم) | open("a.txt", "w")
"a" | إضافة في النهاية | open("a.txt", "a")
read() | قراءة الملف كله | f.read()
readlines() | قائمة بالأسطر | f.readlines()
write() | كتابة نص | f.write("نص")
```

## ملفات CSV

```try python
import csv
with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["علي", 30])
with open("people.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["age"])
```

:::info الملفات هنا مؤقتة
في هذه المنصة تُحفظ الملفات في ذاكرة متصفحك أثناء التشغيل فقط، وتختفي بعده.
:::

```quiz
? أي وضع يضيف إلى نهاية الملف دون مسح محتواه؟
- "w"
* "a"
- "r"

? الكلمة with تغلق الملف تلقائيًا.
= true
```

# @lesson py-reference
title: مرجع Python
summary: أهم الكلمات والدوال المدمجة مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة أو دالة.

```reference python
print() | طباعة | print("مرحبا")
input() | قراءة من المستخدم (لا تعمل في المحرر هنا) | name = input("اسمك: ")
len() | الطول | len([1, 2])
type() | النوع | type(3)
int() / float() / str() | التحويل | int("5")
range() | سلسلة أرقام | range(1, 10, 2)
if / elif / else | الشرط | if x > 0: …
for / while | الحلقات | for i in range(3): …
break / continue | التحكم في الحلقة | break
def / return | الدوال | def f(x): return x
lambda | دالة صغيرة | lambda x: x * 2
class | صنف | class A: …
import / from | الاستيراد | from math import pi
try / except | معالجة الأخطاء | try: … except ValueError: …
raise | رمي خطأ | raise ValueError("…")
with open() | التعامل مع الملفات | with open("a.txt") as f: …
list.append() | إضافة لقائمة | lst.append(1)
dict.get() | قراءة آمنة | d.get("k", 0)
sorted() | نسخة مرتبة | sorted(lst)
sum() / min() / max() | المجموع والأصغر والأكبر | sum([1, 2])
enumerate() | العنصر مع رقمه | for i, x in enumerate(lst): …
zip() | دمج قائمتين | list(zip(a, b))
f"…" | نص مع قيم | f"العمر {age}"
in | هل يحتوي؟ | "a" in "abc"
None | لا قيمة | x = None
```

:::tip ماذا بعد؟
جرّب مشروعًا صغيرًا: حاسبة مصروفات بقاموس، أو لعبة تخمين رقم بـ `random`. وتابع إلى دورة **SQL** لتتعلم التعامل مع قواعد البيانات.
:::
