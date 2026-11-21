# @lesson gfx-intro
title: Graphics on the web
summary: SVG and Canvas, what each is good at, and a first drawing in both.
---
Browsers have two built-in ways to draw:

| | SVG | Canvas |
|---|---|---|
| What it is | Shapes written as HTML-like tags | A pixel surface you paint on with JavaScript |
| Scales without blur | Yes (vector) | No (pixels) |
| Each shape is an element | Yes: style it with CSS, click it | No: once drawn, it is just pixels |
| Best for | Icons, logos, diagrams, charts | Games, animations with many objects, image editing |

```try html
<svg width="220" height="120" style="border:1px solid #ccc">
  <circle cx="60" cy="60" r="40" fill="#4338ca" />
  <rect x="120" y="25" width="80" height="70" rx="10" fill="#0e7490" />
</svg>

<canvas id="c" width="220" height="120" style="border:1px solid #ccc"></canvas>
<script>
  const ctx = document.getElementById("c").getContext("2d");
  ctx.fillStyle = "#4338ca";
  ctx.beginPath();
  ctx.arc(60, 60, 40, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#0e7490";
  ctx.fillRect(120, 25, 80, 70);
</script>
```

Both pictures look the same, but they are made very differently: the SVG is two elements in the page, the canvas is a grid of pixels painted by code.

:::info Coordinates
In both, `(0, 0)` is the **top-left** corner, `x` grows to the right and `y` grows **downwards**.
:::

```quiz
? Which technology keeps each shape as an element you can style with CSS?
* SVG
- Canvas
- Both

? In SVG and Canvas, y grows downwards.
= true
```

# @lesson svg-shapes
title: SVG basic shapes
summary: rect, circle, ellipse, line, polyline, polygon and the viewBox.
---
```try html
<svg viewBox="0 0 300 160" width="100%" style="max-width:450px; border:1px solid #ddd">
  <rect x="10" y="10" width="80" height="50" fill="#fde68a" stroke="#b45309" stroke-width="3" />
  <rect x="110" y="10" width="80" height="50" rx="12" fill="#bfdbfe" />
  <circle cx="240" cy="35" r="25" fill="#fca5a5" />
  <ellipse cx="50" cy="115" rx="40" ry="22" fill="#bbf7d0" stroke="#15803d" />
  <line x1="110" y1="90" x2="190" y2="140" stroke="#334155" stroke-width="4" stroke-linecap="round" />
  <polyline points="200,140 220,95 240,125 260,90 280,140" fill="none" stroke="#7c3aed" stroke-width="3" />
</svg>
```

- `viewBox="0 0 300 160"` defines the drawing's own coordinate system. With `width="100%"` the drawing scales to fit the page without losing quality.
- `fill` paints the inside; `stroke` and `stroke-width` draw the outline.
- `polygon` is like `polyline` but closes the shape automatically.

```reference html
<rect x y width height rx> | Rectangle (rx rounds the corners) | <rect x="0" y="0" width="50" height="20" rx="4"/>
<circle cx cy r> | Circle | <circle cx="50" cy="50" r="40"/>
<ellipse cx cy rx ry> | Ellipse | <ellipse cx="50" cy="30" rx="40" ry="20"/>
<line x1 y1 x2 y2> | Straight line | <line x1="0" y1="0" x2="100" y2="50" stroke="black"/>
<polyline points> / <polygon points> | Open / closed connected lines | <polygon points="50,0 100,100 0,100"/>
viewBox="minx miny w h" | Internal coordinate system | <svg viewBox="0 0 100 100">
fill / stroke / stroke-width | Colors and outline | fill="none" stroke="red"
```

```exercise html
? Draw a circle with radius 30
<circle cx="50" cy="50" ___="30" />
= r
```

```quiz
? What does viewBox let an SVG do?
* Scale its drawing to any size without blur
- Load images faster
- Animate automatically
```

# @lesson svg-paths
title: SVG paths
summary: The path element and its commands: move, line, curve and arc.
---
`<path>` can draw any shape. Its `d` attribute is a list of commands: a letter followed by numbers.

```try html
<svg viewBox="0 0 320 170" width="100%" style="max-width:480px; border:1px solid #ddd">
  <!-- a house: M = move to, L = line to, Z = close -->
  <path d="M 20 90 L 70 40 L 120 90 Z" fill="#fca5a5" />
  <path d="M 30 90 L 30 150 L 110 150 L 110 90" fill="#fde68a" stroke="#92400e" />

  <!-- a wave: Q = quadratic curve (one control point) -->
  <path d="M 140 100 Q 165 40 190 100 Q 215 160 240 100" fill="none" stroke="#2563eb" stroke-width="4" />

  <!-- a heart: C = cubic curves (two control points) -->
  <path d="M 285 75 C 285 55 260 50 260 70 C 260 85 285 100 285 110 C 285 100 310 85 310 70 C 310 50 285 55 285 75 Z" fill="#e11d48" />

  <!-- an arc: A = elliptical arc, here half a circle -->
  <path d="M 150 150 A 40 40 0 0 1 230 150" fill="none" stroke="#15803d" stroke-width="4" />
</svg>
```

| Command | Meaning |
|---|---|
| `M x y` | Move the pen without drawing |
| `L x y` | Straight line to the point |
| `H x` / `V y` | Horizontal / vertical line |
| `Q cx cy x y` | Curve with one control point |
| `C c1x c1y c2x c2y x y` | Curve with two control points |
| `A rx ry rot large sweep x y` | Arc of an ellipse |
| `Z` | Close the shape back to the start |

Lower-case letters (`m`, `l`, `c`...) use positions **relative** to the current point instead of absolute ones.

:::tip You rarely write long paths by hand
Design tools such as Figma, Inkscape and Illustrator export SVG paths. Knowing the commands lets you read, tidy and animate what they produce.
:::

```exercise html
? Which path command closes the shape?
<path d="M 0 0 L 50 0 L 25 40 ___" />
= Z | z
```

```quiz
? What does M do in a path?
* Moves the pen to a point without drawing
- Draws a circle
- Mirrors the shape
```

# @lesson svg-style
title: Styling SVG with CSS, gradients and text
summary: Classes, hover effects, linear and radial gradients, and text.
---
```try html
<style>
  .bar { fill: #6366f1; transition: fill .2s; }
  .bar:hover { fill: #f59e0b; }
  .label { font: bold 14px system-ui, sans-serif; fill: #0f172a; }
</style>
<svg viewBox="0 0 320 170" width="100%" style="max-width:480px">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#38bdf8" />
      <stop offset="1" stop-color="#e0f2fe" />
    </linearGradient>
    <radialGradient id="sun">
      <stop offset="0" stop-color="#fef08a" />
      <stop offset="1" stop-color="#f97316" />
    </radialGradient>
  </defs>
  <rect width="320" height="90" fill="url(#sky)" />
  <circle cx="270" cy="40" r="25" fill="url(#sun)" />
  <rect class="bar" x="20" y="100" width="40" height="60" />
  <rect class="bar" x="70" y="120" width="40" height="40" />
  <rect class="bar" x="120" y="90" width="40" height="70" />
  <text class="label" x="175" y="140">Hover the bars</text>
</svg>
```

- SVG elements accept CSS classes, so `:hover`, transitions and dark mode work as with HTML.
- Reusable things such as gradients go inside `<defs>` and are used with `fill="url(#id)"`.
- `<text>` draws text that stays selectable and searchable.

```reference html
class / <style> | Style SVG with CSS | .bar:hover { fill: orange; }
<defs> | Definitions reused later | <defs><linearGradient id="g">...</defs>
<linearGradient> / <radialGradient> | Gradients | fill="url(#g)"
<stop offset stop-color> | A gradient color point | <stop offset="1" stop-color="#fff"/>
<text x y> | Text | <text x="10" y="20">Hi</text>
<g> | Group shapes to move or style together | <g fill="red">...</g>
```

```exercise html
? Fill a shape with the gradient whose id is sky
<rect width="100" height="50" fill="___(#sky)" />
= url
```

```quiz
? Where do you usually put gradients that shapes will reuse?
* Inside <defs>
- Inside <text>
- In the stroke attribute
```

# @lesson svg-animate
title: Transforms and animation in SVG
summary: translate, rotate, scale, grouping, and CSS animations.
---
```try html
<style>
  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes pulse { 50% { transform: scale(1.25); } }
  .gear { transform-origin: 80px 80px; animation: spin 4s linear infinite; }
  .dot { transform-box: fill-box; transform-origin: center; animation: pulse 1.2s ease-in-out infinite; }
</style>
<svg viewBox="0 0 320 160" width="100%" style="max-width:480px">
  <g class="gear" fill="#475569">
    <circle cx="80" cy="80" r="40" />
    <rect x="72" y="25" width="16" height="20" />
    <rect x="72" y="115" width="16" height="20" />
    <rect x="25" y="72" width="20" height="16" />
    <rect x="115" y="72" width="20" height="16" />
    <circle cx="80" cy="80" r="14" fill="#fff" />
  </g>
  <g transform="translate(190 40)">
    <rect width="40" height="40" fill="#93c5fd" />
    <rect width="40" height="40" fill="#2563eb" transform="rotate(30) scale(0.7)" opacity="0.8" />
  </g>
  <circle class="dot" cx="260" cy="120" r="14" fill="#e11d48" />
</svg>
```

```reference html
transform="translate(x y)" | Move | <g transform="translate(20 10)">
rotate(deg) / scale(s) | Turn / resize | transform="rotate(45)"
transform-origin | The point it turns around (CSS) | transform-origin: 50px 50px
@keyframes + animation | CSS animation | animation: spin 3s linear infinite
opacity | Transparency 0..1 | opacity="0.5"
```

:::tip Respect reduced motion
Some people get dizzy from movement. Wrap decorative animations in `@media (prefers-reduced-motion: no-preference) { ... }` so they only run for people who have not asked their system to reduce motion.
:::

```exercise html
? Move a group 50 to the right and 20 down
<g transform="___(50 20)">
= translate
```

```quiz
? Which CSS property sets the point a shape rotates around?
* transform-origin
- rotate-center
- viewBox
```

# @lesson svg-chart
title: Project: a bar chart in SVG with JavaScript
summary: Build an accessible chart from data with createElementNS.
---
SVG elements must be created with `document.createElementNS` and the SVG namespace. The chart below is built from an array, so changing the data redraws it.

```try html
<svg id="chart" viewBox="0 0 420 220" width="100%" style="max-width:560px" role="img" aria-labelledby="chart-title">
  <title id="chart-title">Monthly sales</title>
</svg>
<script>
  const data = [ ["Jan", 120], ["Feb", 180], ["Mar", 150], ["Apr", 240], ["May", 210], ["Jun", 280] ];
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.getElementById("chart");
  const W = 420, H = 220, pad = 30, max = Math.max(...data.map(d => d[1]));
  const barW = (W - pad * 2) / data.length;

  function add(tag, attrs, text) {
    const el = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    if (text !== undefined) el.textContent = text;
    svg.appendChild(el);
    return el;
  }

  add("line", { x1: pad, y1: H - pad, x2: W - pad, y2: H - pad, stroke: "#94a3b8" });
  data.forEach(([label, value], i) => {
    const h = (value / max) * (H - pad * 2);
    const x = pad + i * barW + 6;
    const bar = add("rect", { x, y: H - pad - h, width: barW - 12, height: h, rx: 4, fill: "#6366f1" });
    add("title", {}, label + ": " + value);
    bar.appendChild(svg.lastChild);           // tooltip on hover
    add("text", { x: x + (barW - 12) / 2, y: H - pad + 16, "text-anchor": "middle", "font-size": 12 }, label);
    add("text", { x: x + (barW - 12) / 2, y: H - pad - h - 5, "text-anchor": "middle", "font-size": 11, fill: "#475569" }, value);
  });
</script>
```

:::tip Make charts accessible
`role="img"` with a `<title>` gives screen readers a name for the chart, and a `<title>` inside each bar shows a tooltip. For important numbers, also show them as text or a table.
:::

```quiz
? Why does the code use createElementNS instead of createElement?
* SVG elements belong to the SVG namespace and must be created in it
- createElement is slower
- createElementNS adds colors automatically
```

# @lesson canvas-basics
title: Canvas basics
summary: The 2D context, rectangles, colors, lines and paths.
---
```try html
<canvas id="c" width="320" height="180" style="border:1px solid #ccc; max-width:100%"></canvas>
<script>
  const canvas = document.getElementById("c");
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#e0f2fe";
  ctx.fillRect(0, 0, canvas.width, canvas.height);     // background

  ctx.fillStyle = "#2563eb";
  ctx.fillRect(20, 20, 100, 60);                        // filled rectangle
  ctx.strokeStyle = "#b91c1c";
  ctx.lineWidth = 4;
  ctx.strokeRect(140, 20, 100, 60);                     // outline only
  ctx.clearRect(40, 35, 20, 20);                        // cut a hole

  ctx.beginPath();                                      // a path: triangle
  ctx.moveTo(40, 160);
  ctx.lineTo(100, 100);
  ctx.lineTo(160, 160);
  ctx.closePath();
  ctx.fillStyle = "#16a34a";
  ctx.fill();

  ctx.beginPath();                                      // a circle
  ctx.arc(240, 130, 35, 0, Math.PI * 2);
  ctx.strokeStyle = "#7c3aed";
  ctx.stroke();
</script>
```

```reference javascript
canvas.getContext("2d") | The drawing context | const ctx = c.getContext("2d")
fillRect / strokeRect / clearRect | Rectangles | ctx.fillRect(x, y, w, h)
fillStyle / strokeStyle / lineWidth | Colors and line width | ctx.fillStyle = "red"
beginPath / moveTo / lineTo / closePath | Build a path | ctx.moveTo(0, 0); ctx.lineTo(50, 50)
arc(x, y, r, start, end) | Circle or arc (angles in radians) | ctx.arc(50, 50, 20, 0, Math.PI * 2)
fill() / stroke() | Paint the current path | ctx.stroke()
```

:::warning Canvas size versus CSS size
The `width` and `height` attributes set how many pixels the canvas has. Stretching it bigger with CSS makes it blurry. For sharp drawings on high-density screens, multiply the attributes by `devicePixelRatio` and scale the context.
:::

```exercise javascript
? Get the 2D drawing context of canvas
const ctx = canvas.getContext("___");
= 2d
```

```quiz
? Which call starts a new path so earlier shapes are not repainted?
* beginPath()
- clearRect()
- closePath()
```

# @lesson canvas-text-images
title: Text, gradients and transforms on Canvas
summary: fillText, fonts and alignment, gradients, shadows, save/restore and rotate.
---
```try html
<canvas id="c" width="340" height="190" style="border:1px solid #ccc; max-width:100%"></canvas>
<script>
  const ctx = document.getElementById("c").getContext("2d");

  const g = ctx.createLinearGradient(0, 0, 340, 0);
  g.addColorStop(0, "#312e81");
  g.addColorStop(1, "#0e7490");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 340, 190);

  ctx.font = "bold 28px system-ui, sans-serif";
  ctx.fillStyle = "#fff";
  ctx.textAlign = "center";
  ctx.shadowColor = "rgba(0,0,0,.4)";
  ctx.shadowBlur = 8;
  ctx.fillText("Canvas text", 170, 60);

  ctx.shadowBlur = 0;
  ctx.font = "16px system-ui, sans-serif";
  ctx.fillText("مرحبًا", 170, 95);

  for (let i = 0; i < 12; i++) {                 // a ring of rotated bars
    ctx.save();
    ctx.translate(170, 145);
    ctx.rotate((i * Math.PI) / 6);
    ctx.fillStyle = `hsl(${i * 30}, 80%, 65%)`;
    ctx.fillRect(18, -3, 22, 6);
    ctx.restore();
  }
</script>
```

```reference javascript
ctx.font / textAlign / textBaseline | Text settings | ctx.font = "20px sans-serif"
fillText / strokeText | Draw text | ctx.fillText("Hi", 10, 30)
createLinearGradient / createRadialGradient | Gradients | g.addColorStop(0, "red")
shadowColor / shadowBlur | Shadows | ctx.shadowBlur = 10
save() / restore() | Remember / bring back the settings | ctx.save(); ...; ctx.restore()
translate / rotate / scale | Transform what follows | ctx.rotate(Math.PI / 4)
drawImage(img, x, y, w, h) | Draw an image | ctx.drawImage(img, 0, 0)
```

:::tip save and restore
Transforms add up. Calling `save()` before and `restore()` after each transformed drawing keeps the next drawing from inheriting the rotation, colors and shadows.
:::

```exercise javascript
? Draw the text "Done" at (20, 40)
ctx.___("Done", 20, 40);
= fillText
```

```quiz
? What do save() and restore() keep track of?
* The drawing settings such as transforms, colors and shadows
- The pixels on the canvas
- The canvas size
```

# @lesson canvas-animation
title: Animation with requestAnimationFrame
summary: The animation loop, moving objects, bouncing and frame timing.
---
Animation on a canvas means: clear, update positions, draw, and repeat about 60 times a second. `requestAnimationFrame` calls your function before each screen refresh.

```try html
<canvas id="c" width="340" height="190" style="border:1px solid #ccc; max-width:100%; background:#0f172a"></canvas>
<script>
  const canvas = document.getElementById("c");
  const ctx = canvas.getContext("2d");
  const balls = Array.from({ length: 12 }, (_, i) => ({
    x: 30 + i * 24, y: 40 + (i % 4) * 30, r: 8 + (i % 3) * 3,
    vx: (i % 2 ? 1 : -1) * (60 + i * 8), vy: 50 + i * 10,          // pixels per second
    color: `hsl(${i * 30}, 85%, 60%)`,
  }));

  let last = performance.now();
  function frame(now) {
    const dt = Math.min((now - last) / 1000, 0.05);   // seconds since the previous frame
    last = now;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const b of balls) {
      b.x += b.vx * dt;
      b.y += b.vy * dt;
      if (b.x < b.r || b.x > canvas.width - b.r) b.vx *= -1;     // bounce off the walls
      if (b.y < b.r || b.y > canvas.height - b.r) b.vy *= -1;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.fillStyle = b.color;
      ctx.fill();
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
</script>
```

:::tip Move by time, not by frames
Screens refresh at 60, 120 or 144 times a second. Multiplying speeds by the time since the last frame (`dt`) keeps the animation the same speed on every screen.
:::

```reference javascript
requestAnimationFrame(fn) | Call fn before the next repaint | requestAnimationFrame(frame)
performance.now() | Precise time in ms | const t = performance.now()
clearRect(0, 0, w, h) | Clear the canvas each frame | ctx.clearRect(0, 0, c.width, c.height)
cancelAnimationFrame(id) | Stop the loop | cancelAnimationFrame(id)
```

```exercise javascript
? Ask the browser to call frame before the next repaint
___(frame);
= requestAnimationFrame
```

```quiz
? Why does the loop multiply the speed by dt?
* So the animation runs at the same speed on screens with different refresh rates
- To make the balls bigger
- Because canvas needs it to clear
```

# @lesson canvas-interactive
title: Project: a drawing pad
summary: Mouse and touch input with pointer events, colors, and saving the image.
---
```try html
<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:8px">
  <input type="color" id="color" value="#4338ca" aria-label="Color">
  <input type="range" id="size" min="2" max="30" value="6" aria-label="Brush size">
  <button id="clear">Clear</button>
  <button id="save">Show as image</button>
</div>
<canvas id="pad" width="340" height="200" style="border:1px solid #ccc; touch-action:none; max-width:100%"></canvas>
<p><img id="out" alt="" style="max-width:120px; border:1px solid #eee"></p>
<script>
  const pad = document.getElementById("pad");
  const ctx = pad.getContext("2d");
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  let drawing = false;

  function pos(e) {
    const r = pad.getBoundingClientRect();       // convert page position to canvas pixels
    return [(e.clientX - r.left) * (pad.width / r.width), (e.clientY - r.top) * (pad.height / r.height)];
  }
  pad.addEventListener("pointerdown", (e) => {
    drawing = true;
    pad.setPointerCapture(e.pointerId);
    ctx.beginPath();
    ctx.moveTo(...pos(e));
  });
  pad.addEventListener("pointermove", (e) => {
    if (!drawing) return;
    ctx.strokeStyle = document.getElementById("color").value;
    ctx.lineWidth = document.getElementById("size").value;
    ctx.lineTo(...pos(e));
    ctx.stroke();
  });
  pad.addEventListener("pointerup", () => (drawing = false));
  document.getElementById("clear").onclick = () => ctx.clearRect(0, 0, pad.width, pad.height);
  document.getElementById("save").onclick = () => (document.getElementById("out").src = pad.toDataURL("image/png"));

  ctx.font = "14px system-ui, sans-serif";
  ctx.fillStyle = "#94a3b8";
  ctx.fillText("Draw here with the mouse or your finger", 20, 25);
</script>
```

- **Pointer events** (`pointerdown`, `pointermove`, `pointerup`) handle mouse, pen and touch with one set of code.
- `touch-action: none` stops the page from scrolling while you draw on a phone.
- `toDataURL("image/png")` turns the drawing into an image you can show, download or upload.

```quiz
? Which events work for mouse, pen and touch with the same code?
* Pointer events
- Click events only
- Keyboard events
```

# @lesson gfx-reference
title: Graphics quick reference
summary: The most used SVG elements and Canvas calls, and how to choose between them.
---
```reference html
<svg viewBox width> | SVG container that scales | <svg viewBox="0 0 100 100" width="100%">
<rect> <circle> <ellipse> <line> | Basic shapes | <circle cx="50" cy="50" r="40"/>
<polyline> <polygon> <path d> | Lines and any shape | <path d="M0 0 L50 50 Z"/>
fill / stroke / opacity | Painting | fill="none" stroke="#333"
<g transform> / <defs> / url(#id) | Group, reuse, gradients | fill="url(#grad)"
<text> / <title> | Text and accessible names | <title>Sales chart</title>
document.createElementNS(svgNS, tag) | Create SVG with JavaScript | createElementNS("http://www.w3.org/2000/svg", "rect")
```

```reference javascript
getContext("2d") | Canvas context | const ctx = canvas.getContext("2d")
fillRect / arc / beginPath / lineTo | Shapes | ctx.arc(x, y, r, 0, Math.PI * 2)
fillStyle / strokeStyle / lineWidth | Colors and lines | ctx.fillStyle = "#4338ca"
fillText / font / textAlign | Text | ctx.fillText("Hi", 10, 20)
save / restore / translate / rotate | Transforms | ctx.save(); ctx.rotate(a); ctx.restore()
requestAnimationFrame | Animation loop | requestAnimationFrame(frame)
pointerdown / pointermove | Input | canvas.addEventListener("pointermove", draw)
toDataURL | Export as an image | canvas.toDataURL("image/png")
```

:::tip Which one should I use?
Use **SVG** for things people read and click: icons, logos, diagrams and charts with up to a few thousand shapes. Use **Canvas** for many moving objects, pixel effects and games. For 3D, look at WebGL libraries such as three.js.
:::

```quiz
? Which is the better choice for a company logo used at many sizes?
* SVG
- Canvas
- A tiny PNG scaled up
```
