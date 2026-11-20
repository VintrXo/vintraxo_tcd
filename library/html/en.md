# @lesson html-intro
title: HTML introduction
summary: What HTML is and how a browser reads a web page.
---
**HTML** is the language web pages are written in. The name stands for *HyperText Markup Language*.

HTML is not a programming language; it is a **markup** language. You wrap each piece of content in a "tag" that tells the browser what it is: a heading, a paragraph, an image, a link…

## Your first page

This is a complete HTML page. Press **Run** to see the result, then change the text and run it again:

```try html
<!DOCTYPE html>
<html>
<head>
  <title>My first page</title>
</head>
<body>
  <h1>Hello, world</h1>
  <p>This is the first paragraph I wrote in HTML.</p>
</body>
</html>
```

## What is happening here?

- `<!DOCTYPE html>` tells the browser the document is HTML5.
- `<html>` is the root element that holds the whole page.
- `<head>` holds information about the page that is not shown inside it, such as the title in the browser tab.
- `<body>` holds everything the visitor sees.
- `<h1>` is a main heading and `<p>` is a paragraph.

:::info How does the browser work?
The browser does not display the tags themselves; it reads them to know how to display the content. That is why you see "Hello, world" in large text and not `<h1>`.
:::

```quiz
? What does HTML stand for?
- A server programming language
* HyperText Markup Language
- A website database
> HTML is a markup language that describes the content of a page.

? The content of the head element is shown inside the page.
= false
> head holds information about the page such as its title; what the visitor sees goes inside body.
```

# @lesson html-editors
title: HTML editors
summary: Where to write HTML and how to open your page in a browser.
---
Any tool that writes plain text is enough to write HTML. Editors made for code make the work easier: they color the code, complete tags and point out mistakes.

## Popular editors

- **Visual Studio Code**: free, runs on every system, and the most used.
- **Notepad++** on Windows, or **TextEdit** on Mac in plain-text mode.
- This platform's editor: every example has a **Run** button that shows the result at once, nothing to install.

## Your first file on your computer

1. Open the editor and create a new file.
2. Write a simple HTML page.
3. Save the file with a name ending in `.html`, such as `index.html`.
4. Open the file in your browser (double-click it).

```html
<!DOCTYPE html>
<html>
<body>
  <h1>A page on my computer</h1>
  <p>I opened it from index.html</p>
</body>
</html>
```

:::tip Tip
Name your site's home page `index.html`; servers open this file automatically when a folder is visited.
:::

```quiz
? What is the right extension for a web page file?
- .txt
* .html
- .doc
```

# @lesson html-basic
title: HTML basics
summary: The basic structure of every page, and headings, paragraphs, links and images in one example.
---
Every HTML page starts with the same structure; then you add what you want to show inside `<body>`.

## The basic structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Page title</title>
</head>
<body>
  ...content here...
</body>
</html>
```

- `lang="en"` sets the language of the page; for Arabic pages use `lang="ar" dir="rtl"` so text runs right to left.
- `<meta charset="UTF-8">` makes sure every character, including Arabic letters, displays correctly.

## Quick examples

Headings go from `<h1>` (largest) to `<h6>` (smallest). A paragraph is `<p>`. A link is `<a>`. An image is `<img>`.

```try html
<h1>Main heading</h1>
<h2>Sub heading</h2>
<p>This is a paragraph.</p>
<a href="https://www.wikipedia.org">A link to Wikipedia</a>
<br>
<img src="https://picsum.photos/200/120" alt="A random picture" width="200">
```

```exercise html
? Complete the code so the text is a paragraph
<___>I am a paragraph</p>
= p
! The tag that closes at the end of the line is the one that opens at its start.
```

```quiz
? Which tag makes sure every character displays correctly?
- <title>
* <meta charset="UTF-8">
- <body>

? dir="rtl" makes the page run from right to left.
= true
```

# @lesson html-elements
title: HTML elements
summary: Opening and closing tags, empty elements and nested elements.
---
An **element** in HTML is everything from the opening tag to the closing tag:

```html
<p>This is a paragraph element.</p>
```

- `<p>` is the opening tag.
- `This is a paragraph element.` is the content.
- `</p>` is the closing tag; it has a slash `/`.

## Empty elements

Some elements have no content and no closing tag, such as `<br>` (line break), `<img>` (image) and `<hr>` (horizontal rule).

```try html
<p>First line<br>Second line</p>
<hr>
<p>A paragraph after the rule.</p>
```

## Nested elements

An element can sit inside another element. A whole page is nested elements: `<body>` inside `<html>`, and `<p>` inside `<body>`.

```try html
<body>
  <h1>A heading</h1>
  <p>A paragraph with a <strong>bold word</strong> inside it.</p>
</body>
```

:::warning Do not forget the closing tag
Some browsers show the page even when a closing tag is missing, but the result may be unexpected. Close every element you open.
:::

```exercise html
? Complete the closing tag
<h2>Sub heading<___>
= /h2
```

```quiz
? Which of these is an empty element (no closing tag)?
- <p>
* <br>
- <h1>

? A closing tag has a slash / before the tag name.
= true
```

# @lesson html-attributes
title: HTML attributes
summary: Extra information written in the opening tag, such as href, src and alt.
---
**Attributes** give an element extra information. They are always written in the opening tag as `name="value"`.

## Important attributes

- `href` on a link `<a>`: the address the link opens.
- `src` on an image `<img>`: the path of the image.
- `alt` on an image: alternative text shown if the image does not load, and read by screen readers.
- `width` and `height`: the width and height of an image.
- `style`: styles the element directly (color, size…).
- `lang` and `dir`: the language and direction of the content.
- `title`: text shown when the mouse is over the element.

```try html
<a href="https://www.wikipedia.org" title="Open Wikipedia">Visit Wikipedia</a>
<p style="color: teal;">A paragraph with its own color.</p>
<img src="https://picsum.photos/180/100" alt="A landscape" width="180" height="100">
```

:::tip Quote attribute values
`href="page.html"` is clearer and safer than `href=page.html`, especially when the value has spaces.
:::

```exercise html
? Complete the attribute that sets the image path
<img ___="logo.png" alt="The logo">
= src
```

```quiz
? Where are attributes written?
* In the opening tag
- In the closing tag
- After the end of the element

? What is the alt attribute of an image for?
- Setting the image width
* Text that describes the image
- Setting the image path
```

# @lesson html-headings
title: Headings
summary: From h1 to h6, and why heading order matters.
---
Headings are defined with the tags `<h1>` to `<h6>`. `<h1>` is the most important and largest, `<h6>` the least important.

```try html
<h1>Heading level 1</h1>
<h2>Heading level 2</h2>
<h3>Heading level 3</h3>
<h4>Heading level 4</h4>
<h5>Heading level 5</h5>
<h6>Heading level 6</h6>
```

## Why do headings matter?

- Search engines use them to understand what the page is about.
- Screen readers jump between headings to help blind users.
- Visitors scan the headings first to find what they need.

:::tip A simple rule
Use `<h1>` once for the page title, then `<h2>` for sections and `<h3>` for subsections. Do not pick a heading for its font size; size is changed with styling.
:::

```exercise html
? Write the largest heading
<___>Page title</h1>
= h1
```

```quiz
? Which heading is the most important?
* <h1>
- <h6>
- <head>

? It is best to use <h1> once, for the page title.
= true
```

# @lesson html-paragraphs
title: Paragraphs
summary: Paragraphs, line breaks, horizontal rules and preformatted text.
---
A paragraph always starts on a new line, and the browser adds space before and after it.

```try html
<p>This is a paragraph.</p>
<p>And this is another paragraph.</p>
```

## Spaces are collapsed

The browser turns runs of spaces and new lines into a single space. To break a line, use `<br>`:

```try html
<p>These      words
are written on    several lines.</p>
<p>First line<br>Second line</p>
```

## Rules and preformatted text

- `<hr>` draws a horizontal line between two topics.
- `<pre>` shows text exactly as written, with its spaces and lines.

```try html
<p>First topic</p>
<hr>
<p>Second topic</p>
<pre>
  A poem
    with its spaces
      kept as they are
</pre>
```

```quiz
? How do you break a line inside a paragraph?
- <hr>
* <br>
- <pre>

? The browser keeps runs of spaces inside <p> as they are.
= false
> Runs of spaces collapse into one, except inside <pre>.
```

# @lesson html-formatting
title: Text formatting
summary: Bold, italic, important, highlighted, deleted, inserted, subscript and superscript.
---
HTML has elements that give text a special meaning:

```reference html
<b> | Bold text (looks only) | <b>bold</b>
<strong> | Important text, shown bold | <strong>Warning</strong>
<i> | Italic text (looks only) | <i>italic</i>
<em> | Emphasized text, shown italic | <em>very important</em>
<mark> | Highlighted text | <mark>look here</mark>
<small> | Smaller text | <small>note</small>
<del> | Deleted text | <del>100</del>
<ins> | Inserted text | <ins>80</ins>
<sub> | Subscript | H<sub>2</sub>O
<sup> | Superscript | x<sup>2</sup>
```

```try html
<p>Price: <del>$100</del> <ins>$80</ins></p>
<p>Water is H<sub>2</sub>O and the area of a square is x<sup>2</sup>.</p>
<p><strong>Note:</strong> save your work <mark>before</mark> closing.</p>
```

:::info b versus strong
Both look bold, but `<strong>` means the text is **important**, and screen readers stress it. Use `<strong>` and `<em>` when you mean the meaning.
:::

```exercise html
? Make the 2 a superscript
x<___>2</sup>
= sup
```

```quiz
? Which element means the text is important?
- <b>
* <strong>
- <small>

? Which element is used for the 2 in H2O?
* <sub>
- <sup>
- <del>
```

# @lesson html-comments
title: Comments
summary: Notes in the code that do not show on the page.
---
A comment is written between `<!--` and `-->`. The browser ignores it, so visitors do not see it, but it helps you and your colleagues.

```try html
<!-- This comment is not shown -->
<p>This paragraph is shown.</p>
<!--
<p>A paragraph switched off for now</p>
-->
```

## When to use comments

- To explain a complex part of the page.
- To switch a part off for a while instead of deleting it.
- To split a long file into clear sections.

:::warning
Comments are visible to anyone who opens "View source" in the browser. Never put passwords or private information in them.
:::

```quiz
? How does a comment start in HTML?
* <!--
- //
- #

? Comments are completely hidden and nobody can see them.
= false
> They are not shown on the page, but they are in the page source.
```

# @lesson html-links
title: Links
summary: Links, opening in a new tab, links inside the page and e-mail links.
---
Links are what make the web a "web". They are written with the `<a>` element and the `href` attribute:

```html
<a href="https://www.wikipedia.org">Visit Wikipedia</a>
```

## Opening a link in a new tab

`target="_blank"` opens the link in a new tab:

```try html
<a href="https://www.wikipedia.org" target="_blank">Wikipedia in a new tab</a>
```

## Kinds of addresses

- **Absolute URL**: `https://example.com/page.html` for a page on another site.
- **Relative URL**: `about.html` for a page on the same site.
- **Link to a part of the page**: `#contact` jumps to the element with `id="contact"`.
- **E-mail**: `mailto:info@example.com` opens the mail program.

```try html
<a href="#end">Jump to the end</a>
<p style="height: 300px;">Long content…</p>
<h2 id="end">The end</h2>
<a href="mailto:info@example.com">E-mail us</a>
```

```exercise html
? Complete the attribute that sets the link address
<a ___="https://example.com">A site</a>
= href
```

```quiz
? Which attribute opens a link in a new tab?
- href="_new"
* target="_blank"
- open="new"

? The link href="#contact" jumps to the element with id="contact".
= true
```

# @lesson html-images
title: Images
summary: Adding an image, alternative text, size, and images as links.
---
An image is added with the empty element `<img>` and two key attributes: `src` for the image path and `alt` to describe it.

```try html
<img src="https://picsum.photos/300/180" alt="A landscape" width="300" height="180">
```

## Why alt matters

- It is shown instead of the image if the image cannot load.
- Screen readers read it to blind users.
- It helps search engines understand the image.

```try html
<img src="no-such-image.jpg" alt="Missing image: this text is shown instead">
```

## An image as a link

Put `<img>` inside `<a>`:

```try html
<a href="https://www.wikipedia.org">
  <img src="https://picsum.photos/120/80" alt="Go to Wikipedia">
</a>
```

:::tip Set width and height
With `width` and `height` the browser reserves the image's space before it loads, so the page does not "jump".
:::

```exercise html
? Complete the attribute that describes the image
<img src="cat.jpg" ___="A sleeping cat">
= alt
```

```quiz
? Which attribute sets the image path?
* src
- href
- alt

? The <img> element needs a closing tag.
= false
```

# @lesson html-lists
title: Lists
summary: Bullet lists, numbered lists, description lists and nested lists.
---
## Bullet list

`<ul>` is an unordered list; each item in it is an `<li>`:

```try html
<ul>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>
```

## Numbered list

`<ol>` is an ordered, numbered list:

```try html
<ol>
  <li>Open the editor</li>
  <li>Write the code</li>
  <li>Save the file</li>
</ol>
```

## Description list

`<dl>` for a term `<dt>` and its description `<dd>`:

```try html
<dl>
  <dt>HTML</dt>
  <dd>The markup language of web pages</dd>
  <dt>CSS</dt>
  <dd>The styling language of web pages</dd>
</dl>
```

## A list inside a list

```try html
<ul>
  <li>Drinks
    <ul>
      <li>Hot</li>
      <li>Cold</li>
    </ul>
  </li>
  <li>Desserts</li>
</ul>
```

```exercise html
? Complete the numbered list tag
<___>
  <li>First</li>
  <li>Second</li>
</ol>
= ol
```

```quiz
? Which tag creates a numbered list?
- <ul>
* <ol>
- <dl>

? Every item of a bullet or numbered list goes inside <li>.
= true
```

# @lesson html-tables
title: Tables
summary: Rows, cells, header cells and merged cells.
---
A table `<table>` is made of rows `<tr>`, and each row of cells: `<th>` for a header cell and `<td>` for a data cell.

```try html
<table border="1">
  <tr>
    <th>Name</th>
    <th>City</th>
  </tr>
  <tr>
    <td>Sara</td>
    <td>Riyadh</td>
  </tr>
  <tr>
    <td>Ahmed</td>
    <td>Cairo</td>
  </tr>
</table>
```

## Table head and body

`<thead>` for the header row, `<tbody>` for the other rows, and `<caption>` for the table title:

```try html
<table border="1">
  <caption>Student grades</caption>
  <thead>
    <tr><th>Student</th><th>Grade</th></tr>
  </thead>
  <tbody>
    <tr><td>Layla</td><td>95</td></tr>
    <tr><td>Omar</td><td>88</td></tr>
  </tbody>
</table>
```

## Merging cells

`colspan` stretches a cell over several columns, `rowspan` over several rows:

```try html
<table border="1">
  <tr><th colspan="2">Full name</th></tr>
  <tr><td>Nour</td><td>Mohamed</td></tr>
</table>
```

```quiz
? Which tag is a table row?
* <tr>
- <td>
- <th>

? Which attribute makes a cell span two columns?
- rowspan="2"
* colspan="2"
- span="2"
```

# @lesson html-block-inline
title: Block and inline elements
summary: The difference between div and span, and why some elements start on a new line.
---
## Block elements

They always start on a new line and take the full width, such as `<div>`, `<p>`, `<h1>`, `<ul>` and `<table>`.

## Inline elements

They stay inside the line and take only the space of their content, such as `<span>`, `<a>`, `<strong>` and `<img>`.

```try html
<div style="background: #e0f2fe;">I am a div: I take the whole line</div>
<div style="background: #fef3c7;">And I am another div on a new line</div>
<p>This paragraph has a <span style="background: #dcfce7;">span</span> inside the line.</p>
```

## div and span for grouping

- `<div>` groups several elements so you can style or arrange them together.
- `<span>` wraps a small part of text so you can style it.

```try html
<div style="border: 1px solid #94a3b8; padding: 8px;">
  <h3>A card</h3>
  <p>Price: <span style="color: crimson;">$50</span></p>
</div>
```

```quiz
? Which element starts on a new line and takes the full width?
* <div>
- <span>
- <a>

? <span> is an inline element.
= true
```

# @lesson html-semantic
title: Semantic elements
summary: header, nav, main, article, section and footer.
---
**Semantic** elements describe the meaning of their content clearly, instead of a generic `<div>` for everything. This helps search engines and screen readers and makes the code easier to read.

```reference html
<header> | Header of the page or a section: logo and title | <header>…</header>
<nav> | Main navigation links | <nav><a href="/">Home</a></nav>
<main> | The main content of the page (once) | <main>…</main>
<article> | Self-contained content: article, post, news item | <article>…</article>
<section> | A section of content with a heading | <section><h2>…</h2></section>
<aside> | Side content related to the topic | <aside>…</aside>
<footer> | Page footer: copyright, links | <footer>…</footer>
```

```try html
<header>
  <h1>My blog</h1>
  <nav><a href="#">Home</a> | <a href="#">About</a></nav>
</header>
<main>
  <article>
    <h2>First post</h2>
    <p>The text of the post…</p>
  </article>
</main>
<footer>
  <small>All rights reserved</small>
</footer>
```

```quiz
? Which element is meant for navigation links?
- <header>
* <nav>
- <aside>

? <main> is used once per page.
= true
```

# @lesson html-forms
title: Forms
summary: A form that collects visitor data: fields, labels and a submit button.
---
A form `<form>` collects data from the visitor and sends it to the server. Inside it are input fields `<input>` and their labels `<label>`.

```try html
<form>
  <label for="name">Name:</label><br>
  <input type="text" id="name" name="name"><br><br>
  <label for="email">E-mail:</label><br>
  <input type="email" id="email" name="email"><br><br>
  <input type="submit" value="Send">
</form>
```

## Important parts

- `<label for="name">` ties the label to the field with `id="name"`; clicking the label puts the cursor in the field.
- `name` is the field's name when the form is sent; without it, its value is not sent.
- `action` on `<form>` is the address that receives the data, and `method` is how it is sent (`get` or `post`).

## Other elements

```try html
<form>
  <label for="msg">Your message:</label><br>
  <textarea id="msg" name="msg" rows="3" cols="30"></textarea><br>
  <label for="city">City:</label>
  <select id="city" name="city">
    <option>Riyadh</option>
    <option>Cairo</option>
    <option>Dubai</option>
  </select><br><br>
  <button type="submit">Send</button>
</form>
```

```exercise html
? Tie the label to the field with id="phone"
<label ___="phone">Phone</label>
<input type="tel" id="phone" name="phone">
= for
```

```quiz
? What is the name attribute of a field for?
- Setting the field color
* Sending the field value under that name
- Showing text inside the field

? Which element is used for long, multi-line text?
- <input type="text">
* <textarea>
- <select>
```

# @lesson html-input-types
title: Input types
summary: Text, password, number, date, single choice, multiple choice, and built-in validation.
---
The `type` attribute changes how a field looks and behaves:

```reference html
text | One line of text | <input type="text">
password | A password shown as dots | <input type="password">
email | An e-mail address, validated | <input type="email">
number | A number with arrows | <input type="number" min="1" max="10">
date | A date picker | <input type="date">
radio | One choice from a group | <input type="radio" name="g">
checkbox | Several choices | <input type="checkbox">
color | A color picker | <input type="color">
range | A slider | <input type="range">
file | A file upload | <input type="file">
```

```try html
<form>
  <input type="password" placeholder="Password"><br><br>
  <input type="number" min="1" max="5" value="1"><br><br>
  <input type="date"><br><br>
  <label><input type="radio" name="size" value="s"> Small</label>
  <label><input type="radio" name="size" value="l"> Large</label><br><br>
  <label><input type="checkbox" name="milk"> Milk</label>
  <label><input type="checkbox" name="sugar"> Sugar</label><br><br>
  <input type="color" value="#4338ca">
</form>
```

## Checking before sending

- `required`: the field must be filled.
- `min` and `max`: the smallest and largest value.
- `maxlength`: the most characters allowed.
- `pattern`: a pattern the value must match.

```try html
<form>
  <input type="email" required placeholder="Your e-mail (required)">
  <input type="submit" value="Try sending it empty">
</form>
```

:::warning Browser checks are not enough
Browser validation is easy to get around. The server must also check all the data it receives.
:::

```quiz
? Which type allows only one choice from a group?
* radio
- checkbox
- range

? The required attribute makes a field mandatory before sending.
= true

? Pick the types that show a special picker in the browser
* date
* color
- text
```

# @lesson html-reference
title: HTML tag reference
summary: A quick table of the most important tags, with an example for each.
type: Reference
---
Use the search box above the table to find any tag quickly.

```reference html
<html> | Root of the page | <html lang="en">…</html>
<head> | Information about the page | <head><title>…</title></head>
<title> | Tab title | <title>My page</title>
<meta> | Metadata | <meta charset="UTF-8">
<link> | Link an external file such as CSS | <link rel="stylesheet" href="style.css">
<script> | JavaScript code | <script src="app.js"></script>
<body> | Visible content of the page | <body>…</body>
<h1>…<h6> | Headings | <h2>Section</h2>
<p> | Paragraph | <p>Text</p>
<br> | Line break | line<br>line
<hr> | Horizontal rule | <hr>
<a> | Link | <a href="page.html">Page</a>
<img> | Image | <img src="a.png" alt="description">
<ul> / <ol> / <li> | Lists | <ul><li>item</li></ul>
<dl> / <dt> / <dd> | Description list | <dl><dt>word</dt><dd>meaning</dd></dl>
<table> | Table | <table><tr><td>cell</td></tr></table>
<tr> / <th> / <td> | Row, header cell, cell | <tr><th>A</th><td>B</td></tr>
<div> | A group (block) | <div>…</div>
<span> | Part of the text (inline) | <span>word</span>
<strong> / <em> | Important / emphasized | <strong>important</strong>
<header> / <footer> | Header and footer | <footer>…</footer>
<nav> | Navigation links | <nav>…</nav>
<main> | Main content | <main>…</main>
<section> / <article> | Section / self-contained content | <article>…</article>
<form> | Form | <form action="/send">…</form>
<input> | Input field | <input type="text" name="q">
<label> | Field label | <label for="q">Search</label>
<textarea> | Multi-line text | <textarea></textarea>
<select> / <option> | Drop-down list | <select><option>A</option></select>
<button> | Button | <button>Press</button>
<!-- --> | Comment | <!-- note -->
```

:::tip What next?
You have finished the HTML basics. The next step: **CSS**, to style, color and lay out your pages.
:::
