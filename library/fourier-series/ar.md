# @lesson fourier-series-synthesis
title: إعادة بناء الإشارة
summary: متسلسلة فورييه تجمع حدًا ثابتًا وتوافقيات جيب وجيب تمام.
---
متسلسلة فورييه تجمع حدًا ثابتًا وتوافقيات جيب وجيب تمام. المجموع الجزئي يحتفظ بعدد محدود منها. في `f(x)=1+2cos(x)+sin(3x)` نفقد الحد الأخير لو وقفنا عند التوافقية الأولى. قارن القيم عند نقطتين بدل الاعتماد على نقطة قد يختفي عندها الفرق.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import cos, pi, sin

for x in (0, pi / 2):
    partial = 1 + 2 * cos(x)
    full = partial + sin(3 * x)
    print(round(partial, 3), round(full, 3))
```

```exercise
? ما قيمة المجموع الجزئي عند x=0؟
___
= 3
```

```quiz
? أي حد يعيد القيمة الكاملة في المثال؟
* sin(3x)
- cos(3x)
- sin(x)
> التوقف عند التوافقية الأولى يُسقط التوافقية الثالثة.
```

# @lesson fourier-series-sine-series
title: متسلسلة الجيب على فترة
summary: على `[0,L]`، دوال `sin(nπx/L)` تنعدم عند الطرفين.
---
على `[0,L]`، دوال `sin(nπx/L)` تنعدم عند الطرفين. معامل النمط n هو `2/L` مضروبًا في تكامل حاصل ضرب الدالة في هذا النمط. المثال يقيس المعاملات الأولى لتوزيع مكوّن من نمطين باستخدام قاعدة المنتصف.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import pi, sin

length = 1
count = 128
width = length / count
points = [(index + 0.5) * width for index in range(count)]
for mode in (1, 3):
    integral = sum((sin(pi * x) + 0.5 * sin(3 * pi * x)) * sin(mode * pi * x)
                   for x in points) * width
    print(mode, round(2 * integral / length, 6))
```

```exercise
? ما معامل النمط الثالث في المثال؟ اكتب الناتج عشريًا.
___
= 0.5
```

```quiz
? ما قيمة نمط الجيب عند x=L؟
- 1
* 0
- L
> لأي عدد صحيح n يكون sin(nπ) صفرًا.
```

# @lesson fourier-series-heat
title: مشروع: برّد قضيبًا بنمطين
summary: لقضيب طرفاه عند الصفر، النمط `sin(nπx/L)` يتناقص بعامل `exp(−κ(nπ/L)²t)` في معادلة الحرارة.
---
لقضيب طرفاه عند الصفر، النمط `sin(nπx/L)` يتناقص بعامل `exp(−κ(nπ/L)²t)` في معادلة الحرارة. افصل التوزيع الابتدائي إلى نمطين، واضرب كل واحد بعامله ثم اجمع. النمط الثالث اضمحلاله الأُسّي أسرع بتسعة أضعاف من الأول.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر إحدى القيم.

```try python
from math import exp, pi, sin

length, diffusivity = 1, 1 / pi ** 2
x = 0.5
for time in (0, 0.25, 1):
    first = exp(-diffusivity * (pi / length) ** 2 * time)
    third = 0.5 * exp(-diffusivity * (3 * pi / length) ** 2 * time)
    temperature = first * sin(pi * x / length) + third * sin(3 * pi * x / length)
    print(time, round(temperature, 3))
```

```exercise
? كم ضعفًا يبلغ معدل اضمحلال النمط الثالث مقارنةً بالأول؟
___
= 9
```

```quiz
? أي نمط يبقى أثره لمدة أطول؟
- الثالث
- يتلاشيان بنفس المعدّل
* الأول
> معدل الاضمحلال يتناسب مع مربع رقم النمط.
```

# @lesson fourier-series-reference
title: دليل متسلسلات فورييه ومعادلة الحرارة
summary: راجع الأمثلة والأساس المطلوب قبل التطبيق.
type: Reference
---
- [[fourier-series-ar/fourier-series-synthesis|إعادة بناء الإشارة]]
- [[fourier-series-ar/fourier-series-sine-series|متسلسلة الجيب على فترة]]
- [[fourier-series-ar/fourier-series-heat|مشروع: برّد قضيبًا بنمطين]]

راجع [[fourier-analysis-ar/fourier-analysis-coefficients|الدرس الأساسي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
