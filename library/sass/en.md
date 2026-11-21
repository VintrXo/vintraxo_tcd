# @lesson sass-intro
title: Sass introduction
summary: What Sass adds to CSS, SCSS syntax, and how it is compiled.
---
**Sass** is a CSS preprocessor: you write styles with variables, nesting, mixins, functions and loops, and the Sass compiler turns them into plain CSS that browsers understand. Bootstrap and many design systems are written in Sass.

There are two syntaxes. This course uses **SCSS**, which looks like CSS with extras (every valid CSS file is valid SCSS). The older indented syntax drops braces and semicolons.

```try html scss
<style type="text/scss">
$brand: #4338ca;
$radius: 10px;

.card {
  padding: 16px;
  border: 2px solid $brand;
  border-radius: $radius;

  h3 { color: $brand; margin: 0 0 8px; }
}
</style>

<div class="card">
  <h3>Hello Sass</h3>
  <p>The variables and nesting above became normal CSS.</p>
</div>
```

The box under the example shows the **compiled CSS** that the browser really uses.

:::info Compiling on your computer
Install with `npm install -g sass`, then `sass styles.scss styles.css`, or `sass --watch scss:css` to recompile on every save. Frameworks such as Vite, Angular and Next.js compile `.scss` files for you.
:::

```quiz
? What does the Sass compiler produce?
* Plain CSS that browsers understand
- JavaScript code
- Images

? Every valid CSS file is also valid SCSS.
= true
```

# @lesson sass-variables
title: Variables
summary: $variables, scope, !default, and Sass variables versus CSS custom properties.
---
```try html scss
<style type="text/scss">
$brand: #0e7490;
$space: 8px;
$font-stack: system-ui, "Segoe UI", sans-serif;

body { font-family: $font-stack; }

.alert {
  $alert-bg: #e0f2fe;                  // only visible inside .alert
  padding: $space * 2;
  margin-block-end: $space;
  background: $alert-bg;
  border-inline-start: 4px solid $brand;
}

:root {
  --brand: #{$brand};                  // hand a Sass value to a CSS variable
}
.badge { color: var(--brand); font-weight: bold; }
</style>

<div class="alert">Saved. <span class="badge">new</span></div>
<div class="alert">Two alerts, one set of variables.</div>
```

```reference css
$name: value; | Declare a variable | $brand: #4338ca;
$a * 2 / $a + 4px | Math with values and units | padding: $space * 2;
#{$var} | Interpolation into selectors, properties or CSS variables | --brand: #{$brand};
!default | Use this value unless one was set before | $brand: blue !default;
var(--name) | CSS custom property (runs in the browser) | color: var(--brand);
```

:::tip Sass variables or CSS variables?
Sass variables exist only while compiling: great for design tokens and calculations. CSS custom properties live in the browser and can change at runtime, for example for a dark mode. Many projects define tokens in Sass and output them as CSS variables.
:::

```exercise css
? Declare a Sass variable named gap with the value 12px
___gap: 12px;
= $
```

```quiz
? When are Sass variables evaluated?
* When the Sass is compiled to CSS
- Every time the page is scrolled
- Only in dark mode
```

# @lesson sass-nesting
title: Nesting and the parent selector
summary: Nested rules, &, pseudo-classes, BEM names and nested media queries.
---
```try html scss
<style type="text/scss">
$brand: #4338ca;

.nav {
  display: flex;
  gap: 4px;

  a {
    padding: 6px 12px;
    border-radius: 999px;
    color: $brand;
    text-decoration: none;

    &:hover { background: #eef2ff; }          // & = the parent selector: .nav a:hover
    &.active { background: $brand; color: #fff; }
  }

  &__title {                                  // builds .nav__title (BEM naming)
    font-weight: bold;
    margin-inline-end: 12px;
  }

  @media (max-width: 500px) {                 // media query kept next to the rule
    flex-direction: column;
  }
}
</style>

<nav class="nav">
  <span class="nav__title">Menu</span>
  <a href="#" class="active">Home</a>
  <a href="#">Courses</a>
  <a href="#">Profile</a>
</nav>
```

```reference css
.a { .b { } } | Nested selector | .card { h3 { } } -> .card h3
& | The parent selector | &:hover, &.active, &__title
&-suffix | Build a class name | .btn { &-primary { } } -> .btn-primary
@media inside a rule | Media query next to its rule | .nav { @media (...) { } }
```

:::warning Do not nest too deep
Deep nesting produces long, very specific selectors that are hard to override. Keep it to about three levels.
:::

```exercise css
? Style the hover state of .btn from inside it
.btn { ___:hover { opacity: .8; } }
= &
```

```quiz
? Inside .card { &.dark { } }, what selector is produced?
* .card.dark
- .card .dark
- .dark .card
```

# @lesson sass-mixins
title: Mixins
summary: Reusable groups of declarations with @mixin, @include, arguments and @content.
---
```try html scss
<style type="text/scss">
@mixin center {
  display: flex;
  align-items: center;
  justify-content: center;
}

@mixin button($bg, $fg: #fff, $radius: 8px) {   // arguments with defaults
  background: $bg;
  color: $fg;
  border: 0;
  border-radius: $radius;
  padding: 8px 16px;
  cursor: pointer;
}

@mixin on-small-screens {
  @media (max-width: 600px) { @content; }      // @content = the block passed in
}

.hero {
  @include center;
  height: 90px;
  background: #f1f5f9;
  gap: 8px;
  @include on-small-screens { flex-direction: column; height: auto; }
}
.btn-save { @include button(#15803d); }
.btn-delete { @include button(#b91c1c, $radius: 999px); }
</style>

<div class="hero">
  <button class="btn-save">Save</button>
  <button class="btn-delete">Delete</button>
</div>
```

```reference css
@mixin name { } | Define a reusable block | @mixin card { padding: 16px; }
@include name; | Use it | .box { @include card; }
@mixin name($a, $b: default) | Arguments and defaults | @mixin pad($x: 8px)
name($b: value) | Named argument | @include button($radius: 4px)
@content | Insert the caller's block | @mixin dark { .dark & { @content; } }
```

```exercise css
? Use the mixin center inside .box
.box { ___ center; }
= @include
```

```quiz
? What does @content do inside a mixin?
* Inserts the block of styles written where the mixin is included
- Prints the page content
- Imports another file
```

# @lesson sass-extend
title: Placeholders and @extend
summary: Share styles between selectors, and when to prefer mixins.
---
```try html scss
<style type="text/scss">
%message {                              // a placeholder: never output on its own
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid transparent;
}

.message-ok   { @extend %message; background: #dcfce7; border-color: #86efac; }
.message-warn { @extend %message; background: #fef3c7; border-color: #fcd34d; }
.message-err  { @extend %message; background: #fee2e2; border-color: #fca5a5; }
</style>

<div class="message-ok">Saved successfully.</div>
<div class="message-warn">Your session expires in 5 minutes.</div>
<div class="message-err">The payment failed.</div>
```

Look at the compiled CSS: the three classes are **grouped into one selector** for the shared rules instead of repeating them.

```reference css
%name { } | Placeholder selector (not output alone) | %clearfix { }
@extend %name; | Share the placeholder's rules | .note { @extend %box; }
@extend .class; | Share another class's rules (use with care) | .error { @extend .alert; }
```

:::tip Mixin or extend?
`@extend` groups selectors and keeps the CSS small, but it can create surprising selector combinations across files. Mixins copy the declarations, which is more predictable and can take arguments. When in doubt, use a mixin.
:::

```exercise css
? Share the rules of the placeholder %box
.note { ___ %box; }
= @extend
```

```quiz
? Why is a placeholder (%name) useful?
* Its rules are shared by the selectors that extend it, and it is not output on its own
- It loads faster than a class
- It works only in media queries
```

# @lesson sass-modules
title: Modules, partials and built-in functions
summary: @use and @forward, partial files, and the sass:color, sass:math and sass:string modules.
---
Real projects split styles into files. A file whose name starts with `_` is a **partial**: it is only loaded by other files, never compiled alone.

```text
styles/
  _tokens.scss       $brand: #4338ca; $radius: 10px;
  _buttons.scss      @use "tokens"; .btn { background: tokens.$brand; }
  main.scss          @use "tokens"; @use "buttons";
```

`@use "tokens"` loads `_tokens.scss` once and gives its members a **namespace** (`tokens.$brand`). This replaces the old `@import`, which is deprecated.

Sass also ships built-in modules. The example uses them (it can only use built-in modules, because the playground has no files):

```try html scss
<style type="text/scss">
@use "sass:color";
@use "sass:math";
@use "sass:string";

$brand: #4338ca;

.swatch { display: inline-block; width: 70px; height: 50px; margin: 4px; border-radius: 8px; color: #fff; font: 12px sans-serif; padding: 4px; }
.base   { background: $brand; }
.light  { background: color.scale($brand, $lightness: 40%); }
.dark   { background: color.scale($brand, $lightness: -30%); }
.mix    { background: color.mix($brand, #0e7490, 50%); }
.faded  { background: color.change($brand, $alpha: 0.5); }

.col { width: math.percentage(math.div(1, 3)); }       // 33.333%
.title::after { content: string.to-upper-case("sass"); }
</style>

<div class="swatch base">base</div><div class="swatch light">lighter</div><div class="swatch dark">darker</div><div class="swatch mix">mix</div><div class="swatch faded">50%</div>
<p class="title">Built-in modules: </p>
```

```reference css
@use "file"; | Load a module once, with a namespace | @use "tokens"; tokens.$brand
@use "file" as t; | Choose the namespace | @use "tokens" as t;
@forward "file"; | Re-export a module's members | @forward "buttons";
_name.scss | Partial file (not compiled alone) | _variables.scss
color.scale / color.adjust / color.mix | Color tools (replace darken, lighten) | color.scale($c, $lightness: -20%)
math.div / math.percentage / math.round | Math (division is math.div) | math.div(100%, 3)
```

:::warning Old functions and @import
`darken()`, `lighten()`, the `/` division operator and `@import` still work but are deprecated. Use `color.scale` or `color.adjust`, `math.div`, and `@use` in new code.
:::

```exercise css
? Load the built-in color module
@use "sass:___";
= color
```

```quiz
? Which rule loads a Sass module with a namespace and replaces @import?
* @use
- @include
- @extend
```

# @lesson sass-functions
title: Your own functions
summary: @function, @return, and turning pixel sizes into rem.
---
```try html scss
<style type="text/scss">
@use "sass:math";

$base-font: 16px;

@function rem($px) {
  @return math.div($px, $base-font) * 1rem;
}

@function spacing($step) {
  @if $step < 0 { @error "spacing() needs a positive step, got #{$step}"; }
  @return $step * 4px;
}

h2 { font-size: rem(28px); margin: 0 0 spacing(2); }
p  { font-size: rem(15px); line-height: 1.6; padding: spacing(3); background: #f8fafc; }
</style>

<h2>Sizes in rem</h2>
<p>28px became 1.75rem and 15px became 0.9375rem, so the text grows with the user's font settings.</p>
```

```reference css
@function name($a) { @return ...; } | Define a function | @function double($x) { @return $x * 2; }
@return | The function's result | @return math.div($px, 16px) * 1rem;
@if / @else | Conditions | @if $dark { ... } @else { ... }
@error / @warn | Stop with an error / print a warning | @error "bad value #{$v}";
```

:::tip Mixins write rules, functions return values
Use a function when you need a value inside a property (`font-size: rem(18px)`). Use a mixin when you need whole declarations or rules.
:::

```exercise css
? Give back the result from a Sass function
@function half($x) { ___ math.div($x, 2); }
= @return
```

```quiz
? What is the difference between a function and a mixin?
* A function returns a value; a mixin outputs declarations
- They are the same
- A mixin returns a value; a function outputs rules
```

# @lesson sass-control
title: Maps, loops and conditions
summary: Maps, @each, @for, @if, and generating utility classes.
---
```try html scss
<style type="text/scss">
@use "sass:map";
@use "sass:color";

$colors: (
  "primary": #4338ca,
  "success": #15803d,
  "warning": #b45309,
  "danger": #b91c1c,
);

@each $name, $color in $colors {                // one class per map entry
  .btn-#{$name} {
    background: $color;
    color: #fff;
    border: 0;
    padding: 6px 12px;
    border-radius: 6px;
    &:hover { background: color.scale($color, $lightness: -15%); }
  }
}

@for $i from 1 through 4 {                      // spacing utilities .mt-1 ... .mt-4
  .mt-#{$i} { margin-top: $i * 4px; }
}

$theme: "dark";
.panel {
  padding: 10px;
  @if $theme == "dark" { background: #1e293b; color: #e2e8f0; }
  @else { background: #f8fafc; color: #0f172a; }
}

.note { color: map.get($colors, "warning"); }
</style>

<button class="btn-primary">Primary</button>
<button class="btn-success">Success</button>
<button class="btn-warning">Warning</button>
<button class="btn-danger">Danger</button>
<div class="panel mt-3">A dark panel, 12px from the buttons.</div>
<p class="note mt-2">This color came from the map.</p>
```

```reference css
$map: (key: value, ...) | A map | $sizes: ("sm": 4px, "lg": 16px);
map.get($map, key) | Read a value | map.get($sizes, "lg")
@each $k, $v in $map | Loop over a map | @each $name, $c in $colors { }
@each $item in $list | Loop over a list | @each $side in top, bottom { }
@for $i from 1 through n | Counted loop | @for $i from 1 through 5 { }
@if / @else if / @else | Conditions | @if $theme == "dark" { }
```

:::tip This is how frameworks work
Bootstrap builds hundreds of classes such as `.btn-primary` and `.mt-3` exactly like this: a map of tokens and a few loops.
:::

```exercise css
? Loop over every name and color in $colors
___ $name, $color in $colors { }
= @each
```

```quiz
? What does @for $i from 1 through 3 produce?
* Three passes with $i = 1, 2 and 3
- Two passes
- One pass with a list
```

# @lesson sass-project
title: Project: a small theme system
summary: Tokens, a button mixin, generated variants and a dark theme with CSS variables.
---
```try html scss
<style type="text/scss">
@use "sass:map";
@use "sass:color";

// 1. design tokens
$tokens: (
  "brand": #4338ca,
  "accent": #0e7490,
  "danger": #b91c1c,
);
$radius: 10px;

// 2. light and dark values as CSS variables, so the theme can change in the browser
:root {
  --bg: #ffffff; --text: #0f172a; --card: #f1f5f9;
  @each $name, $value in $tokens { --#{$name}: #{$value}; }
}
.dark {
  --bg: #0f172a; --text: #e2e8f0; --card: #1e293b;
}

// 3. components built from the tokens
@mixin button-variant($color) {
  background: $color;
  &:hover { background: color.scale($color, $lightness: -15%); }
}

.theme { background: var(--bg); color: var(--text); padding: 14px; border-radius: $radius; }
.card {
  background: var(--card);
  border-radius: $radius;
  padding: 12px;
  margin-bottom: 10px;
  h4 { margin: 0 0 6px; color: var(--brand); }
}
.btn {
  border: 0; color: #fff; padding: 7px 14px; border-radius: $radius; cursor: pointer;
  @each $name, $value in $tokens {
    &-#{$name} { @include button-variant($value); }
  }
}
</style>

<div class="theme" id="t">
  <div class="card"><h4>Order #1024</h4>3 items · 450 EGP</div>
  <button class="btn btn-brand">Pay</button>
  <button class="btn btn-accent">Track</button>
  <button class="btn btn-danger">Cancel</button>
  <button onclick="document.getElementById('t').classList.toggle('dark')">Toggle dark</button>
</div>
```

:::tip Make it yours
Add a "success" token and watch a new `.btn-success` appear in the compiled CSS without writing it, or change `$radius` once to restyle every component.
:::

```quiz
? Why does the project put colors in CSS variables as well as Sass?
* So the theme can switch in the browser without recompiling
- Because Sass cannot store colors
- To make the file shorter
```

# @lesson sass-reference
title: Sass quick reference
summary: The most used Sass features on one page.
---
```reference css
$var: value; | Variable | $brand: #4338ca;
#{$var} | Interpolation | .icon-#{$name} { }
.a { .b { } } / & | Nesting / parent selector | &:hover, &--active
@mixin / @include / @content | Reusable blocks | @include button($bg)
%placeholder / @extend | Shared rules | @extend %card;
@use "file" / @forward | Modules | @use "tokens" as t;
@function / @return | Your own functions | @function rem($px) { }
@if / @each / @for | Logic and loops | @each $k, $v in $map { }
map.get / color.scale / math.div | Built-in modules | color.scale($c, $lightness: 20%)
_partial.scss | Files loaded by others | _buttons.scss
sass input.scss output.css | Compile on the command line | sass --watch scss:css
```

:::tip Where to go next
Restyle a page from the HTML or Bootstrap courses with your own Sass tokens and mixins, then read how Bootstrap's `_variables.scss` lets you customise the whole framework with a few variables.
:::

```quiz
? Which built-in function should replace darken() in new code?
* color.scale or color.adjust
- math.div
- map.get
```
