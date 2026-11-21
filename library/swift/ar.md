# @lesson swift-intro
title: مقدمة Swift
summary: ما هي Swift وأين تُستخدم، وأول برنامج لك.
---
**Swift** لغة Apple الحديثة لتطبيقات iPhone و iPad و Mac و Apple Watch و Apple TV. سريعة وآمنة وسهلة القراءة، وتعمل أيضًا على خوادم Linux. وقد حلّت محل Objective-C كلغة أساسية لمنصات Apple.

```try swift
print("Hello, Swift")
print(6 * 7)
let name = "Sara"
print("Welcome, \(name)!")
```

- يعمل ملف Swift من الأعلى، ولا حاجة لكتابة دالة `main` في البرامج الصغيرة.
- `print` تكتب سطرًا، ولا حاجة للفاصلة المنقوطة.
- `\(...)` تضع قيمة داخل نص (إدراج القيم في النص).

:::info تشغيل الأمثلة
أمثلة Swift تعمل على خادم تشغيل منفصل وآمن. وعلى Mac ثبّت Xcode وجرّب الكود في Playground، وعلى Linux أو Windows ثبّت Swift من swift.org وشغّل `swift main.swift`.
:::

```quiz
? فيمَ تُستخدم Swift أساسًا؟
* تطبيقات أجهزة Apple مثل iPhone و Mac
- قواعد البيانات
- معادلات الجداول الحسابية

? في Swift يدرج "\(name)" قيمة name داخل النص.
= true
```

# @lesson swift-variables
title: الثوابت والمتغيرات والأنواع
summary: let و var واستنتاج النوع والأنواع الأساسية والتحويل بينها.
---
```try swift
let company = "VintraXo"        // let: ثابت لا يتغير
var employees = 120             // var: متغير
employees += 5
let price: Double = 19.99       // نوع مكتوب صراحة
let isOpen = true
let initial: Character = "V"

print(company, employees, isOpen, initial)
print("Price with tax:", price * 1.14)

let age = 25
let message = "Age: " + String(age)      // تحويل Int إلى String
let text = "42"
let number = Int(text) ?? 0              // قد تفشل Int(...)، فتعطي ?? قيمة بديلة
print(message, number + 1)
print(type(of: price), type(of: employees))
```

```reference swift
let x = 5 | ثابت | let pi = 3.14
var x = 5 | متغير | var count = 0
Int / Double / Bool / String / Character | الأنواع الأساسية | let n: Int = 3
"\(value)" | إدراج قيمة في نص | "Total: \(total)"
String(x) / Int("42") / Double("2.5") | التحويل (Int("x") ترجع nil) | Int("12") ?? 0
type(of: x) | نوع القيمة | type(of: 3.5)
```

:::tip فضّل let
استخدم `let` ما لم تكن القيمة تحتاج للتغير فعلًا. والمترجم ينبهك عندما لا يتغير متغير `var` أبدًا.
:::

```exercise swift
? عرّف ثابتًا اسمه city
___ city = "Cairo"
= let
```

```quiz
? ما الفرق بين let و var؟
* لا يمكن تغيير let بعد تعيينه، ويمكن مع var
- الكلمة var أسرع
- الكلمة let للأرقام فقط
```

# @lesson swift-optionals
title: القيم الاختيارية (Optionals)
summary: القيم التي قد تكون غائبة، و if let و guard let والعامل ??.
---
في Swift لا يمكن أن يكون المتغير العادي فارغًا أبدًا. والقيمة التي قد تغيب لها نوع **اختياري** يُكتب بـ `?`: النوع `String?` يعني "نص أو لا شيء (`nil`)".

```try swift
let input = "42x"
let parsed: Int? = Int(input)            // nil لأن "42x" ليس رقمًا
print(parsed as Any)

var email: String? = nil
print(email ?? "no email")               // قيمة بديلة عند nil

email = "sara@example.com"
if let address = email {                 // فك القيمة بأمان
    print("Send to \(address), \(address.count) characters")
}

func greet(_ name: String?) {
    guard let name = name else {         // اخرج مبكرًا عند غيابها
        print("Hello, guest")
        return
    }
    print("Hello, \(name)")
}
greet(nil)
greet("Omar")

let length = email?.count                // الوصول الاختياري: Int?
print(length ?? 0)
```

```reference swift
T? | نوع اختياري: قيمة أو nil | var phone: String?
?? | قيمة بديلة عند nil | name ?? "guest"
if let x = optional | تنفيذ الكود فقط عند وجود قيمة | if let n = Int(s) { }
guard let x = optional else { return } | الخروج المبكر عند nil | guard let id = id else { return }
a?.b | الوصول الاختياري المتسلسل | user?.email?.count
x! | فك إجباري (يتعطل عند nil) | تجنّبه
```

:::warning تجنّب الفك الإجباري
`value!` يوقف التطبيق إذا كانت القيمة `nil`. استخدم `if let` أو `guard let` أو `??` بدلًا منه.
:::

```exercise swift
? أعطِ "guest" إذا كانت name تساوي nil
let shown = name ___ "guest"
= ??
```

```quiz
? ماذا ترجع Int("abc")؟
* nil
- 0
- خطأ يوقف البرنامج

? يمكن لمتغير من نوع String (بلا ?) أن يحمل nil.
= false
```

# @lesson swift-control
title: الشروط و switch
summary: if و else و switch مع النطاقات والصفوف (tuples) و where.
---
```try swift
let score = 78
if score >= 90 {
    print("Excellent")
} else if score >= 70 {
    print("Good")
} else {
    print("Keep practising")
}

let grade: String
switch score {                          // يجب أن يغطي switch كل الحالات
case 90...100: grade = "A"
case 75..<90: grade = "B"
case 60..<75: grade = "C"
default: grade = "F"
}
print("grade", grade)

let day = "fri"
switch day {
case "fri", "sat":
    print("Weekend")
default:
    print("Working day")
}

let point = (3, 0)
switch point {
case (0, 0): print("origin")
case (_, 0): print("on the x axis")
case let (x, y) where x == y: print("diagonal")
default: print("somewhere else")
}
```

```reference swift
if / else if / else | الشروط (بلا أقواس) | if x > 0 { }
switch value { case ...: } | الاختيار حسب القيمة، ويجب أن يغطي كل الحالات | switch n { case 1: ... default: ... }
a...b / a..<b | نطاق مغلق / نصف مفتوح | case 90...100:
case "a", "b": | عدة قيم في حالة واحدة | case "fri", "sat":
case let x where cond: | نمط بشرط | case let (x, y) where x == y:
```

:::tip لا انتقال تلقائي بين الحالات
في Swift لا تنتقل الحالة `case` إلى التي تليها، فلا تحتاج `break` في نهاية كل حالة.
:::

```exercise swift
? طابق الأرقام من 1 إلى 9 شاملة
case 1___9: print("one digit")
= ...
```

```quiz
? ماذا يحدث إذا لم يغطِّ switch كل القيم الممكنة؟
* لا يُترجم الكود
- تُتجاهل القيم الناقصة
- يرجع nil
```

# @lesson swift-loops
title: الحلقات
summary: for-in مع النطاقات والمصفوفات والقواميس، و while و repeat-while.
---
```try swift
for i in 1...3 {
    print("Round \(i)")
}
for i in stride(from: 10, through: 0, by: -5) {
    print(i, terminator: " ")
}
print()

let fruits = ["apple", "banana", "cherry"]
for (index, fruit) in fruits.enumerated() {
    print(index, fruit)
}

let stock = ["tea": 10, "cake": 3]
for (item, count) in stock.sorted(by: { $0.key < $1.key }) {
    print("\(item): \(count)")
}

var n = 3
while n > 0 {
    print(n, terminator: " ")
    n -= 1
}
print("go!")

var attempts = 0
repeat {
    attempts += 1
} while attempts < 3
print("attempts:", attempts)
```

```reference swift
for i in 1...n | المرور على نطاق | for i in 0..<count
for x in array | كل عنصر | for name in names
.enumerated() | الرقم والعنصر | for (i, x) in list.enumerated()
stride(from:to:by:) | خطوات، وتعمل للخلف أيضًا | stride(from: 10, to: 0, by: -2)
while / repeat-while | كرر ما دام الشرط صحيحًا / مرة واحدة على الأقل | repeat { } while x
break / continue | اخرج / تخطَّ | if x < 0 { continue }
```

```exercise swift
? كرر من 0 حتى 5 بدون 5
for i in 0___5 { print(i) }
= ..<
```

```quiz
? أي حلقة تنفذ جسمها مرة واحدة على الأقل دائمًا؟
* repeat-while
- while
- for-in
```

# @lesson swift-collections
title: المصفوفات والقواميس والمجموعات
summary: إنشاء المجموعات وتعديلها، و map و filter و reduce و sorted.
---
```try swift
var prices = [12.5, 20, 35, 8]
prices.append(15)
print(prices.count, prices[0], prices.max() ?? 0)
print(prices.sorted())
print(prices.filter { $0 > 10 })
print(prices.map { $0 * 1.14 }.map { ($0 * 100).rounded() / 100 })
print(prices.reduce(0, +))

var phoneBook = ["Sara": "0100-111", "Omar": "0122-222"]
phoneBook["Lina"] = "0111-333"
print(phoneBook["Omar"] ?? "unknown")
print(phoneBook["Ali"] ?? "not found")         // المفتاح غير الموجود يعطي nil
print(phoneBook.keys.sorted())

var tags: Set = ["swift", "ios", "swift"]
tags.insert("mobile")
print(tags.count, tags.contains("ios"))

let words = ["apple", "avocado", "banana"]
let grouped = Dictionary(grouping: words, by: { $0.first! })
print(grouped.keys.sorted())
```

```reference swift
[a, b, c] / append / count | المصفوفات | var list = [1, 2]; list.append(3)
[key: value] / dict[key] | القواميس (القراءة ترجع قيمة اختيارية) | ages["Sara"] ?? 0
Set | قيم بلا تكرار | var s: Set = [1, 2, 2]
map / filter / reduce | تحويل، وإبقاء، ودمج | nums.map { $0 * 2 }
sorted() / sorted(by:) | نسخة مرتبة | users.sorted { $0.age < $1.age }
$0 / $1 | معاملات مختصرة في الـ closure | list.filter { $0 > 0 }
```

:::tip المصفوفات قيم
إسناد مصفوفة إلى متغير آخر ينشئ نسخة، وتغيير النسخة لا يغيّر الأصل، وهذا يمنع أخطاء مفاجئة كثيرة.
:::

```exercise swift
? أبقِ الأرقام الزوجية فقط
let evens = numbers.___ { $0 % 2 == 0 }
= filter
```

```quiz
? ماذا ترجع قراءة مفتاح غير موجود من قاموس؟
* nil
- 0
- نصًا فارغًا
```

# @lesson swift-functions
title: الدوال و Closures
summary: تسميات المعاملات، والقيم الافتراضية، وإرجاع عدة قيم، والـ closures.
---
```try swift
func greet(person name: String, greeting: String = "Hello") -> String {
    return "\(greeting), \(name)!"
}
print(greet(person: "Sara"))
print(greet(person: "Omar", greeting: "Welcome"))

func square(_ n: Int) -> Int { n * n }      // _ تعني بلا تسمية عند الاستدعاء
print(square(7))

func minMax(_ values: [Int]) -> (min: Int, max: Int)? {
    guard let first = values.first else { return nil }
    var low = first, high = first
    for v in values {
        low = min(low, v)
        high = max(high, v)
    }
    return (low, high)
}
if let range = minMax([5, 3, 9, 1]) {
    print("min \(range.min), max \(range.max)")
}

let withTax = { (price: Double) -> Double in price * 1.14 }
print(withTax(100))

func apply(_ values: [Int], _ transform: (Int) -> Int) -> [Int] {
    values.map(transform)
}
print(apply([1, 2, 3]) { $0 * 10 })           // closure لاحقة
```

```reference swift
func f(label name: T) -> R | دالة بتسمية للمعامل | func move(to point: Point)
_ name | بلا تسمية عند الاستدعاء | func square(_ n: Int)
name: T = value | قيمة افتراضية | greeting: String = "Hi"
-> (a: T, b: U) | إرجاع عدة قيم (tuple) | return (min, max)
{ (x: T) -> R in ... } | closure | let double = { (x: Int) in x * 2 }
f(x) { ... } | closure لاحقة | list.sorted { $0 < $1 }
```

```exercise swift
? اكتب الكلمة التي تعرّف دالة
___ double(_ x: Int) -> Int { x * 2 }
= func
```

```quiz
? لماذا تستخدم Swift تسميات المعاملات مثل greet(person: "Sara")؟
* لأنها تجعل الاستدعاء مقروءًا كجملة وأوضح
- لأن المترجم يشترطها للسرعة
- لأنها تحل محل نوع الإرجاع
```

# @lesson swift-structs-classes
title: الهياكل والأصناف
summary: الخصائص والدوال والمُنشئات و mutating والوراثة، والقيمة مقابل المرجع.
---
```try swift
struct Point {
    var x: Double
    var y: Double
    func distance(to other: Point) -> Double {
        ((x - other.x) * (x - other.x) + (y - other.y) * (y - other.y)).squareRoot()
    }
    mutating func move(dx: Double) { x += dx }     // تغيّر الهيكل نفسه
}

var a = Point(x: 0, y: 0)
let b = Point(x: 3, y: 4)
print(a.distance(to: b))
var c = a                                          // الهياكل تُنسخ
c.move(dx: 10)
print(a.x, c.x)

class Account {
    let owner: String
    private(set) var balance = 0.0                 // تُقرأ من الخارج وتتغير من الداخل فقط
    init(owner: String) { self.owner = owner }
    func deposit(_ amount: Double) {
        guard amount > 0 else { return }
        balance += amount
    }
}
class SavingsAccount: Account {
    func addInterest(rate: Double) { deposit(balance * rate) }
}

let acc = SavingsAccount(owner: "Sara")
let same = acc                                     // الأصناف مراجع مشتركة
same.deposit(1000)
acc.addInterest(rate: 0.05)
print(acc.owner, acc.balance, same.balance)
```

| | Struct | Class |
|---|---|---|
| الإسناد | ينسخ القيمة | يشارك نفس الكائن |
| الوراثة | لا | نعم |
| الاستخدام المعتاد | البيانات: نقاط، وإعدادات، وسجلات | كائنات مشتركة لها هوية: حساب بنكي، وشاشة |

```reference swift
struct S { var x: T } | نوع قيمة | struct User { var name: String }
mutating func | دالة تغيّر الهيكل | mutating func reset()
class C { init(...) } | نوع مرجعي بمُنشئ | init(name: String) { self.name = name }
class B: A | الوراثة | class Admin: User
private(set) var | قراءة من الخارج وتغيير من الداخل | private(set) var total = 0
override func | استبدال دالة الأب | override func describe()
```

:::tip ابدأ بالهياكل
توصي Apple بالهياكل افتراضيًا. واستخدم الصنف عندما تحتاج الوراثة، أو عندما يجب أن تتشارك أجزاء التطبيق كائنًا واحدًا يتغير.
:::

```exercise swift
? علّم دالة في هيكل تغيّر خصائصه
___ func move(dx: Double) { x += dx }
= mutating
```

```quiz
? بعد var c = a حيث a هيكل، تغيير c...
* لا يغيّر a
- يغيّر a أيضًا
- غير مسموح
```

# @lesson swift-enums-protocols
title: التعدادات والبروتوكولات والامتدادات
summary: تعدادات بقيم مرتبطة، والبروتوكولات وامتداداتها، والامتدادات.
---
```try swift
enum PaymentStatus {
    case pending
    case paid(amount: Double)
    case failed(reason: String)
}

func describe(_ status: PaymentStatus) -> String {
    switch status {
    case .pending: return "waiting"
    case .paid(let amount): return "paid \(amount)"
    case .failed(let reason): return "failed: \(reason)"
    }
}
for s in [PaymentStatus.pending, .paid(amount: 450), .failed(reason: "card declined")] {
    print(describe(s))
}

protocol Shape {
    var area: Double { get }
}
extension Shape {
    func describe() -> String { "area \(area)" }  // دالة افتراضية لكل Shape
}
struct Rect: Shape { let w, h: Double; var area: Double { w * h } }
struct Circle: Shape { let r: Double; var area: Double { 3.14159 * r * r } }

let shapes: [Shape] = [Rect(w: 2, h: 3), Circle(r: 1)]
for shape in shapes { print(shape.describe()) }
print(shapes.map { $0.area }.reduce(0, +))

extension Int {
    var isEven: Bool { self % 2 == 0 }             // إضافة لنوع موجود
}
print(4.isEven, 7.isEven)
```

```reference swift
enum E { case a, b(T) } | تعداد، وقد تحمل حالاته قيمًا | enum Result { case ok(Int), error(String) }
switch مع case .b(let x) | قراءة القيم المرتبطة | case .paid(let amount):
protocol P { var x: T { get } } | عقد من الخصائص والدوال | protocol Named { var name: String { get } }
struct S: P | الالتزام ببروتوكول | struct User: Named
extension P { func f() } | دوال افتراضية لكل الأنواع الملتزمة | extension Shape { func describe() }
extension Int { ... } | إضافة مزايا لنوع موجود | extension String { var shout: String { uppercased() } }
```

```exercise swift
? اجعل Rect يلتزم بالبروتوكول Shape
struct Rect___ Shape { let w, h: Double; var area: Double { w * h } }
= :
```

```quiz
? ما هو البروتوكول في Swift؟
* مجموعة متطلبات تتعهد الأنواع بتوفيرها
- اتصال شبكة
- نوع من الحلقات
```

# @lesson swift-errors
title: معالجة الأخطاء
summary: أنواع الأخطاء، و throws و do-try-catch و try? و defer.
---
```try swift
enum OrderError: Error {
    case outOfStock(left: Int)
    case invalidQuantity
}

func buy(stock: Int, qty: Int) throws -> Int {
    guard qty > 0 else { throw OrderError.invalidQuantity }
    guard qty <= stock else { throw OrderError.outOfStock(left: stock) }
    return stock - qty
}

for qty in [2, 10, 0] {
    do {
        let left = try buy(stock: 5, qty: qty)
        print("left: \(left)")
    } catch OrderError.outOfStock(let left) {
        print("sorry, only \(left) left")
    } catch {
        print("problem: \(error)")
    }
}

let maybe = try? buy(stock: 5, qty: 99)           // nil بدل الخطأ
print(maybe as Any)

func process() {
    defer { print("cleanup runs last") }
    print("working...")
}
process()
```

```reference swift
enum E: Error { case ... } | تعريف أخطائك | enum LoginError: Error { case wrongPassword }
func f() throws -> T | دالة قد تفشل | func load() throws -> Data
throw E.case | رمي خطأ | throw LoginError.wrongPassword
do { try f() } catch { } | معالجة الأخطاء | catch { print(error) }
try? / try! | نتيجة اختيارية / تعطل عند الخطأ | let x = try? load()
defer { } | تنفيذ عند الخروج من النطاق | defer { file.close() }
```

```exercise swift
? استدعِ دالة قد ترمي خطأ داخل do { }
let left = ___ buy(stock: 5, qty: 2)
= try
```

```quiz
? ماذا تعطي try? عندما ترمي الدالة خطأ؟
* nil
- 0
- توقف البرنامج
```

# @lesson swift-reference
title: مرجع Swift السريع
summary: أكثر الصيغ استخدامًا في صفحة واحدة.
---
```reference swift
let / var | ثابت / متغير | let pi = 3.14
"\(x)" | إدراج قيمة في نص | "Hi \(name)"
T? / ?? / if let / guard let | القيم الاختيارية | guard let id = id else { return }
if / switch | الشروط | switch n { case 1...9: ... default: ... }
for x in a...b / while | الحلقات | for i in 0..<n
[T] / [K: V] / Set<T> | المجموعات | var ages: [String: Int] = [:]
map / filter / reduce | أدوات المجموعات | list.map { $0 * 2 }
func f(label x: T) -> R | الدوال | func greet(person: String) -> String
{ $0 ... } | الـ closures | names.sorted { $0 < $1 }
struct / class | أنواع القيمة / المرجع | struct Point { var x, y: Double }
enum / protocol / extension | النمذجة | enum Status { case on, off }
throws / do-try-catch | الأخطاء | do { try save() } catch { }
```

:::tip الخطوة التالية
على Mac افتح Xcode وأنشئ تطبيق SwiftUI، وابنِ شاشة قائمة صغيرة بالهياكل والمصفوفات من هذه الدورة. وعلى أي نظام، كتاب Swift الرسمي "The Swift Programming Language" على swift.org مجاني وممتاز.
:::

```quiz
? أي ميزة في Swift تحل مشكلات القيم الفارغة (null)؟
* القيم الاختيارية (T?)
- الأصناف
- الحلقات
```
