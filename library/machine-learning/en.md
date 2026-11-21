# @lesson ml-intro
title: What machine learning is
summary: Learning rules from examples instead of writing them by hand, and the main kinds of problems.
---
In normal programming you write the rules: "if the order is over 1000, give 10% off". In **machine learning** you give the computer many **examples** with the right answers, and it finds the rule itself. The result is a **model** that can answer new cases.

| Kind | Question | Example |
|---|---|---|
| Regression | How much? | Predict a house price or next month's sales |
| Classification | Which group? | Spam or not spam, which flower species |
| Clustering | Which items are alike? | Group customers by behaviour, no labels given |

The first two are **supervised** learning (the examples have answers, called **labels**). Clustering is **unsupervised** (no answers, the model finds structure).

```try python
# the simplest possible "model": learn the average from examples, use it to predict
hours = [1, 2, 3, 4, 5]
scores = [52, 58, 65, 70, 77]

slope = (scores[-1] - scores[0]) / (hours[-1] - hours[0])   # learned from data
start = scores[0] - slope * hours[0]

def predict(h):
    return round(start + slope * h, 1)

print("learned rule: score =", round(start, 1), "+", round(slope, 2), "x hours")
print("prediction for 6 hours:", predict(6))
```

:::info The tools in this course
The examples use **scikit-learn**, the most widely used Python library for classic machine learning, together with NumPy. They run in your browser; the first run downloads the libraries, which can take a few seconds.
:::

```quiz
? A model that predicts next month's sales in money is solving which kind of problem?
* Regression
- Classification
- Clustering

? In unsupervised learning the examples come with the correct answers.
= false
> Unsupervised learning has no labels; the model looks for structure such as groups.
```

# @lesson ml-data
title: Features, labels and splitting data
summary: X and y, the iris dataset, and why we keep a test set.
---
Machine learning data is a table. Each **row** is one example. The input columns are **features** (`X`) and the column we want to predict is the **label** or target (`y`).

```try python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X, y = iris.data, iris.target
print("shape of X:", X.shape)            # 150 flowers, 4 measurements each
print("features:", iris.feature_names)
print("classes:", list(iris.target_names))
print("first flower:", X[0], "-> class", y[0])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("train:", X_train.shape[0], "rows | test:", X_test.shape[0], "rows")
```

- The model **learns** from the training set only.
- The **test set** is hidden during training and used once at the end to estimate how well the model works on new data.
- `random_state` makes the split the same every run; `stratify=y` keeps the same class mix in both parts.

```reference python
X / y | Features / label | X = df[["age", "salary"]]; y = df["left"]
train_test_split | Split into train and test sets | train_test_split(X, y, test_size=0.2)
random_state | Repeatable randomness | random_state=42
stratify=y | Same class proportions in both sets | stratify=y
load_iris / load_diabetes | Small built-in datasets | load_iris(as_frame=True)
```

:::warning Never test on training data
A model can memorise its training rows. Measuring it on those same rows looks great and means nothing. Always evaluate on data the model has not seen.
:::

```exercise python
? Split the data so that 20% goes to the test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___)
= 0.2 | .2
```

```quiz
? What is the label in a dataset of houses used to predict their price?
* The price column
- The number of rooms
- The row number

? The test set is used to train the model.
= false
```

# @lesson ml-linear-regression
title: Linear regression
summary: Fit a straight line to predict a number, and read its coefficients.
---
**Linear regression** predicts a number as a weighted sum of the features: `y = b + w1·x1 + w2·x2 + ...`. Training finds the weights that make the predictions closest to the real values.

```try python
import numpy as np
from sklearn.linear_model import LinearRegression

# size in square metres, rooms -> price in thousands
X = np.array([[50, 1], [65, 2], [80, 2], [95, 3], [110, 3], [130, 4], [150, 4], [170, 5]])
y = np.array([420, 540, 640, 760, 850, 1010, 1150, 1300])

model = LinearRegression()
model.fit(X, y)                      # learn the weights

print("intercept:", round(model.intercept_, 1))
print("weight per m2:", round(model.coef_[0], 2), "| weight per room:", round(model.coef_[1], 1))
new_flats = np.array([[100, 3], [60, 1]])
print("predicted prices:", model.predict(new_flats).round(0))
```

Every scikit-learn model works the same way:

1. Create it: `model = LinearRegression()`
2. Train it: `model.fit(X_train, y_train)`
3. Use it: `model.predict(X_new)`

```reference python
LinearRegression() | Straight-line model | from sklearn.linear_model import LinearRegression
model.fit(X, y) | Learn from examples | model.fit(X_train, y_train)
model.predict(X) | Predict new values | model.predict([[100, 3]])
coef_ / intercept_ | Learned weights / constant | model.coef_
```

:::tip Read the weights
Coefficients tell you how much the prediction changes when one feature grows by 1 while the others stay the same. Compare them only when features are on similar scales.
:::

```exercise python
? Train the model on X and y
model.___(X, y)
= fit
```

```quiz
? Which method makes predictions for new data?
* predict
- fit
- score
```

# @lesson ml-regression-metrics
title: Measuring regression models
summary: MAE, RMSE and R², and comparing against a simple baseline.
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

| Metric | Meaning | Better when |
|---|---|---|
| MAE | Average size of the error, in the target's units | Lower |
| RMSE | Like MAE, but big errors count more | Lower |
| R² | Share of the variation the model explains (1 = perfect, 0 = no better than the mean) | Higher |

:::tip Always compare with a baseline
A `DummyRegressor` predicts the average every time. If your model is not clearly better than that, it has not learned anything useful.
:::

```exercise python
? Import the metric that gives the average absolute error
from sklearn.metrics import ___
= mean_absolute_error
```

```quiz
? What does an R² of 0 mean?
* The model is no better than predicting the average
- The model is perfect
- The model has no errors

? RMSE punishes large errors more than MAE does.
= true
```

# @lesson ml-classification
title: Classification with logistic regression
summary: Predict a category, read probabilities, and measure accuracy.
---
**Classification** predicts a category. Despite its name, **logistic regression** is a classification model: it gives a probability for each class.

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
LogisticRegression(max_iter=...) | Linear classifier with probabilities | LogisticRegression(max_iter=1000)
model.score(X, y) | Accuracy for classifiers | clf.score(X_test, y_test)
predict_proba | Probability of each class | clf.predict_proba(X_new)
classes_ | The class labels, in order | clf.classes_
```

:::tip Probabilities are useful
Instead of a yes/no answer, `predict_proba` tells you how sure the model is. You can act only when it is confident, for example review loan applications by hand when the probability is between 0.4 and 0.6.
:::

```exercise python
? Get the probability of each class for X_new
clf.___(X_new)
= predict_proba
```

```quiz
? What kind of problem does logistic regression solve?
* Classification
- Regression of prices
- Clustering
```

# @lesson ml-classification-metrics
title: Measuring classifiers
summary: Confusion matrix, precision, recall and why accuracy can mislead.
---
Accuracy alone can fool you. If only 5% of transactions are fraud, a model that always says "not fraud" is 95% accurate and completely useless.

```try python
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

# 1 = fraud, 0 = normal (real answers and a model's predictions)
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

| | Predicted no | Predicted yes |
|---|---|---|
| **Actually no** | True negative | False positive |
| **Actually yes** | False negative | True positive |

- **Precision** = TP / (TP + FP): when the model says yes, how often is it right?
- **Recall** = TP / (TP + FN): of all the real yes cases, how many did it find?
- **F1** combines both into one number.

:::tip Choose the metric from the cost of mistakes
Missing a fraud (false negative) costs more than checking a normal payment (false positive), so fraud models care most about recall. A spam filter that hides real email has a costly false positive, so it cares about precision.
:::

```quiz
? A disease test must miss as few sick people as possible. Which metric matters most?
* Recall
- Precision
- Accuracy

? A model can have high accuracy and still be useless on rare classes.
= true
```

# @lesson ml-knn-scaling
title: K-nearest neighbours and feature scaling
summary: Classify by similar examples, and why features must be on the same scale.
---
**K-nearest neighbours** (KNN) classifies a new example by looking at the `k` closest training examples and taking a vote. It depends on distances, so a feature measured in thousands (salary) drowns a feature measured in single digits (years of experience) unless we **scale** them.

```try python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
n = 200
experience = rng.uniform(0, 10, n)              # years
salary = rng.uniform(3000, 30000, n)            # unrelated to the label
promoted = (experience + rng.normal(0, 1, n) > 5).astype(int)
X = np.column_stack([experience, salary])
X_train, X_test, y_train, y_test = train_test_split(X, promoted, test_size=0.3, random_state=0)

raw = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
print("without scaling:", round(raw.score(X_test, y_test), 2))

scaler = StandardScaler().fit(X_train)          # learn mean and spread from TRAIN only
scaled = KNeighborsClassifier(n_neighbors=5).fit(scaler.transform(X_train), y_train)
print("with scaling   :", round(scaled.score(scaler.transform(X_test), y_test), 2))
```

```reference python
KNeighborsClassifier(n_neighbors=k) | Vote of the k nearest examples | KNeighborsClassifier(n_neighbors=7)
StandardScaler | Mean 0, standard deviation 1 | StandardScaler().fit(X_train)
MinMaxScaler | Squeeze to 0..1 | MinMaxScaler()
fit / transform | Learn the scaling / apply it | scaler.transform(X_test)
```

:::warning Fit the scaler on training data only
Learning the scaling from the whole dataset lets information from the test set leak into training, and the test score becomes too optimistic. The next lessons show how a pipeline does this correctly for you.
:::

```exercise python
? Apply a fitted scaler to the test features
X_test_scaled = scaler.___(X_test)
= transform
```

```quiz
? Why does KNN need scaled features?
* It uses distances, so large-range features would dominate
- Scaling makes training data bigger
- KNN only accepts numbers between 0 and 1
```

# @lesson ml-trees
title: Decision trees and random forests
summary: Models made of if/else questions, and many trees voting together.
---
A **decision tree** learns a series of yes/no questions such as "is the petal shorter than 2.45 cm?". It is easy to explain. A **random forest** trains many trees on random parts of the data and lets them vote, which is usually more accurate.

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
DecisionTreeClassifier(max_depth=d) | Tree of questions | DecisionTreeClassifier(max_depth=3)
export_text | Print the rules of a tree | export_text(tree, feature_names=cols)
RandomForestClassifier(n_estimators=n) | Many trees voting | RandomForestClassifier(n_estimators=200)
feature_importances_ | How much each feature helped | forest.feature_importances_
DecisionTreeRegressor / RandomForestRegressor | The same for numbers | RandomForestRegressor()
```

:::tip Trees do not need scaling
A tree compares one feature at a time with a threshold, so the units do not matter. That makes trees and forests a good first choice for tables with mixed columns.
:::

```exercise python
? Create a forest of 200 trees
RandomForestClassifier(n_estimators=___)
= 200
```

```quiz
? Why is a random forest usually more accurate than a single tree?
* Many trees trained on different samples vote, which reduces single-tree mistakes
- It uses deeper trees only
- It does not need training data
```

# @lesson ml-overfitting
title: Overfitting and cross-validation
summary: When a model memorises instead of learning, and how to measure it fairly.
---
A model **overfits** when it learns the noise in the training data: it scores very well on training rows and badly on new ones. A model that is too simple **underfits** and does badly on both.

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

With no depth limit the tree gets every training row right (1.000) but not the test rows: that gap is overfitting.

**Cross-validation** splits the data into `k` parts, trains `k` times leaving a different part out each time, and averages the scores. It gives a steadier estimate than one split.

```reference python
max_depth / min_samples_leaf | Limit a tree's complexity | DecisionTreeClassifier(min_samples_leaf=5)
cross_val_score(model, X, y, cv=k) | k-fold scores | cross_val_score(m, X, y, cv=5)
train score >> test score | Sign of overfitting | compare both
```

```exercise python
? Score a model with 5-fold cross-validation
cross_val_score(model, X, y, cv=___)
= 5
```

```quiz
? A model scores 1.00 on training data and 0.70 on test data. What is happening?
* Overfitting
- Underfitting
- Perfect learning

? Cross-validation trains and tests the model several times on different splits.
= true
```

# @lesson ml-clustering
title: Clustering with k-means
summary: Find groups in data without labels.
---
**K-means** places `k` centres and assigns each point to the nearest one, then moves each centre to the middle of its points, and repeats. It needs no labels, which makes it useful for exploring customers, products or documents.

```try python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# customers: orders per year, average order value
customers = np.array([
    [2, 80], [3, 95], [1, 60], [2, 70],        # occasional, small
    [12, 90], [15, 110], [14, 85], [11, 100],  # frequent, small
    [3, 900], [4, 1100], [2, 950],             # rare, big
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

**Inertia** is the total distance of points to their centre; it always falls as `k` grows. Choose the `k` where it stops falling sharply (the "elbow"), and where the groups make business sense.

```reference python
KMeans(n_clusters=k, n_init=10) | k-means clustering | KMeans(n_clusters=4, n_init=10)
labels_ | The group of each row | km.labels_
cluster_centers_ | The centres | km.cluster_centers_
inertia_ | Total within-group distance | km.inertia_
```

```exercise python
? Ask k-means for 4 groups
KMeans(n_clusters=___, n_init=10)
= 4
```

```quiz
? What does clustering need that classification does not?
* Nothing extra: it works without labels
- Labels for every row
- A test set with answers
```

# @lesson ml-pipelines
title: Pipelines and tuning
summary: Chain preprocessing and a model safely, and search for good settings.
---
A **Pipeline** joins steps (scaling, then the model) into one object. When you call `fit`, each step learns from the training data only, which prevents leakage. **GridSearchCV** tries combinations of settings with cross-validation and keeps the best.

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
Pipeline([("name", step), ...]) | Chain steps | Pipeline([("scale", StandardScaler()), ("m", model)])
"step__param" | A setting inside a pipeline step | {"knn__n_neighbors": [3, 5]}
GridSearchCV(model, grid, cv=5) | Try settings with cross-validation | GridSearchCV(pipe, params, cv=5)
best_params_ / best_score_ | The winning settings and score | grid.best_params_
ColumnTransformer | Different preprocessing per column | numbers scaled, categories encoded
```

:::tip Keep the test set for the very end
Tune with cross-validation on the training data. Look at the test score once, after you have chosen the model, so it stays an honest estimate.
:::

```exercise python
? Name the setting n_neighbors of the pipeline step called knn
{"___": [3, 5, 7]}
= knn__n_neighbors
```

```quiz
? What problem does a Pipeline prevent?
* Information from the test data leaking into preprocessing
- Models running too slowly
- Data being too small
```

# @lesson ml-project
title: Project: predict which employees finish a course
summary: A complete workflow on a realistic table, from data to a recommendation.
---
An HR team wants to know which employees are likely **not** to finish a mandatory course, so they can offer help early. The data below is generated, but its shape is realistic.

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

What to report to the HR team:

1. How much better than the baseline the model is, and how many at-risk employees it catches (the recall of "not finished").
2. Which signals matter most (here: activity in the first week), which suggests an action: encourage people to start early.
3. The limits: the model is trained on past behaviour, and it should support a conversation, never decide anything about a person on its own.

:::tip Make it yours
Change `min_samples_leaf`, try `LogisticRegression` in a pipeline with scaling, or move the 0.4 threshold and see how the number of employees to contact changes.
:::

```quiz
? Why does the project compare the model with a DummyClassifier?
* To check that the model is really better than always predicting the most common answer
- Because DummyClassifier is more accurate
- To make training faster
```

# @lesson ml-reference
title: Machine learning quick reference
summary: The workflow and the most used scikit-learn tools on one page.
---
1. Define the question and the label. 2. Prepare features. 3. Split train / test. 4. Start with a baseline. 5. Train models, tune with cross-validation. 6. Evaluate once on the test set. 7. Explain the result and its limits.

```reference python
train_test_split | Split data | train_test_split(X, y, test_size=0.2, random_state=0)
LinearRegression / Ridge | Predict numbers | LinearRegression().fit(X, y)
LogisticRegression | Classify with probabilities | LogisticRegression(max_iter=1000)
KNeighborsClassifier | Vote of nearest examples | KNeighborsClassifier(n_neighbors=5)
DecisionTree / RandomForest | Trees | RandomForestClassifier(n_estimators=200)
KMeans | Clustering | KMeans(n_clusters=3, n_init=10)
StandardScaler | Scale features | StandardScaler()
Pipeline | Chain steps safely | Pipeline([("s", StandardScaler()), ("m", model)])
cross_val_score / GridSearchCV | Fair evaluation and tuning | GridSearchCV(pipe, params, cv=5)
MAE / RMSE / R² | Regression metrics | mean_absolute_error(y, pred)
accuracy / precision / recall / F1 | Classification metrics | classification_report(y, pred)
DummyRegressor / DummyClassifier | Baselines | DummyClassifier(strategy="most_frequent")
```

:::tip Where to go next
Take a public dataset you care about (from your own department or an open data portal), and follow the seven steps above. Then explore gradient boosting (`HistGradientBoostingClassifier`) and, for images and text, neural networks.
:::

```quiz
? What should you always build before trying complex models?
* A simple baseline to compare against
- A neural network
- A larger test set than training set
```
