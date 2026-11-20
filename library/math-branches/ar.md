# @lesson math-branches-map
title: خريطة فروع الرياضيات
summary: اختر نقطة بداية وشوف إزاي الفروع مرتبطة.
type: Reference
---
ابدأ بالكورسات المرتبطة أدناه، وبعدها استكشف فكرة من كل فرع في الدروس التمهيدية الثلاثة عشر.

## الكورسات الموجودة في المكتبة

- [[math-arithmetic-algebra-ar/arith-order|الحساب والنسب]]
- [[math-arithmetic-algebra-ar/algebra-variables|أساسيات الجبر]]
- [[math-functions-trig-ar/functions-rule|الدوال والرسوم]]
- [[math-geometry-ar/geometry-rectangles|الهندسة والقياس]]
- [[math-functions-trig-ar/trigonometry-angles|حساب المثلثات]]
- [[math-calculus-ar/calculus-limits|التفاضل والتكامل]]
- [[math-linear-algebra-ar/linear-algebra-vectors|الجبر الخطي]]
- [[math-statistics-ar/statistics-mean|الإحصاء والاحتمالات]]
- [[math-discrete-ar/discrete-math-logic|الرياضيات المتقطعة]]
- [[math-arithmetic-algebra-ar/intermediate-algebra-systems|الجبر المتوسط]]
- [[math-statistics-ar/applied-statistics-bayes|الاحتمالات والإحصاء التطبيقي]]
- [[math-linear-algebra-ar/applied-linear-algebra-elimination|الجبر الخطي التطبيقي]]
- [[math-geometry-ar/geometry-trigonometry-congruence|الهندسة والمثلثات المتوسطة]]
- [[math-calculus-ar/intermediate-calculus-chain|التفاضل والتكامل المتوسط]]
- [[math-discrete-ar/mathematical-proof-direct|أساليب البرهان الرياضي]]
- [[math-discrete-ar/number-theory-division|نظرية الأعداد]]
- [[math-pure-ar/real-analysis-sequences|مدخل إلى التحليل الحقيقي]]
- [[math-calculus-ar/differential-equations-initial|المعادلات التفاضلية العادية]]
- [[math-applied-ar/numerical-methods-error|الطرق العددية]]
- [[math-pure-ar/abstract-algebra-groups|الجبر المجرّد]]
- [[math-pure-ar/complex-analysis-polar|مدخل إلى التحليل المركب]]
- [[math-pure-ar/topology-open-sets|مدخل إلى الطوبولوجيا]]
- [[math-pure-ar/measure-theory-sigma|مدخل إلى نظرية القياس]]

## الكورسات المتخصصة

- [[math-pure-ar/functional-analysis-norm|التحليل الدالي]]
- [[math-physics-ar/differential-geometry-tangent|الهندسة التفاضلية]]
- [[math-physics-ar/partial-differential-equations-partials|المعادلات التفاضلية الجزئية]]
- [[math-physics-ar/mathematical-physics-oscillation|الفيزياء الرياضية]]
- [[math-discrete-ar/combinatorics-inclusion|التوافقيات]]
- [[math-pure-ar/category-theory-composition|نظرية الفئات]]
- [[math-applied-ar/operations-research-linear|التحسين وبحوث العمليات]]
- [[math-statistics-ar/stochastic-processes-transition|العمليات العشوائية]]
- [[math-applied-ar/information-theory-entropy|نظرية المعلومات]]
- [[math-applied-ar/game-theory-responses|نظرية الألعاب]]
- [[math-calculus-ar/vector-calculus-direction|حساب المتجهات]]
- [[math-physics-ar/fourier-analysis-harmonics|مدخل إلى تحليل فورييه]]
- [[math-physics-ar/fourier-series-synthesis|متسلسلات فورييه ومعادلة الحرارة]]
- [[math-physics-ar/vector-integral-theorems-green|مبرهنات التكامل في حساب المتجهات]]
- [[math-linear-algebra-ar/matrix-decompositions-least-squares|المربعات الصغرى وSVD وPCA]]
- [[math-statistics-ar/statistical-models-normal|التوزيعات والنماذج الإحصائية]]
- [[math-pure-ar/complex-residues-cauchy|كوشي ولوران والبواقي]]
- [[math-pure-ar/integration-spaces-convergence|مبرهنات التقارب وفضاءات باناخ وهيلبرت]]
- [[math-discrete-ar/graph-theory-degree|نظرية الرسوم البيانية]]
- [[math-applied-ar/convex-optimization-convexity|التحسين المحدّب]]
- [[math-physics-ar/fourier-waves-standing|متسلسلات فورييه ومعادلة الموجة]]
- [[math-applied-ar/algorithmic-algebra-horner|الجبر الخوارزمي]]
- [[math-geometry-ar/computational-geometry-orientation|الهندسة الحسابية]]

## اختار اتجاه الدراسة

للبراهين، ابدأ بالمنطق ونظرية الأعداد ثم الجبر المجرّد والتحليل الحقيقي. للنمذجة، ابدأ بالتفاضل قبل المعادلات التفاضلية، ثم جرّب الطرق العددية والتحسين. للبيانات، ابدأ بالإحصاء الوصفي والاحتمالات قبل الاستدلال والنماذج العشوائية.

## موضوعات للتعمّق

بعد الجولة التمهيدية، افتح دليل الموضوعات المتقدمة عشان تجرّب أمثلة في نظرية القياس، والتحليل الدالي، والهندسة التفاضلية، والمعادلات التفاضلية الجزئية، والفيزياء الرياضية، والتوافقيات المتقدمة، ونظرية الفئات.

# @lesson math-branches-numbers
title: نظرية الأعداد
summary: خوارزمية إقليدس تستبدل العددين بالباقي والقاسم حتى يصبح الباقي صفرًا، ويبقى القاسم المشترك الأكبر ثابتًا.
---
خوارزمية إقليدس تستبدل العددين بالباقي والقاسم حتى يصبح الباقي صفرًا، ويبقى القاسم المشترك الأكبر ثابتًا.

## جرّب بنفسك

```try python
a, b = 84, 30
while b:
    a, b = b, a % b
print(a)
```

```exercise
? أوجد القاسم المشترك الأكبر لـ12 و30.
___
= 6
```

```quiz
? كم القاسم المشترك الأكبر لـ18 و24؟
* 6
- 2
- 12
> العدد 6 يقسم العددين، وقواسم 18 الأكبر منه لا تقسم 24.
```

# @lesson math-branches-proof
title: المنطق والبرهان
summary: مثال مضاد واحد يكفي لنقض دعوى عامة.
---
مثال مضاد واحد يكفي لنقض دعوى عامة. ولإثبات أن مربع كل عدد زوجي زوجي، اكتب العدد بالشكل `2k`، فيصبح مربعه `4k²` من مضاعفات 2.

## جرّب بنفسك

```try python
for n in (2, 3, 5, 7):
    if n % 2 == 0:
        print(n)
```

```exercise
? اكتب مثالًا مضادًا للدعوى أن كل مضاعفات 3 زوجية. استخدم أصغر عدد موجب ينقضها.
___
= 3
```

```quiz
? أي عدد ينقض دعوى أن كل عدد أولي فردي؟
- 3
* 2
- 7
> العدد 2 أولي وزوجي.
```

# @lesson math-branches-abstract
title: الجبر المجرّد
summary: الجمع بترديد 5 يعطي مثالًا على زمرة: العملية مغلقة وتجميعية، والصفر محايد، ولكل عنصر معكوس جمعي.
---
الجمع بترديد 5 يعطي مثالًا على زمرة: العملية مغلقة وتجميعية، والصفر محايد، ولكل عنصر معكوس جمعي. معكوس 2 هو 3 لأن مجموعهما يساوي صفرًا بترديد 5.

## جرّب بنفسك

```try python
for x in range(5):
    print(x, (-x) % 5)
```

```exercise
? ما العنصر المحايد للجمع بترديد 5؟
___
= 0
```

```quiz
? ما المعكوس الجمعي للعدد 1 بترديد 5؟
- 0
- 1
* 4
> مجموع 1 و4 يقبل القسمة على 5.
```

# @lesson math-branches-analysis
title: التحليل الحقيقي
summary: المتتالية `1/n` تتقارب للصفر.
---
المتتالية `1/n` تتقارب للصفر. لأي هامش موجب `ε`، اختر عددًا صحيحًا `N > 1/ε`، فيكون `1/n < ε` لكل `n ≥ N`. الخاصية تنطبق مهما صغر الهامش.

## جرّب بنفسك

```try python
from fractions import Fraction

for tolerance in (Fraction(1, 10), Fraction(1, 100)):
    n = int(1 / tolerance) + 1
    print(n, Fraction(1, n) < tolerance)
```

```exercise
? ما أصغر n صحيح موجب يحقق 1/n < 0.1؟
___
= 11
```

```quiz
? ما أصغر عدد صحيح موجب n يحقق 1/n < 0.01؟
* 101
- 100
- 99
> عند 100 تتحقق المساواة، والشرط يتطلب أقل من.
```

# @lesson math-branches-complex
title: الأعداد المركبة
summary: نمثل `a + bi` بالنقطة `(a, b)` حيث `i² = −1`.
---
نمثل `a + bi` بالنقطة `(a, b)` حيث `i² = −1`. الضرب في `i` يحوّل `(a, b)` إلى `(−b, a)`، أي دوران 90 درجة عكس عقارب الساعة. هذه الحسابات تمهّد لدراسة التحليل المركب.

## جرّب بنفسك

```try python
print((2 + 3j) * 1j)
print(abs(3 + 4j))
```

```exercise
? ما الجزء التخيلي من (2 + 3i) × i؟ اكتب معامل i فقط.
___
= 2
```

```quiz
? ما مقدار العدد 3 + 4i؟
- 7
* 5
- 25
> نجمع مربعي 3 و4 ثم نأخذ الجذر.
```

# @lesson math-branches-topology
title: الطوبولوجيا
summary: تدرس الطوبولوجيا خصائص تبقى عند تشويه الشكل باستمرار من غير قطع أو لصق.
---
تدرس الطوبولوجيا خصائص تبقى عند تشويه الشكل باستمرار من غير قطع أو لصق. مثال على خط الأعداد: الفترة متصلة، وفترتان تفصل بينهما فجوة تكوّنان مكوّنين متصلين.

## جرّب بنفسك

```try python
def connected(first, second):
    left, right = sorted((first, second))
    return left[1] >= right[0]

print(connected((0, 1), (1, 2)))
print(connected((0, 1), (2, 3)))
```

```exercise
? كم مكوّنًا في اتحاد الفترتين [0, 1] و[2, 3]؟
___
= 2
```

```quiz
? كم مكوّنًا متصلًا في اتحاد الفترتين المغلقتين [0, 1] و[1, 2]؟
- 2
- 3
* 1
> تلتقيان عند 1، واتحادهما الفترة [0, 2].
```

# @lesson math-branches-differential
title: المعادلات التفاضلية
summary: المعادلة التفاضلية تربط دالة بمعدل تغيّرها.
---
المعادلة التفاضلية تربط دالة بمعدل تغيّرها. في `y′ = −0.2y` ينقص المتغير بمعدل يتناسب مع قيمته. طريقة أويلر تقرّب القيمة التالية بإضافة المعدل الحالي مضروبًا في طول الخطوة.

## جرّب بنفسك

```try python
y = 100
for _ in range(3):
    y += -0.2 * y * 0.5
    print(round(y, 2))
```

```exercise
? ابدأ من 50 والمعدل −10 والخطوة 0.5. احسب القيمة التالية.
___
= 45
```

```quiz
? لو بدأنا عند 100 والمعدل −20 وطول الخطوة 0.5، فما القيمة التالية بالتقريب؟
* 90
- 80
- 110
> نضيف −20 × 0.5 إلى 100.
```

# @lesson math-branches-numerical
title: الطرق العددية
summary: طريقة التنصيف تحصر جذر دالة متصلة بين طرفين قيمتاهما مختلفتا الإشارة.
---
طريقة التنصيف تحصر جذر دالة متصلة بين طرفين قيمتاهما مختلفتا الإشارة. افحص المنتصف، واحتفظ بالنصف الذي يحافظ على اختلاف الإشارة، أو توقّف لو كان المنتصف جذرًا.

## جرّب بنفسك

```try python
def f(x):
    return x * x - 2

left, right = 1, 2
for _ in range(12):
    middle = (left + right) / 2
    if f(middle) > 0:
        right = middle
    else:
        left = middle
print(round((left + right) / 2, 3))
```

```exercise
? ما منتصف الفترة من 1 إلى 3؟
___
= 2
```

```quiz
? إذا كان طول الفترة 8، كم يصبح بعد تنصيفها مرتين؟
- 4
* 2
- 1
> نقسم الطول على 2 مرتين.
```

# @lesson math-branches-optimization
title: التحسين وبحوث العمليات
summary: في التحسين نختار قرارًا يحقق القيود ويحسّن الهدف.
---
في التحسين نختار قرارًا يحقق القيود ويحسّن الهدف. هنا النوع A يستخدم وحدتين وقيمته 4، والنوع B يستخدم ثلاث وحدات وقيمته 7. نجرّب الاختيارات التي تسعها سعة 7 وحدات.

## جرّب بنفسك

```try python
choices = []
for a in range(4):
    for b in range(3):
        if 2 * a + 3 * b <= 7:
            choices.append((4 * a + 7 * b, a, b))
print(max(choices))
```

```exercise
? كم وحدة سعة يستخدم عنصران من A وعنصر من B؟
___
= 7
```

```quiz
? ما أعلى قيمة ممكنة في المثال؟
- 14
- 21
* 15
> اختيار عنصرين من A وواحد من B يملأ السعة ويعطي 15.
```

# @lesson math-branches-inference
title: الاستدلال الإحصائي
summary: نستخدم عينة لتقدير خصائص المجتمع.
---
نستخدم عينة لتقدير خصائص المجتمع. عند تقدير نسبة من مشاهدات مستقلة، الخطأ المعياري المقدّر يساوي الجذر التربيعي لـ`p(1 − p)/n` حيث `p` نسبة العينة. زيادة الحجم تقلّل التذبذب لكنها لا تعالج التحيّز.

## جرّب بنفسك

```try python
from math import sqrt

p = 0.6
for size in (100, 400):
    print(round(sqrt(p * (1 - p) / size), 4))
```

```exercise
? اكتب نسبة 30 نجاحًا من 100 كعدد عشري مثل 0.25.
___
= 0.3
```

```quiz
? مع ثبات النسبة، في كم نضرب حجم العينة حتى ينخفض الخطأ المعياري إلى النصف؟
* 4
- 2
- 8
> الجذر التربيعي لأربعة يساوي اثنين.
```

# @lesson math-branches-stochastic
title: النماذج العشوائية
summary: في نموذج ماركوف يعتمد توزيع الحالة التالية على الحالة الحالية.
---
في نموذج ماركوف يعتمد توزيع الحالة التالية على الحالة الحالية. المثال يفترض أن احتمال المطر غدًا هو 0.2 بعد يوم جاف و0.6 بعد يوم ممطر، ويحسب الاحتمال بوزن كل انتقال باحتمال حالة اليوم.

## جرّب بنفسك

```try python
rain = 0.0
for _ in range(3):
    rain = 0.2 * (1 - rain) + 0.6 * rain
    print(round(rain, 3))
```

```exercise
? لو كان المطر اليوم مؤكدًا، اكتب احتمال المطر غدًا كعدد عشري.
___
= 0.6
```

```quiz
? ما احتمال المطر غدًا لو كان احتمال المطر اليوم 0.5؟
- 0.2
* 0.4
- 0.6
> نحسب 0.5 × 0.2 + 0.5 × 0.6.
```

# @lesson math-branches-information
title: نظرية المعلومات
summary: يقيس إنتروبي شانون عدم اليقين قبل معرفة النتيجة.
---
يقيس إنتروبي شانون عدم اليقين قبل معرفة النتيجة. لعملة عادلة قيمته بت واحد. لو كانت النتيجة مؤكدة فقيمته صفر. نحسب مجموع `−p × log₂(p)` لكل احتمال موجب.

## جرّب بنفسك

```try python
from math import log2

def entropy(probabilities):
    return -sum(p * log2(p) for p in probabilities if p > 0)

print(entropy([0.5, 0.5]))
print(round(entropy([0.75, 0.25]), 4))
```

```exercise
? كم بتًا في إنتروبي عملة عادلة؟
___
= 1
```

```quiz
? كم بتًا في إنتروبي نتيجة مؤكدة؟
- 1
- 2
* 0
> احتمال النتيجة المؤكدة واحد، ولوغاريتم الواحد صفر.
```

# @lesson math-branches-games
title: نظرية الألعاب
summary: في لعبة لشخصين، عائد كل لاعب قد يتأثر بقرار خصمه.
---
في لعبة لشخصين، عائد كل لاعب قد يتأثر بقرار خصمه. الاستراتيجية المهيمنة بصرامة تعطي عائدًا أعلى من كل بديل أمام كل اختيار ممكن للخصم. المثال يعرض عوائد لاعب واحد لاستراتيجيتين أمام عمودين.

## جرّب بنفسك

```try python
a = [3, 4]
b = [1, 5]
for payoff_a, payoff_b in zip(a, b, strict=True):
    print('A' if payoff_a > payoff_b else 'B')
```

```exercise
? ما أفضل اختيار أمام العمود الأول؟ اكتب A أو B.
___
= A
```

```quiz
? ما أفضل اختيار للاعب أمام العمود الثاني؟
* B
- A
- A أو B
> عند العمود الثاني يعطي B عائد 5 مقابل 4 لـA.
```
