# @lesson vue-intro
title: مقدمة في Vue
summary: ما هو Vue وكيف يربط البيانات بالصفحة.
---
**Vue** إطار JavaScript لبناء واجهات تفاعلية. تكتب قالب HTML عاديًا، وتربطه ببيانات؛ وعندما تتغير البيانات يتحدث القالب تلقائيًا.

```try html vue
<div id="app">
  <h2>{{ message }}</h2>
  <button @click="count++">ضغطت {{ count }} مرة</button>
</div>
<script>
  Vue.createApp({
    data() {
      return { message: "مرحبًا Vue", count: 0 };
    },
  }).mount("#app");
</script>
```

- `createApp({...})` ينشئ التطبيق، و`mount("#app")` يربطه بالعنصر.
- `data()` تعيد البيانات، و`{{ }}` تعرضها في القالب.

:::info في مشروع حقيقي
يُنشأ مشروع Vue عادة بالأمر `npm create vue@latest`، وتُكتب المكونات في ملفات `.vue`. الأمثلة هنا تعمل مباشرة في المتصفح.
:::

```quiz
? ماذا يحدث في Vue عندما تتغير البيانات؟
* يتحدث القالب تلقائيًا
- يجب إعادة تحميل الصفحة
- لا يتغير شيء

? الأقواس المزدوجة {{ }} تعرض البيانات داخل القالب.
= true
```

# @lesson vue-template
title: القوالب والتعبيرات
summary: عرض البيانات والتعبيرات داخل القالب.
---
```try html vue
<div id="app">
  <p>الاسم: {{ user.name }}</p>
  <p>السعر بعد الضريبة: {{ (price * 1.15).toFixed(2) }}</p>
  <p>{{ stock > 0 ? "متوفر" : "نفد" }}</p>
  <p>{{ tags.join("، ") }}</p>
</div>
<script>
  Vue.createApp({
    data() {
      return { user: { name: "ليلى" }, price: 80, stock: 3, tags: ["جديد", "مميز"] };
    },
  }).mount("#app");
</script>
```

داخل `{{ }}` يمكنك كتابة أي **تعبير** JavaScript قصير: حساب، شرط ثلاثي، استدعاء دالة.

:::warning تعبير واحد فقط
لا تكتب جملًا كاملة مثل `if` أو `let` داخل `{{ }}`؛ ضع المنطق الطويل في `methods` أو `computed`.
:::

```quiz
? ماذا يمكن أن يُكتب داخل {{ }}؟
* تعبير JavaScript قصير
- جملة if كاملة
- وسم script

? يمكن استخدام العامل الثلاثي داخل {{ }}.
= true
```

# @lesson vue-bind
title: ربط السمات v-bind
summary: ربط السمات والأصناف والتنسيق بالبيانات.
---
`v-bind:` (واختصاره `:`) يربط سمة HTML بقيمة من البيانات:

```try html vue
<div id="app">
  <img :src="image" :alt="title" width="160">
  <p :class="{ sale: onSale }" :style="{ fontSize: size + 'px' }">{{ title }}</p>
  <button :disabled="stock === 0">اشترِ</button>
  <button @click="onSale = !onSale">بدّل التخفيض</button>
</div>
<style>.sale { color: crimson; font-weight: bold; }</style>
<script>
  Vue.createApp({
    data() {
      return { image: "https://picsum.photos/160/100", title: "حقيبة جلدية", onSale: true, size: 20, stock: 0 };
    },
  }).mount("#app");
</script>
```

- `:src="image"` يأخذ القيمة من البيانات.
- `:class="{ sale: onSale }"` يضيف الصنف عندما الشرط صحيح.

```exercise html
? اربط سمة href بالمتغير url
<a ___="url">رابط</a>
= :href | v-bind:href
```

```quiz
? ما اختصار v-bind:src؟
* :src
- @src
- #src

? القيمة :class="{ active: isOn }" تضيف الصنف active عندما isOn صحيحة.
= true
```

# @lesson vue-events
title: الأحداث v-on
summary: الاستجابة للنقر والكتابة بالدوال methods.
---
`v-on:` (واختصاره `@`) يربط حدثًا بدالة:

```try html vue
<div id="app">
  <p>السلة: {{ cart }} منتجات</p>
  <button @click="add(1)">أضف واحدًا</button>
  <button @click="add(5)">أضف خمسة</button>
  <button @click="cart = 0">أفرغ</button>
  <input @keyup.enter="say" placeholder="اكتب ثم Enter">
  <p>{{ last }}</p>
</div>
<script>
  Vue.createApp({
    data() {
      return { cart: 0, last: "" };
    },
    methods: {
      add(n) {
        this.cart += n;
      },
      say(e) {
        this.last = "كتبت: " + e.target.value;
      },
    },
  }).mount("#app");
</script>
```

- الدوال في `methods`، وتصل للبيانات بـ `this`.
- `@keyup.enter` حدث بمعدّل: عند ضغط Enter فقط.

```exercise html
? أكمل لربط النقر بالدالة save
<button ___="save">حفظ</button>
= @click | v-on:click
```

```quiz
? ما اختصار v-on:click؟
- :click
* @click
- #click

? داخل methods نصل للبيانات عبر this.
= true
```

# @lesson vue-model
title: الربط الثنائي v-model
summary: ربط حقول النماذج بالبيانات في الاتجاهين.
---
`v-model` يجعل الحقل والبيانات متطابقين دائمًا: تكتب فتتغير البيانات، وتتغير البيانات فيتغير الحقل:

```try html vue
<div id="app">
  <input v-model="name" placeholder="اسمك">
  <p>أهلًا {{ name || "يا زائر" }}</p>
  <label><input type="checkbox" v-model="agree"> أوافق</label>
  <select v-model="city"><option>الرياض</option><option>القاهرة</option></select>
  <p>{{ agree ? "موافق" : "غير موافق" }} — {{ city }}</p>
  <input type="range" min="1" max="10" v-model.number="qty"> {{ qty }} × 15 = {{ qty * 15 }}
</div>
<script>
  Vue.createApp({
    data() {
      return { name: "", agree: false, city: "الرياض", qty: 1 };
    },
  }).mount("#app");
</script>
```

`v-model.number` يحوّل القيمة إلى رقم تلقائيًا.

```exercise html
? اربط الحقل بالمتغير email في الاتجاهين
<input ___="email">
= v-model
```

```quiz
? ماذا يفعل v-model؟
* يربط الحقل بالبيانات في الاتجاهين
- يربط سمة واحدة فقط
- يرسل النموذج للخادم

? المعدِّل v-model.number يحوّل القيمة إلى رقم.
= true
```

# @lesson vue-if-for
title: الشروط والقوائم
summary: v-if و v-else و v-show و v-for.
---
```try html vue
<div id="app">
  <button @click="logged = !logged">{{ logged ? "خروج" : "دخول" }}</button>
  <p v-if="logged">أهلًا بعودتك</p>
  <p v-else>سجّل دخولك</p>
  <ul>
    <li v-for="p in products" :key="p.id">
      {{ p.name }} — {{ p.price }} ريال
      <strong v-if="p.price > 50">(فاخر)</strong>
    </li>
  </ul>
  <p v-show="products.length === 0">لا توجد منتجات</p>
</div>
<script>
  Vue.createApp({
    data() {
      return {
        logged: false,
        products: [
          { id: 1, name: "قلم", price: 5 },
          { id: 2, name: "حقيبة", price: 90 },
        ],
      };
    },
  }).mount("#app");
</script>
```

- `v-if` يضيف العنصر أو يزيله، و`v-show` يخفيه بالتنسيق فقط.
- `v-for="p in products"` يكرر العنصر، ومعه `:key` فريد.

```quiz
? أي توجيه يكرر عنصرًا لكل عنصر في مصفوفة؟
- v-if
* v-for
- v-repeat

? التوجيه v-show يبقي العنصر في الصفحة ويخفيه فقط.
= true
```

# @lesson vue-computed
title: الخصائص المحسوبة
summary: قيم تُحسب من البيانات وتتحدث تلقائيًا، و watch.
---
**الخاصية المحسوبة** قيمة مشتقة من البيانات، تُعاد حسابها فقط عندما تتغير البيانات التي تعتمد عليها:

```try html vue
<div id="app">
  <input v-model="search" placeholder="ابحث">
  <ul><li v-for="n in filtered" :key="n">{{ n }}</li></ul>
  <p>عدد النتائج: {{ filtered.length }}</p>
</div>
<script>
  Vue.createApp({
    data() {
      return { search: "", names: ["سارة", "سامي", "عمر", "علي", "ليلى"] };
    },
    computed: {
      filtered() {
        return this.names.filter((n) => n.includes(this.search));
      },
    },
    watch: {
      search(value) {
        console.log("تغيّر البحث إلى", value);
      },
    },
  }).mount("#app");
</script>
```

- `computed` للقيم المشتقة (تصفية، مجموع، تنسيق).
- `watch` لتنفيذ عمل جانبي عند تغيّر قيمة (حفظ، طلب للخادم).

```quiz
? متى يُعاد حساب الخاصية المحسوبة؟
* عندما تتغير البيانات التي تعتمد عليها
- مع كل نقرة في الصفحة
- مرة واحدة فقط

? الخيار watch مناسب لتنفيذ عمل جانبي عند تغير قيمة.
= true
```

# @lesson vue-components
title: المكونات
summary: إنشاء مكوّن بخصائص props وإرسال الأحداث emit.
---
```try html vue
<div id="app">
  <product-card v-for="p in products" :key="p.id" :name="p.name" :price="p.price" @buy="total += $event"></product-card>
  <p>الإجمالي: {{ total }} ريال</p>
</div>
<script>
  const app = Vue.createApp({
    data() {
      return { total: 0, products: [{ id: 1, name: "قلم", price: 5 }, { id: 2, name: "دفتر", price: 12 }] };
    },
  });
  app.component("product-card", {
    props: ["name", "price"],
    emits: ["buy"],
    template: `
      <div style="border:1px solid #ddd;padding:8px;margin:4px">
        {{ name }} — {{ price }} ريال
        <button @click="$emit('buy', price)">اشترِ</button>
      </div>`,
  });
  app.mount("#app");
</script>
```

- `props` بيانات تصل من الأب.
- `$emit('buy', price)` يرسل حدثًا للأب، الذي يستقبله بـ `@buy`.

```quiz
? كيف يرسل المكوّن الابن حدثًا لأبيه؟
* بـ $emit
- بتغيير props
- بـ return

? الخاصية props تستقبل البيانات من المكوّن الأب.
= true
```

# @lesson vue-project
title: مشروع: سلة مشتريات
summary: تطبيق صغير يجمع ما تعلمته.
---
```try html vue
<div id="app" style="max-width: 380px">
  <div v-for="p in products" :key="p.id" style="display:flex;justify-content:space-between;margin:4px 0">
    <span>{{ p.name }} ({{ p.price }})</span>
    <span>
      <button @click="p.qty > 0 && p.qty--">−</button>
      {{ p.qty }}
      <button @click="p.qty++">+</button>
    </span>
  </div>
  <hr>
  <label><input type="checkbox" v-model="coupon"> كوبون خصم 10%</label>
  <p>المجموع: {{ subtotal }} — بعد الخصم: <strong>{{ total.toFixed(2) }}</strong></p>
  <p v-if="subtotal === 0">السلة فارغة</p>
</div>
<script>
  Vue.createApp({
    data() {
      return {
        coupon: false,
        products: [
          { id: 1, name: "قلم", price: 5, qty: 0 },
          { id: 2, name: "دفتر", price: 12, qty: 1 },
          { id: 3, name: "حقيبة", price: 90, qty: 0 },
        ],
      };
    },
    computed: {
      subtotal() {
        return this.products.reduce((s, p) => s + p.price * p.qty, 0);
      },
      total() {
        return this.coupon ? this.subtotal * 0.9 : this.subtotal;
      },
    },
  }).mount("#app");
</script>
```

:::tip طوّره بنفسك
أضف زر «احذف كل شيء»، أو احفظ السلة في `localStorage` بـ `watch`.
:::

```quiz
? لماذا subtotal خاصية محسوبة وليست بيانات عادية؟
* لأنها تُشتق من الكميات والأسعار وتتحدث تلقائيًا
- لأن البيانات العادية لا تقبل الأرقام
- لا يوجد سبب

? التوجيه v-model يعمل مع خانة الاختيار checkbox.
= true
```

# @lesson vue-reference
title: مرجع Vue
summary: أهم التوجيهات والخيارات مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي توجيه.

```reference html
{{ }} | عرض قيمة | {{ message }}
v-bind / : | ربط سمة | :src="url"
v-on / @ | حدث | @click="save"
v-model | ربط ثنائي | <input v-model="name">
v-if / v-else | عرض شرطي | <p v-if="ok">…</p>
v-show | إخفاء بالتنسيق | <p v-show="open">…</p>
v-for | تكرار | <li v-for="x in list" :key="x.id">
data() | البيانات | data() { return { n: 0 }; }
methods | الدوال | methods: { add() { … } }
computed | قيم محسوبة | computed: { total() { … } }
watch | مراقبة قيمة | watch: { q(v) { … } }
props | بيانات من الأب | props: ["title"]
$emit | حدث للأب | $emit("done", value)
createApp / mount | تشغيل التطبيق | Vue.createApp({…}).mount("#app")
```

:::tip ماذا بعد؟
أنشئ مشروعًا حقيقيًا بـ `npm create vue@latest`، وتعرّف على **Composition API** و `ref` و `reactive`.
:::
