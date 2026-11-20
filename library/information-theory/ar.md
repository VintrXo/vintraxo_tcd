# @lesson information-theory-entropy
title: الإنتروبي والمعلومة
summary: معلومة حدث احتماله p هي `−log₂(p)` بت.
---
معلومة حدث احتماله p هي `−log₂(p)` بت. الإنتروبي متوسط هذه المعلومة على النتائج حسب احتمالاتها. الحد ذو الاحتمال صفر يساهم بصفر في المتوسط.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from math import log2

for probabilities in ([0.5, 0.5], [0.75, 0.25]):
    print(round(-sum(p * log2(p) for p in probabilities if p), 4))
```

```exercise
? كم بتًا تحمل نتيجة احتمالها 1/4؟
___
= 2
```

```quiz
? أي عملة لها إنتروبي أعلى في المثال؟
* العادلة
- المنحازة
- متساويتان
> في هذه الحالة عدم اليقين أكبر عند تساوي الاحتمالين.
```

# @lesson information-theory-conditional
title: الإنتروبي الشرطي
summary: الإنتروبي الشرطي `H(Y|X)` هو متوسط إنتروبي Y بعد معرفة X، بوزن كل قيمة لـX.
---
الإنتروبي الشرطي `H(Y|X)` هو متوسط إنتروبي Y بعد معرفة X، بوزن كل قيمة لـX. إذا حدد X قيمة Y، فلا يبقى غموض. الفرق `H(Y)−H(Y|X)` هو المعلومات المتبادلة.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
h_y = 1.0
conditional_entropy = {0: 0.0, 1: 0.0}
h_given_x = sum(0.5 * entropy for entropy in conditional_entropy.values())
print(h_given_x, h_y - h_given_x)
```

```exercise
? إذا كان Y يساوي X، فما قيمة H(Y|X)؟
___
= 0
```

```quiz
? لو X وY مستقلان وكان H(Y)=1، فما H(Y|X)؟
- 0
* 1
- 2
> مع الاستقلال، معرفة X لا تغيّر توزيع Y.
```

# @lesson information-theory-prefix
title: مشروع: قارن ترميزين
summary: في الترميز الخالي من البوادئ لا تبدأ كلمة ترميز بكلمة أخرى كاملة، فيسهل الفصل أثناء القراءة.
---
في الترميز الخالي من البوادئ لا تبدأ كلمة ترميز بكلمة أخرى كاملة، فيسهل الفصل أثناء القراءة. قارن أطوال ترميز ثابت من بتّين للرموز الثلاثة بترميز `0,10,11` يضع أقصر كلمة للرمز الأكثر تكرارًا.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
from fractions import Fraction

probabilities = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
for codes in (['00', '01', '10'], ['0', '10', '11']):
    print(sum(p * len(code) for p, code in zip(probabilities, codes, strict=True)))
```

```exercise
? أي متوسط يعطيه الترميز القصير؟ اكتب كسرًا مثل 1/2.
___
= 3/2
```

```quiz
? هل يمكن أن تكون 0 و01 في ترميز خالٍ من البوادئ معًا؟
- نعم
- لو كان طول 01 زوجيًا فقط
* لا
> الكلمة 0 بادئة للكلمة 01.
```

# @lesson information-theory-reference
title: دليل نظرية المعلومات
summary: راجع الأمثلة وارجع للدرس التمهيدي.
type: Reference
---
- [[information-theory-ar/information-theory-entropy|الإنتروبي والمعلومة]]
- [[information-theory-ar/information-theory-conditional|الإنتروبي الشرطي]]
- [[information-theory-ar/information-theory-prefix|مشروع: قارن ترميزين]]

راجع [[math-branches-ar/math-branches-information|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
