# @lesson jq-intro
title: jQuery introduction
summary: What jQuery is, how to add it, and $(document).ready.
---
**jQuery** is a small JavaScript library that makes common page tasks short: finding elements, reacting to clicks, changing content and styles, animating, and talking to the server. Modern browsers can do all of this with plain JavaScript, but jQuery is still on a very large number of websites, so it is worth reading and writing.

## Adding it to your page

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
```

In this course the line is added to every example automatically.

```try html jq
<p id="msg">Waiting…</p>
<script>
$(function () {                 // runs when the page is ready
  $("#msg").text("Hello from jQuery!");
});
</script>
```

- `$` is the jQuery function. `$("#msg")` finds the element with id `msg`.
- `$(function () { ... })` is short for `$(document).ready(...)`: the code waits until the page has loaded.
- `.text(...)` sets the text of what was found.

```quiz
? What does $("#msg") select?
* The element whose id is msg
- Every element with the class msg
- Every <msg> tag

? jQuery code must be loaded after the jQuery script itself.
= true
```

# @lesson jq-selectors
title: Selectors
summary: Finding elements with CSS selectors and jQuery filters.
---
jQuery uses the same selectors as CSS, plus a few extras.

```try html jq
<ul>
  <li>Tea</li>
  <li class="hot">Coffee</li>
  <li>Juice</li>
  <li class="hot">Cocoa</li>
</ul>
<p>Total items: <b id="count"></b></p>
<script>
$(function () {
  $("li").css("padding", "2px");              // every <li>
  $(".hot").css("color", "crimson");           // class
  $("li:first").css("font-weight", "bold");    // jQuery filter
  $("li:even").css("background", "#f1f1f1");   // 0th, 2nd, ...
  $("ul li").last().append(" (last)");
  $("#count").text($("li").length);
});
</script>
```

```reference javascript
$("#id") | By id | $("#menu")
$(".class") | By class | $(".active")
$("tag") | By tag name | $("p")
$("a b") | b inside a | $("nav a")
$("[name=email]") | By attribute | $("input[type=checkbox]")
:first / :last / :even | jQuery position filters | $("tr:even")
.length | How many were found | $("li").length
.eq(i) / .first() / .last() | One item from the set | $("li").eq(2)
```

:::tip One selection, many elements
`$("li")` returns a set. Calling `.css(...)` on it changes **every** element in the set; you do not need a loop.
:::

```exercise javascript
? Select every element with the class active
$("___")
= .active
```

```quiz
? What does $("li").length give?
* How many li elements were found
- The text length of the first li
- Always 1
```

# @lesson jq-events
title: Events
summary: click, on, hover, keyup, the event object and this.
---
```try html jq
<button id="add">Add one</button>
<button id="reset">Reset</button>
<p>Clicks: <b id="n">0</b></p>
<input id="name" placeholder="Type your name">
<p id="hello"></p>
<div class="box" id="area">Move the mouse over me</div>
<script>
$(function () {
  let count = 0;
  $("#add").on("click", function () {
    count++;
    $("#n").text(count);
  });
  $("#reset").click(() => { count = 0; $("#n").text(0); });

  $("#name").on("keyup", function () {
    $("#hello").text("Hello, " + $(this).val());   // this = the input
  });

  $("#area").hover(
    function () { $(this).addClass("highlight"); },
    function () { $(this).removeClass("highlight"); }
  );

  $(document).on("keydown", function (e) {
    if (e.key === "Escape") $("#name").val("").trigger("keyup");
  });
});
</script>
```

```reference javascript
.on("click", fn) | Attach a handler | $("#save").on("click", save)
.click(fn) / .change(fn) | Shortcuts | $("select").change(update)
.hover(in, out) | Mouse enters / leaves | $(".card").hover(a, b)
$(this) | The element that fired the event | $(this).hide()
e.preventDefault() | Stop the default action | link or form submit
.off("click") | Remove handlers | $("#btn").off("click")
.trigger("click") | Fire an event from code | $("#btn").trigger("click")
```

:::warning Arrow functions and this
Inside an arrow function `this` is not the element. Use a normal `function () { ... }` when you need `$(this)`, or use `e.currentTarget`.
:::

```exercise javascript
? Attach a click handler with the general method
$("#save").___("click", save);
= on
```

```quiz
? Inside a normal handler function, what is $(this)?
* The element that fired the event
- The whole document
- The jQuery library
```

# @lesson jq-dom
title: Changing content
summary: text, html, append, prepend, before, after, remove and empty.
---
```try html jq
<div id="list" class="box"><p>First item</p></div>
<button id="end">Append</button>
<button id="start">Prepend</button>
<button id="clear">Empty</button>
<p id="info"></p>
<script>
$(function () {
  let n = 1;
  $("#end").on("click", function () {
    n++;
    $("#list").append("<p>Item " + n + "</p>");
  });
  $("#start").on("click", function () {
    $("<p>").text("Added at the top").css("color", "teal").prependTo("#list");
  });
  $("#clear").on("click", function () {
    $("#list").empty();
  });
  $("#list").before("<h4>My list</h4>");

  const userText = "<b>not bold</b>";
  $("#info").text(userText);   // shown as text, safe
});
</script>
```

```reference javascript
.text() / .text(v) | Read / set text | $("h1").text("Hi")
.html() / .html(v) | Read / set HTML | $("#box").html("<b>ok</b>")
.append / .prepend | Add inside, at the end / start | $("ul").append("<li>x</li>")
.after / .before | Add next to it | $("h2").after("<hr>")
$("<p>") | Create a new element | $("<li>").text(name)
.appendTo / .prependTo | Insert the new element | $("<li>").appendTo("ul")
.remove() / .empty() | Delete it / delete its children | $(".old").remove()
```

:::danger .text() for user input, never .html()
`.html(userInput)` runs any HTML or scripts the user typed (XSS). Put untrusted text in with `.text()`, or build elements with `$("<li>").text(value)`.
:::

```exercise javascript
? Add a new list item at the end of #todo
$("#todo").___("<li>Read</li>");
= append
```

```quiz
? Which method is safe for showing text that a user typed?
* .text()
- .html()
- .append() with a string of HTML

? .empty() removes the children but keeps the element itself.
= true
```

# @lesson jq-css
title: CSS and classes
summary: css, addClass, removeClass, toggleClass, hasClass and sizes.
---
```try html jq
<style>.big { font-size: 1.6em; } .dark { background: #222; color: #eee; }</style>
<div class="box" id="card">A card</div>
<button id="big">Toggle big</button>
<button id="dark">Toggle dark</button>
<p id="state"></p>
<script>
$(function () {
  function show() {
    $("#state").text(
      "dark: " + $("#card").hasClass("dark") +
      ", width: " + Math.round($("#card").width()) + "px" +
      ", color: " + $("#card").css("color")
    );
  }
  $("#big").on("click", function () { $("#card").toggleClass("big"); show(); });
  $("#dark").on("click", function () { $("#card").toggleClass("dark"); show(); });
  $("#card").css({ border: "2px solid #4a7", "border-radius": "10px" });
  show();
});
</script>
```

```reference javascript
.css("prop") | Read a style | $("p").css("color")
.css("prop", v) / .css({..}) | Set one / several styles | $("p").css({ color: "red" })
.addClass / .removeClass | Add / remove a class | $("li").addClass("done")
.toggleClass | Add if missing, remove if present | $("#menu").toggleClass("open")
.hasClass | Does it have the class? | if ($(this).hasClass("on"))
.width() / .height() | Size in pixels | $(window).width()
```

:::tip Prefer classes over inline styles
Keep the look in CSS and switch it with `addClass` / `toggleClass`. It is easier to change later than many `.css(...)` calls spread across your code.
:::

```exercise javascript
? Switch the class open on and off on #menu
$("#menu").___("open");
= toggleClass
```

```quiz
? What does .toggleClass("done") do when the element already has the class done?
* Removes it
- Adds it a second time
- Nothing
```

# @lesson jq-forms
title: Forms, values and attributes
summary: val, attr, prop, submit and simple validation.
---
```try html jq
<form id="signup">
  <input id="email" type="email" placeholder="Email"><br>
  <label><input id="terms" type="checkbox"> I accept the terms</label><br>
  <select id="plan"><option value="free">Free</option><option value="pro">Pro</option></select>
  <button>Sign up</button>
</form>
<p id="result"></p>
<a id="link" href="https://example.com">a link</a>
<script>
$(function () {
  $("#signup").on("submit", function (e) {
    e.preventDefault();                       // stay on the page
    const email = $("#email").val().trim();
    if (!email.includes("@")) {
      $("#result").text("Please enter a valid email").css("color", "crimson");
      return;
    }
    if (!$("#terms").prop("checked")) {
      $("#result").text("Please accept the terms").css("color", "crimson");
      return;
    }
    $("#result").text("Welcome " + email + ", plan: " + $("#plan").val()).css("color", "green");
    $(this).find("button").prop("disabled", true);
  });
  $("#link").attr("target", "_blank").text("opens in a new tab: " + $("#link").attr("href"));
});
</script>
```

```reference javascript
.val() / .val(v) | Read / set an input's value | $("#q").val()
.attr("name") / .attr(n, v) | Read / set an HTML attribute | $("img").attr("src", url)
.prop("checked") | Live state: checked, disabled, selected | $("#ok").prop("checked")
.prop("disabled", true) | Disable a control | $("button").prop("disabled", true)
.on("submit", fn) | Handle a form submit | $("form").on("submit", send)
.serialize() | Form fields as a query string | $("form").serialize()
```

:::warning Checking in the browser is not enough
Browser checks help the user, but anyone can send any data to your server. Always validate again on the server.
:::

```exercise javascript
? Read whether the checkbox #terms is ticked
$("#terms").___("checked")
= prop
```

```quiz
? Which method reads the text typed in an input?
* .val()
- .text()
- .html()
```

# @lesson jq-effects
title: Effects and animation
summary: hide, show, toggle, fade, slide, animate and chaining.
---
```try html jq
<button id="t">Toggle</button>
<button id="f">Fade</button>
<button id="s">Slide</button>
<button id="a">Animate</button>
<div class="box" id="panel">I am a panel</div>
<script>
$(function () {
  $("#t").on("click", () => $("#panel").toggle());
  $("#f").on("click", () => $("#panel").fadeToggle(400));
  $("#s").on("click", () => $("#panel").slideToggle("fast"));
  $("#a").on("click", function () {
    $("#panel")
      .animate({ paddingLeft: "60px", opacity: 0.5 }, 400)
      .animate({ paddingLeft: "10px", opacity: 1 }, 400, function () {
        $(this).text("Animation finished");    // callback when done
      });
  });
});
</script>
```

```reference javascript
.hide() / .show() / .toggle() | Hide / show / switch | $("#help").toggle()
.fadeIn / .fadeOut / .fadeToggle | Fade | $(".msg").fadeOut(500)
.slideUp / .slideDown / .slideToggle | Slide | $("#menu").slideToggle()
.animate({..}, ms, done) | Animate number styles | $("#box").animate({ left: "100px" })
.delay(ms) | Wait in the animation queue | $("#a").fadeIn().delay(1000).fadeOut()
.stop() | Stop the current animation | $("#a").stop()
```

:::tip Chaining
Most jQuery methods return the same set, so you can chain them: `$("#msg").text("Saved").fadeIn().delay(1500).fadeOut()`.
:::

```exercise javascript
? Hide #note slowly with a fade
$("#note").___(600);
= fadeOut
```

```quiz
? Why can you write $("#a").fadeIn().delay(500).fadeOut()?
* Each method returns the same jQuery set, so calls can be chained
- Because delay is a global function
- Because fadeIn waits for the user
```

# @lesson jq-traversing
title: Traversing the page
summary: parent, children, find, closest, siblings, next and each.
---
```try html jq
<table border="1" cellpadding="6">
  <tr><td>Tea</td><td>12</td><td><button class="del">Delete</button></td></tr>
  <tr><td>Coffee</td><td>20</td><td><button class="del">Delete</button></td></tr>
  <tr><td>Cake</td><td>35</td><td><button class="del">Delete</button></td></tr>
</table>
<p id="total"></p>
<script>
$(function () {
  function total() {
    let sum = 0;
    $("tr").each(function () {
      sum += Number($(this).children().eq(1).text());
    });
    $("#total").text("Total: " + sum);
  }
  $(".del").on("click", function () {
    const row = $(this).closest("tr");        // nearest parent <tr>
    row.find("td").first().css("color", "crimson");
    row.fadeOut(300, function () { $(this).remove(); total(); });
  });
  $("td:contains('Coffee')").next().css("font-weight", "bold");
  total();
});
</script>
```

```reference javascript
.parent() / .parents() | Direct parent / all ancestors | $(this).parent()
.closest(sel) | Nearest ancestor that matches | $(this).closest(".card")
.children() / .find(sel) | Direct children / any descendants | $("#menu").find("a")
.siblings() / .next() / .prev() | Neighbours | $("li.active").next()
.each(fn) | Run a function for each element | $("li").each(function (i) { })
.filter(sel) / .not(sel) | Keep / drop some elements | $("li").not(".done")
```

```exercise javascript
? Find the card that contains the clicked button
$(this).___(".card")
= closest
```

```quiz
? Which method looks down into descendants for a selector?
* .find()
- .closest()
- .parent()
```

# @lesson jq-ajax
title: AJAX with jQuery
summary: $.ajax, $.getJSON, promises and loading data without reloading the page.
---
**AJAX** means asking the server for data in the background and updating part of the page, without a full reload.

```js
$.getJSON("/api/products", function (products) {
  products.forEach(p => $("#list").append($("<li>").text(p.name)));
});

$.ajax({
  url: "/api/orders",
  method: "POST",
  contentType: "application/json",
  data: JSON.stringify({ product: 7, qty: 2 }),
})
  .done(order => console.log("created", order.id))
  .fail(xhr => console.log("error", xhr.status))
  .always(() => console.log("finished"));
```

The example below cannot reach a real server, so `fakeServer` returns a jQuery promise that behaves like `$.getJSON`:

```try html jq
<button id="load">Load products</button>
<p id="status"></p>
<ul id="list"></ul>
<script>
function fakeServer() {                       // stands in for $.getJSON("/api/products")
  const d = $.Deferred();
  setTimeout(() => d.resolve([{ name: "Tea", price: 12 }, { name: "Coffee", price: 20 }]), 600);
  return d.promise();
}
$(function () {
  $("#load").on("click", function () {
    $("#status").text("Loading…");
    $("#list").empty();
    fakeServer()
      .done(function (products) {
        products.forEach(p => $("<li>").text(p.name + " – " + p.price).appendTo("#list"));
        $("#status").text("Loaded " + products.length + " products");
      })
      .fail(() => $("#status").text("Could not load"));
  });
});
</script>
```

```reference javascript
$.getJSON(url, fn) | GET and parse JSON | $.getJSON("/api/me", show)
$.get / $.post | Short GET / POST | $.post("/api/log", { a: 1 })
$.ajax({ url, method, data }) | Full control | $.ajax({ url: "/x", method: "PUT" })
.done / .fail / .always | Success / error / both | req.done(render)
$("#box").load(url) | Load HTML into an element | $("#side").load("/menu.html")
$.Deferred() | Build your own promise | const d = $.Deferred()
```

:::tip jQuery promises and async/await
jQuery requests are "thenables", so in modern code you can write `const data = await $.getJSON(url);` inside an `async` function.
:::

```exercise javascript
? Handle a successful response of the request req
req.___(render);
= done
```

```quiz
? What is the main idea of AJAX?
* Fetch data in the background and update part of the page
- Reload the whole page faster
- Store data in the browser forever
```

# @lesson jq-project
title: Project: a small to-do list
summary: Selectors, events, DOM changes and classes together.
---
```try html jq
<input id="task" placeholder="New task">
<button id="add">Add</button>
<button id="clear">Clear done</button>
<ul id="tasks"></ul>
<p id="left"></p>
<script>
$(function () {
  function update() {
    const left = $("#tasks li").not(".done").length;
    $("#left").text(left + " task(s) left");
  }
  function add() {
    const text = $("#task").val().trim();
    if (!text) return;
    $("<li>").text(text).appendTo("#tasks");
    $("#task").val("").focus();
    update();
  }
  $("#add").on("click", add);
  $("#task").on("keydown", e => { if (e.key === "Enter") add(); });

  // delegated event: works for items added later
  $("#tasks").on("click", "li", function () {
    $(this).toggleClass("done");
    update();
  });
  $("#clear").on("click", function () {
    $("#tasks li.done").slideUp(200, function () { $(this).remove(); update(); });
  });

  ["Read a lesson", "Do the quiz"].forEach(t => $("<li>").text(t).appendTo("#tasks"));
  update();
});
</script>
```

:::tip Delegated events
`$("#tasks").on("click", "li", fn)` puts one handler on the list that also catches clicks on `<li>` elements created later. A plain `$("li").on("click", fn)` only covers items that already exist.
:::

```quiz
? Why does the project use $("#tasks").on("click", "li", ...)?
* So that items added later also respond to clicks
- Because li elements cannot have click handlers
- To make the list sortable
```

# @lesson jq-reference
title: jQuery quick reference
summary: The most used methods on one page, and when to use plain JavaScript instead.
---
```reference javascript
$(function () { }) | Run when the page is ready | $(init)
$("css selector") | Find elements | $("#form input")
.on(event, [child], fn) | Events (and delegation) | $("ul").on("click", "li", fn)
.text / .html / .val | Content and values | $("#q").val()
.append / .remove / $("<tag>") | Change the page | $("<li>").text(x).appendTo("ul")
.addClass / .toggleClass / .css | Styles | $("li").addClass("done")
.attr / .prop | Attributes / live state | $("#ok").prop("checked")
.show / .fadeIn / .slideToggle / .animate | Effects | $("#msg").fadeOut()
.closest / .find / .each | Traversing | $(this).closest("tr")
$.getJSON / $.ajax | Server requests | $.getJSON(url).done(show)
```

## jQuery and plain JavaScript

| jQuery | Plain JavaScript |
|---|---|
| `$("#id")` | `document.querySelector("#id")` |
| `$(".a").addClass("b")` | `document.querySelectorAll(".a").forEach(e => e.classList.add("b"))` |
| `$(el).on("click", fn)` | `el.addEventListener("click", fn)` |
| `$(el).text("x")` | `el.textContent = "x"` |
| `$.getJSON(url)` | `fetch(url).then(r => r.json())` |

:::tip Where to go next
For new projects, plain JavaScript or a framework (React, Vue) is usually the better choice. jQuery knowledge stays useful for maintaining existing sites, WordPress themes and many admin pages.
:::

```quiz
? What is the plain JavaScript equivalent of $(el).on("click", fn)?
* el.addEventListener("click", fn)
- el.click = fn()
- document.on("click", fn)
```
