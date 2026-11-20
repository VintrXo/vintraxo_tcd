# @lesson partial-differential-equations-partials
title: المتغيرات والمشتقات في معادلة الحرارة
summary: في المعادلة `uₜ=κuₓₓ` تعتمد الحرارة على المكان والزمن.
---
في المعادلة `uₜ=κuₓₓ` تعتمد الحرارة على المكان والزمن. المشتقة الزمنية تصف تغيّر الحرارة عند نقطة، والثانية المكانية تصف انحناء توزيعها. الدالة `u=x²+2κt` تحقق المعادلة لأن مشتقتها الثانية المكانية 2.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
kappa = 3
u_t = 2 * kappa
u_xx = 2
print(u_t, kappa * u_xx, u_t == kappa * u_xx)
```

```exercise
? ما uₓₓ للدالة x²+6t؟
___
= 2
```

```quiz
? أي مشتقة تصف تغيّر الحرارة مع الزمن عند مكان ثابت؟
* uₜ
- uₓₓ
- uₓ
> في uₜ نغيّر الزمن ونثبّت المكان.
```

# @lesson partial-differential-equations-boundary
title: الشروط الابتدائية والحدّية
summary: التوزيع الابتدائي يحدد الحرارة عند t=0.
---
التوزيع الابتدائي يحدد الحرارة عند t=0. الشرط الحدّي يحدد سلوك الأطراف لزمن لاحق. في شبكة لقضيب، نثبّت الطرفين عند الصفر ونحدّث النقاط الداخلية باستخدام الفرق الثاني للجيران.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
old = [0, 0, 80, 0, 0]
new = old.copy()
for i in range(1, len(old) - 1):
    new[i] += 0.25 * (old[i - 1] - 2 * old[i] + old[i + 1])
print(new)
```

```exercise
? ما حرارة المركز بعد الخطوة في المثال؟
___
= 40
```

```quiz
? أي قيم لا نحدّثها هنا؟
- المركز
* الطرفان
- كل النقاط الداخلية
> الشرط الحدّي يفرض الصفر عند طرفي القضيب.
```

# @lesson partial-differential-equations-stability
title: مشروع: افحص خطوة الانتشار
summary: في المخطط الصريح، معامل الانتشار للشبكة `r=κΔt/Δx²`.
---
في المخطط الصريح، معامل الانتشار للشبكة `r=κΔt/Δx²`. التحديث يزن الجارين بـr والمركز بـ`1−2r`. مع `0≤r≤1/2` تكون الأوزان غير سالبة ومجموعها واحد. جرّب خطوة أكبر لتشوف كيف تظهر قيمة سالبة في مثال الحرارة.

## جرّب بنفسك

توقّع الناتج، ثم شغّل المثال وغيّر إحدى القيم لاختبار الفكرة.

```try python
left, centre, right = 0, 80, 0
for ratio in (0.25, 0.75):
    updated = ratio * left + (1 - 2 * ratio) * centre + ratio * right
    print(ratio, updated)
```

```exercise
? ما وزن المركز عندما r=0.25؟ اكتب الناتج عشريًا.
___
= 0.5
```

```quiz
? لو ثبتنا κ وΔx وزوّدنا Δt، ماذا يحدث لـr؟
- يقل
- يبقى ثابتًا
* يزيد
> Δt في بسط تعريف r.
```

# @lesson partial-differential-equations-reference
title: دليل المعادلات التفاضلية الجزئية
summary: راجع الأمثلة وارجع للدرس التمهيدي.
type: Reference
---
- [[partial-differential-equations-ar/partial-differential-equations-partials|المتغيرات والمشتقات في معادلة الحرارة]]
- [[partial-differential-equations-ar/partial-differential-equations-boundary|الشروط الابتدائية والحدّية]]
- [[partial-differential-equations-ar/partial-differential-equations-stability|مشروع: افحص خطوة الانتشار]]

راجع [[advanced-math-ar/advanced-math-heat|الدرس التمهيدي]] أو ارجع إلى [[math-branches-ar/math-branches-map|خريطة الرياضيات]].
