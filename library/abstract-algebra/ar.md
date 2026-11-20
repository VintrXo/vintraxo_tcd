# @lesson abstract-algebra-groups
title: مسلّمات الزمرة
summary: الزمرة مجموعة مع عملية مغلقة وتجميعية، لها عنصر محايد ومعكوس لكل عنصر.
---
الزمرة مجموعة مع عملية مغلقة وتجميعية، لها عنصر محايد ومعكوس لكل عنصر. الأعداد `0` إلى `5` مع الجمع بترديد 6 زمرة، والمحايد صفر. التجميعية تأتي من الجمع العادي، وأخذ الباقي لا يغيّر النتيجة بترديد 6.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
modulus = 6
for value in range(modulus):
    inverse = (-value) % modulus
    print(value, inverse, (value + inverse) % modulus)
```

```exercise
? ما معكوس 1 بالجمع بترديد 6؟
___
= 5
```

```quiz
? ما العنصر المحايد للجمع في المثال؟
* 0
- 1
- 5
> إضافة الصفر تترك كل عنصر كما هو.
```

# @lesson abstract-algebra-cyclic
title: الزمر الدورية ورتبة العنصر
summary: رتبة العنصر في زمرة جمعيّة هي أصغر عدد موجب من تكرارات جمعه تعيدنا للصفر.
---
رتبة العنصر في زمرة جمعيّة هي أصغر عدد موجب من تكرارات جمعه تعيدنا للصفر. العنصر يولّد كل البواقي لو مرّ عليها كلها قبل الرجوع. بترديد 6، العنصر 2 يولّد المجموعة `{0,2,4}`، أما 5 فيولّد الزمرة كلها.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import gcd

modulus = 6
for value in (0, 2, 5):
    order = modulus // gcd(value, modulus)
    multiples = [(i * value) % modulus for i in range(order)]
    print(value, order, multiples)
```

```exercise
? كم رتبة 3 بالجمع بترديد 6؟
___
= 2
```

```quiz
? أي عنصر في الخيارات يولّد كل البواقي بترديد 6؟
- 2
* 5
- 3
> القاسم المشترك الأكبر لـ5 و6 يساوي 1، فرتبة 5 تساوي 6.
```

# @lesson abstract-algebra-subgroups
title: الزمر الجزئية والفئات الجانبية
summary: الزمرة الجزئية زمرة بداخل زمرة أكبر بنفس العملية.
---
الزمرة الجزئية زمرة بداخل زمرة أكبر بنفس العملية. لو `H={0,2,4}` تحت الجمع بترديد 6، فالفئة الجانبية `a+H` تتكوّن بإضافة a لكل عنصر. الفئات المميزة تقسم الزمرة إلى أجزاء متساوية الحجم، وهي هنا الزوجيات والفرديات.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
subgroup = (0, 2, 4)
cosets = {tuple(sorted((a + h) % 6 for h in subgroup)) for a in range(6)}
for coset in sorted(cosets):
    print(coset)
```

```exercise
? كم عنصرًا في كل فئة جانبية في المثال؟
___
= 3
```

```quiz
? ما الفئة 1+H؟
- {0, 2, 4}
- {1, 2, 3}
* {1, 3, 5}
> نضيف 1 للأعداد الزوجية في H فنحصل على البواقي الفردية.
```

# @lesson abstract-algebra-homomorphism
title: التماثلات الحافظة للعملية والنواة
summary: التماثل الحافظ للعملية يحقق `f(a+b)=f(a)+f(b)` في الزمر الجمعية.
---
التماثل الحافظ للعملية يحقق `f(a+b)=f(a)+f(b)` في الزمر الجمعية. إرسال باقي القسمة بترديد 6 إلى باقيه بترديد 2 يحفظ الجمع لأن 2 يقسم 6. النواة هي عناصر المصدر التي تذهب إلى المحايد، وهنا هي `{0,2,4}`.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
def parity(value):
    return value % 2

kernel = [x for x in range(6) if parity(x) == 0]
preserves = all(parity((a + b) % 6) == (parity(a) + parity(b)) % 2
                for a in range(6) for b in range(6))
print(kernel)
print(preserves)
```

```exercise
? كم عنصرًا في نواة تحويل الباقي بترديد 6 إلى الباقي بترديد 2؟
___
= 3
```

```quiz
? أي عنصر صورته هي المحايد؟
* 4
- 1
- 5
> المحايد في الهدف صفر، و4 زوجي.
```

# @lesson abstract-algebra-fields
title: الحلقات والحقول
summary: الحلقة فيها جمع وضرب مرتبطان بالتوزيع.
---
الحلقة فيها جمع وضرب مرتبطان بالتوزيع. في الحقل، كل عنصر غير صفري له معكوس ضربي. البواقي بترديد عدد أولي تكوّن حقلًا. بترديد 6، العدد 2 غير صفري لكنه بلا معكوس، لأن كل مضاعفاته تعطي باقيًا زوجيًا.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
for modulus in (5, 6):
    units = [a for a in range(1, modulus)
             if any(a * b % modulus == 1 for b in range(1, modulus))]
    print(modulus, units)
```

```exercise
? ما المعكوس الضربي لـ3 بترديد 5؟
___
= 2
```

```quiz
? هل كل عنصر غير صفري بترديد 6 له معكوس ضربي؟
- نعم
* لا
- فقط لو استبعدنا الصفر
> العدد 2 غير صفري ومع ذلك لا يوجد عدد يضربه إلى 1 بترديد 6.
```

# @lesson abstract-algebra-reference
title: دليل الجبر المجرّد
summary: راجع الأمثلة واربطها بالكورسات التانية.
type: Reference
---
## الأمثلة العملية

- [[abstract-algebra-ar/abstract-algebra-groups|مسلّمات الزمرة]]
- [[abstract-algebra-ar/abstract-algebra-cyclic|الزمر الدورية ورتبة العنصر]]
- [[abstract-algebra-ar/abstract-algebra-subgroups|الزمر الجزئية والفئات الجانبية]]
- [[abstract-algebra-ar/abstract-algebra-homomorphism|التماثلات الحافظة للعملية والنواة]]
- [[abstract-algebra-ar/abstract-algebra-fields|الحلقات والحقول]]

## دروس مرتبطة

- [[number-theory-ar/number-theory-inverse|المعكوس بترديد عدد]]
- [[math-branches-ar/math-branches-abstract|المدخل للجبر المجرّد]]
