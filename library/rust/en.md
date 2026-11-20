# @lesson rust-intro
title: Rust introduction
summary: What Rust is, why it is safe and fast, and your first program.
---
**Rust** is a systems language: as fast as C and C++, but the compiler stops whole families of bugs (dangling pointers, data races) before the program runs. It is used for command-line tools, browsers, operating systems, WebAssembly and servers.

```try rust
fn main() {
    println!("Hello, Rust");
    println!("{}", 6 * 7);
}
```

- The program starts at `fn main()`.
- `println!` ends with `!` because it is a **macro**, not a function. `{}` is replaced by the next value.
- Statements end with `;`.

:::info Running the examples
Rust examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: install with rustup, then `cargo new hello` and `cargo run`.
:::

```quiz
? Why does println! end with an exclamation mark?
* It is a macro
- It prints in bold
- It is an error

? Rust catches many memory bugs at compile time.
= true
```

# @lesson rust-variables
title: Variables and types
summary: let, mut, shadowing, and the basic types.
---
Variables are **immutable** by default. Add `mut` when a value has to change.

```try rust
fn main() {
    let name = "Sara";
    let mut age = 25;          // mut: may change
    age += 1;
    let price: f64 = 19.99;    // an explicit type
    let active = true;
    let letter = 'R';

    println!("Name: {}, age: {}", name, age);
    println!("Price with tax: {:.2}", price * 1.15);
    println!("{} {}", letter, active);

    let spaces = "   ";        // shadowing: a new variable with the same name
    let spaces = spaces.len();
    println!("{} spaces", spaces);

    let big: i64 = 3_000_000_000;
    let small = 255u8;
    println!("{} {}", big, small);
}
```

```reference rust
let x = 5 | Immutable variable | let n = 1;
let mut x | Changeable variable | let mut count = 0;
i32 / i64 / u8 / usize | Integers (signed / unsigned) | let i: usize = 0;
f64 | Decimal numbers | let p: f64 = 2.5;
bool / char | true/false, one Unicode character | let c = 'ب';
&str / String | Borrowed text / owned text | let s = String::from("hi");
{} / {:?} / {:.2} | Display / debug / two decimals | println!("{:?}", v);
const | Constant with a type | const MAX: u32 = 100;
```

:::tip Immutability is the default
Most values never change after you create them. Making change explicit with `mut` lets you and the compiler see quickly where state changes.
:::

```exercise rust
? Make count a variable that can change
let ___ count = 0;
= mut
```

```quiz
? What happens if you assign to a variable declared without mut?
* The program does not compile
- The value changes anyway
- It becomes zero

? Shadowing lets you declare a new variable with the same name.
= true
```

# @lesson rust-control
title: Conditions and loops
summary: if as an expression, loop, while, for and ranges.
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
            break tries;        // loop can return a value
        }
    };
    println!("first square above 50: {}^2", found);
}
```

```reference rust
if c { } else { } | Condition (no brackets needed) | if x > 0 { }
let v = if c { a } else { b } | if as an expression | let m = if a > b { a } else { b };
loop | Repeat until break | loop { break; }
while c | Repeat while true | while n > 0 { }
for x in a..b | Range without b | for i in 0..5
a..=b | Range including b | for i in 1..=3
break / continue | Leave / skip a round | break value;
```

:::warning The condition must be a bool
`if 1 { }` does not compile. Rust never treats a number as true or false; write `if n != 0`.
:::

```exercise rust
? Loop from 1 to 5 including 5
for i in 1___5 { println!("{}", i); }
= ..=
```

```quiz
? Which loop can give back a value with break?
* loop
- for
- while
```

# @lesson rust-functions
title: Functions
summary: Parameters, return types, expressions and closures.
---
```try rust
fn square(n: i32) -> i32 {
    n * n                    // no semicolon: this is the return value
}

fn divide(a: f64, b: f64) -> f64 {
    if b == 0.0 {
        return 0.0;          // early return
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
    let with_tax = |price: f64| price * (1.0 + tax);   // a closure sees tax
    println!("{:.2}", with_tax(100.0));

    let nums = vec![1, 2, 3, 4];
    let doubled: Vec<i32> = nums.iter().map(|n| n * 2).collect();
    println!("{:?}", doubled);
}
```

```reference rust
fn f(a: i32) -> i32 | Function with types | fn add(a: i32, b: i32) -> i32
last expression | The value returned (no ;) | fn one() -> i32 { 1 }
return x; | Return early | if bad { return 0; }
() | Unit: "no value" | fn log(m: &str) { }
|x| expr | Closure | let inc = |x| x + 1;
```

:::tip Expressions and statements
A line ending with `;` is a statement and gives nothing back. The last line of a block **without** `;` is the block's value. Adding a stray `;` after `n * n` makes the function return `()` and the compiler complains.
:::

```exercise rust
? Write the keyword that declares a function
___ cube(n: i32) -> i32 { n * n * n }
= fn
```

```quiz
? What does a function return when its last line is n * n without a semicolon?
* The value of n * n
- Nothing
- An error

? Function parameters in Rust must have types.
= true
```

# @lesson rust-ownership
title: Ownership and moves
summary: Every value has one owner; moving, cloning and copying.
---
Ownership is the idea at the heart of Rust:

1. Every value has exactly one **owner**.
2. When the owner goes out of scope, the value is freed (no garbage collector needed).
3. Assigning or passing a value **moves** it, and the old name can no longer be used.

```try rust
fn take(s: String) {
    println!("took {}", s);
}                              // s is freed here

fn main() {
    let a = String::from("hello");
    let b = a;                 // the String moves from a to b
    // println!("{}", a);      // would not compile: a was moved
    println!("{}", b);

    let c = b.clone();         // a real copy of the text
    take(b);                   // b moves into the function
    println!("still have {}", c);

    let x = 5;
    let y = x;                 // simple numbers are Copy: both stay usable
    println!("{} {}", x, y);
}
```

```reference rust
let b = a; | Move: a is no longer usable | let v2 = v1;
.clone() | Explicit deep copy | let s2 = s1.clone();
Copy types | Integers, floats, bool, char: copied, not moved | let y = x;
scope end | The owner's value is dropped | { let s = String::new(); }
```

:::tip Why this matters
Because only one owner frees each value, Rust has no "double free" and no use of freed memory, and it does not need a garbage collector to get there.
:::

```exercise rust
? Make a full copy of name so that both can be used
let copy = name.___();
= clone
```

```quiz
? After let b = a; where a is a String, what happens to a?
* It is moved and cannot be used
- It keeps a copy
- It becomes empty but usable

? Integers are copied, not moved, when assigned.
= true
```

# @lesson rust-borrowing
title: References and borrowing
summary: &, &mut, and the borrowing rules.
---
Instead of moving a value, you can **borrow** it with a reference. The owner keeps it.

```try rust
fn length(s: &String) -> usize {     // borrows, does not take
    s.len()
}

fn shout(s: &mut String) {            // a mutable borrow
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
    let r2 = &greeting;          // many shared borrows are fine
    println!("{} {}", r1, r2);
}
```

The rules the compiler checks:

- At any time you may have **either** many shared references `&T` **or** one mutable reference `&mut T`, not both.
- A reference can never live longer than the value it points to.

```reference rust
&x | Shared (read-only) borrow | length(&s)
&mut x | Mutable borrow | push(&mut v)
&str | Borrowed slice of text | fn f(s: &str)
&v[a..b] | Slice of a vector or string | &nums[1..3]
*r | The value behind a reference | *count += 1;
```

:::tip Take &str, not &String
A function that only reads text should accept `&str`. It then works with string literals and with `String` values alike.
:::

```exercise rust
? Pass a mutable borrow of list to the function
add_item(___ list);
= &mut
```

```quiz
? Which combination does the borrow checker allow at the same time?
* Several shared references
- A shared and a mutable reference
- Two mutable references
```

# @lesson rust-structs
title: Structs and methods
summary: Defining data types, impl blocks and derive.
---
```try rust
#[derive(Debug, Clone, PartialEq)]
struct Product {
    name: String,
    price: f64,
    stock: u32,
}

impl Product {
    fn new(name: &str, price: f64) -> Product {     // an associated function
        Product { name: name.to_string(), price, stock: 0 }
    }

    fn total_value(&self) -> f64 {                   // reads self
        self.price * self.stock as f64
    }

    fn restock(&mut self, qty: u32) {                // changes self
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

    let cake = Product { name: String::from("Cake"), ..tea };   // update syntax
    println!("{} {}", cake.name, cake.stock);
}
```

```reference rust
struct S { a: T } | Define a struct | struct Point { x: i32, y: i32 }
S { a: v } | Create one | Point { x: 1, y: 2 }
impl S { } | Methods for S | impl Point { fn len(&self) -> f64 { } }
&self / &mut self | Read / change the object | fn reset(&mut self)
S::new() | Associated function (constructor by convention) | Product::new("Tea", 1.0)
#[derive(Debug)] | Generate code (printing, copying, comparing) | #[derive(Debug, Clone)]
```

```exercise rust
? Print a struct with debug formatting
println!("___", tea);
= {:?}
```

```quiz
? Which receiver lets a method change the object?
* &mut self
- &self
- self: const

? #[derive(Debug)] lets you print a struct with {:?}.
= true
```

# @lesson rust-enums
title: Enums, Option and match
summary: Enums with data, pattern matching, and Option instead of null.
---
Rust has no `null`. A value that may be missing has the type `Option<T>`: either `Some(value)` or `None`.

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
enum E { A, B(T) } | Enum, variants can hold data | enum Msg { Quit, Move(i32, i32) }
match x { p => v } | Pattern matching (must cover every case) | match n { 0 => "z", _ => "?" }
_ | Any other value | _ => println!("other")
Option<T> | Some(value) or None | let p: Option<i32> = None;
if let Some(x) = v | Act only on one pattern | if let Some(u) = user { }
unwrap_or(d) | Value or a default | opt.unwrap_or(0)
```

:::warning Be careful with unwrap()
`opt.unwrap()` stops the program (a panic) when the value is `None`. Prefer `match`, `if let` or `unwrap_or`.
:::

```exercise rust
? Write the value for "no value" in an Option
let missing: Option<i32> = ___;
= None
```

```quiz
? What happens if a match does not cover every possible value?
* The program does not compile
- The missing cases are ignored
- It returns null

? Option<T> is how Rust represents a value that may be absent.
= true
```

# @lesson rust-collections
title: Vectors, strings and hash maps
summary: Vec, String, HashMap and iterators.
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
vec![..] / Vec::new() | Create a vector | let mut v = Vec::new();
push / pop / len | Add / remove last / size | v.push(1);
.iter().map().filter() | Iterator chain | v.iter().map(|x| x * 2)
.collect() | Build a collection from an iterator | let v: Vec<_> = it.collect();
String::from / push_str | Owned, growable text | s.push_str("!");
.chars().count() | Count characters (not bytes) | "عربي".chars().count()
HashMap::new / insert / get | Key-value map | m.get("tea")
entry().or_insert() | Insert if missing, then update | *m.entry(k).or_insert(0) += 1;
```

:::tip len() counts bytes
`String::len()` returns bytes; Arabic letters take two bytes each. Use `.chars().count()` to count characters.
:::

```exercise rust
? Turn the iterator into a vector
let v: Vec<i32> = nums.iter().map(|x| x + 1).___();
= collect
```

```quiz
? What does HashMap::get return?
* An Option with the value or None
- The value, or zero
- A Result
```

# @lesson rust-errors
title: Error handling with Result
summary: Result, match, the ? operator and panics.
---
Errors that can be expected (a missing file, bad input) are returned as `Result<T, E>`: either `Ok(value)` or `Err(error)`.

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
    let x: i32 = a.parse()?;     // ? returns the error early
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
Result<T, E> | Ok(value) or Err(error) | fn load() -> Result<String, io::Error>
Ok(v) / Err(e) | Build a result | return Err("bad".to_string());
? | Return the error early, or take the value | let n = s.parse::<i32>()?;
match r { Ok(v) => .., Err(e) => .. } | Handle both cases | match open(p) { .. }
unwrap_or / expect | Default value / stop with a message | r.expect("config missing")
panic!() | Stop the program for a bug that should not happen | panic!("bad state");
```

:::tip Result for expected errors, panic for bugs
Return `Result` when the caller can do something about the error. Use `panic!` only when continuing makes no sense, such as a broken invariant.
:::

```exercise rust
? Return the parse error early with one character
let n: i32 = text.parse()___;
= ?
```

```quiz
? What does the ? operator do on an Err value?
* Returns the error from the current function
- Ignores it
- Turns it into zero

? Result has two variants, Ok and Err.
= true
```

# @lesson rust-traits
title: Traits and generics
summary: Shared behaviour with traits, generic functions and trait bounds.
---
A **trait** describes behaviour that several types share, like an interface in other languages.

```try rust
use std::fmt;

trait Shape {
    fn area(&self) -> f64;
    fn describe(&self) -> String {               // a default method
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

impl fmt::Display for Square {                   // lets {} print a Square
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.side)
    }
}

fn largest<T: PartialOrd + Copy>(items: &[T]) -> T {   // a generic function
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
trait T { fn f(&self); } | Declare a trait | trait Speak { fn speak(&self) -> String; }
impl T for S | Implement it for a type | impl Speak for Dog { .. }
fn f<T: Trait>(x: T) | Generic with a trait bound | fn show<T: Display>(x: T)
&dyn Trait / Box<dyn Trait> | Any type that implements the trait | Vec<Box<dyn Shape>>
Display / Debug | Printing with {} / {:?} | impl fmt::Display for P
PartialOrd / Copy / Clone | Common standard traits | #[derive(Clone, Copy)]
```

```exercise rust
? Implement the trait Shape for Triangle
impl Shape ___ Triangle { fn area(&self) -> f64 { 0.0 } }
= for
```

```quiz
? What is a trait in Rust?
* A set of methods that types can implement
- A kind of loop
- A memory address
```

# @lesson rust-reference
title: Rust quick reference
summary: The most used syntax on one page.
---
```reference rust
fn main() | Entry point | fn main() { }
let / let mut | Variable / changeable variable | let mut n = 0;
println!("{} {:?}", a, b) | Print with formatting | println!("{:.2}", x);
if / loop / while / for | Control flow | for i in 0..n { }
fn f(x: i32) -> i32 | Function | fn sq(x: i32) -> i32 { x * x }
|x| ... | Closure | v.iter().map(|x| x + 1)
String / &str | Owned / borrowed text | let s: &str = "hi";
&x / &mut x | Borrow | change(&mut v);
struct / impl | Data and methods | impl P { fn new() -> P { .. } }
enum / match | Variants and pattern matching | match o { Some(x) => x, None => 0 }
Option / Result | Missing values / errors | let n = s.parse::<i32>()?;
Vec / HashMap | Collections | let mut m = HashMap::new();
trait / impl Trait for T | Shared behaviour | impl Display for P
```

:::tip Where to go next
Use `cargo new` to build a small command-line tool, such as a word counter that reads a file and prints the top words with a `HashMap`. Then read about modules, crates on crates.io, and threads.
:::

```quiz
? Which type does Rust use instead of null for a value that may be missing?
* Option
- Result
- Box
```
