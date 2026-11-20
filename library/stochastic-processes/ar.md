# @lesson stochastic-processes-transition
title: مصفوفة الانتقال
summary: سلسلة ماركوف في زمن متقطع توصف باحتمالات الانتقال من كل حالة للحالة التالية.
---
سلسلة ماركوف في زمن متقطع توصف باحتمالات الانتقال من كل حالة للحالة التالية. نضع كل حالة ابتدائية في صف، ومجموع الصف يساوي واحدًا. نضرب توزيع اليوم كمُتجه صف في المصفوفة للحصول على توزيع الغد.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
matrix = [[0.8, 0.2], [0.4, 0.6]]
distribution = [0.5, 0.5]
next_day = [sum(distribution[i] * matrix[i][j] for i in range(2)) for j in range(2)]
print([round(p, 2) for p in next_day])
```

```exercise
? ما احتمال الانتقال من الحالة الأولى للثانية؟ اكتب الناتج عشريًا.
___
= 0.2
```

```quiz
? كم يساوي مجموع كل صف؟
* 1
- 0.5
- 2
> كل صف يوزّع الاحتمال الكامل بين الحالات التالية.
```

# @lesson stochastic-processes-stationary
title: التوزيع المستقر
summary: التوزيع π مستقر عندما `πP=π`.
---
التوزيع π مستقر عندما `πP=π`. لو احتمال دخول الحالة الثانية من الأولى 0.2، والخروج منها 0.4، فإن الحصة p المستقرة تحقق `p=0.2(1−p)+0.6p`، أي `p=1/3`. الاستقرار يخص التوزيع، والحالة الفردية ما زالت تتغير.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from fractions import Fraction

enter, leave = Fraction(1, 5), Fraction(2, 5)
p = enter / (enter + leave)
print(p, (1 - p) * enter + p * (1 - leave))
```

```exercise
? إذا كان الدخول والخروج متساويين وموجبين، فما الكتلة المستقرة للحالة الثانية؟ استخدم كسرًا مثل 1/3.
___
= 1/2
```

```quiz
? ماذا يحصل للتوزيع المستقر بعد انتقال واحد؟
- يتحول إلى حالة واحدة
* يبقى كما هو
- يتضاعف
> تعريف الاستقرار هو أن الانتقال يعيد التوزيع نفسه.
```

# @lesson stochastic-processes-walk
title: مشروع: احسب توزيع المشي العشوائي
summary: ابدأ من صفر وكل خطوة مستقلة تتحرك ±1 بالتساوي.
---
ابدأ من صفر وكل خطوة مستقلة تتحرك ±1 بالتساوي. احفظ احتمال كل موقع، ثم انقل نصفه إلى كل جار. بعد ثلاث خطوات، المواقع الممكنة فردية لأن كل خطوة تغيّر الزوجية.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from collections import defaultdict
from fractions import Fraction

distribution = {0: Fraction(1)}
for _ in range(3):
    next_step = defaultdict(Fraction)
    for position, probability in distribution.items():
        next_step[position - 1] += probability / 2
        next_step[position + 1] += probability / 2
    distribution = next_step
print([(position, str(probability)) for position, probability in sorted(distribution.items())])
```

```exercise
? ما احتمال الموقع 3 بعد ثلاث خطوات؟ استخدم كسرًا مثل 1/2.
___
= 1/8
```

```quiz
? أي موقع لا يمكن الوصول إليه بعد ثلاث خطوات؟
- 1
- −3
* 0
> الزوجية تتغير كل مرة، فبعد ثلاث خطوات يكون الموقع فرديًا.
```

# @lesson stochastic-processes-reference
title: دليل العمليات العشوائية
summary: راجع الأمثلة وارجع للدرس التمهيدي.
type: Reference
---
- [[stochastic-processes-ar/stochastic-processes-transition|مصفوفة الانتقال]]
- [[stochastic-processes-ar/stochastic-processes-stationary|التوزيع المستقر]]
- [[stochastic-processes-ar/stochastic-processes-walk|مشروع: احسب توزيع المشي العشوائي]]

راجع [[math-branches-ar/math-branches-stochastic|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
