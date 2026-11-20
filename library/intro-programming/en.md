# @lesson prog-what
title: What programming is
summary: Programs, languages, and how a computer follows instructions.
---
A **program** is a list of exact instructions that a computer follows, one step at a time. **Programming** is writing those instructions in a language the computer can run, such as Python, JavaScript or Java.

Computers are fast but very literal: they do exactly what you wrote, not what you meant. A large part of programming is learning to say precisely what you want.

```try python
print("Hello! This is my first program.")
print("2 + 3 =", 2 + 3)
print("Done.")
```

The computer ran three instructions, top to bottom. Change the text or the numbers and run it again; experimenting is the fastest way to learn.

:::info How this course works
Examples here use **Python** because it reads almost like English and runs right in your browser. The ideas (variables, decisions, loops, functions) are the same in every language you learn later.
:::

```quiz
? What is a program?
* A list of exact instructions that a computer follows
- A computer screen
- A type of internet connection

? A computer does what you meant, even if you wrote something slightly different.
= false
> Computers follow instructions exactly as written, which is why precise instructions matter.
```

# @lesson prog-algorithms
title: Algorithms and thinking in steps
summary: Breaking a problem into clear steps, pseudocode, and flowcharts.
---
An **algorithm** is a step-by-step recipe for solving a problem. Before writing code, good programmers often write the steps in plain words, called **pseudocode**.

Problem: find the largest number in a list.

```text
start with the first number as "largest"
for each other number:
    if it is bigger than "largest":
        it becomes the new "largest"
at the end, "largest" is the answer
```

The same algorithm in Python:

```try python
numbers = [12, 45, 7, 89, 23]
largest = numbers[0]
for n in numbers:
    if n > largest:
        largest = n
print("The largest number is", largest)
```

A **flowchart** draws the same steps as boxes (actions) and diamonds (questions with yes/no arrows). Both pseudocode and flowcharts help you plan before you type.

:::tip Break it down
If a problem feels too big, split it: "make a quiz app" becomes "store questions", "show one question", "check the answer", "count the score". Each small step is easy to code.
:::

```quiz
? What is an algorithm?
* A step-by-step method for solving a problem
- A type of computer
- A programming language

? Pseudocode must follow the exact rules of a programming language.
= false
> Pseudocode is plain language used for planning; it does not have to run.
```

# @lesson prog-variables
title: Variables and data types
summary: Storing values with names: numbers, text and true/false.
---
A **variable** is a name for a value, like a labelled box. You can read it later and change it.

```try python
name = "Sara"          # text (a string)
age = 25               # a whole number (an integer)
height = 1.68          # a decimal number (a float)
is_student = True      # true or false (a boolean)

print(name, "is", age, "years old")
age = age + 1          # change the value
print("Next year:", age)
print(type(name), type(age), type(height), type(is_student))

price = 40
quantity = 3
total = price * quantity
print("Total to pay:", total)
```

| Type | Examples | Used for |
|---|---|---|
| Integer | `7`, `-3`, `2026` | Counting, whole amounts |
| Float | `3.14`, `0.5` | Measurements, prices |
| String | `"hello"`, `"سارة"` | Text |
| Boolean | `True`, `False` | Yes/no answers |

:::tip Good names
Choose names that say what the value means: `total_price` is clearer than `tp` or `x`. Future you will thank you.
:::

```exercise python
? Store the number 10 in a variable called score
score ___ 10
= =
```

```quiz
? Which value is a string?
* "42"
- 42
- True

? A variable's value can change while the program runs.
= true
```

# @lesson prog-operators
title: Operators and expressions
summary: Arithmetic, comparisons, and combining conditions with and / or / not.
---
```try python
a = 17
b = 5
print("sum", a + b, "difference", a - b)
print("product", a * b, "division", a / b)
print("whole division", a // b, "remainder", a % b)
print("power", 2 ** 8)

print(a > b, a == b, a != b)       # comparisons give True or False
age = 20
has_ticket = True
print(age >= 18 and has_ticket)    # both must be true
print(age < 12 or age > 65)        # at least one must be true
print(not has_ticket)

greeting = "Hello, " + "world"     # + joins text
print(greeting, "!" * 3)
```

```reference python
+ - * / | Arithmetic | 7 / 2 gives 3.5
// / % | Whole division / remainder | 7 % 2 gives 1
** | Power | 2 ** 3 gives 8
== != < > <= >= | Comparisons (give True/False) | age >= 18
and / or / not | Combine conditions | x > 0 and x < 10
+ on text | Join text | "a" + "b" gives "ab"
```

:::warning = and ==
A single `=` stores a value in a variable. A double `==` asks a question: "are these equal?". Mixing them up is one of the most common beginner mistakes.
:::

```exercise python
? Check whether x is equal to 10
print(x ___ 10)
= ==
```

```quiz
? What does 10 % 3 give?
* 1
- 3
- 3.33

? True and False gives True.
= false
```

# @lesson prog-decisions
title: Making decisions
summary: if, elif and else: running different code depending on conditions.
---
Programs often have to choose: "if it is raining, take an umbrella, otherwise wear sunglasses."

```try python
temperature = 31

if temperature > 30:
    print("It is hot: drink water")
elif temperature > 18:
    print("Nice weather")
else:
    print("Take a jacket")

score = 72
if score >= 50:
    print("Passed")
    if score >= 85:
        print("with distinction")
else:
    print("Try again")

password = "secret123"
if len(password) < 8:
    print("Password too short")
else:
    print("Password length OK")
```

- The condition after `if` is checked first; `elif` (else-if) is checked only if the earlier ones were false; `else` runs when none were true.
- In Python, the **indentation** (the spaces at the start of the line) shows which lines belong to each branch.

```exercise python
? Complete the keyword that runs when no condition was true
if x > 0:
    print("positive")
___:
    print("not positive")
= else
```

```quiz
? When does the code under elif run?
* When the earlier conditions were false and its own condition is true
- Always
- Only when the if condition is true

? Indentation tells Python which lines belong to an if block.
= true
```

# @lesson prog-loops
title: Loops
summary: Repeating work with for and while, and counting and adding in a loop.
---
A **loop** repeats instructions, so you do not have to write them again and again.

```try python
for i in range(1, 6):              # 1, 2, 3, 4, 5
    print("Lap", i)

shopping = ["bread", "milk", "eggs"]
for item in shopping:
    print("Buy", item)

total = 0
for price in [12, 30, 8]:
    total = total + price          # add up as we go
print("Total:", total)

count = 3
while count > 0:                   # repeat while the condition is true
    print(count)
    count = count - 1
print("Go!")

for n in range(1, 20):
    if n % 7 == 0:
        print("First multiple of 7:", n)
        break                      # stop the loop early
```

```reference python
for x in list | Do something for every item | for name in names:
range(a, b) | Numbers from a up to b-1 | range(1, 11)
while condition | Repeat while it is true | while lives > 0:
break | Leave the loop now | if found: break
continue | Skip to the next round | if n < 0: continue
```

:::warning Infinite loops
If a `while` condition never becomes false, the loop never stops. Make sure something inside the loop changes the condition, like `count = count - 1` above.
:::

```exercise python
? Repeat for the numbers 0 to 4
for i in ___(5):
    print(i)
= range
```

```quiz
? Which numbers does range(1, 4) give?
* 1, 2 and 3
- 1, 2, 3 and 4
- 0, 1, 2 and 3
```

# @lesson prog-functions
title: Functions
summary: Packaging steps under a name, parameters, and return values.
---
A **function** is a named group of steps you can run whenever you need it. It can take **inputs** (parameters) and give back a **result** (return value).

```try python
def greet(name):
    print("Welcome,", name)

greet("Sara")
greet("Omar")

def area_of_rectangle(width, height):
    return width * height

room = area_of_rectangle(4, 5)
print("Room area:", room, "square metres")

def price_with_tax(price, tax_rate=0.14):    # a default value
    return round(price * (1 + tax_rate), 2)

print(price_with_tax(100))
print(price_with_tax(100, 0.05))

def is_even(number):
    return number % 2 == 0

for n in [3, 8, 11]:
    print(n, "is even?", is_even(n))
```

:::tip Why functions?
Functions let you write something once and reuse it, give a clear name to a piece of logic, and fix a bug in one place instead of many.
:::

```exercise python
? Write the keyword that defines a function in Python
___ double(x):
    return x * 2
= def
```

```quiz
? What does return do?
* Sends a result back to the code that called the function
- Prints the result on the screen
- Restarts the function

? A function can be called many times with different inputs.
= true
```

# @lesson prog-lists
title: Lists and dictionaries
summary: Storing many values: lists for order, dictionaries for lookups.
---
```try python
grades = [88, 92, 75, 60]
print("First grade:", grades[0])          # counting starts at 0
grades.append(95)
print("All grades:", grades)
print("How many:", len(grades))
print("Average:", sum(grades) / len(grades))
print("Best:", max(grades), "Worst:", min(grades))

phone_book = {"Sara": "0100-111", "Omar": "0122-222"}
phone_book["Lina"] = "0111-333"           # add an entry
print("Omar's number:", phone_book["Omar"])
for person, number in phone_book.items():
    print(person, "->", number)
print("Is Ali in the book?", "Ali" in phone_book)

students = [
    {"name": "Sara", "grade": 91},
    {"name": "Omar", "grade": 78},
]
for s in students:
    print(s["name"], "passed" if s["grade"] >= 50 else "failed")
```

| | List | Dictionary |
|---|---|---|
| Looks like | `[10, 20, 30]` | `{"Sara": 91, "Omar": 78}` |
| Find items by | Position (0, 1, 2...) | Key (a name) |
| Good for | Ordered collections | Looking things up |

```exercise python
? Add the number 7 to the end of the list nums
nums.___(7)
= append
```

```quiz
? What is the position of the first item in a Python list?
* 0
- 1
- -1
```

# @lesson prog-debugging
title: Errors and debugging
summary: Reading error messages, common mistakes, and finding bugs step by step.
---
Every programmer makes mistakes. A **bug** is a mistake in a program; **debugging** is finding and fixing it.

There are three kinds of errors:

1. **Syntax errors**: the code breaks the language's rules (a missing `:` or bracket). The program does not start.
2. **Runtime errors**: the code starts but something impossible happens, like dividing by zero.
3. **Logic errors**: the program runs, but gives the wrong answer.

```try python
prices = [10, 20, 30]

try:
    print(prices[3])                  # there is no fourth item
except IndexError as error:
    print("Runtime error:", error)

try:
    print(100 / 0)
except ZeroDivisionError as error:
    print("Runtime error:", error)

# a logic error: the average should be 20
total = 0
for p in prices:
    total = total + p
average = total / 2                   # bug: should divide by len(prices)
print("Average (wrong):", average)
print("Average (fixed):", total / len(prices))

# print the values to see what is happening
for i, p in enumerate(prices):
    print("step", i, "price", p)
```

:::tip How to debug
Read the error message: it names the problem and the line. Then print values to check what the program really sees, test with small inputs whose answer you know, and change one thing at a time.
:::

```quiz
? A program runs without errors but gives the wrong total. What kind of error is it?
* A logic error
- A syntax error
- A runtime error

? Error messages usually tell you the line where the problem happened.
= true
```

# @lesson prog-project
title: Project: a grade calculator
summary: Variables, lists, loops, decisions and functions in one small program.
---
The program below takes a class's results, computes each student's average and letter grade, and prints a short report.

```try python
def average(numbers):
    return sum(numbers) / len(numbers)

def letter(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 65:
        return "C"
    elif avg >= 50:
        return "D"
    return "F"

results = {
    "Sara": [95, 88, 92],
    "Omar": [72, 65, 80],
    "Lina": [45, 52, 38],
}

passed = 0
best_name, best_avg = None, -1
for name, marks in results.items():
    avg = average(marks)
    grade = letter(avg)
    print(f"{name:6} average {avg:5.1f}  grade {grade}")
    if grade != "F":
        passed += 1
    if avg > best_avg:
        best_name, best_avg = name, avg

print("Passed:", passed, "of", len(results))
print("Top student:", best_name)
```

:::tip Make it yours
Add a new student, change the grade boundaries, or print the class average. Then add a rule: a student with any mark under 40 must retake the course.
:::

```quiz
? Why are average and letter written as separate functions?
* Each does one clear job and can be reused and tested on its own
- Python requires every program to have two functions
- Functions make the program run faster
```

# @lesson prog-next
title: What to learn next
summary: Choosing a path: web, data, apps or systems, and how to keep improving.
---
You now know the core ideas shared by almost every language: **variables, operators, decisions, loops, functions, lists and debugging**. Choose a path and go deeper:

| If you want to build... | Start with |
|---|---|
| Websites | HTML, CSS, then JavaScript |
| Data analysis and AI | Python, then NumPy and pandas |
| Business databases and reports | SQL |
| Android apps | Kotlin |
| Fast systems and tools | Go, Rust or C++ |
| Enterprise software | Java or C# |

How to keep improving:

- **Practise every day**, even for 20 minutes; small regular practice beats long rare sessions.
- **Build small projects** you care about: a budget tracker, a quiz, a to-do list.
- **Read other people's code** and error messages, and look up what you do not understand.
- **Use version control** (Git) from the start, so you can always go back.

```reference python
variable = value | Store a value | total = 0
if / elif / else | Decide | if x > 0:
for / while | Repeat | for item in items:
def f(x): return ... | Reusable function | def square(x): return x * x
[a, b] / {"k": v} | List / dictionary | names.append("Sara")
try / except | Handle errors | except ValueError:
print() | Show a value | print("total", total)
```

```quiz
? Which ideas appear in almost every programming language?
* Variables, decisions, loops and functions
- Only HTML tags
- Only spreadsheet formulas
```
