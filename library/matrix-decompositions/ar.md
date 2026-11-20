# @lesson matrix-decompositions-least-squares
title: المربعات الصغرى بالمصفوفات
summary: في النموذج `Ax≈b`، حل المربعات الصغرى يقلّل معيار الباقي المربّع.
---
في النموذج `Ax≈b`، حل المربعات الصغرى يقلّل معيار الباقي المربّع. لمواءمة خط، ضع عمودًا للمدخل وعمودًا من الواحدات للمقطع في A. يتحقق عند الحل أن الباقي متعامد على أعمدة A، وهو اللي نختبره في المثال.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر إحدى القيم.

```try python
import numpy as np

inputs = np.array([0, 1, 2])
observations = np.array([1, 2, 4])
design = np.column_stack((inputs, np.ones(inputs.size)))
coefficients = np.linalg.lstsq(design, observations, rcond=None)[0]
residual = observations - design @ coefficients
print(np.round(coefficients, 3).tolist())
print(bool(np.allclose(design.T @ residual, 0)))
```

```exercise
? كم عمودًا في مصفوفة تصميم الخط في المثال؟
___
= 2
```

```quiz
? مع ماذا يكون الباقي متعامدًا؟
* أعمدة مصفوفة التصميم
- كل قيمة مشاهدة
- محور x فقط
> لو للباقي مركبة في فضاء الأعمدة، يمكن تغيير التوقع داخل الفضاء لتقليل الخطأ.
```

# @lesson matrix-decompositions-svd
title: تحليل القيم المفردة
summary: تحليل `A=UΣVᵀ` يفكّك المصفوفة حتى لو غير مربعة.
---
تحليل `A=UΣVᵀ` يفكّك المصفوفة حتى لو غير مربعة. القيم المفردة غير سالبة وتعبّر عن مقدار التمديد في الاتجاهات المقابلة. عند الاحتفاظ بأكبر قيمة ومُتجهيها فقط، نحصل على تقريب من الرتبة الأولى.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر إحدى القيم.

```try python
import numpy as np

matrix = np.array([[4, 0, 0], [0, 2, 0]])
left, singular, right = np.linalg.svd(matrix, full_matrices=False)
approximation = singular[0] * np.outer(left[:, 0], right[0])
print(singular.tolist())
print(approximation.tolist())
print(float(np.linalg.norm(matrix - approximation)))
```

```exercise
? ما أكبر قيمة مفردة في المثال؟
___
= 4
```

```quiz
? كم رتبة التقريب الناتج عن الاحتفاظ بزوج واحد من المتجهات مع قيمة موجبة؟
- 2
* 1
- 3
> ناتج الضرب الخارجي لمتجهين غير صفريين رتبته واحدة.
```

# @lesson matrix-decompositions-pca
title: مشروع: اختصر ميزتين إلى مركبة واحدة
summary: في PCA نطرح متوسط كل ميزة، ثم نبحث عن الاتجاه اللي يحتفظ بأكبر قدر من التباين.
---
في PCA نطرح متوسط كل ميزة، ثم نبحث عن الاتجاه اللي يحتفظ بأكبر قدر من التباين. اتجاه المركبة الأولى هو أول متجه مفرد أيمن للبيانات المتمركزة. في المثال تسير الميزتان على خط واحد، فتستوعب مركبة واحدة كل التباين. جرّب تغيير نقطة، وشوف كيف تصبح إعادة البناء تقريبية.

## جرّب بنفسك

توقّع النتيجة، ثم شغّل المثال وغيّر إحدى القيم.

```try python
import numpy as np

data = np.array([[0, 0], [1, 2], [2, 4]])
centre = data.mean(axis=0)
centred = data - centre
_, singular, right = np.linalg.svd(centred, full_matrices=False)
direction = right[0]
scores = centred @ direction
restored = np.outer(scores, direction) + centre
fraction = singular[0] ** 2 / sum(singular ** 2)
print(round(float(fraction), 4), bool(np.allclose(restored, data)))
```

```exercise
? كم مركبة احتفظ بها المثال بعد تقليل الأبعاد؟
___
= 1
```

```quiz
? ليه بنطرح متوسط كل ميزة قبل التحليل؟
- عشان كل القيم تبقى صفرًا
- عشان عدد المشاهدات يزيد
* عشان نحلّل التغيّر حول المركز
> المركبات تصف اتجاهات التغيّر ابتداءً من متوسط البيانات.
```

# @lesson matrix-decompositions-reference
title: دليل المربعات الصغرى وSVD وPCA
summary: راجع الأمثلة والأساس المطلوب قبل التطبيق.
type: Reference
---
- [[matrix-decompositions-ar/matrix-decompositions-least-squares|المربعات الصغرى بالمصفوفات]]
- [[matrix-decompositions-ar/matrix-decompositions-svd|تحليل القيم المفردة]]
- [[matrix-decompositions-ar/matrix-decompositions-pca|مشروع: اختصر ميزتين إلى مركبة واحدة]]

راجع [[applied-linear-algebra-ar/applied-linear-algebra-projection|الدرس الأساسي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
