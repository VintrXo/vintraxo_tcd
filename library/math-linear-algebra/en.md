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

# @lesson applied-linear-algebra-elimination
title: Elimination for linear systems
summary: Write the system as a coefficient matrix and a right-hand side.
---
Write the system as a coefficient matrix and a right-hand side. Elimination subtracts row multiples to remove a variable, followed by back substitution. `numpy.linalg.solve` solves a square system with an invertible matrix.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
import numpy as np

matrix = np.array([[1, 1], [2, 1]])
totals = np.array([10, 16])
solution = np.linalg.solve(matrix, totals)
print(solution.tolist())
print(bool(np.allclose(matrix @ solution, totals)))
```

```exercise
? Find x when x + y = 8 and 2x + y = 13.
___
= 5
```

```quiz
? What do we verify by multiplying the matrix by the solution?
* Recovering the right-hand side
- All coefficients are zero
- The solution is always positive
> A solution satisfies A x = b, so it recovers the right-hand side.
```

# @lesson applied-linear-algebra-span
title: Span and linear independence
summary: A span contains all linear combinations of the given vectors.
---
A span contains all linear combinations of the given vectors. Vectors are independent when the only combination giving zero has all coefficients zero. In the plane, two proportional nonzero vectors span a line; two non-proportional vectors span the plane.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
import numpy as np

line = np.array([[1, 2], [2, 4]])
plane = np.array([[1, 0], [2, 1]])
print(np.linalg.matrix_rank(line))
print(np.linalg.matrix_rank(plane))
```

```exercise
? What is the dimension of the span of (1, 0) and (0, 1)?
___
= 2
```

```quiz
? Are (1, 2) and (2, 4) independent?
- Yes
* No
- Only if reordered
> The second vector is twice the first.
```

# @lesson applied-linear-algebra-determinant
title: Determinants and invertibility
summary: The determinant of a 2 × 2 matrix is `ad − bc`.
---
The determinant of a 2 × 2 matrix is `ad − bc`. Its absolute value is the area scale factor. A zero determinant means the transformation collapses the plane onto a line or point and is not invertible.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
def determinant(matrix):
    (a, b), (c, d) = matrix
    return a * d - b * c

print(determinant([[2, 1], [0, 3]]))
print(determinant([[1, 2], [2, 4]]))
```

```exercise
? Find the determinant of the matrix with rows (3, 0) and (1, 2).
___
= 6
```

```quiz
? What determinant indicates that a square matrix is not invertible?
- 1
- −1
* 0
> A zero determinant means the transformation loses dimension.
```

# @lesson applied-linear-algebra-eigen
title: Eigenvalues and eigenvectors
summary: An eigenvector v is nonzero and satisfies `Av = λv`.
---
An eigenvector v is nonzero and satisfies `Av = λv`. The transformation scales the vector by λ, preserving its line even if it reverses direction, and sending it to zero if λ = 0.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
import numpy as np

matrix = np.array([[3, 0], [0, 2]])
vector = np.array([1, 0])
print((matrix @ vector).tolist())
print(np.linalg.eigvalsh(matrix).tolist())
```

```exercise
? What eigenvalue corresponds to (0, 1) in the example?
___
= 2
```

```quiz
? Which vector is excluded from the definition of an eigenvector?
* The zero vector
- The vector (1, 0)
- The vector (0, 1)
> The zero vector satisfies the equation for every λ and does not identify an eigenvalue.
```

# @lesson applied-linear-algebra-projection
title: Projection onto a direction
summary: Project w onto a nonzero v with `(w · v)/(v · v) × v`.
---
Project w onto a nonzero v with `(w · v)/(v · v) × v`. Subtracting the projection from w leaves a component orthogonal to v. This idea appears in approximating data using a smaller subspace.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
import numpy as np

w = np.array([3, 1])
v = np.array([1, 1])
projection = (w @ v) / (v @ v) * v
residual = w - projection
print(projection.tolist())
print(float(residual @ v))
```

```exercise
? What is the second component of the projection of (4, 3) onto the x-axis?
___
= 0
```

```quiz
? What is the dot product of the residual with the projection direction?
- 1
* 0
- 2
> The residual is orthogonal to the projection direction.
```

# @lesson applied-linear-algebra-project
title: Project: transform a shape with NumPy
summary: Represent each point as a column.
---
Represent each point as a column. Build a horizontal stretch of factor 2 and a 90-degree counterclockwise rotation. In `rotation @ stretch @ points`, the stretch acts first. Reverse the order and compare coordinates.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
import numpy as np

points = np.array([[0, 1, 0], [0, 1, 2]])
stretch = np.array([[2, 0], [0, 1]])
rotation = np.array([[0, -1], [1, 0]])
print((rotation @ stretch @ points).T.tolist())
print((stretch @ rotation @ points).T.tolist())
```

```exercise
? What is the vertical coordinate of (1, 1) after stretching first and then rotating?
___
= 2
```

```quiz
? In the example, does reversing order preserve every resulting coordinate?
- Yes
- Only because the determinant is negative
* No
> The point (1, 1) maps to (−1, 2) in one order and (−2, 1) in the other.
```

# @lesson matrix-decompositions-least-squares
title: Matrix least squares
summary: In `Ax≈b`, least squares minimizes the squared norm of the residual.
---
In `Ax≈b`, least squares minimizes the squared norm of the residual. To fit a line, put one column of inputs and one column of ones for the intercept in A. At a solution, the residual is orthogonal to every column of A, which the example verifies.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
import numpy as np

inputs = np.array([0, 1, 2])
observations = np.array([1, 2, 4])
design = np.column_stack((inputs, np.ones(inputs.size)))
coefficients = np.linalg.lstsq(design, observations, rcond=None)[0]
residual = observations - design @ coefficients
print(np.round(coefficients, 3).tolist())
print(bool(np.allclose(design.T @ residual, 0)))
```

```exercise
? How many columns are in the line-fit design matrix?
___
= 2
```

```quiz
? What is the residual orthogonal to?
* The design matrix columns
- Every observation
- Only the x-axis
> A residual component in the column space could be reduced by moving the fitted value within that space.
```

# @lesson matrix-decompositions-svd
title: Singular value decomposition
summary: The factorization `A=UΣVᵀ` applies even to rectangular matrices.
---
The factorization `A=UΣVᵀ` applies even to rectangular matrices. Singular values are nonnegative and describe the stretch along corresponding directions. Keeping only the largest singular value and its vectors gives a rank-one approximation.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
import numpy as np

matrix = np.array([[4, 0, 0], [0, 2, 0]])
left, singular, right = np.linalg.svd(matrix, full_matrices=False)
approximation = singular[0] * np.outer(left[:, 0], right[0])
print(singular.tolist())
print(approximation.tolist())
print(float(np.linalg.norm(matrix - approximation)))
```

```exercise
? What is the largest singular value in the example?
___
= 4
```

```quiz
? What rank results from retaining one vector pair with a positive singular value?
- 2
* 1
- 3
> The outer product of two nonzero vectors has rank one.
```

# @lesson matrix-decompositions-pca
title: Project: reduce two features to one component
summary: In PCA, centre each feature and seek the direction preserving the most variance.
---
In PCA, centre each feature and seek the direction preserving the most variance. The first component is the first right singular vector of the centred data. Here both features lie on one line, so one component captures all variation. Change one point to make reconstruction approximate.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
import numpy as np

data = np.array([[0, 0], [1, 2], [2, 4]])
centre = data.mean(axis=0)
centred = data - centre
_, singular, right = np.linalg.svd(centred, full_matrices=False)
direction = right[0]
scores = centred @ direction
restored = np.outer(scores, direction) + centre
fraction = singular[0] ** 2 / sum(singular ** 2)
print(round(float(fraction), 4), bool(np.allclose(restored, data)))
```

```exercise
? How many components does the example retain?
___
= 1
```

```quiz
? Why subtract each feature’s mean before PCA?
- To make every value zero
- To increase sample size
* To analyse variation about the centre
> Components describe directions of variation relative to the data mean.
```
