# @lesson ts-intro
title: TypeScript introduction
summary: What TypeScript adds to JavaScript, and your first typed program.
---
**TypeScript** is JavaScript with **types**. You describe what kind of value each variable, parameter and object holds, and the TypeScript compiler (`tsc`) or your editor warns you about mistakes *before* the code runs. The output is plain JavaScript, so it runs anywhere JavaScript runs.

```try html ts
<script type="text/typescript">
function greet(name: string): string {
  return "Hello, " + name;
}
console.log(greet("Sara"));
console.log(6 * 7);
// greet(42);   // error in the editor: number is not assignable to string
</script>
```

- `name: string` says the parameter must be a string; `): string` says what the function returns.
- The types disappear when TypeScript is turned into JavaScript.

:::info How the examples run
Here the browser turns your TypeScript into JavaScript and runs it, then shows `console.log` output above. This quick mode removes the types without checking them; type errors (shown as comments in the examples) appear in an editor such as VS Code, or when you run `npx tsc`.
:::

```quiz
? When does TypeScript report a type mistake?
* Before the code runs, in the editor or the compiler
- Only after the program crashes
- Never, types are only comments

? TypeScript code is turned into plain JavaScript to run.
= true
```

# @lesson ts-types
title: Basic types
summary: string, number, boolean, arrays, any, unknown and type inference.
---
```try html ts
<script type="text/typescript">
let city: string = "Cairo";
let age: number = 25;
let active: boolean = true;
let scores: number[] = [90, 75, 88];
let tags: Array<string> = ["new", "sale"];
let point: [number, number] = [3, 4];      // tuple: fixed length and types

let total = 10;          // inferred as number, no annotation needed
total += 5;
// total = "fifteen";    // error: string is not assignable to number

let data: unknown = JSON.parse('{"id": 7}');
if (typeof data === "object" && data !== null && "id" in data) {
  console.log("id found");
}

console.log(city, age, active, scores.length, tags[0], point[1], total);
</script>
```

```reference typescript
string / number / boolean | Basic types | let n: number = 1;
T[] / Array<T> | Arrays | let names: string[] = [];
[A, B] | Tuple | let p: [number, string] = [1, "a"];
any | Turns checking off (avoid) | let x: any;
unknown | Safe "anything": check before use | let v: unknown;
null / undefined | Missing values | let m: string | null = null;
inference | The type comes from the value | let x = 5; // number
```

:::tip Let inference work
You rarely need to annotate local variables: `let total = 10` is already a `number`. Annotate function parameters, return types and public data shapes.
:::

```exercise typescript
? Declare prices as an array of numbers
let prices: ___ = [10, 20];
= number[] | Array<number>
```

```quiz
? Which type is safest for a value whose shape you do not know yet?
* unknown
- any
- object

? let count = 3; gives count the type number without an annotation.
= true
```

# @lesson ts-functions
title: Functions
summary: Parameter and return types, optional and default parameters, function types.
---
```try html ts
<script type="text/typescript">
function add(a: number, b: number): number {
  return a + b;
}

function greet(name: string, greeting: string = "Hello", title?: string): string {
  const who = title ? title + " " + name : name;
  return greeting + ", " + who;
}

const square = (n: number): number => n * n;

function sum(...nums: number[]): number {
  return nums.reduce((t, n) => t + n, 0);
}

type Operation = (a: number, b: number) => number;
const multiply: Operation = (a, b) => a * b;     // a and b are numbers here

function log(message: string): void {
  console.log("[log] " + message);
}

console.log(add(2, 3), square(4), sum(1, 2, 3), multiply(6, 7));
console.log(greet("Sara"), "|", greet("Omar", "Welcome", "Dr."));
log("done");
// add("2", 3);   // error: string is not assignable to number
</script>
```

```reference typescript
(a: T): R | Parameter and return types | function f(x: number): string
p?: T | Optional parameter | function f(name?: string)
p: T = v | Default value | function f(n = 1)
...rest: T[] | Any number of arguments | function sum(...n: number[])
(a: T) => R | Function type | type Fn = (x: number) => boolean
void | Returns nothing | function log(m: string): void
```

```exercise typescript
? Make the parameter title optional
function greet(name: string, title___: string) { }
= ?
```

```quiz
? What does the return type void mean?
* The function does not return a useful value
- The function returns null
- The function never ends
```

# @lesson ts-objects
title: Object types and interfaces
summary: Describing object shapes with type and interface, optional and readonly properties.
---
```try html ts
<script type="text/typescript">
interface Product {
  readonly id: number;
  name: string;
  price: number;
  tags?: string[];          // optional
}

type Point = { x: number; y: number };

function describe(p: Product): string {
  const tagText = p.tags ? " [" + p.tags.join(", ") + "]" : "";
  return p.name + ": " + p.price.toFixed(2) + tagText;
}

const tea: Product = { id: 1, name: "Tea", price: 12.5 };
const cake: Product = { id: 2, name: "Cake", price: 35, tags: ["sweet"] };
// tea.id = 5;          // error: id is read-only
// const bad: Product = { id: 3, name: "Juice" };   // error: price is missing

interface Discounted extends Product {
  discount: number;
}
const sale: Discounted = { id: 3, name: "Coffee", price: 20, discount: 0.1 };

const origin: Point = { x: 0, y: 0 };
const stock: Record<string, number> = { tea: 10, cake: 3 };

console.log(describe(tea));
console.log(describe(cake));
console.log(sale.name, sale.price * (1 - sale.discount));
console.log(origin, stock["tea"]);
</script>
```

```reference typescript
interface I { a: T } | Name an object shape | interface User { name: string }
type T = { ... } | Type alias for a shape | type Point = { x: number; y: number }
a?: T | Optional property | email?: string
readonly a: T | Cannot be reassigned | readonly id: number
interface B extends A | Extend a shape | interface Admin extends User
Record<K, V> | Object with keys K and values V | Record<string, number>
```

:::tip type or interface?
Both describe object shapes. Many teams use `interface` for objects that may be extended and `type` for everything else, such as unions. Pick one style and stay consistent.
:::

```exercise typescript
? Make the email property optional
interface User { name: string; email___: string }
= ?
```

```quiz
? What happens if you create a Product without a required property?
* The compiler reports an error
- The property becomes 0
- Nothing at all

? A readonly property cannot be reassigned after the object is created.
= true
```

# @lesson ts-unions
title: Unions, literal types and narrowing
summary: string | number, literal types, typeof checks and discriminated unions.
---
```try html ts
<script type="text/typescript">
function format(value: string | number): string {
  if (typeof value === "number") {
    return value.toFixed(2);      // here value is a number
  }
  return value.toUpperCase();     // here value is a string
}

type Status = "pending" | "paid" | "shipped";
let status: Status = "paid";
// status = "lost";               // error: not one of the allowed values

type Shape =
  | { kind: "circle"; r: number }
  | { kind: "rect"; w: number; h: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.r * s.r;
    case "rect":
      return s.w * s.h;
  }
}

function findUser(id: number): string | undefined {
  return id === 1 ? "Sara" : undefined;
}
const user = findUser(2);
console.log(format(3.14159), format("tea"), status);
console.log(area({ kind: "circle", r: 1 }).toFixed(2), area({ kind: "rect", w: 2, h: 3 }));
console.log(user ?? "no user", user?.length);
</script>
```

```reference typescript
A|B | Union: either type | let id: number | string;
"a"|"b" | Literal types: exact values | type Dir = "left" | "right";
typeof x === "string" | Narrow a primitive | if (typeof v === "number")
"key" in obj | Narrow by property | if ("email" in u)
kind: "..." | Discriminated union tag | switch (shape.kind)
?. / ?? | Optional chaining / default | user?.name ?? "guest"
```

:::tip Narrowing
After a check such as `typeof value === "number"`, TypeScript knows the exact type inside that branch, so it allows `value.toFixed()` there and nowhere else.
:::

```exercise typescript
? Allow id to be a number or a string
let id: number | ___;
= string
```

```quiz
? What is type Status = "pending" | "paid"?
* A type that allows only those two exact strings
- Any string
- A boolean
```

# @lesson ts-classes
title: Classes
summary: Typed properties, constructors, access modifiers, implements and abstract classes.
---
```try html ts
<script type="text/typescript">
interface Shape {
  area(): number;
}

abstract class Base implements Shape {
  constructor(public readonly name: string) {}   // parameter property
  abstract area(): number;
  describe(): string {
    return this.name + " with area " + this.area().toFixed(2);
  }
}

class Circle extends Base {
  constructor(private r: number) {
    super("circle");
  }
  area(): number {
    return Math.PI * this.r * this.r;
  }
}

class Account {
  private balance = 0;
  static count = 0;
  constructor(public owner: string) {
    Account.count++;
  }
  deposit(amount: number): void {
    if (amount <= 0) throw new Error("Amount must be positive");
    this.balance += amount;
  }
  get total(): number {
    return this.balance;
  }
}

const acc = new Account("Sara");
acc.deposit(100);
// acc.balance = 1e6;   // error: balance is private
console.log(acc.owner, acc.total, Account.count);
console.log(new Circle(1).describe());
</script>
```

```reference typescript
public / private / protected | Who can access a member | private balance = 0;
readonly | Set once | readonly id: number
constructor(public x: T) | Parameter property: declares and sets | constructor(private db: Db)
implements I | Class follows an interface | class A implements Shape
abstract | Must be implemented by subclasses | abstract area(): number;
static | Belongs to the class | static count = 0;
get / set | Accessors | get total() { return this.t; }
```

```exercise typescript
? Make balance visible only inside the class
___ balance = 0;
= private
```

```quiz
? What does constructor(public owner: string) do?
* Declares an owner property and sets it from the argument
- Makes the constructor public only
- Nothing, public is ignored
```

# @lesson ts-generics
title: Generics
summary: Reusable functions and types with type parameters, and constraints.
---
```try html ts
<script type="text/typescript">
function first<T>(items: T[]): T | undefined {
  return items[0];
}

interface ApiResult<T> {
  ok: boolean;
  data: T;
}

function wrap<T>(data: T): ApiResult<T> {
  return { ok: true, data };
}

function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

class Box<T> {
  private items: T[] = [];
  add(item: T): void { this.items.push(item); }
  all(): T[] { return [...this.items]; }
}

function pluck<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const n = first([10, 20]);            // number | undefined
const s = first(["a", "b"]);          // string | undefined
const res = wrap({ id: 1, name: "Tea" });
const box = new Box<string>();
box.add("apple");
// box.add(5);                         // error: number is not a string

console.log(n, s, res.data.name);
console.log(longest("tea", "coffee"), longest([1, 2, 3], [4]));
console.log(box.all(), pluck({ name: "Sara", age: 25 }, "age"));
</script>
```

```reference typescript
function f<T>(x: T): T | Generic function | function id<T>(x: T) { return x; }
interface I<T> | Generic interface | interface Page<T> { items: T[] }
class C<T> | Generic class | class Stack<T> { }
T extends U | Constraint | <T extends { id: number }>
keyof T | Union of T's keys | type K = keyof User;
T[K] | Type of a property | User["name"]
```

:::tip Why generics?
A generic function keeps the connection between input and output types: `first(["a"])` is known to return a `string`, not just "something".
:::

```exercise typescript
? Declare a generic type parameter T for the function
function last___(items: T[]): T { return items[items.length - 1]; }
= <T>
```

```quiz
? What does <T extends { length: number }> mean?
* T can be any type that has a numeric length property
- T must be exactly a number
- T is an array of numbers
```

# @lesson ts-utility
title: Utility types and enums
summary: Partial, Pick, Omit, Readonly, ReturnType, as const and enums.
---
```try html ts
<script type="text/typescript">
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "member";
}

type UserUpdate = Partial<User>;                  // every property optional
type PublicUser = Omit<User, "email">;            // without email
type Login = Pick<User, "email">;                 // only email
type FrozenUser = Readonly<User>;

function update(user: User, changes: UserUpdate): User {
  return { ...user, ...changes };
}

const sara: User = { id: 1, name: "Sara", email: "s@example.com", role: "member" };
const promoted = update(sara, { role: "admin" });
const shown: PublicUser = { id: 1, name: "Sara", role: "admin" };
const login: Login = { email: "s@example.com" };

enum Level { Low = 1, Medium, High }
const ROLES = ["admin", "member"] as const;       // readonly tuple of literals
type Role = typeof ROLES[number];                  // "admin" | "member"

function makeUser() { return { id: 2, name: "Omar" }; }
type Made = ReturnType<typeof makeUser>;
const m: Made = makeUser();

console.log(promoted.role, shown.name, login.email);
console.log(Level.Medium, Level[3], ROLES.length, m.name);
</script>
```

```reference typescript
Partial<T> | All properties optional | Partial<User>
Required<T> | All properties required | Required<Config>
Pick<T, K> / Omit<T, K> | Keep / remove some properties | Omit<User, "password">
Readonly<T> | No reassigning | Readonly<State>
ReturnType<typeof f> | The return type of a function | ReturnType<typeof load>
enum E { A, B } | Named constants | enum Dir { Up, Down }
as const | Literal, readonly values | const sizes = ["s", "m"] as const;
```

```exercise typescript
? Make every property of User optional
type Draft = ___<User>;
= Partial
```

```quiz
? Which utility type removes properties from a type?
* Omit
- Pick
- Partial
```

# @lesson ts-async
title: Async code and modules
summary: Typing promises, async/await, fetch results, and import/export.
---
```try html ts
<script type="text/typescript">
interface Product {
  id: number;
  name: string;
  price: number;
}

function fakeFetch(): Promise<Product[]> {         // stands in for a real API call
  return new Promise(resolve =>
    setTimeout(() => resolve([{ id: 1, name: "Tea", price: 12 }, { id: 2, name: "Cake", price: 35 }]), 300)
  );
}

async function cheapest(): Promise<Product> {
  const products = await fakeFetch();
  return products.reduce((a, b) => (a.price <= b.price ? a : b));
}

async function main(): Promise<void> {
  try {
    const p = await cheapest();
    console.log("cheapest:", p.name, p.price);
  } catch (e) {
    console.error(e instanceof Error ? e.message : String(e));
  }
}
main();
</script>
```

In a real project, code is split into files called **modules**:

```typescript
// products.ts
export interface Product { id: number; name: string; price: number }
export async function loadProducts(): Promise<Product[]> {
  const res = await fetch("/api/products");
  if (!res.ok) throw new Error("HTTP " + res.status);
  return (await res.json()) as Product[];
}

// main.ts
import { loadProducts, type Product } from "./products";
```

```reference typescript
Promise<T> | A value that arrives later | function load(): Promise<User>
async / await | Write async code step by step | const u = await load();
Promise<void> | Async function with no result | async function save(): Promise<void>
as T | Tell the compiler the type (unchecked) | (await res.json()) as User
export / import | Share code between files | import { load } from "./api";
catch (e) | e is unknown: check it first | if (e instanceof Error)
```

:::warning as does not check anything
`await res.json() as Product[]` only tells the compiler what you expect; the server can still send something else. For data from outside, validate it at runtime.
:::

```exercise typescript
? Give the return type of an async function that returns a number
async function count(): ___<number> { return 3; }
= Promise
```

```quiz
? What is the return type of an async function that returns a string?
* Promise<string>
- string
- async<string>
```

# @lesson ts-setup
title: Setting up a project
summary: tsc, tsconfig.json, strict mode and using TypeScript with tools.
---
On your computer, with Node.js installed:

```text
npm init -y
npm install --save-dev typescript
npx tsc --init          # creates tsconfig.json
npx tsc                 # type-checks and writes .js files
npx tsc --noEmit        # type-check only
```

A small `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "strict": true,
    "outDir": "dist",
    "sourceMap": true
  },
  "include": ["src"]
}
```

- **strict** turns on the most useful checks, including `strictNullChecks`, which makes you handle `null` and `undefined`. Always start new projects with it.
- **target** is the JavaScript version to produce; **outDir** is where the `.js` files go.
- Frameworks (React with Vite, Angular, Next.js, Node with `tsx`) set TypeScript up for you.

```try html ts
<script type="text/typescript">
// with strict on, this is an error until you handle the undefined case:
function initials(name?: string): string {
  if (!name) return "?";
  return name.split(" ").map(p => p[0]).join("").toUpperCase();
}
console.log(initials("sara ali"), initials());
</script>
```

:::tip Adding TypeScript to a JavaScript project
Rename files from `.js` to `.ts` one at a time, start with `"strict": false` if there are too many errors, and switch it on once the code is clean.
:::

```quiz
? Which tsconfig option turns on the strongest set of checks?
* strict
- target
- outDir

? npx tsc --noEmit checks types without writing JavaScript files.
= true
```

# @lesson ts-reference
title: TypeScript quick reference
summary: The most used syntax on one page.
---
```reference typescript
let x: T | Annotate a variable | let n: number = 1;
string / number / boolean / T[] | Basic types | let tags: string[] = [];
(a: T): R | Typed function | function f(x: number): string
interface / type | Object shapes and aliases | interface User { name: string }
a?: T / readonly | Optional / read-only property | readonly id: number
A|B / "a"|"b" | Unions and literal types | type Dir = "up" | "down";
typeof / in / switch on kind | Narrowing | if (typeof v === "string")
class / private / implements | Classes | class A implements I { }
<T> / extends / keyof | Generics | function f<T extends object>(x: T)
Partial / Pick / Omit / Record | Utility types | Partial<User>
Promise<T> / async | Async code | async function f(): Promise<void>
"strict": true | Strict checks in tsconfig | always for new projects
```

:::tip Where to go next
Convert one of your JavaScript exercises to TypeScript with `strict` on and fix every error the compiler finds. Then try a framework: React with TypeScript (Vite) or a Node.js API with typed request handlers.
:::

```quiz
? What is the main benefit of TypeScript over JavaScript?
* Mistakes in types are found before the code runs
- The code runs faster in the browser
- It does not need a browser
```
