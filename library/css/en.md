# @lesson css-intro
title: CSS introduction
summary: What CSS is and why styling is kept apart from content.
---
**CSS** stands for *Cascading Style Sheets*. HTML says **what** is on the page; CSS says **how** it looks: colors, fonts, spacing and the arrangement of elements.

## A quick example

Change a color or a size, then press **Run**:

```try html
<style>
  body { font-family: sans-serif; background: #f8fafc; }
  h1 { color: #4338ca; text-align: center; }
  p { color: #334155; font-size: 18px; }
</style>
<h1>Hello CSS</h1>
<p>The same HTML, but a completely different look.</p>
```

## Why CSS?

- **One file for every page**: change the color of all headings on the site in one place.
- **Cleaner code**: HTML holds only content, and styling lives in its own place.
- **Responsive design**: the same page looks good on a computer and a phone.

:::info Where does "cascading" come from?
When several rules apply to the same element, they all apply in turn, and the most specific or the last one wins when they conflict.
:::

```quiz
? What is CSS for?
- Defining the content of the page
* Defining how the page looks
- Storing the site's data

? One CSS file can style many pages.
= true
```

# @lesson css-syntax
title: CSS syntax
summary: Selector, property and value.
---
A CSS rule is a **selector** that picks elements, followed by **declarations** in curly braces:

```css
h1 {
  color: crimson;
  font-size: 32px;
}
```

- `h1` is the selector: it picks every level-one heading.
- `color` and `font-size` are properties; `crimson` and `32px` are their values.
- Every declaration ends with a semicolon `;`.

```try html
<style>
  p { color: green; text-align: center; }
</style>
<p>All paragraphs are green and centered.</p>
<p>This one too.</p>
```

## Comments in CSS

A comment is written between `/*` and `*/`:

```css
/* color of the main headings */
h1 { color: navy; }
```

```exercise css
? Complete the rule to make paragraphs red
p {
  ___: red;
}
= color
```

```quiz
? In the rule p { color: red; } what is the selector?
* p
- color
- red

? How is a comment written in CSS?
- <!-- comment -->
* /* comment */
- // comment
```

# @lesson css-howto
title: How to add CSS
summary: Inside the tag, in the page head, or in an external file.
---
There are three ways to add CSS:

## 1. An external file (best)

Put the rules in a file such as `style.css` and link it in `<head>`:

```html
<head>
  <link rel="stylesheet" href="style.css">
</head>
```

## 2. Inside the page

Put the rules in a `<style>` element inside `<head>`:

```try html
<style>
  h2 { color: darkorange; }
</style>
<h2>Internal styling</h2>
```

## 3. Inside the tag

Use the `style` attribute on one element:

```try html
<p style="color: purple; font-weight: bold;">Styling for this paragraph only.</p>
```

:::tip Which one should I use?
An external file for the whole site, `<style>` for one special page, and the `style` attribute only in rare cases, because it mixes styling with content.
:::

## Priority

When rules conflict, inline styling wins, then the more specific rule, then the one that comes last.

```try html
<style>
  p { color: blue; }
</style>
<p>Blue from the rule.</p>
<p style="color: red;">Red: inline styling wins.</p>
```

```quiz
? What is the best way to style a whole site?
- A style attribute on every element
* An external CSS file linked with <link>
- A <style> element in every page

? Inline styling wins over a rule in an external file.
= true
```

# @lesson css-selectors
title: Selectors
summary: Element, class, id, grouping and nesting.
---
A selector picks the elements a rule applies to:

```reference css
p | Every p element | p { color: gray; }
.card | Every element with class="card" | .card { padding: 8px; }
#logo | The element with id="logo" | #logo { width: 120px; }
* | Every element | * { box-sizing: border-box; }
h1, h2 | Several selectors at once | h1, h2 { color: navy; }
nav a | Every a inside nav | nav a { text-decoration: none; }
a:hover | While the mouse is over it | a:hover { color: red; }
li:first-child | The first item | li:first-child { font-weight: bold; }
```

```try html
<style>
  .note { background: #fef9c3; padding: 6px; }
  #main-title { color: #4338ca; }
  nav a { margin: 0 6px; }
  a:hover { color: crimson; }
</style>
<h1 id="main-title">A heading with an id</h1>
<p class="note">A paragraph with class note</p>
<p>A normal paragraph</p>
<nav><a href="#">Home</a><a href="#">About</a></nav>
```

:::info Class or id?
An `id` is unique: one element per page. A `class` can be repeated on many elements, and it is what you will use most for styling.
:::

```exercise css
? Complete the selector to pick every element with class="box"
___box {
  border: 1px solid gray;
}
= .
```

```quiz
? Which selector picks the element with id="logo"?
- .logo
* #logo
- logo

? Several elements can share the same class.
= true
```

# @lesson css-colors
title: Colors
summary: Color names, hex values, rgb, hsl and transparency.
---
A color can be written in several ways:

```reference css
color name | More than 140 names | color: tomato;
#RRGGBB | Hexadecimal value | color: #4338ca;
rgb() | Red, green, blue 0–255 | color: rgb(67, 56, 202);
rgba() / rgb(… / a) | With transparency 0–1 | background: rgba(0, 0, 0, 0.5);
hsl() | Hue, saturation, lightness | color: hsl(243, 57%, 50%);
```

```try html
<style>
  .a { background: tomato; }
  .b { background: #0ea5e9; }
  .c { background: rgb(34, 197, 94); }
  .d { background: rgba(67, 56, 202, 0.4); }
  div { color: white; padding: 8px; margin: 4px 0; }
</style>
<div class="a">tomato</div>
<div class="b">#0ea5e9</div>
<div class="c">rgb(34, 197, 94)</div>
<div class="d">rgba with transparency</div>
```

- `color` is the text color.
- `background-color` is the background color.
- `border-color` is the border color.

```exercise css
? Make the element's background yellow
.alert {
  ___: yellow;
}
= background-color | background
```

```quiz
? Which value is a partly transparent color?
- rgb(0, 0, 0)
* rgba(0, 0, 0, 0.5)
- #000000

? The color property changes the background color.
= false
> color is for text; background-color is for the background.
```

# @lesson css-backgrounds
title: Backgrounds
summary: Background color, image, repeat, position, size and gradients.
---
```reference css
background-color | Background color | background-color: #f1f5f9;
background-image | An image or gradient | background-image: url("bg.png");
background-repeat | Whether the image repeats | background-repeat: no-repeat;
background-position | Where the image sits | background-position: center;
background-size | Size of the image | background-size: cover;
background | Shorthand for all of the above | background: #000 url(a.png) no-repeat center / cover;
```

```try html
<style>
  .hero {
    height: 160px;
    color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    background: url("https://picsum.photos/600/300") center / cover no-repeat;
  }
  .grad {
    margin-top: 8px; padding: 20px; color: white;
    background: linear-gradient(to right, #4338ca, #06b6d4);
  }
</style>
<div class="hero">An image background</div>
<div class="grad">A gradient background</div>
```

:::tip cover or contain?
`cover` fills the whole area and may crop the edges of the image. `contain` shows the whole image and may leave empty space.
:::

```quiz
? Which value makes a background image fill the element?
* background-size: cover
- background-repeat: repeat
- background-position: top

? linear-gradient creates a color gradient used as a background.
= true
```

# @lesson css-text
title: Text
summary: Alignment, decoration, transformation, and line and letter spacing.
---
```reference css
text-align | Alignment | text-align: center;
text-decoration | Line under/over/through text | text-decoration: underline;
text-transform | Upper/lower case | text-transform: uppercase;
line-height | Height of a line | line-height: 1.8;
letter-spacing | Space between letters | letter-spacing: 2px;
word-spacing | Space between words | word-spacing: 6px;
text-shadow | Text shadow | text-shadow: 1px 1px 2px gray;
direction | Text direction | direction: rtl;
```

```try html
<style>
  h2 { text-align: center; text-shadow: 2px 2px 4px #94a3b8; }
  .up { text-transform: uppercase; letter-spacing: 3px; }
  .lh { line-height: 2; }
  a { text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
<h2>A centered heading with a shadow</h2>
<p class="up">hello css</p>
<p class="lh">A paragraph with a tall line height reads more comfortably, especially long text that runs over several lines.</p>
<a href="#">A link with no underline until you hover it</a>
```

:::info Alignment and direction
In a `dir="rtl"` page text starts on the right. Use `text-align: start` so alignment works in both directions.
:::

```exercise css
? Remove the underline from links
a {
  text-decoration: ___;
}
= none
```

```quiz
? Which property changes the height of a line?
- letter-spacing
* line-height
- text-align

? text-transform: uppercase affects Arabic letters.
= false
> Arabic letters have no upper and lower case.
```

# @lesson css-fonts
title: Fonts
summary: Font family, size, weight and web fonts.
---
```reference css
font-family | Font with fallbacks | font-family: "Cairo", Tahoma, sans-serif;
font-size | Size | font-size: 18px;
font-weight | Weight | font-weight: bold;
font-style | Italic | font-style: italic;
font | Shorthand | font: italic bold 16px/1.6 sans-serif;
```

```try html
<style>
  .serif { font-family: Georgia, serif; }
  .mono { font-family: "Courier New", monospace; }
  .big { font-size: 2rem; font-weight: 700; }
  .light { font-weight: 300; font-style: italic; }
</style>
<p class="serif">A serif font</p>
<p class="mono">monospace: every letter has the same width</p>
<p class="big">Big bold text</p>
<p class="light">Light italic text</p>
```

## Size units

- `px` a fixed pixel.
- `em` relative to the parent element's font size.
- `rem` relative to the page (root) font size; usually the best choice.
- `%` a percentage.

:::tip Always list fallbacks
If the first font is missing on the visitor's device, the browser uses the next one. Always end the list with a generic family such as `sans-serif`.
:::

```quiz
? Which unit is relative to the root font size?
- px
- em
* rem

? font-weight controls how thick the text is.
= true
```

# @lesson css-box-model
title: The box model
summary: Content, padding, border, margin, and box-sizing.
---
Every element on the page is a **box** of four layers, from inside out:

1. **Content**: the text or image.
2. **Padding**: space between the content and the border.
3. **Border**: a line around the padding.
4. **Margin**: space outside the border that separates the element from others.

```try html
<style>
  .box {
    width: 200px;
    padding: 20px;
    border: 5px solid #4338ca;
    margin: 30px;
    background: #e0e7ff;
  }
</style>
<div class="box">Box content</div>
```

## The real width

By default the total width is `width` + padding + border. In the example: 200 + 40 + 10 = 250 pixels.

With `box-sizing: border-box`, `width` includes the padding and border, which is much easier:

```try html
<style>
  div { width: 200px; padding: 20px; border: 5px solid teal; margin-bottom: 8px; }
  .bb { box-sizing: border-box; }
</style>
<div>Without border-box (250 wide)</div>
<div class="bb">With border-box (200 wide)</div>
```

:::tip A common rule
Many projects start with `* { box-sizing: border-box; }` to apply it to every element.
:::

```quiz
? Which layer sits between the content and the border?
* padding
- margin
- outline

? With box-sizing: border-box, width includes padding and border.
= true
```

# @lesson css-borders
title: Borders
summary: Border style, width and color, and rounded corners.
---
```reference css
border-style | Line style | border-style: dashed;
border-width | Thickness | border-width: 3px;
border-color | Color | border-color: gray;
border | Shorthand | border: 2px solid #4338ca;
border-top / border-inline-start | One side | border-bottom: 1px solid #ddd;
border-radius | Rounded corners | border-radius: 12px;
```

```try html
<style>
  div { padding: 10px; margin: 8px 0; }
  .solid { border: 2px solid #0f766e; }
  .dashed { border: 2px dashed #b45309; }
  .round { border: 2px solid #4338ca; border-radius: 16px; }
  .side { border-inline-start: 6px solid crimson; background: #fff1f2; }
  .circle { width: 80px; height: 80px; border-radius: 50%; background: #06b6d4; }
</style>
<div class="solid">Solid border</div>
<div class="dashed">Dashed border</div>
<div class="round">Rounded corners</div>
<div class="side">A line at the start side only</div>
<div class="circle"></div>
```

```exercise css
? Give the card rounded corners
.card {
  ___: 10px;
}
= border-radius
```

```quiz
? Which value turns a square into a circle?
- border-radius: 10px
* border-radius: 50%
- border-style: circle

? border-inline-start puts the border at the start side, following the text direction.
= true
```

# @lesson css-margin-padding
title: Margin and padding
summary: Values for each side, and centering with auto.
---
`margin` and `padding` take one to four values:

```reference css
One value | All sides | margin: 10px;
Two values | Top/bottom, then right/left | padding: 10px 20px;
Four values | Top, right, bottom, left | margin: 5px 10px 15px 20px;
One side | A given side | margin-top: 12px;
auto | Shares the remaining space | margin: 0 auto;
```

```try html
<style>
  .center { width: 220px; margin: 20px auto; padding: 12px 24px; background: #dcfce7; }
  .tight { padding: 2px; background: #fee2e2; }
  .roomy { padding: 24px; background: #e0f2fe; }
</style>
<div class="center">Centered with margin: auto</div>
<p class="tight">Small padding</p>
<p class="roomy">Large padding</p>
```

:::info The difference, simply
Padding is **inside** the element and takes its background color; margin is **outside** and stays transparent.
:::

```exercise css
? Center the element horizontally
.page {
  width: 600px;
  margin: 0 ___;
}
= auto
```

```quiz
? What does padding: 10px 20px mean?
* 10 top and bottom, 20 right and left
- 10 right and left, 20 top and bottom
- 10 on every side

? The margin takes the element's background color.
= false
```

# @lesson css-display
title: The display property
summary: block, inline, inline-block and none.
---
`display` sets how an element is shown:

```reference css
block | A full line of its own | display: block;
inline | Inside the line, no width or height | display: inline;
inline-block | Inside the line, with width and height | display: inline-block;
none | Hidden, takes no space | display: none;
flex | A Flexbox container | display: flex;
grid | A Grid container | display: grid;
```

```try html
<style>
  .chip { display: inline-block; padding: 4px 12px; margin: 2px; border-radius: 999px; background: #e0e7ff; }
  .menu a { display: block; padding: 6px; border-bottom: 1px solid #e2e8f0; }
  .hidden { display: none; }
</style>
<span class="chip">HTML</span><span class="chip">CSS</span><span class="chip">JS</span>
<div class="menu"><a href="#">A link that takes a full line</a><a href="#">Another link</a></div>
<p class="hidden">You will not see me</p>
<p>The hidden paragraph above takes no space at all.</p>
```

:::tip display: none or visibility: hidden?
`display: none` removes the element from the layout. `visibility: hidden` hides it but leaves its space empty.
:::

```quiz
? Which value allows width and height while staying inside the line?
- inline
* inline-block
- none

? display: none keeps the element's space empty.
= false
```

# @lesson css-position
title: Positioning
summary: static, relative, absolute, fixed and sticky.
---
```reference css
static | The default | position: static;
relative | Moves from its normal place | position: relative; top: 10px;
absolute | Relative to the nearest positioned parent | position: absolute; top: 0; right: 0;
fixed | Fixed to the window | position: fixed; bottom: 16px;
sticky | Sticks while scrolling | position: sticky; top: 0;
z-index | What is on top | z-index: 10;
```

```try html
<style>
  .card { position: relative; width: 240px; height: 120px; background: #f1f5f9; border-radius: 8px; }
  .badge { position: absolute; top: 8px; right: 8px; background: crimson; color: white; padding: 2px 8px; border-radius: 999px; }
  .bar { position: sticky; top: 0; background: #4338ca; color: white; padding: 6px; }
</style>
<div class="bar">A sticky bar: scroll inside the result</div>
<div class="card">A card <span class="badge">new</span></div>
<p style="height: 400px;">Long content to scroll…</p>
```

:::info absolute inside relative
Give the parent `position: relative` so an `absolute` child is placed relative to it, not to the whole page.
:::

```quiz
? Which value keeps an element in the window even while scrolling?
- relative
* fixed
- static

? An absolute element is placed relative to its nearest parent whose position is not static.
= true
```

# @lesson css-flexbox
title: Flexbox
summary: Arranging items in a row or a column, with alignment and distribution.
---
Flexbox arranges items inside a container in **one direction**: a row or a column. Turn it on with `display: flex` on the container:

```try html
<style>
  .row { display: flex; gap: 8px; justify-content: space-between; align-items: center;
         background: #f1f5f9; padding: 8px; }
  .row div { background: #4338ca; color: white; padding: 12px; border-radius: 6px; }
</style>
<div class="row">
  <div>1</div><div>2</div><div>3</div>
</div>
```

```reference css
flex-direction | Direction | flex-direction: column;
justify-content | Distribution on the main axis | justify-content: center;
align-items | Alignment on the cross axis | align-items: center;
flex-wrap | Wrap to a new line | flex-wrap: wrap;
gap | Space between items | gap: 12px;
flex | How much an item grows | flex: 1;
```

## Perfect centering

```try html
<style>
  .center { display: flex; justify-content: center; align-items: center; height: 150px; background: #ecfeff; }
</style>
<div class="center"><strong>Centered horizontally and vertically</strong></div>
```

## Flexible columns

```try html
<style>
  .cols { display: flex; gap: 8px; }
  .side { flex: 1; background: #fef3c7; padding: 8px; }
  .main { flex: 3; background: #dcfce7; padding: 8px; }
</style>
<div class="cols"><div class="side">Side (1)</div><div class="main">Main (3)</div></div>
```

```exercise css
? Center the items horizontally in the container
.box {
  display: flex;
  justify-content: ___;
}
= center
```

```quiz
? Which property distributes items on the main axis?
* justify-content
- align-items
- flex-wrap

? Flexbox is suited to arranging items in one direction.
= true
```

# @lesson css-grid
title: Grid
summary: A grid of rows and columns, the fr unit, and spanning several cells.
---
Grid arranges items in **two dimensions**: rows and columns together.

```try html
<style>
  .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
  .grid div { background: #e0e7ff; padding: 16px; text-align: center; border-radius: 6px; }
  .wide { grid-column: span 2; background: #c7d2fe !important; }
</style>
<div class="grid">
  <div class="wide">Spans two columns</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

- `fr` is a fraction of the free space: `1fr 2fr` gives the second twice the first.
- `repeat(3, 1fr)` is short for three equal columns.
- `grid-column: span 2` makes an item span two columns.

## A grid that adapts by itself

```try html
<style>
  .auto { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; }
  .auto div { background: #dcfce7; padding: 20px; text-align: center; }
</style>
<div class="auto"><div>A</div><div>B</div><div>C</div><div>D</div><div>E</div><div>F</div></div>
```

:::tip Flexbox or Grid?
Flexbox for one row or column (a set of buttons, a bar). Grid for a layout of rows and columns (a page, a photo gallery).
:::

```exercise css
? Make three equal columns
.gallery {
  display: grid;
  grid-template-columns: repeat(3, ___);
}
= 1fr
```

```quiz
? What does the fr unit mean?
- A fixed pixel
* A fraction of the free space
- A percentage of the font size

? Grid arranges items in rows and columns together.
= true
```

# @lesson css-responsive
title: Responsive design
summary: The viewport, media queries and flexible images.
---
A **responsive** page looks good on every screen. The first step goes in `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

## Media queries

They apply rules only when a condition holds, such as the screen width:

```try html
<style>
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .cards div { background: #e0e7ff; padding: 20px; }
  @media (max-width: 600px) {
    .cards { grid-template-columns: 1fr; }
  }
</style>
<div class="cards"><div>1</div><div>2</div><div>3</div></div>
<p>Make the window smaller or use "Full screen" to see the change.</p>
```

## Flexible images

```css
img { max-width: 100%; height: auto; }
```

:::tip Start with the phone
Write the styles for the small screen first, then add `@media (min-width: …)` for larger screens. This is called *mobile first*.
:::

```quiz
? What applies CSS rules depending on the screen width?
- <meta charset>
* @media
- display: flex

? max-width: 100% stops an image from overflowing its container.
= true
```

# @lesson css-transitions
title: Transitions and motion
summary: transition, transform and animation.
---
## Transition

Makes a change between two values smooth instead of sudden:

```try html
<style>
  .btn { background: #4338ca; color: white; padding: 10px 20px; border: 0; border-radius: 8px;
         transition: background 0.3s, transform 0.3s; }
  .btn:hover { background: #06b6d4; transform: scale(1.1); }
</style>
<button class="btn">Hover over me</button>
```

## Transform

```reference css
translate() | Move | transform: translateX(20px);
rotate() | Rotate | transform: rotate(45deg);
scale() | Grow / shrink | transform: scale(1.2);
skew() | Slant | transform: skewX(10deg);
```

## Animation

`@keyframes` defines the stages of a motion, and `animation` plays it:

```try html
<style>
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.3); }
  }
  .dot { width: 40px; height: 40px; border-radius: 50%; background: crimson;
         animation: pulse 1s infinite; margin: 20px; }
</style>
<div class="dot"></div>
```

:::warning Go easy on motion
Too much motion distracts and bothers some people. Respect the `prefers-reduced-motion` setting for people who ask for less motion.
:::

```quiz
? Which property makes a change happen smoothly over time?
* transition
- transform
- position

? @keyframes defines the stages of an animation.
= true
```

# @lesson css-reference
title: CSS property reference
summary: The most important properties with an example for each.
type: Reference
---
Search for any property in the box above the table.

```reference css
color | Text color | color: #333;
background | Background | background: #fff;
font-family | Font | font-family: sans-serif;
font-size | Font size | font-size: 1rem;
font-weight | Font weight | font-weight: 700;
line-height | Line height | line-height: 1.6;
text-align | Alignment | text-align: center;
text-decoration | Text decoration | text-decoration: none;
width / height | Width and height | width: 50%;
max-width | Maximum width | max-width: 800px;
margin | Outer space | margin: 0 auto;
padding | Inner space | padding: 1rem;
border | Border | border: 1px solid #ccc;
border-radius | Rounded corners | border-radius: 8px;
box-sizing | How size is counted | box-sizing: border-box;
box-shadow | Box shadow | box-shadow: 0 2px 8px rgba(0,0,0,.2);
display | How it is shown | display: flex;
position | Positioning | position: absolute;
top / right / bottom / left | Offsets | top: 0;
z-index | Stacking order | z-index: 10;
overflow | Content that does not fit | overflow: auto;
flex-direction | Flexbox direction | flex-direction: column;
justify-content | Distribution | justify-content: space-between;
align-items | Cross-axis alignment | align-items: center;
gap | Space between items | gap: 1rem;
grid-template-columns | Grid columns | grid-template-columns: repeat(3, 1fr);
opacity | Transparency | opacity: 0.5;
cursor | Pointer shape | cursor: pointer;
transition | Transition | transition: all .3s;
transform | Transform | transform: rotate(5deg);
animation | Animation | animation: spin 2s linear infinite;
@media | Screen query | @media (max-width: 600px) { … }
```

:::tip What next?
You can now build a page and style it. The next step: **JavaScript**, to make the page respond to the visitor.
:::
