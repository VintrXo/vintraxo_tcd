# @lesson gfx-intro
title: الرسوم على الويب
summary: SVG و Canvas، وما يناسب كلًا منهما، وأول رسمة بالاثنين.
---
للمتصفحات طريقتان مدمجتان للرسم:

| | SVG | Canvas |
|---|---|---|
| ما هو | أشكال مكتوبة كوسوم تشبه HTML | سطح من البكسلات ترسم عليه بـ JavaScript |
| يكبر دون أن يتشوش | نعم (متجهي) | لا (بكسلات) |
| كل شكل عنصر مستقل | نعم: نسّقه بـ CSS وانقر عليه | لا: بعد رسمه يصبح مجرد بكسلات |
| الأنسب لـ | الأيقونات والشعارات والمخططات والرسوم البيانية | الألعاب والحركة بعناصر كثيرة وتحرير الصور |

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

الصورتان متشابهتان، لكن صناعتهما مختلفة تمامًا: SVG عنصران داخل الصفحة، و Canvas شبكة بكسلات رسمها الكود.

:::info الإحداثيات
في الاثنين تكون النقطة `(0, 0)` في **الزاوية العليا اليسرى**، ويزيد `x` نحو اليمين ويزيد `y` **نحو الأسفل**.
:::

```quiz
? أي تقنية تُبقي كل شكل عنصرًا يمكن تنسيقه بـ CSS؟
* SVG
- Canvas
- كلتاهما

? في SVG و Canvas تزيد قيمة y نحو الأسفل.
= true
```

# @lesson svg-shapes
title: أشكال SVG الأساسية
summary: rect و circle و ellipse و line و polyline و polygon و viewBox.
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

- `viewBox="0 0 300 160"` يحدد نظام إحداثيات الرسمة نفسها. ومع `width="100%"` تكبر الرسمة وتصغر حسب الصفحة دون فقد الجودة.
- `fill` يلوّن الداخل، و `stroke` و `stroke-width` يرسمان الحد الخارجي.
- `polygon` مثل `polyline` لكنه يغلق الشكل تلقائيًا.

```reference html
<rect x y width height rx> | مستطيل (rx تدوّر الزوايا) | <rect x="0" y="0" width="50" height="20" rx="4"/>
<circle cx cy r> | دائرة | <circle cx="50" cy="50" r="40"/>
<ellipse cx cy rx ry> | قطع ناقص | <ellipse cx="50" cy="30" rx="40" ry="20"/>
<line x1 y1 x2 y2> | خط مستقيم | <line x1="0" y1="0" x2="100" y2="50" stroke="black"/>
<polyline points> / <polygon points> | خطوط متصلة مفتوحة / مغلقة | <polygon points="50,0 100,100 0,100"/>
viewBox="minx miny w h" | نظام الإحداثيات الداخلي | <svg viewBox="0 0 100 100">
fill / stroke / stroke-width | الألوان والحد | fill="none" stroke="red"
```

```exercise html
? ارسم دائرة نصف قطرها 30
<circle cx="50" cy="50" ___="30" />
= r
```

```quiz
? ماذا يتيح viewBox لرسمة SVG؟
* تغيير حجمها لأي مقاس دون تشوش
- تحميل الصور أسرع
- الحركة تلقائيًا
```

# @lesson svg-paths
title: المسارات في SVG
summary: عنصر path وأوامره: التحريك والخطوط والمنحنيات والأقواس.
---
يستطيع `<path>` رسم أي شكل. والخاصية `d` قائمة أوامر: حرف يتبعه أرقام.

```try html
<svg viewBox="0 0 320 170" width="100%" style="max-width:480px; border:1px solid #ddd">
  <!-- بيت: M = تحريك، L = خط، Z = إغلاق -->
  <path d="M 20 90 L 70 40 L 120 90 Z" fill="#fca5a5" />
  <path d="M 30 90 L 30 150 L 110 150 L 110 90" fill="#fde68a" stroke="#92400e" />

  <!-- موجة: Q = منحنى بنقطة تحكم واحدة -->
  <path d="M 140 100 Q 165 40 190 100 Q 215 160 240 100" fill="none" stroke="#2563eb" stroke-width="4" />

  <!-- قلب: C = منحنيات بنقطتي تحكم -->
  <path d="M 285 75 C 285 55 260 50 260 70 C 260 85 285 100 285 110 C 285 100 310 85 310 70 C 310 50 285 55 285 75 Z" fill="#e11d48" />

  <!-- قوس: A = قوس من قطع ناقص، هنا نصف دائرة -->
  <path d="M 150 150 A 40 40 0 0 1 230 150" fill="none" stroke="#15803d" stroke-width="4" />
</svg>
```

| الأمر | المعنى |
|---|---|
| `M x y` | تحريك القلم دون رسم |
| `L x y` | خط مستقيم إلى النقطة |
| `H x` / `V y` | خط أفقي / رأسي |
| `Q cx cy x y` | منحنى بنقطة تحكم واحدة |
| `C c1x c1y c2x c2y x y` | منحنى بنقطتي تحكم |
| `A rx ry rot large sweep x y` | قوس من قطع ناقص |
| `Z` | إغلاق الشكل إلى نقطة البداية |

الحروف الصغيرة (`m` و `l` و `c`...) تستخدم مواضع **نسبية** من النقطة الحالية بدل المواضع المطلقة.

:::tip نادرًا ما تكتب المسارات الطويلة يدويًا
أدوات التصميم مثل Figma و Inkscape و Illustrator تصدّر مسارات SVG. ومعرفة الأوامر تساعدك على قراءة ما تنتجه وتنظيفه وتحريكه.
:::

```exercise html
? أي أمر في المسار يغلق الشكل؟
<path d="M 0 0 L 50 0 L 25 40 ___" />
= Z | z
```

```quiz
? ماذا يفعل الأمر M في المسار؟
* يحرّك القلم إلى نقطة دون رسم
- يرسم دائرة
- يعكس الشكل
```

# @lesson svg-style
title: تنسيق SVG بـ CSS والتدرجات والنصوص
summary: الأصناف، وتأثيرات المرور، والتدرجات الخطية والدائرية، والنص.
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
  <text class="label" x="175" y="140">مرّر الفأرة على الأعمدة</text>
</svg>
```

- عناصر SVG تقبل أصناف CSS، فيعمل `:hover` والانتقالات والوضع الداكن كما مع HTML.
- الأشياء المعاد استخدامها مثل التدرجات توضع داخل `<defs>` وتُستخدم بـ `fill="url(#id)"`.
- `<text>` يرسم نصًا يبقى قابلًا للتحديد والبحث.

```reference html
class / <style> | تنسيق SVG بـ CSS | .bar:hover { fill: orange; }
<defs> | تعريفات تُستخدم لاحقًا | <defs><linearGradient id="g">...</defs>
<linearGradient> / <radialGradient> | التدرجات | fill="url(#g)"
<stop offset stop-color> | نقطة لون في التدرج | <stop offset="1" stop-color="#fff"/>
<text x y> | نص | <text x="10" y="20">Hi</text>
<g> | تجميع الأشكال لتحريكها أو تنسيقها معًا | <g fill="red">...</g>
```

```exercise html
? لوّن شكلًا بالتدرج الذي معرّفه sky
<rect width="100" height="50" fill="___(#sky)" />
= url
```

```quiz
? أين توضع عادة التدرجات التي ستعيد الأشكال استخدامها؟
* داخل <defs>
- داخل <text>
- في الخاصية stroke
```

# @lesson svg-animate
title: التحويلات والحركة في SVG
summary: translate و rotate و scale والتجميع وحركات CSS.
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
transform="translate(x y)" | تحريك | <g transform="translate(20 10)">
rotate(deg) / scale(s) | تدوير / تغيير الحجم | transform="rotate(45)"
transform-origin | النقطة التي يدور حولها (CSS) | transform-origin: 50px 50px
@keyframes + animation | حركة CSS | animation: spin 3s linear infinite
opacity | الشفافية من 0 إلى 1 | opacity="0.5"
```

:::tip احترم تقليل الحركة
بعض الناس يشعرون بالدوار من الحركة. ضع الحركات الزخرفية داخل `@media (prefers-reduced-motion: no-preference) { ... }` لتعمل فقط عند من لم يطلب من نظامه تقليل الحركة.
:::

```exercise html
? حرّك مجموعة 50 لليمين و 20 للأسفل
<g transform="___(50 20)">
= translate
```

```quiz
? أي خاصية CSS تحدد النقطة التي يدور حولها الشكل؟
* transform-origin
- rotate-center
- viewBox
```

# @lesson svg-chart
title: مشروع: رسم بياني بالأعمدة في SVG مع JavaScript
summary: بناء رسم بياني من البيانات وسهل الوصول باستخدام createElementNS.
---
يجب إنشاء عناصر SVG بـ `document.createElementNS` ومساحة أسماء SVG. والرسم التالي مبني من مصفوفة، فتغيير البيانات يعيد رسمه.

```try html
<svg id="chart" viewBox="0 0 420 220" width="100%" style="max-width:560px" role="img" aria-labelledby="chart-title">
  <title id="chart-title">المبيعات الشهرية</title>
</svg>
<script>
  const data = [ ["يناير", 120], ["فبراير", 180], ["مارس", 150], ["أبريل", 240], ["مايو", 210], ["يونيو", 280] ];
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
    bar.appendChild(svg.lastChild);           // تلميح عند المرور
    add("text", { x: x + (barW - 12) / 2, y: H - pad + 16, "text-anchor": "middle", "font-size": 12 }, label);
    add("text", { x: x + (barW - 12) / 2, y: H - pad - h - 5, "text-anchor": "middle", "font-size": 11, fill: "#475569" }, value);
  });
</script>
```

:::tip اجعل الرسوم البيانية سهلة الوصول
`role="img"` مع `<title>` يعطي قارئات الشاشة اسمًا للرسم، و `<title>` داخل كل عمود يُظهر تلميحًا عند المرور. وللأرقام المهمة اعرضها أيضًا كنص أو جدول.
:::

```quiz
? لماذا يستخدم الكود createElementNS بدل createElement؟
* لأن عناصر SVG تنتمي لمساحة أسماء SVG ويجب إنشاؤها فيها
- لأن createElement أبطأ
- لأن createElementNS تضيف الألوان تلقائيًا
```

# @lesson canvas-basics
title: أساسيات Canvas
summary: سياق الرسم ثنائي الأبعاد، والمستطيلات والألوان والخطوط والمسارات.
---
```try html
<canvas id="c" width="320" height="180" style="border:1px solid #ccc; max-width:100%"></canvas>
<script>
  const canvas = document.getElementById("c");
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#e0f2fe";
  ctx.fillRect(0, 0, canvas.width, canvas.height);     // الخلفية

  ctx.fillStyle = "#2563eb";
  ctx.fillRect(20, 20, 100, 60);                        // مستطيل ممتلئ
  ctx.strokeStyle = "#b91c1c";
  ctx.lineWidth = 4;
  ctx.strokeRect(140, 20, 100, 60);                     // الحد فقط
  ctx.clearRect(40, 35, 20, 20);                        // قص فتحة

  ctx.beginPath();                                      // مسار: مثلث
  ctx.moveTo(40, 160);
  ctx.lineTo(100, 100);
  ctx.lineTo(160, 160);
  ctx.closePath();
  ctx.fillStyle = "#16a34a";
  ctx.fill();

  ctx.beginPath();                                      // دائرة
  ctx.arc(240, 130, 35, 0, Math.PI * 2);
  ctx.strokeStyle = "#7c3aed";
  ctx.stroke();
</script>
```

```reference javascript
canvas.getContext("2d") | سياق الرسم | const ctx = c.getContext("2d")
fillRect / strokeRect / clearRect | المستطيلات | ctx.fillRect(x, y, w, h)
fillStyle / strokeStyle / lineWidth | الألوان وسُمك الخط | ctx.fillStyle = "red"
beginPath / moveTo / lineTo / closePath | بناء مسار | ctx.moveTo(0, 0); ctx.lineTo(50, 50)
arc(x, y, r, start, end) | دائرة أو قوس (الزوايا بالراديان) | ctx.arc(50, 50, 20, 0, Math.PI * 2)
fill() / stroke() | تلوين المسار الحالي | ctx.stroke()
```

:::warning حجم Canvas مقابل حجم CSS
الخاصيتان `width` و `height` تحددان عدد بكسلات الرسمة، وتكبيرها بـ CSS يجعلها مشوشة. وللرسم الحاد على الشاشات عالية الكثافة اضرب الخاصيتين في `devicePixelRatio` وغيّر مقياس السياق.
:::

```exercise javascript
? احصل على سياق الرسم ثنائي الأبعاد من canvas
const ctx = canvas.getContext("___");
= 2d
```

```quiz
? أي استدعاء يبدأ مسارًا جديدًا حتى لا تُعاد الأشكال السابقة؟
* beginPath()
- clearRect()
- closePath()
```

# @lesson canvas-text-images
title: النصوص والتدرجات والتحويلات في Canvas
summary: fillText والخطوط والمحاذاة والتدرجات والظلال و save/restore والتدوير.
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
  ctx.fillText("نص على Canvas", 170, 60);

  ctx.shadowBlur = 0;
  ctx.font = "16px system-ui, sans-serif";
  ctx.fillText("Hello", 170, 95);

  for (let i = 0; i < 12; i++) {                 // حلقة من أعمدة مدوّرة
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
ctx.font / textAlign / textBaseline | إعدادات النص | ctx.font = "20px sans-serif"
fillText / strokeText | رسم النص | ctx.fillText("Hi", 10, 30)
createLinearGradient / createRadialGradient | التدرجات | g.addColorStop(0, "red")
shadowColor / shadowBlur | الظلال | ctx.shadowBlur = 10
save() / restore() | حفظ الإعدادات / استرجاعها | ctx.save(); ...; ctx.restore()
translate / rotate / scale | تحويل ما يُرسم بعدها | ctx.rotate(Math.PI / 4)
drawImage(img, x, y, w, h) | رسم صورة | ctx.drawImage(img, 0, 0)
```

:::tip save و restore
التحويلات تتراكم. استدعاء `save()` قبل كل رسمة محوّلة و `restore()` بعدها يمنع الرسمة التالية من وراثة التدوير والألوان والظلال.
:::

```exercise javascript
? ارسم النص "Done" عند النقطة (20, 40)
ctx.___("Done", 20, 40);
= fillText
```

```quiz
? ماذا تحفظ save() و restore()؟
* إعدادات الرسم مثل التحويلات والألوان والظلال
- بكسلات الرسمة
- حجم Canvas
```

# @lesson canvas-animation
title: الحركة باستخدام requestAnimationFrame
summary: حلقة الحركة، وتحريك العناصر، والارتداد، وتوقيت الإطارات.
---
الحركة على Canvas تعني: امسح، حدّث المواضع، ارسم، وكرر نحو 60 مرة في الثانية. والدالة `requestAnimationFrame` تستدعي دالتك قبل كل تحديث للشاشة.

```try html
<canvas id="c" width="340" height="190" style="border:1px solid #ccc; max-width:100%; background:#0f172a"></canvas>
<script>
  const canvas = document.getElementById("c");
  const ctx = canvas.getContext("2d");
  const balls = Array.from({ length: 12 }, (_, i) => ({
    x: 30 + i * 24, y: 40 + (i % 4) * 30, r: 8 + (i % 3) * 3,
    vx: (i % 2 ? 1 : -1) * (60 + i * 8), vy: 50 + i * 10,          // بكسل في الثانية
    color: `hsl(${i * 30}, 85%, 60%)`,
  }));

  let last = performance.now();
  function frame(now) {
    const dt = Math.min((now - last) / 1000, 0.05);   // الثواني منذ الإطار السابق
    last = now;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const b of balls) {
      b.x += b.vx * dt;
      b.y += b.vy * dt;
      if (b.x < b.r || b.x > canvas.width - b.r) b.vx *= -1;     // ارتداد عن الجدران
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

:::tip حرّك حسب الوقت لا حسب الإطارات
الشاشات تتحدث 60 أو 120 أو 144 مرة في الثانية. وضرب السرعات في الوقت منذ الإطار السابق (`dt`) يجعل الحركة بنفس السرعة على كل الشاشات.
:::

```reference javascript
requestAnimationFrame(fn) | استدعاء fn قبل إعادة الرسم التالية | requestAnimationFrame(frame)
performance.now() | وقت دقيق بالمللي ثانية | const t = performance.now()
clearRect(0, 0, w, h) | مسح الرسمة في كل إطار | ctx.clearRect(0, 0, c.width, c.height)
cancelAnimationFrame(id) | إيقاف الحلقة | cancelAnimationFrame(id)
```

```exercise javascript
? اطلب من المتصفح استدعاء frame قبل إعادة الرسم التالية
___(frame);
= requestAnimationFrame
```

```quiz
? لماذا تضرب الحلقة السرعة في dt؟
* لتعمل الحركة بنفس السرعة على شاشات بمعدلات تحديث مختلفة
- لتكبير الكرات
- لأن Canvas يحتاجها للمسح
```

# @lesson canvas-interactive
title: مشروع: لوحة رسم
summary: إدخال الفأرة واللمس بأحداث المؤشر، والألوان، وحفظ الرسمة كصورة.
---
```try html
<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:8px">
  <input type="color" id="color" value="#4338ca" aria-label="اللون">
  <input type="range" id="size" min="2" max="30" value="6" aria-label="حجم الفرشاة">
  <button id="clear">امسح</button>
  <button id="save">اعرض كصورة</button>
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
    const r = pad.getBoundingClientRect();       // تحويل موضع الصفحة إلى بكسلات Canvas
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
  ctx.fillText("ارسم هنا بالفأرة أو بإصبعك", 20, 25);
</script>
```

- **أحداث المؤشر** (`pointerdown` و `pointermove` و `pointerup`) تتعامل مع الفأرة والقلم واللمس بكود واحد.
- `touch-action: none` يمنع الصفحة من التمرير أثناء الرسم على الجوال.
- `toDataURL("image/png")` يحوّل الرسمة إلى صورة يمكن عرضها أو تنزيلها أو رفعها.

```quiz
? أي أحداث تعمل مع الفأرة والقلم واللمس بنفس الكود؟
* أحداث المؤشر (Pointer events)
- أحداث النقر فقط
- أحداث لوحة المفاتيح
```

# @lesson gfx-reference
title: مرجع الرسوم السريع
summary: أكثر عناصر SVG واستدعاءات Canvas استخدامًا، وكيف تختار بينهما.
---
```reference html
<svg viewBox width> | حاوية SVG قابلة للتحجيم | <svg viewBox="0 0 100 100" width="100%">
<rect> <circle> <ellipse> <line> | الأشكال الأساسية | <circle cx="50" cy="50" r="40"/>
<polyline> <polygon> <path d> | الخطوط وأي شكل | <path d="M0 0 L50 50 Z"/>
fill / stroke / opacity | التلوين | fill="none" stroke="#333"
<g transform> / <defs> / url(#id) | التجميع وإعادة الاستخدام والتدرجات | fill="url(#grad)"
<text> / <title> | النص والأسماء سهلة الوصول | <title>Sales chart</title>
document.createElementNS(svgNS, tag) | إنشاء SVG بـ JavaScript | createElementNS("http://www.w3.org/2000/svg", "rect")
```

```reference javascript
getContext("2d") | سياق Canvas | const ctx = canvas.getContext("2d")
fillRect / arc / beginPath / lineTo | الأشكال | ctx.arc(x, y, r, 0, Math.PI * 2)
fillStyle / strokeStyle / lineWidth | الألوان والخطوط | ctx.fillStyle = "#4338ca"
fillText / font / textAlign | النصوص | ctx.fillText("Hi", 10, 20)
save / restore / translate / rotate | التحويلات | ctx.save(); ctx.rotate(a); ctx.restore()
requestAnimationFrame | حلقة الحركة | requestAnimationFrame(frame)
pointerdown / pointermove | الإدخال | canvas.addEventListener("pointermove", draw)
toDataURL | التصدير كصورة | canvas.toDataURL("image/png")
```

:::tip أيهما أستخدم؟
استخدم **SVG** لما يقرؤه الناس وينقرون عليه: الأيقونات والشعارات والمخططات والرسوم البيانية حتى بضعة آلاف من الأشكال. واستخدم **Canvas** للعناصر المتحركة الكثيرة وتأثيرات البكسل والألعاب. وللرسم ثلاثي الأبعاد انظر مكتبات WebGL مثل three.js.
:::

```quiz
? أيهما الاختيار الأفضل لشعار شركة يُستخدم بمقاسات كثيرة؟
* SVG
- Canvas
- صورة PNG صغيرة مكبّرة
```
