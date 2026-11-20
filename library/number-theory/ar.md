# @lesson number-theory-division
title: القسمة وخارج القسمة والباقي
summary: إذا كان `b>0`، نكتب أي عدد صحيح `a=bq+r` حيث `0≤r<b`.
---
إذا كان `b>0`، نكتب أي عدد صحيح `a=bq+r` حيث `0≤r<b`. العدد b يقسم a بالضبط عندما r=0. في Python تعطي `divmod(a,b)` الزوج `(q,r)`.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
for a in (23, -23, 25):
    quotient, remainder = divmod(a, 5)
    print(a, quotient, remainder)
```

```exercise
? ما باقي قسمة 38 على 7؟
___
= 3
```

```quiz
? متى يكون 5 قاسمًا لـa؟
* عندما يكون الباقي صفرًا
- عندما يكون الخارج صفرًا
- عندما يكون الباقي 5
> الباقي صفر يعني وجود خارج صحيح يحقق a=5q.
```

# @lesson number-theory-primes
title: الأعداد الأولية والتحليل
summary: العدد الأولي أكبر من 1 وقواسِمه الموجبة 1 والعدد نفسه.
---
العدد الأولي أكبر من 1 وقواسِمه الموجبة 1 والعدد نفسه. لو كان n مركبًا، فإن له عاملًا لا يتجاوز √n، لأن عاملين أكبر من الجذر يعطيان حاصل ضرب أكبر من n. بالقسمة المتكررة نحصل على العوامل الأولية مع تكرارها.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
value = 84
factor = 2
factors = []
while factor * factor <= value:
    while value % factor == 0:
        factors.append(factor)
        value //= factor
    factor += 1
if value > 1:
    factors.append(value)
print(factors)
```

```exercise
? ما أصغر عامل أولي للعدد 35؟
___
= 5
```

```quiz
? أي قائمة تمثل تحليل 18 إلى عوامله الأولية؟
- 2، 9
* 2، 3، 3
- 3، 6
> حاصل ضرب 2 و3 و3 هو 18، وكلها أولية.
```

# @lesson number-theory-euclid
title: إقليدس وهوية بيزو
summary: القاسم المشترك الأكبر لـa وb يساوي القاسم المشترك الأكبر لـb وباقي a عند القسمة على b.
---
القاسم المشترك الأكبر لـa وb يساوي القاسم المشترك الأكبر لـb وباقي a عند القسمة على b. بتتبّع المعاملات أثناء الخطوات نكتب القاسم في صورة `sa+tb`. المثال يبدأ بمعاملي a وb للوصول إلى هوية بيزو.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
a, b = 30, 18
old_r, r = a, b
old_s, s = 1, 0
old_t, t = 0, 1
while r:
    quotient = old_r // r
    old_r, r = r, old_r - quotient * r
    old_s, s = s, old_s - quotient * s
    old_t, t = t, old_t - quotient * t
print(old_r, old_s, old_t)
print(old_s * a + old_t * b)
```

```exercise
? أوجد القاسم المشترك الأكبر للعددين 21 و14.
___
= 7
```

```quiz
? أي تركيب يعطي القاسم المشترك الأكبر لـ30 و18؟
- 30−18
- 30+18
* −30+2×18
> −30+36 يساوي 6، آخر باقٍ غير صفري في خوارزمية إقليدس.
```

# @lesson number-theory-inverse
title: الحساب بترديد عدد والمعكوس
summary: تتطابق قيمتان بترديد m لو كان الفرق بينهما من مضاعفات m.
---
تتطابق قيمتان بترديد m لو كان الفرق بينهما من مضاعفات m. معكوس a هو عدد x يحقق `ax ≡ 1` بترديد m، ويوجد بالضبط عندما يكون القاسم المشترك الأكبر لـa وm يساوي 1. تشرح هوية بيزو السبب.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
modulus = 7
value = 3
inverses = [x for x in range(modulus) if value * x % modulus == 1]
print(inverses)
```

```exercise
? ما معكوس 2 بالضرب بترديد 5؟
___
= 3
```

```quiz
? هل للعدد 2 معكوس بالضرب بترديد 6؟
* لا
- نعم، 2
- نعم، 3
> القاسم المشترك الأكبر هو 2، وكل مضاعفات 2 تبقى زوجية بترديد 6.
```

# @lesson number-theory-reference
title: دليل نظرية الأعداد
summary: راجع الأمثلة العملية وارجع لخريطة الفروع.
type: Reference
---
- [[number-theory-ar/number-theory-division|القسمة وخارج القسمة والباقي]]
- [[number-theory-ar/number-theory-primes|الأعداد الأولية والتحليل]]
- [[number-theory-ar/number-theory-euclid|إقليدس وهوية بيزو]]
- [[number-theory-ar/number-theory-inverse|الحساب بترديد عدد والمعكوس]]

راجع [[math-branches-ar/math-branches-numbers|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الفروع]].
