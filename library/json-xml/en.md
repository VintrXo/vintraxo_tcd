# @lesson json-intro
title: What JSON is
summary: The data format of the web: objects, arrays and values.
---
**JSON** (JavaScript Object Notation) is a text format for data. APIs send it, configuration files use it, and almost every language can read and write it. It looks like JavaScript objects, but it is just text.

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

- An **object** is `{ ... }` with `"key": value` pairs.
- An **array** is `[ ... ]`, an ordered list of values.
- Values can be a string, a number, `true`, `false`, `null`, an object or an array.

```try javascript
const text = '{"id": 7, "customer": "Sara", "items": [{"name": "Tea", "qty": 2}]}';
const order = JSON.parse(text);          // text -> object
console.log(order.customer, order.items[0].name, order.items.length);
console.log(typeof text, typeof order);
```

```quiz
? What is JSON?
* A text format for structured data
- A programming language
- A database

? null is a valid JSON value.
= true
```

# @lesson json-syntax
title: JSON syntax rules
summary: Double quotes, no trailing commas, no comments, and common mistakes.
---
JSON is stricter than JavaScript. The parser rejects anything outside the rules:

| Rule | Valid | Invalid |
|---|---|---|
| Keys in double quotes | `{"a": 1}` | `{a: 1}` |
| Strings in double quotes | `"tea"` | `'tea'` |
| No trailing comma | `[1, 2]` | `[1, 2,]` |
| No comments | | `// note` |
| Only these literals | `true`, `false`, `null` | `undefined`, `NaN` |

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

:::tip Special characters in strings
Inside a JSON string, write a quote as `\"`, a backslash as `\\`, a new line as `\n`, and any Unicode character as `\uXXXX`. Arabic text can also be written directly in UTF-8.
:::

```exercise javascript
? Fix the key so this is valid JSON
{___: "Cairo"}
= "city"
```

```quiz
? Which of these is valid JSON?
* {"ok": true}
- {'ok': true}
- {ok: true}

? JSON allows comments with //.
= false
> Standard JSON has no comments; some tools accept "JSON with comments", but JSON.parse does not.
```

# @lesson json-js
title: JSON in JavaScript
summary: JSON.parse, JSON.stringify, pretty printing, filtering keys and dates.
---
```try javascript
const order = {
  id: 7,
  customer: "Sara",
  items: [{ name: "Tea", qty: 2 }],
  createdAt: new Date("2026-01-03T10:00:00Z"),
  secret: "do-not-send",
  note: undefined,                      // undefined properties are skipped
};

const compact = JSON.stringify(order);
console.log(compact);

const pretty = JSON.stringify(order, ["id", "customer", "items", "name", "qty"], 2);
console.log(pretty);                      // only listed keys, indented by 2

const safe = JSON.stringify(order, (key, value) => (key === "secret" ? undefined : value));
console.log(safe.includes("secret"));

const back = JSON.parse(compact);
console.log(typeof back.createdAt);       // dates come back as strings
console.log(new Date(back.createdAt).getUTCFullYear());

const copy = JSON.parse(JSON.stringify({ a: [1, 2] }));   // a deep copy of plain data
copy.a.push(3);
console.log(copy.a);
```

```reference javascript
JSON.parse(text) | Text to value | const data = JSON.parse(body)
JSON.stringify(v) | Value to text | JSON.stringify({ a: 1 })
JSON.stringify(v, null, 2) | Pretty print with 2 spaces | console.log(JSON.stringify(o, null, 2))
JSON.stringify(v, [keys]) | Keep only some keys | JSON.stringify(u, ["id", "name"])
replacer (key, value) | Change or drop values | (k, v) => k === "password" ? undefined : v
reviver in JSON.parse | Convert values while parsing | JSON.parse(t, (k, v) => k === "date" ? new Date(v) : v)
```

:::warning Dates and special values
`JSON.stringify` turns dates into ISO strings and drops `undefined` and functions; `JSON.parse` does not turn the strings back into dates. Convert them yourself, for example with a reviver.
:::

```exercise javascript
? Turn the object user into indented JSON text
JSON.___(user, null, 2)
= stringify
```

```quiz
? What type does a Date have after JSON.stringify and JSON.parse?
* string
- Date
- number
```

# @lesson json-python
title: JSON in Python
summary: json.loads, json.dumps, files, and Python types.
---
```try python
import json

text = '{"id": 7, "customer": "سارة", "paid": true, "coupon": null, "items": [{"name": "Tea", "qty": 2}]}'
order = json.loads(text)                  # text -> dict
print(order["customer"], order["paid"], order["coupon"])
print(type(order), type(order["items"]))

order["items"].append({"name": "Cake", "qty": 1})
print(json.dumps(order))                                   # Arabic as \u escapes
print(json.dumps(order, ensure_ascii=False, indent=2))     # readable

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
| number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

```reference python
json.loads(text) | Text to Python value | data = json.loads(body)
json.dumps(value) | Python value to text | json.dumps({"a": 1})
indent=2 / ensure_ascii=False | Pretty / keep Arabic readable | json.dumps(d, ensure_ascii=False, indent=2)
json.load(f) / json.dump(v, f) | Read / write a file | json.load(open("a.json"))
json.JSONDecodeError | Raised for invalid JSON | except json.JSONDecodeError
default=str | Handle types JSON does not know | json.dumps(d, default=str)
```

```exercise python
? Parse the JSON text body into a Python value
data = json.___(body)
= loads
```

```quiz
? What does JSON null become in Python?
* None
- null
- 0
```

# @lesson json-apis
title: JSON and APIs
summary: Request and response bodies, nested data, and checking what arrives.
---
Web APIs usually send and receive JSON. A typical request and response:

```text
POST /api/orders
Content-Type: application/json

{"customer": "Sara", "items": [{"product": 3, "qty": 2}]}

HTTP/1.1 201 Created
Content-Type: application/json

{"id": 81, "status": "pending", "total": 25.0}
```

In the browser you call an API with `fetch`:

```js
const res = await fetch("/api/orders", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ customer: "Sara", items: [{ product: 3, qty: 2 }] }),
});
if (!res.ok) throw new Error("HTTP " + res.status);
const order = await res.json();
```

The example below works with a response that has already arrived, and checks it before using it:

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

:::danger Never trust incoming JSON
Data from an API or a user can have missing fields, wrong types or extra keys. Check types before using values, and never pass JSON text to `eval`. For larger projects, describe the expected shape with **JSON Schema** and validate against it.
:::

```quiz
? Which header tells the server that the request body is JSON?
* Content-Type: application/json
- Accept-Language: json
- Body: json

? A price sent as the string "20" passes a typeof p.price === "number" check.
= false
```

# @lesson xml-intro
title: What XML is
summary: Elements, attributes, the root element and well-formed documents.
---
**XML** (eXtensible Markup Language) stores data as a tree of tags you name yourself. It is older than JSON and still common in office files, RSS feeds, SVG images, invoices, banking, Android layouts and many enterprise systems.

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

A **well-formed** XML document follows these rules:

- Exactly one **root element** (here `<order>`) contains everything else.
- Every opening tag has a closing tag, or is self-closing like `<note/>`.
- Tags nest properly: `<a><b></b></a>`, never `<a><b></a></b>`.
- Names are case-sensitive: `<Item>` and `<item>` are different.
- Attribute values are in quotes: `qty="2"`.
- `&` and `<` inside text are written `&amp;` and `&lt;`.

```quiz
? How many root elements can an XML document have?
* Exactly one
- As many as you like
- Two: one for data, one for metadata

? In XML, <Item> and <item> are the same tag.
= false
```

# @lesson xml-python
title: Reading and building XML in Python
summary: ElementTree: parse, find, iterate, attributes, and creating documents.
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
print([n.text for n in root.findall("./items/item/name")])   # a path

new = ET.SubElement(root.find("items"), "item", qty="3")
ET.SubElement(new, "name").text = "Juice"
ET.SubElement(new, "price").text = "15"
root.set("status", "paid")
print(len(root.findall(".//item")), "items now")
print(ET.tostring(root.find("items/item[3]"), encoding="unicode"))
```

```reference python
ET.fromstring(text) / ET.parse(file) | Read XML | tree = ET.parse("feed.xml")
el.tag / el.text / el.attrib | Name, text, attributes | el.attrib["id"]
el.get("name") | One attribute | item.get("qty")
el.find / el.findall / el.findtext | First / all / text of a match | root.findall("./items/item")
el.iter("tag") | Every matching element, any depth | for i in root.iter("item")
ET.SubElement(parent, tag) | Add a child element | ET.SubElement(root, "note")
ET.tostring(el, encoding="unicode") | Element to text | print(ET.tostring(root, encoding="unicode"))
```

:::warning Untrusted XML
XML has features (entities, external references) that attackers can abuse, for example to make a parser read local files. For XML from outside, use a hardened parser such as the `defusedxml` package in Python.
:::

```exercise python
? Read the value of the qty attribute of item
qty = item.___("qty")
= get
```

```quiz
? Which method visits every <item> element at any depth?
* root.iter("item")
- root.find("item")
- root.text("item")
```

# @lesson xml-browser
title: XML in the browser
summary: DOMParser, querySelector on XML, attributes, and XMLSerializer.
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
new DOMParser().parseFromString(t, "application/xml") | Parse XML text | const doc = new DOMParser().parseFromString(xml, "application/xml")
doc.querySelector("parsererror") | Detect invalid XML | if (doc.querySelector("parsererror"))
querySelectorAll("tag[attr=v]") | Find elements | doc.querySelectorAll("item")
el.getAttribute / setAttribute | Read / set attributes | el.getAttribute("id")
el.textContent | Text inside | title.textContent
new XMLSerializer().serializeToString(doc) | Document back to text | new XMLSerializer().serializeToString(doc)
```

```exercise javascript
? Read the id attribute of the element b
b.___("id")
= getAttribute
```

```quiz
? How do you know DOMParser could not parse your XML?
* The result contains a parsererror element
- It throws an exception every time
- It returns null
```

# @lesson xml-advanced
title: Namespaces, XPath and validation
summary: Prefixes and namespaces, XPath paths, and schemas (DTD, XSD).
---
**Namespaces** stop name clashes when one document mixes vocabularies. A prefix is bound to a URI, and elements use the prefix:

```xml
<inv:invoice xmlns:inv="urn:example:invoice" xmlns:addr="urn:example:address">
  <inv:number>2026-0042</inv:number>
  <addr:city>Cairo</addr:city>
</inv:invoice>
```

**XPath** is a path language for selecting parts of an XML tree:

| XPath | Selects |
|---|---|
| `/order/customer` | `customer` directly under the root `order` |
| `//item` | every `item`, at any depth |
| `//item[@qty="2"]` | items whose `qty` attribute is 2 |
| `//item/name/text()` | the text of every item name |
| `count(//item)` | the number of items |

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

A **schema** describes which elements and attributes are allowed. Two common kinds are **DTD** (old, simple) and **XSD** (XML Schema, with data types). Systems such as e-invoicing portals publish an XSD, and a document must validate against it before it is accepted.

```quiz
? What does the XPath //item select?
* Every item element at any depth
- Only the first item
- Items directly under the root only

? A namespace prefix is bound to a URI with xmlns:prefix="...".
= true
```

# @lesson json-xml-compare
title: Project: JSON or XML?
summary: Compare the formats and convert an XML feed to JSON.
---
| | JSON | XML |
|---|---|---|
| Size | Smaller | Larger (closing tags) |
| Data types | Numbers, booleans, null, arrays | Everything is text (types from a schema) |
| Attributes and mixed text | No | Yes |
| Comments | No | Yes |
| Schemas | JSON Schema | DTD, XSD |
| Common in | Web APIs, config, NoSQL | Documents, feeds, enterprise and government systems |

Project: turn an XML product feed into JSON, converting the types along the way.

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

:::tip Try it yourself
Go the other way: build the XML back from the `data` dictionary with `ET.Element` and `ET.SubElement`, and print it with `ET.tostring`.
:::

```quiz
? Why does the project call int() and float() when converting?
* XML values are text, while JSON can hold real numbers
- JSON does not allow text
- Python requires it for printing
```

# @lesson json-xml-reference
title: JSON and XML quick reference
summary: Syntax and the most used functions on one page.
---
```reference javascript
{ "k": v } / [ ... ] | JSON object / array | {"tags": ["a", "b"]}
"text" / 1.5 / true / null | JSON values (double quotes only) | {"ok": true, "n": null}
JSON.parse / JSON.stringify | JavaScript | JSON.stringify(o, null, 2)
json.loads / json.dumps | Python | json.dumps(d, ensure_ascii=False)
<root> ... </root> | One XML root element | <order>...</order>
<tag attr="v">text</tag> | XML element with an attribute | <item qty="2">Tea</item>
<empty/> | Self-closing XML element | <note/>
&amp; / &lt; | Escapes in XML text | Fish &amp; chips
ET.fromstring / findall / get | Python XML | root.findall("./items/item")
DOMParser / querySelectorAll | Browser XML | doc.querySelectorAll("book")
//item[@id="3"] | XPath | //book[@lang="ar"]/title
```

:::tip Where to go next
Call a public JSON API from Python with `urllib.request` or `requests`, save the result to a file, and summarise it. For XML, read an RSS feed and print the latest titles.
:::

```quiz
? Which format supports comments and attributes?
* XML
- JSON
- Both
```
