# @lesson howto-intro
title: بناء مكونات الواجهة
summary: كيف تعمل هذه الدورة، والطبقات الثلاث لكل مكوّن.
---
معظم المواقع مبنية من نفس القطع: تبويبات، وقوائم، ونوافذ حوار، وإشعارات، وشرائح عرض، ونماذج. تبني هذه الدورة كل قطعة من الصفر بـ **HTML** للبنية و **CSS** للشكل و **JavaScript** للسلوك، لتفهم ما تفعله أطر العمل والمكتبات نيابة عنك.

كل مكوّن يتبع ثلاث قواعد:

1. **ابدأ بعنصر HTML المناسب.** الزر `<button>` يستقبل التركيز ويعمل بلوحة المفاتيح مجانًا، أما `<div>` مع معالج نقر فلا.
2. **احفظ الحالة في خصائص** مثل `aria-expanded` أو `hidden` أو صنف، واجعل CSS تستجيب لها.
3. **اجعله يعمل بلوحة المفاتيح وقارئات الشاشة**، لا بالفأرة فقط.

```try html ui
<style>
  .counter { display: inline-flex; align-items: center; gap: 8px; font: 16px system-ui, sans-serif; }
  .counter button { width: 36px; height: 36px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; font-size: 18px; cursor: pointer; }
  .counter button:focus-visible { outline: 3px solid #4338ca; outline-offset: 2px; }
  .counter output { min-width: 2ch; text-align: center; font-weight: bold; }
</style>
<div class="counter">
  <button type="button" aria-label="إنقاص">−</button>
  <output aria-live="polite">0</output>
  <button type="button" aria-label="زيادة">+</button>
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

جرّبه بلوحة المفاتيح: اضغط **Tab** للوصول إلى زر، ثم **Enter** أو **Space** للضغط عليه. الأزرار الحقيقية تعطيك هذا مجانًا.

```quiz
? لماذا نستخدم <button> بدل <div> قابل للنقر؟
* لأن الزر يستقبل التركيز ويعمل بلوحة المفاتيح وقارئات الشاشة تلقائيًا
- لأن div لا يقبل معالج نقر
- لأن الأزرار أسرع في التحميل

? تجعل الخاصية aria-live="polite" قارئات الشاشة تعلن تغييرات العنصر.
= true
```

# @lesson howto-tabs
title: التبويبات
summary: تبويبات سهلة الوصول بالأدوار و aria-selected والتنقل بالأسهم.
---
```try html ui
<style>
  .tabs [role="tablist"] { display: flex; gap: 4px; border-bottom: 2px solid #e2e8f0; }
  .tabs [role="tab"] { border: 0; background: none; padding: 8px 14px; font: 600 15px system-ui, sans-serif; color: #64748b; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; }
  .tabs [role="tab"][aria-selected="true"] { color: #4338ca; border-bottom-color: #4338ca; }
  .tabs [role="tabpanel"] { padding: 14px 4px; font: 15px/1.6 system-ui, sans-serif; }
</style>
<div class="tabs">
  <div role="tablist" aria-label="الدورة">
    <button role="tab" id="t1" aria-controls="p1" aria-selected="true">نظرة عامة</button>
    <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">الدروس</button>
    <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">التقييمات</button>
  </div>
  <div role="tabpanel" id="p1" aria-labelledby="t1">دورة لمدة 6 أسابيع عن الجداول الحسابية للفرق.</div>
  <div role="tabpanel" id="p2" aria-labelledby="t2" hidden>1. الخلايا · 2. المعادلات · 3. الرسوم</div>
  <div role="tabpanel" id="p3" aria-labelledby="t3" hidden>★★★★★ "واضحة وعملية."</div>
</div>
<script>
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function select(tab) {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute("aria-selected", on);
      t.tabIndex = on ? 0 : -1;                       // التبويب النشط فقط ضمن ترتيب Tab
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    }
    tab.focus();
  }
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (e) => {
      const step = { ArrowRight: -1, ArrowLeft: 1 }[e.key];
      if (step) select(tabs[(i + step + tabs.length) % tabs.length]);   // الأسهم تتنقل بين التبويبات
    });
  });
</script>
```

```reference html
role="tablist" / "tab" / "tabpanel" | تعريف كل جزء للتقنيات المساعدة | <div role="tablist">
aria-selected="true" | التبويب النشط | <button role="tab" aria-selected="true">
aria-controls / aria-labelledby | ربط التبويبات باللوحات | aria-controls="p1"
hidden | إخفاء اللوحات غير النشطة | <div role="tabpanel" hidden>
tabindex="-1" | إخراجه من ترتيب Tab (الأسهم تتنقل بدلًا منه) | t.tabIndex = -1
```

```exercise html
? علّم التبويب النشط لقارئات الشاشة
<button role="tab" ___="true">Overview</button>
= aria-selected
```

```quiz
? أي المفاتيح تتنقل عادة بين التبويبات في قائمة تبويبات سهلة الوصول؟
* مفاتيح الأسهم
- Page Up و Page Down
- الفأرة فقط
```

# @lesson howto-accordion
title: القوائم القابلة للطي (الأكورديون)
summary: details و summary مجانًا، وأكورديون يسمح بفتح عنصر واحد فقط.
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
  <summary>كم مدة الدورة؟</summary>
  <p>ستة أسابيع، نحو ساعتين أسبوعيًا.</p>
</details>
<details name="faq">
  <summary>هل أحصل على شهادة؟</summary>
  <p>نعم، بعد اجتياز الاختبار النهائي.</p>
</details>
<details name="faq">
  <summary>هل أستطيع الدراسة من الجوال؟</summary>
  <p>نعم، كل الدروس تعمل على الشاشات الصغيرة.</p>
</details>
```

- `<details>` و `<summary>` يعطيانك أكورديون **بلا JavaScript**: يفتح بالنقر أو Enter أو Space ويُعلن بشكل صحيح.
- إعطاء عدة عناصر `<details>` نفس الاسم `name` يجعلها **مجموعة حصرية**: فتح واحد يغلق الباقي (مدعوم في المتصفحات الحالية).

:::tip الأكورديون المخصص
إذا بنيته بأزرار بدلًا من ذلك فاستخدم `<button aria-expanded="false" aria-controls="panel-id">`، وبدّل `aria-expanded` وخاصية `hidden` للوحة في معالج النقر.
:::

```exercise html
? أي عنصر يحمل العنوان الظاهر دائمًا في كتلة details؟
<details><___>Shipping</summary><p>3 to 5 days.</p></details>
= summary
```

```quiz
? ماذا يحدث عندما تشترك عدة عناصر details في نفس الاسم name؟
* يمكن فتح واحد منها فقط في كل مرة
- تنفتح كلها معًا
- تُعاد تحميل الصفحة
```

# @lesson howto-modal
title: نوافذ الحوار
summary: عنصر dialog و showModal والتركيز والإغلاق بـ Escape وإرجاع قيمة.
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

<button id="open">حذف الحساب…</button>
<p id="result"></p>

<dialog id="confirm" aria-labelledby="confirm-title">
  <form method="dialog">
    <h2 id="confirm-title">حذف حسابك؟</h2>
    <p>سيحذف هذا دوراتك وشهاداتك، ولا يمكن التراجع عنه.</p>
    <div class="actions">
      <button value="cancel" autofocus>إلغاء</button>
      <button value="delete" class="danger">حذف</button>
    </div>
  </form>
</dialog>

<script>
  const dialog = document.getElementById("confirm");
  document.getElementById("open").addEventListener("click", () => dialog.showModal());
  dialog.addEventListener("close", () => {
    document.getElementById("result").textContent = "اخترت: " + dialog.returnValue;
  });
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close("cancel"); });   // النقر خارج النافذة
</script>
```

تعطيك `showModal()` الكثير مجانًا: الخلفية المعتمة، وإبقاء التركيز داخل النافذة، والإغلاق بـ **Escape**، وإعادة التركيز للزر الذي فتحها. والنموذج `<form method="dialog">` يغلق النافذة ويضع قيمة `value` للزر المضغوط في `dialog.returnValue`.

```reference html
<dialog> | نافذة حوار | <dialog id="d">...</dialog>
dialog.showModal() / show() | فتحها كنافذة مانعة / عادية | d.showModal()
dialog.close(value) | إغلاقها وتحديد returnValue | d.close("ok")
<form method="dialog"> | الأزرار تغلق النافذة | <button value="yes">Yes</button>
::backdrop | تنسيق الخلفية المعتمة | dialog::backdrop { background: #0008; }
autofocus | مكان بدء التركيز | <button autofocus>Cancel</button>
```

```exercise javascript
? افتح النافذة d كنافذة مانعة
d.___();
= showModal
```

```quiz
? لماذا نضع autofocus على زر الإلغاء في تأكيد الحذف؟
* حتى يؤدي الضغط على Enter بالخطأ إلى الإجراء الآمن
- لتكبير الزر
- لأن النوافذ تحتاجها لتفتح
```

# @lesson howto-dropdown
title: القوائم المنسدلة
summary: زر قائمة مع aria-expanded، والإغلاق بالنقر خارجها و Escape.
---
```try html ui
<style>
  .menu { position: relative; display: inline-block; font: 15px system-ui, sans-serif; }
  .menu > button { padding: 8px 14px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
  .menu ul { position: absolute; top: calc(100% + 4px); right: 0; min-width: 180px; margin: 0; padding: 6px; list-style: none; background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; box-shadow: 0 10px 30px rgb(0 0 0 / .12); }
  .menu a { display: block; padding: 7px 10px; border-radius: 6px; color: #0f172a; text-decoration: none; }
  .menu a:hover, .menu a:focus { background: #eef2ff; outline: none; }
</style>

<div class="menu">
  <button aria-expanded="false" aria-controls="account-menu">حسابي ▾</button>
  <ul id="account-menu" hidden>
    <li><a href="#">ملفي</a></li>
    <li><a href="#">شهاداتي</a></li>
    <li><a href="#">تسجيل الخروج</a></li>
  </ul>
</div>
<p style="margin-top: 140px; font: 14px system-ui; color: #64748b">انقر خارج القائمة أو اضغط Escape لإغلاقها.</p>

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
aria-expanded | إخبار قارئات الشاشة أن القائمة مفتوحة | btn.setAttribute("aria-expanded", true)
element.hidden | الإظهار والإخفاء | list.hidden = !open
e.target.closest(sel) | هل النقر داخل المكوّن؟ | if (!e.target.closest(".menu"))
keydown "Escape" | الإغلاق وإعادة التركيز للزر | button.focus()
position: absolute | وضع القائمة تحت زرها | top: 100%; left: 0
```

:::tip أعد التركيز
عند إغلاق قائمة أو نافذة، أعد تركيز لوحة المفاتيح إلى الزر الذي فتحها، وإلا يفقد مستخدمو لوحة المفاتيح مكانهم في الصفحة.
:::

```exercise html
? أخبر التقنيات المساعدة أن القائمة مغلقة
<button ___="false">Menu</button>
= aria-expanded
```

```quiz
? ماذا يجب أن يحدث عند ضغط Escape في قائمة مفتوحة؟
* تُغلق القائمة ويعود التركيز إلى زرها
- تنتقل الصفحة إلى الأعلى
- لا شيء
```

# @lesson howto-navbar
title: شريط تنقل متجاوب
summary: شريط علوي يتحول إلى زر قائمة على الشاشات الصغيرة.
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
  @media (max-width: 560px) {                     /* الجوال: الروابط تنطوي في قائمة */
    .toggle { display: block; }
    .links { display: none; flex-basis: 100%; flex-direction: column; }
    .bar.open .links { display: flex; }
  }
</style>

<nav class="bar" aria-label="الرئيسي">
  <span class="brand">الأكاديمية</span>
  <button class="toggle" aria-expanded="false" aria-controls="nav-links" aria-label="القائمة">☰</button>
  <ul class="links" id="nav-links">
    <li><a href="#" aria-current="page">الرئيسية</a></li>
    <li><a href="#">الدورات</a></li>
    <li><a href="#">الشهادات</a></li>
    <li><a href="#">المساعدة</a></li>
  </ul>
</nav>
<p style="padding: 16px">صغّر عرض المعاينة (أو افتحها على الجوال) لترى زر القائمة.</p>

<script>
  const bar = document.querySelector(".bar");
  const toggle = document.querySelector(".toggle");
  toggle.addEventListener("click", () => {
    const open = bar.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
</script>
```

- **استعلام وسائط** يخفي الروابط ويُظهر زر ☰ تحت عرض 560px.
- `aria-current="page"` يعلّم الصفحة الحالية، بصريًا (عبر CSS) ولقارئات الشاشة.
- `<nav aria-label>` يتيح لمستخدمي قارئات الشاشة القفز مباشرة إلى التنقل الرئيسي.

```exercise html
? علّم رابط الصفحة الحالية
<a href="/courses" ___="page">Courses</a>
= aria-current
```

```quiz
? ما الذي يجعل الروابط تنطوي في قائمة على الجوال؟
* استعلام وسائط CSS حسب عرض الشاشة
- ملف HTML مختلف للجوال
- المتصفح يفعل ذلك تلقائيًا
```

# @lesson howto-toast
title: إشعارات التنبيه (Toast)
summary: رسائل قصيرة تظهر وتختفي، وتُعلن لقارئات الشاشة.
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

<button data-kind="ok">حفظ</button>
<button data-kind="err">فشل الدفع</button>
<button data-kind="info">معلومة</button>
<div class="toasts" role="status" aria-live="polite"></div>

<script>
  const box = document.querySelector(".toasts");
  const texts = { ok: "تم الحفظ بنجاح", err: "فشل الدفع. حاول مرة أخرى.", info: "درس جديد متاح" };
  function toast(kind, text, ms = 3000) {
    const t = document.createElement("div");
    t.className = "toast " + kind;
    t.textContent = text;                              // textContent: لا تحقن HTML أبدًا
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
role="status" aria-live="polite" | إعلان الرسائل الجديدة دون مقاطعة | <div role="status" aria-live="polite">
role="alert" | إعلان الرسائل العاجلة فورًا | <div role="alert">Error</div>
position: fixed | البقاء في زاوية أثناء التمرير | inset-block-end: 16px
setTimeout + transitionend | التلاشي ثم الحذف | t.remove()
```

:::warning لا تخفِ الأخطاء المهمة في إشعار عابر
الإشعار يختفي بعد ثوانٍ. والأخطاء التي يجب أن يتصرف فيها المستخدم (مثل فشل الدفع) يجب أن تبقى ظاهرة أيضًا بجوار النموذج أو الزر.
:::

```quiz
? أي خاصية تجعل قارئات الشاشة تعلن الإشعار الجديد بلطف؟
* aria-live="polite"
- aria-hidden="true"
- tabindex="0"
```

# @lesson howto-tooltip
title: التلميحات
summary: تلميحات بـ CSS فقط تعمل أيضًا مع تركيز لوحة المفاتيح.
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
  .tip:hover [role="tooltip"], .tip:focus-within [role="tooltip"] { opacity: 1; }   /* الفأرة ولوحة المفاتيح */
  button { padding: 7px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; }
</style>

<span class="tip">
  <button aria-describedby="tip-export">تصدير</button>
  <span role="tooltip" id="tip-export">نزّل نتائجك كملف CSV</span>
</span>
&nbsp;
<span class="tip">
  <button aria-describedby="tip-share">مشاركة</button>
  <span role="tooltip" id="tip-share">انسخ رابط هذه الدورة</span>
</span>
```

- `:focus-within` يُظهر التلميح عندما يصل مستخدم لوحة المفاتيح إلى الزر بـ Tab، لا عند مرور الفأرة فقط.
- `aria-describedby` يجعل قارئات الشاشة تقرأ نص التلميح بعد اسم الزر.

:::tip التلميحات إضافة فقط
الجوال لا يعرف المرور بالفأرة، والتلميحات سهلة التفويت. لا تضع معلومة أساسية في تلميح فقط أبدًا.
:::

```exercise html
? اربط الزر بوصفه
<button ___="tip-1">Save</button>
= aria-describedby
```

```quiz
? لماذا تستخدم CSS الحالة :focus-within إلى جانب :hover؟
* ليرى مستخدمو لوحة المفاتيح التلميح أيضًا
- لجعل التلميح يومض
- لأن :hover لا تعمل مع الأزرار
```

# @lesson howto-carousel
title: شرائح العرض بخاصية scroll snap
summary: شريط شرائح يُسحب بالإصبع مع scroll-snap وأزرار وعدّاد للشرائح.
---
```try html ui
<style>
  body { font: 15px system-ui, sans-serif; }
  .slider { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; padding-bottom: 8px; }
  .slide { flex: 0 0 80%; scroll-snap-align: center; height: 140px; border-radius: 14px; color: #fff; display: grid; place-items: center; font-size: 22px; font-weight: 800; }
  .controls { display: flex; align-items: center; gap: 10px; margin-top: 8px; }
  .controls button { width: 36px; height: 36px; border-radius: 50%; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
</style>

<div class="slider" tabindex="0" aria-label="دورات مميزة">
  <div class="slide" style="background:#4338ca">بايثون</div>
  <div class="slide" style="background:#0e7490">SQL</div>
  <div class="slide" style="background:#be185d">التسويق</div>
  <div class="slide" style="background:#b45309">الإحصاء</div>
</div>
<div class="controls">
  <button aria-label="السابق">›</button>
  <span id="count" aria-live="polite">1 / 4</span>
  <button aria-label="التالي">‹</button>
</div>

<script>
  const slider = document.querySelector(".slider");
  const slides = [...slider.children];
  const [prev, next] = document.querySelectorAll(".controls button");
  const current = () => Math.round(Math.abs(slider.scrollLeft) / Math.abs(slides[1].offsetLeft - slides[0].offsetLeft));
  const go = (i) => slides[Math.max(0, Math.min(slides.length - 1, i))].scrollIntoView({ inline: "center", block: "nearest" });
  prev.addEventListener("click", () => go(current() - 1));
  next.addEventListener("click", () => go(current() + 1));
  slider.addEventListener("scroll", () => (document.getElementById("count").textContent = current() + 1 + " / " + slides.length));
</script>
```

تجعل `scroll-snap-type` المتصفح يتوقف على شريحة بالضبط، ويعمل السحب على الجوال دون أي كود إضافي. والأزرار تستدعي `scrollIntoView` فقط.

```reference css
overflow-x: auto | تمرير أفقي | .slider { overflow-x: auto; }
scroll-snap-type: x mandatory | التوقف على العناصر أثناء التمرير | scroll-snap-type: x mandatory
scroll-snap-align: center | موضع توقف كل عنصر | .slide { scroll-snap-align: start; }
scroll-behavior: smooth | تمرير برمجي سلس | scroll-behavior: smooth
el.scrollIntoView({ inline: "center" }) | التمرير إلى عنصر | slide.scrollIntoView({ inline: "center" })
```

```exercise css
? اجعل الحاوية تتوقف على شرائحها أفقيًا
.slider { scroll-snap-type: ___ mandatory; }
= x
```

```quiz
? لماذا تكون شرائح العرض المبنية على التمرير الأصلي أسهل على الجوال؟
* لأن السحب يعمل دون كود إضافي
- لأنها تحمّل صورًا أكثر
- لأنها تعطّل التمرير
```

# @lesson howto-form
title: التحقق من النماذج
summary: التحقق المدمج، ورسائل خطأ واضحة، وفحص كلمات المرور بـ JavaScript.
---
```try html ui
<style>
  form { display: grid; gap: 10px; max-width: 340px; font: 15px system-ui, sans-serif; }
  label { display: grid; gap: 4px; font-weight: 600; }
  input { padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font: inherit; }
  input:user-invalid { border-color: #b91c1c; }                 /* فقط بعد أن يلمسه المستخدم */
  .error { color: #b91c1c; font-size: 13px; font-weight: 400; min-height: 1em; }
  button { padding: 9px; border: 0; border-radius: 8px; background: #4338ca; color: #fff; font-weight: 700; }
  #done { color: #15803d; }
</style>

<form novalidate>
  <label>البريد الإلكتروني
    <input type="email" name="email" required autocomplete="email" aria-describedby="email-err">
    <span class="error" id="email-err"></span>
  </label>
  <label>كلمة المرور (8 أحرف على الأقل ومعها رقم)
    <input type="password" name="password" required minlength="8" pattern="(?=.*\d).{8,}" autocomplete="new-password" aria-describedby="pw-err">
    <span class="error" id="pw-err"></span>
  </label>
  <label>أعد كتابة كلمة المرور
    <input type="password" name="confirm" required autocomplete="new-password" aria-describedby="cf-err">
    <span class="error" id="cf-err"></span>
  </label>
  <button>إنشاء الحساب</button>
  <p id="done" role="status"></p>
</form>

<script>
  const form = document.querySelector("form");
  const messages = {
    email: (i) => i.validity.valueMissing ? "أدخل بريدك الإلكتروني." : "أدخل بريدًا صحيحًا مثل name@example.com.",
    password: (i) => i.validity.valueMissing ? "اختر كلمة مرور." : "استخدم 8 أحرف أو أكثر ومعها رقم.",
    confirm: (i) => i.validity.valueMissing ? "أعد كتابة كلمة المرور." : "كلمتا المرور غير متطابقتين.",
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
    if (firstBad) return firstBad.focus();          // انقل المستخدم إلى أول مشكلة
    document.getElementById("done").textContent = "تم إنشاء الحساب (تجربة).";
  });
</script>
```

```reference html
required / minlength / pattern | قواعد مدمجة | <input required minlength="8">
type="email" / "number" / "url" | حقول بأنواع لها فحوصها | <input type="email">
input.checkValidity() / validity | فحص حقل بـ JavaScript | if (!input.checkValidity())
setCustomValidity(msg) | قاعدتك الخاصة ("" تعني صحيح) | input.setCustomValidity("")
:user-invalid | التنسيق فقط بعد تفاعل المستخدم | input:user-invalid { border-color: red; }
aria-invalid / aria-describedby | إخبار قارئات الشاشة بالأخطاء | aria-describedby="email-err"
autocomplete | مساعدة المتصفحات ومديري كلمات المرور | autocomplete="new-password"
```

:::danger فحص المتصفح للراحة فقط
يستطيع أي شخص إرسال بيانات لخادمك دون نموذجك. يجب أن يتحقق الخادم من كل شيء مرة أخرى.
:::

```exercise html
? اجعل الحقل إلزاميًا
<input type="email" ___>
= required
```

```quiz
? بعد فشل الإرسال، أين يجب أن يذهب تركيز لوحة المفاتيح؟
* إلى أول حقل فيه خطأ
- إلى أعلى الصفحة
- لا مكان، يبقى على الزر
```

# @lesson howto-dark-mode
title: زر الوضع الداكن
summary: متغيرات CSS و prefers-color-scheme وتذكّر اختيار المستخدم.
---
```try html ui
<style>
  :root { --bg: #ffffff; --text: #0f172a; --card: #f1f5f9; --brand: #4338ca; color-scheme: light; }
  @media (prefers-color-scheme: dark) {                 /* اتبع إعداد النظام... */
    :root:not([data-theme="light"]) { --bg: #0f172a; --text: #e2e8f0; --card: #1e293b; --brand: #a5b4fc; color-scheme: dark; }
  }
  :root[data-theme="dark"] { --bg: #0f172a; --text: #e2e8f0; --card: #1e293b; --brand: #a5b4fc; color-scheme: dark; }   /* ...ما لم يختر المستخدم */
  body { background: var(--bg); color: var(--text); font: 15px system-ui, sans-serif; padding: 16px; transition: background .2s, color .2s; }
  .card { background: var(--card); padding: 14px; border-radius: 12px; }
  .card h3 { color: var(--brand); margin: 0 0 6px; }
  button { padding: 7px 12px; border-radius: 8px; border: 1px solid currentColor; background: none; color: inherit; cursor: pointer; }
</style>

<button id="theme" aria-pressed="false">🌙 الوضع الداكن</button>
<div class="card" style="margin-top: 12px">
  <h3>تقدمك</h3>
  <p>أنجزت 3 من 8 دروس هذا الأسبوع.</p>
</div>

<script>
  const root = document.documentElement;
  const btn = document.getElementById("theme");
  function apply(theme) {
    root.dataset.theme = theme;
    btn.setAttribute("aria-pressed", theme === "dark");
    btn.textContent = theme === "dark" ? "☀️ الوضع الفاتح" : "🌙 الوضع الداكن";
  }
  let saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}   // قد يكون التخزين محظورًا
  apply(saved || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  btn.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    apply(theme);
    try { localStorage.setItem("theme", theme); } catch (e) {}
  });
</script>
```

```reference css
--name: value / var(--name) | متغيرات CSS للألوان | color: var(--text);
@media (prefers-color-scheme: dark) | إعداد الوضع الداكن في النظام | @media (prefers-color-scheme: dark) { }
:root[data-theme="dark"] | اختيار المستخدم يتقدم | <html data-theme="dark">
color-scheme: dark | عناصر نماذج وأشرطة تمرير داكنة | :root { color-scheme: dark; }
localStorage | تذكر الاختيار في هذا المتصفح | localStorage.setItem("theme", "dark")
```

```exercise css
? استخدم المتغير المسمى text للون
body { color: ___(--text); }
= var
```

```quiz
? لماذا نعرّف الألوان كمتغيرات CSS للوضع الداكن؟
* ليكفي تغيير قيم قليلة عند تبديل السمة
- لأن الوضع الداكن يحتاج JavaScript لكل عنصر
- لتسريع تحميل الصفحة
```

# @lesson howto-filter
title: البحث في قائمة وتصفيتها
summary: التصفية أثناء الكتابة، وعرض العدد، والتعامل مع "لا نتائج".
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

<input type="search" placeholder="ابحث في الدورات" aria-label="ابحث في الدورات">
<div class="chips" role="group" aria-label="المستوى">
  <button aria-pressed="true" data-level="all">الكل</button>
  <button aria-pressed="false" data-level="Beginner">مبتدئ</button>
  <button aria-pressed="false" data-level="Advanced">متقدم</button>
</div>
<p id="count" role="status"></p>
<ul id="list"></ul>

<script>
  const courses = [
    ["أساسيات بايثون", "Beginner"], ["SQL للمحللين", "Beginner"], ["تعلّم الآلة", "Advanced"],
    ["أداء PostgreSQL", "Advanced"], ["معادلات Excel", "Beginner"], ["الإحصاء ببايثون", "Advanced"],
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
      if (i >= 0) {                                         // أبرز التطابق بأمان دون innerHTML
        const mark = document.createElement("mark");
        mark.textContent = name.slice(i, i + q.length);
        title.append(name.slice(0, i), mark, name.slice(i + q.length));
      } else title.textContent = name;
      const small = document.createElement("small");
      small.textContent = lv === "Beginner" ? "مبتدئ" : "متقدم";
      li.append(title, small);
      return li;
    }));
    count.textContent = shown.length ? "عدد الدورات: " + shown.length : "لا توجد دورات مطابقة. جرّب كلمة أقصر.";
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

- مربع البحث يصفّي أثناء الكتابة، وأزرار المستوى تضيّق أكثر، ويعمل الاثنان معًا.
- يُبرز التطابق بعنصر `<mark>` مبني من عقد نصية، فلا يمكن لكلمة البحث حقن HTML أبدًا.
- `role="status"` يعلن عدد النتائج لمستخدمي قارئات الشاشة.

```quiz
? لماذا يبني كود الإبراز عناصر بدل استخدام innerHTML؟
* حتى لا يُفسَّر النص الذي يكتبه المستخدم كـ HTML أبدًا
- لأن innerHTML غير مدعومة في القوائم
- لترتيب القائمة تلقائيًا
```

# @lesson howto-reference
title: مرجع مكونات الواجهة السريع
summary: العنصر والخصائص المناسبة لكل مكوّن شائع.
---
| المكوّن | ابدأ بـ | الخصائص الأساسية |
|---|---|---|
| زر | `<button type="button">` | `aria-label` لأزرار الأيقونات |
| تبويبات | `role="tablist"` و `tab` و `tabpanel` | `aria-selected` و `aria-controls` والأسهم |
| أكورديون | `<details>` / `<summary>` | `name` للمجموعات الحصرية |
| نافذة حوار | `<dialog>` + `showModal()` | `<form method="dialog">` و `autofocus` |
| قائمة منسدلة | `<button>` + قائمة | `aria-expanded` و Escape والنقر بالخارج |
| تنقل | `<nav aria-label>` | `aria-current="page"` واستعلام وسائط |
| إشعار | حاوية بـ `role="status"` | `aria-live="polite"` |
| تلميح | `role="tooltip"` | `aria-describedby` و `:focus-within` |
| شرائح عرض | حاوية تمرير | `scroll-snap-type` و `scrollIntoView` |
| نموذج | `<label>` + `<input>` | `required` و `aria-invalid` و `aria-describedby` |

```reference html
:focus-visible | إظهار حلقة التركيز لمستخدمي لوحة المفاتيح | button:focus-visible { outline: 3px solid; }
hidden | الإخفاء عن الجميع | panel.hidden = true
aria-label / aria-labelledby | إعطاء العنصر اسمًا | <button aria-label="Close">×</button>
aria-expanded / aria-pressed / aria-selected | حالة عناصر التبديل | btn.setAttribute("aria-expanded", true)
aria-live / role="status" | إعلان التغييرات | <p role="status"></p>
textContent | وضع نص المستخدم في الصفحة بأمان | el.textContent = name
```

:::tip الخطوة التالية
خذ مكوّنًا تحتاجه في عملك، وابنه بهذه الطريقة، واختبره بلوحة المفاتيح فقط (Tab و Shift+Tab و Enter و Space و Escape والأسهم). ثم انظر كيف تنفّذ مكتبة مثل Headless UI أو Radix النمط نفسه.
:::

```quiz
? ما أسرع طريقة لتختبر بنفسك سهولة الوصول لمكوّن؟
* استخدامه بلوحة المفاتيح فقط
- النظر إليه على شاشة كبيرة
- عدّ أسطر JavaScript
```
