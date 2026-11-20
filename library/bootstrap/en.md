# @lesson bs-intro
title: Bootstrap introduction
summary: What Bootstrap is and how to add it to your page.
---
**Bootstrap** is a free CSS and JavaScript library that gives you ready-made components (buttons, cards, menus, forms…) and a responsive grid, so you can build a clean page that works on phones and computers quickly.

## Adding it to your page

Put these two lines in your page (in this course they are added to every example automatically):

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

:::info Right-to-left pages
For Arabic and other right-to-left pages use `bootstrap.rtl.min.css` with `<html lang="ar" dir="rtl">`.
:::

## First example

```try html bs
<div class="container">
  <h1 class="text-primary">Hello Bootstrap</h1>
  <p class="lead">A paragraph in slightly larger text.</p>
  <button class="btn btn-success">A ready-made button</button>
</div>
```

All the styling came from ready-made **classes** such as `text-primary` and `btn btn-success`, with no CSS written.

```quiz
? How do you usually use Bootstrap components?
* By adding ready-made classes to elements
- By writing JavaScript for every element
- By renaming the tags

? Bootstrap ships a special file for right-to-left pages.
= true
```

# @lesson bs-containers
title: Containers
summary: container, container-fluid and responsive containers.
---
Every Bootstrap layout starts with a **container**:

```reference html
.container | Fixed maximum width that changes with screen size, centered | <div class="container">…</div>
.container-fluid | Always full width | <div class="container-fluid">…</div>
.container-md | Full width up to medium screens, then fixed | <div class="container-md">…</div>
```

```try html bs
<div class="container bg-light border p-3 mb-2">container: limited width, centered</div>
<div class="container-fluid bg-info-subtle border p-3">container-fluid: the whole width</div>
```

:::tip Try full screen
Press **Full screen** and change the window width to see the container change.
:::

```quiz
? Which container always takes the full screen width?
- .container
* .container-fluid
- .container-sm

? .container centers the content with a limited width.
= true
```

# @lesson bs-grid
title: The grid system
summary: Rows, the 12 columns, and responsive sizes.
---
The grid splits a line into **12 columns**. Use `row`, then `col` columns:

```try html bs
<div class="container text-center">
  <div class="row g-2">
    <div class="col"><div class="p-3 bg-primary-subtle">Column</div></div>
    <div class="col"><div class="p-3 bg-primary-subtle">Column</div></div>
    <div class="col"><div class="p-3 bg-primary-subtle">Column</div></div>
  </div>
</div>
```

## Fixed sizes

`col-8` and `col-4` take 8 and 4 of 12:

```try html bs
<div class="container">
  <div class="row g-2">
    <div class="col-8"><div class="p-3 bg-success-subtle">Main (8)</div></div>
    <div class="col-4"><div class="p-3 bg-warning-subtle">Side (4)</div></div>
  </div>
</div>
```

## Responsive

`col-12 col-md-6 col-lg-4`: full width on phones, half on medium screens, a third on large ones:

```try html bs
<div class="container">
  <div class="row g-2">
    <div class="col-12 col-md-6 col-lg-4"><div class="p-3 border">1</div></div>
    <div class="col-12 col-md-6 col-lg-4"><div class="p-3 border">2</div></div>
    <div class="col-12 col-md-6 col-lg-4"><div class="p-3 border">3</div></div>
  </div>
</div>
```

```reference html
xs (no name) | Under 576px | col-12
sm | 576px and up | col-sm-6
md | 768px and up | col-md-4
lg | 992px and up | col-lg-3
xl | 1200px and up | col-xl-2
```

```exercise html
? Make the column half the row on medium screens and up
<div class="col-12 col-___-6">…</div>
= md
```

```quiz
? How many columns does a Bootstrap row have?
- 10
* 12
- 16

? The class g-2 adds space between columns.
= true
```

# @lesson bs-typography-colors
title: Text and colors
summary: Text classes, colors and backgrounds.
---
```try html bs
<h1 class="display-5">A big heading</h1>
<p class="lead">An intro paragraph.</p>
<p class="text-muted">Muted text</p>
<p class="fw-bold text-center">Bold and centered</p>
<p class="text-danger">Error</p> <p class="text-success">Success</p>
<div class="p-2 bg-dark text-white">Dark background</div>
<div class="p-2 bg-warning-subtle mt-2">Soft background</div>
```

## The theme colors

`primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light` and `dark`. Use them with `text-`, `bg-`, `btn-` and `border-`.

```reference html
text-{color} | Text color | text-primary
bg-{color} | Background color | bg-success
bg-{color}-subtle | Soft background | bg-info-subtle
fw-bold / fw-light | Font weight | fw-bold
fs-1 … fs-6 | Font size | fs-4
text-center / text-end | Alignment | text-center
display-1 … display-6 | Big headings | display-4
lead | Standout paragraph | lead
```

```quiz
? Which class makes text red to show an error?
* text-danger
- text-error
- text-red

? bg-success-subtle gives a soft green background.
= true
```

# @lesson bs-utilities
title: Spacing and display utilities
summary: m and p for spacing, d-flex, and border, rounded and shadow.
---
## Spacing

`m` for margin and `p` for padding, then the side, then a size from 0 to 5:

```reference html
m-3 / p-3 | Every side | p-3
mt / mb | Top / bottom | mb-4
ms / me | Start / end (follows direction) | ms-2
mx / my | Horizontal / vertical | mx-auto
gap-3 | Space between items | d-flex gap-3
```

```try html bs
<div class="d-flex gap-2 p-3 bg-light">
  <div class="p-3 bg-white border rounded">A</div>
  <div class="p-3 bg-white border rounded shadow-sm">B</div>
  <div class="p-3 bg-white border rounded-pill shadow">C</div>
</div>
<div class="d-flex justify-content-between align-items-center mt-3 p-2 border">
  <span>Left</span><span>Middle</span><span>Right</span>
</div>
```

## Showing and hiding

```try html bs
<p class="d-none d-md-block bg-info-subtle p-2">Shown only on medium screens and up</p>
<p class="d-md-none bg-warning-subtle p-2">Shown only on phones</p>
```

```exercise html
? Add padding of size 3 on every side
<div class="___-3">…</div>
= p
```

```quiz
? What does the class mb-4 mean?
* A bottom margin of size 4
- A bottom padding of size 4
- A width of 4 columns

? ms-2 adds a margin at the start side, following the page direction.
= true
```

# @lesson bs-tables-images
title: Tables and images
summary: table and table-striped, and responsive images.
---
```try html bs
<table class="table table-striped table-hover">
  <thead class="table-dark">
    <tr><th>Product</th><th>Price</th></tr>
  </thead>
  <tbody>
    <tr><td>Pen</td><td>5</td></tr>
    <tr><td>Notebook</td><td>12</td></tr>
    <tr class="table-success"><td>Bag</td><td>90</td></tr>
  </tbody>
</table>
```

```reference html
table | A Bootstrap-styled table | <table class="table">
table-striped | Striped rows | table table-striped
table-hover | Highlight the row on hover | table table-hover
table-bordered | Borders on every cell | table table-bordered
table-responsive | Horizontal scroll on small screens | <div class="table-responsive">
```

## Images

```try html bs
<img src="https://picsum.photos/600/300" class="img-fluid rounded" alt="A landscape">
<img src="https://picsum.photos/120" class="rounded-circle mt-2" alt="A profile picture" width="80">
```

`img-fluid` keeps an image within the width of its container.

```quiz
? Which class makes an image responsive?
* img-fluid
- img-responsive-x
- img-auto

? table-striped colors the rows alternately.
= true
```

# @lesson bs-buttons
title: Buttons
summary: Button colors and sizes, outline buttons and button groups.
---
```try html bs
<button class="btn btn-primary">Primary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-outline-danger">Delete</button>
<button class="btn btn-secondary" disabled>Disabled</button>
<hr>
<button class="btn btn-primary btn-lg">Large</button>
<button class="btn btn-primary btn-sm">Small</button>
<a href="#" class="btn btn-link">A button as a link</a>
<hr>
<div class="btn-group">
  <button class="btn btn-outline-primary">Day</button>
  <button class="btn btn-outline-primary active">Week</button>
  <button class="btn btn-outline-primary">Month</button>
</div>
```

```reference html
btn btn-{color} | A colored button | btn btn-primary
btn-outline-{color} | Outline only | btn btn-outline-success
btn-lg / btn-sm | Size | btn btn-primary btn-lg
w-100 | Full width | btn btn-primary w-100
btn-group | Group of buttons | <div class="btn-group">
```

```exercise html
? Make the button red with an outline only
<button class="btn btn-___-danger">Delete</button>
= outline
```

```quiz
? Which class makes a large button?
- btn-big
* btn-lg
- btn-xl

? The btn classes can be used on an a element too.
= true
```

# @lesson bs-cards
title: Cards
summary: A card with image, title and text, and a grid of cards.
---
```try html bs
<div class="card" style="max-width: 18rem;">
  <img src="https://picsum.photos/400/220" class="card-img-top" alt="Product picture">
  <div class="card-body">
    <h5 class="card-title">Wireless headphones</h5>
    <p class="card-text">Clear sound and a 30-hour battery.</p>
    <a href="#" class="btn btn-primary">Buy now</a>
  </div>
</div>
```

## A grid of cards

```try html bs
<div class="row row-cols-1 row-cols-md-3 g-3">
  <div class="col"><div class="card h-100"><div class="card-body"><h5 class="card-title">Basic</h5><p class="card-text">$15</p></div></div></div>
  <div class="col"><div class="card h-100 border-primary"><div class="card-body"><h5 class="card-title text-primary">Pro</h5><p class="card-text">$35</p></div></div></div>
  <div class="col"><div class="card h-100"><div class="card-body"><h5 class="card-title">Enterprise</h5><p class="card-text">Contact us</p></div></div></div>
</div>
```

`h-100` gives the cards the same height, and `row-cols-md-3` puts three cards per row from medium screens.

```quiz
? Which class holds the main content of a card?
* card-body
- card-content
- card-inner

? h-100 gives the cards in a row the same height.
= true
```

# @lesson bs-alerts-badges
title: Alerts, badges and progress
summary: alert, badge, progress and spinner.
---
```try html bs
<div class="alert alert-success">Your changes were saved.</div>
<div class="alert alert-warning alert-dismissible fade show">
  Warning: the battery is low.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
<h5>Messages <span class="badge bg-danger">4</span></h5>
<span class="badge rounded-pill text-bg-info">New</span>
<div class="progress my-3" role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 65%">65%</div>
</div>
<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading…</span></div>
```

:::tip Closable alerts
`data-bs-dismiss="alert"` is all it takes to close an alert; Bootstrap's JavaScript does the rest.
:::

```quiz
? Which class makes a small colored number next to text?
- alert
* badge
- chip

? data-bs-dismiss="alert" makes a button close the alert.
= true
```

# @lesson bs-forms
title: Forms
summary: form-control, form-label, form-check and validation.
---
```try html bs
<form class="needs-validation" novalidate style="max-width: 420px">
  <div class="mb-3">
    <label for="email" class="form-label">E-mail</label>
    <input type="email" class="form-control" id="email" required>
    <div class="invalid-feedback">Enter a valid e-mail.</div>
  </div>
  <div class="mb-3">
    <label for="city" class="form-label">City</label>
    <select id="city" class="form-select"><option>Riyadh</option><option>Cairo</option></select>
  </div>
  <div class="form-check mb-3">
    <input class="form-check-input" type="checkbox" id="agree" required>
    <label class="form-check-label" for="agree">I accept the terms</label>
  </div>
  <button class="btn btn-primary w-100">Sign up</button>
</form>
<script>
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    e.target.classList.add("was-validated");
  });
</script>
```

```reference html
form-label | Field label | <label class="form-label">
form-control | Text field | <input class="form-control">
form-select | Drop-down | <select class="form-select">
form-check | Checkbox with its label | <div class="form-check">
input-group | Field with an add-on | <div class="input-group">
invalid-feedback | Error message | <div class="invalid-feedback">
was-validated | Show validation results | form.classList.add("was-validated")
```

```exercise html
? Complete the class that styles a text field
<input type="text" class="form-___">
= control
```

```quiz
? Which class styles a drop-down?
* form-select
- form-control-list
- dropdown-input

? was-validated shows the validation messages of a form.
= true
```

# @lesson bs-navbar
title: The navbar
summary: A responsive navbar that folds into a button on phones.
---
```try html bs
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">My shop</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="Menu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="nav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Products</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Contact</a></li>
      </ul>
    </div>
  </div>
</nav>
```

- `navbar-expand-lg`: shown in full on large screens and folded into a button on smaller ones.
- The `navbar-toggler` button opens the folded menu through `data-bs-target`.

:::tip See it folded
Press **Full screen** and narrow the window; the menu icon appears.
:::

```quiz
? What makes the navbar fold on small screens?
* navbar-expand-lg with navbar-collapse
- navbar-small
- d-none

? data-bs-target names the element the button opens.
= true
```

# @lesson bs-modal
title: Modals
summary: A modal that opens from a button with no JavaScript of your own.
---
```try html bs
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#confirm">Delete account</button>

<div class="modal fade" id="confirm" tabindex="-1" aria-labelledby="confirmTitle" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="confirmTitle">Confirm</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">Are you sure? This cannot be undone.</div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-danger">Delete</button>
      </div>
    </div>
  </div>
</div>
```

## Other interactive components, the same way

```reference html
modal | Pop-up window | data-bs-toggle="modal"
collapse | Show and hide content | data-bs-toggle="collapse"
dropdown | Drop-down menu | data-bs-toggle="dropdown"
tooltip | Hint on hover | data-bs-toggle="tooltip"
offcanvas | Sliding side panel | data-bs-toggle="offcanvas"
carousel | Slideshow | <div class="carousel slide">
accordion | Collapsible sections | <div class="accordion">
```

```quiz
? Which attribute opens the modal when the button is pressed?
* data-bs-toggle="modal"
- onclick="modal()"
- href="#modal"

? Bootstrap's interactive components need bootstrap.bundle.js.
= true
```

# @lesson bs-reference
title: Bootstrap reference
summary: The most important classes with an example for each.
type: Reference
---
Search the table for any class.

```reference html
container / container-fluid | Containers | <div class="container">
row / col | The grid | <div class="row"><div class="col-md-6">
g-{0-5} | Space between columns | row g-3
m- / p- | Margin and padding | mt-3 p-2
d-flex / d-none / d-md-block | Display | d-flex gap-2
justify-content-* | Horizontal distribution | justify-content-between
align-items-* | Vertical alignment | align-items-center
text-* / bg-* | Colors | text-primary bg-light
fw-bold / fs-* | Font | fw-bold fs-5
border / rounded / shadow | Border, corners, shadow | border rounded shadow-sm
btn btn-* | Buttons | btn btn-success
card / card-body | Cards | <div class="card">
alert alert-* | Alerts | alert alert-warning
badge | Badges | badge text-bg-danger
table table-* | Tables | table table-striped
img-fluid | Responsive image | <img class="img-fluid">
form-control / form-select | Forms | <input class="form-control">
navbar | Navbar | navbar navbar-expand-lg
modal | Modal | data-bs-toggle="modal"
visually-hidden | Text for screen readers only | <span class="visually-hidden">
```

:::tip What next?
Build a full landing page: a navbar, a welcome section, three cards and a contact form. Then try the **React** course to build interactive interfaces.
:::
