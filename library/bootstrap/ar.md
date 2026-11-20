# @lesson bs-intro
title: مقدمة في Bootstrap
summary: ما هي Bootstrap وكيف تضيفها لصفحتك.
---
**Bootstrap** مكتبة CSS وJavaScript مجانية تعطيك مكونات جاهزة (أزرار، بطاقات، قوائم، نماذج…) وشبكة متجاوبة، فتبني صفحة أنيقة تعمل على الجوال والكمبيوتر بسرعة.

## إضافتها لصفحتك

ضع هذين السطرين في صفحتك (في هذه الدورة يُضافان تلقائيًا لكل مثال):

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

:::info الصفحات العربية
للصفحات من اليمين لليسار استخدم الملف `bootstrap.rtl.min.css` مع `<html lang="ar" dir="rtl">`؛ أمثلة هذه الدورة تستخدمه.
:::

## أول مثال

```try html bs
<div class="container">
  <h1 class="text-primary">مرحبًا Bootstrap</h1>
  <p class="lead">فقرة بخط أكبر قليلًا.</p>
  <button class="btn btn-success">زر جاهز</button>
</div>
```

كل التنسيق جاء من **أصناف** جاهزة مثل `text-primary` و `btn btn-success`، دون كتابة CSS.

```quiz
? كيف تستخدم مكونات Bootstrap غالبًا؟
* بإضافة أصناف class جاهزة للعناصر
- بكتابة JavaScript لكل عنصر
- بتغيير أسماء الوسوم

? توفّر Bootstrap ملفًا خاصًا للصفحات من اليمين لليسار.
= true
```

# @lesson bs-containers
title: الحاويات
summary: container و container-fluid والحاويات المتجاوبة.
---
كل تخطيط في Bootstrap يبدأ بـ **حاوية**:

```reference html
.container | عرض أقصى ثابت يتغير مع حجم الشاشة، وفي المنتصف | <div class="container">…</div>
.container-fluid | العرض كاملًا دائمًا | <div class="container-fluid">…</div>
.container-md | كامل حتى الشاشة المتوسطة ثم ثابت | <div class="container-md">…</div>
```

```try html bs
<div class="container bg-light border p-3 mb-2">container: عرض محدود في المنتصف</div>
<div class="container-fluid bg-info-subtle border p-3">container-fluid: العرض كله</div>
```

:::tip جرّب ملء الشاشة
اضغط **ملء الشاشة** وغيّر عرض النافذة لترى الحاوية تتغير.
:::

```quiz
? أي حاوية تأخذ عرض الشاشة كله دائمًا؟
- .container
* .container-fluid
- .container-sm

? الحاوية .container تضع المحتوى في منتصف الصفحة بعرض محدود.
= true
```

# @lesson bs-grid
title: نظام الشبكة
summary: الصفوف والأعمدة الـ 12، والأحجام المتجاوبة.
---
الشبكة تقسّم السطر إلى **12 عمودًا**. ضع `row` ثم أعمدة `col`:

```try html bs
<div class="container text-center">
  <div class="row g-2">
    <div class="col"><div class="p-3 bg-primary-subtle">عمود</div></div>
    <div class="col"><div class="p-3 bg-primary-subtle">عمود</div></div>
    <div class="col"><div class="p-3 bg-primary-subtle">عمود</div></div>
  </div>
</div>
```

## أحجام محددة

`col-8` و `col-4` يأخذان 8 و4 من 12:

```try html bs
<div class="container">
  <div class="row g-2">
    <div class="col-8"><div class="p-3 bg-success-subtle">رئيسي (8)</div></div>
    <div class="col-4"><div class="p-3 bg-warning-subtle">جانبي (4)</div></div>
  </div>
</div>
```

## متجاوبة

`col-12 col-md-6 col-lg-4`: عمود كامل على الجوال، نصف على الشاشة المتوسطة، ثلث على الكبيرة:

```try html bs
<div class="container">
  <div class="row g-2">
    <div class="col-12 col-md-6 col-lg-4"><div class="p-3 border">١</div></div>
    <div class="col-12 col-md-6 col-lg-4"><div class="p-3 border">٢</div></div>
    <div class="col-12 col-md-6 col-lg-4"><div class="p-3 border">٣</div></div>
  </div>
</div>
```

```reference html
xs (بلا اسم) | أقل من 576px | col-12
sm | 576px فأكثر | col-sm-6
md | 768px فأكثر | col-md-4
lg | 992px فأكثر | col-lg-3
xl | 1200px فأكثر | col-xl-2
```

```exercise html
? اجعل العمود نصف الصف على الشاشات المتوسطة فأكبر
<div class="col-12 col-___-6">…</div>
= md
```

```quiz
? كم عمودًا في صف Bootstrap؟
- 10
* 12
- 16

? الصنف g-2 يضيف مسافة بين الأعمدة.
= true
```

# @lesson bs-typography-colors
title: النصوص والألوان
summary: أصناف النصوص، والألوان، والخلفيات.
---
```try html bs
<h1 class="display-5">عنوان كبير</h1>
<p class="lead">فقرة تمهيدية.</p>
<p class="text-muted">نص خافت</p>
<p class="fw-bold text-center">عريض في المنتصف</p>
<p class="text-danger">خطأ</p> <p class="text-success">نجاح</p>
<div class="p-2 bg-dark text-white">خلفية داكنة</div>
<div class="p-2 bg-warning-subtle mt-2">خلفية ناعمة</div>
```

## الألوان الأساسية

`primary` و `secondary` و `success` و `danger` و `warning` و `info` و `light` و `dark`. استخدمها مع `text-` و `bg-` و `btn-` و `border-`.

```reference html
text-{لون} | لون النص | text-primary
bg-{لون} | لون الخلفية | bg-success
bg-{لون}-subtle | خلفية ناعمة | bg-info-subtle
fw-bold / fw-light | سماكة الخط | fw-bold
fs-1 … fs-6 | حجم الخط | fs-4
text-center / text-end | المحاذاة | text-center
display-1 … display-6 | عناوين كبيرة | display-4
lead | فقرة بارزة | lead
```

```quiz
? أي صنف يجعل النص أحمر يدل على خطأ؟
* text-danger
- text-error
- text-red

? الصنف bg-success-subtle يعطي خلفية خضراء ناعمة.
= true
```

# @lesson bs-utilities
title: أصناف المسافات والعرض
summary: m و p للمسافات، و d-flex، و border و rounded و shadow.
---
## المسافات

`m` للهامش و `p` للحشوة، ثم الجهة ثم الحجم من 0 إلى 5:

```reference html
m-3 / p-3 | كل الجهات | p-3
mt / mb | أعلى / أسفل | mb-4
ms / me | البداية / النهاية (حسب الاتجاه) | ms-2
mx / my | أفقي / عمودي | mx-auto
gap-3 | مسافة بين العناصر | d-flex gap-3
```

```try html bs
<div class="d-flex gap-2 p-3 bg-light">
  <div class="p-3 bg-white border rounded">أ</div>
  <div class="p-3 bg-white border rounded shadow-sm">ب</div>
  <div class="p-3 bg-white border rounded-pill shadow">ج</div>
</div>
<div class="d-flex justify-content-between align-items-center mt-3 p-2 border">
  <span>يمين</span><span>منتصف</span><span>يسار</span>
</div>
```

## العرض والإخفاء

```try html bs
<p class="d-none d-md-block bg-info-subtle p-2">أظهر فقط على الشاشات المتوسطة فأكبر</p>
<p class="d-md-none bg-warning-subtle p-2">أظهر فقط على الجوال</p>
```

```exercise html
? أضف حشوة بحجم 3 لكل الجهات
<div class="___-3">…</div>
= p
```

```quiz
? ما معنى الصنف mb-4؟
* هامش سفلي بحجم 4
- حشوة سفلية بحجم 4
- عرض 4 أعمدة

? الصنف ms-2 يضيف هامشًا في بداية العنصر حسب اتجاه الصفحة.
= true
```

# @lesson bs-tables-images
title: الجداول والصور
summary: table و table-striped، والصور المتجاوبة.
---
```try html bs
<table class="table table-striped table-hover">
  <thead class="table-dark">
    <tr><th>المنتج</th><th>السعر</th></tr>
  </thead>
  <tbody>
    <tr><td>قلم</td><td>5</td></tr>
    <tr><td>دفتر</td><td>12</td></tr>
    <tr class="table-success"><td>حقيبة</td><td>90</td></tr>
  </tbody>
</table>
```

```reference html
table | جدول بتنسيق Bootstrap | <table class="table">
table-striped | صفوف مخططة | table table-striped
table-hover | تمييز الصف عند المرور | table table-hover
table-bordered | حدود لكل الخلايا | table table-bordered
table-responsive | تمرير أفقي على الشاشات الصغيرة | <div class="table-responsive">
```

## الصور

```try html bs
<img src="https://picsum.photos/600/300" class="img-fluid rounded" alt="منظر">
<img src="https://picsum.photos/120" class="rounded-circle mt-2" alt="صورة شخصية" width="80">
```

`img-fluid` تجعل الصورة لا تتجاوز عرض حاويتها.

```quiz
? أي صنف يجعل الصورة متجاوبة؟
* img-fluid
- img-responsive-x
- img-auto

? الصنف table-striped يلوّن الصفوف بالتناوب.
= true
```

# @lesson bs-buttons
title: الأزرار
summary: ألوان الأزرار وأحجامها والأزرار المحددة ومجموعاتها.
---
```try html bs
<button class="btn btn-primary">أساسي</button>
<button class="btn btn-success">نجاح</button>
<button class="btn btn-outline-danger">حذف</button>
<button class="btn btn-secondary" disabled>معطّل</button>
<hr>
<button class="btn btn-primary btn-lg">كبير</button>
<button class="btn btn-primary btn-sm">صغير</button>
<a href="#" class="btn btn-link">زر كرابط</a>
<hr>
<div class="btn-group">
  <button class="btn btn-outline-primary">يوم</button>
  <button class="btn btn-outline-primary active">أسبوع</button>
  <button class="btn btn-outline-primary">شهر</button>
</div>
```

```reference html
btn btn-{لون} | زر ملوّن | btn btn-primary
btn-outline-{لون} | زر بإطار فقط | btn btn-outline-success
btn-lg / btn-sm | الحجم | btn btn-primary btn-lg
w-100 | بعرض كامل | btn btn-primary w-100
btn-group | مجموعة أزرار | <div class="btn-group">
```

```exercise html
? اجعل الزر أحمر بإطار فقط
<button class="btn btn-___-danger">حذف</button>
= outline
```

```quiz
? أي صنف ينشئ زرًا كبيرًا؟
- btn-big
* btn-lg
- btn-xl

? يمكن استخدام الأصناف btn على عنصر a أيضًا.
= true
```

# @lesson bs-cards
title: البطاقات
summary: البطاقة بصورتها وعنوانها ونصها، وشبكة بطاقات.
---
```try html bs
<div class="card" style="max-width: 18rem;">
  <img src="https://picsum.photos/400/220" class="card-img-top" alt="صورة المنتج">
  <div class="card-body">
    <h5 class="card-title">سماعات لاسلكية</h5>
    <p class="card-text">صوت نقي وبطارية تدوم 30 ساعة.</p>
    <a href="#" class="btn btn-primary">اشترِ الآن</a>
  </div>
</div>
```

## شبكة بطاقات

```try html bs
<div class="row row-cols-1 row-cols-md-3 g-3">
  <div class="col"><div class="card h-100"><div class="card-body"><h5 class="card-title">أساسي</h5><p class="card-text">50 ريال</p></div></div></div>
  <div class="col"><div class="card h-100 border-primary"><div class="card-body"><h5 class="card-title text-primary">احترافي</h5><p class="card-text">120 ريال</p></div></div></div>
  <div class="col"><div class="card h-100"><div class="card-body"><h5 class="card-title">مؤسسات</h5><p class="card-text">تواصل معنا</p></div></div></div>
</div>
```

`h-100` يجعل البطاقات بنفس الارتفاع، و `row-cols-md-3` ثلاث بطاقات في الصف من الشاشة المتوسطة.

```quiz
? أي صنف يحتوي محتوى البطاقة الأساسي؟
* card-body
- card-content
- card-inner

? الصنف h-100 يجعل البطاقات في الصف بنفس الارتفاع.
= true
```

# @lesson bs-alerts-badges
title: التنبيهات والشارات والتقدم
summary: alert و badge و progress و spinner.
---
```try html bs
<div class="alert alert-success">تم حفظ التغييرات.</div>
<div class="alert alert-warning alert-dismissible fade show">
  تنبيه: البطارية منخفضة.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="إغلاق"></button>
</div>
<h5>الرسائل <span class="badge bg-danger">4</span></h5>
<span class="badge rounded-pill text-bg-info">جديد</span>
<div class="progress my-3" role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 65%">65%</div>
</div>
<div class="spinner-border text-primary" role="status"><span class="visually-hidden">جارٍ التحميل…</span></div>
```

:::tip الأزرار القابلة للإغلاق
`data-bs-dismiss="alert"` يكفي لإغلاق التنبيه؛ ملف JavaScript في Bootstrap يتولى الباقي.
:::

```quiz
? أي صنف ينشئ رقمًا صغيرًا ملونًا بجانب النص؟
- alert
* badge
- chip

? السمة data-bs-dismiss="alert" تجعل الزر يغلق التنبيه.
= true
```

# @lesson bs-forms
title: النماذج
summary: form-control و form-label و form-check والتحقق.
---
```try html bs
<form class="needs-validation" novalidate style="max-width: 420px">
  <div class="mb-3">
    <label for="email" class="form-label">البريد الإلكتروني</label>
    <input type="email" class="form-control" id="email" required>
    <div class="invalid-feedback">اكتب بريدًا صحيحًا.</div>
  </div>
  <div class="mb-3">
    <label for="city" class="form-label">المدينة</label>
    <select id="city" class="form-select"><option>الرياض</option><option>القاهرة</option></select>
  </div>
  <div class="form-check mb-3">
    <input class="form-check-input" type="checkbox" id="agree" required>
    <label class="form-check-label" for="agree">أوافق على الشروط</label>
  </div>
  <button class="btn btn-primary w-100">تسجيل</button>
</form>
<script>
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    e.target.classList.add("was-validated");
  });
</script>
```

```reference html
form-label | تسمية الحقل | <label class="form-label">
form-control | حقل نص | <input class="form-control">
form-select | قائمة منسدلة | <select class="form-select">
form-check | خانة اختيار مع تسميتها | <div class="form-check">
input-group | حقل مع إضافة | <div class="input-group">
invalid-feedback | رسالة خطأ | <div class="invalid-feedback">
was-validated | إظهار نتائج التحقق | form.classList.add("was-validated")
```

```exercise html
? أكمل الصنف الذي ينسق حقل النص
<input type="text" class="form-___">
= control
```

```quiz
? أي صنف ينسق القائمة المنسدلة؟
* form-select
- form-control-list
- dropdown-input

? الصنف was-validated يظهر رسائل التحقق في النموذج.
= true
```

# @lesson bs-navbar
title: شريط التنقل
summary: navbar متجاوب يطوى في زر على الجوال.
---
```try html bs
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">متجري</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="القائمة">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="nav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link active" href="#">الرئيسية</a></li>
        <li class="nav-item"><a class="nav-link" href="#">المنتجات</a></li>
        <li class="nav-item"><a class="nav-link" href="#">تواصل</a></li>
      </ul>
    </div>
  </div>
</nav>
```

- `navbar-expand-lg`: يظهر كاملًا على الشاشات الكبيرة، ويطوى في زر على الأصغر.
- زر `navbar-toggler` يفتح القائمة المطوية عبر `data-bs-target`.

:::tip جرّبه مطويًا
اضغط **ملء الشاشة** وصغّر النافذة؛ ستظهر أيقونة القائمة.
:::

```quiz
? ما الذي يجعل شريط التنقل يطوى على الشاشات الصغيرة؟
* navbar-expand-lg مع navbar-collapse
- navbar-small
- d-none

? السمة data-bs-target تحدد العنصر الذي يفتحه الزر.
= true
```

# @lesson bs-modal
title: النافذة المنبثقة
summary: modal تفتح بزر دون كتابة JavaScript.
---
```try html bs
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#confirm">احذف الحساب</button>

<div class="modal fade" id="confirm" tabindex="-1" aria-labelledby="confirmTitle" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="confirmTitle">تأكيد</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="إغلاق"></button>
      </div>
      <div class="modal-body">هل أنت متأكد؟ لا يمكن التراجع.</div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
        <button class="btn btn-danger">احذف</button>
      </div>
    </div>
  </div>
</div>
```

## مكونات تفاعلية أخرى بنفس الطريقة

```reference html
modal | نافذة منبثقة | data-bs-toggle="modal"
collapse | إظهار وإخفاء محتوى | data-bs-toggle="collapse"
dropdown | قائمة منسدلة | data-bs-toggle="dropdown"
tooltip | تلميح عند المرور | data-bs-toggle="tooltip"
offcanvas | قائمة جانبية منزلقة | data-bs-toggle="offcanvas"
carousel | عرض شرائح | <div class="carousel slide">
accordion | أقسام قابلة للطي | <div class="accordion">
```

```quiz
? أي سمة تفتح النافذة المنبثقة عند الضغط على الزر؟
* data-bs-toggle="modal"
- onclick="modal()"
- href="#modal"

? المكونات التفاعلية في Bootstrap تحتاج ملف bootstrap.bundle.js.
= true
```

# @lesson bs-reference
title: مرجع Bootstrap
summary: أهم الأصناف مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي صنف.

```reference html
container / container-fluid | الحاويات | <div class="container">
row / col | الشبكة | <div class="row"><div class="col-md-6">
g-{0-5} | المسافة بين الأعمدة | row g-3
m- / p- | الهوامش والحشوة | mt-3 p-2
d-flex / d-none / d-md-block | العرض | d-flex gap-2
justify-content-* | توزيع أفقي | justify-content-between
align-items-* | محاذاة عمودية | align-items-center
text-* / bg-* | الألوان | text-primary bg-light
fw-bold / fs-* | الخط | fw-bold fs-5
border / rounded / shadow | الإطار والزوايا والظل | border rounded shadow-sm
btn btn-* | الأزرار | btn btn-success
card / card-body | البطاقات | <div class="card">
alert alert-* | التنبيهات | alert alert-warning
badge | الشارات | badge text-bg-danger
table table-* | الجداول | table table-striped
img-fluid | صورة متجاوبة | <img class="img-fluid">
form-control / form-select | النماذج | <input class="form-control">
navbar | شريط التنقل | navbar navbar-expand-lg
modal | نافذة منبثقة | data-bs-toggle="modal"
visually-hidden | نص لقارئ الشاشة فقط | <span class="visually-hidden">
```

:::tip ماذا بعد؟
ابنِ صفحة هبوط كاملة: شريط تنقل، قسم ترحيب، ثلاث بطاقات، ونموذج تواصل. ثم جرّب دورة **React** لبناء واجهات تفاعلية.
:::
