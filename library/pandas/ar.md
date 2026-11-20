# @lesson pd-intro
title: مقدمة في Pandas
summary: ما هي Pandas ولماذا يستخدمها محللو البيانات.
---
**Pandas** مكتبة بايثون لتحليل البيانات الجدولية: تقرأ ملفات CSV وExcel وقواعد البيانات، وتنظّف البيانات، وتصفّيها، وتجمعها، وتحسب منها الإحصاءات، بسطور قليلة.

في هذه الدورة يوجد ملف مبيعات جاهز اسمه `sales.csv`. اضغط **تشغيل** (أول تشغيل يحمّل Pandas ويأخذ ثواني):

```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df.head())
print("عدد الصفوف:", len(df))
```

:::info الاسم المختصر pd
الاستيراد المتعارف عليه `import pandas as pd`، والجدول يُسمى عادة `df` اختصارًا لـ DataFrame.
:::

```quiz
? ما وظيفة Pandas الأساسية؟
* تحليل البيانات الجدولية
- رسم واجهات المواقع
- إدارة إصدارات الكود

? الدالة pd.read_csv تقرأ ملف CSV إلى جدول.
= true
```

# @lesson pd-series
title: السلسلة Series
summary: عمود واحد من البيانات مع فهرس.
---
**Series** عمود واحد من القيم، لكل قيمة **فهرس** (عنوان):

```try python
import pandas as pd

temps = pd.Series([31, 35, 29, 40], index=["السبت", "الأحد", "الاثنين", "الثلاثاء"])
print(temps)
print(temps["الأحد"])
print(temps.max(), temps.idxmax())
print(temps[temps > 30])
```

- `idxmax()` يعيد فهرس أكبر قيمة.
- العمليات والتصفية مثل NumPy تمامًا.

```quiz
? ما هي Series في Pandas؟
* عمود واحد من القيم مع فهرس
- جدول كامل
- ملف CSV

? الدالة idxmax تعيد فهرس أكبر قيمة.
= true
```

# @lesson pd-dataframe
title: الجدول DataFrame
summary: إنشاء جدول، والأعمدة، والفهرس، ونظرة سريعة.
---
**DataFrame** جدول من صفوف وأعمدة؛ كل عمود Series:

```try python
import pandas as pd

df = pd.DataFrame({
    "name": ["سارة", "عمر", "ليلى"],
    "age": [28, 35, 24],
    "city": ["الرياض", "القاهرة", "دبي"],
})
print(df)
print(df.columns.tolist())
print(df.shape)
print(df.dtypes)
```

## نظرة سريعة على أي جدول

```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
df.info()
print(df.describe())
```

```reference python
head() / tail() | أول / آخر الصفوف | df.head(3)
shape | عدد الصفوف والأعمدة | df.shape
columns | أسماء الأعمدة | df.columns
dtypes | نوع كل عمود | df.dtypes
info() | ملخص الجدول | df.info()
describe() | إحصاءات الأعمدة الرقمية | df.describe()
```

```quiz
? ماذا تعيد df.shape؟
* عدد الصفوف والأعمدة
- أسماء الأعمدة
- أول خمسة صفوف

? كل عمود في DataFrame هو Series.
= true
```

# @lesson pd-csv
title: قراءة البيانات وحفظها
summary: read_csv و to_csv، وخيارات القراءة.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"])
print(df.dtypes)

df["total"] = df["qty"] * df["price"]
df.to_csv("sales_total.csv", index=False)
print(open("sales_total.csv", encoding="utf-8").read()[:200])
```

```reference python
pd.read_csv | قراءة CSV | pd.read_csv("a.csv")
pd.read_excel | قراءة Excel | pd.read_excel("a.xlsx")
pd.read_json | قراءة JSON | pd.read_json("a.json")
parse_dates | تحويل أعمدة لتواريخ | read_csv(…, parse_dates=["date"])
df.to_csv | حفظ CSV | df.to_csv("out.csv", index=False)
df.to_excel | حفظ Excel | df.to_excel("out.xlsx")
```

:::tip index=False
بدونها يحفظ Pandas رقم الصف كعمود إضافي في الملف.
:::

```quiz
? أي خيار يمنع حفظ رقم الصف في الملف؟
* index=False
- header=False
- rows=False

? الخيار parse_dates يحوّل الأعمدة المحددة إلى تواريخ.
= true
```

# @lesson pd-select
title: اختيار الأعمدة والصفوف
summary: الأعمدة، و loc بالعناوين، و iloc بالأرقام.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df["product"].head(3))               # عمود واحد
print(df[["product", "price"]].head(3))     # عدة أعمدة
print(df.iloc[0])                            # الصف الأول بالرقم
print(df.iloc[2:5, [1, 2]])                  # صفوف وأعمدة بالأرقام
print(df.loc[3, "branch"])                   # بالعنوان
print(df.loc[0:2, "product":"qty"])
```

- `iloc` بالمواضع الرقمية (مثل القوائم).
- `loc` بالعناوين: الفهرس وأسماء الأعمدة.

```exercise python
? اختر الصف الخامس بالموضع
row = df.___[4]
= iloc
```

```quiz
? ما الفرق بين loc و iloc؟
* loc بالعناوين، و iloc بالمواضع الرقمية
- لا فرق
- iloc للأعمدة فقط

? الصيغة df[["a", "b"]] تختار عمودين.
= true
```

# @lesson pd-filter
title: التصفية
summary: الشروط، و isin، و query.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df[df["price"] > 1000])
print(df[(df["branch"] == "الرياض") & (df["qty"] >= 3)])
print(df[df["category"].isin(["أثاث", "إكسسوارات"])])
print(df.query("qty > 20"))
print(df[df["product"].str.contains("حاسوب")])
```

- `&` (و) و `|` (أو) مع أقواس حول كل شرط.
- `isin([...])` القيمة ضمن قائمة.
- `.str.contains()` بحث داخل النصوص.

```exercise python
? اختر المبيعات التي كميتها أكبر من 10
big = df[df["qty"] ___ 10]
= >
```

```quiz
? أي دالة تختار الصفوف التي قيمتها ضمن قائمة؟
* isin
- contains
- between_list

? يجب وضع كل شرط بين قوسين عند استخدام & في التصفية.
= true
```

# @lesson pd-clean
title: تنظيف البيانات
summary: القيم الناقصة والمكررة وتصحيح الأنواع.
---
البيانات الحقيقية فيها نواقص وتكرار. ملفنا فيه كمية ناقصة، وفرع ناقص، وصف مكرر:

```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df.isna().sum())               # عدد النواقص في كل عمود
print("مكرر:", df.duplicated().sum())

df = df.drop_duplicates()
df["qty"] = df["qty"].fillna(df["qty"].median())
df["branch"] = df["branch"].fillna("غير معروف")
df["qty"] = df["qty"].astype(int)
print(df.isna().sum().sum(), len(df))
```

```reference python
isna() | أين القيم الناقصة | df.isna().sum()
dropna() | حذف الصفوف الناقصة | df.dropna()
fillna() | تعبئة الناقص | df["a"].fillna(0)
duplicated() | الصفوف المكررة | df.duplicated()
drop_duplicates() | حذف المكرر | df.drop_duplicates()
astype() | تغيير النوع | df["a"].astype(int)
rename() | إعادة تسمية الأعمدة | df.rename(columns={"a": "b"})
str.strip() | حذف المسافات | df["a"].str.strip()
```

:::tip احذف أم عبّئ؟
الحذف أبسط لكنه يضيع بيانات. التعبئة بالوسيط أو بقيمة منطقية تحافظ على الصفوف؛ اختر حسب معنى البيانات.
:::

```quiz
? أي دالة تعبّئ القيم الناقصة؟
- dropna
* fillna
- isna

? الدالة drop_duplicates تحذف الصفوف المكررة.
= true
```

# @lesson pd-sort-new
title: الترتيب والأعمدة الجديدة
summary: sort_values، والأعمدة المحسوبة، و apply، والتواريخ.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"]).drop_duplicates()
df["total"] = df["qty"] * df["price"]
df["month"] = df["date"].dt.month
df["size"] = df["total"].apply(lambda t: "كبيرة" if t >= 5000 else "عادية")
print(df.sort_values("total", ascending=False).head(5)[["product", "total", "size"]])
print(df.nlargest(3, "total")[["product", "total"]])
```

- `dt.month` و `dt.year` و `dt.day_name()` لأجزاء التاريخ.
- `apply` يطبّق دالة على كل قيمة.

```exercise python
? رتّب الجدول حسب السعر من الأعلى
df.sort_values("price", ___=False)
= ascending
```

```quiz
? كيف تضيف عمودًا جديدًا محسوبًا؟
* df["total"] = df["qty"] * df["price"]
- df.add("total")
- df.new_column("total")

? الدالة nlargest تعيد الصفوف ذات القيم الأكبر.
= true
```

# @lesson pd-groupby
title: التجميع groupby
summary: الإجمالي والمتوسط لكل مجموعة، و agg، و pivot_table.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv").drop_duplicates()
df["total"] = df["qty"].fillna(0) * df["price"]

print(df.groupby("branch")["total"].sum())
print(df.groupby("category").agg(orders=("product", "count"), revenue=("total", "sum")))
print(df.pivot_table(index="branch", columns="category", values="total", aggfunc="sum", fill_value=0))
```

- `groupby("عمود")` يقسم الصفوف إلى مجموعات.
- `agg` يحسب عدة إحصاءات بأسماء تختارها.
- `pivot_table` جدول محوري كالذي في Excel.

```exercise python
? احسب متوسط السعر لكل قسم
df.groupby("category")["price"].___()
= mean
```

```quiz
? ماذا يفعل df.groupby("branch")["total"].sum()؟
* يحسب مجموع total لكل فرع
- يرتب الفروع
- يحذف الفروع المكررة

? الدالة pivot_table تنشئ جدولًا محوريًا.
= true
```

# @lesson pd-merge
title: الدمج بين الجداول
summary: merge مثل JOIN في SQL، و concat.
---
ملف `branches.csv` فيه مدير كل فرع وسنة افتتاحه. ندمجه مع المبيعات:

```try python sales
import pandas as pd

sales = pd.read_csv("sales.csv").drop_duplicates()
branches = pd.read_csv("branches.csv")
merged = sales.merge(branches, on="branch", how="left")
print(merged[["date", "branch", "manager", "product"]].head(6))
```

```reference python
merge(on=…) | دمج بعمود مشترك | a.merge(b, on="id")
how="inner" | المتطابق فقط | a.merge(b, on="id", how="inner")
how="left" | كل صفوف الأيسر | a.merge(b, on="id", how="left")
pd.concat | وضع جداول تحت بعض | pd.concat([a, b])
```

:::info مثل SQL
`merge` يعادل `JOIN`، و `how="left"` يعادل `LEFT JOIN`. لاحظ أن الصف الذي فرعه ناقص لن يجد مديرًا.
:::

```quiz
? ما المقابل في SQL للدالة merge؟
* JOIN
- GROUP BY
- UNION

? الدالة pd.concat تضع الجداول تحت بعضها.
= true
```

# @lesson pd-project
title: مشروع: تقرير المبيعات
summary: تقرير كامل من الملف الخام إلى النتائج.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"])
df = df.drop_duplicates()
df["qty"] = df["qty"].fillna(df["qty"].median()).astype(int)
df["branch"] = df["branch"].fillna("غير معروف")
df["total"] = df["qty"] * df["price"]
df["month"] = df["date"].dt.strftime("%Y-%m")

print("إجمالي الإيراد:", df["total"].sum())
print("\nالإيراد الشهري:")
print(df.groupby("month")["total"].sum())
print("\nأفضل 3 منتجات:")
print(df.groupby("product")["total"].sum().nlargest(3))
print("\nحصة كل فرع (%):")
print((df.groupby("branch")["total"].sum() / df["total"].sum() * 100).round(1))
```

:::tip طوّره بنفسك
احسب متوسط قيمة الطلب لكل فرع، أو أي شهر كان الأفضل لكل قسم.
:::

```quiz
? لماذا نحذف المكرر ونعبّئ النواقص قبل الحساب؟
* لتكون النتائج صحيحة وغير مضللة
- لأن Pandas لا تقرأ الملفات بدونها
- لتسريع الطباعة فقط

? الدالة dt.strftime("%Y-%m") تحوّل التاريخ إلى سنة وشهر.
= true
```

# @lesson pd-reference
title: مرجع Pandas
summary: أهم الدوال مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي دالة.

```reference python
pd.read_csv | قراءة CSV | pd.read_csv("a.csv")
pd.DataFrame | إنشاء جدول | pd.DataFrame({"a": [1, 2]})
head / tail | أول / آخر الصفوف | df.head()
info / describe | ملخص وإحصاءات | df.describe()
df["col"] / df[[…]] | اختيار أعمدة | df[["a", "b"]]
loc / iloc | اختيار بالعنوان / الموضع | df.loc[0, "a"]
df[df[…] > x] | التصفية | df[df["qty"] > 5]
isin / query | تصفية متقدمة | df.query("qty > 5")
isna / fillna / dropna | القيم الناقصة | df.fillna(0)
drop_duplicates | حذف المكرر | df.drop_duplicates()
astype | تغيير النوع | df["a"].astype(int)
sort_values / nlargest | الترتيب | df.sort_values("a")
apply | تطبيق دالة | df["a"].apply(f)
groupby / agg | التجميع | df.groupby("b")["a"].sum()
pivot_table | جدول محوري | df.pivot_table(index="b", values="a")
merge / concat | الدمج | a.merge(b, on="id")
dt.month / dt.year | أجزاء التاريخ | df["d"].dt.month
to_csv / to_excel | الحفظ | df.to_csv("out.csv", index=False)
```

:::tip ماذا بعد؟
جرّب تحليل ملف حقيقي من عملك: مبيعات، حضور، أو طلبات. وابدأ برسم النتائج بمكتبة **Matplotlib**.
:::
