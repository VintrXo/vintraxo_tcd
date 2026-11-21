# @lesson ml-intro
title: ما هو تعلّم الآلة
summary: تعلّم القواعد من الأمثلة بدل كتابتها يدويًا، وأنواع المشكلات الأساسية.
---
في البرمجة العادية تكتب القواعد بنفسك: "إذا زاد الطلب عن 1000 فأعطِ خصم 10%". أما في **تعلّم الآلة** فتعطي الحاسوب **أمثلة** كثيرة مع إجاباتها الصحيحة، فيستخرج القاعدة بنفسه. والنتيجة **نموذج** يستطيع الإجابة عن حالات جديدة.

| النوع | السؤال | مثال |
|---|---|---|
| الانحدار (Regression) | كم؟ | توقع سعر منزل أو مبيعات الشهر القادم |
| التصنيف (Classification) | أي فئة؟ | بريد مزعج أم لا، ونوع الزهرة |
| التجميع (Clustering) | ما العناصر المتشابهة؟ | تقسيم العملاء حسب سلوكهم بدون إجابات معطاة |

النوعان الأولان **تعلّم موجَّه** (للأمثلة إجابات تسمى **التسميات labels**)، والتجميع **تعلّم غير موجَّه** (بلا إجابات، والنموذج يكتشف البنية بنفسه).

```try python
# أبسط "نموذج" ممكن: تعلّم القاعدة من الأمثلة واستخدمها للتوقع
hours = [1, 2, 3, 4, 5]
scores = [52, 58, 65, 70, 77]

slope = (scores[-1] - scores[0]) / (hours[-1] - hours[0])   # متعلَّم من البيانات
start = scores[0] - slope * hours[0]

def predict(h):
    return round(start + slope * h, 1)

print("learned rule: score =", round(start, 1), "+", round(slope, 2), "x hours")
print("prediction for 6 hours:", predict(6))
```

:::info أدوات هذه الدورة
تستخدم الأمثلة مكتبة **scikit-learn**، أشهر مكتبة Python لتعلّم الآلة التقليدي، مع NumPy. وتعمل داخل متصفحك؛ وأول تشغيل يحمّل المكتبات وقد يستغرق بضع ثوانٍ.
:::

```quiz
? نموذج يتوقع مبيعات الشهر القادم بالمال يحل أي نوع من المشكلات؟
* الانحدار
- التصنيف
- التجميع

? في التعلّم غير الموجَّه تأتي الأمثلة مع إجاباتها الصحيحة.
= false
> التعلّم غير الموجَّه بلا تسميات؛ والنموذج يبحث عن بنية مثل المجموعات.
```

# @lesson ml-data
title: الخصائص والتسميات وتقسيم البيانات
summary: X و y، وبيانات زهرة السوسن، ولماذا نحتفظ بمجموعة اختبار.
---
بيانات تعلّم الآلة جدول: كل **صف** مثال واحد، وأعمدة المدخلات هي **الخصائص (features)** ونرمز لها `X`، والعمود الذي نريد توقعه هو **التسمية (label)** أو الهدف `y`.

```try python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X, y = iris.data, iris.target
print("shape of X:", X.shape)            # 150 زهرة، و 4 قياسات لكل منها
print("features:", iris.feature_names)
print("classes:", list(iris.target_names))
print("first flower:", X[0], "-> class", y[0])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("train:", X_train.shape[0], "rows | test:", X_test.shape[0], "rows")
```

- يتعلّم النموذج من مجموعة **التدريب** فقط.
- **مجموعة الاختبار** تبقى مخفية أثناء التدريب، وتُستخدم مرة واحدة في النهاية لتقدير أداء النموذج على بيانات جديدة.
- `random_state` يجعل التقسيم نفسه في كل تشغيل، و `stratify=y` يحافظ على نسبة الفئات نفسها في الجزأين.

```reference python
X / y | الخصائص / التسمية | X = df[["age", "salary"]]; y = df["left"]
train_test_split | التقسيم إلى تدريب واختبار | train_test_split(X, y, test_size=0.2)
random_state | عشوائية قابلة للتكرار | random_state=42
stratify=y | نفس نسب الفئات في المجموعتين | stratify=y
load_iris / load_diabetes | بيانات صغيرة مدمجة | load_iris(as_frame=True)
```

:::warning لا تختبر أبدًا على بيانات التدريب
يستطيع النموذج حفظ صفوف التدريب. وقياسه على الصفوف نفسها يعطي نتيجة رائعة بلا أي معنى. قيّمه دائمًا على بيانات لم يرها.
:::

```exercise python
? قسّم البيانات بحيث تذهب 20% منها لمجموعة الاختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___)
= 0.2 | .2
```

```quiz
? ما التسمية في بيانات منازل تُستخدم لتوقع أسعارها؟
* عمود السعر
- عدد الغرف
- رقم الصف

? تُستخدم مجموعة الاختبار لتدريب النموذج.
= false
```

# @lesson ml-linear-regression
title: الانحدار الخطي
summary: رسم خط مستقيم لتوقع رقم، وقراءة معاملاته.
---
**الانحدار الخطي** يتوقع رقمًا كمجموع موزون للخصائص: `y = b + w1·x1 + w2·x2 + ...`. والتدريب يبحث عن الأوزان التي تجعل التوقعات أقرب ما يمكن للقيم الحقيقية.

```try python
import numpy as np
from sklearn.linear_model import LinearRegression

# المساحة بالمتر المربع، والغرف -> السعر بالآلاف
X = np.array([[50, 1], [65, 2], [80, 2], [95, 3], [110, 3], [130, 4], [150, 4], [170, 5]])
y = np.array([420, 540, 640, 760, 850, 1010, 1150, 1300])

model = LinearRegression()
model.fit(X, y)                      # تعلّم الأوزان

print("intercept:", round(model.intercept_, 1))
print("weight per m2:", round(model.coef_[0], 2), "| weight per room:", round(model.coef_[1], 1))
new_flats = np.array([[100, 3], [60, 1]])
print("predicted prices:", model.predict(new_flats).round(0))
```

كل نماذج scikit-learn تعمل بالطريقة نفسها:

1. أنشئ النموذج: `model = LinearRegression()`
2. درّبه: `model.fit(X_train, y_train)`
3. استخدمه: `model.predict(X_new)`

```reference python
LinearRegression() | نموذج الخط المستقيم | from sklearn.linear_model import LinearRegression
model.fit(X, y) | التعلّم من الأمثلة | model.fit(X_train, y_train)
model.predict(X) | توقع قيم جديدة | model.predict([[100, 3]])
coef_ / intercept_ | الأوزان المتعلَّمة / الثابت | model.coef_
```

:::tip اقرأ الأوزان
تخبرك المعاملات بمقدار تغير التوقع عندما تزيد خاصية واحدة بمقدار 1 وتبقى الأخرى ثابتة. ولا تقارن بينها إلا إذا كانت الخصائص بمقاييس متقاربة.
:::

```exercise python
? درّب النموذج على X و y
model.___(X, y)
= fit
```

```quiz
? أي دالة تُنتج توقعات لبيانات جديدة؟
* predict
- fit
- score
```

# @lesson ml-regression-metrics
title: قياس نماذج الانحدار
summary: MAE و RMSE و R²، والمقارنة بخط أساس بسيط.
---
```try python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

for name, model in [("baseline (mean)", DummyRegressor()), ("linear regression", LinearRegression())]:
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    print(f"{name:18} MAE={mae:6.1f}  RMSE={rmse:6.1f}  R2={r2:5.2f}")
```

| المقياس | المعنى | الأفضل عندما |
|---|---|---|
| MAE | متوسط حجم الخطأ بوحدة الهدف نفسها | يكون أقل |
| RMSE | مثل MAE لكن الأخطاء الكبيرة تُحسب أكثر | يكون أقل |
| R² | نسبة التباين التي يفسرها النموذج (1 = مثالي، 0 = ليس أفضل من المتوسط) | يكون أعلى |

:::tip قارن دائمًا بخط أساس
`DummyRegressor` يتوقع المتوسط في كل مرة. وإذا لم يكن نموذجك أفضل منه بوضوح فهو لم يتعلّم شيئًا مفيدًا.
:::

```exercise python
? استورد المقياس الذي يعطي متوسط الخطأ المطلق
from sklearn.metrics import ___
= mean_absolute_error
```

```quiz
? ماذا تعني قيمة R² تساوي 0؟
* النموذج ليس أفضل من توقع المتوسط
- النموذج مثالي
- النموذج بلا أخطاء

? يعاقب RMSE الأخطاء الكبيرة أكثر مما يفعل MAE.
= true
```

# @lesson ml-classification
title: التصنيف بالانحدار اللوجستي
summary: توقع فئة، وقراءة الاحتمالات، وقياس الدقة.
---
**التصنيف** يتوقع فئة. ورغم اسمه، فإن **الانحدار اللوجستي** نموذج تصنيف: يعطي احتمالًا لكل فئة.

```try python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=1, stratify=iris.target
)

clf = LogisticRegression(max_iter=500)
clf.fit(X_train, y_train)

print("test accuracy:", round(clf.score(X_test, y_test), 3))
flower = [[6.1, 2.8, 4.7, 1.2]]
print("predicted class:", iris.target_names[clf.predict(flower)[0]])
probs = clf.predict_proba(flower)[0]
for name, p in zip(iris.target_names, probs):
    print(f"  {name:10} {p:.2f}")
```

```reference python
LogisticRegression(max_iter=...) | مصنِّف خطي باحتمالات | LogisticRegression(max_iter=1000)
model.score(X, y) | الدقة في المصنِّفات | clf.score(X_test, y_test)
predict_proba | احتمال كل فئة | clf.predict_proba(X_new)
classes_ | الفئات بالترتيب | clf.classes_
```

:::tip الاحتمالات مفيدة
بدل إجابة نعم/لا، تخبرك `predict_proba` بمدى ثقة النموذج. ويمكنك التصرف فقط عندما يكون واثقًا، مثلًا مراجعة طلبات القروض يدويًا عندما يكون الاحتمال بين 0.4 و 0.6.
:::

```exercise python
? احصل على احتمال كل فئة للبيانات X_new
clf.___(X_new)
= predict_proba
```

```quiz
? أي نوع من المشكلات يحله الانحدار اللوجستي؟
* التصنيف
- انحدار الأسعار
- التجميع
```

# @lesson ml-classification-metrics
title: قياس المصنِّفات
summary: مصفوفة الالتباس، والدقة الإيجابية، والاستدعاء، ولماذا قد تخدعك الدقة العامة.
---
الدقة وحدها قد تخدعك. إذا كانت 5% فقط من المعاملات احتيالًا، فإن نموذجًا يقول دائمًا "ليست احتيالًا" دقيق بنسبة 95% وعديم الفائدة تمامًا.

```try python
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

# 1 = احتيال، 0 = عادي (الإجابات الحقيقية وتوقعات نموذج)
actual    = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
predicted = [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()
print("true negatives", tn, "| false positives", fp, "| false negatives", fn, "| true positives", tp)
print("accuracy :", accuracy_score(actual, predicted))
print("precision:", round(precision_score(actual, predicted), 2), "(of the alarms, how many were real fraud)")
print("recall   :", round(recall_score(actual, predicted), 2), "(of the real fraud, how much we caught)")
print("F1       :", round(f1_score(actual, predicted), 2))

always_normal = [0] * len(actual)
print("'always normal' accuracy:", accuracy_score(actual, always_normal), "recall:", recall_score(actual, always_normal))
```

| | التوقع: لا | التوقع: نعم |
|---|---|---|
| **الحقيقة: لا** | سلبي صحيح (TN) | إيجابي خاطئ (FP) |
| **الحقيقة: نعم** | سلبي خاطئ (FN) | إيجابي صحيح (TP) |

- **الدقة الإيجابية (Precision)** = TP / (TP + FP): عندما يقول النموذج نعم، كم مرة يكون محقًا؟
- **الاستدعاء (Recall)** = TP / (TP + FN): من كل حالات نعم الحقيقية، كم وجد منها؟
- **F1** يجمع المقياسين في رقم واحد.

:::tip اختر المقياس حسب تكلفة الخطأ
تفويت عملية احتيال (سلبي خاطئ) أغلى من فحص دفعة عادية (إيجابي خاطئ)، لذلك تهتم نماذج الاحتيال بالاستدعاء أكثر. أما فلتر البريد المزعج الذي يخفي رسائل حقيقية فالإيجابي الخاطئ عنده مكلف، فيهتم بالدقة الإيجابية.
:::

```quiz
? اختبار لمرض يجب أن يفوّت أقل عدد ممكن من المرضى. أي مقياس هو الأهم؟
* الاستدعاء (Recall)
- الدقة الإيجابية (Precision)
- الدقة العامة (Accuracy)

? يمكن أن تكون دقة النموذج عالية ويبقى عديم الفائدة مع الفئات النادرة.
= true
```

# @lesson ml-knn-scaling
title: أقرب الجيران وتوحيد مقاييس الخصائص
summary: التصنيف بالأمثلة المتشابهة، ولماذا يجب أن تكون الخصائص بمقياس واحد.
---
خوارزمية **أقرب الجيران (KNN)** تصنّف المثال الجديد بالنظر إلى أقرب `k` أمثلة تدريب وأخذ رأي الأغلبية. وهي تعتمد على المسافات، لذلك فإن خاصية بالآلاف (الراتب) تطغى على خاصية بالآحاد (سنوات الخبرة) ما لم **نوحّد مقاييسها**.

```try python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
n = 200
experience = rng.uniform(0, 10, n)              # سنوات
salary = rng.uniform(3000, 30000, n)            # لا علاقة له بالتسمية
promoted = (experience + rng.normal(0, 1, n) > 5).astype(int)
X = np.column_stack([experience, salary])
X_train, X_test, y_train, y_test = train_test_split(X, promoted, test_size=0.3, random_state=0)

raw = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
print("without scaling:", round(raw.score(X_test, y_test), 2))

scaler = StandardScaler().fit(X_train)          # تعلّم المتوسط والتشتت من بيانات التدريب فقط
scaled = KNeighborsClassifier(n_neighbors=5).fit(scaler.transform(X_train), y_train)
print("with scaling   :", round(scaled.score(scaler.transform(X_test), y_test), 2))
```

```reference python
KNeighborsClassifier(n_neighbors=k) | رأي أقرب k أمثلة | KNeighborsClassifier(n_neighbors=7)
StandardScaler | متوسط 0 وانحراف معياري 1 | StandardScaler().fit(X_train)
MinMaxScaler | ضغط القيم بين 0 و 1 | MinMaxScaler()
fit / transform | تعلّم المقياس / تطبيقه | scaler.transform(X_test)
```

:::warning درّب أداة التوحيد على بيانات التدريب فقط
تعلّم المقياس من البيانات كلها يسرّب معلومات من مجموعة الاختبار إلى التدريب، فتصبح نتيجة الاختبار متفائلة أكثر من اللازم. والدروس القادمة تبيّن كيف يفعل خط المعالجة (Pipeline) ذلك بشكل صحيح تلقائيًا.
:::

```exercise python
? طبّق أداة التوحيد المدرَّبة على خصائص الاختبار
X_test_scaled = scaler.___(X_test)
= transform
```

```quiz
? لماذا تحتاج KNN إلى خصائص موحّدة المقياس؟
* لأنها تستخدم المسافات فتطغى الخصائص ذات المدى الكبير
- لأن التوحيد يكبّر بيانات التدريب
- لأن KNN تقبل فقط أرقامًا بين 0 و 1
```

# @lesson ml-trees
title: أشجار القرار والغابات العشوائية
summary: نماذج من أسئلة إذا/وإلا، وأشجار كثيرة تصوّت معًا.
---
**شجرة القرار** تتعلّم سلسلة أسئلة نعم/لا مثل "هل طول البتلة أقل من 2.45 سم؟"، ومن السهل شرحها. أما **الغابة العشوائية** فتدرّب أشجارًا كثيرة على أجزاء عشوائية من البيانات وتجعلها تصوّت، وهي غالبًا أدق.

```try python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=3, stratify=iris.target
)

tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
print(export_text(tree, feature_names=list(iris.feature_names)))
print("tree accuracy  :", round(tree.score(X_test, y_test), 3))

forest = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_train, y_train)
print("forest accuracy:", round(forest.score(X_test, y_test), 3))
for name, imp in sorted(zip(iris.feature_names, forest.feature_importances_), key=lambda p: -p[1]):
    print(f"  {name:20} {imp:.2f}")
```

```reference python
DecisionTreeClassifier(max_depth=d) | شجرة أسئلة | DecisionTreeClassifier(max_depth=3)
export_text | طباعة قواعد الشجرة | export_text(tree, feature_names=cols)
RandomForestClassifier(n_estimators=n) | أشجار كثيرة تصوّت | RandomForestClassifier(n_estimators=200)
feature_importances_ | مدى فائدة كل خاصية | forest.feature_importances_
DecisionTreeRegressor / RandomForestRegressor | الشيء نفسه للأرقام | RandomForestRegressor()
```

:::tip الأشجار لا تحتاج توحيد المقاييس
تقارن الشجرة خاصية واحدة في كل مرة بحد معين، فلا تهم الوحدات. ولهذا فالأشجار والغابات اختيار أول جيد للجداول ذات الأعمدة المختلطة.
:::

```exercise python
? أنشئ غابة من 200 شجرة
RandomForestClassifier(n_estimators=___)
= 200
```

```quiz
? لماذا تكون الغابة العشوائية غالبًا أدق من شجرة واحدة؟
* لأن أشجارًا كثيرة مدرّبة على عينات مختلفة تصوّت فتقل أخطاء الشجرة الواحدة
- لأنها تستخدم أشجارًا أعمق فقط
- لأنها لا تحتاج بيانات تدريب
```

# @lesson ml-overfitting
title: فرط التخصيص والتحقق المتقاطع
summary: عندما يحفظ النموذج بدل أن يتعلّم، وكيف نقيسه بعدل.
---
يحدث **فرط التخصيص (Overfitting)** عندما يتعلّم النموذج الضوضاء في بيانات التدريب: نتيجته ممتازة على صفوف التدريب وسيئة على الجديدة. والنموذج البسيط جدًا يعاني **نقص التخصيص (Underfitting)** فيسوء أداؤه في الحالتين.

```try python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

print("depth  train  test")
for depth in [1, 2, 3, 5, 10, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    print(f"{str(depth):5} {tree.score(X_train, y_train):6.3f} {tree.score(X_test, y_test):5.3f}")

scores = cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=0), X, y, cv=5)
print("5-fold scores:", scores.round(3), "mean:", round(scores.mean(), 3))
```

بلا حد للعمق تصيب الشجرة كل صفوف التدريب (1.000) لكن ليس صفوف الاختبار: وهذه الفجوة هي فرط التخصيص.

**التحقق المتقاطع (Cross-validation)** يقسّم البيانات إلى `k` أجزاء، ويدرّب `k` مرات تاركًا جزءًا مختلفًا كل مرة، ثم يحسب متوسط النتائج. فيعطي تقديرًا أثبت من تقسيم واحد.

```reference python
max_depth / min_samples_leaf | تحديد تعقيد الشجرة | DecisionTreeClassifier(min_samples_leaf=5)
cross_val_score(model, X, y, cv=k) | نتائج k أجزاء | cross_val_score(m, X, y, cv=5)
نتيجة التدريب أكبر بكثير من الاختبار | علامة على فرط التخصيص | قارن بين النتيجتين
```

```exercise python
? قيّم نموذجًا بالتحقق المتقاطع على 5 أجزاء
cross_val_score(model, X, y, cv=___)
= 5
```

```quiz
? نموذج نتيجته 1.00 على التدريب و 0.70 على الاختبار. ماذا يحدث؟
* فرط التخصيص
- نقص التخصيص
- تعلّم مثالي

? يدرّب التحقق المتقاطع النموذج ويختبره عدة مرات على تقسيمات مختلفة.
= true
```

# @lesson ml-clustering
title: التجميع بخوارزمية k-means
summary: اكتشاف المجموعات في البيانات بدون تسميات.
---
خوارزمية **k-means** تضع `k` مراكز وتنسب كل نقطة لأقرب مركز، ثم تنقل كل مركز إلى منتصف نقاطه، وتكرر. ولا تحتاج تسميات، فهي مفيدة لاستكشاف العملاء أو المنتجات أو المستندات.

```try python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# العملاء: الطلبات في السنة، ومتوسط قيمة الطلب
customers = np.array([
    [2, 80], [3, 95], [1, 60], [2, 70],        # متقطعون، طلبات صغيرة
    [12, 90], [15, 110], [14, 85], [11, 100],  # متكررون، طلبات صغيرة
    [3, 900], [4, 1100], [2, 950],             # نادرون، طلبات كبيرة
])
X = StandardScaler().fit_transform(customers)

for k in [2, 3, 4]:
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print("k =", k, "inertia =", round(km.inertia_, 2))

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
for c in range(3):
    members = customers[km.labels_ == c]
    print(f"group {c}: {len(members)} customers, avg orders {members[:, 0].mean():.1f}, avg value {members[:, 1].mean():.0f}")
```

**القصور الذاتي (Inertia)** هو مجموع مسافات النقاط عن مراكزها، وهو يقل دائمًا كلما زاد `k`. اختر `k` عند النقطة التي يتوقف فيها عن الانخفاض الحاد ("المرفق")، وحيث تكون المجموعات منطقية من ناحية العمل.

```reference python
KMeans(n_clusters=k, n_init=10) | التجميع بـ k-means | KMeans(n_clusters=4, n_init=10)
labels_ | مجموعة كل صف | km.labels_
cluster_centers_ | المراكز | km.cluster_centers_
inertia_ | مجموع المسافات داخل المجموعات | km.inertia_
```

```exercise python
? اطلب من k-means أربع مجموعات
KMeans(n_clusters=___, n_init=10)
= 4
```

```quiz
? ماذا يحتاج التجميع زيادة على التصنيف؟
* لا شيء إضافي: يعمل بدون تسميات
- تسمية لكل صف
- مجموعة اختبار بإجابات
```

# @lesson ml-pipelines
title: خطوط المعالجة وضبط الإعدادات
summary: ربط المعالجة المسبقة بالنموذج بأمان، والبحث عن أفضل الإعدادات.
---
**خط المعالجة (Pipeline)** يجمع الخطوات (التوحيد ثم النموذج) في كائن واحد. وعند استدعاء `fit` تتعلّم كل خطوة من بيانات التدريب فقط، فلا يحدث تسريب. أما **GridSearchCV** فيجرّب تركيبات من الإعدادات بالتحقق المتقاطع ويحتفظ بالأفضل.

```try python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("knn", KNeighborsClassifier()),
])
grid = GridSearchCV(pipe, {"knn__n_neighbors": [1, 3, 5, 9, 15]}, cv=5)
grid.fit(X_train, y_train)

print("best setting:", grid.best_params_)
print("cross-validated accuracy:", round(grid.best_score_, 3))
print("test accuracy:", round(grid.score(X_test, y_test), 3))
```

```reference python
Pipeline([("name", step), ...]) | ربط الخطوات | Pipeline([("scale", StandardScaler()), ("m", model)])
"step__param" | إعداد داخل خطوة | {"knn__n_neighbors": [3, 5]}
GridSearchCV(model, grid, cv=5) | تجربة الإعدادات بالتحقق المتقاطع | GridSearchCV(pipe, params, cv=5)
best_params_ / best_score_ | أفضل الإعدادات ونتيجتها | grid.best_params_
ColumnTransformer | معالجة مختلفة لكل عمود | توحيد الأرقام وترميز الفئات
```

:::tip احتفظ بمجموعة الاختبار للنهاية
اضبط الإعدادات بالتحقق المتقاطع على بيانات التدريب، وانظر إلى نتيجة الاختبار مرة واحدة بعد اختيار النموذج، لتبقى تقديرًا صادقًا.
:::

```exercise python
? سمِّ الإعداد n_neighbors في خطوة خط المعالجة المسماة knn
{"___": [3, 5, 7]}
= knn__n_neighbors
```

```quiz
? ما المشكلة التي يمنعها خط المعالجة (Pipeline)؟
* تسرّب معلومات بيانات الاختبار إلى المعالجة المسبقة
- بطء تشغيل النماذج
- صغر حجم البيانات
```

# @lesson ml-project
title: مشروع: توقع الموظفين الذين سيكملون الدورة
summary: سير عمل كامل على جدول واقعي، من البيانات إلى التوصية.
---
يريد فريق الموارد البشرية معرفة الموظفين الذين قد **لا** يكملون دورة إلزامية، ليقدّم لهم المساعدة مبكرًا. البيانات التالية مولّدة، لكن شكلها واقعي.

```try python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report

rng = np.random.default_rng(7)
n = 600
df = pd.DataFrame({
    "weekly_hours_logged": rng.uniform(0, 6, n).round(1),
    "lessons_done_week1": rng.integers(0, 8, n),
    "manager_reminders": rng.integers(0, 4, n),
    "years_at_company": rng.integers(0, 15, n),
})
chance = 0.15 + 0.12 * df.weekly_hours_logged + 0.07 * df.lessons_done_week1 + 0.05 * df.manager_reminders
df["finished"] = (rng.uniform(0, 1, n) < chance.clip(0, 0.95)).astype(int)
print(df.head(3))
print("finish rate:", round(df.finished.mean(), 2))

X = df.drop(columns="finished")
y = df["finished"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
model = RandomForestClassifier(n_estimators=200, min_samples_leaf=5, random_state=0).fit(X_train, y_train)
print("baseline accuracy:", round(baseline.score(X_test, y_test), 3))
print("model accuracy   :", round(model.score(X_test, y_test), 3))
print(classification_report(y_test, model.predict(X_test), target_names=["not finished", "finished"]))

for name, imp in sorted(zip(X.columns, model.feature_importances_), key=lambda p: -p[1]):
    print(f"{name:22} {imp:.2f}")

at_risk = X_test[model.predict_proba(X_test)[:, 1] < 0.4]
print("employees to contact this week:", len(at_risk))
```

ما تقدّمه لفريق الموارد البشرية:

1. كم يتفوق النموذج على خط الأساس، وكم موظفًا معرضًا للخطر يلتقط (استدعاء فئة "لم يكمل").
2. أي الإشارات أهم (هنا: النشاط في الأسبوع الأول)، وهذا يقترح إجراءً: شجّع الناس على البدء مبكرًا.
3. الحدود: النموذج مدرَّب على سلوك سابق، ويجب أن يساعد على بدء حوار، ولا يقرر أبدًا أي شيء بشأن شخص وحده.

:::tip اجعله مشروعك
غيّر `min_samples_leaf`، أو جرّب `LogisticRegression` في خط معالجة مع التوحيد، أو حرّك حد 0.4 ولاحظ كيف يتغير عدد الموظفين الذين يجب التواصل معهم.
:::

```quiz
? لماذا يقارن المشروع النموذج بـ DummyClassifier؟
* للتأكد من أن النموذج أفضل فعلًا من توقع الإجابة الأكثر شيوعًا دائمًا
- لأن DummyClassifier أدق
- لتسريع التدريب
```

# @lesson ml-reference
title: مرجع تعلّم الآلة السريع
summary: سير العمل وأكثر أدوات scikit-learn استخدامًا في صفحة واحدة.
---
1. حدّد السؤال والتسمية. 2. جهّز الخصائص. 3. قسّم إلى تدريب واختبار. 4. ابدأ بخط أساس. 5. درّب النماذج واضبطها بالتحقق المتقاطع. 6. قيّم مرة واحدة على مجموعة الاختبار. 7. اشرح النتيجة وحدودها.

```reference python
train_test_split | تقسيم البيانات | train_test_split(X, y, test_size=0.2, random_state=0)
LinearRegression / Ridge | توقع الأرقام | LinearRegression().fit(X, y)
LogisticRegression | التصنيف بالاحتمالات | LogisticRegression(max_iter=1000)
KNeighborsClassifier | رأي أقرب الأمثلة | KNeighborsClassifier(n_neighbors=5)
DecisionTree / RandomForest | الأشجار | RandomForestClassifier(n_estimators=200)
KMeans | التجميع | KMeans(n_clusters=3, n_init=10)
StandardScaler | توحيد المقاييس | StandardScaler()
Pipeline | ربط الخطوات بأمان | Pipeline([("s", StandardScaler()), ("m", model)])
cross_val_score / GridSearchCV | تقييم عادل وضبط | GridSearchCV(pipe, params, cv=5)
MAE / RMSE / R² | مقاييس الانحدار | mean_absolute_error(y, pred)
accuracy / precision / recall / F1 | مقاييس التصنيف | classification_report(y, pred)
DummyRegressor / DummyClassifier | خطوط الأساس | DummyClassifier(strategy="most_frequent")
```

:::tip الخطوة التالية
خذ بيانات عامة تهمك (من قسمك أو من بوابة بيانات مفتوحة)، واتبع الخطوات السبع السابقة. ثم استكشف التعزيز المتدرج (`HistGradientBoostingClassifier`)، والشبكات العصبية للصور والنصوص.
:::

```quiz
? ما الذي يجب أن تبنيه دائمًا قبل تجربة النماذج المعقدة؟
* خط أساس بسيط للمقارنة
- شبكة عصبية
- مجموعة اختبار أكبر من التدريب
```
