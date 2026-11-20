# @lesson applied-linear-algebra-elimination
title: الحذف لحل الأنظمة
summary: نحوّل النظام إلى مصفوفة معاملات وطرف أيمن.
---
نحوّل النظام إلى مصفوفة معاملات وطرف أيمن. الحذف يطرح مضاعفات من الصفوف لإزالة متغير، ثم يرجع بالتعويض. `numpy.linalg.solve` يحل النظام المربع عندما تكون المصفوفة قابلة للعكس.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
import numpy as np

matrix = np.array([[1, 1], [2, 1]])
totals = np.array([10, 16])
solution = np.linalg.solve(matrix, totals)
print(solution.tolist())
print(bool(np.allclose(matrix @ solution, totals)))
```

```exercise
? أوجد x لو x + y = 8 و2x + y = 13.
___
= 5
```

```quiz
? ماذا نتحقق منه بضرب المصفوفة في الحل؟
* استرجاع الطرف الأيمن
- أن جميع المعاملات صفر
- أن الحل دائمًا موجب
> الحل يحقق A x = b، فيُرجع الطرف الأيمن.
```

# @lesson applied-linear-algebra-span
title: الامتداد والاستقلال الخطي
summary: امتداد مجموعة متجهات هو كل التركيبات الخطية منها.
---
امتداد مجموعة متجهات هو كل التركيبات الخطية منها. المتجهات مستقلة إذا كان التركيب الذي يعطي الصفر يتطلب أن تكون كل المعاملات صفرًا. في المستوى، متجهان غير صفريين متناسبان يولدان خطًا، ومتجهان غير متناسبين يولدان المستوى.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
import numpy as np

line = np.array([[1, 2], [2, 4]])
plane = np.array([[1, 0], [2, 1]])
print(np.linalg.matrix_rank(line))
print(np.linalg.matrix_rank(plane))
```

```exercise
? كم بُعدًا في امتداد المتجهين (1, 0) و(0, 1)؟
___
= 2
```

```quiz
? هل (1, 2) و(2, 4) مستقلان؟
- نعم
* لا
- فقط إذا غيرنا ترتيبهما
> المتجه الثاني ضعف الأول.
```

# @lesson applied-linear-algebra-determinant
title: المحدد وقابلية العكس
summary: محدد مصفوفة 2 × 2 هو `ad − bc`.
---
محدد مصفوفة 2 × 2 هو `ad − bc`. قيمته المطلقة عامل تغيير المساحة، والصفر يعني أن التحويل يسحق المستوى إلى خط أو نقطة، فالمصفوفة غير قابلة للعكس.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
def determinant(matrix):
    (a, b), (c, d) = matrix
    return a * d - b * c

print(determinant([[2, 1], [0, 3]]))
print(determinant([[1, 2], [2, 4]]))
```

```exercise
? احسب محدد مصفوفة صفها الأول (3, 0) والثاني (1, 2).
___
= 6
```

```quiz
? ما القيمة التي تدل أن المصفوفة المربعة غير قابلة للعكس؟
- 1
- −1
* 0
> المحدد الصفري يعني أن التحويل يفقد بُعدًا.
```

# @lesson applied-linear-algebra-eigen
title: القيم والمتجهات الذاتية
summary: المتجه الذاتي v متجه غير صفري يحقق `Av = λv`.
---
المتجه الذاتي v متجه غير صفري يحقق `Av = λv`. التحويل يضرب المتجه في عدد λ، فيحافظ على الخط الذي يقع عليه حتى لو عكس الاتجاه، وقد يرسله للصفر عندما λ = 0.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
import numpy as np

matrix = np.array([[3, 0], [0, 2]])
vector = np.array([1, 0])
print((matrix @ vector).tolist())
print(np.linalg.eigvalsh(matrix).tolist())
```

```exercise
? ما القيمة الذاتية الموافقة للمتجه (0, 1) في مثال الدرس؟
___
= 2
```

```quiz
? أي متجه ممنوع في تعريف المتجه الذاتي؟
* المتجه الصفري
- المتجه (1, 0)
- المتجه (0, 1)
> المتجه الصفري يحقق المعادلة مع كل λ، فلا يحدد قيمة ذاتية.
```

# @lesson applied-linear-algebra-projection
title: الإسقاط على اتجاه
summary: إسقاط w على اتجاه متجه غير صفري v يعطينا `(w · v)/(v · v) × v`.
---
إسقاط w على اتجاه متجه غير صفري v يعطينا `(w · v)/(v · v) × v`. نطرح الإسقاط من w فتبقى مركبة متعامدة على v. الفكرة مستخدمة في تقريب البيانات بأقرب نقطة في فضاء أصغر.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
import numpy as np

w = np.array([3, 1])
v = np.array([1, 1])
projection = (w @ v) / (v @ v) * v
residual = w - projection
print(projection.tolist())
print(float(residual @ v))
```

```exercise
? ما المركبة الثانية لإسقاط (4, 3) على محور x؟
___
= 0
```

```quiz
? ما ناتج الضرب النقطي بين الباقي واتجاه الإسقاط؟
- 1
* 0
- 2
> الباقي متعامد على اتجاه الإسقاط.
```

# @lesson applied-linear-algebra-project
title: مشروع: حوّل شكلًا باستخدام NumPy
summary: مثّل كل نقطة كعمود.
---
مثّل كل نقطة كعمود. كوّن مصفوفة تمديد أفقي بمعامل 2 ومصفوفة دوران 90 درجة عكس عقارب الساعة. في `rotation @ stretch @ points`، التمديد يحصل أولًا. اعكس الترتيب وقارن إحداثيات النقاط.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر أحد المدخلات وشوف الفرق.

```try python
import numpy as np

points = np.array([[0, 1, 0], [0, 1, 2]])
stretch = np.array([[2, 0], [0, 1]])
rotation = np.array([[0, -1], [1, 0]])
print((rotation @ stretch @ points).T.tolist())
print((stretch @ rotation @ points).T.tolist())
```

```exercise
? ما الإحداثي الرأسي للنقطة (1, 1) بعد التمديد أولًا ثم الدوران؟
___
= 2
```

```quiz
? في المثال، هل عكس الترتيب يحافظ على كل إحداثيات الشكل؟
- نعم
- فقط لأن المحدد سالب
* لا
> النقطة (1, 1) تذهب إلى (−1, 2) في ترتيب وإلى (−2, 1) في الآخر.
```

# @lesson applied-linear-algebra-reference
title: دليل الجبر الخطي التطبيقي
summary: راجع الأمثلة وكمّل في الكورسات المرتبطة.
type: Reference
---
## الأمثلة العملية

- [[applied-linear-algebra-ar/applied-linear-algebra-elimination|الحذف لحل الأنظمة]]
- [[applied-linear-algebra-ar/applied-linear-algebra-span|الامتداد والاستقلال الخطي]]
- [[applied-linear-algebra-ar/applied-linear-algebra-determinant|المحدد وقابلية العكس]]
- [[applied-linear-algebra-ar/applied-linear-algebra-eigen|القيم والمتجهات الذاتية]]
- [[applied-linear-algebra-ar/applied-linear-algebra-projection|الإسقاط على اتجاه]]
- [[applied-linear-algebra-ar/applied-linear-algebra-project|مشروع: حوّل شكلًا باستخدام NumPy]]

## كورسات مرتبطة

- [[linear-algebra-ar/linear-algebra-multiply|ضرب المصفوفات]]
- [[numpy-ar/np-arrays|إنشاء المصفوفات في NumPy]]
