# @lesson fourier-analysis-harmonics
title: الدورة والتوافقيات
summary: التوافقية رقم n على دورة `2π` هي موجة مثل `sin(nx)` تكمل n ذبذبات في الدورة.
---
التوافقية رقم n على دورة `2π` هي موجة مثل `sin(nx)` تكمل n ذبذبات في الدورة. جمع أكثر من توافقية يُنتج إشارة دورية أعقد. الفكرة هي وصف الإشارة بمقادير هذه الموجات وأطوارها.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import pi, sin

for angle in (0, pi / 4, pi / 2):
    print(round(sin(angle), 3), round(sin(2 * angle), 3))
```

```exercise
? كم ذبذبة تكمل sin(4x) من 0 إلى 2π؟
___
= 4
```

```quiz
? ما طول دورة sin(2x)؟
* π
- 2π
- 4π
> الزاوية الداخلية تتضاعف، فيكفي أن يزيد x بمقدار π.
```

# @lesson fourier-analysis-orthogonality
title: التعامد بين التوافقيات
summary: تكامل حاصل ضرب `sin(mx)` و`sin(nx)` عبر دورة كاملة يساوي صفرًا إذا كان m وn صحيحين موجبين مختلفين.
---
تكامل حاصل ضرب `sin(mx)` و`sin(nx)` عبر دورة كاملة يساوي صفرًا إذا كان m وn صحيحين موجبين مختلفين. ولو m=n يكون التكامل π. ده يسمح بقياس مساهمة تردد واحد دون خلطه بالترددات الأخرى. المثال يستخدم متوسط العينات لتوضيح الفرق.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import sin, tau

points = [tau * index / 64 for index in range(64)]
for harmonic in (1, 2):
    average = sum(sin(x) * sin(harmonic * x) for x in points) / len(points)
    print(harmonic, f'{round(average, 6) + 0.0:.6f}')
```

```exercise
? ما متوسط sin²(x) خلال دورة؟ اكتب الناتج عشريًا.
___
= 0.5
```

```quiz
? ما تكامل sin(x)sin(3x) خلال دورة كاملة؟
- π
* 0
- 2π
> الترددان مختلفان، فتتلاشى الأجزاء الموجبة والسالبة في التكامل.
```

# @lesson fourier-analysis-coefficients
title: معاملات فورييه
summary: في المثال `f(x)=1+2cos(x)+3sin(2x)`.
---
في المثال `f(x)=1+2cos(x)+3sin(2x)`. على دورة كاملة، متوسط f يعطينا الحد الثابت. وضرب f في جيب أو جيب تمام التوافقية المطلوبة ثم أخذ ضعف المتوسط يعطينا معاملها، لأن متوسط مربع التوافقية يساوي النصف ومتوسط جدائها بالتوافقيات الأخرى صفر.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import cos, sin, tau

count = 64
points = [tau * index / count for index in range(count)]
values = [1 + 2 * cos(x) + 3 * sin(2 * x) for x in points]
constant = sum(values) / count
cos_one = 2 * sum(y * cos(x) for x, y in zip(points, values, strict=True)) / count
sin_two = 2 * sum(y * sin(2 * x) for x, y in zip(points, values, strict=True)) / count
print(*(round(value, 4) for value in (constant, cos_one, sin_two)))
```

```exercise
? ما معامل cos(x) في 4 + 5cos(x)؟
___
= 5
```

```quiz
? ما متوسط الإشارة في المثال خلال دورة كاملة؟
- 2
- 3
* 1
> الجيب وجيب التمام متوسطهما صفر على الدورة، فيبقى الثابت 1.
```

# @lesson fourier-analysis-spectrum
title: مشروع: اكتشف ترددين في إشارة
summary: التحويل المتقطع يقارن العينات بأُسس مركّبة تدور بترددات مختلفة.
---
التحويل المتقطع يقارن العينات بأُسس مركّبة تدور بترددات مختلفة. هنا نفحص أربعة ترددات موجبة مرشحة لإشارة فيها موجتان، ونستخدم مقدار المعامل للمقارنة. غيّر سعة إحدى الموجتين وشوف أثرها على التردد المطابق.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from cmath import exp
from math import sin, tau

count = 32
signal = [sin(tau * i / count) + 0.5 * sin(tau * 3 * i / count)
          for i in range(count)]
for frequency in range(1, 5):
    coeff = sum(value * exp(-1j * tau * frequency * i / count)
                for i, value in enumerate(signal))
    print(frequency, round(2 * abs(coeff) / count, 3))
```

```exercise
? ما سعة التردد الثالث في المثال؟ اكتب الناتج عشريًا.
___
= 0.5
```

```quiz
? أي ترددين موجودان في الإشارة؟
* 1 و3
- 1 و2
- 2 و4
> المقدار بعد التحويل غير صفري عند 1 و3 فقط بين الترددات المفحوصة.
```

# @lesson fourier-analysis-reference
title: دليل مدخل إلى تحليل فورييه
summary: راجع الأمثلة وارجع للدروس المرتبطة.
type: Reference
---
## الأمثلة العملية

- [[fourier-analysis-ar/fourier-analysis-harmonics|الدورة والتوافقيات]]
- [[fourier-analysis-ar/fourier-analysis-orthogonality|التعامد بين التوافقيات]]
- [[fourier-analysis-ar/fourier-analysis-coefficients|معاملات فورييه]]
- [[fourier-analysis-ar/fourier-analysis-spectrum|مشروع: اكتشف ترددين في إشارة]]

## دروس مرتبطة

- [[trigonometry-ar/trigonometry-period|الدورية في الجيب]]
- [[partial-differential-equations-ar/partial-differential-equations-partials|معادلة الحرارة]]
