# @lesson css-intro
title: مقدمة في CSS
summary: ما هي CSS ولماذا نفصل التنسيق عن المحتوى.
---
**CSS** اختصار لـ *Cascading Style Sheets* أي «أوراق الأنماط المتتالية». HTML تحدد **ما** في الصفحة، وCSS تحدد **كيف** يبدو: الألوان، الخطوط، المسافات، وترتيب العناصر.

## مثال سريع

جرّب تغيير اللون أو الحجم ثم اضغط **تشغيل**:

```try html
<style>
  body { font-family: sans-serif; background: #f8fafc; }
  h1 { color: #4338ca; text-align: center; }
  p { color: #334155; font-size: 18px; }
</style>
<h1>مرحبًا CSS</h1>
<p>نفس HTML، لكن بشكل مختلف تمامًا.</p>
```

## لماذا CSS؟

- **ملف واحد لكل الصفحات**: غيّر لون العناوين في كل الموقع من مكان واحد.
- **كود أنظف**: HTML للمحتوى فقط، والتنسيق في مكانه.
- **تصميم متجاوب**: نفس الصفحة تبدو جيدة على الكمبيوتر والجوال.

:::info من أين جاء اسم «المتتالية»؟
عندما تنطبق عدة قواعد على نفس العنصر، تُطبَّق كلها «بالتتابع»، وتفوز القاعدة الأدق أو الأخيرة عند التعارض.
:::

```quiz
? ما وظيفة CSS؟
- تحديد محتوى الصفحة
* تحديد شكل الصفحة وتنسيقها
- تخزين بيانات الموقع

? يمكن لملف CSS واحد أن ينسّق صفحات كثيرة.
= true
```

# @lesson css-syntax
title: صيغة CSS
summary: المحدِّد والخاصية والقيمة.
---
قاعدة CSS تتكون من **محدِّد** يختار العناصر، ثم **إعلانات** بين قوسين معقوفين:

```css
h1 {
  color: crimson;
  font-size: 32px;
}
```

- `h1` المحدِّد: يختار كل عناوين المستوى الأول.
- `color` و `font-size` خصائص، و`crimson` و `32px` قيمها.
- كل إعلان ينتهي بفاصلة منقوطة `;`.

```try html
<style>
  p { color: green; text-align: center; }
</style>
<p>كل الفقرات خضراء وفي المنتصف.</p>
<p>وهذه أيضًا.</p>
```

## التعليقات في CSS

التعليق يُكتب بين `/*` و `*/`:

```css
/* لون العناوين الرئيسية */
h1 { color: navy; }
```

```exercise css
? أكمل القاعدة لتلوين الفقرات بالأحمر
p {
  ___: red;
}
= color
```

```quiz
? في القاعدة p { color: red; } ما هو المحدِّد؟
* p
- color
- red

? كيف يُكتب التعليق في CSS؟
- <!-- تعليق -->
* /* تعليق */
- // تعليق
```

# @lesson css-howto
title: طرق إضافة CSS
summary: داخل الوسم، في رأس الصفحة، أو في ملف خارجي.
---
توجد ثلاث طرق لإضافة CSS:

## 1. ملف خارجي (الأفضل)

ضع القواعد في ملف مثل `style.css` واربطه في `<head>`:

```html
<head>
  <link rel="stylesheet" href="style.css">
</head>
```

## 2. داخل الصفحة

ضع القواعد في عنصر `<style>` داخل `<head>`:

```try html
<style>
  h2 { color: darkorange; }
</style>
<h2>تنسيق داخلي</h2>
```

## 3. داخل الوسم

استخدم السمة `style` على عنصر واحد:

```try html
<p style="color: purple; font-weight: bold;">تنسيق مباشر لهذه الفقرة فقط.</p>
```

:::tip أيها أستخدم؟
الملف الخارجي للموقع كله، و`<style>` لصفحة واحدة خاصة، والسمة `style` للحالات النادرة فقط؛ لأنها تخلط التنسيق بالمحتوى.
:::

## الأولوية

إذا تعارضت القواعد، يفوز التنسيق داخل الوسم، ثم القاعدة الأكثر تحديدًا، ثم الأحدث في الترتيب.

```try html
<style>
  p { color: blue; }
</style>
<p>زرقاء من القاعدة.</p>
<p style="color: red;">حمراء: التنسيق المباشر يفوز.</p>
```

```quiz
? ما أفضل طريقة لتنسيق موقع كامل؟
- السمة style على كل عنصر
* ملف CSS خارجي مربوط بـ <link>
- عنصر <style> في كل صفحة

? التنسيق داخل الوسم يفوز على قاعدة في ملف خارجي.
= true
```

# @lesson css-selectors
title: المحدِّدات
summary: العنصر، الصنف، المعرّف، التجميع، والتداخل.
---
المحدِّد يختار العناصر التي تنطبق عليها القاعدة:

```reference css
p | كل عناصر p | p { color: gray; }
.card | كل عنصر class="card" | .card { padding: 8px; }
#logo | العنصر الذي id="logo" | #logo { width: 120px; }
* | كل العناصر | * { box-sizing: border-box; }
h1, h2 | تجميع عدة محدِّدات | h1, h2 { color: navy; }
nav a | كل a داخل nav | nav a { text-decoration: none; }
a:hover | عند مرور الفأرة | a:hover { color: red; }
li:first-child | أول عنصر | li:first-child { font-weight: bold; }
```

```try html
<style>
  .note { background: #fef9c3; padding: 6px; }
  #main-title { color: #4338ca; }
  nav a { margin: 0 6px; }
  a:hover { color: crimson; }
</style>
<h1 id="main-title">عنوان بمعرّف</h1>
<p class="note">فقرة بصنف note</p>
<p>فقرة عادية</p>
<nav><a href="#">الرئيسية</a><a href="#">من نحن</a></nav>
```

:::info الصنف أم المعرّف؟
`id` فريد: عنصر واحد في الصفحة. `class` يمكن تكراره على عناصر كثيرة، وهو الأكثر استخدامًا في التنسيق.
:::

```exercise css
? أكمل المحدِّد ليختار كل عنصر class="box"
___box {
  border: 1px solid gray;
}
= .
```

```quiz
? أي محدِّد يختار العنصر id="logo"؟
- .logo
* #logo
- logo

? يمكن أن يحمل أكثر من عنصر نفس الصنف class.
= true
```

# @lesson css-colors
title: الألوان
summary: أسماء الألوان، والقيم الست عشرية، و rgb و hsl والشفافية.
---
يمكن كتابة اللون بعدة طرق:

```reference css
اسم اللون | أكثر من 140 اسمًا | color: tomato;
#RRGGBB | قيمة ست عشرية | color: #4338ca;
rgb() | أحمر وأخضر وأزرق 0–255 | color: rgb(67, 56, 202);
rgba() / rgb(… / a) | مع الشفافية 0–1 | background: rgba(0, 0, 0, 0.5);
hsl() | درجة وتشبّع وإضاءة | color: hsl(243, 57%, 50%);
```

```try html
<style>
  .a { background: tomato; }
  .b { background: #0ea5e9; }
  .c { background: rgb(34, 197, 94); }
  .d { background: rgba(67, 56, 202, 0.4); }
  div { color: white; padding: 8px; margin: 4px 0; }
</style>
<div class="a">tomato</div>
<div class="b">#0ea5e9</div>
<div class="c">rgb(34, 197, 94)</div>
<div class="d">rgba مع شفافية</div>
```

- `color` لون النص.
- `background-color` لون الخلفية.
- `border-color` لون الإطار.

```exercise css
? اجعل خلفية العنصر صفراء
.alert {
  ___: yellow;
}
= background-color | background
```

```quiz
? أي قيمة تعني لونًا شفافًا جزئيًا؟
- rgb(0, 0, 0)
* rgba(0, 0, 0, 0.5)
- #000000

? الخاصية color تغيّر لون الخلفية.
= false
> color للنص، وbackground-color للخلفية.
```

# @lesson css-backgrounds
title: الخلفيات
summary: لون الخلفية، والصورة، والتكرار، والموضع، والحجم، والتدرّج.
---
```reference css
background-color | لون الخلفية | background-color: #f1f5f9;
background-image | صورة أو تدرّج | background-image: url("bg.png");
background-repeat | تكرار الصورة | background-repeat: no-repeat;
background-position | موضع الصورة | background-position: center;
background-size | حجم الصورة | background-size: cover;
background | اختصار لكل ما سبق | background: #000 url(a.png) no-repeat center / cover;
```

```try html
<style>
  .hero {
    height: 160px;
    color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    background: url("https://picsum.photos/600/300") center / cover no-repeat;
  }
  .grad {
    margin-top: 8px; padding: 20px; color: white;
    background: linear-gradient(to left, #4338ca, #06b6d4);
  }
</style>
<div class="hero">خلفية بصورة</div>
<div class="grad">خلفية بتدرّج لوني</div>
```

:::tip cover أم contain؟
`cover` تملأ المساحة كلها وقد تقص أطراف الصورة. `contain` تُظهر الصورة كاملة وقد تترك فراغًا.
:::

```quiz
? أي قيمة تجعل صورة الخلفية تملأ العنصر كله؟
* background-size: cover
- background-repeat: repeat
- background-position: top

? الدالة linear-gradient تنشئ تدرّجًا لونيًا يُستخدم كخلفية.
= true
```

# @lesson css-text
title: النصوص
summary: المحاذاة، والتزيين، والتحويل، والمسافات بين الأسطر والحروف.
---
```reference css
text-align | المحاذاة | text-align: center;
text-decoration | خط تحت/فوق/وسط النص | text-decoration: underline;
text-transform | أحرف كبيرة/صغيرة (للاتينية) | text-transform: uppercase;
line-height | ارتفاع السطر | line-height: 1.8;
letter-spacing | المسافة بين الحروف | letter-spacing: 2px;
word-spacing | المسافة بين الكلمات | word-spacing: 6px;
text-shadow | ظل النص | text-shadow: 1px 1px 2px gray;
direction | اتجاه النص | direction: rtl;
```

```try html
<style>
  h2 { text-align: center; text-shadow: 2px 2px 4px #94a3b8; }
  .en { text-transform: uppercase; letter-spacing: 3px; direction: ltr; }
  .lh { line-height: 2; }
  a { text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
<h2>عنوان في المنتصف بظل</h2>
<p class="en">hello css</p>
<p class="lh">فقرة بارتفاع سطر كبير يجعل القراءة أريح خصوصًا للنصوص العربية الطويلة التي تمتد على أكثر من سطر.</p>
<a href="#">رابط بلا خط حتى تمر عليه</a>
```

:::info المحاذاة في الصفحات العربية
في صفحة `dir="rtl"` يبدأ النص من اليمين تلقائيًا. استخدم `text-align: start` لتعمل المحاذاة صحيحة في الاتجاهين.
:::

```exercise css
? أزل الخط من تحت الروابط
a {
  text-decoration: ___;
}
= none
```

```quiz
? أي خاصية تغيّر ارتفاع السطر؟
- letter-spacing
* line-height
- text-align

? القيمة text-transform: uppercase تؤثر على الحروف العربية.
= false
> الحروف العربية ليس لها أحرف كبيرة وصغيرة.
```

# @lesson css-fonts
title: الخطوط
summary: نوع الخط، والحجم، والسماكة، والخطوط من الإنترنت.
---
```reference css
font-family | نوع الخط مع بدائل | font-family: "Cairo", Tahoma, sans-serif;
font-size | الحجم | font-size: 18px;
font-weight | السماكة | font-weight: bold;
font-style | مائل | font-style: italic;
font | اختصار | font: italic bold 16px/1.6 sans-serif;
```

```try html
<style>
  .serif { font-family: Georgia, serif; }
  .mono { font-family: "Courier New", monospace; direction: ltr; }
  .big { font-size: 2rem; font-weight: 700; }
  .light { font-weight: 300; font-style: italic; }
</style>
<p class="serif">خط بحواف (serif)</p>
<p class="mono">monospace: كل الحروف بنفس العرض</p>
<p class="big">نص كبير وعريض</p>
<p class="light">نص خفيف ومائل</p>
```

## وحدات الحجم

- `px` بكسل ثابت.
- `em` نسبة إلى حجم خط العنصر الأب.
- `rem` نسبة إلى حجم خط الصفحة (الجذر)، وهي الأنسب غالبًا.
- `%` نسبة مئوية.

:::tip اكتب بدائل للخط
إذا لم يتوفر الخط الأول على جهاز الزائر، يستخدم المتصفح التالي في القائمة. اختم القائمة دائمًا بعائلة عامة مثل `sans-serif`.
:::

```quiz
? أي وحدة تُحسب نسبة إلى حجم خط الصفحة الجذر؟
- px
- em
* rem

? الخاصية font-weight تتحكم في سماكة الخط.
= true
```

# @lesson css-box-model
title: نموذج الصندوق
summary: المحتوى والحشوة والإطار والهامش، و box-sizing.
---
كل عنصر في الصفحة **صندوق** من أربع طبقات، من الداخل للخارج:

1. **المحتوى** (content): النص أو الصورة.
2. **الحشوة** (padding): مسافة بين المحتوى والإطار.
3. **الإطار** (border): خط حول الحشوة.
4. **الهامش** (margin): مسافة خارج الإطار تفصل العنصر عن غيره.

```try html
<style>
  .box {
    width: 200px;
    padding: 20px;
    border: 5px solid #4338ca;
    margin: 30px;
    background: #e0e7ff;
  }
</style>
<div class="box">محتوى الصندوق</div>
```

## العرض الحقيقي

افتراضيًا: العرض الكلي = `width` + الحشوة + الإطار. في المثال: 200 + 40 + 10 = 250 بكسل.

مع `box-sizing: border-box` يصبح `width` شاملًا للحشوة والإطار، وهذا أسهل كثيرًا:

```try html
<style>
  div { width: 200px; padding: 20px; border: 5px solid teal; margin-bottom: 8px; }
  .bb { box-sizing: border-box; }
</style>
<div>بدون border-box (عرضه 250)</div>
<div class="bb">مع border-box (عرضه 200)</div>
```

:::tip قاعدة شائعة
كثير من المشاريع تبدأ بـ `* { box-sizing: border-box; }` لتطبيقها على كل العناصر.
:::

```quiz
? ما الطبقة التي تقع بين المحتوى والإطار؟
* padding
- margin
- outline

? مع box-sizing: border-box يشمل width الحشوة والإطار.
= true
```

# @lesson css-borders
title: الإطارات
summary: نمط الإطار وسماكته ولونه، والزوايا المستديرة.
---
```reference css
border-style | نمط الخط | border-style: dashed;
border-width | السماكة | border-width: 3px;
border-color | اللون | border-color: gray;
border | اختصار | border: 2px solid #4338ca;
border-top / border-inline-start | جهة واحدة | border-bottom: 1px solid #ddd;
border-radius | زوايا مستديرة | border-radius: 12px;
```

```try html
<style>
  div { padding: 10px; margin: 8px 0; }
  .solid { border: 2px solid #0f766e; }
  .dashed { border: 2px dashed #b45309; }
  .round { border: 2px solid #4338ca; border-radius: 16px; }
  .side { border-inline-start: 6px solid crimson; background: #fff1f2; }
  .circle { width: 80px; height: 80px; border-radius: 50%; background: #06b6d4; }
</style>
<div class="solid">إطار متصل</div>
<div class="dashed">إطار متقطع</div>
<div class="round">زوايا مستديرة</div>
<div class="side">خط في بداية العنصر فقط</div>
<div class="circle"></div>
```

```exercise css
? اجعل زوايا البطاقة مستديرة
.card {
  ___: 10px;
}
= border-radius
```

```quiz
? أي قيمة تجعل مربعًا دائرة؟
- border-radius: 10px
* border-radius: 50%
- border-style: circle

? الخاصية border-inline-start تضع الإطار في بداية العنصر حسب اتجاه النص.
= true
```

# @lesson css-margin-padding
title: الهوامش والحشوة
summary: كتابة القيم لكل جهة، والتوسيط بـ auto.
---
`margin` و `padding` يقبلان من قيمة إلى أربع قيم:

```reference css
قيمة واحدة | كل الجهات | margin: 10px;
قيمتان | أعلى/أسفل ثم يمين/يسار | padding: 10px 20px;
أربع قيم | أعلى، يمين، أسفل، يسار | margin: 5px 10px 15px 20px;
جهة واحدة | جهة محددة | margin-top: 12px;
auto | يوزع المساحة المتبقية | margin: 0 auto;
```

```try html
<style>
  .center { width: 220px; margin: 20px auto; padding: 12px 24px; background: #dcfce7; }
  .tight { padding: 2px; background: #fee2e2; }
  .roomy { padding: 24px; background: #e0f2fe; }
</style>
<div class="center">في المنتصف بـ margin: auto</div>
<p class="tight">حشوة صغيرة</p>
<p class="roomy">حشوة كبيرة</p>
```

:::info الفرق ببساطة
الحشوة **داخل** العنصر وتأخذ لون خلفيته، والهامش **خارجه** ويبقى شفافًا.
:::

```exercise css
? وسّط العنصر أفقيًا
.page {
  width: 600px;
  margin: 0 ___;
}
= auto
```

```quiz
? ماذا تعني padding: 10px 20px؟
* 10 أعلى وأسفل، و20 يمين ويسار
- 10 يمين ويسار، و20 أعلى وأسفل
- 10 لكل الجهات

? الهامش margin يأخذ لون خلفية العنصر.
= false
```

# @lesson css-display
title: الخاصية display
summary: block و inline و inline-block و none.
---
`display` تحدد كيف يُعرض العنصر:

```reference css
block | سطر كامل لوحده | display: block;
inline | داخل السطر بلا عرض أو ارتفاع | display: inline;
inline-block | داخل السطر مع عرض وارتفاع | display: inline-block;
none | يختفي تمامًا ولا يأخذ مساحة | display: none;
flex | حاوية Flexbox | display: flex;
grid | حاوية Grid | display: grid;
```

```try html
<style>
  .chip { display: inline-block; padding: 4px 12px; margin: 2px; border-radius: 999px; background: #e0e7ff; }
  .menu a { display: block; padding: 6px; border-bottom: 1px solid #e2e8f0; }
  .hidden { display: none; }
</style>
<span class="chip">HTML</span><span class="chip">CSS</span><span class="chip">JS</span>
<div class="menu"><a href="#">رابط يأخذ سطرًا كاملًا</a><a href="#">رابط آخر</a></div>
<p class="hidden">لن تراني</p>
<p>الفقرة المخفية أعلاه لا تأخذ أي مساحة.</p>
```

:::tip display: none أم visibility: hidden؟
`display: none` يزيل العنصر من التخطيط. `visibility: hidden` يخفيه لكن يترك مكانه فارغًا.
:::

```quiz
? أي قيمة تسمح بعرض وارتفاع مع البقاء داخل السطر؟
- inline
* inline-block
- none

? القيمة display: none تُبقي مكان العنصر فارغًا.
= false
```

# @lesson css-position
title: التموضع
summary: static و relative و absolute و fixed و sticky.
---
```reference css
static | الوضع الافتراضي | position: static;
relative | يتحرك من مكانه الأصلي | position: relative; top: 10px;
absolute | بالنسبة لأقرب أب متموضع | position: absolute; top: 0; right: 0;
fixed | ثابت بالنسبة للنافذة | position: fixed; bottom: 16px;
sticky | يلتصق عند التمرير | position: sticky; top: 0;
z-index | من فوق من | z-index: 10;
```

```try html
<style>
  .card { position: relative; width: 240px; height: 120px; background: #f1f5f9; border-radius: 8px; }
  .badge { position: absolute; top: 8px; left: 8px; background: crimson; color: white; padding: 2px 8px; border-radius: 999px; }
  .bar { position: sticky; top: 0; background: #4338ca; color: white; padding: 6px; }
</style>
<div class="bar">شريط لاصق: مرّر داخل النتيجة</div>
<div class="card">بطاقة <span class="badge">جديد</span></div>
<p style="height: 400px;">محتوى طويل للتمرير…</p>
```

:::info absolute داخل relative
اجعل الأب `position: relative` ليصبح العنصر `absolute` متموضعًا بالنسبة له، وليس بالنسبة للصفحة كلها.
:::

```quiz
? أي قيمة تثبّت العنصر في النافذة حتى أثناء التمرير؟
- relative
* fixed
- static

? العنصر absolute يتموضع بالنسبة لأقرب أب له position غير static.
= true
```

# @lesson css-flexbox
title: Flexbox
summary: ترتيب العناصر في صف أو عمود، والمحاذاة والتوزيع.
---
Flexbox يرتب العناصر داخل حاوية في **اتجاه واحد**: صف أو عمود. فعّله بـ `display: flex` على الحاوية:

```try html
<style>
  .row { display: flex; gap: 8px; justify-content: space-between; align-items: center;
         background: #f1f5f9; padding: 8px; }
  .row div { background: #4338ca; color: white; padding: 12px; border-radius: 6px; }
</style>
<div class="row">
  <div>1</div><div>2</div><div>3</div>
</div>
```

```reference css
flex-direction | الاتجاه | flex-direction: column;
justify-content | التوزيع على المحور الرئيسي | justify-content: center;
align-items | المحاذاة على المحور العرضي | align-items: center;
flex-wrap | النزول لسطر جديد | flex-wrap: wrap;
gap | المسافة بين العناصر | gap: 12px;
flex | نسبة نمو العنصر | flex: 1;
```

## التوسيط في المنتصف تمامًا

```try html
<style>
  .center { display: flex; justify-content: center; align-items: center; height: 150px; background: #ecfeff; }
</style>
<div class="center"><strong>في المنتصف أفقيًا وعموديًا</strong></div>
```

## أعمدة مرنة

```try html
<style>
  .cols { display: flex; gap: 8px; }
  .side { flex: 1; background: #fef3c7; padding: 8px; }
  .main { flex: 3; background: #dcfce7; padding: 8px; }
</style>
<div class="cols"><div class="side">جانبي (1)</div><div class="main">رئيسي (3)</div></div>
```

```exercise css
? وسّط العناصر أفقيًا داخل الحاوية
.box {
  display: flex;
  justify-content: ___;
}
= center
```

```quiz
? أي خاصية توزع العناصر على المحور الرئيسي؟
* justify-content
- align-items
- flex-wrap

? نظام Flexbox مناسب لترتيب العناصر في اتجاه واحد.
= true
```

# @lesson css-grid
title: Grid
summary: شبكة من صفوف وأعمدة، والوحدة fr، والتمدد على عدة خلايا.
---
Grid يرتب العناصر في **بعدين**: صفوف وأعمدة معًا.

```try html
<style>
  .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
  .grid div { background: #e0e7ff; padding: 16px; text-align: center; border-radius: 6px; }
  .wide { grid-column: span 2; background: #c7d2fe !important; }
</style>
<div class="grid">
  <div class="wide">يمتد على عمودين</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

- `fr` جزء من المساحة المتاحة: `1fr 2fr` يعطي الثاني ضعف الأول.
- `repeat(3, 1fr)` اختصار لثلاثة أعمدة متساوية.
- `grid-column: span 2` يجعل العنصر يمتد على عمودين.

## شبكة تتكيف تلقائيًا

```try html
<style>
  .auto { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; }
  .auto div { background: #dcfce7; padding: 20px; text-align: center; }
</style>
<div class="auto"><div>أ</div><div>ب</div><div>ج</div><div>د</div><div>هـ</div><div>و</div></div>
```

:::tip Flexbox أم Grid؟
Flexbox لصف أو عمود واحد (قائمة أزرار، شريط). Grid لتخطيط من صفوف وأعمدة (صفحة، معرض صور).
:::

```exercise css
? أنشئ ثلاثة أعمدة متساوية
.gallery {
  display: grid;
  grid-template-columns: repeat(3, ___);
}
= 1fr
```

```quiz
? ماذا تعني الوحدة fr؟
- بكسل ثابت
* جزء من المساحة المتاحة
- نسبة من حجم الخط

? نظام Grid يرتب العناصر في صفوف وأعمدة معًا.
= true
```

# @lesson css-responsive
title: التصميم المتجاوب
summary: viewport، والاستعلامات media، والصور المرنة.
---
الصفحة **المتجاوبة** تبدو جيدة على كل الشاشات. الخطوة الأولى في `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

## الاستعلامات media

تطبّق قواعد فقط عندما تتحقق شروط معينة، مثل عرض الشاشة:

```try html
<style>
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .cards div { background: #e0e7ff; padding: 20px; }
  @media (max-width: 600px) {
    .cards { grid-template-columns: 1fr; }
  }
</style>
<div class="cards"><div>1</div><div>2</div><div>3</div></div>
<p>صغّر النافذة أو استخدم «ملء الشاشة» لترى التغيير.</p>
```

## صور مرنة

```css
img { max-width: 100%; height: auto; }
```

:::tip ابدأ بالجوال
اكتب التنسيق للشاشة الصغيرة أولًا، ثم أضف `@media (min-width: …)` للشاشات الأكبر. هذا يسمى *mobile first*.
:::

```quiz
? ما الذي يطبق قواعد CSS حسب عرض الشاشة؟
- <meta charset>
* @media
- display: flex

? القيمة max-width: 100% تمنع الصورة من تجاوز عرض حاويتها.
= true
```

# @lesson css-transitions
title: الانتقالات والحركة
summary: transition و transform و animation.
---
## الانتقال (transition)

يجعل التغيير بين قيمتين ناعمًا بدل أن يكون فجائيًا:

```try html
<style>
  .btn { background: #4338ca; color: white; padding: 10px 20px; border: 0; border-radius: 8px;
         transition: background 0.3s, transform 0.3s; }
  .btn:hover { background: #06b6d4; transform: scale(1.1); }
</style>
<button class="btn">مرّر الفأرة فوقي</button>
```

## التحويل (transform)

```reference css
translate() | تحريك | transform: translateX(20px);
rotate() | تدوير | transform: rotate(45deg);
scale() | تكبير/تصغير | transform: scale(1.2);
skew() | إمالة | transform: skewX(10deg);
```

## الحركة (animation)

`@keyframes` تحدد مراحل الحركة، و`animation` تشغّلها:

```try html
<style>
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.3); }
  }
  .dot { width: 40px; height: 40px; border-radius: 50%; background: crimson;
         animation: pulse 1s infinite; margin: 20px; }
</style>
<div class="dot"></div>
```

:::warning اعتدل في الحركة
الحركة الكثيرة تشتت وتزعج بعض الناس. احترم إعداد `prefers-reduced-motion` عند من يطلب حركة أقل.
:::

```quiz
? أي خاصية تجعل التغيير يحدث بنعومة خلال مدة زمنية؟
* transition
- transform
- position

? القاعدة @keyframes تحدد مراحل الحركة في animation.
= true
```

# @lesson css-reference
title: مرجع خصائص CSS
summary: أهم الخصائص مع مثال لكل خاصية.
type: Reference
---
ابحث عن أي خاصية في المربع أعلى الجدول.

```reference css
color | لون النص | color: #333;
background | الخلفية | background: #fff;
font-family | نوع الخط | font-family: sans-serif;
font-size | حجم الخط | font-size: 1rem;
font-weight | سماكة الخط | font-weight: 700;
line-height | ارتفاع السطر | line-height: 1.6;
text-align | المحاذاة | text-align: center;
text-decoration | تزيين النص | text-decoration: none;
width / height | العرض والارتفاع | width: 50%;
max-width | أقصى عرض | max-width: 800px;
margin | الهامش الخارجي | margin: 0 auto;
padding | الحشوة الداخلية | padding: 1rem;
border | الإطار | border: 1px solid #ccc;
border-radius | الزوايا المستديرة | border-radius: 8px;
box-sizing | حساب الحجم | box-sizing: border-box;
box-shadow | ظل الصندوق | box-shadow: 0 2px 8px rgba(0,0,0,.2);
display | طريقة العرض | display: flex;
position | التموضع | position: absolute;
top / right / bottom / left | الإزاحة | top: 0;
z-index | الترتيب فوق بعض | z-index: 10;
overflow | المحتوى الزائد | overflow: auto;
flex-direction | اتجاه Flexbox | flex-direction: column;
justify-content | التوزيع | justify-content: space-between;
align-items | المحاذاة العرضية | align-items: center;
gap | المسافة بين العناصر | gap: 1rem;
grid-template-columns | أعمدة Grid | grid-template-columns: repeat(3, 1fr);
opacity | الشفافية | opacity: 0.5;
cursor | شكل المؤشر | cursor: pointer;
transition | الانتقال | transition: all .3s;
transform | التحويل | transform: rotate(5deg);
animation | الحركة | animation: spin 2s linear infinite;
@media | استعلام الشاشة | @media (max-width: 600px) { … }
```

:::tip ماذا بعد؟
أصبحت تعرف كيف تبني صفحة وتنسقها. الخطوة التالية: **JavaScript** لتجعل الصفحة تتفاعل مع الزائر.
:::
