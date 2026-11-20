# @lesson jq-intro
title: مقدمة jQuery
summary: ما هي jQuery، وكيف تضيفها، و $(document).ready.
---
**jQuery** مكتبة JavaScript صغيرة تختصر المهام الشائعة في الصفحة: إيجاد العناصر، والاستجابة للنقرات، وتغيير المحتوى والتنسيق، والحركة، والتواصل مع الخادم. المتصفحات الحديثة تستطيع كل هذا بـ JavaScript العادية، لكن jQuery ما زالت موجودة في عدد ضخم من المواقع، فيستحق أن تعرف قراءتها وكتابتها.

## إضافتها إلى صفحتك

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
```

في هذه الدورة يُضاف هذا السطر لكل مثال تلقائيًا.

```try html jq
<p id="msg">انتظر…</p>
<script>
$(function () {                 // يعمل عندما تجهز الصفحة
  $("#msg").text("مرحبًا من jQuery!");
});
</script>
```

- `$` هي دالة jQuery، و `$("#msg")` تجد العنصر الذي معرّفه `msg`.
- `$(function () { ... })` اختصار لـ `$(document).ready(...)`: ينتظر الكود حتى تكتمل الصفحة.
- `.text(...)` تضع نص العنصر الذي وُجد.

```quiz
? ماذا يحدد $("#msg")؟
* العنصر الذي معرّفه msg
- كل عنصر له الصنف msg
- كل وسوم <msg>

? يجب تحميل كود jQuery بعد ملف jQuery نفسه.
= true
```

# @lesson jq-selectors
title: المحددات
summary: إيجاد العناصر بمحددات CSS ومرشحات jQuery.
---
تستخدم jQuery نفس محددات CSS مع بعض الإضافات.

```try html jq
<ul>
  <li>شاي</li>
  <li class="hot">قهوة</li>
  <li>عصير</li>
  <li class="hot">كاكاو</li>
</ul>
<p>عدد العناصر: <b id="count"></b></p>
<script>
$(function () {
  $("li").css("padding", "2px");              // كل <li>
  $(".hot").css("color", "crimson");           // بالصنف
  $("li:first").css("font-weight", "bold");    // مرشح من jQuery
  $("li:even").css("background", "#f1f1f1");   // العنصر 0 و 2 و ...
  $("ul li").last().append(" (الأخير)");
  $("#count").text($("li").length);
});
</script>
```

```reference javascript
$("#id") | بالمعرّف | $("#menu")
$(".class") | بالصنف | $(".active")
$("tag") | باسم الوسم | $("p")
$("a b") | b داخل a | $("nav a")
$("[name=email]") | بالخاصية | $("input[type=checkbox]")
:first / :last / :even | مرشحات الموضع في jQuery | $("tr:even")
.length | عدد ما وُجد | $("li").length
.eq(i) / .first() / .last() | عنصر واحد من المجموعة | $("li").eq(2)
```

:::tip تحديد واحد وعناصر كثيرة
ترجع `$("li")` مجموعة، واستدعاء `.css(...)` عليها يغيّر **كل** عناصرها؛ لا تحتاج حلقة.
:::

```exercise javascript
? حدّد كل العناصر التي لها الصنف active
$("___")
= .active
```

```quiz
? ماذا يعطي $("li").length؟
* عدد عناصر li التي وُجدت
- طول نص أول li
- دائمًا 1
```

# @lesson jq-events
title: الأحداث
summary: click و on و hover و keyup وكائن الحدث و this.
---
```try html jq
<button id="add">أضف واحدًا</button>
<button id="reset">صفّر</button>
<p>النقرات: <b id="n">0</b></p>
<input id="name" placeholder="اكتب اسمك">
<p id="hello"></p>
<div class="box" id="area">مرّر الفأرة فوقي</div>
<script>
$(function () {
  let count = 0;
  $("#add").on("click", function () {
    count++;
    $("#n").text(count);
  });
  $("#reset").click(() => { count = 0; $("#n").text(0); });

  $("#name").on("keyup", function () {
    $("#hello").text("أهلًا، " + $(this).val());   // this = حقل الإدخال
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
.on("click", fn) | ربط معالج حدث | $("#save").on("click", save)
.click(fn) / .change(fn) | اختصارات | $("select").change(update)
.hover(in, out) | دخول الفأرة / خروجها | $(".card").hover(a, b)
$(this) | العنصر الذي أطلق الحدث | $(this).hide()
e.preventDefault() | منع السلوك الافتراضي | رابط أو إرسال نموذج
.off("click") | إزالة المعالجات | $("#btn").off("click")
.trigger("click") | إطلاق حدث من الكود | $("#btn").trigger("click")
```

:::warning الدوال السهمية و this
داخل الدالة السهمية لا تكون `this` هي العنصر. استخدم `function () { ... }` العادية عندما تحتاج `$(this)`، أو استخدم `e.currentTarget`.
:::

```exercise javascript
? اربط معالج النقر بالطريقة العامة
$("#save").___("click", save);
= on
```

```quiz
? داخل دالة معالجة عادية، ما هو $(this)؟
* العنصر الذي أطلق الحدث
- المستند كله
- مكتبة jQuery
```

# @lesson jq-dom
title: تغيير المحتوى
summary: text و html و append و prepend و before و after و remove و empty.
---
```try html jq
<div id="list" class="box"><p>العنصر الأول</p></div>
<button id="end">أضف في النهاية</button>
<button id="start">أضف في البداية</button>
<button id="clear">أفرغ</button>
<p id="info"></p>
<script>
$(function () {
  let n = 1;
  $("#end").on("click", function () {
    n++;
    $("#list").append("<p>عنصر " + n + "</p>");
  });
  $("#start").on("click", function () {
    $("<p>").text("أُضيف في الأعلى").css("color", "teal").prependTo("#list");
  });
  $("#clear").on("click", function () {
    $("#list").empty();
  });
  $("#list").before("<h4>قائمتي</h4>");

  const userText = "<b>ليس عريضًا</b>";
  $("#info").text(userText);   // يظهر كنص، وهذا آمن
});
</script>
```

```reference javascript
.text() / .text(v) | قراءة / وضع النص | $("h1").text("Hi")
.html() / .html(v) | قراءة / وضع HTML | $("#box").html("<b>ok</b>")
.append / .prepend | إضافة بالداخل في النهاية / البداية | $("ul").append("<li>x</li>")
.after / .before | إضافة بجواره | $("h2").after("<hr>")
$("<p>") | إنشاء عنصر جديد | $("<li>").text(name)
.appendTo / .prependTo | إدراج العنصر الجديد | $("<li>").appendTo("ul")
.remove() / .empty() | حذفه / حذف أبنائه | $(".old").remove()
```

:::danger استخدم .text() لمدخلات المستخدم وليس .html()
`.html(userInput)` تنفّذ أي HTML أو سكربت كتبه المستخدم (XSS). ضع النص غير الموثوق بـ `.text()`، أو ابنِ العناصر بـ `$("<li>").text(value)`.
:::

```exercise javascript
? أضف عنصر قائمة جديدًا في نهاية #todo
$("#todo").___("<li>Read</li>");
= append
```

```quiz
? أي دالة آمنة لعرض نص كتبه المستخدم؟
* .text()
- .html()
- .append() مع نص HTML

? تحذف .empty() الأبناء وتُبقي العنصر نفسه.
= true
```

# @lesson jq-css
title: التنسيق والأصناف
summary: css و addClass و removeClass و toggleClass و hasClass والأحجام.
---
```try html jq
<style>.big { font-size: 1.6em; } .dark { background: #222; color: #eee; }</style>
<div class="box" id="card">بطاقة</div>
<button id="big">تكبير / تصغير</button>
<button id="dark">وضع داكن</button>
<p id="state"></p>
<script>
$(function () {
  function show() {
    $("#state").text(
      "داكن: " + $("#card").hasClass("dark") +
      "، العرض: " + Math.round($("#card").width()) + "px" +
      "، اللون: " + $("#card").css("color")
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
.css("prop") | قراءة تنسيق | $("p").css("color")
.css("prop", v) / .css({..}) | وضع تنسيق / عدة تنسيقات | $("p").css({ color: "red" })
.addClass / .removeClass | إضافة / إزالة صنف | $("li").addClass("done")
.toggleClass | أضف إن لم يوجد واحذف إن وُجد | $("#menu").toggleClass("open")
.hasClass | هل له هذا الصنف؟ | if ($(this).hasClass("on"))
.width() / .height() | الحجم بالبكسل | $(window).width()
```

:::tip فضّل الأصناف على التنسيق المباشر
احتفظ بالشكل في CSS وبدّله بـ `addClass` و `toggleClass`. هذا أسهل في التعديل لاحقًا من استدعاءات `.css(...)` كثيرة متفرقة في الكود.
:::

```exercise javascript
? بدّل الصنف open تشغيلًا وإيقافًا على #menu
$("#menu").___("open");
= toggleClass
```

```quiz
? ماذا تفعل .toggleClass("done") إذا كان للعنصر الصنف done بالفعل؟
* تزيله
- تضيفه مرة ثانية
- لا شيء
```

# @lesson jq-forms
title: النماذج والقيم والخصائص
summary: val و attr و prop و submit والتحقق البسيط.
---
```try html jq
<form id="signup">
  <input id="email" type="email" placeholder="البريد الإلكتروني"><br>
  <label><input id="terms" type="checkbox"> أوافق على الشروط</label><br>
  <select id="plan"><option value="free">مجانية</option><option value="pro">احترافية</option></select>
  <button>اشترك</button>
</form>
<p id="result"></p>
<a id="link" href="https://example.com">رابط</a>
<script>
$(function () {
  $("#signup").on("submit", function (e) {
    e.preventDefault();                       // ابقَ في الصفحة
    const email = $("#email").val().trim();
    if (!email.includes("@")) {
      $("#result").text("أدخل بريدًا صحيحًا").css("color", "crimson");
      return;
    }
    if (!$("#terms").prop("checked")) {
      $("#result").text("يجب الموافقة على الشروط").css("color", "crimson");
      return;
    }
    $("#result").text("أهلًا " + email + "، الباقة: " + $("#plan").val()).css("color", "green");
    $(this).find("button").prop("disabled", true);
  });
  $("#link").attr("target", "_blank").text("يفتح في نافذة جديدة: " + $("#link").attr("href"));
});
</script>
```

```reference javascript
.val() / .val(v) | قراءة / وضع قيمة حقل | $("#q").val()
.attr("name") / .attr(n, v) | قراءة / وضع خاصية HTML | $("img").attr("src", url)
.prop("checked") | الحالة الحالية: مُختار، معطّل، محدد | $("#ok").prop("checked")
.prop("disabled", true) | تعطيل عنصر تحكم | $("button").prop("disabled", true)
.on("submit", fn) | معالجة إرسال النموذج | $("form").on("submit", send)
.serialize() | حقول النموذج كنص استعلام | $("form").serialize()
```

:::warning التحقق في المتصفح لا يكفي
التحقق في المتصفح يساعد المستخدم، لكن أي شخص يستطيع إرسال أي بيانات لخادمك. تحقّق دائمًا مرة أخرى على الخادم.
:::

```exercise javascript
? اقرأ هل مربع الاختيار #terms مُعلَّم
$("#terms").___("checked")
= prop
```

```quiz
? أي دالة تقرأ النص المكتوب في حقل إدخال؟
* .val()
- .text()
- .html()
```

# @lesson jq-effects
title: المؤثرات والحركة
summary: hide و show و toggle و fade و slide و animate والتسلسل.
---
```try html jq
<button id="t">إظهار / إخفاء</button>
<button id="f">تلاشٍ</button>
<button id="s">انزلاق</button>
<button id="a">تحريك</button>
<div class="box" id="panel">أنا لوحة</div>
<script>
$(function () {
  $("#t").on("click", () => $("#panel").toggle());
  $("#f").on("click", () => $("#panel").fadeToggle(400));
  $("#s").on("click", () => $("#panel").slideToggle("fast"));
  $("#a").on("click", function () {
    $("#panel")
      .animate({ paddingRight: "60px", opacity: 0.5 }, 400)
      .animate({ paddingRight: "10px", opacity: 1 }, 400, function () {
        $(this).text("انتهت الحركة");    // تُستدعى عند الانتهاء
      });
  });
});
</script>
```

```reference javascript
.hide() / .show() / .toggle() | إخفاء / إظهار / تبديل | $("#help").toggle()
.fadeIn / .fadeOut / .fadeToggle | التلاشي | $(".msg").fadeOut(500)
.slideUp / .slideDown / .slideToggle | الانزلاق | $("#menu").slideToggle()
.animate({..}, ms, done) | تحريك التنسيقات الرقمية | $("#box").animate({ left: "100px" })
.delay(ms) | الانتظار في طابور الحركة | $("#a").fadeIn().delay(1000).fadeOut()
.stop() | إيقاف الحركة الحالية | $("#a").stop()
```

:::tip التسلسل
معظم دوال jQuery ترجع نفس المجموعة، فتستطيع تسلسلها: `$("#msg").text("Saved").fadeIn().delay(1500).fadeOut()`.
:::

```exercise javascript
? أخفِ #note ببطء بالتلاشي
$("#note").___(600);
= fadeOut
```

```quiz
? لماذا يمكنك كتابة $("#a").fadeIn().delay(500).fadeOut()؟
* لأن كل دالة ترجع نفس مجموعة jQuery فيمكن تسلسل الاستدعاءات
- لأن delay دالة عامة
- لأن fadeIn تنتظر المستخدم
```

# @lesson jq-traversing
title: التنقل في الصفحة
summary: parent و children و find و closest و siblings و next و each.
---
```try html jq
<table border="1" cellpadding="6">
  <tr><td>شاي</td><td>12</td><td><button class="del">حذف</button></td></tr>
  <tr><td>قهوة</td><td>20</td><td><button class="del">حذف</button></td></tr>
  <tr><td>كعكة</td><td>35</td><td><button class="del">حذف</button></td></tr>
</table>
<p id="total"></p>
<script>
$(function () {
  function total() {
    let sum = 0;
    $("tr").each(function () {
      sum += Number($(this).children().eq(1).text());
    });
    $("#total").text("الإجمالي: " + sum);
  }
  $(".del").on("click", function () {
    const row = $(this).closest("tr");        // أقرب <tr> أب
    row.find("td").first().css("color", "crimson");
    row.fadeOut(300, function () { $(this).remove(); total(); });
  });
  $("td:contains('قهوة')").next().css("font-weight", "bold");
  total();
});
</script>
```

```reference javascript
.parent() / .parents() | الأب المباشر / كل الأسلاف | $(this).parent()
.closest(sel) | أقرب سلف مطابق | $(this).closest(".card")
.children() / .find(sel) | الأبناء المباشرون / أي عنصر بالداخل | $("#menu").find("a")
.siblings() / .next() / .prev() | الجيران | $("li.active").next()
.each(fn) | تنفيذ دالة لكل عنصر | $("li").each(function (i) { })
.filter(sel) / .not(sel) | الإبقاء على / استبعاد بعض العناصر | $("li").not(".done")
```

```exercise javascript
? جد البطاقة التي تحتوي الزر الذي نُقر
$(this).___(".card")
= closest
```

```quiz
? أي دالة تبحث في العناصر الموجودة بالداخل عن محدد؟
* .find()
- .closest()
- .parent()
```

# @lesson jq-ajax
title: AJAX مع jQuery
summary: $.ajax و $.getJSON والوعود وتحميل البيانات بدون إعادة تحميل الصفحة.
---
**AJAX** تعني طلب بيانات من الخادم في الخلفية وتحديث جزء من الصفحة، بدون إعادة تحميلها بالكامل.

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

المثال التالي لا يصل إلى خادم حقيقي، لذلك ترجع `fakeServer` وعدًا من jQuery يتصرف مثل `$.getJSON`:

```try html jq
<button id="load">حمّل المنتجات</button>
<p id="status"></p>
<ul id="list"></ul>
<script>
function fakeServer() {                       // بديل عن $.getJSON("/api/products")
  const d = $.Deferred();
  setTimeout(() => d.resolve([{ name: "شاي", price: 12 }, { name: "قهوة", price: 20 }]), 600);
  return d.promise();
}
$(function () {
  $("#load").on("click", function () {
    $("#status").text("جارٍ التحميل…");
    $("#list").empty();
    fakeServer()
      .done(function (products) {
        products.forEach(p => $("<li>").text(p.name + " – " + p.price).appendTo("#list"));
        $("#status").text("تم تحميل " + products.length + " منتجات");
      })
      .fail(() => $("#status").text("تعذّر التحميل"));
  });
});
</script>
```

```reference javascript
$.getJSON(url, fn) | طلب GET وتحويل JSON | $.getJSON("/api/me", show)
$.get / $.post | GET / POST مختصر | $.post("/api/log", { a: 1 })
$.ajax({ url, method, data }) | تحكم كامل | $.ajax({ url: "/x", method: "PUT" })
.done / .fail / .always | نجاح / خطأ / الحالتان | req.done(render)
$("#box").load(url) | تحميل HTML داخل عنصر | $("#side").load("/menu.html")
$.Deferred() | بناء وعد خاص بك | const d = $.Deferred()
```

:::tip وعود jQuery و async/await
طلبات jQuery تدعم `then`، فتستطيع في الكود الحديث كتابة `const data = await $.getJSON(url);` داخل دالة `async`.
:::

```exercise javascript
? عالج الاستجابة الناجحة للطلب req
req.___(render);
= done
```

```quiz
? ما الفكرة الأساسية في AJAX؟
* جلب البيانات في الخلفية وتحديث جزء من الصفحة
- إعادة تحميل الصفحة كلها أسرع
- تخزين البيانات في المتصفح للأبد
```

# @lesson jq-project
title: مشروع: قائمة مهام صغيرة
summary: المحددات والأحداث وتغيير الصفحة والأصناف معًا.
---
```try html jq
<input id="task" placeholder="مهمة جديدة">
<button id="add">أضف</button>
<button id="clear">احذف المنجز</button>
<ul id="tasks"></ul>
<p id="left"></p>
<script>
$(function () {
  function update() {
    const left = $("#tasks li").not(".done").length;
    $("#left").text("المتبقي: " + left);
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

  // حدث مفوَّض: يعمل مع العناصر المضافة لاحقًا
  $("#tasks").on("click", "li", function () {
    $(this).toggleClass("done");
    update();
  });
  $("#clear").on("click", function () {
    $("#tasks li.done").slideUp(200, function () { $(this).remove(); update(); });
  });

  ["اقرأ درسًا", "حلّ الاختبار"].forEach(t => $("<li>").text(t).appendTo("#tasks"));
  update();
});
</script>
```

:::tip الأحداث المفوَّضة
`$("#tasks").on("click", "li", fn)` تضع معالجًا واحدًا على القائمة يلتقط أيضًا النقر على عناصر `<li>` التي تُنشأ لاحقًا. أما `$("li").on("click", fn)` فتغطي فقط العناصر الموجودة الآن.
:::

```quiz
? لماذا يستخدم المشروع $("#tasks").on("click", "li", ...)؟
* لكي تستجيب للنقر العناصر المضافة لاحقًا أيضًا
- لأن عناصر li لا تقبل معالجات النقر
- لجعل القائمة قابلة للترتيب
```

# @lesson jq-reference
title: مرجع jQuery السريع
summary: أكثر الدوال استخدامًا في صفحة واحدة، ومتى تستخدم JavaScript العادية بدلًا منها.
---
```reference javascript
$(function () { }) | التنفيذ عندما تجهز الصفحة | $(init)
$("css selector") | إيجاد العناصر | $("#form input")
.on(event, [child], fn) | الأحداث (والتفويض) | $("ul").on("click", "li", fn)
.text / .html / .val | المحتوى والقيم | $("#q").val()
.append / .remove / $("<tag>") | تغيير الصفحة | $("<li>").text(x).appendTo("ul")
.addClass / .toggleClass / .css | التنسيق | $("li").addClass("done")
.attr / .prop | الخصائص / الحالة الحالية | $("#ok").prop("checked")
.show / .fadeIn / .slideToggle / .animate | المؤثرات | $("#msg").fadeOut()
.closest / .find / .each | التنقل | $(this).closest("tr")
$.getJSON / $.ajax | طلبات الخادم | $.getJSON(url).done(show)
```

## jQuery و JavaScript العادية

| jQuery | JavaScript العادية |
|---|---|
| `$("#id")` | `document.querySelector("#id")` |
| `$(".a").addClass("b")` | `document.querySelectorAll(".a").forEach(e => e.classList.add("b"))` |
| `$(el).on("click", fn)` | `el.addEventListener("click", fn)` |
| `$(el).text("x")` | `el.textContent = "x"` |
| `$.getJSON(url)` | `fetch(url).then(r => r.json())` |

:::tip الخطوة التالية
في المشاريع الجديدة غالبًا تكون JavaScript العادية أو إطار عمل (React و Vue) الخيار الأفضل. وتبقى معرفة jQuery مفيدة لصيانة المواقع الموجودة وقوالب WordPress وكثير من لوحات الإدارة.
:::

```quiz
? ما المقابل في JavaScript العادية لـ $(el).on("click", fn)؟
* el.addEventListener("click", fn)
- el.click = fn()
- document.on("click", fn)
```
