# @lesson py-intro
title: Python introduction
summary: What Python is and why it is one of the most used languages.
---
**Python** is an easy-to-read programming language used for data analysis, artificial intelligence, automation, web development and teaching.

## Your first program

Press **Run** (the first run takes a few seconds to load Python in your browser):

```try python
print("Hello, Python")
print(3 + 4)
```

## Why Python?

- **Easy to read**: its code is close to plain English.
- **Huge libraries**: there is a ready-made library for almost every field.
- **Runs everywhere**: Windows, Mac, Linux and servers.

:::info Python on this platform
Every example runs right in your browser, with nothing to install and without sending your code to any server.
:::

```quiz
? Which function prints text in Python?
* print()
- echo()
- console.log()

? Python is used in artificial intelligence and data analysis.
= true
```

# @lesson py-syntax
title: Python syntax
summary: Indentation, comments, and writing several lines.
---
## Indentation

Python uses **the space at the start of a line** to mark blocks, instead of the curly braces of other languages:

```try python
age = 20
if age >= 18:
    print("adult")
    print("this line is inside the condition too")
print("this line is outside the condition")
```

:::warning Indentation is required
Forgetting the indentation after `if` or `for` raises an `IndentationError`. Always use four spaces.
:::

## Comments

A comment starts with `#`, and the interpreter ignores it when running:

```try python
# this is a comment
print("hello")  # a comment at the end of a line
```

```exercise python
? Complete the symbol that starts a comment
___ this comment is not run
= #
```

```quiz
? How does Python mark blocks of code?
- Curly braces {}
* Indentation
- The word end

? A comment in Python starts with #.
= true
```

# @lesson py-variables
title: Variables
summary: Creating variables, naming them, and multiple assignment.
---
A variable in Python is created as soon as you assign a value to it, with no special keyword:

```try python
name = "Sara"
age = 25
height = 1.65
print(name, age, height)
age = 26
print("New age:", age)
```

## Multiple assignment

```try python
x, y, z = 1, 2, 3
print(x, y, z)
a = b = 0
print(a, b)
x, y = y, x      # swap the two values
print(x, y)
```

## Naming rules

- It starts with a letter or `_`, never a digit.
- Upper and lower case differ.
- The usual style: lower-case words joined by `_`, such as `total_price`.

```exercise python
? Assign the number 10 to the variable count
count ___ 10
= =
```

```quiz
? Which variable name is valid?
- 2name
* user_name
- user-name

? In Python you need the keyword let to create a variable.
= false
```

# @lesson py-types
title: Data types
summary: str, int, float, bool and None, the type function, and conversion.
---
```reference python
str | Text | "hello"
int | Whole number | 42
float | Decimal number | 3.14
bool | Boolean | True, False
None | No value | x = None
list | List | [1, 2, 3]
tuple | Fixed sequence | (1, 2)
dict | Dictionary | {"a": 1}
set | Set without duplicates | {1, 2}
```

```try python
print(type("text"))
print(type(10))
print(type(2.5))
print(type(True))
print(type(None))
```

## Converting between types

```try python
print(int("42") + 1)
print(float("3.5") * 2)
print(str(100) + " dollars")
print(bool(0), bool(5))
```

:::warning You cannot add text and a number
`"Age: " + 25` raises an error. Turn the number into text: `"Age: " + str(25)`, or use an f-string as you will see in the strings lesson.
:::

```quiz
? What is the type of 3.14?
- int
* float
- str

? The value True is of type bool.
= true
```

# @lesson py-numbers
title: Numbers and operators
summary: Arithmetic, floor division, remainder, power and rounding.
---
```reference python
+ - * | Add, subtract, multiply | 7 * 3 → 21
/ | Division (always a float) | 7 / 2 → 3.5
// | Floor division | 7 // 2 → 3
% | Remainder | 7 % 2 → 1
** | Power | 2 ** 10 → 1024
round() | Rounding | round(3.14159, 2) → 3.14
abs() | Absolute value | abs(-5) → 5
max() / min() | Largest / smallest | max(3, 9, 4) → 9
```

```try python
price = 120
discount = 0.15
final = price * (1 - discount)
print("Final price:", final)
print("Rounded:", round(final, 1))
print("Is the number even?", 10 % 2 == 0)
print(2 ** 10)
```

## Short operators

```try python
score = 10
score += 5
score *= 2
print(score)
```

```exercise python
? Complete the code to get the floor division of 17 by 5
print(17 ___ 5)
= //
```

```quiz
? What is 7 / 2 in Python 3?
- 3
* 3.5
- 4

? The % operator gives the remainder of a division.
= true
```

# @lesson py-strings
title: Strings
summary: f-strings, slicing, and useful methods.
---
## f-strings

The easiest way to put values inside text:

```try python
name = "Omar"
score = 92.456
print(f"Student {name} scored {score:.1f}")
```

## Indexing and slicing

```try python
word = "Python"
print(word[0])      # first letter
print(word[-1])     # last letter
print(word[0:3])    # from 0 to 2
print(len(word))
```

## Useful methods

```try python
text = "  Hello Python  "
print(text.strip())
print(text.lower())
print(text.replace("Python", "World"))
print("a,b,c".split(","))
print("-".join(["2026", "11", "20"]))
print("Py" in "Python")
```

```reference python
len() | Length | len("abc") → 3
upper() / lower() | Upper / lower case | "a".upper()
strip() | Remove spaces at both ends | " a ".strip()
replace() | Replace | "a-b".replace("-", "+")
split() | Split into a list | "a b".split()
join() | Join a list into text | ",".join(["a", "b"])
find() | Position of a substring | "abc".find("c") → 2
startswith() | Starts with? | "abc".startswith("a")
in | Contains? | "b" in "abc"
```

```exercise python
? Complete the code to make an f-string
name = "Layla"
print(___"Hello {name}")
= f
```

```quiz
? What is "Python"[0]?
* "P"
- "y"
- "n"

? strip removes spaces from both ends of a string.
= true
```

# @lesson py-conditions
title: Conditions
summary: if, elif and else, logical operators, and one-line conditions.
---
```try python
temperature = 31
if temperature > 35:
    print("very hot")
elif temperature > 25:
    print("warm")
else:
    print("mild")
```

## Logical operators

`and`, `or` and `not`:

```try python
age = 22
has_id = True
if age >= 18 and has_id:
    print("entry allowed")
if not has_id:
    print("bring your ID")
```

## One-line condition

```try python
n = 7
kind = "even" if n % 2 == 0 else "odd"
print(kind)
```

```exercise python
? Complete the keyword that means "else if"
x = 0
if x > 0:
    print("positive")
___ x < 0:
    print("negative")
else:
    print("zero")
= elif
```

```quiz
? Which keyword adds another condition in Python?
- else if
* elif
- elseif

? and gives True only if both sides are True.
= true
```

# @lesson py-loops
title: Loops
summary: for with range, while, break and continue.
---
## for and range

```try python
for i in range(1, 6):
    print("Number", i)
```

`range(start, stop, step)` produces numbers from `start` up to, but not including, `stop`:

```try python
print(list(range(5)))
print(list(range(2, 10, 2)))
```

## Looping over a list

```try python
cities = ["Riyadh", "Dubai", "Cairo"]
for index, city in enumerate(cities, start=1):
    print(index, city)
```

## while

```try python
balance = 100
while balance > 0:
    balance -= 30
    print("Balance:", balance)
```

## break and continue

```try python
for n in range(1, 10):
    if n == 3:
        continue
    if n == 7:
        break
    print(n)
```

```exercise python
? Complete the code to print the numbers 0 to 4
for i in ___(5):
    print(i)
= range
```

```quiz
? What is the last number produced by range(1, 5)?
- 5
* 4
- 1

? continue skips the rest of the current pass and moves to the next.
= true
```

# @lesson py-lists
title: Lists
summary: Creating lists, adding and removing, sorting and slicing.
---
A **list** is an ordered collection that can change:

```try python
fruits = ["apple", "banana"]
fruits.append("orange")
fruits.insert(0, "grape")
print(fruits)
fruits.remove("banana")
last = fruits.pop()
print(fruits, "| removed:", last)
print(len(fruits), fruits[0])
```

## Sorting and slicing

```try python
nums = [5, 2, 9, 1, 7]
print(sorted(nums))
nums.sort(reverse=True)
print(nums)
print(nums[1:3])
print(sum(nums), max(nums), min(nums))
```

```reference python
append() | Add at the end | lst.append(4)
insert() | Add at a position | lst.insert(0, "a")
remove() | Remove a value | lst.remove("a")
pop() | Remove and return an item | lst.pop()
sort() | Sort the list itself | lst.sort()
sorted() | A sorted copy | sorted(lst)
reverse() | Reverse the order | lst.reverse()
index() | Position of a value | lst.index(9)
count() | How many times | lst.count(2)
len() / sum() | Length / total | sum(lst)
```

```exercise python
? Add 4 at the end of the list
nums = [1, 2, 3]
nums.___(4)
= append
```

```quiz
? What is the difference between sort() and sorted()?
* sort() sorts the list itself; sorted() returns a sorted copy
- There is no difference
- sorted() is only for text

? The index -1 points to the last item of a list.
= true
```

# @lesson py-tuples-sets
title: Tuples and sets
summary: Fixed tuples, sets without duplicates, and set operations.
---
## Tuple

Like a list, but it **cannot change** after it is created:

```try python
point = (10, 20)
x, y = point
print(x, y)
print(point[0])
```

## Set

No order and no duplicates; useful for removing repeats and comparing:

```try python
tags = {"python", "web", "python", "data"}
print(tags)
emails = ["a@x.com", "b@x.com", "a@x.com"]
print(set(emails))
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)   # intersection
print(a | b)   # union
print(a - b)   # difference
```

```quiz
? Which type cannot change its items after it is created?
- list
* tuple
- set

? A set removes repeated values automatically.
= true
```

# @lesson py-dicts
title: Dictionaries
summary: Keys and values, adding and updating, looping, and get.
---
A **dictionary** maps keys to values:

```try python
student = {"name": "Nour", "age": 21, "city": "Jeddah"}
print(student["name"])
student["age"] = 22            # update
student["major"] = "Computing" # add
print(student)
print(student.get("phone", "not found"))
```

## Looping over a dictionary

```try python
prices = {"pen": 5, "notebook": 12, "bag": 90}
for item, price in prices.items():
    print(f"{item}: {price} dollars")
print(list(prices.keys()))
print(sum(prices.values()))
```

## A list of dictionaries

```try python
employees = [
    {"name": "Ali", "salary": 8000},
    {"name": "Mona", "salary": 9500},
]
top = max(employees, key=lambda e: e["salary"])
print("Highest paid:", top["name"])
```

:::tip Use get
`d["key"]` raises an error if the key is missing, while `d.get("key", default)` returns a fallback value.
:::

```exercise python
? Read the value safely with a fallback
age = person.___("age", 0)
= get
```

```quiz
? Which method returns the key-value pairs?
- keys()
- values()
* items()

? A dictionary stores data as keys and values.
= true
```

# @lesson py-comprehensions
title: Comprehensions
summary: Building lists and dictionaries in one line.
---
A **list comprehension** is a short way to build a list from another:

```try python
nums = [1, 2, 3, 4, 5, 6]
squares = [n * n for n in nums]
evens = [n for n in nums if n % 2 == 0]
print(squares)
print(evens)
```

It is the same as:

```python
squares = []
for n in nums:
    squares.append(n * n)
```

## Dictionary and set

```try python
names = ["Sara", "Omar", "Layla"]
lengths = {name: len(name) for name in names}
print(lengths)
unique_lengths = {len(name) for name in names}
print(unique_lengths)
```

:::tip Do not overdo it
Comprehensions are great for simple transforms and filters. When one grows long and complex, use a normal loop so it stays readable.
:::

```exercise python
? Complete the code to build a list with each number doubled
doubled = [n * 2 ___ n in nums]
= for
```

```quiz
? What is [n for n in range(5) if n > 2]?
* [3, 4]
- [2, 3, 4]
- [0, 1, 2]

? A comprehension can build a dictionary too.
= true
```

# @lesson py-functions
title: Functions
summary: def, default and keyword arguments, return values, and lambda.
---
```try python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

print(greet("Sara"))
print(greet("Omar", greeting="Welcome"))
```

- `def` defines the function.
- The parameter `greeting` has a default value.
- Arguments can be passed by name: `greeting="Welcome"`.

## Returning several values

```try python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

low, high, avg = stats([4, 8, 15, 16])
print(low, high, avg)
```

## Any number of arguments

```try python
def total(*prices):
    return sum(prices)

print(total(10, 20, 30))
```

## lambda

A small function without a name:

```try python
square = lambda x: x * x
print(square(9))
words = ["apple", "fig", "watermelon"]
print(sorted(words, key=lambda w: len(w)))
```

```exercise python
? Complete the keyword that defines a function
___ add(a, b):
    return a + b
= def
```

```quiz
? What does return do?
* Gives back a result from the function
- Prints the result
- Repeats the function

? A Python function can return more than one value.
= true
```

# @lesson py-modules
title: Modules
summary: import, and the math, random and datetime modules.
---
A **module** is a file of ready-made functions. You import it with `import`:

```try python
import math
print(math.sqrt(144))
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))
```

```try python
import random
print(random.randint(1, 6))
print(random.choice(["red", "blue", "green"]))
```

```try python
from datetime import date, timedelta
today = date(2026, 11, 20)
print(today + timedelta(days=30))
print(today.strftime("%Y-%m-%d"))
```

## Ways to import

```reference python
import math | Import the whole module | math.sqrt(9)
from math import sqrt | Import one function | sqrt(9)
import math as m | A short name | m.pi
from datetime import date | A class from a module | date.today()
```

:::info Python libraries
Besides the built-in modules there are thousands of external libraries, such as `pandas` for data analysis and `requests` for the web, installed with `pip install`.
:::

```exercise python
? Complete the code to import the math module
___ math
print(math.pi)
= import
```

```quiz
? Which module contains the sqrt function?
* math
- random
- datetime

? from math import sqrt lets you use sqrt directly, without math.
= true
```

# @lesson py-errors
title: Handling errors
summary: try, except, else and finally, and raise.
---
```try python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    else:
        return result
    finally:
        print("Attempt finished")

print(safe_divide(10, 2))
print(safe_divide(1, 0))
```

## Common errors

```reference python
ValueError | Unsuitable value | int("abc")
TypeError | Unsuitable type | "a" + 1
ZeroDivisionError | Division by zero | 1 / 0
KeyError | Missing key | {}["x"]
IndexError | Index outside the list | [1][5]
FileNotFoundError | Missing file | open("x.txt")
```

## Raising an error yourself

```try python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age

try:
    set_age(-3)
except ValueError as e:
    print("Error:", e)
```

```exercise python
? Complete the code to catch the conversion error
try:
    n = int("abc")
___ ValueError:
    print("not a number")
= except
```

```quiz
? Which error does int("abc") raise?
* ValueError
- KeyError
- IndexError

? raise throws an error yourself.
= true
```

# @lesson py-classes
title: Classes and objects
summary: class, __init__ and self, attributes and methods, and inheritance.
---
A **class** is a template for creating objects that have data and behavior:

```try python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def __str__(self):
        return f"{self.owner}'s account: {self.balance} dollars"

acc = Account("Sara", 100)
acc.deposit(50)
print(acc)
```

- `__init__` runs when an object is created.
- `self` refers to the object itself.
- `__str__` decides how the object is printed.

## Inheritance

```try python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return f"{self.name} says: meow"

print(Cat("Mishmish").speak())
```

```exercise python
? Complete the keyword that defines a class
___ Car:
    pass
= class
```

```quiz
? When does __init__ run?
* When a new object is created
- When the object is deleted
- When the object is printed

? The class Cat(Animal) inherits from Animal.
= true
```

# @lesson py-files
title: Files
summary: Writing and reading, with, and file modes.
---
```try python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("First line\n")
    f.write("Second line\n")

with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

- `with` closes the file automatically when done, even if an error happens.
- `encoding="utf-8"` matters for text in any language, Arabic included.

```reference python
"r" | Read (the default) | open("a.txt")
"w" | Write (erases the old content) | open("a.txt", "w")
"a" | Append at the end | open("a.txt", "a")
read() | Read the whole file | f.read()
readlines() | A list of lines | f.readlines()
write() | Write text | f.write("text")
```

## CSV files

```try python
import csv
with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Ali", 30])
with open("people.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["age"])
```

:::info Files here are temporary
On this platform files are kept in your browser's memory while the code runs, and disappear afterwards.
:::

```quiz
? Which mode adds to the end of a file without erasing it?
- "w"
* "a"
- "r"

? with closes the file automatically.
= true
```

# @lesson py-reference
title: Python reference
summary: The most important keywords and built-in functions with an example for each.
type: Reference
---
Search the table for any keyword or function.

```reference python
print() | Print | print("hello")
input() | Read from the user (does not work in this editor) | name = input("Your name: ")
len() | Length | len([1, 2])
type() | Type | type(3)
int() / float() / str() | Conversion | int("5")
range() | A sequence of numbers | range(1, 10, 2)
if / elif / else | Condition | if x > 0: …
for / while | Loops | for i in range(3): …
break / continue | Loop control | break
def / return | Functions | def f(x): return x
lambda | Small function | lambda x: x * 2
class | Class | class A: …
import / from | Importing | from math import pi
try / except | Handle errors | try: … except ValueError: …
raise | Raise an error | raise ValueError("…")
with open() | Work with files | with open("a.txt") as f: …
list.append() | Add to a list | lst.append(1)
dict.get() | Safe read | d.get("k", 0)
sorted() | A sorted copy | sorted(lst)
sum() / min() / max() | Total, smallest, largest | sum([1, 2])
enumerate() | Item with its number | for i, x in enumerate(lst): …
zip() | Pair two lists | list(zip(a, b))
f"…" | Text with values | f"Age {age}"
in | Contains? | "a" in "abc"
None | No value | x = None
```

:::tip What next?
Try a small project: an expense tracker with a dictionary, or a number-guessing game with `random`. Then go on to the **SQL** course to learn to work with databases.
:::
