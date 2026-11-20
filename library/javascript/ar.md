# @lesson js-intro
title: مقدمة في JavaScript
summary: ما هي JavaScript وماذا تستطيع أن تفعل.
---
**JavaScript** هي لغة البرمجة التي تعمل داخل المتصفح. HTML تبني الصفحة، وCSS تنسقها، وJavaScript تجعلها **تتفاعل**: تستجيب للنقرات، تتحقق من النماذج، تغيّر المحتوى، وتجلب البيانات من الخادم.

## أول برنامج

اضغط **تشغيل**. ما يطبعه `console.log` يظهر تحت المحرر:

```try javascript
console.log("مرحبًا يا JavaScript");
console.log(2 + 3);
```

## JavaScript تغيّر الصفحة

```try html
<p id="msg">النص الأصلي</p>
<button onclick="document.getElementById('msg').textContent = 'تغيّر النص!'">اضغط</button>
```

:::info JavaScript ليست Java
الاسم متشابه لكنهما لغتان مختلفتان تمامًا. JavaScript تعمل في كل متصفح دون تثبيت أي شيء، وتعمل أيضًا على الخوادم عبر Node.js.
:::

```quiz
? أين تعمل JavaScript أساسًا؟
* داخل المتصفح
- داخل قاعدة البيانات فقط
- داخل ملف CSS

? لغة JavaScript هي نفسها لغة Java.
= false
```

# @lesson js-output
title: الإخراج
summary: console.log، ونافذة التنبيه، وتغيير محتوى الصفحة.
---
توجد عدة طرق لإظهار النتائج:

- `console.log()` يطبع في وحدة التحكم؛ الأكثر استخدامًا أثناء التعلم واكتشاف الأخطاء.
- `alert()` يظهر نافذة تنبيه للزائر.
- `element.textContent` يغيّر نص عنصر في الصفحة.

```try javascript
console.log("نص");
console.log("المجموع:", 10 + 5);
console.log([1, 2, 3]);
console.log({ name: "سارة", age: 25 });
```

## الكتابة في الصفحة

```try html
<p id="out"></p>
<script>
  document.getElementById("out").textContent = "كتبتُ هذا من JavaScript";
</script>
```

:::tip افتح أدوات المطور
في أي متصفح اضغط `F12` ثم اختر **Console** لترى ما يطبعه `console.log` في صفحاتك.
:::

```exercise javascript
? أكمل السطر ليطبع كلمة مرحبا
console.___("مرحبا");
= log
```

```quiz
? أي أمر يطبع في وحدة التحكم؟
- print()
* console.log()
- echo()

? الخاصية textContent تغيّر نص عنصر في الصفحة.
= true
```

# @lesson js-variables
title: المتغيرات
summary: let و const، وتسمية المتغيرات.
---
**المتغير** اسم يحفظ قيمة لتستخدمها لاحقًا.

```try javascript
let city = "الرياض";
const year = 2026;
console.log(city, year);
city = "القاهرة";       // let يمكن تغييرها
console.log(city);
```

- `let` لمتغير يمكن تغيير قيمته.
- `const` لقيمة ثابتة لا تتغير بعد تعريفها.
- `var` طريقة قديمة؛ تجنّبها في الكود الجديد.

## قواعد التسمية

- يبدأ الاسم بحرف أو `_` أو `$`، ولا يبدأ برقم.
- الأحرف الكبيرة تختلف عن الصغيرة: `age` غير `Age`.
- الاسم الواضح أفضل: `totalPrice` بدل `x`.

```try javascript
const price = 50;
const quantity = 3;
const totalPrice = price * quantity;
console.log("الإجمالي:", totalPrice);
```

:::warning تغيير const خطأ
`const year = 2026;` ثم `year = 2027;` يسبب خطأ. استخدم `const` افتراضيًا، و`let` فقط عندما تحتاج للتغيير.
:::

```exercise javascript
? عرّف ثابتًا اسمه pi
___ pi = 3.14;
= const
```

```quiz
? أي كلمة تعرّف متغيرًا يمكن تغيير قيمته؟
* let
- const
- static

? يجوز أن يبدأ اسم المتغير برقم.
= false
```

# @lesson js-types
title: أنواع البيانات
summary: النصوص والأرقام والقيم المنطقية و undefined و null، و typeof.
---
```reference javascript
string | نص | "مرحبا"
number | رقم صحيح أو عشري | 42, 3.14
boolean | صح أو خطأ | true, false
undefined | متغير بلا قيمة | let x;
null | «لا شيء» عن قصد | let y = null;
object | كائن | { name: "علي" }
array | مصفوفة (نوعها object) | [1, 2, 3]
```

العامل `typeof` يخبرك بنوع القيمة:

```try javascript
console.log(typeof "نص");
console.log(typeof 42);
console.log(typeof true);
let x;
console.log(typeof x);
console.log(typeof { a: 1 });
```

## تحويل الأنواع

```try javascript
console.log(Number("10") + 5);   // 15
console.log("10" + 5);           // "105": دمج نصوص
console.log(String(99));
console.log(parseInt("42px"));   // 42
```

:::warning انتبه للجمع مع النصوص
`"10" + 5` يعطي `"105"` لأن `+` مع نص يدمج النصوص. حوّل النص إلى رقم أولًا بـ `Number()`.
:::

```quiz
? ما ناتج typeof 42؟
- "string"
* "number"
- "integer"

? ناتج "10" + 5 هو 15.
= false
> النتيجة "105" لأن الجمع مع نص يدمجه.
```

# @lesson js-operators
title: العوامل
summary: الحساب والإسناد والمقارنة والمنطق.
---
```reference javascript
+ - * / | الحساب | 10 / 4 → 2.5
% | باقي القسمة | 10 % 3 → 1
** | الأس | 2 ** 3 → 8
+= -= | إسناد مع عملية | x += 5
=== | يساوي (القيمة والنوع) | 5 === 5 → true
!== | لا يساوي | 5 !== "5" → true
> < >= <= | المقارنة | 3 > 2 → true
&& | و | true && false → false
|| | أو | true || false → true
! | النفي | !true → false
```

```try javascript
let score = 10;
score += 5;
console.log(score);
console.log(17 % 5);
console.log(5 === "5");
console.log(5 == "5");
console.log(score > 12 && score < 20);
```

:::tip استخدم === دائمًا
`==` يحوّل الأنواع قبل المقارنة فيعطي نتائج غريبة أحيانًا. `===` يقارن القيمة والنوع معًا.
:::

```exercise javascript
? أكمل لحساب باقي قسمة 10 على 3
console.log(10 ___ 3);
= %
```

```quiz
? ما ناتج 2 ** 3؟
- 6
* 8
- 9

? ناتج المقارنة 5 === "5" هو true.
= false
```

# @lesson js-strings
title: النصوص
summary: القوالب النصية، والطول، والبحث، والتقطيع، والاستبدال.
---
النص يُكتب بين `"…"` أو `'…'` أو بين علامتي `` ` `` (القوالب النصية).

## القوالب النصية

تسمح بإدراج قيم داخل النص بـ `${ }`:

```try javascript
const name = "ليلى";
const age = 22;
console.log(`اسمي ${name} وعمري ${age} سنة`);
```

## دوال مفيدة

```try javascript
const text = "Hello JavaScript";
console.log(text.length);
console.log(text.toUpperCase());
console.log(text.includes("Java"));
console.log(text.slice(0, 5));
console.log(text.replace("Hello", "Hi"));
console.log("  مسافات  ".trim());
console.log("أ,ب,ج".split(","));
```

```reference javascript
length | عدد الحروف | "abc".length → 3
toUpperCase() | أحرف كبيرة | "a".toUpperCase()
includes() | هل يحتوي؟ | "abc".includes("b")
indexOf() | موضع أول ظهور | "abc".indexOf("c") → 2
slice(a, b) | جزء من النص | "hello".slice(1, 3)
replace() | استبدال | "a-b".replace("-", "+")
trim() | حذف المسافات من الطرفين | " a ".trim()
split() | تقسيم إلى مصفوفة | "a,b".split(",")
```

```exercise javascript
? أكمل القالب النصي لإدراج المتغير name
console.log(`مرحبا ${___}`);
= name
```

```quiz
? ما ناتج "abc".length؟
- 2
* 3
- 4

? أي دالة تحذف المسافات من طرفي النص؟
- slice()
* trim()
- split()
```

# @lesson js-conditions
title: الشروط
summary: if و else if و else، والعامل الثلاثي، و switch.
---
الشرط يجعل البرنامج يتخذ قرارًا:

```try javascript
const hour = 14;
if (hour < 12) {
  console.log("صباح الخير");
} else if (hour < 18) {
  console.log("مساء الخير");
} else {
  console.log("طاب مساؤك");
}
```

## العامل الثلاثي

اختصار لـ `if/else` بسيطة:

```try javascript
const age = 20;
const status = age >= 18 ? "بالغ" : "قاصر";
console.log(status);
```

## switch

مفيد عند مقارنة قيمة واحدة بعدة احتمالات:

```try javascript
const day = 5;
switch (day) {
  case 5:
    console.log("الجمعة");
    break;
  case 6:
    console.log("السبت");
    break;
  default:
    console.log("يوم آخر");
}
```

:::warning لا تنسَ break
بدون `break` يكمل `switch` تنفيذ الحالات التالية أيضًا.
:::

```exercise javascript
? أكمل الشرط
const n = 7;
___ (n > 5) {
  console.log("كبير");
}
= if
```

```quiz
? ما ناتج: 10 > 5 ? "نعم" : "لا"؟
* "نعم"
- "لا"
- خطأ

? في switch يمنع break تنفيذ الحالات التالية.
= true
```

# @lesson js-loops
title: الحلقات
summary: for و while و for...of و break و continue.
---
الحلقة تكرر كودًا عدة مرات.

## for

```try javascript
for (let i = 1; i <= 5; i++) {
  console.log("الرقم", i);
}
```

## while

```try javascript
let n = 3;
while (n > 0) {
  console.log("العد التنازلي:", n);
  n--;
}
console.log("انطلق!");
```

## for...of لعناصر المصفوفة

```try javascript
const fruits = ["تفاح", "موز", "برتقال"];
for (const fruit of fruits) {
  console.log(fruit);
}
```

## break و continue

```try javascript
for (let i = 1; i <= 10; i++) {
  if (i === 3) continue;  // تخطَّ 3
  if (i === 6) break;     // توقف عند 6
  console.log(i);
}
```

:::warning الحلقة اللانهائية
إذا لم يصبح الشرط خطأ أبدًا، لن تتوقف الحلقة. محرر المنصة يوقفها تلقائيًا بعد ثوانٍ، لكن في صفحتك الحقيقية ستتجمد الصفحة.
:::

```exercise javascript
? أكمل الحلقة لتطبع الأرقام من 0 إلى 4
for (let i = 0; i < 5; i___) {
  console.log(i);
}
= ++
```

```quiz
? أي كلمة توقف الحلقة فورًا؟
* break
- continue
- stop

? الحلقة for...of تمر على عناصر المصفوفة واحدًا واحدًا.
= true
```

# @lesson js-functions
title: الدوال
summary: تعريف الدالة، والمعاملات، والقيمة المرجعة، والدوال السهمية.
---
**الدالة** كتلة كود لها اسم، تكتبها مرة وتستدعيها متى شئت.

```try javascript
function greet(name) {
  return "أهلًا يا " + name;
}
console.log(greet("سارة"));
console.log(greet("عمر"));
```

- `name` **معامل**: قيمة تمررها للدالة.
- `return` تعيد النتيجة وتنهي الدالة.

## قيمة افتراضية

```try javascript
function area(width, height = 1) {
  return width * height;
}
console.log(area(5, 4));
console.log(area(5));
```

## الدوال السهمية

صيغة مختصرة شائعة جدًا:

```try javascript
const square = (x) => x * x;
const add = (a, b) => a + b;
console.log(square(6), add(2, 3));
```

```exercise javascript
? أكمل الدالة لتعيد ضعف الرقم
function double(n) {
  ___ n * 2;
}
= return
```

```quiz
? ما وظيفة return؟
- طباعة قيمة
* إعادة قيمة من الدالة
- تكرار الدالة

? الدالة (a, b) => a + b دالة سهمية تجمع رقمين.
= true
```

# @lesson js-arrays
title: المصفوفات
summary: إنشاء مصفوفة، والوصول للعناصر، والإضافة والحذف.
---
**المصفوفة** قائمة مرتبة من القيم:

```try javascript
const colors = ["أحمر", "أخضر", "أزرق"];
console.log(colors[0]);        // أول عنصر: الفهرس يبدأ من 0
console.log(colors.length);
colors.push("أصفر");           // إضافة في النهاية
console.log(colors);
colors.pop();                  // حذف الأخير
colors.unshift("أسود");        // إضافة في البداية
console.log(colors);
```

```reference javascript
length | عدد العناصر | arr.length
push() | إضافة في النهاية | arr.push(4)
pop() | حذف الأخير | arr.pop()
unshift() | إضافة في البداية | arr.unshift(0)
shift() | حذف الأول | arr.shift()
includes() | هل يحتوي؟ | arr.includes(2)
indexOf() | موضع العنصر | arr.indexOf(2)
join() | دمج في نص | arr.join(", ")
slice() | نسخة من جزء | arr.slice(1, 3)
```

:::info الفهرس يبدأ من صفر
العنصر الأول هو `arr[0]` والأخير هو `arr[arr.length - 1]`.
:::

```exercise javascript
? أضف العنصر 4 في نهاية المصفوفة
const nums = [1, 2, 3];
nums.___(4);
= push
```

```quiz
? ما فهرس العنصر الأول في المصفوفة؟
* 0
- 1
- -1

? الدالة pop تحذف آخر عنصر.
= true
```

# @lesson js-array-methods
title: دوال المصفوفات
summary: forEach و map و filter و find و reduce و sort.
---
هذه الدوال تجعل العمل مع البيانات قصيرًا وواضحًا:

```try javascript
const prices = [120, 45, 300, 80];

prices.forEach((p) => console.log("السعر:", p));

const withTax = prices.map((p) => p * 1.15);
console.log("مع الضريبة:", withTax);

const cheap = prices.filter((p) => p < 100);
console.log("الرخيص:", cheap);

const first = prices.find((p) => p > 100);
console.log("أول سعر فوق 100:", first);

const total = prices.reduce((sum, p) => sum + p, 0);
console.log("المجموع:", total);

console.log("مرتبة:", [...prices].sort((a, b) => a - b));
```

```reference javascript
forEach() | نفّذ لكل عنصر | arr.forEach(x => console.log(x))
map() | مصفوفة جديدة بعد تحويل كل عنصر | arr.map(x => x * 2)
filter() | العناصر التي تحقق شرطًا | arr.filter(x => x > 0)
find() | أول عنصر يحقق الشرط | arr.find(x => x.id === 3)
some() / every() | هل بعضها/كلها يحقق الشرط؟ | arr.some(x => x < 0)
reduce() | جمع المصفوفة في قيمة واحدة | arr.reduce((s, x) => s + x, 0)
sort() | ترتيب (يغيّر الأصل) | arr.sort((a, b) => a - b)
```

:::warning sort مع الأرقام
`[10, 9, 1].sort()` يرتب كنصوص فيعطي `[1, 10, 9]`. للأرقام مرّر دالة مقارنة: `sort((a, b) => a - b)`.
:::

```exercise javascript
? احتفظ بالأرقام الزوجية فقط
const evens = [1, 2, 3, 4].___((n) => n % 2 === 0);
= filter
```

```quiz
? أي دالة تعيد مصفوفة جديدة بعد تحويل كل عنصر؟
* map()
- forEach()
- find()

? الدالة reduce تجمع عناصر المصفوفة في قيمة واحدة.
= true
```

# @lesson js-objects
title: الكائنات
summary: الخصائص، والوصول إليها، والدوال داخل الكائن، والمرور على الخصائص.
---
**الكائن** يجمع بيانات مترابطة على شكل «مفتاح: قيمة»:

```try javascript
const student = {
  name: "نور",
  age: 21,
  courses: ["HTML", "CSS"],
  greet() {
    return "أنا " + this.name;
  },
};

console.log(student.name);
console.log(student["age"]);
console.log(student.greet());
student.city = "جدة";          // إضافة خاصية
console.log(student);
```

## المرور على الخصائص

```try javascript
const product = { name: "قلم", price: 5, stock: 120 };
for (const [key, value] of Object.entries(product)) {
  console.log(key, "=", value);
}
console.log(Object.keys(product));
```

## مصفوفة كائنات

الشكل الأكثر شيوعًا للبيانات الحقيقية:

```try javascript
const users = [
  { name: "علي", active: true },
  { name: "منى", active: false },
  { name: "خالد", active: true },
];
const names = users.filter((u) => u.active).map((u) => u.name);
console.log(names);
```

```exercise javascript
? اطبع خاصية الاسم من الكائن
const car = { brand: "تويوتا" };
console.log(car.___);
= brand
```

```quiz
? كيف تصل لخاصية age في الكائن person؟
* person.age
- person->age
- person(age)

? يمكن أن يحتوي الكائن دوال.
= true
```

# @lesson js-dom
title: التحكم في الصفحة (DOM)
summary: اختيار العناصر وتغيير نصها وتنسيقها وإنشاء عناصر جديدة.
---
**DOM** هو تمثيل الصفحة ككائنات يمكن لـ JavaScript قراءتها وتغييرها.

## اختيار العناصر

```reference javascript
getElementById() | عنصر بمعرّفه | document.getElementById("title")
querySelector() | أول عنصر يطابق محدِّد CSS | document.querySelector(".card")
querySelectorAll() | كل العناصر المطابقة | document.querySelectorAll("li")
```

## التغيير

```try html
<h2 id="title">عنوان</h2>
<ul id="list"><li>أول</li></ul>
<script>
  const title = document.getElementById("title");
  title.textContent = "عنوان جديد";
  title.style.color = "#4338ca";
  title.classList.add("big");

  const li = document.createElement("li");
  li.textContent = "عنصر أضافته JavaScript";
  document.getElementById("list").append(li);
</script>
```

:::warning textContent أم innerHTML؟
`textContent` يضع نصًا عاديًا وهو آمن. `innerHTML` يفسّر النص كـ HTML؛ لا تستخدمه مع نص كتبه المستخدم لأنه قد يسمح بحقن كود ضار.
:::

```exercise javascript
? اختر أول عنصر له الصنف card
const card = document.___(".card");
= querySelector
```

```quiz
? أي دالة تعيد كل العناصر المطابقة لمحدِّد CSS؟
- getElementById()
- querySelector()
* querySelectorAll()

? وضع نص كتبه المستخدم في innerHTML آمن دائمًا.
= false
> قد يحتوي النص على كود ضار؛ استخدم textContent.
```

# @lesson js-events
title: الأحداث
summary: النقر والكتابة والإرسال، و addEventListener.
---
**الحدث** شيء يحدث في الصفحة: نقرة، كتابة، تمرير، إرسال نموذج… وتستجيب له JavaScript بدالة.

```try html
<button id="btn">اضغط</button>
<p id="count">0</p>
<script>
  let clicks = 0;
  document.getElementById("btn").addEventListener("click", () => {
    clicks++;
    document.getElementById("count").textContent = clicks;
  });
</script>
```

## حدث الكتابة

```try html
<input id="name" placeholder="اكتب اسمك">
<p id="hello"></p>
<script>
  document.getElementById("name").addEventListener("input", (e) => {
    document.getElementById("hello").textContent = "أهلًا " + e.target.value;
  });
</script>
```

## منع الإرسال الافتراضي للنموذج

```try html
<form id="f"><input name="q" required><button>بحث</button></form>
<p id="r"></p>
<script>
  document.getElementById("f").addEventListener("submit", (e) => {
    e.preventDefault();
    document.getElementById("r").textContent = "تبحث عن: " + e.target.q.value;
  });
</script>
```

```reference javascript
click | نقرة | btn.addEventListener("click", fn)
input | تغيّر قيمة حقل أثناء الكتابة | input.addEventListener("input", fn)
change | تغيّر قيمة بعد الانتهاء | select.addEventListener("change", fn)
submit | إرسال نموذج | form.addEventListener("submit", fn)
keydown | ضغط زر في لوحة المفاتيح | document.addEventListener("keydown", fn)
mouseover | مرور الفأرة | el.addEventListener("mouseover", fn)
```

```exercise javascript
? أكمل لربط دالة بحدث النقر
btn.addEventListener("___", () => console.log("نقرة"));
= click
```

```quiz
? أي دالة تمنع النموذج من إعادة تحميل الصفحة عند الإرسال؟
* e.preventDefault()
- e.stop()
- return false دائمًا

? الحدث input يحدث أثناء الكتابة في الحقل.
= true
```

# @lesson js-json
title: JSON
summary: تحويل الكائنات إلى نص والعكس.
---
**JSON** صيغة نصية لتبادل البيانات بين المتصفح والخادم، وتشبه كائنات JavaScript.

```try javascript
const user = { name: "سلمى", age: 30, skills: ["SQL", "Python"] };

const text = JSON.stringify(user);
console.log(text);
console.log(typeof text);

const back = JSON.parse(text);
console.log(back.skills[0]);
```

- `JSON.stringify()` يحوّل كائنًا إلى نص.
- `JSON.parse()` يحوّل نص JSON إلى كائن.

## قواعد JSON

- المفاتيح بين علامتي تنصيص مزدوجة: `"name"`.
- القيم: نص، رقم، `true`/`false`، `null`، مصفوفة، أو كائن.
- لا تعليقات ولا دوال ولا فاصلة زائدة في النهاية.

```try javascript
try {
  JSON.parse("{name: 'خطأ'}");
} catch (e) {
  console.log("JSON غير صحيح:", e.message);
}
```

```quiz
? أي دالة تحوّل نص JSON إلى كائن؟
- JSON.stringify()
* JSON.parse()
- JSON.toObject()

? في JSON تُكتب المفاتيح بين علامتي تنصيص مزدوجة.
= true
```

# @lesson js-errors
title: معالجة الأخطاء
summary: try و catch و finally، ورمي الأخطاء بـ throw.
---
بعض العمليات قد تفشل: بيانات غير صحيحة، شبكة مقطوعة… بدل أن يتوقف البرنامج، التقط الخطأ وتصرّف:

```try javascript
function divide(a, b) {
  if (b === 0) {
    throw new Error("لا يمكن القسمة على صفر");
  }
  return a / b;
}

try {
  console.log(divide(10, 2));
  console.log(divide(5, 0));
} catch (error) {
  console.log("حدث خطأ:", error.message);
} finally {
  console.log("انتهى");
}
```

- `try` الكود الذي قد يفشل.
- `catch` ما يحدث عند الخطأ.
- `finally` يُنفَّذ في الحالتين.
- `throw` ترمي خطأ بنفسك.

:::tip رسائل واضحة
اكتب في `throw new Error()` رسالة تشرح ما الخطأ وكيف يُصلح؛ ستشكر نفسك لاحقًا.
:::

```exercise javascript
? أكمل لالتقاط الخطأ
try {
  JSON.parse("{");
} ___ (e) {
  console.log("خطأ");
}
= catch
```

```quiz
? أي جزء يُنفَّذ سواء حدث خطأ أم لا؟
- try
- catch
* finally

? يمكنك رمي خطأ بنفسك باستخدام throw.
= true
```

# @lesson js-async
title: الكود غير المتزامن
summary: setTimeout، والوعود Promise، و async و await، و fetch.
---
بعض العمليات تأخذ وقتًا: انتظار مؤقت، أو طلب من الخادم. JavaScript لا تتوقف تنتظر؛ تكمل وتعود للنتيجة عندما تجهز.

## setTimeout

```try javascript
console.log("1: قبل");
setTimeout(() => console.log("3: بعد ثانية"), 1000);
console.log("2: مباشرة");
```

## الوعود و async/await

**Promise** وعد بنتيجة ستأتي لاحقًا. `await` تنتظر الوعد داخل دالة `async`:

```try javascript
function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function run() {
  console.log("بدأنا");
  await wait(500);
  console.log("بعد نصف ثانية");
  await wait(500);
  console.log("انتهينا");
}
run();
```

## جلب البيانات بـ fetch

```js
async function loadUsers() {
  try {
    const response = await fetch("https://example.com/api/users");
    const users = await response.json();
    console.log(users);
  } catch (e) {
    console.log("فشل الطلب:", e.message);
  }
}
```

:::info لماذا لا يعمل fetch هنا؟
محرر المنصة يشغّل الكود في صندوق معزول بلا إنترنت حفاظًا على الأمان. جرّب مثال `fetch` في صفحتك الخاصة.
:::

```exercise javascript
? أكمل لانتظار الوعد داخل الدالة
async function go() {
  ___ wait(100);
}
= await
```

```quiz
? بأي ترتيب يُطبع: console.log(1)، setTimeout(() => console.log(2), 0)، console.log(3)؟
- 1 ثم 2 ثم 3
* 1 ثم 3 ثم 2
- 2 ثم 1 ثم 3
> setTimeout ينتظر حتى ينتهي الكود الحالي، حتى لو كان التأخير 0.

? يمكن استخدام await داخل دالة async.
= true
```

# @lesson js-reference
title: مرجع JavaScript
summary: أهم الكلمات والدوال مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة أو دالة.

```reference javascript
let / const | تعريف متغير / ثابت | const x = 5;
if / else | شرط | if (x > 0) { … } else { … }
switch | اختيار من حالات | switch (v) { case 1: …; break; }
for | حلقة بعدّاد | for (let i = 0; i < 3; i++) { … }
for...of | المرور على العناصر | for (const x of arr) { … }
while | حلقة بشرط | while (n > 0) { n--; }
function | دالة | function f(a) { return a; }
=> | دالة سهمية | const f = (a) => a * 2;
return | إعادة قيمة | return total;
console.log() | طباعة | console.log("مرحبا");
typeof | نوع القيمة | typeof 42
=== | يساوي تمامًا | a === b
`${}` | قالب نصي | `مرحبا ${name}`
Array.push() | إضافة لمصفوفة | arr.push(1)
Array.map() | تحويل العناصر | arr.map(x => x * 2)
Array.filter() | تصفية | arr.filter(x => x > 0)
Array.reduce() | تجميع | arr.reduce((s, x) => s + x, 0)
Object.keys() | مفاتيح الكائن | Object.keys(obj)
JSON.stringify() | كائن إلى نص | JSON.stringify(obj)
JSON.parse() | نص إلى كائن | JSON.parse(text)
document.querySelector() | اختيار عنصر | document.querySelector("#id")
addEventListener() | الاستماع لحدث | btn.addEventListener("click", f)
textContent | نص العنصر | el.textContent = "نص"
classList.add() | إضافة صنف | el.classList.add("active")
try / catch | معالجة الأخطاء | try { … } catch (e) { … }
throw | رمي خطأ | throw new Error("…")
setTimeout() | تنفيذ بعد مدة | setTimeout(f, 1000)
async / await | انتظار وعد | const r = await fetch(url);
fetch() | طلب من الخادم | fetch("/api/data")
```

:::tip ماذا بعد؟
أنهيت أساسيات JavaScript. جرّب بناء مشروع صغير: قائمة مهام تضيف وتحذف العناصر، أو آلة حاسبة بسيطة.
:::
