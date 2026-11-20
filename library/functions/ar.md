# @lesson functions-rule
title: مدخلات الدالة ومخرجاتها
summary: الدالة تعطي لكل مدخل مسموح مخرجًا واحدًا.
---
الدالة تعطي لكل مدخل مسموح مخرجًا واحدًا. في `f(x) = 2x + 1` يقابل المدخل 3 المخرج 7. ممكن لمدخلين مختلفين أن يشتركا في نفس المخرج.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر قيمة وجرب من جديد.

```try python
def f(x):
    return 2 * x + 1

for x in (-1, 0, 3):
    print(x, f(x))
```

```exercise
? احسب f(4) إذا كانت f(x) = 2x + 1.
___
= 9
```

```quiz
? إذا أعطى المدخل نفسه مخرجين مختلفين، هل العلاقة دالة؟
- نعم
* لا
- فقط إذا كان الناتجان موجبين
> يشترط أن يقابل المدخل الواحد مخرج واحد.
```

# @lesson functions-points
title: الإحداثيات وجدول القيم
summary: النقطة `(x, y)` تتحرك أفقيًا حسب `x` ورأسيًا حسب `y`.
---
النقطة `(x, y)` تتحرك أفقيًا حسب `x` ورأسيًا حسب `y`. نحسب قيمة الدالة لكل مدخل ثم نرسم الزوج الناتج. للقاعدة `y = x + 2` تقع النقطة `(1, 3)` على الرسم.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر قيمة وجرب من جديد.

```try python
for x in range(-2, 3):
    print((x, x + 2))
```

```exercise
? ما الإحداثي الرأسي عند x = −1 على y = x + 2؟
___
= 1
```

```quiz
? أي نقطة تقع على الرسم y = 2x − 1؟
- (3, 2)
- (0, 1)
* (2, 3)
> عند x = 2 نجد y = 2 × 2 − 1 = 3.
```

# @lesson functions-slope
title: الميل والمقطع
summary: في `y = mx + b` يحدد `m` مقدار تغيّر `y` مع زيادة `x` بوحدة، ويحدد `b` قيمة `y` عند `x = 0`.
---
في `y = mx + b` يحدد `m` مقدار تغيّر `y` مع زيادة `x` بوحدة، ويحدد `b` قيمة `y` عند `x = 0`. غيّر الميل في الرسم ولاحظ اتجاه الخط.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر قيمة وجرب من جديد.

```try python
m = -2
b = 3
print(b)
print((m * 2 + b) - (m * 1 + b))
```

```try html
<html lang="ar" dir="rtl">
<label>الميل <input id="slope" type="range" min="-3" max="3" value="1" step="0.5"></label>
<output id="equation" dir="ltr"></output>
<canvas id="graph" width="360" height="220" style="display:block;max-width:100%;background:#f1f5f9" aria-label="رسم الدالة الخطية"></canvas>
<script>
const slope = document.querySelector('#slope');
const canvas = document.querySelector('#graph');
const ctx = canvas.getContext('2d');
function draw() {
  const m = Number(slope.value);
  document.querySelector('#equation').textContent = 'y = ' + m + 'x + 1';
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(0, 110);
  ctx.lineTo(360, 110);
  ctx.moveTo(180, 0);
  ctx.lineTo(180, 220);
  ctx.stroke();
  ctx.strokeStyle = '#2563eb';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(0, 110 - 20 * (m * -9 + 1));
  ctx.lineTo(360, 110 - 20 * (m * 9 + 1));
  ctx.stroke();
  ctx.fillStyle = '#2563eb';
  ctx.beginPath();
  ctx.arc(180, 90, 4, 0, Math.PI * 2);
  ctx.fill();
}
slope.addEventListener('input', draw);
draw();
</script>
</html>
```

```exercise
? اكتب قيمة المقطع الرأسي في y = 5x − 4.
___
= -4
```

```quiz
? احسب الميل بين النقطتين (1, 2) و(3, 8).
* 3
- 6
- 2
> التغير الرأسي 6 والأفقي 2. الميل هو 6 ÷ 2.
```

# @lesson functions-domain
title: المجال والقيود
summary: المجال هو المدخلات المسموح بها.
---
المجال هو المدخلات المسموح بها. لا نستخدم الصفر في مقام `1/x`. في نموذج يصف عدد الكتب، المدخلات المسموحة أعداد صحيحة غير سالبة لأن العدد يمثل كمية فعلية.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر قيمة وجرب من جديد.

```try python
for x in (-2, -1, 0, 1, 2):
    if x == 0:
        print(x, 'undefined')
    else:
        print(x, 1 / x)
```

```exercise
? ما القيمة الممنوعة في الدالة 1/(x − 3)؟
___
= 3
```

```quiz
? أي مدخل غير مناسب لدالة تحسب تكلفة عدد من الكتب؟
- 0
* 2.5
- 3
> عدد الكتب كمية صحيحة، و2.5 ليس عددًا صحيحًا.
```

# @lesson functions-quadratic
title: الدوال التربيعية
summary: رسم `y = x²` منحنى وليس خطًا مستقيمًا.
---
رسم `y = x²` منحنى وليس خطًا مستقيمًا. يعطي العدد ومقابله السالب الناتج نفسه، ولذلك يكون الرسم متماثلًا حول المحور الرأسي.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر قيمة وجرب من جديد.

```try python
for x in range(-3, 4):
    print(x, x ** 2)
```

```exercise
? أوجد y عند x = −4 في y = x².
___
= 16
```

```quiz
? ما أقل قيمة للدالة y = x² + 2؟
- 0
- -2
* 2
> مربع أي عدد حقيقي غير سالب ويصل للصفر عند x = 0.
```

# @lesson functions-plans
title: مشروع: قارن خطط اشتراك
summary: الخطة الأولى تكلف 20 ثابتة و5 لكل استخدام، والثانية تكلف 8 لكل استخدام بلا رسوم ثابتة.
---
الخطة الأولى تكلف 20 ثابتة و5 لكل استخدام، والثانية تكلف 8 لكل استخدام بلا رسوم ثابتة. اكتب الدالتين وجرّب أعداد استخدام مختلفة لتحدد أول عدد صحيح تصبح عنده الخطة الأولى أرخص.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر قيمة وجرب من جديد.

```try python
def plan_a(uses):
    return 20 + 5 * uses

def plan_b(uses):
    return 8 * uses

for uses in range(5, 9):
    print(uses, plan_a(uses), plan_b(uses))
```

```exercise
? ما تكلفة الخطة الأولى عند 6 استخدامات؟
___
= 50
```

```quiz
? ما أول عدد صحيح تصبح عنده الخطة الأولى أرخص؟
* 7
- 6
- 8
> عند 6 استخدامات التكلفتان 50 و48. عند 7 تصبحان 55 و56.
```

# @lesson functions-reference
title: مرجع الدوال والرسوم
summary: القواعد الأساسية مع أمثلة سريعة.
type: Reference
---
```reference
الدالة | لكل مدخل مسموح مخرج واحد | f(3) = 7 إذا كانت f(x) = 2x + 1
الميل | التغير الرأسي مقسومًا على التغير الأفقي | 6 ÷ 2 = 3
المقطع الرأسي | قيمة y عند x = 0 | في y = 2x + 1 المقطع 1
```
