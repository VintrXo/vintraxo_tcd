# @lesson json-intro
title: ما هو JSON
summary: صيغة بيانات الويب: الكائنات والمصفوفات والقيم.
---
**JSON** (JavaScript Object Notation) صيغة نصية للبيانات. ترسلها واجهات API، وتستخدمها ملفات الإعدادات، وتقرأها وتكتبها كل اللغات تقريبًا. تشبه كائنات JavaScript لكنها مجرد نص.

```json
{
  "id": 7,
  "customer": "Sara",
  "paid": true,
  "items": [
    { "name": "Tea", "qty": 2, "price": 12.5 },
    { "name": "Cake", "qty": 1, "price": 35 }
  ],
  "coupon": null
}
```

- **الكائن** هو `{ ... }` بأزواج `"key": value`.
- **المصفوفة** هي `[ ... ]`، قائمة مرتبة من القيم.
- القيمة يمكن أن تكون نصًا أو رقمًا أو `true` أو `false` أو `null` أو كائنًا أو مصفوفة.

```try javascript
const text = '{"id": 7, "customer": "Sara", "items": [{"name": "Tea", "qty": 2}]}';
const order = JSON.parse(text);          // نص -> كائن
console.log(order.customer, order.items[0].name, order.items.length);
console.log(typeof text, typeof order);
```

```quiz
? ما هو JSON؟
* صيغة نصية للبيانات المنظمة
- لغة برمجة
- قاعدة بيانات

? القيمة null قيمة صحيحة في JSON.
= true
```

# @lesson json-syntax
title: قواعد كتابة JSON
summary: علامات التنصيص المزدوجة، وبلا فاصلة زائدة، وبلا تعليقات، والأخطاء الشائعة.
---
JSON أكثر صرامة من JavaScript، ويرفض المحلل أي شيء خارج القواعد:

| القاعدة | صحيح | خطأ |
|---|---|---|
| المفاتيح بين علامتي تنصيص مزدوجتين | `{"a": 1}` | `{a: 1}` |
| النصوص بين علامتي تنصيص مزدوجتين | `"tea"` | `'tea'` |
| لا فاصلة بعد آخر عنصر | `[1, 2]` | `[1, 2,]` |
| لا تعليقات | | `// note` |
| هذه القيم الحرفية فقط | `true` و `false` و `null` | `undefined` و `NaN` |

```try javascript
const samples = [
  '{"name": "Sara", "age": 25}',
  "{'name': 'Sara'}",
  '{"tags": ["a", "b",]}',
  '{name: "Sara"}',
  '{"price": 12.50, "note": "line1\\nline2", "emoji": "\\u2615"}',
];
for (const s of samples) {
  try {
    JSON.parse(s);
    console.log("valid:  ", s);
  } catch (e) {
    console.log("INVALID:", s, "->", e.name);
  }
}
```

:::tip الحروف الخاصة داخل النصوص
داخل نص JSON اكتب علامة التنصيص هكذا `\"`، والشرطة المائلة العكسية `\\`، والسطر الجديد `\n`، وأي حرف Unicode بصيغة `\uXXXX`. ويمكن كتابة النص العربي مباشرة بترميز UTF-8.
:::

```exercise javascript
? أصلح المفتاح ليصبح JSON صحيحًا
{___: "Cairo"}
= "city"
```

```quiz
? أيٌّ مما يلي JSON صحيح؟
* {"ok": true}
- {'ok': true}
- {ok: true}

? يسمح JSON بالتعليقات باستخدام //.
= false
> JSON القياسي بلا تعليقات؛ بعض الأدوات تقبل "JSON مع تعليقات" لكن JSON.parse لا تقبله.
```

# @lesson json-js
title: JSON في JavaScript
summary: JSON.parse و JSON.stringify والطباعة المنسقة وتصفية المفاتيح والتواريخ.
---
```try javascript
const order = {
  id: 7,
  customer: "Sara",
  items: [{ name: "Tea", qty: 2 }],
  createdAt: new Date("2026-01-03T10:00:00Z"),
  secret: "do-not-send",
  note: undefined,                      // الخصائص undefined تُتجاهل
};

const compact = JSON.stringify(order);
console.log(compact);

const pretty = JSON.stringify(order, ["id", "customer", "items", "name", "qty"], 2);
console.log(pretty);                      // المفاتيح المذكورة فقط، بإزاحة 2

const safe = JSON.stringify(order, (key, value) => (key === "secret" ? undefined : value));
console.log(safe.includes("secret"));

const back = JSON.parse(compact);
console.log(typeof back.createdAt);       // التواريخ تعود كنصوص
console.log(new Date(back.createdAt).getUTCFullYear());

const copy = JSON.parse(JSON.stringify({ a: [1, 2] }));   // نسخة عميقة لبيانات بسيطة
copy.a.push(3);
console.log(copy.a);
```

```reference javascript
JSON.parse(text) | نص إلى قيمة | const data = JSON.parse(body)
JSON.stringify(v) | قيمة إلى نص | JSON.stringify({ a: 1 })
JSON.stringify(v, null, 2) | طباعة منسقة بمسافتين | console.log(JSON.stringify(o, null, 2))
JSON.stringify(v, [keys]) | الإبقاء على بعض المفاتيح فقط | JSON.stringify(u, ["id", "name"])
replacer (key, value) | تغيير القيم أو حذفها | (k, v) => k === "password" ? undefined : v
reviver في JSON.parse | تحويل القيم أثناء القراءة | JSON.parse(t, (k, v) => k === "date" ? new Date(v) : v)
```

:::warning التواريخ والقيم الخاصة
تحوّل `JSON.stringify` التواريخ إلى نصوص بصيغة ISO وتحذف `undefined` والدوال، ولا تعيد `JSON.parse` النصوص إلى تواريخ. حوّلها بنفسك، مثلًا باستخدام reviver.
:::

```exercise javascript
? حوّل الكائن user إلى نص JSON منسق
JSON.___(user, null, 2)
= stringify
```

```quiz
? ما نوع قيمة Date بعد JSON.stringify ثم JSON.parse؟
* string
- Date
- number
```

# @lesson json-python
title: JSON في Python
summary: json.loads و json.dumps والملفات وأنواع Python.
---
```try python
import json

text = '{"id": 7, "customer": "سارة", "paid": true, "coupon": null, "items": [{"name": "Tea", "qty": 2}]}'
order = json.loads(text)                  # نص -> قاموس
print(order["customer"], order["paid"], order["coupon"])
print(type(order), type(order["items"]))

order["items"].append({"name": "Cake", "qty": 1})
print(json.dumps(order))                                   # العربية بصيغة \u
print(json.dumps(order, ensure_ascii=False, indent=2))     # مقروءة

with open("order.json", "w", encoding="utf-8") as f:
    json.dump(order, f, ensure_ascii=False)
with open("order.json", encoding="utf-8") as f:
    again = json.load(f)
print(len(again["items"]), "items read back")

try:
    json.loads("{'bad': 1}")
except json.JSONDecodeError as e:
    print("error at line", e.lineno, "column", e.colno)
```

| JSON | Python |
|---|---|
| object | `dict` |
| array | `list` |
| string | `str` |
| number | `int` أو `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

```reference python
json.loads(text) | نص إلى قيمة Python | data = json.loads(body)
json.dumps(value) | قيمة Python إلى نص | json.dumps({"a": 1})
indent=2 / ensure_ascii=False | تنسيق / إبقاء العربية مقروءة | json.dumps(d, ensure_ascii=False, indent=2)
json.load(f) / json.dump(v, f) | قراءة / كتابة ملف | json.load(open("a.json"))
json.JSONDecodeError | يُرمى مع JSON غير صحيح | except json.JSONDecodeError
default=str | التعامل مع أنواع لا يعرفها JSON | json.dumps(d, default=str)
```

```exercise python
? حلّل نص JSON الموجود في body إلى قيمة Python
data = json.___(body)
= loads
```

```quiz
? إلى ماذا تتحول القيمة null من JSON في Python؟
* None
- null
- 0
```

# @lesson json-apis
title: JSON وواجهات API
summary: أجسام الطلبات والاستجابات، والبيانات المتداخلة، وفحص ما يصل.
---
واجهات الويب ترسل وتستقبل JSON عادةً. مثال لطلب واستجابة:

```text
POST /api/orders
Content-Type: application/json

{"customer": "Sara", "items": [{"product": 3, "qty": 2}]}

HTTP/1.1 201 Created
Content-Type: application/json

{"id": 81, "status": "pending", "total": 25.0}
```

في المتصفح تستدعي الواجهة باستخدام `fetch`:

```js
const res = await fetch("/api/orders", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ customer: "Sara", items: [{ product: 3, qty: 2 }] }),
});
if (!res.ok) throw new Error("HTTP " + res.status);
const order = await res.json();
```

المثال التالي يعمل على استجابة وصلت بالفعل، ويفحصها قبل استخدامها:

```try javascript
const body = `{
  "page": 1,
  "results": [
    {"id": 1, "name": "Tea",    "price": 12.5, "tags": ["hot"]},
    {"id": 2, "name": "Juice",  "price": 15,   "tags": ["cold", "fresh"]},
    {"id": 3, "name": "Coffee", "price": "20"}
  ]
}`;
const data = JSON.parse(body);

const valid = [];
for (const p of data.results) {
  if (typeof p.id !== "number" || typeof p.name !== "string" || typeof p.price !== "number") {
    console.log("skipped bad record:", JSON.stringify(p));
    continue;
  }
  valid.push({ ...p, tags: p.tags ?? [] });
}
console.log(valid.map(p => p.name + " " + p.price).join(", "));
console.log("all tags:", [...new Set(valid.flatMap(p => p.tags))]);
console.log("first tag of Juice:", data.results[1]?.tags?.[0]);
```

:::danger لا تثق أبدًا في JSON القادم
البيانات القادمة من API أو من مستخدم قد تنقصها حقول، أو تأتي بأنواع خاطئة أو مفاتيح زائدة. افحص الأنواع قبل استخدام القيم، ولا تمرر نص JSON إلى `eval` أبدًا. وفي المشاريع الأكبر صِف الشكل المتوقع بـ **JSON Schema** وتحقّق منه.
:::

```quiz
? أي ترويسة تخبر الخادم أن جسم الطلب بصيغة JSON؟
* Content-Type: application/json
- Accept-Language: json
- Body: json

? السعر المرسل كنص "20" ينجح في فحص typeof p.price === "number".
= false
```

# @lesson xml-intro
title: ما هو XML
summary: العناصر والخصائص والعنصر الجذر والمستند سليم البنية.
---
**XML** (eXtensible Markup Language) تحفظ البيانات كشجرة من الوسوم التي تسمّيها بنفسك. أقدم من JSON، وما زالت شائعة في ملفات المكتب وخلاصات RSS وصور SVG والفواتير والبنوك وواجهات Android وكثير من أنظمة الشركات.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<order id="7" currency="EGP">
  <customer>Sara</customer>
  <items>
    <item qty="2"><name>Tea</name><price>12.5</price></item>
    <item qty="1"><name>Cake</name><price>35</price></item>
  </items>
  <note/>
</order>
```

المستند **سليم البنية (well-formed)** يتبع هذه القواعد:

- **عنصر جذر** واحد بالضبط (هنا `<order>`) يحتوي كل شيء.
- لكل وسم فتح وسم إغلاق، أو يكون مغلقًا ذاتيًا مثل `<note/>`.
- تتداخل الوسوم بشكل صحيح: `<a><b></b></a>`، وليس `<a><b></a></b>` أبدًا.
- الأسماء حساسة لحالة الأحرف: `<Item>` و `<item>` مختلفان.
- قيم الخصائص بين علامتي تنصيص: `qty="2"`.
- يُكتب `&` و `<` داخل النص بالشكل `&amp;` و `&lt;`.

```quiz
? كم عنصرًا جذرًا يمكن أن يحتوي مستند XML؟
* واحدًا بالضبط
- أي عدد تريده
- اثنين: واحد للبيانات وواحد للوصف

? في XML الوسمان <Item> و <item> متماثلان.
= false
```

# @lesson xml-python
title: قراءة XML وبناؤه في Python
summary: ElementTree: التحليل والبحث والمرور والخصائص وإنشاء المستندات.
---
```try python
import xml.etree.ElementTree as ET

xml_text = """<order id="7" currency="EGP">
  <customer>Sara</customer>
  <items>
    <item qty="2"><name>Tea</name><price>12.5</price></item>
    <item qty="1"><name>Cake</name><price>35</price></item>
  </items>
</order>"""

root = ET.fromstring(xml_text)
print(root.tag, root.attrib)                      # order {'id': '7', 'currency': 'EGP'}
print("customer:", root.find("customer").text)

total = 0
for item in root.iter("item"):
    qty = int(item.get("qty"))
    price = float(item.findtext("price"))
    total += qty * price
    print(item.findtext("name"), qty, price)
print("total:", total)
print([n.text for n in root.findall("./items/item/name")])   # مسار

new = ET.SubElement(root.find("items"), "item", qty="3")
ET.SubElement(new, "name").text = "Juice"
ET.SubElement(new, "price").text = "15"
root.set("status", "paid")
print(len(root.findall(".//item")), "items now")
print(ET.tostring(root.find("items/item[3]"), encoding="unicode"))
```

```reference python
ET.fromstring(text) / ET.parse(file) | قراءة XML | tree = ET.parse("feed.xml")
el.tag / el.text / el.attrib | الاسم والنص والخصائص | el.attrib["id"]
el.get("name") | خاصية واحدة | item.get("qty")
el.find / el.findall / el.findtext | أول تطابق / الكل / نص التطابق | root.findall("./items/item")
el.iter("tag") | كل عنصر مطابق بأي عمق | for i in root.iter("item")
ET.SubElement(parent, tag) | إضافة عنصر ابن | ET.SubElement(root, "note")
ET.tostring(el, encoding="unicode") | العنصر إلى نص | print(ET.tostring(root, encoding="unicode"))
```

:::warning XML غير الموثوق
في XML ميزات (الكيانات والمراجع الخارجية) يمكن أن يستغلها المهاجمون، مثلًا لجعل المحلل يقرأ ملفات محلية. مع XML القادم من الخارج استخدم محللًا مُحصّنًا مثل حزمة `defusedxml` في Python.
:::

```exercise python
? اقرأ قيمة الخاصية qty من العنصر item
qty = item.___("qty")
= get
```

```quiz
? أي دالة تمر على كل عنصر <item> بأي عمق؟
* root.iter("item")
- root.find("item")
- root.text("item")
```

# @lesson xml-browser
title: XML في المتصفح
summary: DOMParser و querySelector مع XML والخصائص و XMLSerializer.
---
```try html
<pre id="out"></pre>
<script>
const text = `<?xml version="1.0"?>
<catalog>
  <book id="b1" lang="en"><title>Clean Code</title><year>2008</year></book>
  <book id="b2" lang="ar"><title>مقدمة ابن خلدون</title><year>1377</year></book>
  <book id="b3" lang="en"><title>Refactoring</title><year>1999</year></book>
</catalog>`;
const lines = [];
const doc = new DOMParser().parseFromString(text, "application/xml");
if (doc.querySelector("parsererror")) {
  lines.push("Invalid XML");
} else {
  for (const b of doc.querySelectorAll("book")) {
    lines.push(b.getAttribute("id") + ": " + b.querySelector("title").textContent + " (" + b.querySelector("year").textContent + ")");
  }
  lines.push("English books: " + doc.querySelectorAll('book[lang="en"]').length);
  const newBook = doc.createElement("book");
  newBook.setAttribute("id", "b4");
  newBook.textContent = "New";
  doc.documentElement.appendChild(newBook);
  lines.push("now " + doc.querySelectorAll("book").length + " books");
}
const broken = new DOMParser().parseFromString("<a><b></a>", "application/xml");
lines.push("broken document detected: " + !!broken.querySelector("parsererror"));
document.getElementById("out").textContent = lines.join("\n");
</script>
```

```reference javascript
new DOMParser().parseFromString(t, "application/xml") | تحليل نص XML | const doc = new DOMParser().parseFromString(xml, "application/xml")
doc.querySelector("parsererror") | اكتشاف XML غير صحيح | if (doc.querySelector("parsererror"))
querySelectorAll("tag[attr=v]") | إيجاد العناصر | doc.querySelectorAll("item")
el.getAttribute / setAttribute | قراءة / وضع الخصائص | el.getAttribute("id")
el.textContent | النص بالداخل | title.textContent
new XMLSerializer().serializeToString(doc) | المستند إلى نص مرة أخرى | new XMLSerializer().serializeToString(doc)
```

```exercise javascript
? اقرأ الخاصية id من العنصر b
b.___("id")
= getAttribute
```

```quiz
? كيف تعرف أن DOMParser لم يستطع تحليل XML؟
* تحتوي النتيجة على عنصر parsererror
- يرمي استثناءً في كل مرة
- يرجع null
```

# @lesson xml-advanced
title: مساحات الأسماء و XPath والتحقق
summary: البادئات ومساحات الأسماء، ومسارات XPath، والمخططات (DTD و XSD).
---
**مساحات الأسماء (namespaces)** تمنع تعارض الأسماء عندما يخلط مستند واحد بين مفردات مختلفة. تُربط البادئة بعنوان URI، وتستخدم العناصر البادئة:

```xml
<inv:invoice xmlns:inv="urn:example:invoice" xmlns:addr="urn:example:address">
  <inv:number>2026-0042</inv:number>
  <addr:city>Cairo</addr:city>
</inv:invoice>
```

**XPath** لغة مسارات لاختيار أجزاء من شجرة XML:

| XPath | يختار |
|---|---|
| `/order/customer` | `customer` مباشرة تحت الجذر `order` |
| `//item` | كل `item` بأي عمق |
| `//item[@qty="2"]` | العناصر التي قيمة خاصيتها `qty` تساوي 2 |
| `//item/name/text()` | نص كل اسم عنصر |
| `count(//item)` | عدد العناصر |

```try python
import xml.etree.ElementTree as ET

text = """<inv:invoice xmlns:inv="urn:example:invoice" xmlns:addr="urn:example:address">
  <inv:number>2026-0042</inv:number>
  <addr:city>Cairo</addr:city>
  <inv:line qty="2"><inv:product>Tea</inv:product></inv:line>
  <inv:line qty="5"><inv:product>Cake</inv:product></inv:line>
</inv:invoice>"""
ns = {"inv": "urn:example:invoice", "addr": "urn:example:address"}
root = ET.fromstring(text)
print(root.tag)                                         # {urn:example:invoice}invoice
print(root.findtext("inv:number", namespaces=ns))
print(root.findtext("addr:city", namespaces=ns))
print([l.findtext("inv:product", namespaces=ns) for l in root.findall('inv:line[@qty="5"]', ns)])
```

**المخطط (schema)** يصف العناصر والخصائص المسموحة. أشهر نوعين هما **DTD** (قديم وبسيط) و **XSD** (XML Schema، بأنواع بيانات). أنظمة مثل بوابات الفاتورة الإلكترونية تنشر ملف XSD، ويجب أن يطابقه المستند قبل قبوله.

```quiz
? ماذا يختار مسار XPath التالي: //item؟
* كل عناصر item بأي عمق
- أول item فقط
- عناصر item تحت الجذر مباشرة فقط

? تُربط بادئة مساحة الأسماء بعنوان URI عبر xmlns:prefix="...".
= true
```

# @lesson json-xml-compare
title: مشروع: JSON أم XML؟
summary: قارن بين الصيغتين وحوّل خلاصة XML إلى JSON.
---
| | JSON | XML |
|---|---|---|
| الحجم | أصغر | أكبر (وسوم الإغلاق) |
| أنواع البيانات | أرقام وقيم منطقية و null ومصفوفات | كل شيء نص (الأنواع من المخطط) |
| الخصائص والنص المختلط | لا | نعم |
| التعليقات | لا | نعم |
| المخططات | JSON Schema | DTD و XSD |
| شائع في | واجهات الويب والإعدادات و NoSQL | المستندات والخلاصات وأنظمة الشركات والحكومات |

المشروع: حوّل خلاصة منتجات بصيغة XML إلى JSON، مع تحويل الأنواع أثناء ذلك.

```try python
import json
import xml.etree.ElementTree as ET

feed = """<products updated="2026-01-03">
  <product id="1" available="true"><name>Tea</name><price>12.5</price><tag>hot</tag></product>
  <product id="2" available="false"><name>Juice</name><price>15</price><tag>cold</tag><tag>fresh</tag></product>
</products>"""

root = ET.fromstring(feed)
data = {
    "updated": root.get("updated"),
    "products": [
        {
            "id": int(p.get("id")),
            "name": p.findtext("name"),
            "price": float(p.findtext("price")),
            "available": p.get("available") == "true",
            "tags": [t.text for t in p.findall("tag")],
        }
        for p in root.findall("product")
    ],
}
print(json.dumps(data, indent=2))
print("available:", [p["name"] for p in data["products"] if p["available"]])
```

:::tip جرّب بنفسك
اعمل الاتجاه المعاكس: ابنِ XML من القاموس `data` باستخدام `ET.Element` و `ET.SubElement`، واطبعه بـ `ET.tostring`.
:::

```quiz
? لماذا يستدعي المشروع int() و float() أثناء التحويل؟
* لأن قيم XML نصوص بينما يحمل JSON أرقامًا حقيقية
- لأن JSON لا يسمح بالنصوص
- لأن Python تحتاجها للطباعة
```

# @lesson json-xml-reference
title: مرجع JSON و XML السريع
summary: الصيغ وأكثر الدوال استخدامًا في صفحة واحدة.
---
```reference javascript
{ "k": v } / [ ... ] | كائن / مصفوفة JSON | {"tags": ["a", "b"]}
"text" / 1.5 / true / null | قيم JSON (تنصيص مزدوج فقط) | {"ok": true, "n": null}
JSON.parse / JSON.stringify | JavaScript | JSON.stringify(o, null, 2)
json.loads / json.dumps | Python | json.dumps(d, ensure_ascii=False)
<root> ... </root> | عنصر جذر واحد في XML | <order>...</order>
<tag attr="v">text</tag> | عنصر XML بخاصية | <item qty="2">Tea</item>
<empty/> | عنصر XML مغلق ذاتيًا | <note/>
&amp; / &lt; | الهروب داخل نص XML | Fish &amp; chips
ET.fromstring / findall / get | XML في Python | root.findall("./items/item")
DOMParser / querySelectorAll | XML في المتصفح | doc.querySelectorAll("book")
//item[@id="3"] | XPath | //book[@lang="ar"]/title
```

:::tip الخطوة التالية
استدعِ واجهة JSON عامة من Python باستخدام `urllib.request` أو `requests`، واحفظ النتيجة في ملف ولخّصها. ومع XML اقرأ خلاصة RSS واطبع أحدث العناوين.
:::

```quiz
? أي صيغة تدعم التعليقات والخصائص؟
* XML
- JSON
- كلتاهما
```
