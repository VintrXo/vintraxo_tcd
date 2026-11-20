# @lesson mathematical-physics-oscillation
title: المذبذب التوافقي
summary: في نموذج كتلة على زنبرك بلا احتكاك، `mx″=−kx`.
---
في نموذج كتلة على زنبرك بلا احتكاك، `mx″=−kx`. الحل الذي يبدأ من أقصى إزاحة A بسرعة صفرية هو `A cos(ωt)` حيث `ω=√(k/m)`. زيادة الصلابة ترفع التردد الزاوي عند ثبات الكتلة.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from math import pi, sqrt

mass, stiffness = 1, 4
omega = sqrt(stiffness / mass)
print(omega, round(2 * pi / omega, 3))
```

```exercise
? ما التردد الزاوي عندما k=9 وm=1؟
___
= 3
```

```quiz
? عند مضاعفة الكتلة أربع مرات مع ثبات الصلابة، ماذا يحدث للتردد الزاوي؟
* ينخفض للنصف
- يتضاعف
- لا يتغير
> الكتلة في مقام الجذر التربيعي.
```

# @lesson mathematical-physics-energy
title: حفظ الطاقة والتحقق من النموذج
summary: رياضيًا، مشتقة `E=mv²/2+kx²/2` تساوي `v(mv′+kx)=0` في نموذج الزنبرك المثالي.
---
رياضيًا، مشتقة `E=mv²/2+kx²/2` تساوي `v(mv′+kx)=0` في نموذج الزنبرك المثالي. تقدر تستخدم حفظ الطاقة كاختبار لحساباتك. الأمثلة العددية قد يظهر فيها فرق صغير من التقريب.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from math import cos, sin

m, k, amplitude, omega = 1, 4, 0.5, 2
for t in (0, 0.5, 1):
    x = amplitude * cos(omega * t)
    v = -amplitude * omega * sin(omega * t)
    print(round((m * v * v + k * x * x) / 2, 6))
```

```exercise
? ما طاقة الوضع عند x=0؟
___
= 0
```

```quiz
? ماذا يبقى ثابتًا في هذا النموذج؟
- السرعة دائمًا
* مجموع طاقتي الحركة والوضع
- الإزاحة دائمًا
> الطاقة تتحول بين الشكلين مع ثبات المجموع.
```

# @lesson mathematical-physics-wave
title: مشروع: الموجة المنتقلة
summary: الموجة `u(x,t)=sin(x−ct)` تتحرك إلى اليمين بسرعة c موجبة، لأن نفس الطور يظهر عند x أكبر بعد مرور الوقت.
---
الموجة `u(x,t)=sin(x−ct)` تتحرك إلى اليمين بسرعة c موجبة، لأن نفس الطور يظهر عند x أكبر بعد مرور الوقت. تحقق أنها تُبقي القيمة نفسها على المسار `x=x₀+ct`. في معادلة الموجة المثالية سرعة الانتشار تحدد علاقة المشتقتين الثانية في المكان والزمن.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from math import sin

speed, start = 2, 1
for t in (0, 1, 2):
    x = start + speed * t
    print(x, round(sin(x - speed * t), 3))
```

```exercise
? لو c=2 وبدأ الطور عند x=1، فأين يكون عند t=3؟
___
= 7
```

```quiz
? في أي اتجاه تتحرك الموجة لو c موجبة؟
- يسارًا
- لا تتحرك
* يمينًا
> عند ثبات الطور يزيد x بمقدار ct.
```

# @lesson mathematical-physics-reference
title: دليل الفيزياء الرياضية
summary: راجع الأمثلة وارجع للدرس التمهيدي.
type: Reference
---
- [[mathematical-physics-ar/mathematical-physics-oscillation|المذبذب التوافقي]]
- [[mathematical-physics-ar/mathematical-physics-energy|حفظ الطاقة والتحقق من النموذج]]
- [[mathematical-physics-ar/mathematical-physics-wave|مشروع: الموجة المنتقلة]]

راجع [[advanced-math-ar/advanced-math-physics|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
