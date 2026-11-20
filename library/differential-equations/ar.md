# @lesson differential-equations-initial
title: المعادلة والشرط الابتدائي
summary: المعادلة `y′=2t` تحدد الميل عند كل زمن.
---
المعادلة `y′=2t` تحدد الميل عند كل زمن. عائلة الحلول `y=t²+C` لها الميل نفسه. الشرط `y(0)=3` يختار عضوًا واحدًا من العائلة، عند C=3.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
initial = 3
for time in (0, 1, 2):
    value = time ** 2 + initial
    print(time, value)
```

```exercise
? لو y′=2t وy(0)=5، فما قيمة y(2)؟
___
= 9
```

```quiz
? لماذا نحتاج الشرط الابتدائي هنا؟
* لتحديد ثابت التكامل
- لتغيير الميل
- لحذف الزمن
> عدة حلول لها المشتقة نفسها وتختلف بمقدار ثابت.
```

# @lesson differential-equations-growth
title: النمو والاضمحلال الأسي
summary: عندما يكون معدل التغير متناسبًا مع القيمة، نكتب `y′=ky`.
---
عندما يكون معدل التغير متناسبًا مع القيمة، نكتب `y′=ky`. الحل الذي يبدأ من y₀ هو `y₀ exp(kt)`. إذا كانت القيمة الابتدائية موجبة وk سالبًا، تقل القيمة مع الزمن.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
from math import exp

for time in (0, 1, 2):
    print(time, round(100 * exp(-0.5 * time), 2))
```

```exercise
? ما y عند t=0 إذا كانت y=80 exp(−0.2t)؟
___
= 80
```

```quiz
? ماذا يحدث لقيمة موجبة في نموذج y′=−0.5y عندما يزيد الزمن؟
- تزيد
* تنخفض
- تبقى ثابتة
> المشتقة سالبة ما دامت y موجبة.
```

# @lesson differential-equations-separation
title: فصل المتغيرات
summary: لو `y′=−ty` و`y(0)=4`، نفصل المتغيرين على جزء فيه y غير صفرية.
---
لو `y′=−ty` و`y(0)=4`، نفصل المتغيرين على جزء فيه y غير صفرية. تكامل `dy/y=−t dt` يعطي `ln|y|=−t²/2+C`. الشرط الابتدائي الموجب يحدد `y=4 exp(−t²/2)`. الحل الصفري موجود أيضًا للمعادلة لكن لا يحقق الشرط.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
from math import exp

for time in (0, 1, 2):
    print(round(4 * exp(-time ** 2 / 2), 3))
```

```exercise
? ما قيمة y(0) لو y=7 exp(−t²/2)؟
___
= 7
```

```quiz
? أي حل لازم نتحقق منه منفصلًا بعد القسمة على y؟
- y=1
- y=t
* y=0
> القسمة على y تستبعد الصفر من خطوات الفصل.
```

# @lesson differential-equations-euler
title: مشروع: قارن خطوات أويلر
summary: في طريقة أويلر نحدث y باستخدام الميل الحالي في خطوة قصيرة.
---
في طريقة أويلر نحدث y باستخدام الميل الحالي في خطوة قصيرة. لحل `y′=−y` من 0 إلى 1 بقيمة أولية واحدة، قارن الناتج عند 4 و20 خطوة بالحل `exp(−1)`. تقليل الخطوة يقلل الخطأ هنا.

## جرّب بنفسك

احسب الناتج أولًا، ثم شغّل المثال وغيّر أحد المدخلات.

```try python
from math import exp

exact = exp(-1)
for steps in (4, 20):
    step = 1 / steps
    y = 1.0
    for _ in range(steps):
        y -= step * y
    print(steps, round(y, 4), round(abs(exact - y), 4))
```

```exercise
? لو أخذنا 10 خطوات متساوية من 0 إلى 1، فما طول الخطوة؟
___
= 0.1
```

```quiz
? أي ناتج أقرب إلى الحل الدقيق في المثال؟
* 20 خطوة
- 4 خطوات
- الخطأ متساوٍ
> الخطأ المطلق في 20 خطوة أصغر في المثال.
```

# @lesson differential-equations-reference
title: دليل المعادلات التفاضلية العادية
summary: راجع الأمثلة العملية وارجع لخريطة الفروع.
type: Reference
---
- [[differential-equations-ar/differential-equations-initial|المعادلة والشرط الابتدائي]]
- [[differential-equations-ar/differential-equations-growth|النمو والاضمحلال الأسي]]
- [[differential-equations-ar/differential-equations-separation|فصل المتغيرات]]
- [[differential-equations-ar/differential-equations-euler|مشروع: قارن خطوات أويلر]]

راجع [[math-branches-ar/math-branches-differential|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الفروع]].
