# @lesson operations-research-linear
title: النمذجة والبرمجة الخطية
summary: عرّف متغيرات القرار، والقيود، ودالة الهدف.
---
عرّف متغيرات القرار، والقيود، ودالة الهدف. في المثال `x+y≤4` و`x≤2` و`x,y≥0`، نريد تعظيم `3x+2y`. المنطقة مضلع محدود، وتوجد قيمة عظمى عند رأس منه. افحص الرؤوس الناتجة عن تقاطع حدود القيود.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
vertices = [(0, 0), (2, 0), (2, 2), (0, 4)]
value, point = max((3 * x + 2 * y, (x, y)) for x, y in vertices)
print(value, point)
```

```exercise
? ما قيمة الهدف عند (0,4)؟
___
= 8
```

```quiz
? أي نقطة تحقق القيود وتعطي أكبر قيمة؟
* (2, 2)
- (0, 4)
- (3, 1)
> النقطة (2,2) تحقق القيود وتعطي 10.
```

# @lesson operations-research-integer
title: القرارات الصحيحة والاسترخاء الخطي
summary: لو القرار عدد صناديق، فلازم يكون صحيحًا.
---
لو القرار عدد صناديق، فلازم يكون صحيحًا. حذف شرط الصحة يوسّع الاختيارات ويعطي حدًا أعلى لمسألة تعظيم. مع `2x≤5` وهدف `3x`، الحل المستمر x=2.5 لكن الصحيح الأفضل x=2.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
capacity, weight, value = 5, 2, 3
print(value * capacity / weight)
print(value * (capacity // weight))
```

```exercise
? ما أكبر عدد صحيح من صناديق وزن كل منها 2 إذا كانت السعة 7؟
___
= 3
```

```quiz
? ماذا يعطي الاسترخاء لمسألة تعظيم صحيحة؟
- حدًا أدنى دائمًا
* حدًا أعلى
- حلًا صحيحًا دائمًا
> الاسترخاء يسمح بكل الحلول الأصلية وقد يضيف حلولًا أفضل.
```

# @lesson operations-research-assignment
title: مشروع: وزّع مهام على عاملين
summary: لكل عامل تكلفة مختلفة حسب المهمة.
---
لكل عامل تكلفة مختلفة حسب المهمة. عيّن كل مهمة لعامل واحد وكل عامل لمهمة واحدة. في المثال الصغير نقارن جميع التباديل. ده يوضّح لماذا الاختيار الأرخص لعامل واحد قد يترك مهمة مكلفة للعامل الثاني.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from itertools import permutations

costs = [[1, 3], [2, 9]]
options = [(sum(costs[i][job] for i, job in enumerate(jobs)), jobs)
           for jobs in permutations(range(2))]
print(sorted(options))
```

```exercise
? ما إجمالي التكلفة لو أخذ العامل الأول المهمة الأولى والثاني المهمة الثانية؟
___
= 10
```

```quiz
? ما أقل تكلفة إجمالية ممكنة؟
- 3
- 10
* 5
> العامل الأول يأخذ المهمة الثانية بتكلفة 3، والثاني الأولى بتكلفة 2.
```

# @lesson operations-research-reference
title: دليل التحسين وبحوث العمليات
summary: راجع الأمثلة وارجع للدرس التمهيدي.
type: Reference
---
- [[operations-research-ar/operations-research-linear|النمذجة والبرمجة الخطية]]
- [[operations-research-ar/operations-research-integer|القرارات الصحيحة والاسترخاء الخطي]]
- [[operations-research-ar/operations-research-assignment|مشروع: وزّع مهام على عاملين]]

راجع [[math-branches-ar/math-branches-optimization|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
