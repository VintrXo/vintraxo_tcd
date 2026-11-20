# @lesson geometry-trigonometry-congruence
title: تطابق المثلثات
summary: المثلثان المتطابقان لهما الشكل والحجم نفسيهما.
---
المثلثان المتطابقان لهما الشكل والحجم نفسيهما. حالة ضلع–ضلع–ضلع تعني أن تساوي أطوال الأضلاع المتناظرة الثلاثة يكفي لإثبات التطابق. نتحقق أولًا من متباينة المثلث لاستبعاد الأطوال التي لا تكوّن مثلثًا.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
def valid_triangle(sides):
    a, b, c = sorted(sides)
    return a > 0 and a + b > c

first = (3, 4, 5)
second = (5, 3, 4)
print(valid_triangle(first) and sorted(first) == sorted(second))
print(valid_triangle((2, 3, 5)))
```

```exercise
? في مثلث أضلاعه 2 و3 و4، كم يساوي مجموع الضلعين الأقصر؟
___
= 5
```

```quiz
? لماذا لا تصلح الأطوال 2 و3 و5 لتكوين مثلث؟
* مجموع الضلعين الأقصر يساوي الأطول
- لا بد أن تتساوى الأضلاع
- الضلع الأطول فردي
> لازم يكون مجموع الضلعين الأقصر أكبر من الثالث حتى تتقفل الأضلاع على مساحة.
```

# @lesson geometry-trigonometry-similarity
title: تشابه المثلثات
summary: تساوي زاويتين متناظرتين يكفي للتشابه لأن مجموع زوايا المثلث 180 درجة فتتساوى الثالثة أيضًا.
---
تساوي زاويتين متناظرتين يكفي للتشابه لأن مجموع زوايا المثلث 180 درجة فتتساوى الثالثة أيضًا. لو كان عامل تكبير الأطوال k، تتضاعف المساحة بعامل `k²`.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
scale = 3
base, height = 4, 2
original_area = base * height / 2
scaled_area = (scale * base) * (scale * height) / 2
print(original_area, scaled_area)
```

```exercise
? كم يصبح ضلع طوله 7 بعد تكبير الأطوال بعامل 2؟
___
= 14
```

```quiz
? بكم تتضاعف المساحة عند تكبير الأطوال بعامل 3؟
- 3
* 9
- 6
> القاعدة والارتفاع يتضاعفان كل منهما بعامل 3، فنضرب العاملين.
```

# @lesson geometry-trigonometry-identity
title: الهوية المثلثية الأساسية
summary: إحداثيا نقطة دائرة الوحدة هما `cos(θ)` و`sin(θ)`.
---
إحداثيا نقطة دائرة الوحدة هما `cos(θ)` و`sin(θ)`. بعدها عن الأصل واحد، فبتطبيق فيثاغورس نحصل على `sin²(θ) + cos²(θ) = 1`. من قيمة أحدهما نعرف مقدار الآخر، والإشارة يحددها الربع.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
from math import cos, radians, sin

for angle in (30, 120, 225):
    theta = radians(angle)
    print(angle, round(sin(theta) ** 2 + cos(theta) ** 2, 8))
```

```exercise
? لو sin(θ) = 0.6، ما مقدار cos(θ) كعدد عشري؟
___
= 0.8
```

```quiz
? لو الزاوية في الربع الثاني، ما إشارة جيب التمام؟
- موجبة
- صفر دائمًا
* سالبة
> في الربع الثاني النقطة تقع يسار المحور الرأسي، فالإحداثي الأفقي سالب.
```

# @lesson geometry-trigonometry-sine
title: قانون الجيب
summary: لكل ضلع طوله a زاوية مقابلة A.
---
لكل ضلع طوله a زاوية مقابلة A. قانون الجيب يقول إن `a/sin(A) = b/sin(B) = c/sin(C)`. يمكن اشتقاق النسب بمساواة تعبيرين لارتفاع المثلث. إذا عرفت ضلعًا وزاويته وزاوية ثانية، تقدر تحسب الضلع المقابل لها.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
from math import radians, sin

a, angle_a, angle_b = 6, 30, 60
b = a * sin(radians(angle_b)) / sin(radians(angle_a))
print(round(b, 2))
```

```exercise
? إذا كانت الزاويتان المتقابلتان مع الضلعين A وB متساويتين وطول الأول 8، فكم طول الثاني؟
___
= 8
```

```quiz
? أي زاوية نضع جيبها مع الضلع b في النسبة؟
* الزاوية المقابلة لـb
- أي زاوية مجاورة لـb
- أكبر زاوية دائمًا
> كل ضلع يقترن بزاويته المقابلة.
```

# @lesson geometry-trigonometry-cosine
title: قانون جيب التمام
summary: لو عرفت ضلعين a وb والزاوية C المحصورة بينهما، فالضلع المقابل لها يحقق `c² = a² + b² − 2ab cos(C)`.
---
لو عرفت ضلعين a وb والزاوية C المحصورة بينهما، فالضلع المقابل لها يحقق `c² = a² + b² − 2ab cos(C)`. عندما تكون C قائمة يختفي الحد الأخير ونرجع لنظرية فيثاغورس.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
from math import cos, radians, sqrt

a, b = 3, 4
for angle in (60, 90, 120):
    c = sqrt(a * a + b * b - 2 * a * b * cos(radians(angle)))
    print(angle, round(c, 2))
```

```exercise
? لو a = b = 5 والزاوية بينهما 60 درجة، فكم طول الضلع المقابل؟
___
= 5
```

```quiz
? عند ثبات a وb وزيادة الزاوية من 60 إلى 120 درجة، ماذا يحدث للضلع الثالث؟
- يقصر
* يزداد طوله
- يبقى ثابتًا
> جيب التمام يقل، فيصبح المقدار المطروح أصغر وتزيد قيمة مربع الضلع.
```

# @lesson geometry-trigonometry-survey
title: مشروع: قِس المسافة بين معلمين
summary: معلمان على بُعد 30 و40 مترًا من مكان وقوفك.
---
معلمان على بُعد 30 و40 مترًا من مكان وقوفك. الزاوية بين خطّي النظر 60 درجة. ارسم مثلثًا، حدّد الضلع المقابل للزاوية، ثم احسب المسافة. كرّر الحساب بزاوية 65 درجة عشان تقدّر تأثير فرق القياس.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر أحد المدخلات وقارن.

```try python
from math import cos, radians, sqrt

for angle in (60, 65):
    distance = sqrt(30 ** 2 + 40 ** 2 - 2 * 30 * 40 * cos(radians(angle)))
    print(angle, round(distance, 1))
```

```exercise
? لو كانت زاوية النظر بين المعلمين 90 درجة، فكم مترًا تفصلهما؟
___
= 50
```

```quiz
? أي قانون يستخدم المسافتين من مكانك والزاوية المحصورة مباشرة؟
- قانون الجيب
- حساب مساحة الدائرة
* قانون جيب التمام
> المعطيات ضلعان والزاوية المحصورة، والمطلوب الضلع المقابل.
```

# @lesson geometry-trigonometry-reference
title: دليل الهندسة والمثلثات المتوسطة
summary: راجع الأمثلة وارجع للدروس المرتبطة.
type: Reference
---
## أمثلة الكورس

- [[geometry-trigonometry-ar/geometry-trigonometry-congruence|تطابق المثلثات]]
- [[geometry-trigonometry-ar/geometry-trigonometry-similarity|تشابه المثلثات]]
- [[geometry-trigonometry-ar/geometry-trigonometry-identity|الهوية المثلثية الأساسية]]
- [[geometry-trigonometry-ar/geometry-trigonometry-sine|قانون الجيب]]
- [[geometry-trigonometry-ar/geometry-trigonometry-cosine|قانون جيب التمام]]
- [[geometry-trigonometry-ar/geometry-trigonometry-survey|مشروع: قِس المسافة بين معلمين]]

## دروس مرتبطة

- [[geometry-ar/geometry-pythagoras|نظرية فيثاغورس]]
- [[trigonometry-ar/trigonometry-circle|دائرة الوحدة]]
