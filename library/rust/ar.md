# @lesson rust-intro
title: مقدمة Rust
summary: ما هي Rust ولماذا هي آمنة وسريعة، وأول برنامج لك.
---
**Rust** لغة أنظمة: سريعة مثل C و C++، لكن المترجم يمنع عائلات كاملة من الأخطاء (المؤشرات المعلّقة وتعارض البيانات بين الخيوط) قبل أن يعمل البرنامج. تُستخدم في أدوات سطر الأوامر والمتصفحات وأنظمة التشغيل و WebAssembly والخوادم.

```try rust
fn main() {
    println!("Hello, Rust");
    println!("{}", 6 * 7);
}
```

- يبدأ البرنامج من `fn main()`.
- تنتهي `println!` بعلامة `!` لأنها **ماكرو** وليست دالة، و `{}` تُستبدل بالقيمة التالية.
- تنتهي الجمل بـ `;`.

:::info تشغيل الأمثلة
أمثلة Rust تعمل على خادم تشغيل منفصل وآمن؛ إن لم يكن مفعّلًا بعد فستعمل فور تفعيله. وعلى جهازك: ثبّت Rust عبر rustup ثم `cargo new hello` و `cargo run`.
:::

```quiz
? لماذا تنتهي println! بعلامة تعجب؟
* لأنها ماكرو
- لأنها تطبع بخط عريض
- لأنها خطأ

? تكتشف Rust كثيرًا من أخطاء الذاكرة وقت الترجمة.
= true
```

# @lesson rust-variables
title: المتغيرات والأنواع
summary: let و mut والتظليل والأنواع الأساسية.
---
المتغيرات **ثابتة** افتراضيًا. أضف `mut` عندما يجب أن تتغير القيمة.

```try rust
fn main() {
    let name = "Sara";
    let mut age = 25;          // mut: يمكن أن تتغير
    age += 1;
    let price: f64 = 19.99;    // نوع مكتوب صراحة
    let active = true;
    let letter = 'R';

    println!("Name: {}, age: {}", name, age);
    println!("Price with tax: {:.2}", price * 1.15);
    println!("{} {}", letter, active);

    let spaces = "   ";        // التظليل: متغير جديد بنفس الاسم
    let spaces = spaces.len();
    println!("{} spaces", spaces);

    let big: i64 = 3_000_000_000;
    let small = 255u8;
    println!("{} {}", big, small);
}
```

```reference rust
let x = 5 | متغير ثابت | let n = 1;
let mut x | متغير قابل للتغيير | let mut count = 0;
i32 / i64 / u8 / usize | أعداد صحيحة (بإشارة / بدون إشارة) | let i: usize = 0;
f64 | أعداد عشرية | let p: f64 = 2.5;
bool / char | صح/خطأ، حرف Unicode واحد | let c = 'ب';
&str / String | نص مستعار / نص مملوك | let s = String::from("hi");
{} / {:?} / {:.2} | عرض / تتبع / رقمان عشريان | println!("{:?}", v);
const | ثابت بنوع محدد | const MAX: u32 = 100;
```

:::tip الثبات هو الأصل
معظم القيم لا تتغير بعد إنشائها. جعل التغيير صريحًا بـ `mut` يُظهر لك وللمترجم بسرعة أين تتغير الحالة.
:::

```exercise rust
? اجعل count متغيرًا يمكن تغييره
let ___ count = 0;
= mut
```

```quiz
? ماذا يحدث إذا أسندت قيمة لمتغير عُرّف بدون mut؟
* لا يُترجم البرنامج
- تتغير القيمة على أي حال
- تصبح صفرًا

? التظليل يسمح بتعريف متغير جديد بنفس الاسم.
= true
```

# @lesson rust-control
title: الشروط والحلقات
summary: if كتعبير، و loop و while و for والنطاقات.
---
```try rust
fn main() {
    let score = 78;
    let grade = if score >= 90 { "A" } else if score >= 70 { "B" } else { "C" };
    println!("grade {}", grade);

    for i in 1..=3 {
        println!("Round {}", i);
    }
    for i in (0..10).step_by(5) {
        print!("{} ", i);
    }
    println!();

    let mut n = 3;
    while n > 0 {
        print!("{} ", n);
        n -= 1;
    }
    println!("go!");

    let mut tries = 0;
    let found = loop {
        tries += 1;
        if tries * tries > 50 {
            break tries;        // يمكن أن ترجع loop قيمة
        }
    };
    println!("first square above 50: {}^2", found);
}
```

```reference rust
if c { } else { } | شرط (بدون أقواس) | if x > 0 { }
let v = if c { a } else { b } | if كتعبير | let m = if a > b { a } else { b };
loop | كرر حتى break | loop { break; }
while c | كرر ما دام الشرط صحيحًا | while n > 0 { }
for x in a..b | نطاق بدون b | for i in 0..5
a..=b | نطاق يشمل b | for i in 1..=3
break / continue | اخرج / تخطَّ الدورة | break value;
```

:::warning يجب أن يكون الشرط bool
`if 1 { }` لا تُترجم. لا تعامل Rust الرقم كصح أو خطأ أبدًا؛ اكتب `if n != 0`.
:::

```exercise rust
? كرر من 1 إلى 5 شاملًا 5
for i in 1___5 { println!("{}", i); }
= ..=
```

```quiz
? أي حلقة يمكنها إرجاع قيمة مع break؟
* loop
- for
- while
```

# @lesson rust-functions
title: الدوال
summary: المعاملات وأنواع الإرجاع والتعبيرات و closures.
---
```try rust
fn square(n: i32) -> i32 {
    n * n                    // بدون فاصلة منقوطة: هذه قيمة الإرجاع
}

fn divide(a: f64, b: f64) -> f64 {
    if b == 0.0 {
        return 0.0;          // إرجاع مبكر
    }
    a / b
}

fn greet(name: &str) {
    println!("Hello, {}!", name);
}

fn main() {
    println!("{}", square(7));
    println!("{}", divide(10.0, 4.0));
    greet("Sara");

    let tax = 0.15;
    let with_tax = |price: f64| price * (1.0 + tax);   // closure ترى tax
    println!("{:.2}", with_tax(100.0));

    let nums = vec![1, 2, 3, 4];
    let doubled: Vec<i32> = nums.iter().map(|n| n * 2).collect();
    println!("{:?}", doubled);
}
```

```reference rust
fn f(a: i32) -> i32 | دالة بأنواع | fn add(a: i32, b: i32) -> i32
آخر تعبير | القيمة المرجعة (بدون ;) | fn one() -> i32 { 1 }
return x; | إرجاع مبكر | if bad { return 0; }
() | Unit: "لا قيمة" | fn log(m: &str) { }
|x| expr | closure | let inc = |x| x + 1;
```

:::tip التعبيرات والجمل
السطر الذي ينتهي بـ `;` جملة لا ترجع شيئًا. وآخر سطر في الكتلة **بدون** `;` هو قيمتها. إضافة `;` زائدة بعد `n * n` تجعل الدالة ترجع `()` فيعترض المترجم.
:::

```exercise rust
? اكتب الكلمة التي تعرّف دالة
___ cube(n: i32) -> i32 { n * n * n }
= fn
```

```quiz
? ماذا ترجع الدالة إذا كان آخر سطر فيها n * n بدون فاصلة منقوطة؟
* قيمة n * n
- لا شيء
- خطأ

? يجب أن تكون لمعاملات الدوال في Rust أنواع.
= true
```

# @lesson rust-ownership
title: الملكية والنقل
summary: لكل قيمة مالك واحد؛ النقل والنسخ.
---
الملكية هي الفكرة الأساسية في Rust:

1. لكل قيمة **مالك** واحد بالضبط.
2. عندما يخرج المالك من نطاقه تُحرَّر القيمة (بدون جامع قمامة).
3. الإسناد أو التمرير **ينقل** القيمة، ولا يمكن استخدام الاسم القديم بعدها.

```try rust
fn take(s: String) {
    println!("took {}", s);
}                              // تُحرَّر s هنا

fn main() {
    let a = String::from("hello");
    let b = a;                 // ينتقل النص من a إلى b
    // println!("{}", a);      // لن يُترجم: a نُقلت
    println!("{}", b);

    let c = b.clone();         // نسخة حقيقية من النص
    take(b);                   // تنتقل b إلى الدالة
    println!("still have {}", c);

    let x = 5;
    let y = x;                 // الأرقام البسيطة Copy: يبقى الاثنان صالحين
    println!("{} {}", x, y);
}
```

```reference rust
let b = a; | نقل: لم تعد a صالحة | let v2 = v1;
.clone() | نسخ كامل صريح | let s2 = s1.clone();
أنواع Copy | الأعداد و bool و char: تُنسخ ولا تُنقل | let y = x;
نهاية النطاق | تُحذف قيمة المالك | { let s = String::new(); }
```

:::tip لماذا يهم هذا؟
لأن مالكًا واحدًا فقط يحرّر كل قيمة، لا يوجد في Rust تحرير مزدوج ولا استخدام لذاكرة محرّرة، ولا تحتاج جامع قمامة لتحقيق ذلك.
:::

```exercise rust
? انسخ name نسخة كاملة ليمكن استخدام الاثنين
let copy = name.___();
= clone
```

```quiz
? بعد let b = a; حيث a من نوع String، ماذا يحدث لـ a؟
* تُنقل ولا يمكن استخدامها
- تحتفظ بنسخة
- تصبح فارغة لكن صالحة

? الأعداد الصحيحة تُنسخ ولا تُنقل عند الإسناد.
= true
```

# @lesson rust-borrowing
title: المراجع والاستعارة
summary: & و &mut وقواعد الاستعارة.
---
بدل نقل القيمة يمكنك **استعارتها** بمرجع، ويبقى المالك محتفظًا بها.

```try rust
fn length(s: &String) -> usize {     // يستعير ولا يأخذ
    s.len()
}

fn shout(s: &mut String) {            // استعارة قابلة للتغيير
    s.push_str("!");
}

fn first_word(text: &str) -> &str {
    match text.find(' ') {
        Some(i) => &text[..i],
        None => text,
    }
}

fn main() {
    let mut greeting = String::from("hello world");
    println!("{} has {} bytes", greeting, length(&greeting));
    shout(&mut greeting);
    println!("{}", greeting);
    println!("first word: {}", first_word(&greeting));

    let r1 = &greeting;
    let r2 = &greeting;          // استعارات مشتركة كثيرة مسموحة
    println!("{} {}", r1, r2);
}
```

القواعد التي يتحقق منها المترجم:

- في أي لحظة يمكنك امتلاك **إما** مراجع مشتركة كثيرة `&T` **أو** مرجع واحد قابل للتغيير `&mut T`، وليس الاثنين معًا.
- لا يمكن أن يعيش المرجع أطول من القيمة التي يشير إليها.

```reference rust
&x | استعارة مشتركة (للقراءة) | length(&s)
&mut x | استعارة قابلة للتغيير | push(&mut v)
&str | شريحة نص مستعارة | fn f(s: &str)
&v[a..b] | شريحة من متجه أو نص | &nums[1..3]
*r | القيمة خلف المرجع | *count += 1;
```

:::tip اقبل &str لا &String
الدالة التي تقرأ النص فقط يجب أن تقبل `&str`؛ فتعمل مع النصوص الحرفية ومع قيم `String` معًا.
:::

```exercise rust
? مرّر استعارة قابلة للتغيير لـ list إلى الدالة
add_item(___ list);
= &mut
```

```quiz
? أي تركيبة يسمح بها مدقق الاستعارة في نفس الوقت؟
* عدة مراجع مشتركة
- مرجع مشترك ومرجع قابل للتغيير
- مرجعان قابلان للتغيير
```

# @lesson rust-structs
title: الهياكل والدوال المرتبطة
summary: تعريف أنواع البيانات، وكتل impl، و derive.
---
```try rust
#[derive(Debug, Clone, PartialEq)]
struct Product {
    name: String,
    price: f64,
    stock: u32,
}

impl Product {
    fn new(name: &str, price: f64) -> Product {     // دالة مرتبطة
        Product { name: name.to_string(), price, stock: 0 }
    }

    fn total_value(&self) -> f64 {                   // تقرأ self
        self.price * self.stock as f64
    }

    fn restock(&mut self, qty: u32) {                // تغيّر self
        self.stock += qty;
    }
}

fn main() {
    let mut tea = Product::new("Tea", 12.5);
    tea.restock(10);
    println!("{}: {:.2}", tea.name, tea.total_value());
    println!("{:?}", tea);

    let copy = tea.clone();
    println!("{}", copy == tea);

    let cake = Product { name: String::from("Cake"), ..tea };   // صيغة التحديث
    println!("{} {}", cake.name, cake.stock);
}
```

```reference rust
struct S { a: T } | تعريف هيكل | struct Point { x: i32, y: i32 }
S { a: v } | إنشاء قيمة منه | Point { x: 1, y: 2 }
impl S { } | دوال الهيكل S | impl Point { fn len(&self) -> f64 { } }
&self / &mut self | قراءة / تغيير الكائن | fn reset(&mut self)
S::new() | دالة مرتبطة (المُنشئ حسب العرف) | Product::new("Tea", 1.0)
#[derive(Debug)] | توليد كود (طباعة، نسخ، مقارنة) | #[derive(Debug, Clone)]
```

```exercise rust
? اطبع الهيكل بتنسيق التتبع
println!("___", tea);
= {:?}
```

```quiz
? أي مستقبِل يسمح للدالة بتغيير الكائن؟
* &mut self
- &self
- self: const

? تسمح #[derive(Debug)] بطباعة الهيكل باستخدام {:?}.
= true
```

# @lesson rust-enums
title: التعدادات و Option و match
summary: تعدادات تحمل بيانات، ومطابقة الأنماط، و Option بدل null.
---
لا يوجد `null` في Rust. القيمة التي قد تكون غائبة نوعها `Option<T>`: إما `Some(value)` أو `None`.

```try rust
enum Shape {
    Circle(f64),
    Rect { w: f64, h: f64 },
    Point,
}

fn area(s: &Shape) -> f64 {
    match s {
        Shape::Circle(r) => 3.14159 * r * r,
        Shape::Rect { w, h } => w * h,
        Shape::Point => 0.0,
    }
}

fn find_price(item: &str) -> Option<f64> {
    match item {
        "tea" => Some(12.5),
        "coffee" => Some(20.0),
        _ => None,
    }
}

fn main() {
    let shapes = vec![Shape::Circle(1.0), Shape::Rect { w: 2.0, h: 3.0 }, Shape::Point];
    for s in &shapes {
        println!("{:.2}", area(s));
    }

    for item in &["tea", "water"] {
        match find_price(item) {
            Some(p) => println!("{} costs {}", item, p),
            None => println!("{} not found", item),
        }
    }

    if let Some(p) = find_price("coffee") {
        println!("coffee: {}", p);
    }
    println!("{}", find_price("juice").unwrap_or(0.0));

    let n = 7;
    let kind = match n {
        0 => "zero",
        1..=9 => "one digit",
        _ => "big",
    };
    println!("{}", kind);
}
```

```reference rust
enum E { A, B(T) } | تعداد، وقد تحمل حالاته بيانات | enum Msg { Quit, Move(i32, i32) }
match x { p => v } | مطابقة الأنماط (يجب أن تغطي كل الحالات) | match n { 0 => "z", _ => "?" }
_ | أي قيمة أخرى | _ => println!("other")
Option<T> | Some(value) أو None | let p: Option<i32> = None;
if let Some(x) = v | التصرف مع نمط واحد فقط | if let Some(u) = user { }
unwrap_or(d) | القيمة أو قيمة افتراضية | opt.unwrap_or(0)
```

:::warning احذر من unwrap()
توقف `opt.unwrap()` البرنامج (panic) إذا كانت القيمة `None`. فضّل `match` أو `if let` أو `unwrap_or`.
:::

```exercise rust
? اكتب قيمة "لا قيمة" في Option
let missing: Option<i32> = ___;
= None
```

```quiz
? ماذا يحدث إذا لم تغطِّ match كل القيم الممكنة؟
* لا يُترجم البرنامج
- تُتجاهل الحالات الناقصة
- ترجع null

? يمثّل Option<T> في Rust القيمة التي قد تكون غائبة.
= true
```

# @lesson rust-collections
title: المتجهات والنصوص والخرائط
summary: Vec و String و HashMap والمكررات.
---
```try rust
use std::collections::HashMap;

fn main() {
    let mut nums = vec![5, 3, 8, 1];
    nums.push(4);
    nums.sort();
    println!("{:?} len {}", nums, nums.len());
    println!("first {} last {:?}", nums[0], nums.last());

    let total: i32 = nums.iter().sum();
    let evens: Vec<i32> = nums.iter().filter(|n| *n % 2 == 0).cloned().collect();
    println!("total {} evens {:?}", total, evens);
    println!("max {:?}", nums.iter().max());

    let mut text = String::from("Hello");
    text.push_str(", Rust");
    println!("{} ({} bytes)", text, text.len());
    println!("{}", text.to_uppercase());
    let words: Vec<&str> = "a,b,c".split(',').collect();
    println!("{:?}", words);
    println!("{} chars in مرحبا", "مرحبا".chars().count());

    let mut stock: HashMap<&str, u32> = HashMap::new();
    stock.insert("tea", 10);
    stock.insert("cake", 3);
    *stock.entry("tea").or_insert(0) += 5;
    if let Some(n) = stock.get("tea") {
        println!("tea: {}", n);
    }
    println!("has juice: {}", stock.contains_key("juice"));

    let text = "the cat and the hat";
    let mut counts = HashMap::new();
    for w in text.split_whitespace() {
        *counts.entry(w).or_insert(0) += 1;
    }
    println!("the = {}", counts["the"]);
}
```

```reference rust
vec![..] / Vec::new() | إنشاء متجه | let mut v = Vec::new();
push / pop / len | إضافة / حذف الأخير / الحجم | v.push(1);
.iter().map().filter() | سلسلة مكررات | v.iter().map(|x| x * 2)
.collect() | بناء مجموعة من مكرر | let v: Vec<_> = it.collect();
String::from / push_str | نص مملوك قابل للنمو | s.push_str("!");
.chars().count() | عدّ الحروف (لا البايتات) | "عربي".chars().count()
HashMap::new / insert / get | خريطة مفتاح وقيمة | m.get("tea")
entry().or_insert() | أضف إن لم يوجد ثم حدّث | *m.entry(k).or_insert(0) += 1;
```

:::tip تعدّ len() البايتات
ترجع `String::len()` عدد البايتات، والحرف العربي يأخذ بايتين. استخدم `.chars().count()` لعدّ الحروف.
:::

```exercise rust
? حوّل المكرر إلى متجه
let v: Vec<i32> = nums.iter().map(|x| x + 1).___();
= collect
```

```quiz
? ماذا ترجع HashMap::get؟
* Option فيه القيمة أو None
- القيمة أو صفرًا
- Result
```

# @lesson rust-errors
title: معالجة الأخطاء مع Result
summary: Result و match والعامل ? و panic.
---
الأخطاء المتوقعة (ملف غير موجود، مدخلات خاطئة) تُرجع كـ `Result<T, E>`: إما `Ok(value)` أو `Err(error)`.

```try rust
use std::num::ParseIntError;

fn parse_age(text: &str) -> Result<u32, String> {
    let n: u32 = match text.trim().parse() {
        Ok(n) => n,
        Err(_) => return Err(format!("'{}' is not a number", text)),
    };
    if n > 150 {
        return Err(String::from("age is too large"));
    }
    Ok(n)
}

fn sum_two(a: &str, b: &str) -> Result<i32, ParseIntError> {
    let x: i32 = a.parse()?;     // ? ترجع الخطأ مبكرًا
    let y: i32 = b.parse()?;
    Ok(x + y)
}

fn main() {
    for input in &["25", "abc", "200"] {
        match parse_age(input) {
            Ok(age) => println!("age {}", age),
            Err(e) => println!("error: {}", e),
        }
    }
    println!("{:?}", sum_two("4", "5"));
    println!("{:?}", sum_two("4", "x").is_err());
    println!("{}", parse_age("x").unwrap_or(0));
}
```

```reference rust
Result<T, E> | Ok(value) أو Err(error) | fn load() -> Result<String, io::Error>
Ok(v) / Err(e) | بناء نتيجة | return Err("bad".to_string());
? | أرجع الخطأ مبكرًا أو خذ القيمة | let n = s.parse::<i32>()?;
match r { Ok(v) => .., Err(e) => .. } | التعامل مع الحالتين | match open(p) { .. }
unwrap_or / expect | قيمة افتراضية / توقف برسالة | r.expect("config missing")
panic!() | إيقاف البرنامج لخلل لا يُفترض حدوثه | panic!("bad state");
```

:::tip Result للأخطاء المتوقعة و panic للأخطاء البرمجية
أرجع `Result` حين يستطيع المستدعي فعل شيء بشأن الخطأ. واستخدم `panic!` فقط حين لا يكون للاستمرار معنى، مثل كسر شرط يجب أن يبقى صحيحًا دائمًا.
:::

```exercise rust
? أرجع خطأ التحويل مبكرًا بحرف واحد
let n: i32 = text.parse()___;
= ?
```

```quiz
? ماذا يفعل العامل ? مع قيمة Err؟
* يرجع الخطأ من الدالة الحالية
- يتجاهله
- يحوّله إلى صفر

? للنوع Result حالتان: Ok و Err.
= true
```

# @lesson rust-traits
title: السمات والأنواع العامة
summary: سلوك مشترك عبر traits، ودوال عامة، وقيود السمات.
---
**السمة (trait)** تصف سلوكًا تشترك فيه عدة أنواع، مثل الواجهة في لغات أخرى.

```try rust
use std::fmt;

trait Shape {
    fn area(&self) -> f64;
    fn describe(&self) -> String {               // دالة افتراضية
        format!("shape with area {:.2}", self.area())
    }
}

struct Circle { r: f64 }
struct Square { side: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { 3.14159 * self.r * self.r }
}
impl Shape for Square {
    fn area(&self) -> f64 { self.side * self.side }
    fn describe(&self) -> String { format!("square {}x{}", self.side, self.side) }
}

impl fmt::Display for Square {                   // تسمح لـ {} بطباعة Square
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.side)
    }
}

fn largest<T: PartialOrd + Copy>(items: &[T]) -> T {   // دالة عامة
    let mut best = items[0];
    for &item in items {
        if item > best {
            best = item;
        }
    }
    best
}

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Circle { r: 1.0 }), Box::new(Square { side: 2.0 })];
    for s in &shapes {
        println!("{}", s.describe());
    }
    println!("{}", Square { side: 3.0 });
    println!("{} {}", largest(&[3, 9, 4]), largest(&[1.5, 0.5]));
}
```

```reference rust
trait T { fn f(&self); } | تعريف سمة | trait Speak { fn speak(&self) -> String; }
impl T for S | تنفيذها لنوع | impl Speak for Dog { .. }
fn f<T: Trait>(x: T) | دالة عامة بقيد سمة | fn show<T: Display>(x: T)
&dyn Trait / Box<dyn Trait> | أي نوع ينفّذ السمة | Vec<Box<dyn Shape>>
Display / Debug | الطباعة بـ {} / {:?} | impl fmt::Display for P
PartialOrd / Copy / Clone | سمات قياسية شائعة | #[derive(Clone, Copy)]
```

```exercise rust
? نفّذ السمة Shape للنوع Triangle
impl Shape ___ Triangle { fn area(&self) -> f64 { 0.0 } }
= for
```

```quiz
? ما هي السمة (trait) في Rust؟
* مجموعة دوال يمكن للأنواع تنفيذها
- نوع من الحلقات
- عنوان في الذاكرة
```

# @lesson rust-reference
title: مرجع Rust السريع
summary: أكثر الصيغ استخدامًا في صفحة واحدة.
---
```reference rust
fn main() | نقطة البداية | fn main() { }
let / let mut | متغير / متغير قابل للتغيير | let mut n = 0;
println!("{} {:?}", a, b) | طباعة منسقة | println!("{:.2}", x);
if / loop / while / for | التحكم في التدفق | for i in 0..n { }
fn f(x: i32) -> i32 | دالة | fn sq(x: i32) -> i32 { x * x }
|x| ... | closure | v.iter().map(|x| x + 1)
String / &str | نص مملوك / مستعار | let s: &str = "hi";
&x / &mut x | الاستعارة | change(&mut v);
struct / impl | البيانات والدوال | impl P { fn new() -> P { .. } }
enum / match | الحالات ومطابقة الأنماط | match o { Some(x) => x, None => 0 }
Option / Result | القيم الغائبة / الأخطاء | let n = s.parse::<i32>()?;
Vec / HashMap | المجموعات | let mut m = HashMap::new();
trait / impl Trait for T | السلوك المشترك | impl Display for P
```

:::tip الخطوة التالية
استخدم `cargo new` لبناء أداة سطر أوامر صغيرة، مثل عدّاد كلمات يقرأ ملفًا ويطبع أكثر الكلمات تكرارًا باستخدام `HashMap`. بعدها اقرأ عن الوحدات (modules) والمكتبات في crates.io والخيوط.
:::

```quiz
? أي نوع تستخدمه Rust بدل null للقيمة التي قد تكون غائبة؟
* Option
- Result
- Box
```
