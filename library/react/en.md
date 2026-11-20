# @lesson react-intro
title: React introduction
summary: What React is and why interfaces are built with it.
---
**React** is a JavaScript library for building user interfaces from **components**: small, independent pieces (a button, a card, a list…) that you combine into a full page. When data changes, React updates only the part of the page that changed.

## Your first app

In this course React is loaded into every example automatically. Press **Run**:

```try html react
<script type="text/babel">
  function App() {
    return <h1>Hello React</h1>;
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- `App` is a component: a function that returns what to show.
- `createRoot(...).render(...)` puts the component inside the `root` element.

:::info In a real project
React projects are usually created with a tool such as **Vite**: `npm create vite@latest my-app -- --template react`. The examples here run straight in the browser so you can learn without installing anything.
:::

```quiz
? What are React interfaces built from?
* Small components combined together
- Only separate HTML pages
- Database tables

? A React component can be a function that returns what to show.
= true
```

# @lesson react-jsx
title: JSX
summary: Writing HTML-like interfaces inside JavaScript.
---
**JSX** lets you write what the interface looks like, as if it were HTML, inside JavaScript:

```try html react
<script type="text/babel">
  const name = "Sara";
  const items = 3;
  function App() {
    return (
      <div>
        <h2>Hello {name}</h2>
        <p>You have {items * 2} items in your cart.</p>
        <p className="note" style={{ color: "teal", fontSize: 18 }}>Styled text</p>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

## JSX rules

- Values and expressions go in `{ }`.
- `className` instead of `class`, and `htmlFor` instead of `for`.
- `style` takes an object: `style={{ color: "red" }}`.
- A component returns one root element; to group several use `<>…</>`.
- Every element is closed: `<img />` and `<br />`.

```exercise javascript
? Complete the code to use a CSS class in JSX
<p ___="title">Text</p>
= className
```

```quiz
? How do you put a variable in JSX?
- ${name}
* {name}
- {{name}}

? In JSX we write className instead of class.
= true
```

# @lesson react-components
title: Components
summary: Creating components and nesting them.
---
A component is a function whose name starts with a **capital letter** and that returns JSX. You then use it like a tag:

```try html react
<script type="text/babel">
  function Header() {
    return <header style={{ background: "#eef2ff", padding: 8 }}><h2>My shop</h2></header>;
  }
  function Product() {
    return <div style={{ border: "1px solid #ddd", padding: 8, margin: 4 }}>A product</div>;
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

:::tip Split the interface
Look at any page as a set of boxes: a header, a menu, cards, a footer. Each box is its own component, easy to understand and reuse.
:::

```quiz
? What must a component's name start with?
* A capital letter
- A lower-case letter
- An underscore

? The same component can be used many times on a page.
= true
```

# @lesson react-props
title: Props
summary: Passing data from a parent component to a child.
---
**Props** are data you pass to a component as attributes, so one component becomes a template for many variations:

```try html react
<script type="text/babel">
  function ProductCard({ name, price, sale = false }) {
    return (
      <div style={{ border: "1px solid #ddd", padding: 8, margin: 4 }}>
        <strong>{name}</strong> — ${price} {sale && <span style={{ color: "crimson" }}>(on sale)</span>}
      </div>
    );
  }
  function App() {
    return (
      <>
        <ProductCard name="Pen" price={5} />
        <ProductCard name="Bag" price={90} sale={true} />
      </>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- Strings go in quotes, everything else in `{ }`: `price={5}`.
- Props are **read-only**; a component does not change them.

```exercise javascript
? Pass the number 10 as the price prop
<ProductCard name="Notebook" price=___ />
= {10}
```

```quiz
? Which way do props flow?
* From parent to child
- From child to parent
- Directly between any two components

? A component may change the props it receives.
= false
```

# @lesson react-state
title: State with useState
summary: Data that changes inside a component and re-renders it.
---
**State** is data a component owns; when it changes, React re-renders the component automatically:

```try html react
<script type="text/babel">
  const { useState } = React;
  function Counter() {
    const [count, setCount] = useState(0);
    return (
      <div>
        <p>Count: {count}</p>
        <button onClick={() => setCount(count + 1)}>Add</button>
        <button onClick={() => setCount(0)}>Reset</button>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<Counter />);
</script>
```

- `useState(0)` returns the current value and a function to change it.
- Never change state directly (`count++`); always use the setter.

:::info In a real project
You import it like this: `import { useState } from "react";`. Here we take it from `React` because the library is loaded on the page.
:::

```exercise javascript
? Complete the code to create state starting as an empty string
const [name, setName] = ___("");
= useState
```

```quiz
? What happens when setCount is called?
* The value changes and the component re-renders
- The value changes without re-rendering
- The component is removed

? The right way to change state is its setter, such as setCount.
= true
```

# @lesson react-events
title: Events
summary: onClick, onChange and onSubmit.
---
```try html react
<script type="text/babel">
  const { useState } = React;
  function App() {
    const [text, setText] = useState("");
    const [liked, setLiked] = useState(false);
    return (
      <div>
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Type something" />
        <p>You typed: {text}</p>
        <button onClick={() => setLiked(!liked)}>{liked ? "❤️ Liked" : "🤍 Like"}</button>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- Event names are camelCase: `onClick`, `onChange`, `onSubmit`.
- Pass a **function**, not a call: `onClick={handle}`, not `onClick={handle()}`.

```quiz
? How is a click event written in React?
- onclick="…"
* onClick={…}
- on-click={…}

? Writing onClick={save()} runs save while rendering, not on click.
= true
```

# @lesson react-conditional
title: Conditional rendering
summary: Showing elements depending on a condition, with && and the ternary.
---
```try html react
<script type="text/babel">
  const { useState } = React;
  function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const messages = 3;
    return (
      <div>
        {loggedIn ? <h3>Welcome back</h3> : <h3>Please log in</h3>}
        {loggedIn && messages > 0 && <p>You have {messages} new messages</p>}
        <button onClick={() => setLoggedIn(!loggedIn)}>{loggedIn ? "Log out" : "Log in"}</button>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

- `condition ? a : b` picks one of two elements.
- `condition && element` shows the element only when the condition holds.

```quiz
? What does {isAdmin && <Panel />} show when isAdmin is false?
* Nothing
- Panel
- The word false

? The ternary operator picks between two elements depending on the condition.
= true
```

# @lesson react-lists
title: Lists and keys
summary: Rendering an array with map, and why key is needed.
---
```try html react
<script type="text/babel">
  const products = [
    { id: 1, name: "Pen", price: 5 },
    { id: 2, name: "Notebook", price: 12 },
    { id: 3, name: "Bag", price: 90 },
  ];
  function App() {
    return (
      <ul>
        {products.map((p) => (
          <li key={p.id}>{p.name}: ${p.price}</li>
        ))}
      </ul>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
```

:::warning Do not forget key
`key` helps React tell which item changed. Use a stable, unique id such as `p.id`, and avoid the array index when the list can change.
:::

```exercise javascript
? Add the right key to each item
{users.map((u) => <li ___={u.id}>{u.name}</li>)}
= key
```

```quiz
? Which function renders a list from an array?
* map
- forEach
- reduce

? key must be unique among the items of a list.
= true
```

# @lesson react-forms
title: Forms
summary: Controlled fields and submitting a form.
---
In React you keep a field's value in state, which makes it **controlled**:

```try html react
<script type="text/babel">
  const { useState } = React;
  function SignUp() {
    const [form, setForm] = useState({ name: "", city: "Riyadh" });
    const [sent, setSent] = useState(null);
    const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
    const submit = (e) => {
      e.preventDefault();
      setSent(form);
    };
    return (
      <form onSubmit={submit}>
        <input name="name" value={form.name} onChange={update} placeholder="Name" required />
        <select name="city" value={form.city} onChange={update}>
          <option>Riyadh</option><option>Cairo</option>
        </select>
        <button>Send</button>
        {sent && <p>Done: {sent.name} from {sent.city}</p>}
      </form>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<SignUp />);
</script>
```

- `value` comes from state and `onChange` updates it.
- `{ ...form, [name]: value }` copies the object and changes one field.
- `e.preventDefault()` stops the page from reloading.

```quiz
? What is a controlled field?
* Its value is kept in state and updated by onChange
- A field you cannot type in
- A field checked by the server

? You must call e.preventDefault() in onSubmit to stop the page reloading.
= true
```

# @lesson react-effects
title: Effects with useEffect
summary: Running code after rendering: timers and fetching data.
---
`useEffect` is for "side" code that runs after a component renders: a timer, fetching data, or updating the page title:

```try html react
<script type="text/babel">
  const { useState, useEffect } = React;
  function Clock() {
    const [seconds, setSeconds] = useState(0);
    useEffect(() => {
      const id = setInterval(() => setSeconds((s) => s + 1), 1000);
      return () => clearInterval(id);   // clean up when the component goes away
    }, []);                              // [] = once, after the first render
    return <p>{seconds} seconds have passed</p>;
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<Clock />);
</script>
```

## The dependency array

- `[]` once, after the first render.
- `[query]` whenever `query` changes.
- No array: after every render (rarely what you want).

```js
useEffect(() => {
  fetch(`/api/products?q=${query}`)
    .then((r) => r.json())
    .then(setProducts);
}, [query]);
```

```quiz
? When does useEffect with an empty dependency array [] run?
* Once, after the first render
- Before every render
- Never

? The function returned by useEffect is for cleanup, such as stopping a timer.
= true
```

# @lesson react-project
title: Project: a to-do list
summary: A small app that brings together everything you learned.
---
A to-do list that adds, removes and ticks off tasks:

```try html react
<script type="text/babel">
  const { useState } = React;
  function TodoApp() {
    const [todos, setTodos] = useState([{ id: 1, text: "Learn React", done: false }]);
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
          <input value={text} onChange={(e) => setText(e.target.value)} placeholder="New task" />
          <button>Add</button>
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
        <p>Left: {left}</p>
      </div>
    );
  }
  ReactDOM.createRoot(document.getElementById("root")).render(<TodoApp />);
</script>
```

:::tip Extend it yourself
Add a "clear completed" button, or a filter that shows all / remaining / done.
:::

```quiz
? Why do we copy the array with [...todos, item] instead of todos.push()?
* Because state is not changed directly; React gets a new copy
- Because push does not exist in JavaScript
- There is no difference

? filter is a good way to remove an item from a list in state.
= true
```

# @lesson react-reference
title: React reference
summary: The key ideas and functions with an example for each.
type: Reference
---
Search the table for any idea.

```reference javascript
component | A function that returns JSX | function Card() { return <div />; }
JSX | Interface inside JavaScript | <h1>{title}</h1>
{ } | An expression in JSX | <p>{price * 2}</p>
className | CSS class | <div className="box">
style | Inline style | style={{ color: "red" }}
props | Data from the parent | <Card title="A" />
children | Content between a component's tags | function Box({ children }) { … }
useState | State | const [v, setV] = useState(0);
useEffect | Effect after render | useEffect(() => { … }, []);
useRef | Reference to an element or value | const inputRef = useRef(null);
onClick / onChange | Events | <button onClick={go}>
&& / ? : | Conditional rendering | {ok && <p>Done</p>}
map + key | Render a list | items.map(i => <li key={i.id}>…</li>)
<>…</> | Group without an extra element | <><A /><B /></>
createRoot | Start the app | ReactDOM.createRoot(el).render(<App />)
```

:::tip What next?
Try **Vite** on your computer to create a real React project, then learn routing between pages (React Router) and fetching data.
:::
