# @lesson kotlin-intro
title: مقدمة Kotlin
summary: ما هي Kotlin وأين تُستخدم، وأول برنامج لك.
---
**Kotlin** لغة حديثة من شركة JetBrains تعمل على آلة Java الافتراضية. هي اللغة الموصى بها لتطبيقات Android، وتُستخدم أيضًا على الخوادم. تعمل مع كل مكتبات Java لكن بكود أقصر وأكثر أمانًا.

```try kotlin
fun main() {
    println("Hello, Kotlin")
    println(6 * 7)
}
```

- يبدأ البرنامج من `fun main()`.
- `println` تطبع سطرًا، ولا حاجة للفاصلة المنقوطة.
- ملفات Kotlin تنتهي بـ `.kt`.

:::info تشغيل الأمثلة
أمثلة Kotlin تعمل على خادم تشغيل منفصل وآمن؛ إن لم يكن مفعّلًا بعد فستعمل فور تفعيله. وعلى جهازك: ثبّت مترجم Kotlin ثم `kotlinc main.kt -include-runtime -d main.jar` و `java -jar main.jar`، أو استخدم IntelliJ IDEA أو Android Studio.
:::

```quiz
? على أي منصة تعمل Kotlin أساسًا؟
* آلة Java الافتراضية (JVM)
- في المتصفح فقط
- على Windows فقط

? يستطيع كود Kotlin استخدام مكتبات Java.
= true
```

# @lesson kotlin-variables
title: المتغيرات والأنواع
summary: val و var واستنتاج النوع وقوالب النصوص.
---
```try kotlin
fun main() {
    val name = "Sara"          // val: لا يُعاد إسنادها
    var age = 25               // var: يمكن تغييرها
    age += 1
    val price: Double = 19.99  // نوع مكتوب صراحة
    val active = true
    val letter: Char = 'K'

    println("Name: $name, age: $age")
    println("Price with tax: ${price * 1.15}")
    println("$letter $active")
    println(age::class.simpleName)
}
```

```reference kotlin
val | متغير للقراءة فقط | val pi = 3.14
var | متغير قابل للتغيير | var count = 0
Int / Long / Double | الأرقام | val n: Long = 10L
String / Char / Boolean | نص، حرف واحد، صح/خطأ | val c = 'a'
"$x" / "${expr}" | قوالب النصوص | "Total: ${a + b}"
const val | ثابت وقت الترجمة (خارج الأصناف) | const val MAX = 10
```

:::tip فضّل val
ابدأ بـ `val` ولا تنتقل إلى `var` إلا إذا كانت القيمة يجب أن تتغير فعلًا. الكود الذي فيه متغيرات متغيّرة أقل أسهل في المتابعة.
:::

```exercise kotlin
? عرّف متغيرًا للقراءة فقط اسمه city
___ city = "Cairo"
= val
```

```quiz
? ما الفرق بين val و var؟
* لا يمكن إعادة إسناد val، ويمكن مع var
- var أسرع
- val للأرقام فقط

? يمكن أن يحتوي قالب النص ${a + b} على تعبير.
= true
```

# @lesson kotlin-conditions
title: الشروط و when
summary: if كتعبير، و when، والنطاقات.
---
في Kotlin تُعد `if` و `when` تعبيرات: أي أنها ترجع قيمة.

```try kotlin
fun main() {
    val score = 78
    val grade = if (score >= 90) "A" else if (score >= 70) "B" else "C"
    println(grade)

    val label = when (score) {
        in 90..100 -> "Excellent"
        in 70..89 -> "Good"
        else -> "Keep practising"
    }
    println(label)

    val day = "fri"
    when (day) {
        "fri", "sat" -> println("Weekend")
        else -> println("Working day")
    }

    val x = -4
    when {
        x < 0 -> println("negative")
        x == 0 -> println("zero")
        else -> println("positive")
    }
}
```

```reference kotlin
if (c) a else b | if كتعبير | val m = if (a > b) a else b
when (x) { ... } | الاختيار حسب القيمة | when (n) { 1 -> "one" else -> "?" }
when { ... } | سلسلة شروط | when { x < 0 -> ... }
in a..b | داخل نطاق | if (age in 18..60)
!in | ليس داخل | if (c !in "aeiou")
```

:::tip لا يوجد شرط ثلاثي
لا يوجد في Kotlin العامل `? :`؛ فـ `if (c) a else b` تؤدي نفس المهمة.
:::

```exercise kotlin
? تحقّق أن n بين 1 و 10 شاملة
if (n ___ 1..10) println("ok")
= in
```

```quiz
? ماذا ترجع when إذا لم يطابق أي فرع وكان هناك فرع else؟
* قيمة فرع else
- null
- خطأ
```

# @lesson kotlin-loops
title: الحلقات والنطاقات
summary: for على النطاقات والقوائم، و while و until و step و downTo.
---
```try kotlin
fun main() {
    for (i in 1..3) println("Round $i")
    for (i in 0 until 3) print("$i ")
    println()
    for (i in 10 downTo 0 step 5) print("$i ")
    println()

    val colors = listOf("red", "green", "blue")
    for (color in colors) println(color)
    for ((index, color) in colors.withIndex()) println("$index: $color")

    var n = 3
    while (n > 0) {
        print("$n ")
        n--
    }
    println("go!")

    repeat(2) { println("hello") }
}
```

```reference kotlin
a..b | نطاق يشمل b | 1..5
a until b | نطاق بدون b | 0 until size
downTo / step | العد تنازليًا / القفز | 10 downTo 0 step 2
for (x in items) | كل عنصر | for (c in "abc")
withIndex() | الرقم والعنصر | for ((i, v) in list.withIndex())
while / do-while | كرر ما دام الشرط صحيحًا | while (n > 0)
repeat(n) | كرر n مرة | repeat(3) { }
```

```exercise kotlin
? عُدّ من 0 حتى 5 بدون 5
for (i in 0 ___ 5) println(i)
= until
```

```quiz
? ما الأرقام التي يشملها النطاق 1..3؟
* 1 و 2 و 3
- 1 و 2
- 0 و 1 و 2 و 3
```

# @lesson kotlin-functions
title: الدوال
summary: المعاملات والقيم الافتراضية والمعاملات بالاسم ودوال التعبير الواحد و lambda.
---
```try kotlin
fun greet(name: String, greeting: String = "Hello"): String {
    return "$greeting, $name!"
}

fun square(n: Int) = n * n    // دالة بتعبير واحد

fun total(vararg prices: Double): Double = prices.sum()

fun main() {
    println(greet("Sara"))
    println(greet(greeting = "Welcome", name = "Omar"))  // معاملات بالاسم
    println(square(7))
    println(total(10.0, 20.5, 4.0))

    val double = { x: Int -> x * 2 }   // lambda محفوظة في متغير
    println(double(21))
    val nums = listOf(1, 2, 3, 4)
    println(nums.map { it * it })       // it: المعامل الوحيد
}
```

```reference kotlin
fun f(a: Int): Int | دالة بأنواع | fun add(a: Int, b: Int): Int
b: Int = 0 | قيمة افتراضية | fun f(n: Int = 1)
f(name = x) | معامل بالاسم | greet(name = "Sara")
fun f(x: Int) = expr | دالة بتعبير واحد | fun sq(x: Int) = x * x
vararg | أي عدد من المعاملات | fun sum(vararg n: Int)
{ x -> ... } | lambda | val inc = { x: Int -> x + 1 }
it | معامل lambda الوحيد | list.filter { it > 0 }
```

:::tip Unit
الدالة التي لا ترجع شيئًا مفيدًا ترجع `Unit`، ولا داعي لكتابتها: `fun log(msg: String) { println(msg) }`.
:::

```exercise kotlin
? اكتب الكلمة التي تعرّف دالة
___ cube(n: Int) = n * n * n
= fun
```

```quiz
? ماذا تعني it داخل list.map { it * 2 }؟
* العنصر الحالي من القائمة
- القائمة كلها
- رقم العنصر

? المعاملات بالاسم تسمح بتمرير المعاملات بأي ترتيب.
= true
```

# @lesson kotlin-null-safety
title: الأمان من null
summary: الأنواع التي تقبل null، و ?. و ?: و !! والتحويل الذكي.
---
أنواع Kotlin تقول إن كانت القيمة قد تكون غائبة. `String` لا يمكن أن يكون null أبدًا، أما `String?` فيمكن. المترجم يجبرك على التعامل مع حالة null، فتختفي معظم أعطال "null pointer".

```try kotlin
fun lengthOf(text: String?): Int {
    if (text == null) return 0
    return text.length          // تحويل ذكي: text هنا من نوع String
}

fun main() {
    var email: String? = null
    println(email?.length)          // استدعاء آمن: null بدل العطل
    println(email ?: "no email")    // عامل Elvis: قيمة افتراضية
    println(lengthOf(email))

    email = "sara@example.com"
    println(email?.length)
    println(email.toUpperCase())    // المترجم يعرف أنها ليست null الآن

    val input = "42x"
    val number = input.toIntOrNull() ?: -1
    println(number)
}
```

```reference kotlin
String? | نوع يقبل null | var name: String? = null
?. | استدعاء آمن | user?.email?.length
?: | عامل Elvis: قيمة بديلة عند null | name ?: "guest"
!! | "أنا متأكد أنها ليست null" (تتعطل إن كانت) | name!!.length
toIntOrNull() | تحويل أو null | "12".toIntOrNull()
let | نفّذ جزءًا إن لم تكن null | email?.let { send(it) }
```

:::warning تجنّب !!
`!!` تحوّل null إلى عطل. غالبًا الأفضل استخدام `?.` أو `?:` أو فحص بـ `if`.
:::

```exercise kotlin
? أعطِ "guest" إذا كانت name تساوي null
val shown = name ___ "guest"
= ?:
```

```quiz
? ماذا يعطي user?.name إذا كانت user تساوي null؟
* null
- نصًا فارغًا
- عطلًا

? المتغير من نوع String يمكن أن يحمل null.
= false
> النوع String? (بعلامة الاستفهام) فقط هو الذي يقبل null.
```

# @lesson kotlin-collections
title: القوائم والمجموعات والخرائط
summary: المجموعات للقراءة فقط والقابلة للتغيير وأهم عملياتها.
---
```try kotlin
fun main() {
    val nums = listOf(5, 3, 8, 1)
    println(nums.sorted())
    println(nums.filter { it > 2 }.map { it * 10 })
    println("${nums.sum()} ${nums.max()} ${nums.average()}")
    println(nums.first() + nums.last())

    val cart = mutableListOf("tea")
    cart.add("cake")
    cart += "juice"
    cart.remove("tea")
    println(cart)

    val tags = setOf("a", "b", "a")
    println(tags.size)                       // التكرار يُحذف

    val prices = mutableMapOf("tea" to 12.5, "coffee" to 20.0)
    prices["cake"] = 35.0
    for ((item, price) in prices) println("$item = $price")
    println(prices.getOrDefault("water", 0.0))

    val words = listOf("apple", "avocado", "banana")
    println(words.groupBy { it.first() })
}
```

```reference kotlin
listOf / mutableListOf | قائمة للقراءة / قابلة للتغيير | mutableListOf(1, 2)
setOf | مجموعة بلا تكرار | setOf("a", "b")
mapOf / mutableMapOf | خريطة من مفاتيح إلى قيم | mapOf("a" to 1)
filter / map | إبقاء المطابق / تحويل | list.filter { it > 0 }
sorted / sortedBy | نسخة مرتبة | users.sortedBy { it.age }
sum / count / average | المجاميع | list.count { it % 2 == 0 }
groupBy | تجميع حسب مفتاح | words.groupBy { it.length }
any / all | هل يطابق أي / كل عنصر؟ | list.any { it < 0 }
```

:::tip الدالة max() في الإصدارات الأحدث
في Kotlin 1.4 وما بعدها تغيّر اسم `max()` إلى `maxOrNull()`، ثم عادت `max()` لاحقًا بنتيجة لا تكون null. خادم التشغيل هنا يستخدم إصدارًا أقدم تعمل فيه `max()` كما في المثال.
:::

```exercise kotlin
? أنشئ قائمة يمكن إضافة عناصر إليها
val todo = ___("read")
= mutableListOf
```

```quiz
? أي نوع من المجموعات يحذف القيم المكررة؟
* setOf
- listOf
- mapOf
```

# @lesson kotlin-classes
title: الأصناف والكائنات
summary: المُنشئ الأساسي والخصائص والدوال و init و data class.
---
```try kotlin
class Account(val owner: String) {
    var balance = 0.0
        private set          // تُقرأ من الخارج وتُغيَّر من الداخل فقط

    fun deposit(amount: Double) {
        require(amount > 0) { "Amount must be positive" }
        balance += amount
    }
}

data class Product(val name: String, val price: Double)

fun main() {
    val acc = Account("Sara")
    acc.deposit(1000.0)
    println("${acc.owner}: ${acc.balance}")

    val tea = Product("Tea", 12.5)
    val sameTea = Product("Tea", 12.5)
    println(tea)                    // data class: نص مقروء تلقائيًا
    println(tea == sameTea)         // true: تقارن القيم
    val cheaper = tea.copy(price = 10.0)
    println(cheaper)
    val (name, price) = cheaper     // التفكيك
    println("$name costs $price")
}
```

- **المُنشئ الأساسي** يأتي بعد اسم الصنف، و `val`/`var` فيه تنشئ خصائص مباشرة.
- `private set` تجعل الجميع يقرأ الخاصية والصنف وحده يغيّرها.
- **data class** تحصل مجانًا على `toString` و `equals` و `hashCode` و `copy` والتفكيك.

```reference kotlin
class A(val x: Int) | صنف بخاصية من المُنشئ | class User(val name: String)
A(5) | إنشاء كائن (بدون new) | val u = User("Sara")
init { } | كود يعمل عند الإنشاء | init { require(age >= 0) }
private / internal / public | مستوى الوصول | private val id = 1
data class | صنف قيم بدوال مولّدة | data class Point(val x: Int, val y: Int)
copy() | نسخة مع بعض التغييرات | p.copy(x = 0)
object | نسخة وحيدة (singleton) | object Config { val debug = false }
```

```exercise kotlin
? عرّف صنفًا تُولَّد له equals و toString
___ class Point(val x: Int, val y: Int)
= data
```

```quiz
? كيف تنشئ كائنًا من الصنف User في Kotlin؟
* User("Sara")
- new User("Sara")
- User.new("Sara")

? كائنان من data class بنفس القيم متساويان بـ ==.
= true
```

# @lesson kotlin-inheritance
title: الوراثة والواجهات والأصناف المغلقة
summary: open و override و abstract والواجهات و when مع sealed class.
---
الأصناف في Kotlin **نهائية** افتراضيًا؛ ضع `open` لتسمح بالوراثة منها.

```try kotlin
interface Shape {
    fun area(): Double
    fun describe() = "Shape with area ${"%.2f".format(area())}"
}

open class Rectangle(val w: Double, val h: Double) : Shape {
    override fun area() = w * h
}

class Square(side: Double) : Rectangle(side, side)

class Circle(val r: Double) : Shape {
    override fun area() = Math.PI * r * r
}

sealed class Result
class Success(val value: Int) : Result()
class Failure(val message: String) : Result()

fun show(r: Result) = when (r) {       // لا حاجة لـ else: كل الحالات معروفة
    is Success -> "ok: ${r.value}"
    is Failure -> "error: ${r.message}"
}

fun main() {
    val shapes: List<Shape> = listOf(Rectangle(2.0, 3.0), Square(2.0), Circle(1.0))
    for (s in shapes) println(s.describe())
    println(show(Success(42)))
    println(show(Failure("not found")))
}
```

```reference kotlin
open class | السماح بالوراثة | open class Animal
class B : A() | الوراثة من A | class Dog : Animal()
override | استبدال دالة الأب | override fun sound() = "woof"
abstract | يجب أن ينفذها الأبناء | abstract fun area(): Double
interface | عقد، وقد يحوي دوال افتراضية | interface Named { val name: String }
sealed class | مجموعة مغلقة من الأصناف الأبناء | sealed class State
is | فحص النوع مع تحويل ذكي | if (x is String) x.length
```

```exercise kotlin
? علّم الصنف ليمكن لأصناف أخرى الوراثة منه
___ class Animal(val name: String)
= open
```

```quiz
? لماذا لا تحتاج when مع sealed class إلى else؟
* لأن المترجم يعرف كل الأصناف الأبناء الممكنة
- لأن when لا تحتاج else أبدًا
- لأن الأصناف المغلقة لا تُستخدم مع when
```

# @lesson kotlin-errors
title: الاستثناءات
summary: try كتعبير، و throw و require و runCatching.
---
```try kotlin
class OutOfStock(message: String) : Exception(message)

fun buy(stock: Int, qty: Int): Int {
    require(qty > 0) { "Quantity must be positive" }
    if (qty > stock) throw OutOfStock("Only $stock left")
    return stock - qty
}

fun main() {
    for (qty in listOf(2, 10, 0)) {
        try {
            println("Left: ${buy(5, qty)}")
        } catch (e: OutOfStock) {
            println("Sorry: ${e.message}")
        } catch (e: IllegalArgumentException) {
            println("Bad input: ${e.message}")
        } finally {
            println("-- checked $qty")
        }
    }

    val n = try { "12a".toInt() } catch (e: NumberFormatException) { 0 }
    println(n)

    val result = runCatching { 10 / 0 }
    println(result.isFailure)
    println(result.getOrDefault(-1))
}
```

```reference kotlin
throw | رمي استثناء | throw IllegalStateException("x")
try / catch / finally | معالجة الاستثناءات | try { } catch (e: Exception) { }
val x = try { } catch ... | try كتعبير | val n = try { s.toInt() } catch (e: Exception) { 0 }
require(cond) | فحص معامل (IllegalArgumentException) | require(age >= 0)
check(cond) | فحص الحالة (IllegalStateException) | check(isOpen)
runCatching { } | تغليف النتيجة أو الخطأ | runCatching { load() }.getOrNull()
```

:::tip لا توجد استثناءات إجبارية
على عكس Java، لا تجبرك Kotlin أبدًا على التقاط الاستثناءات أو التصريح بها. أنت تقرر أين يكون التعامل معها منطقيًا.
:::

```exercise kotlin
? تحقّق من صحة المعامل، وارمِ IllegalArgumentException إن لم يكن صحيحًا
___(price >= 0) { "Price cannot be negative" }
= require
```

```quiz
? أي استثناء ترميه require(false)؟
* IllegalArgumentException
- IllegalStateException
- NullPointerException
```

# @lesson kotlin-extensions
title: دوال التوسيع ودوال النطاق
summary: إضافة دوال لأنواع موجودة، و let و apply و also و run.
---
```try kotlin
fun String.initials(): String =
    split(" ").filter { it.isNotEmpty() }.joinToString("") { it.first().toUpperCase().toString() }

val Int.isEven: Boolean
    get() = this % 2 == 0

data class User(var name: String = "", var age: Int = 0)

fun main() {
    println("sara ali hassan".initials())
    println(4.isEven)

    val user = User().apply {        // تجهيز كائن، وترجعه
        name = "Omar"
        age = 30
    }
    println(user)

    val email: String? = "omar@example.com"
    email?.let { println("Sending to $it") }   // فقط إن لم تكن null

    val size = listOf(1, 2, 3).also { println("list: $it") }.size
    println(size)

    val msg = user.run { "$name is $age" }     // حساب قيمة من الكائن
    println(msg)
}
```

```reference kotlin
fun T.f() | دالة توسيع | fun String.shout() = toUpperCase() + "!"
val T.p get() | خاصية توسيع | val Int.isEven get() = this % 2 == 0
let | it في الداخل؛ ترجع نتيجة الجزء | x?.let { use(it) }
apply | this في الداخل؛ ترجع الكائن | User().apply { name = "A" }
also | it في الداخل؛ ترجع الكائن | list.also { log(it) }
run | this في الداخل؛ ترجع نتيجة الجزء | user.run { name.length }
```

:::tip أي دالة نطاق أستخدم؟
استخدم `apply` لتجهيز كائن، و `let` مع `?.` لقيمة قد تكون null، و `also` للأعمال الجانبية مثل التسجيل.
:::

```exercise kotlin
? نفّذ الجزء فقط إذا لم تكن email تساوي null
email?.___ { send(it) }
= let
```

```quiz
? ماذا ترجع apply؟
* الكائن نفسه
- آخر قيمة في الجزء
- Unit
```

# @lesson kotlin-reference
title: مرجع Kotlin السريع
summary: أكثر الصيغ استخدامًا في صفحة واحدة.
---
```reference kotlin
fun main() | نقطة البداية | fun main() { }
val / var | متغير للقراءة / قابل للتغيير | val n = 1
"$x ${e}" | قوالب النصوص | "Hi $name"
if / when | شروط كتعبيرات | val s = if (ok) "y" else "n"
for (i in 1..n) | حلقة على نطاق | for (i in 0 until n)
fun f(x: Int) = ... | دالة | fun sq(x: Int) = x * x
{ x -> } / it | lambda | list.map { it * 2 }
T? / ?. / ?: | الأمان من null | name?.length ?: 0
listOf / mutableListOf / mapOf | المجموعات | mapOf("a" to 1)
class A(val x: Int) | صنف | val a = A(1)
data class | صنف قيم | data class P(val x: Int)
open / override / sealed | الوراثة | sealed class Result
try / catch / require | الأخطاء | require(x > 0)
fun T.ext() | دالة توسيع | fun Int.twice() = this * 2
let / apply / also / run | دوال النطاق | obj.apply { }
```

:::tip الخطوة التالية
ابنِ تطبيق طرفية صغيرًا، مثل قائمة مشتريات بـ data class وقائمة قابلة للتغيير و `when` للأوامر. بعدها جرّب Android مع Jetpack Compose، أو خادمًا مع Ktor.
:::

```quiz
? أي عامل يعطي قيمة بديلة عندما يكون الطرف الأيسر null؟
* ?:
- ?.
- !!
```
