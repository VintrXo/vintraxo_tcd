# @lesson swift-intro
title: Swift introduction
summary: What Swift is, where it is used, and your first program.
---
**Swift** is Apple's modern language for iPhone, iPad, Mac, Apple Watch and Apple TV apps. It is fast, safe and readable, and it also runs on Linux servers. Swift replaced Objective-C as the main language for Apple platforms.

```try swift
print("Hello, Swift")
print(6 * 7)
let name = "Sara"
print("Welcome, \(name)!")
```

- A Swift file runs from the top; there is no `main` function to write for small programs.
- `print` writes a line; no semicolons are needed.
- `\(...)` puts a value inside a string (string interpolation).

:::info Running the examples
Swift examples run on a separate, secure server. On a Mac, install Xcode and try code in a Playground; on Linux or Windows, install Swift from swift.org and run `swift main.swift`.
:::

```quiz
? What is Swift mainly used for?
* Apps for Apple devices such as iPhone and Mac
- Databases
- Spreadsheet formulas

? In Swift, "\(name)" inserts the value of name into the string.
= true
```

# @lesson swift-variables
title: Constants, variables and types
summary: let and var, type inference, basic types and conversions.
---
```try swift
let company = "VintraXo"        // let: a constant, cannot change
var employees = 120             // var: a variable
employees += 5
let price: Double = 19.99       // an explicit type
let isOpen = true
let initial: Character = "V"

print(company, employees, isOpen, initial)
print("Price with tax:", price * 1.14)

let age = 25
let message = "Age: " + String(age)      // convert Int to String
let text = "42"
let number = Int(text) ?? 0              // Int(...) may fail, so ?? gives a default
print(message, number + 1)
print(type(of: price), type(of: employees))
```

```reference swift
let x = 5 | Constant | let pi = 3.14
var x = 5 | Variable | var count = 0
Int / Double / Bool / String / Character | Basic types | let n: Int = 3
"\(value)" | String interpolation | "Total: \(total)"
String(x) / Int("42") / Double("2.5") | Conversions (Int("x") is nil) | Int("12") ?? 0
type(of: x) | The type of a value | type(of: 3.5)
```

:::tip Prefer let
Use `let` unless the value really has to change. The compiler warns you when a `var` is never changed.
:::

```exercise swift
? Declare a constant named city
___ city = "Cairo"
= let
```

```quiz
? What is the difference between let and var?
* let cannot be changed after it is set; var can
- var is faster
- let is only for numbers
```

# @lesson swift-optionals
title: Optionals
summary: Values that may be missing, if let, guard let and the ?? operator.
---
In Swift, a normal variable can never be empty. A value that might be missing has an **optional** type, written with `?`: `String?` means "a String or nothing (`nil`)".

```try swift
let input = "42x"
let parsed: Int? = Int(input)            // nil, because "42x" is not a number
print(parsed as Any)

var email: String? = nil
print(email ?? "no email")               // default when nil

email = "sara@example.com"
if let address = email {                 // unwrap safely
    print("Send to \(address), \(address.count) characters")
}

func greet(_ name: String?) {
    guard let name = name else {         // leave early when missing
        print("Hello, guest")
        return
    }
    print("Hello, \(name)")
}
greet(nil)
greet("Omar")

let length = email?.count                // optional chaining: Int?
print(length ?? 0)
```

```reference swift
T? | Optional type: a value or nil | var phone: String?
?? | Default when nil | name ?? "guest"
if let x = optional | Run code only when there is a value | if let n = Int(s) { }
guard let x = optional else { return } | Leave early when nil | guard let id = id else { return }
a?.b | Optional chaining | user?.email?.count
x! | Force unwrap (crashes when nil) | avoid
```

:::warning Avoid force unwrapping
`value!` stops the app if the value is `nil`. Use `if let`, `guard let` or `??` instead.
:::

```exercise swift
? Give "guest" when name is nil
let shown = name ___ "guest"
= ??
```

```quiz
? What does Int("abc") return?
* nil
- 0
- An error that stops the program

? A variable of type String (without ?) can hold nil.
= false
```

# @lesson swift-control
title: Conditions and switch
summary: if, else, switch with ranges, tuples and where.
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
switch score {                          // switch must cover every case
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
if / else if / else | Conditions (no brackets needed) | if x > 0 { }
switch value { case ...: } | Choose by value; must be exhaustive | switch n { case 1: ... default: ... }
a...b / a..<b | Closed / half-open range | case 90...100:
case "a", "b": | Several values in one case | case "fri", "sat":
case let x where cond: | Pattern with a condition | case let (x, y) where x == y:
```

:::tip No fallthrough by default
In Swift, a `case` does not fall into the next one, so you never need `break` at the end of each case.
:::

```exercise swift
? Match the numbers from 1 to 9 inclusive
case 1___9: print("one digit")
= ...
```

```quiz
? What happens if a switch does not cover every possible value?
* The code does not compile
- The missing values are ignored
- It returns nil
```

# @lesson swift-loops
title: Loops
summary: for-in with ranges, arrays and dictionaries, while and repeat-while.
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
for i in 1...n | Loop over a range | for i in 0..<count
for x in array | Each element | for name in names
.enumerated() | Index and element | for (i, x) in list.enumerated()
stride(from:to:by:) | Steps, also backwards | stride(from: 10, to: 0, by: -2)
while / repeat-while | Repeat while true / at least once | repeat { } while x
break / continue | Leave / skip | if x < 0 { continue }
```

```exercise swift
? Loop from 0 up to, but not including, 5
for i in 0___5 { print(i) }
= ..<
```

```quiz
? Which loop always runs its body at least once?
* repeat-while
- while
- for-in
```

# @lesson swift-collections
title: Arrays, dictionaries and sets
summary: Creating and changing collections, and map, filter, reduce and sorted.
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
print(phoneBook["Ali"] ?? "not found")         // a missing key gives nil
print(phoneBook.keys.sorted())

var tags: Set = ["swift", "ios", "swift"]
tags.insert("mobile")
print(tags.count, tags.contains("ios"))

let words = ["apple", "avocado", "banana"]
let grouped = Dictionary(grouping: words, by: { $0.first! })
print(grouped.keys.sorted())
```

```reference swift
[a, b, c] / append / count | Arrays | var list = [1, 2]; list.append(3)
[key: value] / dict[key] | Dictionaries (reading gives an optional) | ages["Sara"] ?? 0
Set | Unique values | var s: Set = [1, 2, 2]
map / filter / reduce | Transform, keep, combine | nums.map { $0 * 2 }
sorted() / sorted(by:) | Sorted copy | users.sorted { $0.age < $1.age }
$0 / $1 | Shorthand closure parameters | list.filter { $0 > 0 }
```

:::tip Arrays are values
Assigning an array to another variable makes a copy. Changing the copy does not change the original, which avoids many surprising bugs.
:::

```exercise swift
? Keep only the even numbers
let evens = numbers.___ { $0 % 2 == 0 }
= filter
```

```quiz
? What does reading a missing key from a dictionary return?
* nil
- 0
- An empty string
```

# @lesson swift-functions
title: Functions and closures
summary: Argument labels, default values, multiple return values and closures.
---
```try swift
func greet(person name: String, greeting: String = "Hello") -> String {
    return "\(greeting), \(name)!"
}
print(greet(person: "Sara"))
print(greet(person: "Omar", greeting: "Welcome"))

func square(_ n: Int) -> Int { n * n }      // _ means no label when calling
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
print(apply([1, 2, 3]) { $0 * 10 })           // trailing closure
```

```reference swift
func f(label name: T) -> R | Function with an argument label | func move(to point: Point)
_ name | No label when calling | func square(_ n: Int)
name: T = value | Default value | greeting: String = "Hi"
-> (a: T, b: U) | Return several values (tuple) | return (min, max)
{ (x: T) -> R in ... } | Closure | let double = { (x: Int) in x * 2 }
f(x) { ... } | Trailing closure | list.sorted { $0 < $1 }
```

```exercise swift
? Write the keyword that declares a function
___ double(_ x: Int) -> Int { x * 2 }
= func
```

```quiz
? Why does Swift use argument labels such as greet(person: "Sara")?
* They make calls read like sentences and clearer
- They are required by the compiler for speed
- They replace the return type
```

# @lesson swift-structs-classes
title: Structs and classes
summary: Properties, methods, initializers, mutating, inheritance, and value versus reference.
---
```try swift
struct Point {
    var x: Double
    var y: Double
    func distance(to other: Point) -> Double {
        ((x - other.x) * (x - other.x) + (y - other.y) * (y - other.y)).squareRoot()
    }
    mutating func move(dx: Double) { x += dx }     // changes the struct itself
}

var a = Point(x: 0, y: 0)
let b = Point(x: 3, y: 4)
print(a.distance(to: b))
var c = a                                          // structs are copied
c.move(dx: 10)
print(a.x, c.x)

class Account {
    let owner: String
    private(set) var balance = 0.0                 // readable outside, changed only inside
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
let same = acc                                     // classes are shared references
same.deposit(1000)
acc.addInterest(rate: 0.05)
print(acc.owner, acc.balance, same.balance)
```

| | Struct | Class |
|---|---|---|
| Assigning | Copies the value | Shares the same object |
| Inheritance | No | Yes |
| Typical use | Data: points, settings, records | Shared objects with identity: a bank account, a screen |

```reference swift
struct S { var x: T } | Value type | struct User { var name: String }
mutating func | A struct method that changes it | mutating func reset()
class C { init(...) } | Reference type with an initializer | init(name: String) { self.name = name }
class B: A | Inheritance | class Admin: User
private(set) var | Read outside, change inside | private(set) var total = 0
override func | Replace a parent method | override func describe()
```

:::tip Start with structs
Apple recommends structs by default. Use a class when you need inheritance or when several parts of the app must share one changing object.
:::

```exercise swift
? Mark a struct method that changes its properties
___ func move(dx: Double) { x += dx }
= mutating
```

```quiz
? After var c = a where a is a struct, changing c...
* Does not change a
- Also changes a
- Is not allowed
```

# @lesson swift-enums-protocols
title: Enums, protocols and extensions
summary: Enums with associated values, protocols, protocol extensions and extensions.
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
    func describe() -> String { "area \(area)" }  // default method for every Shape
}
struct Rect: Shape { let w, h: Double; var area: Double { w * h } }
struct Circle: Shape { let r: Double; var area: Double { 3.14159 * r * r } }

let shapes: [Shape] = [Rect(w: 2, h: 3), Circle(r: 1)]
for shape in shapes { print(shape.describe()) }
print(shapes.map { $0.area }.reduce(0, +))

extension Int {
    var isEven: Bool { self % 2 == 0 }             // add to an existing type
}
print(4.isEven, 7.isEven)
```

```reference swift
enum E { case a, b(T) } | Enum, cases can carry values | enum Result { case ok(Int), error(String) }
switch with case .b(let x) | Read associated values | case .paid(let amount):
protocol P { var x: T { get } } | A contract of properties and methods | protocol Named { var name: String { get } }
struct S: P | Conform to a protocol | struct User: Named
extension P { func f() } | Default methods for all conforming types | extension Shape { func describe() }
extension Int { ... } | Add features to an existing type | extension String { var shout: String { uppercased() } }
```

```exercise swift
? Make Rect conform to the protocol Shape
struct Rect___ Shape { let w, h: Double; var area: Double { w * h } }
= :
```

```quiz
? What is a protocol in Swift?
* A set of requirements that types promise to provide
- A network connection
- A kind of loop
```

# @lesson swift-errors
title: Error handling
summary: Error types, throws, do-try-catch, try? and defer.
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

let maybe = try? buy(stock: 5, qty: 99)           // nil instead of an error
print(maybe as Any)

func process() {
    defer { print("cleanup runs last") }
    print("working...")
}
process()
```

```reference swift
enum E: Error { case ... } | Define your errors | enum LoginError: Error { case wrongPassword }
func f() throws -> T | A function that can fail | func load() throws -> Data
throw E.case | Raise an error | throw LoginError.wrongPassword
do { try f() } catch { } | Handle errors | catch { print(error) }
try? / try! | Optional result / crash on error | let x = try? load()
defer { } | Run when leaving the scope | defer { file.close() }
```

```exercise swift
? Call a throwing function inside do { }
let left = ___ buy(stock: 5, qty: 2)
= try
```

```quiz
? What does try? give when the function throws?
* nil
- 0
- It stops the program
```

# @lesson swift-reference
title: Swift quick reference
summary: The most used syntax on one page.
---
```reference swift
let / var | Constant / variable | let pi = 3.14
"\(x)" | String interpolation | "Hi \(name)"
T? / ?? / if let / guard let | Optionals | guard let id = id else { return }
if / switch | Conditions | switch n { case 1...9: ... default: ... }
for x in a...b / while | Loops | for i in 0..<n
[T] / [K: V] / Set<T> | Collections | var ages: [String: Int] = [:]
map / filter / reduce | Collection tools | list.map { $0 * 2 }
func f(label x: T) -> R | Functions | func greet(person: String) -> String
{ $0 ... } | Closures | names.sorted { $0 < $1 }
struct / class | Value / reference types | struct Point { var x, y: Double }
enum / protocol / extension | Modelling | enum Status { case on, off }
throws / do-try-catch | Errors | do { try save() } catch { }
```

:::tip Where to go next
On a Mac, open Xcode, create a SwiftUI app and build a small list screen with the structs and arrays from this course. On any system, Swift's official book "The Swift Programming Language" at swift.org is free and excellent.
:::

```quiz
? Which feature replaces "null" safety problems in Swift?
* Optionals (T?)
- Classes
- Loops
```
