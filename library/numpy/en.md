# @lesson np-intro
title: NumPy introduction
summary: Why NumPy is faster than plain Python lists.
---
**NumPy** is a Python library for computing with numbers. At its heart is a type called **ndarray**: an array of numbers of one type, stored contiguously in memory, which makes operations on it far faster than on plain lists. Pandas and most data science and AI libraries are built on it.

Press **Run** (the first run loads NumPy in your browser and takes a few seconds):

```try python
import numpy as np

prices = np.array([120, 45, 300, 80])
print(prices * 1.15)        # tax on every price at once
print(prices.sum(), prices.mean())
```

Notice: no `for` loop. The operation applies to every item together; this is called **vectorized** computing.

:::info The short name np
The usual import is `import numpy as np`; you will see it in every book and project.
:::

```quiz
? What is the core type in NumPy?
* ndarray
- list
- dict

? In NumPy you need a for loop to multiply every item by a number.
= false
> Operations are vectorized: prices * 1.15 multiplies every item at once.
```

# @lesson np-arrays
title: Creating arrays
summary: array, zeros, ones, arange and linspace, dimensions and data type.
---
```try python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1, 2, 3], [4, 5, 6]])      # two dimensions: two rows, three columns
print(a, a.ndim)
print(b)
print(b.ndim, b.shape, b.size, b.dtype)
```

## Ready-made arrays

```try python
import numpy as np

print(np.zeros(4))
print(np.ones((2, 3)))
print(np.arange(0, 10, 2))        # like range
print(np.linspace(0, 1, 5))       # 5 evenly spaced numbers from 0 to 1
print(np.full((2, 2), 7))
```

```reference python
np.array() | From a list | np.array([1, 2, 3])
np.zeros() / np.ones() | Zeros / ones | np.zeros((2, 3))
np.arange() | A sequence with a step | np.arange(0, 10, 2)
np.linspace() | A number of points between two limits | np.linspace(0, 1, 5)
np.eye() | Identity matrix | np.eye(3)
.shape / .ndim / .size | Shape / dimensions / count | a.shape
.dtype | Data type | a.dtype
```

```exercise python
? Create an array from 0 to 4
import numpy as np
a = np.___(5)
= arange
```

```quiz
? What is the shape of np.array([[1, 2, 3], [4, 5, 6]])?
* (2, 3)
- (3, 2)
- (6,)

? np.zeros((2, 3)) creates an array of zeros with two rows and three columns.
= true
```

# @lesson np-indexing
title: Indexing and slicing
summary: Reaching items, rows and columns.
---
```try python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
print(a[0], a[-1])
print(a[1:4])
print(a[::2])

m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(m[1, 2])       # row 1, column 2
print(m[0])          # the first row
print(m[:, 1])       # the whole second column
print(m[:2, 1:])     # part of the array
```

:::warning Slicing does not copy
`b = a[1:3]` gives a "view" of the same data; changing `b` changes `a`. To copy, use `a[1:3].copy()`.
:::

```exercise python
? Select the whole first column of m
first_col = m[___, 0]
= :
```

```quiz
? What does m[1, 2] return?
* The item in row 1, column 2
- Rows 1 and 2
- Columns 1 and 2

? Changing a slice of an array can change the original array.
= true
```

# @lesson np-shape
title: Changing shape
summary: reshape, flatten, transpose and joining.
---
```try python
import numpy as np

a = np.arange(12)
m = a.reshape(3, 4)
print(m)
print(m.T)                 # the transpose: rows become columns
print(m.flatten())
print(a.reshape(2, -1))    # -1: work out this dimension
```

## Joining

```try python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
print(np.concatenate([a, b]))      # one under the other
print(np.hstack([a, a]))           # side by side
```

```exercise python
? Turn 6 numbers into an array of two rows and three columns
m = np.arange(6).___(2, 3)
= reshape
```

```quiz
? What does -1 mean in reshape(2, -1)?
* Work out this dimension automatically
- Reverse the order
- Drop the last item

? .T gives the transpose of an array.
= true
```

# @lesson np-math
title: Operations and broadcasting
summary: Operations between arrays, broadcasting, and math functions.
---
```try python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b, a * b, b / a)
print(a ** 2)
print(np.sqrt(b), np.round(np.sqrt(b), 2))
```

## Broadcasting

The smaller array stretches automatically to fit the larger one:

```try python
import numpy as np

prices = np.array([[100, 200, 300],
                   [ 50,  60,  70]])
discount = np.array([0.9, 0.8, 1.0])   # a discount per column
print(prices * discount)
print(prices + 5)                       # one number added to everything
```

```reference python
+ - * / ** | Item-by-item operations | a * b
np.sqrt / np.exp / np.log | Math functions | np.sqrt(a)
np.round | Rounding | np.round(a, 2)
np.abs | Absolute value | np.abs(a)
@ / np.dot | Matrix multiplication | a @ b
```

:::info * or @?
`a * b` multiplies each item by its partner. `a @ b` is mathematical matrix multiplication (linear algebra).
:::

```quiz
? What is np.array([1, 2, 3]) * 2?
* [2 4 6]
- [1 2 3 1 2 3]
- An error

? Broadcasting lets you add one number to a whole array.
= true
```

# @lesson np-stats
title: Statistics and axis
summary: sum, mean, min, max and std, per row or per column.
---
```try python
import numpy as np

sales = np.array([[120, 90, 150],    # branch one: three months
                  [ 80, 110, 95],    # branch two
                  [200, 180, 210]])  # branch three
print("Total:", sales.sum())
print("Per month:", sales.sum(axis=0))
print("Per branch:", sales.sum(axis=1))
print("Mean:", sales.mean().round(1))
print("Best sale:", sales.max(), "at position", sales.argmax())
print("Standard deviation:", sales.std().round(1))
```

- `axis=0` goes down the rows: one result per **column**.
- `axis=1` goes across the columns: one result per **row**.

```reference python
sum() | Total | a.sum(axis=0)
mean() | Mean | a.mean()
median() | Median | np.median(a)
min() / max() | Smallest / largest | a.max()
argmin() / argmax() | Position of smallest / largest | a.argmax()
std() / var() | Deviation / variance | a.std()
cumsum() | Running total | a.cumsum()
```

```exercise python
? Compute the total of each row
row_totals = sales.sum(axis=___)
= 1
```

```quiz
? What does sales.sum(axis=0) give?
* A total for each column
- A total for each row
- One number

? argmax returns the position of the largest value.
= true
```

# @lesson np-filter
title: Filtering with conditions
summary: Boolean masks, where, and counting.
---
A comparison gives an array of `True/False` that you use to pick items:

```try python
import numpy as np

scores = np.array([45, 88, 92, 67, 30, 75])
mask = scores >= 60
print(mask)
print(scores[mask])                         # those who passed
print(scores[(scores > 50) & (scores < 90)])
print("Passed:", mask.sum())
print(np.where(scores >= 60, "pass", "fail"))
```

- `&` (and) and `|` (or), with parentheses around each condition.
- `mask.sum()` counts the `True` values.

```exercise python
? Pick the numbers greater than 10
big = a[a ___ 10]
= >
```

```quiz
? What does scores[scores >= 60] return?
* Only the items that meet the condition
- True and False values
- Only the first position

? np.where picks a value for each item depending on a condition.
= true
```

# @lesson np-random
title: Random numbers
summary: The generator, distributions and random choice.
---
```try python
import numpy as np

rng = np.random.default_rng(seed=42)       # seed makes results repeatable
print(rng.integers(1, 7, size=10))          # roll a die 10 times
print(rng.random(3))                        # numbers between 0 and 1
heights = rng.normal(loc=170, scale=8, size=1000)
print(heights.mean().round(1), heights.std().round(1))
print(rng.choice(["red", "green", "blue"], size=5))
```

:::tip Why a seed?
With the same `seed` you get the same numbers every time, so others can repeat your experiment exactly.
:::

```quiz
? What is a seed for?
* Getting the same random numbers on every run
- Speeding up computation
- Preventing repeated numbers

? rng.normal generates numbers from the normal distribution.
= true
```

# @lesson np-project
title: Project: analyzing grades
summary: An exercise that brings together what you learned, on students' grades.
---
```try python
import numpy as np

rng = np.random.default_rng(7)
# 8 students × 3 subjects
grades = rng.integers(40, 101, size=(8, 3))
subjects = np.array(["math", "science", "language"])
print(grades)

avg_student = grades.mean(axis=1).round(1)
avg_subject = grades.mean(axis=0).round(1)
print("Average per student:", avg_student)
print("Average per subject:", dict(zip(subjects, avg_subject)))
print("Hardest subject:", subjects[avg_subject.argmin()])
print("Best student no.:", avg_student.argmax() + 1)
print("Students above 75:", np.where(avg_student > 75)[0] + 1)

curved = np.clip(grades + 5, 0, 100)    # add 5 marks, capped at 100
print("After the curve:", curved.mean().round(1))
```

:::tip Extend it yourself
Compute the pass rate per subject (60 and up), or rank the students by average with `np.argsort`.
:::

```quiz
? What does np.clip(a, 0, 100) do?
* Keeps the values between 0 and 100
- Deletes values out of range
- Rounds the values

? The average per student uses axis=1 because each row is a student.
= true
```

# @lesson np-reference
title: NumPy reference
summary: The most important functions with an example for each.
type: Reference
---
Search the table for any function.

```reference python
np.array | Create an array | np.array([1, 2])
np.arange / np.linspace | Number sequences | np.arange(10)
np.zeros / np.ones / np.full | Ready-made arrays | np.zeros((2, 2))
.shape / .reshape | Shape and reshaping | a.reshape(2, 3)
.T | Transpose | m.T
a[i, j] / a[:, j] | Indexing | m[:, 0]
a[a > 5] | Filtering | a[a > 5]
np.where | Pick by condition | np.where(a > 0, a, 0)
sum / mean / std | Statistics | a.mean(axis=0)
min / max / argmax | Extremes | a.argmax()
np.sqrt / np.round | Math functions | np.round(a, 2)
@ | Matrix multiplication | a @ b
np.concatenate / hstack | Joining | np.hstack([a, b])
np.unique | Distinct values | np.unique(a)
np.sort / argsort | Sorting | np.argsort(a)
np.clip | Clamp values | np.clip(a, 0, 1)
default_rng | Random generator | np.random.default_rng(1)
```

:::tip What next?
Go on to the **Pandas** course to analyze tables and real data.
:::
