# @lesson complex-analysis-polar
title: الصيغة القطبية
summary: العدد المركب غير الصفري يُكتب `r(cos θ+i sin θ)`، حيث r هو المقدار وθ زاوية تحدَّد بترديد دورة كاملة.
---
العدد المركب غير الصفري يُكتب `r(cos θ+i sin θ)`، حيث r هو المقدار وθ زاوية تحدَّد بترديد دورة كاملة. عند الضرب نضرب المقدارين ونجمع الزاويتين، وده يفسّر الدوران عند الضرب في i.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from cmath import phase
from math import degrees

for z in (1 + 1j, (1 + 1j) * 1j):
    print(round(abs(z), 3), round(degrees(phase(z))))
```

```exercise
? كم درجة زاوية العدد 1+i مع المحور الحقيقي الموجب؟
___
= 45
```

```quiz
? ما أثر الضرب في i على المقدار؟
* يتركه ثابتًا
- يضاعفه
- يجعله صفرًا
> مقدار i يساوي واحدًا، فنضرب المقدار في واحد.
```

# @lesson complex-analysis-roots
title: جذور الوحدة
summary: حل `zⁿ=1` له مقدار 1، وزواياه `2πk/n` حيث k من صفر إلى n−1.
---
حل `zⁿ=1` له مقدار 1، وزواياه `2πk/n` حيث k من صفر إلى n−1. هندسيًا تقع الحلول موزعة بالتساوي على دائرة الوحدة. للجذر الرابع أربعة حلول، اثنان على كل محور.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from cmath import rect
from math import tau

count = 4
for k in range(count):
    root = rect(1, tau * k / count)
    print(round(root.real), round(root.imag), abs(root ** count - 1) < 1e-9)
```

```exercise
? كم حلًا مركبًا مميزًا للمعادلة z⁶=1؟
___
= 6
```

```quiz
? كم درجة تفصل جذرين متجاورين من جذور الوحدة الرابعة؟
- 45
* 90
- 180
> نقسّم دورة كاملة إلى أربع زوايا متساوية.
```

# @lesson complex-analysis-derivative
title: المشتقة المركبة واتجاه الاقتراب
summary: المشتقة المركبة تتطلب أن تقترب نسبة الفرق من نفس القيمة مهما كان اتجاه الخطوة.
---
المشتقة المركبة تتطلب أن تقترب نسبة الفرق من نفس القيمة مهما كان اتجاه الخطوة. لـ`z²` تختزل النسبة إلى `2z+h`. أما المرافق `conj(z)` فنسبته `conj(h)/h`، فتساوي 1 لخطوة حقيقية و−1 لخطوة تخيلية، ولذلك لا توجد مشتقة مركبة.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
z = 1 + 2j
for h in (0.01, 0.01j):
    quotient = ((z + h) ** 2 - z ** 2) / h
    print(round(quotient.real, 2), round(quotient.imag, 2))
    print(round((h.conjugate() / h).real))
```

```exercise
? ما الجزء الحقيقي من مشتقة z² عند z=1+2i؟
___
= 2
```

```quiz
? ما الذي يمنع وجود مشتقة مركبة للمرافق؟
- يحتاج قيمة حقيقية فقط
- الدالة تساوي صفرًا دائمًا
* النسبة تختلف باختلاف الاتجاه
> الاقتراب أفقيًا يعطي 1 ورأسيًا يعطي −1.
```

# @lesson complex-analysis-cauchy-riemann
title: معادلات كوشي–ريمان
summary: نفصل الدالة إلى `f=u+iv`.
---
نفصل الدالة إلى `f=u+iv`. لازم تحقق المشتقة المركبة المعادلتين `uₓ=vᵧ` و`uᵧ=−vₓ`. عندما تكون المشتقات الجزئية مستمرة قرب نقطة وتتحقق المعادلتان عندها، تكفيان للاشتقاق المركب هناك. مع `f(z)=z²` نجد `u=x²−y²` و`v=2xy`.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
x, y = 2, 3
u_x, u_y = 2 * x, -2 * y
v_x, v_y = 2 * y, 2 * x
print(u_x, u_y, v_x, v_y)
print(u_x == v_y, u_y == -v_x)
```

```exercise
? احسب uₓ عند x=3 للدالة u=x²−y².
___
= 6
```

```quiz
? أي علاقة لازم تتحقق بين uᵧ وvₓ؟
* uᵧ=−vₓ
- uᵧ=vₓ
- uᵧ=vᵧ
> بمقارنة اتجاهي الاقتراب، تظهر الإشارة السالبة من القسمة على i.
```

# @lesson complex-analysis-contours
title: مشروع: التكامل حول دائرة
summary: للتكامل حول دائرة نصف قطرها 1 عكس عقارب الساعة، نضع `z(t)=exp(it)` من 0 إلى `2π`.
---
للتكامل حول دائرة نصف قطرها 1 عكس عقارب الساعة، نضع `z(t)=exp(it)` من 0 إلى `2π`. لدالة `1/z` يصبح `z′(t)/z(t)=i`، فيساوي التكامل `2πi`. قارن بتكامل دالة `z` على نفس المسار، والذي يساوي صفرًا لأن لها دالة أصلية `z²/2`.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from cmath import exp
from math import tau

count = 128
step = tau / count
points = [exp(1j * (i + 0.5) * step) for i in range(count)]
for function in (lambda z: 1 / z, lambda z: z):
    integral = sum(function(z) * (1j * z) * step for z in points)
    print(round(abs(integral), 6))
```

```exercise
? ما الجزء الحقيقي من التكامل 2πi؟
___
= 0
```

```quiz
? ما نتيجة التكامل حول الدائرة للدالة z؟
- 2πi
* 0
- 1
> مسار الدائرة مغلق، ودالة z لها دالة أصلية تُعطي فرقًا صفرًا بين طرفي المسار.
```

# @lesson complex-analysis-reference
title: دليل مدخل إلى التحليل المركب
summary: راجع الأمثلة واربطها بالكورسات التانية.
type: Reference
---
## الأمثلة العملية

- [[complex-analysis-ar/complex-analysis-polar|الصيغة القطبية]]
- [[complex-analysis-ar/complex-analysis-roots|جذور الوحدة]]
- [[complex-analysis-ar/complex-analysis-derivative|المشتقة المركبة واتجاه الاقتراب]]
- [[complex-analysis-ar/complex-analysis-cauchy-riemann|معادلات كوشي–ريمان]]
- [[complex-analysis-ar/complex-analysis-contours|مشروع: التكامل حول دائرة]]

## دروس مرتبطة

- [[math-branches-ar/math-branches-complex|الأعداد المركبة]]
- [[real-analysis-ar/real-analysis-continuity|الاستمرارية في التحليل الحقيقي]]
