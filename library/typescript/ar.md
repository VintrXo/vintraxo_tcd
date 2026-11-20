# @lesson ts-intro
title: مقدمة TypeScript
summary: ماذا تضيف TypeScript إلى JavaScript، وأول برنامج بالأنواع.
---
**TypeScript** هي JavaScript مع **الأنواع**. تصف نوع القيمة في كل متغير ومعامل وكائن، فينبهك مترجم TypeScript (`tsc`) أو محرر الكود إلى الأخطاء *قبل* تشغيل الكود. والناتج JavaScript عادية، فتعمل في أي مكان تعمل فيه JavaScript.

```try html ts
<script type="text/typescript">
function greet(name: string): string {
  return "Hello, " + name;
}
console.log(greet("Sara"));
console.log(6 * 7);
// greet(42);   // خطأ في المحرر: لا يمكن إسناد number إلى string
</script>
```

- `name: string` تعني أن المعامل يجب أن يكون نصًا، و `): string` تحدد ما ترجعه الدالة.
- تختفي الأنواع عند تحويل TypeScript إلى JavaScript.

:::info كيف تعمل الأمثلة
هنا يحوّل المتصفح كود TypeScript إلى JavaScript ويشغّله، ثم يعرض ناتج `console.log` في الأعلى. هذا الوضع السريع يحذف الأنواع دون فحصها؛ أما أخطاء الأنواع (المكتوبة كتعليقات في الأمثلة) فتظهر في محرر مثل VS Code، أو عند تشغيل `npx tsc`.
:::

```quiz
? متى تُبلغ TypeScript عن خطأ في الأنواع؟
* قبل تشغيل الكود، في المحرر أو المترجم
- بعد تعطل البرنامج فقط
- أبدًا، فالأنواع مجرد تعليقات

? يُحوَّل كود TypeScript إلى JavaScript عادية ليعمل.
= true
```

# @lesson ts-types
title: الأنواع الأساسية
summary: string و number و boolean والمصفوفات و any و unknown واستنتاج النوع.
---
```try html ts
<script type="text/typescript">
let city: string = "Cairo";
let age: number = 25;
let active: boolean = true;
let scores: number[] = [90, 75, 88];
let tags: Array<string> = ["new", "sale"];
let point: [number, number] = [3, 4];      // صف: طول وأنواع ثابتة

let total = 10;          // استُنتج كـ number، ولا حاجة لكتابة النوع
total += 5;
// total = "fifteen";    // خطأ: لا يمكن إسناد string إلى number

let data: unknown = JSON.parse('{"id": 7}');
if (typeof data === "object" && data !== null && "id" in data) {
  console.log("id found");
}

console.log(city, age, active, scores.length, tags[0], point[1], total);
</script>
```

```reference typescript
string / number / boolean | الأنواع الأساسية | let n: number = 1;
T[] / Array<T> | المصفوفات | let names: string[] = [];
[A, B] | الصف (tuple) | let p: [number, string] = [1, "a"];
any | يوقف الفحص (تجنّبه) | let x: any;
unknown | "أي شيء" بأمان: افحصه قبل الاستخدام | let v: unknown;
null / undefined | القيم الغائبة | let m: string | null = null;
الاستنتاج | النوع يأتي من القيمة | let x = 5; // number
```

:::tip دع الاستنتاج يعمل
نادرًا ما تحتاج لكتابة نوع المتغيرات المحلية: `let total = 10` هي `number` بالفعل. اكتب أنواع معاملات الدوال وما ترجعه وأشكال البيانات العامة.
:::

```exercise typescript
? عرّف prices كمصفوفة أرقام
let prices: ___ = [10, 20];
= number[] | Array<number>
```

```quiz
? أي نوع هو الأكثر أمانًا لقيمة لا تعرف شكلها بعد؟
* unknown
- any
- object

? السطر let count = 3; يعطي count النوع number بدون كتابة النوع.
= true
```

# @lesson ts-functions
title: الدوال
summary: أنواع المعاملات والإرجاع، والمعاملات الاختيارية والافتراضية، وأنواع الدوال.
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
const multiply: Operation = (a, b) => a * b;     // a و b أرقام هنا

function log(message: string): void {
  console.log("[log] " + message);
}

console.log(add(2, 3), square(4), sum(1, 2, 3), multiply(6, 7));
console.log(greet("Sara"), "|", greet("Omar", "Welcome", "Dr."));
log("done");
// add("2", 3);   // خطأ: لا يمكن إسناد string إلى number
</script>
```

```reference typescript
(a: T): R | نوع المعامل والإرجاع | function f(x: number): string
p?: T | معامل اختياري | function f(name?: string)
p: T = v | قيمة افتراضية | function f(n = 1)
...rest: T[] | أي عدد من المعاملات | function sum(...n: number[])
(a: T) => R | نوع دالة | type Fn = (x: number) => boolean
void | لا ترجع شيئًا | function log(m: string): void
```

```exercise typescript
? اجعل المعامل title اختياريًا
function greet(name: string, title___: string) { }
= ?
```

```quiz
? ماذا يعني نوع الإرجاع void؟
* الدالة لا ترجع قيمة مفيدة
- الدالة ترجع null
- الدالة لا تنتهي أبدًا
```

# @lesson ts-objects
title: أنواع الكائنات والواجهات
summary: وصف أشكال الكائنات بـ type و interface، والخصائص الاختيارية و readonly.
---
```try html ts
<script type="text/typescript">
interface Product {
  readonly id: number;
  name: string;
  price: number;
  tags?: string[];          // اختيارية
}

type Point = { x: number; y: number };

function describe(p: Product): string {
  const tagText = p.tags ? " [" + p.tags.join(", ") + "]" : "";
  return p.name + ": " + p.price.toFixed(2) + tagText;
}

const tea: Product = { id: 1, name: "Tea", price: 12.5 };
const cake: Product = { id: 2, name: "Cake", price: 35, tags: ["sweet"] };
// tea.id = 5;          // خطأ: id للقراءة فقط
// const bad: Product = { id: 3, name: "Juice" };   // خطأ: price ناقصة

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
interface I { a: T } | تسمية شكل كائن | interface User { name: string }
type T = { ... } | اسم بديل لشكل | type Point = { x: number; y: number }
a?: T | خاصية اختيارية | email?: string
readonly a: T | لا يُعاد إسنادها | readonly id: number
interface B extends A | توسيع شكل | interface Admin extends User
Record<K, V> | كائن مفاتيحه K وقيمه V | Record<string, number>
```

:::tip type أم interface؟
كلاهما يصف أشكال الكائنات. فرق كثيرة تستخدم `interface` للكائنات التي قد تُوسَّع، و `type` لكل ما عدا ذلك مثل الاتحادات. اختر أسلوبًا والتزم به.
:::

```exercise typescript
? اجعل الخاصية email اختيارية
interface User { name: string; email___: string }
= ?
```

```quiz
? ماذا يحدث إذا أنشأت Product بدون خاصية مطلوبة؟
* يبلغ المترجم عن خطأ
- تصبح الخاصية 0
- لا شيء على الإطلاق

? لا يمكن إعادة إسناد خاصية readonly بعد إنشاء الكائن.
= true
```

# @lesson ts-unions
title: الاتحادات والأنواع الحرفية والتضييق
summary: string | number، والأنواع الحرفية، وفحوص typeof، والاتحادات المميَّزة.
---
```try html ts
<script type="text/typescript">
function format(value: string | number): string {
  if (typeof value === "number") {
    return value.toFixed(2);      // هنا value رقم
  }
  return value.toUpperCase();     // هنا value نص
}

type Status = "pending" | "paid" | "shipped";
let status: Status = "paid";
// status = "lost";               // خطأ: ليست من القيم المسموحة

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
A|B | اتحاد: أحد النوعين | let id: number | string;
"a"|"b" | أنواع حرفية: قيم محددة بالضبط | type Dir = "left" | "right";
typeof x === "string" | تضييق نوع بسيط | if (typeof v === "number")
"key" in obj | التضييق بخاصية | if ("email" in u)
kind: "..." | وسم الاتحاد المميَّز | switch (shape.kind)
?. / ?? | الوصول الاختياري / قيمة بديلة | user?.name ?? "guest"
```

:::tip التضييق
بعد فحص مثل `typeof value === "number"` تعرف TypeScript النوع بالضبط داخل هذا الفرع، فتسمح بـ `value.toFixed()` هناك فقط.
:::

```exercise typescript
? اسمح لـ id أن يكون رقمًا أو نصًا
let id: number | ___;
= string
```

```quiz
? ما هو type Status = "pending" | "paid"؟
* نوع يسمح بهذين النصين بالضبط فقط
- أي نص
- قيمة منطقية
```

# @lesson ts-classes
title: الأصناف
summary: خصائص بأنواع، والمُنشئ، ومستويات الوصول، و implements، والأصناف المجردة.
---
```try html ts
<script type="text/typescript">
interface Shape {
  area(): number;
}

abstract class Base implements Shape {
  constructor(public readonly name: string) {}   // خاصية من معامل المُنشئ
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
// acc.balance = 1e6;   // خطأ: balance خاصة
console.log(acc.owner, acc.total, Account.count);
console.log(new Circle(1).describe());
</script>
```

```reference typescript
public / private / protected | من يصل إلى العضو | private balance = 0;
readonly | تُضبط مرة واحدة | readonly id: number
constructor(public x: T) | خاصية من المعامل: تعريف وإسناد | constructor(private db: Db)
implements I | الصنف يلتزم بواجهة | class A implements Shape
abstract | يجب أن تنفذه الأصناف الأبناء | abstract area(): number;
static | تخص الصنف نفسه | static count = 0;
get / set | دوال الوصول | get total() { return this.t; }
```

```exercise typescript
? اجعل balance مرئيًا داخل الصنف فقط
___ balance = 0;
= private
```

```quiz
? ماذا يفعل constructor(public owner: string)؟
* يعرّف خاصية owner ويضبطها من المعامل
- يجعل المُنشئ عامًا فقط
- لا شيء، فكلمة public تُتجاهل
```

# @lesson ts-generics
title: الأنواع العامة (Generics)
summary: دوال وأنواع قابلة لإعادة الاستخدام بمعاملات نوع، والقيود.
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
// box.add(5);                         // خطأ: الرقم ليس نصًا

console.log(n, s, res.data.name);
console.log(longest("tea", "coffee"), longest([1, 2, 3], [4]));
console.log(box.all(), pluck({ name: "Sara", age: 25 }, "age"));
</script>
```

```reference typescript
function f<T>(x: T): T | دالة عامة | function id<T>(x: T) { return x; }
interface I<T> | واجهة عامة | interface Page<T> { items: T[] }
class C<T> | صنف عام | class Stack<T> { }
T extends U | قيد | <T extends { id: number }>
keyof T | اتحاد مفاتيح T | type K = keyof User;
T[K] | نوع خاصية | User["name"]
```

:::tip لماذا الأنواع العامة؟
تحافظ الدالة العامة على العلاقة بين نوع المدخل ونوع المخرج: فمعروف أن `first(["a"])` ترجع `string`، لا مجرد "شيء ما".
:::

```exercise typescript
? عرّف معامل نوع عام T للدالة
function last___(items: T[]): T { return items[items.length - 1]; }
= <T>
```

```quiz
? ماذا يعني <T extends { length: number }>؟
* يمكن أن يكون T أي نوع له خاصية length رقمية
- يجب أن يكون T رقمًا بالضبط
- T مصفوفة أرقام
```

# @lesson ts-utility
title: الأنواع المساعدة و enum
summary: Partial و Pick و Omit و Readonly و ReturnType و as const و enum.
---
```try html ts
<script type="text/typescript">
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "member";
}

type UserUpdate = Partial<User>;                  // كل الخصائص اختيارية
type PublicUser = Omit<User, "email">;            // بدون email
type Login = Pick<User, "email">;                 // email فقط
type FrozenUser = Readonly<User>;

function update(user: User, changes: UserUpdate): User {
  return { ...user, ...changes };
}

const sara: User = { id: 1, name: "Sara", email: "s@example.com", role: "member" };
const promoted = update(sara, { role: "admin" });
const shown: PublicUser = { id: 1, name: "Sara", role: "admin" };
const login: Login = { email: "s@example.com" };

enum Level { Low = 1, Medium, High }
const ROLES = ["admin", "member"] as const;       // صف قيم حرفية للقراءة فقط
type Role = typeof ROLES[number];                  // "admin" | "member"

function makeUser() { return { id: 2, name: "Omar" }; }
type Made = ReturnType<typeof makeUser>;
const m: Made = makeUser();

console.log(promoted.role, shown.name, login.email);
console.log(Level.Medium, Level[3], ROLES.length, m.name);
</script>
```

```reference typescript
Partial<T> | كل الخصائص اختيارية | Partial<User>
Required<T> | كل الخصائص مطلوبة | Required<Config>
Pick<T, K> / Omit<T, K> | الإبقاء على / حذف بعض الخصائص | Omit<User, "password">
Readonly<T> | بلا إعادة إسناد | Readonly<State>
ReturnType<typeof f> | نوع ما ترجعه دالة | ReturnType<typeof load>
enum E { A, B } | ثوابت بأسماء | enum Dir { Up, Down }
as const | قيم حرفية للقراءة فقط | const sizes = ["s", "m"] as const;
```

```exercise typescript
? اجعل كل خصائص User اختيارية
type Draft = ___<User>;
= Partial
```

```quiz
? أي نوع مساعد يحذف خصائص من نوع؟
* Omit
- Pick
- Partial
```

# @lesson ts-async
title: الكود غير المتزامن والوحدات
summary: أنواع الوعود، و async/await، ونتائج fetch، و import/export.
---
```try html ts
<script type="text/typescript">
interface Product {
  id: number;
  name: string;
  price: number;
}

function fakeFetch(): Promise<Product[]> {         // بديل عن طلب API حقيقي
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

في المشروع الحقيقي يُقسَّم الكود إلى ملفات تسمى **وحدات (modules)**:

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
Promise<T> | قيمة تصل لاحقًا | function load(): Promise<User>
async / await | كتابة الكود غير المتزامن خطوة بخطوة | const u = await load();
Promise<void> | دالة غير متزامنة بلا نتيجة | async function save(): Promise<void>
as T | إخبار المترجم بالنوع (بلا فحص) | (await res.json()) as User
export / import | مشاركة الكود بين الملفات | import { load } from "./api";
catch (e) | نوع e هو unknown: افحصه أولًا | if (e instanceof Error)
```

:::warning as لا تفحص شيئًا
`await res.json() as Product[]` تخبر المترجم فقط بما تتوقعه؛ وقد يرسل الخادم شيئًا آخر. تحقّق من البيانات القادمة من الخارج أثناء التشغيل.
:::

```exercise typescript
? اكتب نوع إرجاع دالة async ترجع رقمًا
async function count(): ___<number> { return 3; }
= Promise
```

```quiz
? ما نوع إرجاع دالة async ترجع نصًا؟
* Promise<string>
- string
- async<string>
```

# @lesson ts-setup
title: تجهيز مشروع
summary: tsc و tsconfig.json والوضع الصارم واستخدام TypeScript مع الأدوات.
---
على جهازك، مع تثبيت Node.js:

```text
npm init -y
npm install --save-dev typescript
npx tsc --init          # ينشئ tsconfig.json
npx tsc                 # يفحص الأنواع ويكتب ملفات .js
npx tsc --noEmit        # فحص الأنواع فقط
```

ملف `tsconfig.json` صغير:

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

- **strict** يشغّل أهم الفحوص، ومنها `strictNullChecks` التي تجبرك على التعامل مع `null` و `undefined`. ابدأ به دائمًا في المشاريع الجديدة.
- **target** إصدار JavaScript الناتج، و **outDir** مكان ملفات `.js`.
- أطر العمل (React مع Vite و Angular و Next.js و Node مع `tsx`) تجهّز TypeScript لك.

```try html ts
<script type="text/typescript">
// مع strict يكون هذا خطأ حتى تتعامل مع حالة undefined:
function initials(name?: string): string {
  if (!name) return "?";
  return name.split(" ").map(p => p[0]).join("").toUpperCase();
}
console.log(initials("sara ali"), initials());
</script>
```

:::tip إضافة TypeScript لمشروع JavaScript
غيّر امتداد الملفات من `.js` إلى `.ts` واحدًا تلو الآخر، وابدأ بـ `"strict": false` إذا كانت الأخطاء كثيرة جدًا، ثم شغّله عندما يصبح الكود نظيفًا.
:::

```quiz
? أي خيار في tsconfig يشغّل أقوى مجموعة فحوص؟
* strict
- target
- outDir

? يفحص npx tsc --noEmit الأنواع دون كتابة ملفات JavaScript.
= true
```

# @lesson ts-reference
title: مرجع TypeScript السريع
summary: أكثر الصيغ استخدامًا في صفحة واحدة.
---
```reference typescript
let x: T | نوع متغير | let n: number = 1;
string / number / boolean / T[] | الأنواع الأساسية | let tags: string[] = [];
(a: T): R | دالة بأنواع | function f(x: number): string
interface / type | أشكال الكائنات والأسماء البديلة | interface User { name: string }
a?: T / readonly | خاصية اختيارية / للقراءة فقط | readonly id: number
A|B / "a"|"b" | الاتحادات والأنواع الحرفية | type Dir = "up" | "down";
typeof / in / switch on kind | التضييق | if (typeof v === "string")
class / private / implements | الأصناف | class A implements I { }
<T> / extends / keyof | الأنواع العامة | function f<T extends object>(x: T)
Partial / Pick / Omit / Record | الأنواع المساعدة | Partial<User>
Promise<T> / async | الكود غير المتزامن | async function f(): Promise<void>
"strict": true | الفحوص الصارمة في tsconfig | دائمًا في المشاريع الجديدة
```

:::tip الخطوة التالية
حوّل أحد تمارينك في JavaScript إلى TypeScript مع تشغيل `strict`، وأصلح كل خطأ يجده المترجم. ثم جرّب إطار عمل: React مع TypeScript (Vite) أو واجهة API في Node.js بمعالجات طلبات لها أنواع.
:::

```quiz
? ما الفائدة الأساسية من TypeScript مقارنة بـ JavaScript؟
* اكتشاف أخطاء الأنواع قبل تشغيل الكود
- يعمل الكود أسرع في المتصفح
- لا تحتاج متصفحًا
```
