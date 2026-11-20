# @lesson react-intro
title: مقدمة في React
summary: ما هي React ولماذا تُبنى بها الواجهات.
---
**React** مكتبة JavaScript لبناء واجهات المستخدم من **مكونات**: قطع صغيرة مستقلة (زر، بطاقة، قائمة…) تركّبها معًا لتبني صفحة كاملة. عندما تتغير البيانات، تحدّث React الجزء المتغير من الصفحة فقط.

## أول تطبيق

في هذه الدورة تُحمَّل React تلقائيًا في كل مثال. اضغط **تشغيل**:

```try html react
<script type="text/babel">
  function App() {
    return <h1>مرحبًا React</h1>;
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- `App` مكوّن: دالة تعيد ما يُعرض.
- `createRoot(...).render(...)` يضع المكوّن داخل العنصر `root`.

:::info في مشروع حقيقي
تُنشأ مشاريع React عادة بأداة مثل **Vite**: `npm create vite@latest my-app -- --template react`. الأمثلة هنا تعمل مباشرة في المتصفح لتتعلم دون تثبيت.
:::

```quiz
? مما تُبنى واجهات React؟
* من مكونات صغيرة تُركّب معًا
- من صفحات HTML منفصلة فقط
- من جداول قاعدة البيانات

? المكوّن في React يمكن أن يكون دالة تعيد ما يُعرض.
= true
```

# @lesson react-jsx
title: JSX
summary: كتابة واجهة تشبه HTML داخل JavaScript.
---
**JSX** صيغة تكتب بها شكل الواجهة كأنه HTML داخل JavaScript:

```try html react
<script type="text/babel">
  const name = "سارة";
  const items = 3;
  function App() {
    return (
      <div>
        <h2>أهلًا {name}</h2>
        <p>في سلتك {items * 2} منتجات.</p>
        <p className="note" style={{ color: "teal", fontSize: 18 }}>نص بتنسيق</p>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

## قواعد JSX

- القيم والتعبيرات بين `{ }`.
- `className` بدل `class`، و`htmlFor` بدل `for`.
- `style` يأخذ كائنًا: `style={{ color: "red" }}`.
- يعيد المكوّن عنصرًا جذرًا واحدًا؛ لتجميع أكثر من عنصر استخدم `<>…</>`.
- كل عنصر يُغلق: `<img />` و `<br />`.

```exercise javascript
? أكمل لاستخدام صنف CSS في JSX
<p ___="title">نص</p>
= className
```

```quiz
? كيف تكتب متغيرًا داخل JSX؟
- ${name}
* {name}
- {{name}}

? في JSX نكتب className بدل class.
= true
```

# @lesson react-components
title: المكونات
summary: إنشاء مكونات وتركيبها داخل بعضها.
---
المكوّن دالة يبدأ اسمها **بحرف كبير** وتعيد JSX. ثم تستخدمه كوسم:

```try html react
<script type="text/babel">
  function Header() {
    return <header style={{ background: "#eef2ff", padding: 8 }}><h2>متجري</h2></header>;
  }
  function Product() {
    return <div style={{ border: "1px solid #ddd", padding: 8, margin: 4 }}>منتج</div>;
  }
  function App() {
    return (
      <>
        <Header />
        <Product />
        <Product />
        <Product />
      </>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

:::tip قسّم الواجهة
انظر لأي صفحة كمجموعة صناديق: رأس، قائمة، بطاقات، تذييل. كل صندوق مكوّن مستقل يسهل فهمه وإعادة استخدامه.
:::

```quiz
? بماذا يجب أن يبدأ اسم المكوّن؟
* بحرف كبير
- بحرف صغير
- بشرطة سفلية

? يمكن استخدام نفس المكوّن عدة مرات في الصفحة.
= true
```

# @lesson react-props
title: الخصائص props
summary: تمرير البيانات من المكوّن الأب إلى الابن.
---
**props** بيانات تمررها للمكوّن كسمات، فيصبح المكوّن الواحد قالبًا لأشكال مختلفة:

```try html react
<script type="text/babel">
  function ProductCard({ name, price, sale = false }) {
    return (
      <div style={{ border: "1px solid #ddd", padding: 8, margin: 4 }}>
        <strong>{name}</strong> — {price} ريال {sale && <span style={{ color: "crimson" }}>(تخفيض)</span>}
      </div>
    );
  }
  function App() {
    return (
      <>
        <ProductCard name="قلم" price={5} />
        <ProductCard name="حقيبة" price={90} sale={true} />
      </>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- النصوص بين علامتي تنصيص، وغيرها بين `{ }`: `price={5}`.
- props **للقراءة فقط**؛ المكوّن لا يغيّرها.

```exercise javascript
? مرّر الرقم 10 كخاصية price
<ProductCard name="دفتر" price=___ />
= {10}
```

```quiz
? في أي اتجاه تنتقل props؟
* من الأب إلى الابن
- من الابن إلى الأب
- بين أي مكونين مباشرة

? يجوز للمكوّن أن يغيّر قيمة props التي وصلته.
= false
```

# @lesson react-state
title: الحالة useState
summary: بيانات تتغير داخل المكوّن وتعيد عرضه.
---
**الحالة** بيانات يملكها المكوّن، وعندما تتغير تعيد React عرضه تلقائيًا:

```try html react
<script type="text/babel">
  const { useState } = React;
  function Counter() {
    const [count, setCount] = useState(0);
    return (
      <div>
        <p>العدد: {count}</p>
        <button onClick={() => setCount(count + 1)}>زِد</button>
        <button onClick={() => setCount(0)}>صفّر</button>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<Counter />);
</script>
```

- `useState(0)` يعيد القيمة الحالية ودالة لتغييرها.
- لا تغيّر الحالة مباشرة (`count++`)؛ استخدم دالة الضبط دائمًا.

:::info في مشروع حقيقي
تستورد الدالة هكذا: `import { useState } from "react";`. هنا نأخذها من `React` لأن المكتبة محمّلة في الصفحة.
:::

```exercise javascript
? أكمل لإنشاء حالة ابتدائية قيمتها نص فارغ
const [name, setName] = ___("");
= useState
```

```quiz
? ماذا يحدث عند استدعاء setCount؟
* تتغير القيمة ويعاد عرض المكوّن
- تتغير القيمة دون إعادة عرض
- يُحذف المكوّن

? الطريقة الصحيحة لتغيير الحالة هي دالة الضبط مثل setCount.
= true
```

# @lesson react-events
title: الأحداث
summary: onClick و onChange و onSubmit.
---
```try html react
<script type="text/babel">
  const { useState } = React;
  function App() {
    const [text, setText] = useState("");
    const [liked, setLiked] = useState(false);
    return (
      <div>
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="اكتب شيئًا" />
        <p>كتبت: {text}</p>
        <button onClick={() => setLiked(!liked)}>{liked ? "❤️ أعجبني" : "🤍 إعجاب"}</button>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- أسماء الأحداث بصيغة camelCase: `onClick` و `onChange` و `onSubmit`.
- مرّر **دالة**، لا استدعاء: `onClick={handle}` وليس `onClick={handle()}`.

```quiz
? كيف يُكتب حدث النقر في React؟
- onclick="…"
* onClick={…}
- on-click={…}

? كتابة onClick={save()} تنفّذ save عند العرض بدل النقر.
= true
```

# @lesson react-conditional
title: العرض الشرطي
summary: إظهار عناصر حسب شرط بـ && والعامل الثلاثي.
---
```try html react
<script type="text/babel">
  const { useState } = React;
  function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const messages = 3;
    return (
      <div>
        {loggedIn ? <h3>أهلًا بعودتك</h3> : <h3>سجّل دخولك</h3>}
        {loggedIn && messages > 0 && <p>لديك {messages} رسائل جديدة</p>}
        <button onClick={() => setLoggedIn(!loggedIn)}>{loggedIn ? "خروج" : "دخول"}</button>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- `شرط ? أ : ب` لاختيار أحد عنصرين.
- `شرط && عنصر` لإظهار العنصر فقط عند تحقق الشرط.

```quiz
? ماذا يعرض {isAdmin && <Panel />} عندما isAdmin قيمتها false؟
* لا شيء
- Panel
- كلمة false

? العامل الثلاثي يختار بين عنصرين حسب الشرط.
= true
```

# @lesson react-lists
title: القوائم والمفاتيح
summary: عرض مصفوفة بـ map، ولماذا نحتاج key.
---
```try html react
<script type="text/babel">
  const products = [
    { id: 1, name: "قلم", price: 5 },
    { id: 2, name: "دفتر", price: 12 },
    { id: 3, name: "حقيبة", price: 90 },
  ];
  function App() {
    return (
      <ul>
        {products.map((p) => (
          <li key={p.id}>{p.name}: {p.price} ريال</li>
        ))}
      </ul>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

:::warning لا تنسَ key
`key` يساعد React على معرفة أي عنصر تغيّر. استخدم معرّفًا ثابتًا وفريدًا مثل `p.id`، وتجنب فهرس المصفوفة إذا كانت القائمة تتغير.
:::

```exercise javascript
? أضف المفتاح الصحيح لكل عنصر
{users.map((u) => <li ___={u.id}>{u.name}</li>)}
= key
```

```quiz
? أي دالة تُستخدم لعرض قائمة من مصفوفة؟
* map
- forEach
- reduce

? الخاصية key يجب أن تكون فريدة بين عناصر القائمة.
= true
```

# @lesson react-forms
title: النماذج
summary: الحقول المتحكَّم بها، وإرسال النموذج.
---
في React تحفظ قيمة الحقل في الحالة، فيصبح **متحكَّمًا به**:

```try html react
<script type="text/babel">
  const { useState } = React;
  function SignUp() {
    const [form, setForm] = useState({ name: "", city: "الرياض" });
    const [sent, setSent] = useState(null);
    const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
    const submit = (e) => {
      e.preventDefault();
      setSent(form);
    };
    return (
      <form onSubmit={submit}>
        <input name="name" value={form.name} onChange={update} placeholder="الاسم" required />
        <select name="city" value={form.city} onChange={update}>
          <option>الرياض</option><option>القاهرة</option>
        </select>
        <button>إرسال</button>
        {sent && <p>تم: {sent.name} من {sent.city}</p>}
      </form>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<SignUp />);
</script>
```

- `value` من الحالة و `onChange` يحدّثها.
- `{ ...form, [name]: value }` ينسخ الكائن ويغيّر حقلًا واحدًا.
- `e.preventDefault()` يمنع إعادة تحميل الصفحة.

```quiz
? ما المقصود بالحقل المتحكَّم به؟
* قيمته محفوظة في الحالة وتُحدَّث بـ onChange
- حقل لا يمكن الكتابة فيه
- حقل يتحقق منه الخادم

? يجب استدعاء e.preventDefault() في onSubmit لمنع إعادة تحميل الصفحة.
= true
```

# @lesson react-effects
title: التأثيرات useEffect
summary: تنفيذ كود بعد العرض: مؤقتات، وجلب بيانات.
---
`useEffect` لكود «جانبي» يعمل بعد عرض المكوّن: مؤقت، أو جلب بيانات، أو تحديث عنوان الصفحة:

```try html react
<script type="text/babel">
  const { useState, useEffect } = React;
  function Clock() {
    const [seconds, setSeconds] = useState(0);
    useEffect(() => {
      const id = setInterval(() => setSeconds((s) => s + 1), 1000);
      return () => clearInterval(id);   // التنظيف عند إزالة المكوّن
    }, []);                              // [] = مرة واحدة بعد أول عرض
    return <p>مرّ {seconds} ثانية</p>;
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<Clock />);
</script>
```

## مصفوفة التبعيات

- `[]` مرة واحدة بعد أول عرض.
- `[query]` كلما تغيّرت `query`.
- بدون مصفوفة: بعد كل عرض (نادرًا ما تحتاجه).

```js
useEffect(() => {
  fetch(`/api/products?q=${query}`)
    .then((r) => r.json())
    .then(setProducts);
}, [query]);
```

```quiz
? متى يعمل useEffect بمصفوفة تبعيات فارغة []؟
* مرة واحدة بعد أول عرض
- قبل كل عرض
- لا يعمل أبدًا

? الدالة التي يعيدها useEffect تُستخدم للتنظيف، مثل إيقاف المؤقت.
= true
```

# @lesson react-project
title: مشروع: قائمة مهام
summary: تطبيق صغير يجمع كل ما تعلمته.
---
قائمة مهام تضيف وتحذف وتعلّم المهام كمنجزة:

```try html react
<script type="text/babel">
  const { useState } = React;
  function TodoApp() {
    const [todos, setTodos] = useState([{ id: 1, text: "تعلّم React", done: false }]);
    const [text, setText] = useState("");
    const add = (e) => {
      e.preventDefault();
      if (!text.trim()) return;
      setTodos([...todos, { id: Date.now(), text, done: false }]);
      setText("");
    };
    const toggle = (id) => setTodos(todos.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
    const remove = (id) => setTodos(todos.filter((t) => t.id !== id));
    const left = todos.filter((t) => !t.done).length;
    return (
      <div style={{ maxWidth: 360 }}>
        <form onSubmit={add}>
          <input value={text} onChange={(e) => setText(e.target.value)} placeholder="مهمة جديدة" />
          <button>أضف</button>
        </form>
        <ul>
          {todos.map((t) => (
            <li key={t.id}>
              <label style={{ textDecoration: t.done ? "line-through" : "none" }}>
                <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} /> {t.text}
              </label>
              <button onClick={() => remove(t.id)}>✕</button>
            </li>
          ))}
        </ul>
        <p>متبقٍ: {left}</p>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<TodoApp />);
</script>
```

:::tip طوّره بنفسك
أضف زر «احذف المنجز»، أو فلترًا يعرض الكل/المتبقي/المنجز.
:::

```quiz
? لماذا ننسخ المصفوفة بـ [...todos, جديد] بدل todos.push()؟
* لأن الحالة لا تُعدَّل مباشرة؛ نعطي React نسخة جديدة
- لأن push غير موجودة في JavaScript
- لا فرق بينهما

? الدالة filter مناسبة لحذف عنصر من القائمة في الحالة.
= true
```

# @lesson react-reference
title: مرجع React
summary: أهم المفاهيم والدوال مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي مفهوم.

```reference javascript
مكوّن | دالة تعيد JSX | function Card() { return <div />; }
JSX | واجهة داخل JavaScript | <h1>{title}</h1>
{ } | تعبير داخل JSX | <p>{price * 2}</p>
className | صنف CSS | <div className="box">
style | تنسيق مباشر | style={{ color: "red" }}
props | بيانات من الأب | <Card title="أ" />
children | المحتوى بين وسمي المكوّن | function Box({ children }) { … }
useState | حالة | const [v, setV] = useState(0);
useEffect | تأثير بعد العرض | useEffect(() => { … }, []);
useRef | مرجع لعنصر أو قيمة | const inputRef = useRef(null);
onClick / onChange | الأحداث | <button onClick={go}>
&& / ? : | العرض الشرطي | {ok && <p>تم</p>}
map + key | عرض قائمة | items.map(i => <li key={i.id}>…</li>)
<>…</> | تجميع بلا عنصر إضافي | <><A /><B /></>
createRoot | تشغيل التطبيق | ReactDOM.createRoot(el).render(<App />)
```

:::tip ماذا بعد؟
جرّب **Vite** على جهازك لإنشاء مشروع React حقيقي، وتعلّم بعدها التوجيه بين الصفحات (React Router) وجلب البيانات.
:::
