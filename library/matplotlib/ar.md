# @lesson mpl-intro
title: مقدمة Matplotlib
summary: ما هي Matplotlib، وواجهة pyplot، وأول رسم خطي لك.
---
**Matplotlib** أشهر مكتبة رسوم بيانية في Python. ببضعة أسطر تحوّل الأرقام إلى رسوم خطية وأعمدة ومدرجات تكرارية وغيرها، وتحفظها صورًا للتقارير. وتستخدمها pandas ومكتبات كثيرة من الداخل.

```try python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
visitors = [820, 940, 1100, 1050, 1300, 1490]

plt.plot(months, visitors)
plt.title("Website visitors")
plt.xlabel("Month")
plt.ylabel("Visitors")
print("chart ready")
```

- `import matplotlib.pyplot as plt` هي الطريقة المعتادة لاستيرادها.
- `plt.plot(x, y)` ترسم خطًا، و `title` و `xlabel` و `ylabel` تضيف النصوص.
- هنا يظهر الرسم تحت الناتج. وفي سكربت على جهازك تستدعي `plt.show()` لفتح نافذة، أو `plt.savefig("chart.png")` لحفظ ملف.

:::info تشغيل الأمثلة
ترسم Python نفسها الرسوم داخل متصفحك. وأول تشغيل يحمّل Matplotlib وقد يستغرق بضع ثوانٍ.
:::

:::warning النص العربي داخل الرسوم
لا تصل Matplotlib الحروف العربية ببعضها ولا تعرضها من اليمين لليسار بشكل صحيح، لذلك كُتبت عناوين الرسوم في الأمثلة بالإنجليزية. وفي مشاريعك يمكن استخدام مكتبتي `arabic_reshaper` و `python-bidi` لتجهيز النص العربي قبل رسمه.
:::

```quiz
? ما الطريقة المعتادة لاستيراد Matplotlib؟
* import matplotlib.pyplot as plt
- import matplotlib as plot
- from charts import plt

? يحفظ plt.savefig("chart.png") الرسم كملف صورة.
= true
```

# @lesson mpl-line
title: الرسوم الخطية
summary: عدة خطوط، والعلامات، وأنماط الخطوط، والألوان، ومفتاح الرسم، والشبكة.
---
```try python
import matplotlib.pyplot as plt

months = range(1, 13)
cairo = [14, 16, 19, 23, 27, 29, 30, 30, 28, 25, 20, 16]
alex = [13, 14, 16, 19, 22, 25, 26, 27, 26, 23, 19, 15]

plt.figure(figsize=(7, 3.5))
plt.plot(months, cairo, marker="o", color="#b45309", label="Cairo")
plt.plot(months, alex, marker="s", linestyle="--", color="#0e7490", label="Alexandria")
plt.title("Average temperature by month")
plt.xlabel("Month")
plt.ylabel("°C")
plt.xticks(list(months))
plt.grid(alpha=0.3)
plt.legend()
print("two lines, one legend")
```

```reference python
plt.plot(x, y) | رسم خطي | plt.plot(days, sales)
marker="o" | علامات النقاط (o s ^ x .) | marker="s"
linestyle="--" | نمط الخط (- -- : -.) | linestyle=":"
color="..." / label="..." | اللون والاسم في المفتاح | color="#4338ca", label="2025"
plt.legend() / plt.grid() | مفتاح الرسم / خطوط الشبكة | plt.grid(alpha=0.3)
plt.figure(figsize=(w, h)) | الحجم بالبوصة | plt.figure(figsize=(8, 4))
plt.xticks(...) / plt.ylim(a, b) | علامات المحور / مداه | plt.ylim(0, 100)
```

```exercise python
? اعرض على الرسم الأسماء المعطاة بـ label=...
plt.___()
= legend
```

```quiz
? أي معامل يرسم خطًا متقطعًا؟
* linestyle="--"
- marker="--"
- color="dashed"
```

# @lesson mpl-bar
title: رسوم الأعمدة
summary: الأعمدة الرأسية والأفقية، والترتيب، وعرض القيم، والأعمدة المجمّعة.
---
```try python
import matplotlib.pyplot as plt
import numpy as np

branches = ["Cairo", "Giza", "Alex", "Tanta", "Aswan"]
sales = [420, 310, 365, 140, 95]

order = np.argsort(sales)                      # رتّب ليسهل قراءة الرسم
plt.figure(figsize=(6, 3))
bars = plt.barh(np.array(branches)[order], np.array(sales)[order], color="#6366f1")
plt.bar_label(bars, padding=3)                 # الأرقام عند نهاية كل عمود
plt.title("Sales by branch (thousand EGP)")
plt.xlim(0, 480)

plt.figure(figsize=(6, 3))
quarters = np.arange(4)
width = 0.38
plt.bar(quarters - width / 2, [120, 150, 170, 210], width, label="2024", color="#94a3b8")
plt.bar(quarters + width / 2, [140, 165, 200, 260], width, label="2025", color="#4338ca")
plt.xticks(quarters, ["Q1", "Q2", "Q3", "Q4"])
plt.title("Revenue by quarter")
plt.legend()
print("two charts drawn")
```

كل `plt.figure()` تبدأ رسمًا جديدًا، لذلك ينتج هذا المثال صورتين.

```reference python
plt.bar(x, heights) | أعمدة رأسية | plt.bar(names, values)
plt.barh(y, widths) | أعمدة أفقية (مناسبة للأسماء الطويلة) | plt.barh(names, values)
plt.bar_label(bars) | كتابة القيم على الأعمدة | plt.bar_label(bars, fmt="%.0f")
width / offsets | أعمدة مجمّعة متجاورة | plt.bar(x - w/2, a, w)
np.argsort(values) | ترتيب القيم | order = np.argsort(values)
```

:::tip الأعمدة تبدأ من الصفر
يُقرأ طول العمود كحجم، لذلك يجب أن يبدأ محور القيم في رسم الأعمدة من الصفر. أما الرسم الخطي فيمكنه التكبير على نطاق محدد.
:::

```exercise python
? ارسم أعمدة أفقية
plt.___(names, values)
= barh
```

```quiz
? متى تكون الأعمدة الأفقية اختيارًا أفضل؟
* عندما تكون أسماء الفئات طويلة أو كثيرة
- مع الأرقام السالبة فقط
- عند وجود فئتين فقط
```

# @lesson mpl-scatter
title: رسوم التشتت
summary: العلاقة بين رقمين، والترميز باللون والحجم، وخط الاتجاه.
---
```try python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
hours = rng.uniform(1, 12, 60)
score = 40 + 4.5 * hours + rng.normal(0, 6, 60)
team = rng.integers(0, 3, 60)

plt.figure(figsize=(6, 4))
points = plt.scatter(hours, score, c=team, cmap="viridis", s=40, alpha=0.8)
slope, intercept = np.polyfit(hours, score, 1)          # الخط المستقيم الأنسب
xs = np.linspace(1, 12, 50)
plt.plot(xs, slope * xs + intercept, color="crimson", label=f"trend: +{slope:.1f} per hour")
plt.colorbar(points, label="team")
plt.xlabel("Training hours")
plt.ylabel("Test score")
plt.legend()
print("correlation:", round(np.corrcoef(hours, score)[0, 1], 2))
```

```reference python
plt.scatter(x, y) | رسم تشتت | plt.scatter(age, salary)
c=values, cmap="..." | التلوين حسب قيمة | c=team, cmap="viridis"
s=size / alpha | حجم النقطة / الشفافية | s=20, alpha=0.5
plt.colorbar() | مفتاح مقياس الألوان | plt.colorbar(points)
np.polyfit(x, y, 1) | خط مستقيم مناسب للبيانات | slope, b = np.polyfit(x, y, 1)
```

```exercise python
? اجعل النقاط نصف شفافة
plt.scatter(x, y, ___=0.5)
= alpha
```

```quiz
? ماذا يُظهر رسم التشتت بأفضل شكل؟
* العلاقة بين متغيرين رقميين
- أجزاء من كل
- تغير قيمة واحدة مع الزمن فقط
```

# @lesson mpl-distribution
title: المدرجات التكرارية والصناديق
summary: كيف تتوزع القيم: الفئات، ومقارنة المجموعات، والقيم الشاذة.
---
```try python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
cairo = rng.normal(28, 4, 300)                 # وقت التوصيل بالدقائق
giza = rng.normal(35, 7, 300)

fig, (left, right) = plt.subplots(1, 2, figsize=(9, 3.5))
left.hist(cairo, bins=20, alpha=0.7, label="Cairo", color="#4338ca")
left.hist(giza, bins=20, alpha=0.7, label="Giza", color="#f59e0b")
left.set_title("Delivery time (minutes)")
left.legend()

right.boxplot([cairo, giza], labels=["Cairo", "Giza"])
right.set_title("Same data as box plots")
print("medians:", round(float(np.median(cairo)), 1), round(float(np.median(giza)), 1))
```

- **المدرج التكراري** يقسم القيم إلى نطاقات (`bins`) ويعرض عدد القيم في كل نطاق.
- **الرسم الصندوقي** يعرض الوسيط (الخط)، والنصف الأوسط من البيانات (الصندوق)، والانتشار (الشوارب)، والقيم الشاذة (النقاط).

```reference python
plt.hist(values, bins=n) | مدرج تكراري | plt.hist(ages, bins=10)
plt.boxplot([a, b], labels=[...]) | صناديق متجاورة | plt.boxplot([x, y])
fig, (a, b) = plt.subplots(1, 2) | رسمان في شكل واحد | fig, axes = plt.subplots(2, 2)
ax.set_title / ax.legend | دوال على رسم واحد (axes) | ax.set_xlabel("min")
```

```exercise python
? قسّم القيم إلى 30 نطاقًا
plt.hist(values, ___=30)
= bins
```

```quiz
? أي رسم يُظهر القيم الشاذة كنقاط منفصلة؟
* الرسم الصندوقي
- الرسم الدائري
- الرسم الخطي
```

# @lesson mpl-pie
title: الرسوم الدائرية والحلقية، ومتى لا نستخدمها
summary: أجزاء من كل، والنسب المئوية، ولماذا تكون الأعمدة غالبًا أفضل.
---
```try python
import matplotlib.pyplot as plt

channels = ["Search", "Social", "Email", "Direct"]
signups = [420, 260, 180, 140]

fig, (left, right) = plt.subplots(1, 2, figsize=(9, 3.5))
left.pie(signups, labels=channels, autopct="%1.0f%%", startangle=90,
         wedgeprops={"width": 0.45})                        # العرض يصنع شكلًا حلقيًا
left.set_title("Signups by channel")

right.barh(channels[::-1], signups[::-1], color="#6366f1")
right.set_title("The same data as bars")
print("largest share:", channels[signups.index(max(signups))])
```

:::tip الدائري لأجزاء قليلة فقط
يقارن الناس الأطوال بدقة أكبر بكثير من الزوايا. استخدم الرسم الدائري أو الحلقي فقط لجزأين إلى أربعة أجزاء من كل واحد، عندما تكون الرسالة "هذا الجزء نحو النصف". ولأي شيء آخر فرسم الأعمدة المرتب أوضح.
:::

```reference python
plt.pie(values, labels=...) | رسم دائري | plt.pie(shares, labels=names)
autopct="%1.0f%%" | إظهار النسب المئوية | autopct="%1.1f%%"
startangle=90 | البدء من الأعلى | startangle=90
wedgeprops={"width": w} | فتحة الحلقة | wedgeprops={"width": 0.4}
```

```quiz
? لماذا يكون رسم الأعمدة غالبًا أوضح من الرسم الدائري؟
* لأن الناس يقارنون الأطوال بدقة أكبر من الزوايا
- لأن الرسم الدائري لا يعرض النسب
- لأن رسم الأعمدة يستخدم ألوانًا أكثر
```

# @lesson mpl-subplots
title: الأشكال والمحاور والرسوم الفرعية
summary: الواجهة الكائنية: fig و ax، وشبكات الرسوم، والمحاور المشتركة.
---
لأي شيء أكثر من رسم سريع واحد، استخدم الأسلوب **الكائني**: `fig` هو الصورة كلها، وكل `ax` رسم واحد داخلها.

```try python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
fig, axes = plt.subplots(2, 2, figsize=(8, 5), sharex=True)
axes[0, 0].plot(x, np.sin(x), color="#4338ca")
axes[0, 0].set_title("sin(x)")
axes[0, 1].plot(x, np.cos(x), color="#0e7490")
axes[0, 1].set_title("cos(x)")
axes[1, 0].fill_between(x, np.sin(x) ** 2, color="#f59e0b", alpha=0.6)
axes[1, 0].set_title("sin²(x)")
axes[1, 1].plot(x, np.sin(x) * np.exp(-x / 3), color="#be185d")
axes[1, 1].set_title("damped wave")
for ax in axes.flat:
    ax.grid(alpha=0.3)
fig.suptitle("Four charts, one figure")
fig.tight_layout()
print("charts in the figure:", len(axes.flat))
```

```reference python
fig, ax = plt.subplots() | رسم واحد بالأسلوب الكائني | ax.plot(x, y)
plt.subplots(rows, cols) | شبكة من الرسوم | fig, axes = plt.subplots(2, 3)
axes[r, c] / axes.flat | رسم واحد / كل الرسوم | for ax in axes.flat: ...
ax.set_title / set_xlabel / set_ylim | دوال بدل plt.title... | ax.set_ylim(0, 1)
sharex=True / sharey=True | نفس مدى المحور | plt.subplots(2, 1, sharex=True)
fig.suptitle / fig.tight_layout() | عنوان عام / إصلاح التداخل | fig.tight_layout()
```

```exercise python
? أنشئ شبكة رسوم من صفين وثلاثة أعمدة
fig, axes = plt.___(2, 3)
= subplots
```

```quiz
? في الأسلوب الكائني، ما هو ax؟
* رسم واحد (محاور) داخل الشكل
- ملف الصورة كله
- المحور x فقط
```

# @lesson mpl-customize
title: التعليقات التوضيحية والتنسيق
summary: الإشارة إلى النقاط المهمة، وتنسيق المحاور، والأنماط، وألوان تناسب الجميع.
---
```try python
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.style.use("ggplot")
days = list(range(1, 15))
users = [120, 135, 150, 148, 160, 158, 300, 290, 310, 305, 320, 330, 335, 350]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(days, users, color="#4338ca", linewidth=2.5)
ax.annotate("Launch campaign", xy=(7, 300), xytext=(2.5, 320),
            arrowprops={"arrowstyle": "->", "color": "#334155"})
ax.axvline(7, color="#94a3b8", linestyle=":")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f} users"))
ax.set_title("Daily active users", loc="left", fontsize=13, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Day")
print("styles available:", len(plt.style.available))
```

```reference python
ax.annotate(text, xy, xytext, arrowprops) | الإشارة إلى شيء مهم | ax.annotate("Peak", xy=(5, 90))
ax.axvline / ax.axhline | خطوط مرجعية | ax.axhline(target, linestyle="--")
plt.style.use("...") | مظهر جاهز | plt.style.use("ggplot")
FuncFormatter | تسميات مخصصة للمحاور | FuncFormatter(lambda v, _: f"{v:.0%}")
ax.spines[...].set_visible(False) | إزالة حدود الرسم | ax.spines[["top", "right"]].set_visible(False)
cmap="viridis" | ألوان تناسب من لديهم عمى ألوان | plt.scatter(x, y, c=v, cmap="viridis")
```

:::tip الرسم يقول شيئًا واحدًا
ضع الرسالة الأساسية في العنوان ("تضاعف المستخدمون بعد الحملة")، وأبرز الخط أو العمود المهم، واحذف الزخرفة التي لا تفيد القارئ.
:::

```exercise python
? أضف خطًا مرجعيًا أفقيًا عند القيمة المستهدفة
ax.___(target, linestyle="--")
= axhline
```

```quiz
? فيمَ تُستخدم annotate()؟
* إضافة تسمية وسهم يشيران إلى موضع مهم
- حفظ الرسم
- تغيير نوع الرسم
```

# @lesson mpl-pandas
title: رسم بيانات pandas
summary: DataFrame.plot، والتجميع قبل الرسم، وحفظ الصور.
---
```try python
import pandas as pd
import matplotlib.pyplot as plt

orders = pd.DataFrame({
    "month": ["2025-01", "2025-01", "2025-02", "2025-02", "2025-03", "2025-03", "2025-04", "2025-04"],
    "channel": ["Online", "Store"] * 4,
    "revenue": [120, 200, 150, 190, 210, 185, 260, 180],
})

table = orders.pivot_table(index="month", columns="channel", values="revenue", aggfunc="sum")
print(table)

ax = table.plot(kind="bar", figsize=(6, 3.5), color=["#4338ca", "#94a3b8"], rot=0)
ax.set_title("Revenue by channel")
ax.set_ylabel("thousand EGP")

ax2 = table.sum(axis=1).plot(kind="line", marker="o", figsize=(6, 3), color="#0e7490")
ax2.set_title("Total revenue")

plt.gcf().savefig("total_revenue.png", dpi=80)        # الحفظ في ملف
print("saved total_revenue.png")
```

```reference python
df.plot(kind="line" / "bar" / "barh" / "hist" / "scatter") | الرسم مباشرة من DataFrame | df.plot(kind="bar", x="name", y="sales")
df.pivot_table(index, columns, values, aggfunc) | إعادة تشكيل البيانات قبل الرسم | df.pivot_table(index="month", columns="channel", values="rev")
series.plot() | رسم عمود واحد | df["sales"].plot()
rot=0 | إبقاء تسميات المحور أفقية | df.plot(kind="bar", rot=0)
fig.savefig("file.png", dpi=...) | حفظ الصورة | fig.savefig("chart.png", dpi=150)
```

```exercise python
? ارسم DataFrame كرسم أعمدة
df.plot(kind="___")
= bar
```

```quiz
? ماذا ترجع df.plot() لتكمل التخصيص؟
* كائن محاور (ax)
- DataFrame جديدًا
- ملف صورة
```

# @lesson mpl-project
title: مشروع: لوحة مبيعات في صفحة واحدة
summary: أربعة رسوم تجيب عن أربعة أسئلة في شكل واحد.
---
```try python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
days = pd.date_range("2025-01-01", periods=90, freq="D")
df = pd.DataFrame({
    "day": np.tile(days, 3),
    "branch": np.repeat(["Cairo", "Giza", "Alex"], 90),
})
base = df["branch"].map({"Cairo": 52, "Giza": 38, "Alex": 44})
trend = np.tile(np.linspace(0, 12, 90), 3)
df["orders"] = (base + trend + rng.normal(0, 6, len(df))).round().clip(lower=0)
df["avg_value"] = rng.normal(180, 25, len(df)).round()

fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
fig.suptitle("Q1 sales dashboard", fontsize=15, fontweight="bold")

daily = df.groupby("day")["orders"].sum()
axes[0, 0].plot(daily.index, daily.rolling(7).mean(), color="#4338ca")
axes[0, 0].set_title("1. Are orders growing? (7-day average)")
axes[0, 0].tick_params(axis="x", labelrotation=30)

by_branch = df.groupby("branch")["orders"].sum().sort_values()
bars = axes[0, 1].barh(by_branch.index, by_branch.values, color="#0e7490")
axes[0, 1].bar_label(bars, fmt="%.0f", padding=3)
axes[0, 1].set_title("2. Which branch sells most?")

axes[1, 0].hist(df["avg_value"], bins=20, color="#f59e0b")
axes[1, 0].set_title("3. How big is a typical order? (EGP)")

weekday = df.assign(wd=df["day"].dt.day_name().str[:3]).groupby("wd")["orders"].mean()
weekday = weekday.reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
axes[1, 1].bar(weekday.index, weekday.values, color="#be185d")
axes[1, 1].set_title("4. Which weekday is busiest?")

for ax in axes.flat:
    ax.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(hspace=0.5, wspace=0.3)
print("total orders:", int(df["orders"].sum()), "| best branch:", by_branch.index[-1])
```

:::tip اجعله مشروعك
استبدل البيانات المولّدة بملف CSV من عملك (`pd.read_csv`)، واحتفظ بالأسئلة الأربعة، وحوّل العناوين إلى إجابات، مثل "القاهرة تبيع أكثر من الجيزة بنسبة 30%".
:::

```quiz
? لماذا يطرح عنوان كل رسم في المشروع سؤالًا؟
* ليكون لكل رسم هدف واضح للقارئ
- لأن Matplotlib تشترط العناوين
- لتكبير الشكل
```

# @lesson mpl-reference
title: مرجع Matplotlib السريع
summary: أنواع الرسوم وأهم الإعدادات والممارسات الجيدة في صفحة واحدة.
---
```reference python
plt.plot / ax.plot | رسم خطي | ax.plot(x, y, marker="o")
plt.bar / plt.barh | رسوم الأعمدة | ax.barh(names, values)
plt.scatter | رسم تشتت | ax.scatter(x, y, c=v, cmap="viridis")
plt.hist / plt.boxplot | التوزيعات | ax.hist(values, bins=20)
plt.pie | أجزاء من كل (أجزاء قليلة فقط) | ax.pie(shares, autopct="%1.0f%%")
fig, axes = plt.subplots(r, c) | عدة رسوم | axes[0, 1].plot(...)
title / xlabel / ylabel / legend | النصوص | ax.set_title("Sales")
annotate / axhline | الإبراز | ax.axhline(100, linestyle="--")
plt.style.use / spines | المظهر | plt.style.use("ggplot")
df.plot(kind=...) | من pandas | df.plot(kind="bar")
savefig("file.png", dpi=...) | الحفظ | fig.savefig("out.png", dpi=150)
```

:::tip الخطوة التالية
أعد رسم مخطط من تقرير في عملك ثم حسّنه: عنوان يقول النتيجة، وأعمدة مرتبة، وألوان أقل. وللرسوم التفاعلية على الويب انظر Plotly، وللرسوم الإحصائية بكود أقل انظر seaborn.
:::

```quiz
? أي استدعاء يضع عدة رسوم في شكل واحد؟
* plt.subplots
- plt.legend
- plt.savefig
```
