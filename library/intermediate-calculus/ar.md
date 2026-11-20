# @lesson intermediate-calculus-chain
title: قاعدة السلسلة
summary: لو `y = f(g(x))`، فالمشتقة هي مشتقة الدالة الخارجية عند `g(x)` مضروبة في مشتقة الداخلية.
---
لو `y = f(g(x))`، فالمشتقة هي مشتقة الدالة الخارجية عند `g(x)` مضروبة في مشتقة الداخلية. لمشتقة `(3x+1)²`، نضرب `2(3x+1)` في 3.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
def derivative(x):
    return 2 * (3 * x + 1) * 3

for x in (0, 1, 2):
    print(x, derivative(x))
```

```exercise
? ما مشتقة (2x + 1)² عند x = 1؟
___
= 12
```

```quiz
? ما مشتقة (3x + 1)²؟
* 6(3x + 1)
- 2(3x + 1)
- 6x
> الضرب في 3 يأتي من مشتقة المقدار الداخلي.
```

# @lesson intermediate-calculus-substitution
title: التكامل بالتعويض
summary: التعويض يعكس قاعدة السلسلة.
---
التعويض يعكس قاعدة السلسلة. في تكامل `2x(1+x²)` نختار `u = 1+x²` فيكون `du = 2x dx`. إذا كان التكامل محددًا، نحول الحدين إلى قيم u أيضًا. من x = 0 إلى 1 يتحول التكامل إلى مساحة تحت u من 1 إلى 2.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
def antiderivative(u):
    return u ** 2 / 2

print(antiderivative(2) - antiderivative(1))
```

```exercise
? لو u = 1 + x²، فما u عند x = 2؟
___
= 5
```

```quiz
? ما قيمة التكامل في المثال؟
- 2
* 1.5
- 0.5
> دالة أصلية لـu هي u²/2. الفرق بين قيمتيها عند 2 و1 هو 1.5.
```

# @lesson intermediate-calculus-parts
title: التكامل بالأجزاء
summary: قاعدة الضرب تعطي `∫u dv = uv − ∫v du`.
---
قاعدة الضرب تعطي `∫u dv = uv − ∫v du`. في تكامل `x·exp(x)` نختار `u=x` و`dv=exp(x)dx`، فنحصل على دالة أصلية `(x−1)exp(x)`. اشتقها للتحقق.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
from math import exp

def antiderivative(x):
    return (x - 1) * exp(x)

print(antiderivative(1) - antiderivative(0))
```

```exercise
? احسب التكامل المحدد لـ x·exp(x) من 0 إلى 1.
___
= 1
```

```quiz
? ليه اختيار u = x مفيد في المثال؟
- مشتقته صفر
- لأن exp(x) ثابتة
* مشتقته 1 فتتبسط المسألة
> التكامل المتبقي يصبح تكامل exp(x) وحدها.
```

# @lesson intermediate-calculus-partial
title: المشتقات الجزئية
summary: في دالة بمتغيرين، نحسب المشتقة الجزئية بالنسبة لمتغير واحد ونثبّت الآخر.
---
في دالة بمتغيرين، نحسب المشتقة الجزئية بالنسبة لمتغير واحد ونثبّت الآخر. لـ`f(x,y) = x² + xy + y²` تكون المشتقة بالنسبة إلى x هي `2x+y` وبالنسبة إلى y هي `x+2y`.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
x, y = 2, 3
partial_x = 2 * x + y
partial_y = x + 2 * y
print(partial_x, partial_y)
```

```exercise
? احسب المشتقة الجزئية بالنسبة إلى x عند (1, 2) في المثال.
___
= 4
```

```quiz
? ما مشتقة xy بالنسبة إلى y مع تثبيت x؟
* x
- y
- xy
> مع تثبيت x تكون xy دالة خطية في y بمعامل x.
```

# @lesson intermediate-calculus-gradient
title: التدرّج
summary: التدرّج متجه المشتقات الجزئية.
---
التدرّج متجه المشتقات الجزئية. إذا كان غير صفري، يشير لاتجاه أسرع زيادة محلية. لو تحرّكنا بمقدار صغير في الاتجاه العكسي، نتوقع نقصًا في قيمة الدالة. لازم نختار خطوة مناسبة ونتحقق من النقص فعليًا.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
def loss(x, y):
    return x ** 2 + y ** 2

x, y = 2, 3
step = 0.1
print(loss(x, y))
print(round(loss(x - step * 2 * x, y - step * 2 * y), 2))
```

```exercise
? ما المركبة الأولى لتدرّج x² + y² عند (2, 3)؟
___
= 4
```

```quiz
? ما الاتجاه الذي نستخدمه لخطوة نزول صغيرة؟
- نفس اتجاه التدرّج
* عكس التدرّج
- أي اتجاه ثابت دائمًا
> التدرّج يشير للزيادة المحلية، وعكسه للنقص المحلي.
```

# @lesson intermediate-calculus-fit
title: مشروع: حسّن معاملين لنموذج
summary: نموذج يتوقع قيمة y بالصيغة `m*x+b`.
---
نموذج يتوقع قيمة y بالصيغة `m*x+b`. قِس الخطأ بمتوسط مربعات الفروق، واحسب مشتقته بالنسبة للميل والمقطع. ابدأ بمعاملين صفريين، ثم خذ خطوتين عكس التدرّج وقارن الخطأ بعد كل خطوة.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
points = [(0, 1), (1, 3), (2, 5)]
slope = intercept = 0
for _ in range(3):
    errors = [(x, slope * x + intercept - y) for x, y in points]
    print(round(sum(error ** 2 for _, error in errors) / len(points), 3))
    d_slope = 2 * sum(x * error for x, error in errors) / len(points)
    d_intercept = 2 * sum(error for _, error in errors) / len(points)
    slope -= 0.1 * d_slope
    intercept -= 0.1 * d_intercept
```

```exercise
? لو كان النموذج y = 2x + 1، ما توقعه عند x = 2؟
___
= 5
```

```quiz
? ليه بنحسب مشتقتي الخطأ قبل تحديث الميل والمقطع؟
- عشان الخطأ يكون صفرًا دائمًا
- عشان المقطع ما يتغيّرش
* عشان المركبتين يخصّوا النقطة نفسها
> التدرّج متجه نقيّمه عند زوج محدد من المعاملات قبل أخذ خطوة واحدة.
```

# @lesson intermediate-calculus-reference
title: دليل التفاضل والتكامل المتوسط
summary: راجع الأمثلة وارجع للدروس المرتبطة.
type: Reference
---
## أمثلة الكورس

- [[intermediate-calculus-ar/intermediate-calculus-chain|قاعدة السلسلة]]
- [[intermediate-calculus-ar/intermediate-calculus-substitution|التكامل بالتعويض]]
- [[intermediate-calculus-ar/intermediate-calculus-parts|التكامل بالأجزاء]]
- [[intermediate-calculus-ar/intermediate-calculus-partial|المشتقات الجزئية]]
- [[intermediate-calculus-ar/intermediate-calculus-gradient|التدرّج]]
- [[intermediate-calculus-ar/intermediate-calculus-fit|مشروع: حسّن معاملين لنموذج]]

## دروس مرتبطة

- [[calculus-ar/calculus-power|قاعدة القوى]]
- [[applied-statistics-ar/applied-statistics-regression|الانحدار الخطي البسيط]]
