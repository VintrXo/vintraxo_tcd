# @lesson howto-intro
title: Building UI components
summary: How this course works, and the three layers of every component.
---
Most websites are made of the same building blocks: tabs, menus, dialogs, notifications, sliders and forms. This course builds each one from scratch with **HTML** for structure, **CSS** for looks and **JavaScript** for behaviour, so you understand what frameworks and libraries do for you.

Every component follows three rules:

1. **Start with the right HTML element.** A `<button>` is focusable and works with the keyboard for free; a `<div>` with a click handler is not.
2. **Keep state in attributes** such as `aria-expanded`, `hidden` or a class, and let CSS react to it.
3. **Make it work with the keyboard and screen readers**, not only with a mouse.

```try html ui
<style>
  .counter { display: inline-flex; align-items: center; gap: 8px; font: 16px system-ui, sans-serif; }
  .counter button { width: 36px; height: 36px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; font-size: 18px; cursor: pointer; }
  .counter button:focus-visible { outline: 3px solid #4338ca; outline-offset: 2px; }
  .counter output { min-width: 2ch; text-align: center; font-weight: bold; }
</style>
<div class="counter">
  <button type="button" aria-label="Decrease">−</button>
  <output aria-live="polite">0</output>
  <button type="button" aria-label="Increase">+</button>
</div>
<script>
  const [minus, plus] = document.querySelectorAll(".counter button");
  const out = document.querySelector(".counter output");
  let value = 0;
  const render = () => (out.textContent = value);
  minus.addEventListener("click", () => { value = Math.max(0, value - 1); render(); });
  plus.addEventListener("click", () => { value += 1; render(); });
</script>
```

Try it with the keyboard: press **Tab** to reach a button and **Enter** or **Space** to press it. Real buttons give you that for free.

```quiz
? Why use a <button> instead of a clickable <div>?
* A button is focusable and works with the keyboard and screen readers by default
- A div cannot have a click handler
- Buttons load faster

? aria-live="polite" makes screen readers announce changes to that element.
= true
```

# @lesson howto-tabs
title: Tabs
summary: Accessible tabs with roles, aria-selected and arrow-key navigation.
---
```try html ui
<style>
  .tabs [role="tablist"] { display: flex; gap: 4px; border-bottom: 2px solid #e2e8f0; }
  .tabs [role="tab"] { border: 0; background: none; padding: 8px 14px; font: 600 15px system-ui, sans-serif; color: #64748b; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; }
  .tabs [role="tab"][aria-selected="true"] { color: #4338ca; border-bottom-color: #4338ca; }
  .tabs [role="tabpanel"] { padding: 14px 4px; font: 15px/1.6 system-ui, sans-serif; }
</style>
<div class="tabs">
  <div role="tablist" aria-label="Course">
    <button role="tab" id="t1" aria-controls="p1" aria-selected="true">Overview</button>
    <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">Lessons</button>
    <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">Reviews</button>
  </div>
  <div role="tabpanel" id="p1" aria-labelledby="t1">A 6-week course on spreadsheets for teams.</div>
  <div role="tabpanel" id="p2" aria-labelledby="t2" hidden>1. Cells · 2. Formulas · 3. Charts</div>
  <div role="tabpanel" id="p3" aria-labelledby="t3" hidden>★★★★★ "Clear and practical."</div>
</div>
<script>
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function select(tab) {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute("aria-selected", on);
      t.tabIndex = on ? 0 : -1;                       // only the active tab is in the Tab order
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    }
    tab.focus();
  }
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (e) => {
      const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (step) select(tabs[(i + step + tabs.length) % tabs.length]);   // arrows move between tabs
    });
  });
</script>
```

```reference html
role="tablist" / "tab" / "tabpanel" | Tell assistive technology what each part is | <div role="tablist">
aria-selected="true" | The active tab | <button role="tab" aria-selected="true">
aria-controls / aria-labelledby | Link tabs and panels | aria-controls="p1"
hidden | Hide the inactive panels | <div role="tabpanel" hidden>
tabindex="-1" | Remove from the Tab order (arrows move instead) | t.tabIndex = -1
```

```exercise html
? Mark the active tab for screen readers
<button role="tab" ___="true">Overview</button>
= aria-selected
```

```quiz
? Which keys usually move between tabs in an accessible tab list?
* The arrow keys
- Page Up and Page Down
- Only the mouse
```

# @lesson howto-accordion
title: Accordions
summary: details and summary for free, and a custom accordion that allows one open item.
---
```try html ui
<style>
  details { border: 1px solid #e2e8f0; border-radius: 10px; margin-bottom: 8px; font: 15px/1.6 system-ui, sans-serif; }
  summary { padding: 10px 14px; cursor: pointer; font-weight: 600; list-style: none; display: flex; justify-content: space-between; }
  summary::-webkit-details-marker { display: none; }
  summary::after { content: "+"; font-size: 20px; color: #4338ca; }
  details[open] summary::after { content: "−"; }
  details > p { margin: 0; padding: 0 14px 12px; color: #475569; }
</style>

<details name="faq" open>
  <summary>How long is the course?</summary>
  <p>Six weeks, about two hours a week.</p>
</details>
<details name="faq">
  <summary>Do I get a certificate?</summary>
  <p>Yes, after you pass the final quiz.</p>
</details>
<details name="faq">
  <summary>Can I study on my phone?</summary>
  <p>Yes, every lesson works on small screens.</p>
</details>
```

- `<details>` and `<summary>` give you an accordion with **no JavaScript**: it opens with a click, Enter or Space and is announced correctly.
- Giving several `<details>` the same `name` makes them an **exclusive** group: opening one closes the others (supported in current browsers).

:::tip Custom accordions
If you build one with buttons instead, use `<button aria-expanded="false" aria-controls="panel-id">` and toggle both `aria-expanded` and the panel's `hidden` attribute in your click handler.
:::

```exercise html
? Which element holds the always-visible title of a details block?
<details><___>Shipping</summary><p>3 to 5 days.</p></details>
= summary
```

```quiz
? What happens when several details elements share the same name?
* Only one of them can be open at a time
- They all open together
- The page reloads
```

# @lesson howto-modal
title: Modal dialogs
summary: The dialog element, showModal, focus, closing with Escape, and returning a value.
---
```try html ui
<style>
  dialog { border: 0; border-radius: 14px; padding: 20px; max-width: 360px; font: 15px/1.6 system-ui, sans-serif; box-shadow: 0 20px 50px rgb(0 0 0 / .25); }
  dialog::backdrop { background: rgb(15 23 42 / .5); }
  dialog h2 { margin: 0 0 8px; font-size: 18px; }
  .actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 14px; }
  button { padding: 7px 14px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
  .danger { background: #b91c1c; color: #fff; border-color: #b91c1c; }
</style>

<button id="open">Delete account…</button>
<p id="result"></p>

<dialog id="confirm" aria-labelledby="confirm-title">
  <form method="dialog">
    <h2 id="confirm-title">Delete your account?</h2>
    <p>This removes your courses and certificates. It cannot be undone.</p>
    <div class="actions">
      <button value="cancel" autofocus>Cancel</button>
      <button value="delete" class="danger">Delete</button>
    </div>
  </form>
</dialog>

<script>
  const dialog = document.getElementById("confirm");
  document.getElementById("open").addEventListener("click", () => dialog.showModal());
  dialog.addEventListener("close", () => {
    document.getElementById("result").textContent = "You chose: " + dialog.returnValue;
  });
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close("cancel"); });   // click outside
</script>
```

`showModal()` gives you a lot for free: the backdrop, keeping focus inside the dialog, closing with **Escape**, and returning focus to the button that opened it. A `<form method="dialog">` closes the dialog and puts the pressed button's `value` in `dialog.returnValue`.

```reference html
<dialog> | A dialog box | <dialog id="d">...</dialog>
dialog.showModal() / show() | Open as modal / non-modal | d.showModal()
dialog.close(value) | Close and set returnValue | d.close("ok")
<form method="dialog"> | Buttons close the dialog | <button value="yes">Yes</button>
::backdrop | Style the dimmed background | dialog::backdrop { background: #0008; }
autofocus | Where focus starts | <button autofocus>Cancel</button>
```

```exercise javascript
? Open the dialog d as a modal
d.___();
= showModal
```

```quiz
? Why put autofocus on the Cancel button in a delete confirmation?
* So pressing Enter by accident does the safe action
- To make the button bigger
- Because dialogs need it to open
```

# @lesson howto-dropdown
title: Dropdown menus
summary: A menu button with aria-expanded, closing on outside click and Escape.
---
```try html ui
<style>
  .menu { position: relative; display: inline-block; font: 15px system-ui, sans-serif; }
  .menu > button { padding: 8px 14px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
  .menu ul { position: absolute; top: calc(100% + 4px); left: 0; min-width: 180px; margin: 0; padding: 6px; list-style: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; box-shadow: 0 10px 30px rgb(0 0 0 / .12); }
  .menu a { display: block; padding: 7px 10px; border-radius: 6px; color: #0f172a; text-decoration: none; }
  .menu a:hover, .menu a:focus { background: #eef2ff; outline: none; }
</style>

<div class="menu">
  <button aria-expanded="false" aria-controls="account-menu">My account ▾</button>
  <ul id="account-menu" hidden>
    <li><a href="#">Profile</a></li>
    <li><a href="#">My certificates</a></li>
    <li><a href="#">Sign out</a></li>
  </ul>
</div>
<p style="margin-top: 140px; font: 14px system-ui; color: #64748b">Click outside the menu or press Escape to close it.</p>

<script>
  const button = document.querySelector(".menu > button");
  const list = document.getElementById("account-menu");
  function setOpen(open) {
    button.setAttribute("aria-expanded", open);
    list.hidden = !open;
    if (open) list.querySelector("a").focus();
  }
  button.addEventListener("click", () => setOpen(list.hidden));
  document.addEventListener("click", (e) => { if (!e.target.closest(".menu")) setOpen(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !list.hidden) { setOpen(false); button.focus(); }
  });
</script>
```

```reference javascript
aria-expanded | Tell screen readers if the menu is open | btn.setAttribute("aria-expanded", true)
element.hidden | Show or hide | list.hidden = !open
e.target.closest(sel) | Was the click inside the component? | if (!e.target.closest(".menu"))
keydown "Escape" | Close and return focus to the button | button.focus()
position: absolute | Place the menu under its button | top: 100%; left: 0
```

:::tip Return focus
When a menu or dialog closes, move the keyboard focus back to the button that opened it. Otherwise keyboard users lose their place on the page.
:::

```exercise html
? Tell assistive technology the menu is closed
<button ___="false">Menu</button>
= aria-expanded
```

```quiz
? What should happen when the user presses Escape in an open menu?
* The menu closes and focus returns to its button
- The page scrolls to the top
- Nothing
```

# @lesson howto-navbar
title: A responsive navigation bar
summary: A top bar that turns into a menu button on small screens.
---
```try html ui
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font: 15px system-ui, sans-serif; }
  .bar { display: flex; align-items: center; gap: 16px; padding: 10px 16px; background: #312e81; color: #fff; flex-wrap: wrap; }
  .brand { font-weight: 800; margin-inline-end: auto; }
  .links { display: flex; gap: 6px; margin: 0; padding: 0; list-style: none; }
  .links a { color: #e0e7ff; text-decoration: none; padding: 6px 10px; border-radius: 6px; }
  .links a[aria-current="page"], .links a:hover { background: rgb(255 255 255 / .15); color: #fff; }
  .toggle { display: none; background: none; border: 1px solid rgb(255 255 255 / .4); color: #fff; border-radius: 6px; padding: 4px 10px; font-size: 18px; }
  @media (max-width: 560px) {                     /* phones: the links fold into a menu */
    .toggle { display: block; }
    .links { display: none; flex-basis: 100%; flex-direction: column; }
    .bar.open .links { display: flex; }
  }
</style>

<nav class="bar" aria-label="Main">
  <span class="brand">Academy</span>
  <button class="toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">☰</button>
  <ul class="links" id="nav-links">
    <li><a href="#" aria-current="page">Home</a></li>
    <li><a href="#">Courses</a></li>
    <li><a href="#">Certificates</a></li>
    <li><a href="#">Help</a></li>
  </ul>
</nav>
<p style="padding: 16px">Make the preview narrower (or use full screen on a phone) to see the menu button.</p>

<script>
  const bar = document.querySelector(".bar");
  const toggle = document.querySelector(".toggle");
  toggle.addEventListener("click", () => {
    const open = bar.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
</script>
```

- A **media query** hides the links and shows the ☰ button below 560px wide.
- `aria-current="page"` marks the page you are on, both visually (via CSS) and for screen readers.
- `<nav aria-label="Main">` lets screen-reader users jump straight to the main navigation.

```exercise html
? Mark the link of the current page
<a href="/courses" ___="page">Courses</a>
= aria-current
```

```quiz
? What makes the links collapse into a menu on phones?
* A CSS media query on the screen width
- A different HTML file for phones
- The browser does it automatically
```

# @lesson howto-toast
title: Toast notifications
summary: Short messages that appear and disappear, announced to screen readers.
---
```try html ui
<style>
  .toasts { position: fixed; inset-block-end: 16px; inset-inline-end: 16px; display: grid; gap: 8px; z-index: 10; }
  .toast { min-width: 220px; padding: 10px 14px; border-radius: 10px; color: #fff; font: 14px system-ui, sans-serif; box-shadow: 0 8px 24px rgb(0 0 0 / .2); animation: in .25s ease-out; }
  .toast.ok { background: #15803d; } .toast.err { background: #b91c1c; } .toast.info { background: #334155; }
  .toast.leaving { opacity: 0; transform: translateY(8px); transition: .3s; }
  @keyframes in { from { opacity: 0; transform: translateY(8px); } }
  button { margin: 4px; padding: 7px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
</style>

<button data-kind="ok">Save</button>
<button data-kind="err">Fail payment</button>
<button data-kind="info">Info</button>
<div class="toasts" role="status" aria-live="polite"></div>

<script>
  const box = document.querySelector(".toasts");
  const texts = { ok: "Saved successfully", err: "Payment failed. Try again.", info: "A new lesson is available" };
  function toast(kind, text, ms = 3000) {
    const t = document.createElement("div");
    t.className = "toast " + kind;
    t.textContent = text;                              // textContent: never inject HTML
    box.appendChild(t);
    setTimeout(() => {
      t.classList.add("leaving");
      t.addEventListener("transitionend", () => t.remove(), { once: true });
    }, ms);
  }
  document.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => toast(b.dataset.kind, texts[b.dataset.kind])));
</script>
```

```reference html
role="status" aria-live="polite" | Announce new messages without interrupting | <div role="status" aria-live="polite">
role="alert" | Announce urgent messages at once | <div role="alert">Error</div>
position: fixed | Stay in a corner while scrolling | inset-block-end: 16px
setTimeout + transitionend | Fade out, then remove | t.remove()
```

:::warning Do not hide important errors in toasts
A toast disappears after a few seconds. Errors the user must act on (such as a failed payment) should also stay visible next to the form or button.
:::

```quiz
? Which attribute makes screen readers announce a new toast politely?
* aria-live="polite"
- aria-hidden="true"
- tabindex="0"
```

# @lesson howto-tooltip
title: Tooltips
summary: Pure CSS tooltips that also work with keyboard focus.
---
```try html ui
<style>
  body { font: 15px system-ui, sans-serif; padding: 50px 16px; }
  .tip { position: relative; display: inline-block; }
  .tip [role="tooltip"] {
    position: absolute; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%);
    background: #0f172a; color: #fff; padding: 6px 10px; border-radius: 6px; font-size: 13px; white-space: nowrap;
    opacity: 0; pointer-events: none; transition: opacity .15s;
  }
  .tip [role="tooltip"]::after { content: ""; position: absolute; top: 100%; left: 50%; margin-left: -5px; border: 5px solid transparent; border-top-color: #0f172a; }
  .tip:hover [role="tooltip"], .tip:focus-within [role="tooltip"] { opacity: 1; }   /* mouse AND keyboard */
  button { padding: 7px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; }
</style>

<span class="tip">
  <button aria-describedby="tip-export">Export</button>
  <span role="tooltip" id="tip-export">Download your results as CSV</span>
</span>
&nbsp;
<span class="tip">
  <button aria-describedby="tip-share">Share</button>
  <span role="tooltip" id="tip-share">Copy a link to this course</span>
</span>
```

- `:focus-within` shows the tooltip when a keyboard user tabs to the button, not only on mouse hover.
- `aria-describedby` makes screen readers read the tooltip text after the button's name.

:::tip Tooltips are extras
Phones have no hover, and tooltips are easy to miss. Never put essential information only in a tooltip.
:::

```exercise html
? Link the button to its description
<button ___="tip-1">Save</button>
= aria-describedby
```

```quiz
? Why does the CSS use :focus-within as well as :hover?
* So keyboard users see the tooltip too
- To make the tooltip blink
- Because :hover does not work on buttons
```

# @lesson howto-carousel
title: Carousels with CSS scroll snap
summary: A swipeable slider with scroll-snap, buttons and a slide counter.
---
```try html ui
<style>
  body { font: 15px system-ui, sans-serif; }
  .slider { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; padding-bottom: 8px; }
  .slide { flex: 0 0 80%; scroll-snap-align: center; height: 140px; border-radius: 14px; color: #fff; display: grid; place-items: center; font-size: 22px; font-weight: 800; }
  .controls { display: flex; align-items: center; gap: 10px; margin-top: 8px; }
  .controls button { width: 36px; height: 36px; border-radius: 50%; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
</style>

<div class="slider" tabindex="0" aria-label="Featured courses">
  <div class="slide" style="background:#4338ca">Python</div>
  <div class="slide" style="background:#0e7490">SQL</div>
  <div class="slide" style="background:#be185d">Marketing</div>
  <div class="slide" style="background:#b45309">Statistics</div>
</div>
<div class="controls">
  <button aria-label="Previous">‹</button>
  <span id="count" aria-live="polite">1 / 4</span>
  <button aria-label="Next">›</button>
</div>

<script>
  const slider = document.querySelector(".slider");
  const slides = [...slider.children];
  const [prev, next] = document.querySelectorAll(".controls button");
  const current = () => Math.round(slider.scrollLeft / (slides[1].offsetLeft - slides[0].offsetLeft));
  const go = (i) => slides[Math.max(0, Math.min(slides.length - 1, i))].scrollIntoView({ inline: "center", block: "nearest" });
  prev.addEventListener("click", () => go(current() - 1));
  next.addEventListener("click", () => go(current() + 1));
  slider.addEventListener("scroll", () => (document.getElementById("count").textContent = current() + 1 + " / " + slides.length));
</script>
```

`scroll-snap-type` makes the browser stop exactly on a slide, and swiping on phones works with no extra code. The buttons only call `scrollIntoView`.

```reference css
overflow-x: auto | Horizontal scrolling | .slider { overflow-x: auto; }
scroll-snap-type: x mandatory | Snap to items while scrolling | scroll-snap-type: x mandatory
scroll-snap-align: center | Where each item snaps | .slide { scroll-snap-align: start; }
scroll-behavior: smooth | Animate programmatic scrolling | scroll-behavior: smooth
el.scrollIntoView({ inline: "center" }) | Scroll to an item | slide.scrollIntoView({ inline: "center" })
```

```exercise css
? Make the container snap to its slides horizontally
.slider { scroll-snap-type: ___ mandatory; }
= x
```

```quiz
? Why are carousels built on native scrolling easier to use on phones?
* Swiping works without extra code
- They load more images
- They disable scrolling
```

# @lesson howto-form
title: Form validation
summary: Built-in validation, clear error messages, and checking passwords with JavaScript.
---
```try html ui
<style>
  form { display: grid; gap: 10px; max-width: 340px; font: 15px system-ui, sans-serif; }
  label { display: grid; gap: 4px; font-weight: 600; }
  input { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font: inherit; }
  input:user-invalid { border-color: #b91c1c; }                 /* only after the user touched it */
  .error { color: #b91c1c; font-size: 13px; font-weight: 400; min-height: 1em; }
  button { padding: 9px; border: 0; border-radius: 8px; background: #4338ca; color: #fff; font-weight: 700; }
  #done { color: #15803d; }
</style>

<form novalidate>
  <label>Email
    <input type="email" name="email" required autocomplete="email" aria-describedby="email-err">
    <span class="error" id="email-err"></span>
  </label>
  <label>Password (at least 8 characters, with a number)
    <input type="password" name="password" required minlength="8" pattern="(?=.*\d).{8,}" autocomplete="new-password" aria-describedby="pw-err">
    <span class="error" id="pw-err"></span>
  </label>
  <label>Repeat password
    <input type="password" name="confirm" required autocomplete="new-password" aria-describedby="cf-err">
    <span class="error" id="cf-err"></span>
  </label>
  <button>Create account</button>
  <p id="done" role="status"></p>
</form>

<script>
  const form = document.querySelector("form");
  const messages = {
    email: (i) => i.validity.valueMissing ? "Enter your email." : "Enter a valid email like name@example.com.",
    password: (i) => i.validity.valueMissing ? "Choose a password." : "Use 8 or more characters including a number.",
    confirm: (i) => i.validity.valueMissing ? "Repeat your password." : "The passwords do not match.",
  };
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    form.confirm.setCustomValidity(form.confirm.value === form.password.value ? "" : "mismatch");
    let firstBad = null;
    for (const input of form.querySelectorAll("input")) {
      const err = document.getElementById(input.getAttribute("aria-describedby"));
      const ok = input.checkValidity();
      err.textContent = ok ? "" : messages[input.name](input);
      input.setAttribute("aria-invalid", !ok);
      if (!ok && !firstBad) firstBad = input;
    }
    if (firstBad) return firstBad.focus();          // send the user to the first problem
    document.getElementById("done").textContent = "Account created (demo).";
  });
</script>
```

```reference html
required / minlength / pattern | Built-in rules | <input required minlength="8">
type="email" / "number" / "url" | Typed inputs with their own checks | <input type="email">
input.checkValidity() / validity | Check a field in JavaScript | if (!input.checkValidity())
setCustomValidity(msg) | Your own rule ("" means valid) | input.setCustomValidity("")
:user-invalid | Style only after the user interacted | input:user-invalid { border-color: red; }
aria-invalid / aria-describedby | Tell screen readers about errors | aria-describedby="email-err"
autocomplete | Let browsers and password managers help | autocomplete="new-password"
```

:::danger The browser check is only for comfort
Anyone can send data to your server without your form. The server must validate everything again.
:::

```exercise html
? Make the field mandatory
<input type="email" ___>
= required
```

```quiz
? After a failed submit, where should the keyboard focus go?
* To the first field with an error
- To the top of the page
- Nowhere, it should stay on the button
```

# @lesson howto-dark-mode
title: Dark mode toggle
summary: CSS variables, prefers-color-scheme, and remembering the user's choice.
---
```try html ui
<style>
  :root { --bg: #ffffff; --text: #0f172a; --card: #f1f5f9; --brand: #4338ca; color-scheme: light; }
  @media (prefers-color-scheme: dark) {                 /* follow the system... */
    :root:not([data-theme="light"]) { --bg: #0f172a; --text: #e2e8f0; --card: #1e293b; --brand: #a5b4fc; color-scheme: dark; }
  }
  :root[data-theme="dark"] { --bg: #0f172a; --text: #e2e8f0; --card: #1e293b; --brand: #a5b4fc; color-scheme: dark; }   /* ...unless the user chose */
  body { background: var(--bg); color: var(--text); font: 15px system-ui, sans-serif; padding: 16px; transition: background .2s, color .2s; }
  .card { background: var(--card); padding: 14px; border-radius: 12px; }
  .card h3 { color: var(--brand); margin: 0 0 6px; }
  button { padding: 7px 12px; border-radius: 8px; border: 1px solid currentColor; background: none; color: inherit; cursor: pointer; }
</style>

<button id="theme" aria-pressed="false">🌙 Dark mode</button>
<div class="card" style="margin-top: 12px">
  <h3>Your progress</h3>
  <p>3 of 8 lessons done this week.</p>
</div>

<script>
  const root = document.documentElement;
  const btn = document.getElementById("theme");
  function apply(theme) {
    root.dataset.theme = theme;
    btn.setAttribute("aria-pressed", theme === "dark");
    btn.textContent = theme === "dark" ? "☀️ Light mode" : "🌙 Dark mode";
  }
  let saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}   // storage can be blocked
  apply(saved || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  btn.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    apply(theme);
    try { localStorage.setItem("theme", theme); } catch (e) {}
  });
</script>
```

```reference css
--name: value / var(--name) | CSS variables for colors | color: var(--text);
@media (prefers-color-scheme: dark) | The system's dark setting | @media (prefers-color-scheme: dark) { }
:root[data-theme="dark"] | The user's own choice wins | <html data-theme="dark">
color-scheme: dark | Dark form controls and scrollbars | :root { color-scheme: dark; }
localStorage | Remember the choice in this browser | localStorage.setItem("theme", "dark")
```

```exercise css
? Use the variable named text for the color
body { color: ___(--text); }
= var
```

```quiz
? Why define colors as CSS variables for a dark mode?
* So switching themes only changes a few variable values
- Because dark mode needs JavaScript for every element
- To make the page load faster
```

# @lesson howto-filter
title: Search and filter a list
summary: Filter items while typing, show a count, and handle "no results".
---
```try html ui
<style>
  body { font: 15px system-ui, sans-serif; }
  input[type=search] { width: 100%; max-width: 360px; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 10px; }
  .chips { display: flex; gap: 6px; margin: 10px 0; flex-wrap: wrap; }
  .chips button { border: 1px solid #cbd5e1; background: #fff; padding: 4px 12px; border-radius: 999px; cursor: pointer; }
  .chips button[aria-pressed="true"] { background: #4338ca; color: #fff; border-color: #4338ca; }
  ul { list-style: none; padding: 0; display: grid; gap: 6px; max-width: 360px; }
  li { padding: 8px 12px; background: #f8fafc; border-radius: 8px; display: flex; justify-content: space-between; }
  li small { color: #64748b; }
  mark { background: #fef08a; }
</style>

<input type="search" placeholder="Search courses" aria-label="Search courses">
<div class="chips" role="group" aria-label="Level">
  <button aria-pressed="true" data-level="all">All</button>
  <button aria-pressed="false" data-level="Beginner">Beginner</button>
  <button aria-pressed="false" data-level="Advanced">Advanced</button>
</div>
<p id="count" role="status"></p>
<ul id="list"></ul>

<script>
  const courses = [
    ["Python basics", "Beginner"], ["SQL for analysts", "Beginner"], ["Machine learning", "Advanced"],
    ["PostgreSQL performance", "Advanced"], ["Excel formulas", "Beginner"], ["Statistics with Python", "Advanced"],
  ];
  const input = document.querySelector("input"), list = document.getElementById("list"), count = document.getElementById("count");
  let level = "all";
  function render() {
    const q = input.value.trim().toLowerCase();
    const shown = courses.filter(([name, lv]) => (level === "all" || lv === level) && name.toLowerCase().includes(q));
    list.replaceChildren(...shown.map(([name, lv]) => {
      const li = document.createElement("li");
      const title = document.createElement("span");
      const i = q ? name.toLowerCase().indexOf(q) : -1;
      if (i >= 0) {                                         // highlight the match safely, without innerHTML
        const mark = document.createElement("mark");
        mark.textContent = name.slice(i, i + q.length);
        title.append(name.slice(0, i), mark, name.slice(i + q.length));
      } else title.textContent = name;
      const small = document.createElement("small");
      small.textContent = lv;
      li.append(title, small);
      return li;
    }));
    count.textContent = shown.length ? shown.length + " course(s)" : "No courses match. Try a shorter word.";
  }
  input.addEventListener("input", render);
  document.querySelectorAll(".chips button").forEach((b) => b.addEventListener("click", () => {
    level = b.dataset.level;
    document.querySelectorAll(".chips button").forEach((x) => x.setAttribute("aria-pressed", x === b));
    render();
  }));
  render();
</script>
```

- The search box filters as you type; the level buttons narrow further; both work together.
- The match is highlighted with a `<mark>` element built from text nodes, so a search word can never inject HTML.
- `role="status"` announces the number of results to screen-reader users.

```quiz
? Why does the highlight code build elements instead of using innerHTML?
* So text typed by the user can never be interpreted as HTML
- Because innerHTML is not supported in lists
- To make the list sort itself
```

# @lesson howto-reference
title: UI components quick reference
summary: The right element and attributes for each common component.
---
| Component | Start with | Key attributes |
|---|---|---|
| Button | `<button type="button">` | `aria-label` for icon buttons |
| Tabs | `role="tablist"`, `tab`, `tabpanel` | `aria-selected`, `aria-controls`, arrow keys |
| Accordion | `<details>` / `<summary>` | `name` for exclusive groups |
| Dialog | `<dialog>` + `showModal()` | `<form method="dialog">`, `autofocus` |
| Dropdown | `<button>` + list | `aria-expanded`, Escape, outside click |
| Navigation | `<nav aria-label>` | `aria-current="page"`, media query |
| Toast | container with `role="status"` | `aria-live="polite"` |
| Tooltip | `role="tooltip"` | `aria-describedby`, `:focus-within` |
| Carousel | scroll container | `scroll-snap-type`, `scrollIntoView` |
| Form | `<label>` + `<input>` | `required`, `aria-invalid`, `aria-describedby` |

```reference html
:focus-visible | Show focus rings for keyboard users | button:focus-visible { outline: 3px solid; }
hidden | Hide content from everyone | panel.hidden = true
aria-label / aria-labelledby | Give an element a name | <button aria-label="Close">×</button>
aria-expanded / aria-pressed / aria-selected | State of toggles | btn.setAttribute("aria-expanded", true)
aria-live / role="status" | Announce changes | <p role="status"></p>
textContent | Put user text on the page safely | el.textContent = name
```

:::tip Where to go next
Take one component you need at work, build it this way, and test it with only the keyboard (Tab, Shift+Tab, Enter, Space, Escape, arrows). Then look at how a library such as Headless UI or Radix implements the same pattern.
:::

```quiz
? What is the quickest way to test a component's accessibility yourself?
* Use it with only the keyboard
- Look at it on a big screen
- Count the lines of JavaScript
```
