# @lesson intermediate-algebra-systems
title: أنظمة المعادلات
summary: في نظام `x + y = 10` و`2x + y = 16`، اطرح الأولى من الثانية لإلغاء y، ثم عوّض عن x في الأولى.
---
في نظام `x + y = 10` و`2x + y = 16`، اطرح الأولى من الثانية لإلغاء y، ثم عوّض عن x في الأولى. الحل لازم يحقق المعادلتين.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
x = 16 - 10
y = 10 - x
print(x, y)
print(x + y == 10 and 2 * x + y == 16)
```

```exercise
? ما x في النظام x + y = 7 و2x + y = 11؟
___
= 4
```

```quiz
? ما قيمة y في مثال الدرس؟
* 4
- 6
- 10
> قيمة x تساوي 6، فتتبقى 4 من المجموع 10.
```

# @lesson intermediate-algebra-factoring
title: التحليل إلى عوامل
summary: فك الأقواس بيحوّل حاصل الضرب إلى مجموع، والتحليل بيرجعنا لحاصل الضرب.
---
فك الأقواس بيحوّل حاصل الضرب إلى مجموع، والتحليل بيرجعنا لحاصل الضرب. عشان تحلل `x² + 5x + 6`، دوّر على عددين مجموعهما 5 وحاصل ضربهما 6، فتحصل على `(x + 2)(x + 3)`.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
for x in (-3, -2, 0, 1):
    expanded = x ** 2 + 5 * x + 6
    factored = (x + 2) * (x + 3)
    print(x, expanded, factored)
```

```exercise
? في تحليل x² + 7x + 10، أحد العددين 2. ما الآخر؟
___
= 5
```

```quiz
? أي تحليل يساوي x² − 9؟
- (x − 9)(x + 1)
* (x − 3)(x + 3)
- (x − 3)²
> فرق المربعين يساوي حاصل ضرب الفرق والمجموع.
```

# @lesson intermediate-algebra-quadratics
title: المعادلات التربيعية
summary: للمعادلة `ax² + bx + c = 0` مع `a ≠ 0`، المميّز `D = b² − 4ac` يحدد عدد الحلول الحقيقية.
---
للمعادلة `ax² + bx + c = 0` مع `a ≠ 0`، المميّز `D = b² − 4ac` يحدد عدد الحلول الحقيقية. لو D موجب، الجذران هما `(-b ± √D)/(2a)`. لو صفر، يوجد جذر واحد مكرر، ولو سالب لا توجد جذور حقيقية.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
from math import sqrt

a, b, c = 1, -5, 6
discriminant = b * b - 4 * a * c
if discriminant < 0:
    print('No real roots')
else:
    roots = {(-b + sign * sqrt(discriminant)) / (2 * a) for sign in (-1, 1)}
    print(sorted(roots))
```

```exercise
? ما الجذر المكرر للمعادلة x² − 4x + 4 = 0؟
___
= 2
```

```quiz
? كم جذرًا حقيقيًا للمعادلة x² + 1 = 0؟
- 1
- 2
* 0
> المميّز يساوي −4.
```

# @lesson intermediate-algebra-exponents
title: الأسس واللوغاريتمات
summary: للأساس الموجب `b ≠ 1`، العبارة `log_b(x) = y` تعني `bʸ = x`، وشرط المدخل `x > 0`.
---
للأساس الموجب `b ≠ 1`، العبارة `log_b(x) = y` تعني `bʸ = x`، وشرط المدخل `x > 0`. مثال: `log₂(8) = 3`.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
from math import log2

for exponent in (-2, 0, 3):
    value = 2 ** exponent
    print(value, log2(value))
```

```exercise
? ما قيمة log₂(32)؟
___
= 5
```

```quiz
? ما قيمة 2 مرفوعًا للأس −3؟
* 1/8
- −8
- 8
> الأس السالب يأخذ مقلوب القوة الموجبة.
```

# @lesson intermediate-algebra-sequences
title: المتتاليات والمتسلسلات
summary: في المتتالية الحسابية نضيف فرقًا ثابتًا، وفي الهندسية نضرب في نسبة ثابتة.
---
في المتتالية الحسابية نضيف فرقًا ثابتًا، وفي الهندسية نضرب في نسبة ثابتة. المتسلسلة هي مجموع الحدود. إذا بدأت هندسية بالقيمة a ونسبتها r، فالحد رقم n هو `a × r^(n−1)`.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
arithmetic = [3 + 2 * i for i in range(4)]
geometric = [3 * 2 ** i for i in range(4)]
print(arithmetic, sum(arithmetic))
print(geometric, sum(geometric))
```

```exercise
? ما الحد الرابع في 2، 6، 18، …؟
___
= 54
```

```quiz
? ما مجموع أول أربعة حدود في 3، 6، 12، 24، …؟
- 24
* 45
- 48
> المتسلسلة تجمع الحدود الأربعة.
```

# @lesson intermediate-algebra-project
title: مشروع: استرد تكلفة تجهيز ورشة
summary: الورشة تكلف 120 للتجهيز و15 لكل مشارك.
---
الورشة تكلف 120 للتجهيز و15 لكل مشارك. سعر التذكرة 25. عرّف دالتي الإيراد والتكلفة، وعيّن أصغر عدد مشاركين يجعل الإيراد يغطي التكلفة، ثم افحص حالة انخفاض السعر إلى 23.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
from math import ceil

fixed = 120
variable = 15
for price in (25, 23):
    attendees = ceil(fixed / (price - variable))
    profit = attendees * price - (fixed + variable * attendees)
    print(price, attendees, profit)
```

```exercise
? ما نقطة التعادل بعدد الحضور لو سعر التذكرة 30؟
___
= 8
```

```quiz
? ما عدد الحضور اللازم على الأقل إذا كان سعر التذكرة 23؟
- 12
- 18
* 15
> كل مشارك يغطي 8 من التكلفة الثابتة، و120 ÷ 8 يساوي 15.
```

# @lesson intermediate-algebra-reference
title: دليل الجبر المتوسط
summary: راجع الأمثلة وكمّل في الكورسات المرتبطة.
type: Reference
---
## الأمثلة العملية

- [[intermediate-algebra-ar/intermediate-algebra-systems|أنظمة المعادلات]]
- [[intermediate-algebra-ar/intermediate-algebra-factoring|التحليل إلى عوامل]]
- [[intermediate-algebra-ar/intermediate-algebra-quadratics|المعادلات التربيعية]]
- [[intermediate-algebra-ar/intermediate-algebra-exponents|الأسس واللوغاريتمات]]
- [[intermediate-algebra-ar/intermediate-algebra-sequences|المتتاليات والمتسلسلات]]
- [[intermediate-algebra-ar/intermediate-algebra-project|مشروع: استرد تكلفة تجهيز ورشة]]

## كورسات مرتبطة

- [[algebra-ar/algebra-equations|المعادلات الخطية]]
- [[calculus-ar/calculus-limits|فكرة النهاية]]
