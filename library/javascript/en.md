# @lesson js-intro
title: JavaScript introduction
summary: What JavaScript is and what it can do.
---
**JavaScript** is the programming language that runs inside the browser. HTML builds the page, CSS styles it, and JavaScript makes it **interactive**: it responds to clicks, checks forms, changes content and fetches data from the server.

## Your first program

Press **Run**. What `console.log` prints shows under the editor:

```try javascript
console.log("Hello, JavaScript");
console.log(2 + 3);
```

## JavaScript changes the page

```try html
<p id="msg">The original text</p>
<button onclick="document.getElementById('msg').textContent = 'The text changed!'">Press</button>
```

:::info JavaScript is not Java
The names are alike, but they are two completely different languages. JavaScript runs in every browser with nothing to install, and on servers through Node.js.
:::

```quiz
? Where does JavaScript mainly run?
* Inside the browser
- Only inside the database
- Inside a CSS file

? JavaScript is the same language as Java.
= false
```

# @lesson js-output
title: Output
summary: console.log, alert boxes, and changing page content.
---
There are several ways to show results:

- `console.log()` prints to the console; the most used while learning and finding mistakes.
- `alert()` shows an alert box to the visitor.
- `element.textContent` changes the text of an element on the page.

```try javascript
console.log("text");
console.log("Sum:", 10 + 5);
console.log([1, 2, 3]);
console.log({ name: "Sara", age: 25 });
```

## Writing to the page

```try html
<p id="out"></p>
<script>
  document.getElementById("out").textContent = "I wrote this from JavaScript";
</script>
```

:::tip Open the developer tools
In any browser press `F12` and choose **Console** to see what `console.log` prints in your own pages.
:::

```exercise javascript
? Complete the line so it prints the word hello
console.___("hello");
= log
```

```quiz
? Which command prints to the console?
- print()
* console.log()
- echo()

? The textContent property changes the text of an element on the page.
= true
```

# @lesson js-variables
title: Variables
summary: let and const, and naming variables.
---
A **variable** is a name that holds a value for later use.

```try javascript
let city = "Riyadh";
const year = 2026;
console.log(city, year);
city = "Cairo";        // let can change
console.log(city);
```

- `let` for a variable whose value can change.
- `const` for a value that never changes after it is set.
- `var` is the old way; avoid it in new code.

## Naming rules

- A name starts with a letter, `_` or `$`, never a digit.
- Upper and lower case differ: `age` is not `Age`.
- A clear name is better: `totalPrice` instead of `x`.

```try javascript
const price = 50;
const quantity = 3;
const totalPrice = price * quantity;
console.log("Total:", totalPrice);
```

:::warning Changing a const is an error
`const year = 2026;` followed by `year = 2027;` throws an error. Use `const` by default and `let` only when you need to change the value.
:::

```exercise javascript
? Declare a constant named pi
___ pi = 3.14;
= const
```

```quiz
? Which keyword declares a variable whose value can change?
* let
- const
- static

? A variable name may start with a digit.
= false
```

# @lesson js-types
title: Data types
summary: Strings, numbers, booleans, undefined and null, and typeof.
---
```reference javascript
string | Text | "hello"
number | Whole or decimal number | 42, 3.14
boolean | True or false | true, false
undefined | A variable with no value | let x;
null | "Nothing", on purpose | let y = null;
object | An object | { name: "Ali" }
array | An array (its type is object) | [1, 2, 3]
```

The `typeof` operator tells you the type of a value:

```try javascript
console.log(typeof "text");
console.log(typeof 42);
console.log(typeof true);
let x;
console.log(typeof x);
console.log(typeof { a: 1 });
```

## Converting types

```try javascript
console.log(Number("10") + 5);   // 15
console.log("10" + 5);           // "105": strings are joined
console.log(String(99));
console.log(parseInt("42px"));   // 42
```

:::warning Careful with + and strings
`"10" + 5` gives `"105"` because `+` with a string joins strings. Turn the string into a number first with `Number()`.
:::

```quiz
? What is typeof 42?
- "string"
* "number"
- "integer"

? "10" + 5 gives 15.
= false
> The result is "105", because + with a string joins them.
```

# @lesson js-operators
title: Operators
summary: Arithmetic, assignment, comparison and logic.
---
```reference javascript
+ - * / | Arithmetic | 10 / 4 → 2.5
% | Remainder | 10 % 3 → 1
** | Power | 2 ** 3 → 8
+= -= | Assign with an operation | x += 5
=== | Equal (value and type) | 5 === 5 → true
!== | Not equal | 5 !== "5" → true
> < >= <= | Comparison | 3 > 2 → true
&& | And | true && false → false
|| | Or | true || false → true
! | Not | !true → false
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

:::tip Always use ===
`==` converts types before comparing, which sometimes gives strange results. `===` compares value and type together.
:::

```exercise javascript
? Complete the line to get the remainder of 10 divided by 3
console.log(10 ___ 3);
= %
```

```quiz
? What is 2 ** 3?
- 6
* 8
- 9

? The comparison 5 === "5" is true.
= false
```

# @lesson js-strings
title: Strings
summary: Template literals, length, searching, slicing and replacing.
---
A string is written between `"…"`, `'…'` or backticks `` ` `` (template literals).

## Template literals

They let you put values inside text with `${ }`:

```try javascript
const name = "Layla";
const age = 22;
console.log(`My name is ${name} and I am ${age}`);
```

## Useful methods

```try javascript
const text = "Hello JavaScript";
console.log(text.length);
console.log(text.toUpperCase());
console.log(text.includes("Java"));
console.log(text.slice(0, 5));
console.log(text.replace("Hello", "Hi"));
console.log("  spaces  ".trim());
console.log("a,b,c".split(","));
```

```reference javascript
length | Number of characters | "abc".length → 3
toUpperCase() | Upper case | "a".toUpperCase()
includes() | Does it contain? | "abc".includes("b")
indexOf() | Position of the first match | "abc".indexOf("c") → 2
slice(a, b) | Part of the string | "hello".slice(1, 3)
replace() | Replace | "a-b".replace("-", "+")
trim() | Remove spaces at both ends | " a ".trim()
split() | Split into an array | "a,b".split(",")
```

```exercise javascript
? Complete the template literal to insert the variable name
console.log(`Hello ${___}`);
= name
```

```quiz
? What is "abc".length?
- 2
* 3
- 4

? Which method removes spaces from both ends of a string?
- slice()
* trim()
- split()
```

# @lesson js-conditions
title: Conditions
summary: if, else if and else, the ternary operator, and switch.
---
A condition lets the program make a decision:

```try javascript
const hour = 14;
if (hour < 12) {
  console.log("Good morning");
} else if (hour < 18) {
  console.log("Good afternoon");
} else {
  console.log("Good evening");
}
```

## The ternary operator

A short form of a simple `if/else`:

```try javascript
const age = 20;
const status = age >= 18 ? "adult" : "minor";
console.log(status);
```

## switch

Useful when one value is compared with several possibilities:

```try javascript
const day = 5;
switch (day) {
  case 5:
    console.log("Friday");
    break;
  case 6:
    console.log("Saturday");
    break;
  default:
    console.log("Another day");
}
```

:::warning Do not forget break
Without `break`, `switch` also runs the cases that follow.
:::

```exercise javascript
? Complete the condition
const n = 7;
___ (n > 5) {
  console.log("big");
}
= if
```

```quiz
? What is: 10 > 5 ? "yes" : "no"
* "yes"
- "no"
- An error

? In a switch, break stops the following cases from running.
= true
```

# @lesson js-loops
title: Loops
summary: for, while, for...of, break and continue.
---
A loop repeats code several times.

## for

```try javascript
for (let i = 1; i <= 5; i++) {
  console.log("Number", i);
}
```

## while

```try javascript
let n = 3;
while (n > 0) {
  console.log("Countdown:", n);
  n--;
}
console.log("Go!");
```

## for...of over an array

```try javascript
const fruits = ["apple", "banana", "orange"];
for (const fruit of fruits) {
  console.log(fruit);
}
```

## break and continue

```try javascript
for (let i = 1; i <= 10; i++) {
  if (i === 3) continue;  // skip 3
  if (i === 6) break;     // stop at 6
  console.log(i);
}
```

:::warning Infinite loops
If the condition never becomes false, the loop never stops. The platform's editor stops it after a few seconds, but in your real page the page will freeze.
:::

```exercise javascript
? Complete the loop so it prints 0 to 4
for (let i = 0; i < 5; i___) {
  console.log(i);
}
= ++
```

```quiz
? Which keyword stops a loop at once?
* break
- continue
- stop

? for...of goes through the items of an array one by one.
= true
```

# @lesson js-functions
title: Functions
summary: Defining a function, parameters, return values, and arrow functions.
---
A **function** is a named block of code: you write it once and call it whenever you like.

```try javascript
function greet(name) {
  return "Hello, " + name;
}
console.log(greet("Sara"));
console.log(greet("Omar"));
```

- `name` is a **parameter**: a value you pass to the function.
- `return` gives back the result and ends the function.

## Default values

```try javascript
function area(width, height = 1) {
  return width * height;
}
console.log(area(5, 4));
console.log(area(5));
```

## Arrow functions

A short form you will see everywhere:

```try javascript
const square = (x) => x * x;
const add = (a, b) => a + b;
console.log(square(6), add(2, 3));
```

```exercise javascript
? Complete the function so it returns double the number
function double(n) {
  ___ n * 2;
}
= return
```

```quiz
? What does return do?
- Prints a value
* Gives back a value from the function
- Repeats the function

? (a, b) => a + b is an arrow function that adds two numbers.
= true
```

# @lesson js-arrays
title: Arrays
summary: Creating an array, reading items, adding and removing.
---
An **array** is an ordered list of values:

```try javascript
const colors = ["red", "green", "blue"];
console.log(colors[0]);        // the first item: indexes start at 0
console.log(colors.length);
colors.push("yellow");         // add at the end
console.log(colors);
colors.pop();                  // remove the last
colors.unshift("black");       // add at the start
console.log(colors);
```

```reference javascript
length | Number of items | arr.length
push() | Add at the end | arr.push(4)
pop() | Remove the last | arr.pop()
unshift() | Add at the start | arr.unshift(0)
shift() | Remove the first | arr.shift()
includes() | Does it contain? | arr.includes(2)
indexOf() | Position of an item | arr.indexOf(2)
join() | Join into a string | arr.join(", ")
slice() | Copy of a part | arr.slice(1, 3)
```

:::info Indexes start at zero
The first item is `arr[0]` and the last is `arr[arr.length - 1]`.
:::

```exercise javascript
? Add the item 4 at the end of the array
const nums = [1, 2, 3];
nums.___(4);
= push
```

```quiz
? What is the index of the first item in an array?
* 0
- 1
- -1

? pop removes the last item.
= true
```

# @lesson js-array-methods
title: Array methods
summary: forEach, map, filter, find, reduce and sort.
---
These methods make working with data short and clear:

```try javascript
const prices = [120, 45, 300, 80];

prices.forEach((p) => console.log("Price:", p));

const withTax = prices.map((p) => p * 1.15);
console.log("With tax:", withTax);

const cheap = prices.filter((p) => p < 100);
console.log("Cheap:", cheap);

const first = prices.find((p) => p > 100);
console.log("First price over 100:", first);

const total = prices.reduce((sum, p) => sum + p, 0);
console.log("Total:", total);

console.log("Sorted:", [...prices].sort((a, b) => a - b));
```

```reference javascript
forEach() | Run for every item | arr.forEach(x => console.log(x))
map() | New array after changing every item | arr.map(x => x * 2)
filter() | The items that pass a test | arr.filter(x => x > 0)
find() | The first item that passes | arr.find(x => x.id === 3)
some() / every() | Do some / all pass? | arr.some(x => x < 0)
reduce() | Fold the array into one value | arr.reduce((s, x) => s + x, 0)
sort() | Sort (changes the original) | arr.sort((a, b) => a - b)
```

:::warning sort with numbers
`[10, 9, 1].sort()` sorts as strings and gives `[1, 10, 9]`. For numbers pass a compare function: `sort((a, b) => a - b)`.
:::

```exercise javascript
? Keep only the even numbers
const evens = [1, 2, 3, 4].___((n) => n % 2 === 0);
= filter
```

```quiz
? Which method returns a new array after changing every item?
* map()
- forEach()
- find()

? reduce folds the items of an array into one value.
= true
```

# @lesson js-objects
title: Objects
summary: Properties, reading them, methods, and looping over properties.
---
An **object** groups related data as "key: value" pairs:

```try javascript
const student = {
  name: "Nour",
  age: 21,
  courses: ["HTML", "CSS"],
  greet() {
    return "I am " + this.name;
  },
};

console.log(student.name);
console.log(student["age"]);
console.log(student.greet());
student.city = "Jeddah";        // add a property
console.log(student);
```

## Looping over properties

```try javascript
const product = { name: "pen", price: 5, stock: 120 };
for (const [key, value] of Object.entries(product)) {
  console.log(key, "=", value);
}
console.log(Object.keys(product));
```

## An array of objects

The most common shape of real data:

```try javascript
const users = [
  { name: "Ali", active: true },
  { name: "Mona", active: false },
  { name: "Khaled", active: true },
];
const names = users.filter((u) => u.active).map((u) => u.name);
console.log(names);
```

```exercise javascript
? Print the brand property of the object
const car = { brand: "Toyota" };
console.log(car.___);
= brand
```

```quiz
? How do you read the age property of the object person?
* person.age
- person->age
- person(age)

? An object can contain functions.
= true
```

# @lesson js-dom
title: Controlling the page (DOM)
summary: Selecting elements, changing their text and style, and creating new ones.
---
The **DOM** is the page represented as objects that JavaScript can read and change.

## Selecting elements

```reference javascript
getElementById() | An element by its id | document.getElementById("title")
querySelector() | The first match of a CSS selector | document.querySelector(".card")
querySelectorAll() | Every match | document.querySelectorAll("li")
```

## Changing things

```try html
<h2 id="title">A heading</h2>
<ul id="list"><li>First</li></ul>
<script>
  const title = document.getElementById("title");
  title.textContent = "A new heading";
  title.style.color = "#4338ca";
  title.classList.add("big");

  const li = document.createElement("li");
  li.textContent = "An item added by JavaScript";
  document.getElementById("list").append(li);
</script>
```

:::warning textContent or innerHTML?
`textContent` sets plain text and is safe. `innerHTML` treats the text as HTML; never use it with text typed by a user, because it can let harmful code in.
:::

```exercise javascript
? Select the first element with the class card
const card = document.___(".card");
= querySelector
```

```quiz
? Which method returns every element that matches a CSS selector?
- getElementById()
- querySelector()
* querySelectorAll()

? Putting text typed by a user into innerHTML is always safe.
= false
> The text may contain harmful code; use textContent.
```

# @lesson js-events
title: Events
summary: Clicks, typing and submitting, and addEventListener.
---
An **event** is something that happens on the page: a click, typing, scrolling, a form being sent… and JavaScript responds with a function.

```try html
<button id="btn">Press</button>
<p id="count">0</p>
<script>
  let clicks = 0;
  document.getElementById("btn").addEventListener("click", () => {
    clicks++;
    document.getElementById("count").textContent = clicks;
  });
</script>
```

## Typing

```try html
<input id="name" placeholder="Type your name">
<p id="hello"></p>
<script>
  document.getElementById("name").addEventListener("input", (e) => {
    document.getElementById("hello").textContent = "Hello " + e.target.value;
  });
</script>
```

## Stopping a form's default submit

```try html
<form id="f"><input name="q" required><button>Search</button></form>
<p id="r"></p>
<script>
  document.getElementById("f").addEventListener("submit", (e) => {
    e.preventDefault();
    document.getElementById("r").textContent = "You are searching for: " + e.target.q.value;
  });
</script>
```

```reference javascript
click | A click | btn.addEventListener("click", fn)
input | A field changes while typing | input.addEventListener("input", fn)
change | A value changes when done | select.addEventListener("change", fn)
submit | A form is sent | form.addEventListener("submit", fn)
keydown | A key is pressed | document.addEventListener("keydown", fn)
mouseover | The mouse moves over | el.addEventListener("mouseover", fn)
```

```exercise javascript
? Complete the line to run a function on click
btn.addEventListener("___", () => console.log("click"));
= click
```

```quiz
? Which call stops a form from reloading the page when it is sent?
* e.preventDefault()
- e.stop()
- always return false

? The input event fires while typing in a field.
= true
```

# @lesson js-json
title: JSON
summary: Turning objects into text and back.
---
**JSON** is a text format for exchanging data between the browser and the server, and it looks like JavaScript objects.

```try javascript
const user = { name: "Salma", age: 30, skills: ["SQL", "Python"] };

const text = JSON.stringify(user);
console.log(text);
console.log(typeof text);

const back = JSON.parse(text);
console.log(back.skills[0]);
```

- `JSON.stringify()` turns an object into text.
- `JSON.parse()` turns JSON text into an object.

## JSON rules

- Keys go in double quotes: `"name"`.
- Values: a string, a number, `true`/`false`, `null`, an array or an object.
- No comments, no functions, no trailing comma.

```try javascript
try {
  JSON.parse("{name: 'wrong'}");
} catch (e) {
  console.log("Invalid JSON:", e.message);
}
```

```quiz
? Which function turns JSON text into an object?
- JSON.stringify()
* JSON.parse()
- JSON.toObject()

? In JSON, keys are written in double quotes.
= true
```

# @lesson js-errors
title: Handling errors
summary: try, catch and finally, and throwing errors with throw.
---
Some operations can fail: bad data, a lost network… Instead of letting the program stop, catch the error and act:

```try javascript
function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}

try {
  console.log(divide(10, 2));
  console.log(divide(5, 0));
} catch (error) {
  console.log("Something went wrong:", error.message);
} finally {
  console.log("Done");
}
```

- `try` the code that may fail.
- `catch` what happens on an error.
- `finally` runs either way.
- `throw` raises an error yourself.

:::tip Clear messages
Write a message in `throw new Error()` that says what went wrong and how to fix it; you will thank yourself later.
:::

```exercise javascript
? Complete the code to catch the error
try {
  JSON.parse("{");
} ___ (e) {
  console.log("error");
}
= catch
```

```quiz
? Which part runs whether or not an error happens?
- try
- catch
* finally

? You can raise an error yourself with throw.
= true
```

# @lesson js-async
title: Asynchronous code
summary: setTimeout, promises, async and await, and fetch.
---
Some operations take time: a timer, or a request to the server. JavaScript does not stop and wait; it carries on and comes back to the result when it is ready.

## setTimeout

```try javascript
console.log("1: before");
setTimeout(() => console.log("3: one second later"), 1000);
console.log("2: right away");
```

## Promises and async/await

A **Promise** is a promise of a result that comes later. `await` waits for a promise inside an `async` function:

```try javascript
function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function run() {
  console.log("Started");
  await wait(500);
  console.log("Half a second later");
  await wait(500);
  console.log("Finished");
}
run();
```

## Fetching data with fetch

```js
async function loadUsers() {
  try {
    const response = await fetch("https://example.com/api/users");
    const users = await response.json();
    console.log(users);
  } catch (e) {
    console.log("The request failed:", e.message);
  }
}
```

:::info Why does fetch not work here?
The platform's editor runs code in an isolated box with no internet, for safety. Try the `fetch` example in your own page.
:::

```exercise javascript
? Complete the code to wait for the promise inside the function
async function go() {
  ___ wait(100);
}
= await
```

```quiz
? In what order do these print: console.log(1), setTimeout(() => console.log(2), 0), console.log(3)?
- 1, 2, 3
* 1, 3, 2
- 2, 1, 3
> setTimeout waits until the current code has finished, even with a delay of 0.

? await can be used inside an async function.
= true
```

# @lesson js-reference
title: JavaScript reference
summary: The most important keywords and functions with an example for each.
type: Reference
---
Search the table for any keyword or function.

```reference javascript
let / const | Declare a variable / constant | const x = 5;
if / else | Condition | if (x > 0) { … } else { … }
switch | Pick from cases | switch (v) { case 1: …; break; }
for | Counting loop | for (let i = 0; i < 3; i++) { … }
for...of | Loop over items | for (const x of arr) { … }
while | Loop with a condition | while (n > 0) { n--; }
function | Function | function f(a) { return a; }
=> | Arrow function | const f = (a) => a * 2;
return | Give back a value | return total;
console.log() | Print | console.log("hello");
typeof | Type of a value | typeof 42
=== | Strictly equal | a === b
`${}` | Template literal | `Hello ${name}`
Array.push() | Add to an array | arr.push(1)
Array.map() | Change the items | arr.map(x => x * 2)
Array.filter() | Filter | arr.filter(x => x > 0)
Array.reduce() | Fold | arr.reduce((s, x) => s + x, 0)
Object.keys() | Keys of an object | Object.keys(obj)
JSON.stringify() | Object to text | JSON.stringify(obj)
JSON.parse() | Text to object | JSON.parse(text)
document.querySelector() | Select an element | document.querySelector("#id")
addEventListener() | Listen for an event | btn.addEventListener("click", f)
textContent | Text of an element | el.textContent = "text"
classList.add() | Add a class | el.classList.add("active")
try / catch | Handle errors | try { … } catch (e) { … }
throw | Raise an error | throw new Error("…")
setTimeout() | Run after a delay | setTimeout(f, 1000)
async / await | Wait for a promise | const r = await fetch(url);
fetch() | Request to the server | fetch("/api/data")
```

:::tip What next?
You have finished the JavaScript basics. Try a small project: a to-do list that adds and removes items, or a simple calculator.
:::
