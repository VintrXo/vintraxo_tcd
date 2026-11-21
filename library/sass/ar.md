# @lesson sass-intro
title: مقدمة Sass
summary: ماذا تضيف Sass إلى CSS، وصيغة SCSS، وكيف تُترجم.
---
**Sass** معالج مسبق لـ CSS: تكتب التنسيقات بمتغيرات وتداخل و mixins ودوال وحلقات، ثم يحوّلها مترجم Sass إلى CSS عادية يفهمها المتصفح. Bootstrap وكثير من أنظمة التصميم مكتوبة بـ Sass.

هناك صيغتان، وتستخدم هذه الدورة **SCSS** التي تشبه CSS مع إضافات (أي ملف CSS صحيح هو SCSS صحيح). أما الصيغة القديمة المعتمدة على الإزاحة فتحذف الأقواس والفواصل المنقوطة.

```try html scss
<style type="text/scss">
$brand: #4338ca;
$radius: 10px;

.card {
  padding: 16px;
  border: 2px solid $brand;
  border-radius: $radius;

  h3 { color: $brand; margin: 0 0 8px; }
}
</style>

<div class="card">
  <h3>مرحبًا Sass</h3>
  <p>المتغيرات والتداخل في الأعلى أصبحت CSS عادية.</p>
</div>
```

الصندوق أسفل المثال يعرض **CSS الناتجة** التي يستخدمها المتصفح فعلًا.

:::info الترجمة على جهازك
ثبّتها بـ `npm install -g sass`، ثم `sass styles.scss styles.css`، أو `sass --watch scss:css` لإعادة الترجمة عند كل حفظ. وأطر العمل مثل Vite و Angular و Next.js تترجم ملفات `.scss` تلقائيًا.
:::

```quiz
? ماذا ينتج مترجم Sass؟
* CSS عادية يفهمها المتصفح
- كود JavaScript
- صورًا

? أي ملف CSS صحيح هو أيضًا SCSS صحيح.
= true
```

# @lesson sass-variables
title: المتغيرات
summary: متغيرات $ ونطاقها و !default، ومتغيرات Sass مقابل متغيرات CSS.
---
```try html scss
<style type="text/scss">
$brand: #0e7490;
$space: 8px;
$font-stack: system-ui, "Segoe UI", sans-serif;

body { font-family: $font-stack; }

.alert {
  $alert-bg: #e0f2fe;                  // مرئي داخل .alert فقط
  padding: $space * 2;
  margin-block-end: $space;
  background: $alert-bg;
  border-inline-start: 4px solid $brand;
}

:root {
  --brand: #{$brand};                  // تمرير قيمة Sass إلى متغير CSS
}
.badge { color: var(--brand); font-weight: bold; }
</style>

<div class="alert">تم الحفظ. <span class="badge">جديد</span></div>
<div class="alert">تنبيهان ومجموعة متغيرات واحدة.</div>
```

```reference css
$name: value; | تعريف متغير | $brand: #4338ca;
$a * 2 / $a + 4px | حسابات بالقيم والوحدات | padding: $space * 2;
#{$var} | إدراج القيمة في المحددات أو الخصائص أو متغيرات CSS | --brand: #{$brand};
!default | استخدم هذه القيمة ما لم تُحدد قيمة قبلها | $brand: blue !default;
var(--name) | متغير CSS (يعمل في المتصفح) | color: var(--brand);
```

:::tip متغيرات Sass أم متغيرات CSS؟
متغيرات Sass موجودة فقط أثناء الترجمة: ممتازة لرموز التصميم والحسابات. أما متغيرات CSS فتعيش في المتصفح ويمكن أن تتغير أثناء التشغيل، مثلًا للوضع الداكن. وكثير من المشاريع تعرّف الرموز في Sass وتخرجها كمتغيرات CSS.
:::

```exercise css
? عرّف متغير Sass اسمه gap بالقيمة 12px
___gap: 12px;
= $
```

```quiz
? متى تُحسب متغيرات Sass؟
* عند ترجمة Sass إلى CSS
- في كل مرة تُمرَّر فيها الصفحة
- في الوضع الداكن فقط
```

# @lesson sass-nesting
title: التداخل ومحدد الأب
summary: القواعد المتداخلة، و &، والحالات الزائفة، وتسمية BEM، واستعلامات الوسائط المتداخلة.
---
```try html scss
<style type="text/scss">
$brand: #4338ca;

.nav {
  display: flex;
  gap: 4px;

  a {
    padding: 6px 12px;
    border-radius: 999px;
    color: $brand;
    text-decoration: none;

    &:hover { background: #eef2ff; }          // & = محدد الأب: .nav a:hover
    &.active { background: $brand; color: #fff; }
  }

  &__title {                                  // يبني .nav__title (تسمية BEM)
    font-weight: bold;
    margin-inline-end: 12px;
  }

  @media (max-width: 500px) {                 // استعلام الوسائط بجوار قاعدته
    flex-direction: column;
  }
}
</style>

<nav class="nav">
  <span class="nav__title">القائمة</span>
  <a href="#" class="active">الرئيسية</a>
  <a href="#">الدورات</a>
  <a href="#">ملفي</a>
</nav>
```

```reference css
.a { .b { } } | محدد متداخل | .card { h3 { } } -> .card h3
& | محدد الأب | &:hover, &.active, &__title
&-suffix | بناء اسم صنف | .btn { &-primary { } } -> .btn-primary
@media داخل قاعدة | استعلام وسائط بجوار قاعدته | .nav { @media (...) { } }
```

:::warning لا تتعمق في التداخل
التداخل العميق ينتج محددات طويلة وخاصة جدًا يصعب تجاوزها. اكتفِ بنحو ثلاثة مستويات.
:::

```exercise css
? نسّق حالة المرور على .btn من داخلها
.btn { ___:hover { opacity: .8; } }
= &
```

```quiz
? داخل .card { &.dark { } }، ما المحدد الناتج؟
* .card.dark
- .card .dark
- .dark .card
```

# @lesson sass-mixins
title: الـ Mixins
summary: مجموعات تنسيق قابلة لإعادة الاستخدام بـ @mixin و @include والمعاملات و @content.
---
```try html scss
<style type="text/scss">
@mixin center {
  display: flex;
  align-items: center;
  justify-content: center;
}

@mixin button($bg, $fg: #fff, $radius: 8px) {   // معاملات بقيم افتراضية
  background: $bg;
  color: $fg;
  border: 0;
  border-radius: $radius;
  padding: 8px 16px;
  cursor: pointer;
}

@mixin on-small-screens {
  @media (max-width: 600px) { @content; }      // @content = الكتلة المرسلة
}

.hero {
  @include center;
  height: 90px;
  background: #f1f5f9;
  gap: 8px;
  @include on-small-screens { flex-direction: column; height: auto; }
}
.btn-save { @include button(#15803d); }
.btn-delete { @include button(#b91c1c, $radius: 999px); }
</style>

<div class="hero">
  <button class="btn-save">حفظ</button>
  <button class="btn-delete">حذف</button>
</div>
```

```reference css
@mixin name { } | تعريف كتلة قابلة لإعادة الاستخدام | @mixin card { padding: 16px; }
@include name; | استخدامها | .box { @include card; }
@mixin name($a, $b: default) | المعاملات والقيم الافتراضية | @mixin pad($x: 8px)
name($b: value) | معامل بالاسم | @include button($radius: 4px)
@content | إدراج كتلة المستدعي | @mixin dark { .dark & { @content; } }
```

```exercise css
? استخدم الـ mixin المسمى center داخل .box
.box { ___ center; }
= @include
```

```quiz
? ماذا يفعل @content داخل mixin؟
* يدرج كتلة التنسيقات المكتوبة حيث استُدعي الـ mixin
- يطبع محتوى الصفحة
- يستورد ملفًا آخر
```

# @lesson sass-extend
title: العناصر النائبة و @extend
summary: مشاركة التنسيقات بين المحددات، ومتى نفضّل الـ mixins.
---
```try html scss
<style type="text/scss">
%message {                              // محدد نائب: لا يُخرج وحده أبدًا
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid transparent;
}

.message-ok   { @extend %message; background: #dcfce7; border-color: #86efac; }
.message-warn { @extend %message; background: #fef3c7; border-color: #fcd34d; }
.message-err  { @extend %message; background: #fee2e2; border-color: #fca5a5; }
</style>

<div class="message-ok">تم الحفظ بنجاح.</div>
<div class="message-warn">تنتهي جلستك خلال 5 دقائق.</div>
<div class="message-err">فشل الدفع.</div>
```

انظر إلى CSS الناتجة: الأصناف الثلاثة **مجمّعة في محدد واحد** للقواعد المشتركة بدل تكرارها.

```reference css
%name { } | محدد نائب (لا يُخرج وحده) | %clearfix { }
@extend %name; | مشاركة قواعد المحدد النائب | .note { @extend %box; }
@extend .class; | مشاركة قواعد صنف آخر (بحذر) | .error { @extend .alert; }
```

:::tip mixin أم extend؟
`@extend` يجمع المحددات ويُبقي CSS صغيرة، لكنه قد يُنتج تركيبات محددات مفاجئة عبر الملفات. أما الـ mixins فتنسخ التنسيقات، وهذا أوضح ويقبل المعاملات. وعند الشك استخدم mixin.
:::

```exercise css
? شارك قواعد المحدد النائب %box
.note { ___ %box; }
= @extend
```

```quiz
? لماذا يفيد المحدد النائب (%name)؟
* تتشارك قواعده المحددات التي تمدّه، ولا يُخرج وحده
- يُحمَّل أسرع من الصنف
- يعمل فقط داخل استعلامات الوسائط
```

# @lesson sass-modules
title: الوحدات والملفات الجزئية والدوال المدمجة
summary: @use و @forward، والملفات الجزئية، ووحدات sass:color و sass:math و sass:string.
---
المشاريع الحقيقية تقسّم التنسيقات إلى ملفات. والملف الذي يبدأ اسمه بـ `_` **ملف جزئي (partial)**: تحمّله ملفات أخرى فقط ولا يُترجم وحده.

```text
styles/
  _tokens.scss       $brand: #4338ca; $radius: 10px;
  _buttons.scss      @use "tokens"; .btn { background: tokens.$brand; }
  main.scss          @use "tokens"; @use "buttons";
```

`@use "tokens"` يحمّل `_tokens.scss` مرة واحدة ويعطي محتواه **مساحة أسماء** (`tokens.$brand`)، وهو يحل محل `@import` القديمة المهمَلة.

وتأتي Sass بوحدات مدمجة يستخدمها المثال التالي (يستخدم الوحدات المدمجة فقط لأن ساحة التجربة بلا ملفات):

```try html scss
<style type="text/scss">
@use "sass:color";
@use "sass:math";
@use "sass:string";

$brand: #4338ca;

.swatch { display: inline-block; width: 70px; height: 50px; margin: 4px; border-radius: 8px; color: #fff; font: 12px sans-serif; padding: 4px; }
.base   { background: $brand; }
.light  { background: color.scale($brand, $lightness: 40%); }
.dark   { background: color.scale($brand, $lightness: -30%); }
.mix    { background: color.mix($brand, #0e7490, 50%); }
.faded  { background: color.change($brand, $alpha: 0.5); }

.col { width: math.percentage(math.div(1, 3)); }       // 33.333%
.title::after { content: string.to-upper-case("sass"); }
</style>

<div class="swatch base">base</div><div class="swatch light">lighter</div><div class="swatch dark">darker</div><div class="swatch mix">mix</div><div class="swatch faded">50%</div>
<p class="title">الوحدات المدمجة: </p>
```

```reference css
@use "file"; | تحميل وحدة مرة واحدة بمساحة أسماء | @use "tokens"; tokens.$brand
@use "file" as t; | اختيار مساحة الأسماء | @use "tokens" as t;
@forward "file"; | إعادة تصدير محتوى وحدة | @forward "buttons";
_name.scss | ملف جزئي (لا يُترجم وحده) | _variables.scss
color.scale / color.adjust / color.mix | أدوات الألوان (بدل darken و lighten) | color.scale($c, $lightness: -20%)
math.div / math.percentage / math.round | الحساب (القسمة بـ math.div) | math.div(100%, 3)
```

:::warning الدوال القديمة و @import
ما زالت `darken()` و `lighten()` وعامل القسمة `/` و `@import` تعمل لكنها مهمَلة. استخدم `color.scale` أو `color.adjust` و `math.div` و `@use` في الكود الجديد.
:::

```exercise css
? حمّل وحدة الألوان المدمجة
@use "sass:___";
= color
```

```quiz
? أي قاعدة تحمّل وحدة Sass بمساحة أسماء وتحل محل @import؟
* @use
- @include
- @extend
```

# @lesson sass-functions
title: دوالك الخاصة
summary: @function و @return، وتحويل أحجام البكسل إلى rem.
---
```try html scss
<style type="text/scss">
@use "sass:math";

$base-font: 16px;

@function rem($px) {
  @return math.div($px, $base-font) * 1rem;
}

@function spacing($step) {
  @if $step < 0 { @error "spacing() needs a positive step, got #{$step}"; }
  @return $step * 4px;
}

h2 { font-size: rem(28px); margin: 0 0 spacing(2); }
p  { font-size: rem(15px); line-height: 1.6; padding: spacing(3); background: #f8fafc; }
</style>

<h2>الأحجام بوحدة rem</h2>
<p>أصبحت 28px تساوي 1.75rem و 15px تساوي 0.9375rem، فيكبر النص مع إعدادات خط المستخدم.</p>
```

```reference css
@function name($a) { @return ...; } | تعريف دالة | @function double($x) { @return $x * 2; }
@return | نتيجة الدالة | @return math.div($px, 16px) * 1rem;
@if / @else | الشروط | @if $dark { ... } @else { ... }
@error / @warn | التوقف بخطأ / طباعة تحذير | @error "bad value #{$v}";
```

:::tip الـ mixins تكتب قواعد والدوال ترجع قيمًا
استخدم دالة عندما تحتاج قيمة داخل خاصية (`font-size: rem(18px)`)، واستخدم mixin عندما تحتاج تنسيقات أو قواعد كاملة.
:::

```exercise css
? أرجع النتيجة من دالة Sass
@function half($x) { ___ math.div($x, 2); }
= @return
```

```quiz
? ما الفرق بين الدالة والـ mixin؟
* الدالة ترجع قيمة، والـ mixin تُخرج تنسيقات
- لا فرق بينهما
- الـ mixin ترجع قيمة والدالة تُخرج قواعد
```

# @lesson sass-control
title: الخرائط والحلقات والشروط
summary: الخرائط و @each و @for و @if، وتوليد الأصناف المساعدة.
---
```try html scss
<style type="text/scss">
@use "sass:map";
@use "sass:color";

$colors: (
  "primary": #4338ca,
  "success": #15803d,
  "warning": #b45309,
  "danger": #b91c1c,
);

@each $name, $color in $colors {                // صنف لكل عنصر في الخريطة
  .btn-#{$name} {
    background: $color;
    color: #fff;
    border: 0;
    padding: 6px 12px;
    border-radius: 6px;
    &:hover { background: color.scale($color, $lightness: -15%); }
  }
}

@for $i from 1 through 4 {                      // أصناف مسافات مساعدة .mt-1 ... .mt-4
  .mt-#{$i} { margin-top: $i * 4px; }
}

$theme: "dark";
.panel {
  padding: 10px;
  @if $theme == "dark" { background: #1e293b; color: #e2e8f0; }
  @else { background: #f8fafc; color: #0f172a; }
}

.note { color: map.get($colors, "warning"); }
</style>

<button class="btn-primary">Primary</button>
<button class="btn-success">Success</button>
<button class="btn-warning">Warning</button>
<button class="btn-danger">Danger</button>
<div class="panel mt-3">لوحة داكنة تبعد 12px عن الأزرار.</div>
<p class="note mt-2">هذا اللون جاء من الخريطة.</p>
```

```reference css
$map: (key: value, ...) | خريطة | $sizes: ("sm": 4px, "lg": 16px);
map.get($map, key) | قراءة قيمة | map.get($sizes, "lg")
@each $k, $v in $map | المرور على خريطة | @each $name, $c in $colors { }
@each $item in $list | المرور على قائمة | @each $side in top, bottom { }
@for $i from 1 through n | حلقة بعدد محدد | @for $i from 1 through 5 { }
@if / @else if / @else | الشروط | @if $theme == "dark" { }
```

:::tip هكذا تعمل أطر العمل
يبني Bootstrap مئات الأصناف مثل `.btn-primary` و `.mt-3` بهذه الطريقة بالضبط: خريطة رموز وبضع حلقات.
:::

```exercise css
? مرّ على كل اسم ولون في $colors
___ $name, $color in $colors { }
= @each
```

```quiz
? ماذا ينتج @for $i from 1 through 3؟
* ثلاث دورات بقيم $i = 1 و 2 و 3
- دورتين
- دورة واحدة بقائمة
```

# @lesson sass-project
title: مشروع: نظام سمات صغير
summary: رموز التصميم، و mixin للأزرار، وأشكال مولّدة، وسمة داكنة بمتغيرات CSS.
---
```try html scss
<style type="text/scss">
@use "sass:map";
@use "sass:color";

// 1. رموز التصميم
$tokens: (
  "brand": #4338ca,
  "accent": #0e7490,
  "danger": #b91c1c,
);
$radius: 10px;

// 2. قيم الفاتح والداكن كمتغيرات CSS لتتغير السمة في المتصفح
:root {
  --bg: #ffffff; --text: #0f172a; --card: #f1f5f9;
  @each $name, $value in $tokens { --#{$name}: #{$value}; }
}
.dark {
  --bg: #0f172a; --text: #e2e8f0; --card: #1e293b;
}

// 3. مكونات مبنية من الرموز
@mixin button-variant($color) {
  background: $color;
  &:hover { background: color.scale($color, $lightness: -15%); }
}

.theme { background: var(--bg); color: var(--text); padding: 14px; border-radius: $radius; }
.card {
  background: var(--card);
  border-radius: $radius;
  padding: 12px;
  margin-bottom: 10px;
  h4 { margin: 0 0 6px; color: var(--brand); }
}
.btn {
  border: 0; color: #fff; padding: 7px 14px; border-radius: $radius; cursor: pointer;
  @each $name, $value in $tokens {
    &-#{$name} { @include button-variant($value); }
  }
}
</style>

<div class="theme" id="t">
  <div class="card"><h4>طلب رقم 1024</h4>3 منتجات · 450 جنيه</div>
  <button class="btn btn-brand">ادفع</button>
  <button class="btn btn-accent">تتبّع</button>
  <button class="btn btn-danger">إلغاء</button>
  <button onclick="document.getElementById('t').classList.toggle('dark')">الوضع الداكن</button>
</div>
```

:::tip اجعله مشروعك
أضف رمز "success" وشاهد صنف `.btn-success` جديدًا يظهر في CSS الناتجة دون أن تكتبه، أو غيّر `$radius` مرة واحدة ليتغير شكل كل المكونات.
:::

```quiz
? لماذا يضع المشروع الألوان في متغيرات CSS إلى جانب Sass؟
* لتتبدل السمة في المتصفح دون إعادة الترجمة
- لأن Sass لا تخزن الألوان
- لتقصير الملف
```

# @lesson sass-reference
title: مرجع Sass السريع
summary: أكثر مزايا Sass استخدامًا في صفحة واحدة.
---
```reference css
$var: value; | متغير | $brand: #4338ca;
#{$var} | الإدراج | .icon-#{$name} { }
.a { .b { } } / & | التداخل / محدد الأب | &:hover, &--active
@mixin / @include / @content | كتل قابلة لإعادة الاستخدام | @include button($bg)
%placeholder / @extend | قواعد مشتركة | @extend %card;
@use "file" / @forward | الوحدات | @use "tokens" as t;
@function / @return | دوالك الخاصة | @function rem($px) { }
@if / @each / @for | المنطق والحلقات | @each $k, $v in $map { }
map.get / color.scale / math.div | الوحدات المدمجة | color.scale($c, $lightness: 20%)
_partial.scss | ملفات تحمّلها ملفات أخرى | _buttons.scss
sass input.scss output.css | الترجمة من سطر الأوامر | sass --watch scss:css
```

:::tip الخطوة التالية
أعد تنسيق صفحة من دورتي HTML أو Bootstrap برموز و mixins خاصة بك في Sass، ثم اقرأ كيف يتيح ملف `_variables.scss` في Bootstrap تخصيص الإطار كله ببضعة متغيرات.
:::

```quiz
? أي دالة مدمجة يجب أن تحل محل darken() في الكود الجديد؟
* color.scale أو color.adjust
- math.div
- map.get
```
