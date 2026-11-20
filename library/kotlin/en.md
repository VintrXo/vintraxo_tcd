# @lesson kotlin-intro
title: Kotlin introduction
summary: What Kotlin is, where it is used, and your first program.
---
**Kotlin** is a modern language from JetBrains that runs on the Java virtual machine. It is the recommended language for Android apps and is also used on servers. It works with all Java libraries, but with shorter and safer code.

```try kotlin
fun main() {
    println("Hello, Kotlin")
    println(6 * 7)
}
```

- The program starts at `fun main()`.
- `println` prints a line; no semicolons are needed.
- Kotlin files end in `.kt`.

:::info Running the examples
Kotlin examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: install the Kotlin compiler, then `kotlinc main.kt -include-runtime -d main.jar` and `java -jar main.jar`, or use IntelliJ IDEA or Android Studio.
:::

```quiz
? Which platform does Kotlin mainly run on?
* The Java virtual machine (JVM)
- Only in the browser
- Only on Windows

? Kotlin code can use Java libraries.
= true
```

# @lesson kotlin-variables
title: Variables and types
summary: val, var, type inference and string templates.
---
```try kotlin
fun main() {
    val name = "Sara"          // val: cannot be reassigned
    var age = 25               // var: can change
    age += 1
    val price: Double = 19.99  // an explicit type
    val active = true
    val letter: Char = 'K'

    println("Name: $name, age: $age")
    println("Price with tax: ${price * 1.15}")
    println("$letter $active")
    println(age::class.simpleName)
}
```

```reference kotlin
val | Read-only variable | val pi = 3.14
var | Changeable variable | var count = 0
Int / Long / Double | Numbers | val n: Long = 10L
String / Char / Boolean | Text, one character, true/false | val c = 'a'
"$x" / "${expr}" | String templates | "Total: ${a + b}"
const val | Compile-time constant (top level) | const val MAX = 10
```

:::tip Prefer val
Start with `val` and switch to `var` only when the value really has to change. Code with fewer changing variables is easier to follow.
:::

```exercise kotlin
? Declare a read-only variable named city
___ city = "Cairo"
= val
```

```quiz
? What is the difference between val and var?
* val cannot be reassigned, var can
- var is faster
- val is only for numbers

? A string template ${a + b} can contain an expression.
= true
```

# @lesson kotlin-conditions
title: Conditions and when
summary: if as an expression, when, and ranges.
---
In Kotlin, `if` and `when` are expressions: they give back a value.

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
if (c) a else b | if as an expression | val m = if (a > b) a else b
when (x) { ... } | Choose by value | when (n) { 1 -> "one" else -> "?" }
when { ... } | Chain of conditions | when { x < 0 -> ... }
in a..b | Inside a range | if (age in 18..60)
!in | Not inside | if (c !in "aeiou")
```

:::tip No ternary operator
Kotlin has no `? :` ternary; `if (c) a else b` does the same job.
:::

```exercise kotlin
? Check whether n is between 1 and 10 inclusive
if (n ___ 1..10) println("ok")
= in
```

```quiz
? What does when give when no branch matches and there is an else branch?
* The value of the else branch
- null
- An error
```

# @lesson kotlin-loops
title: Loops and ranges
summary: for over ranges and lists, while, until, step and downTo.
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
a..b | Range including b | 1..5
a until b | Range without b | 0 until size
downTo / step | Count down / jump | 10 downTo 0 step 2
for (x in items) | Each item | for (c in "abc")
withIndex() | Index and item | for ((i, v) in list.withIndex())
while / do-while | Repeat while true | while (n > 0)
repeat(n) | Repeat n times | repeat(3) { }
```

```exercise kotlin
? Count from 0 up to, but not including, 5
for (i in 0 ___ 5) println(i)
= until
```

```quiz
? Which numbers does 1..3 include?
* 1, 2 and 3
- 1 and 2
- 0, 1, 2 and 3
```

# @lesson kotlin-functions
title: Functions
summary: Parameters, defaults, named arguments, single-expression functions and lambdas.
---
```try kotlin
fun greet(name: String, greeting: String = "Hello"): String {
    return "$greeting, $name!"
}

fun square(n: Int) = n * n    // single-expression function

fun total(vararg prices: Double): Double = prices.sum()

fun main() {
    println(greet("Sara"))
    println(greet(greeting = "Welcome", name = "Omar"))  // named arguments
    println(square(7))
    println(total(10.0, 20.5, 4.0))

    val double = { x: Int -> x * 2 }   // a lambda stored in a variable
    println(double(21))
    val nums = listOf(1, 2, 3, 4)
    println(nums.map { it * it })       // it: the single parameter
}
```

```reference kotlin
fun f(a: Int): Int | Function with types | fun add(a: Int, b: Int): Int
b: Int = 0 | Default value | fun f(n: Int = 1)
f(name = x) | Named argument | greet(name = "Sara")
fun f(x: Int) = expr | Single-expression function | fun sq(x: Int) = x * x
vararg | Any number of arguments | fun sum(vararg n: Int)
{ x -> ... } | Lambda | val inc = { x: Int -> x + 1 }
it | The single lambda parameter | list.filter { it > 0 }
```

:::tip Unit
A function that returns nothing useful returns `Unit`, and you do not have to write it: `fun log(msg: String) { println(msg) }`.
:::

```exercise kotlin
? Write the keyword that declares a function
___ cube(n: Int) = n * n * n
= fun
```

```quiz
? What does it mean inside list.map { it * 2 }?
* The current item of the list
- The whole list
- The index

? Named arguments let you pass arguments in any order.
= true
```

# @lesson kotlin-null-safety
title: Null safety
summary: Nullable types, ?., ?:, !! and smart casts.
---
Kotlin's types say whether a value may be missing. `String` can never be null; `String?` can. The compiler makes you deal with the null case, which removes most "null pointer" crashes.

```try kotlin
fun lengthOf(text: String?): Int {
    if (text == null) return 0
    return text.length          // smart cast: text is String here
}

fun main() {
    var email: String? = null
    println(email?.length)          // safe call: null instead of a crash
    println(email ?: "no email")    // Elvis: a default value
    println(lengthOf(email))

    email = "sara@example.com"
    println(email?.length)
    println(email.toUpperCase())    // the compiler knows it is not null now

    val input = "42x"
    val number = input.toIntOrNull() ?: -1
    println(number)
}
```

```reference kotlin
String? | A type that allows null | var name: String? = null
?. | Safe call | user?.email?.length
?: | Elvis operator: default when null | name ?: "guest"
!! | "I am sure it is not null" (crashes if it is) | name!!.length
toIntOrNull() | Parse or give null | "12".toIntOrNull()
let | Run a block when not null | email?.let { send(it) }
```

:::warning Avoid !!
`!!` turns a null into a crash. It is almost always better to use `?.`, `?:` or an `if` check.
:::

```exercise kotlin
? Give "guest" when name is null
val shown = name ___ "guest"
= ?:
```

```quiz
? What does user?.name give when user is null?
* null
- An empty string
- A crash

? A variable of type String can hold null.
= false
> Only String? (with a question mark) allows null.
```

# @lesson kotlin-collections
title: Lists, sets and maps
summary: Read-only and mutable collections and the most useful operations.
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
    println(tags.size)                       // duplicates are removed

    val prices = mutableMapOf("tea" to 12.5, "coffee" to 20.0)
    prices["cake"] = 35.0
    for ((item, price) in prices) println("$item = $price")
    println(prices.getOrDefault("water", 0.0))

    val words = listOf("apple", "avocado", "banana")
    println(words.groupBy { it.first() })
}
```

```reference kotlin
listOf / mutableListOf | Read-only / changeable list | mutableListOf(1, 2)
setOf | Set without duplicates | setOf("a", "b")
mapOf / mutableMapOf | Map from keys to values | mapOf("a" to 1)
filter / map | Keep matching / transform | list.filter { it > 0 }
sorted / sortedBy | Sorted copy | users.sortedBy { it.age }
sum / count / average | Totals | list.count { it % 2 == 0 }
groupBy | Group by a key | words.groupBy { it.length }
any / all | Does any / every item match? | list.any { it < 0 }
```

:::tip max() in newer Kotlin
In Kotlin 1.4 and later, `max()` was renamed `maxOrNull()`, and later `max()` returned with a non-null result. The runner here uses an older Kotlin, where `max()` works as shown.
:::

```exercise kotlin
? Create a list you can add items to
val todo = ___("read")
= mutableListOf
```

```quiz
? Which collection removes duplicate values?
* setOf
- listOf
- mapOf
```

# @lesson kotlin-classes
title: Classes and objects
summary: Primary constructors, properties, methods, init and data classes.
---
```try kotlin
class Account(val owner: String) {
    var balance = 0.0
        private set          // readable outside, changeable only inside

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
    println(tea)                    // data class: readable toString
    println(tea == sameTea)         // true: compares values
    val cheaper = tea.copy(price = 10.0)
    println(cheaper)
    val (name, price) = cheaper     // destructuring
    println("$name costs $price")
}
```

- The **primary constructor** comes after the class name; `val`/`var` there make properties directly.
- `private set` lets everyone read a property but only the class change it.
- A **data class** gets `toString`, `equals`, `hashCode`, `copy` and destructuring for free.

```reference kotlin
class A(val x: Int) | Class with a property from the constructor | class User(val name: String)
A(5) | Create an object (no new) | val u = User("Sara")
init { } | Code that runs on creation | init { require(age >= 0) }
private / internal / public | Visibility | private val id = 1
data class | Value class with generated methods | data class Point(val x: Int, val y: Int)
copy() | Copy with some changes | p.copy(x = 0)
object | A single instance (singleton) | object Config { val debug = false }
```

```exercise kotlin
? Declare a class whose equals and toString are generated
___ class Point(val x: Int, val y: Int)
= data
```

```quiz
? How do you create an object of class User in Kotlin?
* User("Sara")
- new User("Sara")
- User.new("Sara")

? Two data class objects with the same values are equal with ==.
= true
```

# @lesson kotlin-inheritance
title: Inheritance, interfaces and sealed classes
summary: open, override, abstract, interfaces and when over sealed classes.
---
Classes in Kotlin are **final** by default; mark one `open` to allow inheritance.

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

fun show(r: Result) = when (r) {       // no else needed: all cases are known
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
open class | Allow inheritance | open class Animal
class B : A() | Inherit from A | class Dog : Animal()
override | Replace a parent method | override fun sound() = "woof"
abstract | Must be implemented by children | abstract fun area(): Double
interface | A contract, may have default methods | interface Named { val name: String }
sealed class | A closed set of subclasses | sealed class State
is | Type check with smart cast | if (x is String) x.length
```

```exercise kotlin
? Mark the class so other classes can extend it
___ class Animal(val name: String)
= open
```

```quiz
? Why does when over a sealed class not need else?
* The compiler knows every possible subclass
- when never needs else
- Sealed classes cannot be used in when
```

# @lesson kotlin-errors
title: Exceptions
summary: try as an expression, throw, require and runCatching.
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
throw | Raise an exception | throw IllegalStateException("x")
try / catch / finally | Handle exceptions | try { } catch (e: Exception) { }
val x = try { } catch ... | try as an expression | val n = try { s.toInt() } catch (e: Exception) { 0 }
require(cond) | Check an argument (IllegalArgumentException) | require(age >= 0)
check(cond) | Check the state (IllegalStateException) | check(isOpen)
runCatching { } | Wrap the result or the error | runCatching { load() }.getOrNull()
```

:::tip No checked exceptions
Unlike Java, Kotlin never forces you to catch or declare exceptions. Decide yourself where it makes sense to handle them.
:::

```exercise kotlin
? Check that the argument is valid, throwing IllegalArgumentException if not
___(price >= 0) { "Price cannot be negative" }
= require
```

```quiz
? Which exception does require(false) throw?
* IllegalArgumentException
- IllegalStateException
- NullPointerException
```

# @lesson kotlin-extensions
title: Extension functions and scope functions
summary: Adding functions to existing types, and let, apply, also, run.
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

    val user = User().apply {        // configure an object, returns it
        name = "Omar"
        age = 30
    }
    println(user)

    val email: String? = "omar@example.com"
    email?.let { println("Sending to $it") }   // only when not null

    val size = listOf(1, 2, 3).also { println("list: $it") }.size
    println(size)

    val msg = user.run { "$name is $age" }     // compute from the object
    println(msg)
}
```

```reference kotlin
fun T.f() | Extension function | fun String.shout() = toUpperCase() + "!"
val T.p get() | Extension property | val Int.isEven get() = this % 2 == 0
let | it inside; returns the block result | x?.let { use(it) }
apply | this inside; returns the object | User().apply { name = "A" }
also | it inside; returns the object | list.also { log(it) }
run | this inside; returns the block result | user.run { name.length }
```

:::tip Which scope function?
Use `apply` to set up an object, `let` with `?.` to work with a value that may be null, and `also` for side effects such as logging.
:::

```exercise kotlin
? Run the block only when email is not null
email?.___ { send(it) }
= let
```

```quiz
? What does apply return?
* The object itself
- The block's last value
- Unit
```

# @lesson kotlin-reference
title: Kotlin quick reference
summary: The most used syntax on one page.
---
```reference kotlin
fun main() | Entry point | fun main() { }
val / var | Read-only / changeable variable | val n = 1
"$x ${e}" | String templates | "Hi $name"
if / when | Conditions as expressions | val s = if (ok) "y" else "n"
for (i in 1..n) | Loop over a range | for (i in 0 until n)
fun f(x: Int) = ... | Function | fun sq(x: Int) = x * x
{ x -> } / it | Lambdas | list.map { it * 2 }
T? / ?. / ?: | Null safety | name?.length ?: 0
listOf / mutableListOf / mapOf | Collections | mapOf("a" to 1)
class A(val x: Int) | Class | val a = A(1)
data class | Value class | data class P(val x: Int)
open / override / sealed | Inheritance | sealed class Result
try / catch / require | Errors | require(x > 0)
fun T.ext() | Extension function | fun Int.twice() = this * 2
let / apply / also / run | Scope functions | obj.apply { }
```

:::tip Where to go next
Build a small console app, for example a shopping list with data classes, a mutable list and `when` for commands. Then try Android with Jetpack Compose, or a server with Ktor.
:::

```quiz
? Which operator gives a default value when the left side is null?
* ?:
- ?.
- !!
```
