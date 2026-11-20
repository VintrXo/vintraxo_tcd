# @lesson vue-intro
title: Vue introduction
summary: What Vue is and how it binds data to the page.
---
**Vue** is a JavaScript framework for interactive interfaces. You write a normal HTML template and bind it to data; when the data changes, the template updates by itself.

```try html vue
<div id="app">
  <h2>{{ message }}</h2>
  <button @click="count++">Clicked {{ count }} times</button>
</div>
<script>
  Vue.createApp({
    data() {
      return { message: "Hello Vue", count: 0 };
    },
  }).mount("#app");
</script>
```

- `createApp({...})` creates the app, and `mount("#app")` attaches it to the element.
- `data()` returns the data, and `{{ }}` shows it in the template.

:::info In a real project
A Vue project is usually created with `npm create vue@latest`, and components are written in `.vue` files. The examples here run straight in the browser.
:::

```quiz
? What happens in Vue when the data changes?
* The template updates by itself
- You must reload the page
- Nothing changes

? Double braces {{ }} show data inside the template.
= true
```

# @lesson vue-template
title: Templates and expressions
summary: Showing data and expressions in the template.
---
```try html vue
<div id="app">
  <p>Name: {{ user.name }}</p>
  <p>Price with tax: {{ (price * 1.15).toFixed(2) }}</p>
  <p>{{ stock > 0 ? "In stock" : "Sold out" }}</p>
  <p>{{ tags.join(", ") }}</p>
</div>
<script>
  Vue.createApp({
    data() {
      return { user: { name: "Layla" }, price: 80, stock: 3, tags: ["new", "featured"] };
    },
  }).mount("#app");
</script>
```

Inside `{{ }}` you can write any short JavaScript **expression**: arithmetic, a ternary, a function call.

:::warning One expression only
Do not write full statements such as `if` or `let` inside `{{ }}`; put longer logic in `methods` or `computed`.
:::

```quiz
? What can go inside {{ }}?
* A short JavaScript expression
- A full if statement
- A script tag

? A ternary operator can be used inside {{ }}.
= true
```

# @lesson vue-bind
title: Binding attributes with v-bind
summary: Binding attributes, classes and styles to data.
---
`v-bind:` (short form `:`) binds an HTML attribute to a value from the data:

```try html vue
<div id="app">
  <img :src="image" :alt="title" width="160">
  <p :class="{ sale: onSale }" :style="{ fontSize: size + 'px' }">{{ title }}</p>
  <button :disabled="stock === 0">Buy</button>
  <button @click="onSale = !onSale">Toggle sale</button>
</div>
<style>.sale { color: crimson; font-weight: bold; }</style>
<script>
  Vue.createApp({
    data() {
      return { image: "https://picsum.photos/160/100", title: "Leather bag", onSale: true, size: 20, stock: 0 };
    },
  }).mount("#app");
</script>
```

- `:src="image"` takes the value from the data.
- `:class="{ sale: onSale }"` adds the class when the condition is true.

```exercise html
? Bind the href attribute to the variable url
<a ___="url">Link</a>
= :href | v-bind:href
```

```quiz
? What is the short form of v-bind:src?
* :src
- @src
- #src

? :class="{ active: isOn }" adds the class active when isOn is true.
= true
```

# @lesson vue-events
title: Events with v-on
summary: Responding to clicks and typing with methods.
---
`v-on:` (short form `@`) binds an event to a function:

```try html vue
<div id="app">
  <p>Cart: {{ cart }} items</p>
  <button @click="add(1)">Add one</button>
  <button @click="add(5)">Add five</button>
  <button @click="cart = 0">Empty</button>
  <input @keyup.enter="say" placeholder="Type, then Enter">
  <p>{{ last }}</p>
</div>
<script>
  Vue.createApp({
    data() {
      return { cart: 0, last: "" };
    },
    methods: {
      add(n) {
        this.cart += n;
      },
      say(e) {
        this.last = "You typed: " + e.target.value;
      },
    },
  }).mount("#app");
</script>
```

- Functions go in `methods` and reach the data through `this`.
- `@keyup.enter` is an event with a modifier: only when Enter is pressed.

```exercise html
? Complete the code to bind a click to the function save
<button ___="save">Save</button>
= @click | v-on:click
```

```quiz
? What is the short form of v-on:click?
- :click
* @click
- #click

? Inside methods we reach the data through this.
= true
```

# @lesson vue-model
title: Two-way binding with v-model
summary: Binding form fields to data in both directions.
---
`v-model` keeps a field and the data always in step: type and the data changes; change the data and the field changes:

```try html vue
<div id="app">
  <input v-model="name" placeholder="Your name">
  <p>Hello {{ name || "visitor" }}</p>
  <label><input type="checkbox" v-model="agree"> I agree</label>
  <select v-model="city"><option>Riyadh</option><option>Cairo</option></select>
  <p>{{ agree ? "Agreed" : "Not agreed" }} — {{ city }}</p>
  <input type="range" min="1" max="10" v-model.number="qty"> {{ qty }} × 15 = {{ qty * 15 }}
</div>
<script>
  Vue.createApp({
    data() {
      return { name: "", agree: false, city: "Riyadh", qty: 1 };
    },
  }).mount("#app");
</script>
```

`v-model.number` turns the value into a number automatically.

```exercise html
? Bind the field to the variable email in both directions
<input ___="email">
= v-model
```

```quiz
? What does v-model do?
* Binds a field to the data in both directions
- Binds only one attribute
- Sends the form to the server

? The v-model.number modifier turns the value into a number.
= true
```

# @lesson vue-if-for
title: Conditions and lists
summary: v-if, v-else, v-show and v-for.
---
```try html vue
<div id="app">
  <button @click="logged = !logged">{{ logged ? "Log out" : "Log in" }}</button>
  <p v-if="logged">Welcome back</p>
  <p v-else>Please log in</p>
  <ul>
    <li v-for="p in products" :key="p.id">
      {{ p.name }} — ${{ p.price }}
      <strong v-if="p.price > 50">(premium)</strong>
    </li>
  </ul>
  <p v-show="products.length === 0">No products</p>
</div>
<script>
  Vue.createApp({
    data() {
      return {
        logged: false,
        products: [
          { id: 1, name: "Pen", price: 5 },
          { id: 2, name: "Bag", price: 90 },
        ],
      };
    },
  }).mount("#app");
</script>
```

- `v-if` adds or removes the element; `v-show` only hides it with styling.
- `v-for="p in products"` repeats the element, with a unique `:key`.

```quiz
? Which directive repeats an element for each item of an array?
- v-if
* v-for
- v-repeat

? v-show keeps the element on the page and only hides it.
= true
```

# @lesson vue-computed
title: Computed properties
summary: Values computed from data that update automatically, and watch.
---
A **computed property** is a value derived from data; it is recomputed only when the data it depends on changes:

```try html vue
<div id="app">
  <input v-model="search" placeholder="Search">
  <ul><li v-for="n in filtered" :key="n">{{ n }}</li></ul>
  <p>Results: {{ filtered.length }}</p>
</div>
<script>
  Vue.createApp({
    data() {
      return { search: "", names: ["Sara", "Sami", "Omar", "Ali", "Layla"] };
    },
    computed: {
      filtered() {
        return this.names.filter((n) => n.toLowerCase().includes(this.search.toLowerCase()));
      },
    },
    watch: {
      search(value) {
        console.log("search changed to", value);
      },
    },
  }).mount("#app");
</script>
```

- `computed` for derived values (filtering, totals, formatting).
- `watch` to run side work when a value changes (saving, a server request).

```quiz
? When is a computed property recomputed?
* When the data it depends on changes
- On every click on the page
- Only once

? watch is suited to running side work when a value changes.
= true
```

# @lesson vue-components
title: Components
summary: A component with props, and sending events with emit.
---
```try html vue
<div id="app">
  <product-card v-for="p in products" :key="p.id" :name="p.name" :price="p.price" @buy="total += $event"></product-card>
  <p>Total: ${{ total }}</p>
</div>
<script>
  const app = Vue.createApp({
    data() {
      return { total: 0, products: [{ id: 1, name: "Pen", price: 5 }, { id: 2, name: "Notebook", price: 12 }] };
    },
  });
  app.component("product-card", {
    props: ["name", "price"],
    emits: ["buy"],
    template: `
      <div style="border:1px solid #ddd;padding:8px;margin:4px">
        {{ name }} — {{ price }} USD
        <button @click="$emit('buy', price)">Buy</button>
      </div>`,
  });
  app.mount("#app");
</script>
```

- `props` is data that comes from the parent.
- `$emit('buy', price)` sends an event to the parent, which listens with `@buy`.

```quiz
? How does a child component send an event to its parent?
* With $emit
- By changing props
- With return

? props receives data from the parent component.
= true
```

# @lesson vue-project
title: Project: a shopping cart
summary: A small app that brings together what you learned.
---
```try html vue
<div id="app" style="max-width: 380px">
  <div v-for="p in products" :key="p.id" style="display:flex;justify-content:space-between;margin:4px 0">
    <span>{{ p.name }} ({{ p.price }})</span>
    <span>
      <button @click="p.qty > 0 && p.qty--">−</button>
      {{ p.qty }}
      <button @click="p.qty++">+</button>
    </span>
  </div>
  <hr>
  <label><input type="checkbox" v-model="coupon"> 10% coupon</label>
  <p>Subtotal: {{ subtotal }} — after discount: <strong>{{ total.toFixed(2) }}</strong></p>
  <p v-if="subtotal === 0">The cart is empty</p>
</div>
<script>
  Vue.createApp({
    data() {
      return {
        coupon: false,
        products: [
          { id: 1, name: "Pen", price: 5, qty: 0 },
          { id: 2, name: "Notebook", price: 12, qty: 1 },
          { id: 3, name: "Bag", price: 90, qty: 0 },
        ],
      };
    },
    computed: {
      subtotal() {
        return this.products.reduce((s, p) => s + p.price * p.qty, 0);
      },
      total() {
        return this.coupon ? this.subtotal * 0.9 : this.subtotal;
      },
    },
  }).mount("#app");
</script>
```

:::tip Extend it yourself
Add a "remove everything" button, or save the cart in `localStorage` with `watch`.
:::

```quiz
? Why is subtotal a computed property rather than plain data?
* Because it is derived from quantities and prices and updates automatically
- Because plain data cannot hold numbers
- There is no reason

? v-model works with a checkbox.
= true
```

# @lesson vue-reference
title: Vue reference
summary: The main directives and options with an example for each.
type: Reference
---
Search the table for any directive.

```reference html
{{ }} | Show a value | {{ message }}
v-bind / : | Bind an attribute | :src="url"
v-on / @ | Event | @click="save"
v-model | Two-way binding | <input v-model="name">
v-if / v-else | Conditional rendering | <p v-if="ok">…</p>
v-show | Hide with styling | <p v-show="open">…</p>
v-for | Repeat | <li v-for="x in list" :key="x.id">
data() | The data | data() { return { n: 0 }; }
methods | Functions | methods: { add() { … } }
computed | Computed values | computed: { total() { … } }
watch | Watch a value | watch: { q(v) { … } }
props | Data from the parent | props: ["title"]
$emit | Event to the parent | $emit("done", value)
createApp / mount | Start the app | Vue.createApp({…}).mount("#app")
```

:::tip What next?
Create a real project with `npm create vue@latest`, and get to know the **Composition API**, `ref` and `reactive`.
:::
