# @lesson np-intro
title: مقدمة في NumPy
summary: لماذا NumPy أسرع من قوائم بايثون العادية.
---
**NumPy** مكتبة بايثون للحساب على الأرقام. قلبها نوع اسمه **ndarray**: مصفوفة أرقام من نوع واحد مخزنة بشكل متصل في الذاكرة، فتصبح العمليات عليها أسرع بكثير من القوائم العادية. عليها تُبنى Pandas وأغلب مكتبات علم البيانات والذكاء الاصطناعي.

اضغط **تشغيل** (أول تشغيل يحمّل NumPy في متصفحك ويأخذ ثواني):

```try python
import numpy as np

prices = np.array([120, 45, 300, 80])
print(prices * 1.15)        # الضريبة على كل الأسعار دفعة واحدة
print(prices.sum(), prices.mean())
```

لاحظ: لا حلقة `for`. العملية تُطبَّق على كل العناصر معًا؛ هذا يسمى **العمليات المتجهة**.

:::info الاسم المختصر np
الاستيراد المتعارف عليه هو `import numpy as np`؛ ستراه في كل الكتب والمشاريع.
:::

```quiz
? ما النوع الأساسي في NumPy؟
* ndarray
- list
- dict

? في NumPy نحتاج حلقة for لضرب كل العناصر في رقم.
= false
> العمليات متجهة: prices * 1.15 تضرب كل العناصر مرة واحدة.
```

# @lesson np-arrays
title: إنشاء المصفوفات
summary: array و zeros و ones و arange و linspace، والأبعاد ونوع البيانات.
---
```try python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1, 2, 3], [4, 5, 6]])      # بعدان: صفان وثلاثة أعمدة
print(a, a.ndim)
print(b)
print(b.ndim, b.shape, b.size, b.dtype)
```

## مصفوفات جاهزة

```try python
import numpy as np

print(np.zeros(4))
print(np.ones((2, 3)))
print(np.arange(0, 10, 2))        # مثل range
print(np.linspace(0, 1, 5))       # 5 أرقام متساوية البعد من 0 إلى 1
print(np.full((2, 2), 7))
```

```reference python
np.array() | من قائمة | np.array([1, 2, 3])
np.zeros() / np.ones() | أصفار / آحاد | np.zeros((2, 3))
np.arange() | سلسلة بخطوة | np.arange(0, 10, 2)
np.linspace() | عدد نقاط بين حدين | np.linspace(0, 1, 5)
np.eye() | مصفوفة الوحدة | np.eye(3)
.shape / .ndim / .size | الشكل / الأبعاد / العدد | a.shape
.dtype | نوع البيانات | a.dtype
```

```exercise python
? أنشئ مصفوفة من 0 إلى 4
import numpy as np
a = np.___(5)
= arange
```

```quiz
? ما شكل np.array([[1, 2, 3], [4, 5, 6]])؟
* (2, 3)
- (3, 2)
- (6,)

? الدالة np.zeros((2, 3)) تنشئ مصفوفة أصفار بصفين وثلاثة أعمدة.
= true
```

# @lesson np-indexing
title: الفهرسة والتقطيع
summary: الوصول للعناصر والصفوف والأعمدة.
---
```try python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
print(a[0], a[-1])
print(a[1:4])
print(a[::2])

m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(m[1, 2])       # الصف 1، العمود 2
print(m[0])          # الصف الأول
print(m[:, 1])       # العمود الثاني كله
print(m[:2, 1:])     # جزء من المصفوفة
```

:::warning التقطيع لا ينسخ
`b = a[1:3]` يعطي «نافذة» على نفس البيانات؛ تغيير `b` يغيّر `a`. للنسخ استخدم `a[1:3].copy()`.
:::

```exercise python
? اختر العمود الأول كاملًا من المصفوفة m
first_col = m[___, 0]
= :
```

```quiz
? ماذا يعيد m[1, 2]؟
* العنصر في الصف 1 والعمود 2
- الصفين 1 و2
- العمودين 1 و2

? تغيير جزء مقطوع من مصفوفة قد يغيّر المصفوفة الأصلية.
= true
```

# @lesson np-shape
title: تغيير الشكل
summary: reshape و flatten و transpose و الدمج.
---
```try python
import numpy as np

a = np.arange(12)
m = a.reshape(3, 4)
print(m)
print(m.T)                 # المنقول: الصفوف تصبح أعمدة
print(m.flatten())
print(a.reshape(2, -1))    # -1: احسب البعد تلقائيًا
```

## الدمج

```try python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
print(np.concatenate([a, b]))      # تحت بعض
print(np.hstack([a, a]))           # جنب بعض
```

```exercise python
? حوّل 6 أرقام إلى مصفوفة بصفين وثلاثة أعمدة
m = np.arange(6).___(2, 3)
= reshape
```

```quiz
? ماذا يعني -1 في reshape(2, -1)؟
* احسب هذا البعد تلقائيًا
- اعكس الترتيب
- احذف آخر عنصر

? الخاصية .T تعطي منقول المصفوفة.
= true
```

# @lesson np-math
title: العمليات والبث
summary: العمليات بين المصفوفات، والبث broadcasting، والدوال الرياضية.
---
```try python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b, a * b, b / a)
print(a ** 2)
print(np.sqrt(b), np.round(np.sqrt(b), 2))
```

## البث (broadcasting)

تتمدد المصفوفة الأصغر تلقائيًا لتناسب الأكبر:

```try python
import numpy as np

prices = np.array([[100, 200, 300],
                   [ 50,  60,  70]])
discount = np.array([0.9, 0.8, 1.0])   # خصم لكل عمود
print(prices * discount)
print(prices + 5)                       # رقم واحد يُضاف للكل
```

```reference python
+ - * / ** | عمليات عنصر بعنصر | a * b
np.sqrt / np.exp / np.log | دوال رياضية | np.sqrt(a)
np.round | التقريب | np.round(a, 2)
np.abs | القيمة المطلقة | np.abs(a)
@ / np.dot | ضرب المصفوفات | a @ b
```

:::info الضرب * أم @؟
`a * b` يضرب كل عنصر في مقابله. `a @ b` ضرب المصفوفات الرياضي (جبر خطي).
:::

```quiz
? ما ناتج np.array([1, 2, 3]) * 2؟
* [2 4 6]
- [1 2 3 1 2 3]
- خطأ

? البث يسمح بجمع رقم واحد مع مصفوفة كاملة.
= true
```

# @lesson np-stats
title: الإحصاء والمحور axis
summary: sum و mean و min و max و std، والحساب لكل صف أو عمود.
---
```try python
import numpy as np

sales = np.array([[120, 90, 150],    # الفرع الأول: ثلاثة أشهر
                  [ 80, 110, 95],    # الفرع الثاني
                  [200, 180, 210]])  # الفرع الثالث
print("الإجمالي:", sales.sum())
print("لكل شهر:", sales.sum(axis=0))
print("لكل فرع:", sales.sum(axis=1))
print("المتوسط:", sales.mean().round(1))
print("أعلى بيع:", sales.max(), "في الموضع", sales.argmax())
print("الانحراف المعياري:", sales.std().round(1))
```

- `axis=0` نزولًا عبر الصفوف: نتيجة لكل **عمود**.
- `axis=1` عبر الأعمدة: نتيجة لكل **صف**.

```reference python
sum() | المجموع | a.sum(axis=0)
mean() | المتوسط | a.mean()
median() | الوسيط | np.median(a)
min() / max() | الأصغر / الأكبر | a.max()
argmin() / argmax() | موضع الأصغر / الأكبر | a.argmax()
std() / var() | الانحراف / التباين | a.std()
cumsum() | المجموع التراكمي | a.cumsum()
```

```exercise python
? احسب المجموع لكل صف
row_totals = sales.sum(axis=___)
= 1
```

```quiz
? ماذا يعطي sales.sum(axis=0)؟
* مجموعًا لكل عمود
- مجموعًا لكل صف
- رقمًا واحدًا

? الدالة argmax تعيد موضع أكبر قيمة.
= true
```

# @lesson np-filter
title: التصفية بالشروط
summary: أقنعة منطقية، و where، والعدّ.
---
المقارنة تعطي مصفوفة `True/False` تستخدمها لاختيار العناصر:

```try python
import numpy as np

scores = np.array([45, 88, 92, 67, 30, 75])
mask = scores >= 60
print(mask)
print(scores[mask])                         # الناجحون
print(scores[(scores > 50) & (scores < 90)])
print("عدد الناجحين:", mask.sum())
print(np.where(scores >= 60, "ناجح", "راسب"))
```

- `&` (و) و `|` (أو) مع أقواس حول كل شرط.
- `mask.sum()` يعدّ قيم `True`.

```exercise python
? اختر الأرقام الأكبر من 10
big = a[a ___ 10]
= >
```

```quiz
? ماذا يعيد scores[scores >= 60]؟
* العناصر التي تحقق الشرط فقط
- قيم True و False
- الموضع الأول فقط

? الدالة np.where تختار قيمة حسب شرط لكل عنصر.
= true
```

# @lesson np-random
title: الأرقام العشوائية
summary: مولّد الأرقام، والتوزيعات، والاختيار العشوائي.
---
```try python
import numpy as np

rng = np.random.default_rng(seed=42)       # seed يجعل النتائج قابلة للتكرار
print(rng.integers(1, 7, size=10))          # رمي نرد 10 مرات
print(rng.random(3))                        # أرقام بين 0 و1
heights = rng.normal(loc=170, scale=8, size=1000)
print(heights.mean().round(1), heights.std().round(1))
print(rng.choice(["أحمر", "أخضر", "أزرق"], size=5))
```

:::tip لماذا seed؟
بنفس `seed` تحصل على نفس الأرقام كل مرة، فيستطيع غيرك تكرار تجربتك بالضبط.
:::

```quiz
? ما فائدة seed؟
* الحصول على نفس الأرقام العشوائية عند كل تشغيل
- تسريع الحساب
- منع التكرار في الأرقام

? الدالة rng.normal تولّد أرقامًا من التوزيع الطبيعي.
= true
```

# @lesson np-project
title: مشروع: تحليل درجات
summary: تطبيق يجمع ما تعلمته على بيانات درجات طلاب.
---
```try python
import numpy as np

rng = np.random.default_rng(7)
# 8 طلاب × 3 مواد
grades = rng.integers(40, 101, size=(8, 3))
subjects = np.array(["رياضيات", "علوم", "لغة"])
print(grades)

avg_student = grades.mean(axis=1).round(1)
avg_subject = grades.mean(axis=0).round(1)
print("متوسط كل طالب:", avg_student)
print("متوسط كل مادة:", dict(zip(subjects, avg_subject)))
print("أصعب مادة:", subjects[avg_subject.argmin()])
print("أفضل طالب رقم:", avg_student.argmax() + 1)
print("طلاب فوق 75:", np.where(avg_student > 75)[0] + 1)

curved = np.clip(grades + 5, 0, 100)    # رفع 5 درجات بحد أقصى 100
print("بعد الرفع:", curved.mean().round(1))
```

:::tip طوّره بنفسك
احسب نسبة الناجحين في كل مادة (60 فأكثر)، أو رتّب الطلاب حسب المتوسط بـ `np.argsort`.
:::

```quiz
? ماذا تفعل np.clip(a, 0, 100)؟
* تحصر القيم بين 0 و100
- تحذف القيم خارج النطاق
- تقرّب القيم

? المتوسط لكل طالب يُحسب بـ axis=1 لأن كل صف طالب.
= true
```

# @lesson np-reference
title: مرجع NumPy
summary: أهم الدوال مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي دالة.

```reference python
np.array | إنشاء مصفوفة | np.array([1, 2])
np.arange / np.linspace | سلاسل أرقام | np.arange(10)
np.zeros / np.ones / np.full | مصفوفات جاهزة | np.zeros((2, 2))
.shape / .reshape | الشكل وتغييره | a.reshape(2, 3)
.T | المنقول | m.T
a[i, j] / a[:, j] | الفهرسة | m[:, 0]
a[a > 5] | التصفية | a[a > 5]
np.where | اختيار بشرط | np.where(a > 0, a, 0)
sum / mean / std | الإحصاء | a.mean(axis=0)
min / max / argmax | الأطراف | a.argmax()
np.sqrt / np.round | دوال رياضية | np.round(a, 2)
@ | ضرب المصفوفات | a @ b
np.concatenate / hstack | الدمج | np.hstack([a, b])
np.unique | القيم المميزة | np.unique(a)
np.sort / argsort | الترتيب | np.argsort(a)
np.clip | حصر القيم | np.clip(a, 0, 1)
default_rng | مولد عشوائي | np.random.default_rng(1)
```

:::tip ماذا بعد؟
تابع إلى دورة **Pandas** لتحليل الجداول والبيانات الحقيقية.
:::
