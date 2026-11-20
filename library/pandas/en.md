# @lesson pd-intro
title: Pandas introduction
summary: What Pandas is and why data analysts use it.
---
**Pandas** is a Python library for analyzing table data: it reads CSV and Excel files and databases, cleans data, filters it, groups it and computes statistics, in a few lines.

This course has a ready-made sales file called `sales.csv`. Press **Run** (the first run loads Pandas and takes a few seconds):

```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df.head())
print("Rows:", len(df))
```

:::info The short name pd
The usual import is `import pandas as pd`, and a table is usually called `df`, short for DataFrame.
:::

```quiz
? What is Pandas mainly for?
* Analyzing table data
- Drawing website interfaces
- Version control

? pd.read_csv reads a CSV file into a table.
= true
```

# @lesson pd-series
title: Series
summary: One column of data with an index.
---
A **Series** is one column of values, where each value has an **index** (a label):

```try python
import pandas as pd

temps = pd.Series([31, 35, 29, 40], index=["Sat", "Sun", "Mon", "Tue"])
print(temps)
print(temps["Sun"])
print(temps.max(), temps.idxmax())
print(temps[temps > 30])
```

- `idxmax()` returns the label of the largest value.
- Operations and filtering work just like NumPy.

```quiz
? What is a Series in Pandas?
* One column of values with an index
- A whole table
- A CSV file

? idxmax returns the label of the largest value.
= true
```

# @lesson pd-dataframe
title: DataFrame
summary: Creating a table, columns, the index, and a quick look.
---
A **DataFrame** is a table of rows and columns; each column is a Series:

```try python
import pandas as pd

df = pd.DataFrame({
    "name": ["Sara", "Omar", "Layla"],
    "age": [28, 35, 24],
    "city": ["Riyadh", "Cairo", "Dubai"],
})
print(df)
print(df.columns.tolist())
print(df.shape)
print(df.dtypes)
```

## A quick look at any table

```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
df.info()
print(df.describe())
```

```reference python
head() / tail() | First / last rows | df.head(3)
shape | Number of rows and columns | df.shape
columns | Column names | df.columns
dtypes | Type of each column | df.dtypes
info() | Table summary | df.info()
describe() | Statistics of numeric columns | df.describe()
```

```quiz
? What does df.shape return?
* The number of rows and columns
- The column names
- The first five rows

? Every column of a DataFrame is a Series.
= true
```

# @lesson pd-csv
title: Reading and saving data
summary: read_csv and to_csv, and reading options.
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
pd.read_csv | Read CSV | pd.read_csv("a.csv")
pd.read_excel | Read Excel | pd.read_excel("a.xlsx")
pd.read_json | Read JSON | pd.read_json("a.json")
parse_dates | Turn columns into dates | read_csv(…, parse_dates=["date"])
df.to_csv | Save CSV | df.to_csv("out.csv", index=False)
df.to_excel | Save Excel | df.to_excel("out.xlsx")
```

:::tip index=False
Without it, Pandas saves the row number as an extra column in the file.
:::

```quiz
? Which option stops the row number being saved in the file?
* index=False
- header=False
- rows=False

? parse_dates turns the given columns into dates.
= true
```

# @lesson pd-select
title: Selecting columns and rows
summary: Columns, loc by label, and iloc by position.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df["product"].head(3))               # one column
print(df[["product", "price"]].head(3))     # several columns
print(df.iloc[0])                            # first row by position
print(df.iloc[2:5, [1, 2]])                  # rows and columns by position
print(df.loc[3, "branch"])                   # by label
print(df.loc[0:2, "product":"qty"])
```

- `iloc` works by numeric position (like lists).
- `loc` works by label: the index and the column names.

```exercise python
? Select the fifth row by position
row = df.___[4]
= iloc
```

```quiz
? What is the difference between loc and iloc?
* loc is by label, iloc by numeric position
- There is no difference
- iloc is only for columns

? df[["a", "b"]] selects two columns.
= true
```

# @lesson pd-filter
title: Filtering
summary: Conditions, isin, and query.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df[df["price"] > 1000])
print(df[(df["branch"] == "Riyadh") & (df["qty"] >= 3)])
print(df[df["category"].isin(["Furniture", "Accessories"])])
print(df.query("qty > 20"))
print(df[df["product"].str.contains("Laptop")])
```

- `&` (and) and `|` (or), with parentheses around each condition.
- `isin([...])` the value is in a list.
- `.str.contains()` searches inside text.

```exercise python
? Select the sales with a quantity above 10
big = df[df["qty"] ___ 10]
= >
```

```quiz
? Which function selects rows whose value is in a list?
* isin
- contains
- between_list

? Each condition must be in parentheses when using & in a filter.
= true
```

# @lesson pd-clean
title: Cleaning data
summary: Missing and duplicated values, and fixing types.
---
Real data has gaps and repeats. Our file has a missing quantity, a missing branch and a duplicated row:

```try python sales
import pandas as pd

df = pd.read_csv("sales.csv")
print(df.isna().sum())               # missing values per column
print("Duplicated:", df.duplicated().sum())

df = df.drop_duplicates()
df["qty"] = df["qty"].fillna(df["qty"].median())
df["branch"] = df["branch"].fillna("Unknown")
df["qty"] = df["qty"].astype(int)
print(df.isna().sum().sum(), len(df))
```

```reference python
isna() | Where values are missing | df.isna().sum()
dropna() | Drop rows with gaps | df.dropna()
fillna() | Fill gaps | df["a"].fillna(0)
duplicated() | Repeated rows | df.duplicated()
drop_duplicates() | Drop repeats | df.drop_duplicates()
astype() | Change type | df["a"].astype(int)
rename() | Rename columns | df.rename(columns={"a": "b"})
str.strip() | Remove spaces | df["a"].str.strip()
```

:::tip Drop or fill?
Dropping is simpler but loses data. Filling with the median or a sensible value keeps the rows; choose by what the data means.
:::

```quiz
? Which function fills missing values?
- dropna
* fillna
- isna

? drop_duplicates removes repeated rows.
= true
```

# @lesson pd-sort-new
title: Sorting and new columns
summary: sort_values, computed columns, apply, and dates.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"]).drop_duplicates()
df["total"] = df["qty"] * df["price"]
df["month"] = df["date"].dt.month
df["size"] = df["total"].apply(lambda t: "large" if t >= 5000 else "normal")
print(df.sort_values("total", ascending=False).head(5)[["product", "total", "size"]])
print(df.nlargest(3, "total")[["product", "total"]])
```

- `dt.month`, `dt.year` and `dt.day_name()` give parts of a date.
- `apply` applies a function to every value.

```exercise python
? Sort the table by price, highest first
df.sort_values("price", ___=False)
= ascending
```

```quiz
? How do you add a new computed column?
* df["total"] = df["qty"] * df["price"]
- df.add("total")
- df.new_column("total")

? nlargest returns the rows with the largest values.
= true
```

# @lesson pd-groupby
title: Grouping with groupby
summary: Totals and averages per group, agg, and pivot_table.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv").drop_duplicates()
df["total"] = df["qty"].fillna(0) * df["price"]

print(df.groupby("branch")["total"].sum())
print(df.groupby("category").agg(orders=("product", "count"), revenue=("total", "sum")))
print(df.pivot_table(index="branch", columns="category", values="total", aggfunc="sum", fill_value=0))
```

- `groupby("column")` splits the rows into groups.
- `agg` computes several statistics under names you choose.
- `pivot_table` makes a pivot table like the one in Excel.

```exercise python
? Compute the average price per category
df.groupby("category")["price"].___()
= mean
```

```quiz
? What does df.groupby("branch")["total"].sum() do?
* Totals the total column for each branch
- Sorts the branches
- Removes duplicated branches

? pivot_table creates a pivot table.
= true
```

# @lesson pd-merge
title: Merging tables
summary: merge, like JOIN in SQL, and concat.
---
The file `branches.csv` has each branch's manager and opening year. We merge it with the sales:

```try python sales
import pandas as pd

sales = pd.read_csv("sales.csv").drop_duplicates()
branches = pd.read_csv("branches.csv")
merged = sales.merge(branches, on="branch", how="left")
print(merged[["date", "branch", "manager", "product"]].head(6))
```

```reference python
merge(on=…) | Merge on a shared column | a.merge(b, on="id")
how="inner" | Only matching rows | a.merge(b, on="id", how="inner")
how="left" | Every row of the left table | a.merge(b, on="id", how="left")
pd.concat | Stack tables | pd.concat([a, b])
```

:::info Like SQL
`merge` matches `JOIN`, and `how="left"` matches `LEFT JOIN`. Note that the row with a missing branch finds no manager.
:::

```quiz
? What is the SQL equivalent of merge?
* JOIN
- GROUP BY
- UNION

? pd.concat stacks tables on top of each other.
= true
```

# @lesson pd-project
title: Project: a sales report
summary: A full report from the raw file to the results.
---
```try python sales
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"])
df = df.drop_duplicates()
df["qty"] = df["qty"].fillna(df["qty"].median()).astype(int)
df["branch"] = df["branch"].fillna("Unknown")
df["total"] = df["qty"] * df["price"]
df["month"] = df["date"].dt.strftime("%Y-%m")

print("Total revenue:", df["total"].sum())
print("\nRevenue per month:")
print(df.groupby("month")["total"].sum())
print("\nTop 3 products:")
print(df.groupby("product")["total"].sum().nlargest(3))
print("\nShare per branch (%):")
print((df.groupby("branch")["total"].sum() / df["total"].sum() * 100).round(1))
```

:::tip Extend it yourself
Compute the average order value per branch, or which month was best for each category.
:::

```quiz
? Why remove duplicates and fill gaps before computing?
* So the results are correct and not misleading
- Because Pandas cannot read files otherwise
- Only to print faster

? dt.strftime("%Y-%m") turns a date into year and month.
= true
```

# @lesson pd-reference
title: Pandas reference
summary: The most important functions with an example for each.
type: Reference
---
Search the table for any function.

```reference python
pd.read_csv | Read CSV | pd.read_csv("a.csv")
pd.DataFrame | Create a table | pd.DataFrame({"a": [1, 2]})
head / tail | First / last rows | df.head()
info / describe | Summary and statistics | df.describe()
df["col"] / df[[…]] | Select columns | df[["a", "b"]]
loc / iloc | Select by label / position | df.loc[0, "a"]
df[df[…] > x] | Filter | df[df["qty"] > 5]
isin / query | Advanced filtering | df.query("qty > 5")
isna / fillna / dropna | Missing values | df.fillna(0)
drop_duplicates | Remove repeats | df.drop_duplicates()
astype | Change type | df["a"].astype(int)
sort_values / nlargest | Sorting | df.sort_values("a")
apply | Apply a function | df["a"].apply(f)
groupby / agg | Grouping | df.groupby("b")["a"].sum()
pivot_table | Pivot table | df.pivot_table(index="b", values="a")
merge / concat | Combining | a.merge(b, on="id")
dt.month / dt.year | Parts of a date | df["d"].dt.month
to_csv / to_excel | Saving | df.to_csv("out.csv", index=False)
```

:::tip What next?
Try analyzing a real file from your work: sales, attendance or orders. Then start charting the results with the **Matplotlib** library.
:::
