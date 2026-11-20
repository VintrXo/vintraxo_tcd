# @lesson linear-algebra-vectors
title: Vectors and components
summary: The vector `(3, 4)` can represent moving three units right and four up.
---
The vector `(3, 4)` can represent moving three units right and four up. Its length is the square root of its components’ squared sum, or 5. Its direction depends on the values and signs of the components.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
from math import hypot

x, y = 3, 4
print(hypot(x, y))
```

```exercise
? What is the length of the vector (6, 8)?
___
= 10
```

```quiz
? What movement does the vector (−2, 3) describe?
* Two left and three up
- Two right and three up
- Three left and two up
> The horizontal component is negative and the vertical component is positive.
```

# @lesson linear-algebra-addition
title: Vector addition and scaling
summary: Add corresponding components when adding vectors of the same dimension.
---
Add corresponding components when adding vectors of the same dimension. Scaling multiplies every component by the scalar. A negative scalar reverses the direction of a nonzero vector.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
a = (3, -2)
b = (1, 5)
scale = -2
print((a[0] + b[0], a[1] + b[1]))
print(tuple(scale * value for value in a))
```

```exercise
? Enter the first component of the sum of (4, 3) and (−1, 2).
___
= 3
```

```quiz
? What is the result of scaling (2, −1) by −3?
- (6, −3)
* (−6, 3)
- (−6, −1)
> Multiply each component by −3.
```

# @lesson linear-algebra-dot
title: Dot product
summary: A dot product sums the products of corresponding components of two vectors of the same dimension.
---
A dot product sums the products of corresponding components of two vectors of the same dimension. It produces a scalar. Two nonzero vectors with a zero dot product are perpendicular.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
a = (2, 1)
b = (3, 4)
print(sum(x * y for x, y in zip(a, b, strict=True)))
```

```exercise
? Find the dot product of (1, 2) and (3, 1).
___
= 5
```

```quiz
? What is the dot product of (2, 1) and (1, −2)?
- 4
- (2, −2)
* 0
> Compute 2 × 1 + 1 × (−2); the two terms cancel.
```

# @lesson linear-algebra-matrices
title: Matrix rows and columns
summary: Matrix shape is written as rows followed by columns.
---
Matrix shape is written as rows followed by columns. Two rows and three columns give a `2 × 3` matrix. Swapping rows and columns gives a `3 × 2` transpose.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
matrix = [[1, 2, 3], [4, 5, 6]]
print(len(matrix), len(matrix[0]))
print([list(column) for column in zip(*matrix, strict=True)])
```

```exercise
? How many rows are in the transpose of a 2 × 4 matrix?
___
= 4
```

```quiz
? What is the shape of a matrix with 3 rows and 2 columns?
* 3 × 2
- 2 × 3
- 6 × 1
> Write the number of rows first.
```

# @lesson linear-algebra-multiply
title: Matrix multiplication
summary: Entry `i, j` of a product is the dot product of row `i` of the first matrix with column `j` of the second.
---
Entry `i, j` of a product is the dot product of row `i` of the first matrix with column `j` of the second. The first matrix must have as many columns as the second has rows. Matrix order matters.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
a = [[1, 2], [3, 4]]
b = [[2, 0], [1, 3]]
columns = list(zip(*b, strict=True))
product = [
    [sum(x * y for x, y in zip(row, column, strict=True)) for column in columns]
    for row in a
]
print(product)
```

```exercise
? How many columns are in the product of a 2 × 3 and a 3 × 4 matrix?
___
= 4
```

```quiz
? In the example, what is the entry in row one, column two?
- 4
* 6
- 8
> Use row (1, 2) and column (0, 3), giving 1 × 0 + 2 × 3.
```

# @lesson linear-algebra-transform
title: Project: rotate and stretch a shape
summary: Represent a triangle’s vertices as two-dimensional vectors.
---
Represent a triangle’s vertices as two-dimensional vectors. A 90-degree counterclockwise rotation about the origin maps `(x, y)` to `(−y, x)`. After rotating, double only the horizontal coordinate. Try stretching first and compare the resulting vertices.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
vertices = [(0, 0), (2, 0), (1, 1)]
rotate = [(0, -1), (1, 0)]
stretch = [(2, 0), (0, 1)]

def transform(matrix, points):
    return [
        tuple(sum(a * b for a, b in zip(row, point, strict=True)) for row in matrix)
        for point in points
    ]

print(transform(stretch, transform(rotate, vertices)))
print(transform(rotate, transform(stretch, vertices)))
```

```exercise
? What is the vertical coordinate of (3, 0) after rotation alone?
___
= 3
```

```quiz
? Where does (1, 1) go after rotating and then doubling the horizontal coordinate?
- (−1, 2)
- (2, −1)
* (−2, 1)
> Rotation gives (−1, 1), then only the first component doubles.
```

# @lesson linear-algebra-reference
title: Introduction to linear algebra reference
summary: Key rules with quick examples.
type: Reference
---
```reference
Dot product | Sum corresponding component products | (1, 2) · (3, 1) = 5
Transpose | Swap rows and columns | A 2 × 3 shape becomes 3 × 2
Matrix product | Pair a row of the first matrix with a column of the second | (2 × 3) by (3 × 4) gives (2 × 4)
```

Continue with NumPy. In [[numpy-en/np-arrays|Creating arrays]], learn to turn lists of rows into arrays. Then try `a @ b` in place of the loop in the matrix multiplication example.
