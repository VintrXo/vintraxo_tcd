# @lesson category-theory-composition
title: الكائنات والأسهم والتركيب
summary: في فئة المجموعات، السهم دالة من مجموعة إلى أخرى.
---
في فئة المجموعات، السهم دالة من مجموعة إلى أخرى. نركّب `g∘f` إذا كان هدف f هو مصدر g، ونطبّق f أولًا. سهم الهوية يحافظ على كل عنصر. التركيب في أي فئة تجميعي.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
def f(x):
    return x + 1

def g(x):
    return 2 * x

print(g(f(3)), f(g(3)))
```

```exercise
? ما قيمة g(f(4)) في المثال؟
___
= 10
```

```quiz
? في g∘f، أي دالة نطبّقها أولًا؟
* f
- g
- دالة الهوية
> ناتج f يدخل إلى g.
```

# @lesson category-theory-isomorphism
title: التشاكل والأسهم العكسية
summary: السهم تشاكل إذا كان له معكوس في الاتجاهين، بحيث يعطي كل تركيب سهم الهوية على طرفه.
---
السهم تشاكل إذا كان له معكوس في الاتجاهين، بحيث يعطي كل تركيب سهم الهوية على طرفه. في فئة المجموعات، الدالة التقابلية تشاكل ومعكوسها دالة. الدالة التي ترسل عنصرين لنفس الناتج لا يمكن عكسها لاسترجاع الاثنين.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
forward = {'a': 1, 'b': 2}
backward = {value: key for key, value in forward.items()}
print(backward[forward['b']])
print(forward[backward[1]])
```

```exercise
? إذا كان f(a)=1 وf(b)=2، فما ناتج المعكوس عند 2؟ اكتب a أو b.
___
= b
```

```quiz
? ما ناتج تركيب السهم ومعكوسه بالترتيب الموافق؟
- أي سهم جديد
* سهم الهوية
- سهم ثابت دائمًا
> وجود هويتين من التركيب في الاتجاهين جزء من تعريف التشاكل.
```

# @lesson category-theory-functor
title: مشروع: مؤثر يحفظ التركيب
summary: المؤثر الفئوي ينقل الكائنات والأسهم ويحفظ الهوية والتركيب.
---
المؤثر الفئوي ينقل الكائنات والأسهم ويحفظ الهوية والتركيب. مؤثر مجموعة الأجزاء ينقل كل مجموعة إلى مجموعة أجزائها، وينقل كل دالة إلى عملية أخذ صورة مجموعة جزئية. صورة جزء تحت `g∘f` تساوي صورة صورته تحت f ثم g.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
def image(function, subset):
    return {function(value) for value in subset}

subset = {1, 2}
f = lambda x: x + 1
g = lambda x: 2 * x
separate = image(g, image(f, subset))
composed = image(lambda x: g(f(x)), subset)
print(sorted(separate), separate == composed)
```

```exercise
? كم عنصرًا في صورة {1,2} تحت x ↦ 2x؟
___
= 2
```

```quiz
? ما الخاصيتان اللتان يحفظهما المؤثر الفئوي؟
- الترتيب العددي دائمًا
- كل حجم مجموعة
* الهوية والتركيب
> المؤثر يرسل الهوية لهوية، وتركيب سهمين لتركيب صورتيهما.
```

# @lesson category-theory-reference
title: دليل مدخل إلى نظرية الفئات
summary: راجع الأمثلة وارجع للدرس التمهيدي.
type: Reference
---
- [[category-theory-ar/category-theory-composition|الكائنات والأسهم والتركيب]]
- [[category-theory-ar/category-theory-isomorphism|التشاكل والأسهم العكسية]]
- [[category-theory-ar/category-theory-functor|مشروع: مؤثر يحفظ التركيب]]

راجع [[advanced-math-ar/advanced-math-categories|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
