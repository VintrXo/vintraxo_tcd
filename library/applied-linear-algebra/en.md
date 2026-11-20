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

# @lesson applied-linear-algebra-reference
title: Applied linear algebra study guide
summary: Revisit the worked examples and follow the connected courses.
type: Reference
---
## Worked examples

- [[applied-linear-algebra-en/applied-linear-algebra-elimination|Elimination for linear systems]]
- [[applied-linear-algebra-en/applied-linear-algebra-span|Span and linear independence]]
- [[applied-linear-algebra-en/applied-linear-algebra-determinant|Determinants and invertibility]]
- [[applied-linear-algebra-en/applied-linear-algebra-eigen|Eigenvalues and eigenvectors]]
- [[applied-linear-algebra-en/applied-linear-algebra-projection|Projection onto a direction]]
- [[applied-linear-algebra-en/applied-linear-algebra-project|Project: transform a shape with NumPy]]

## Related courses

- [[linear-algebra-en/linear-algebra-multiply|Matrix multiplication]]
- [[numpy-en/np-arrays|Creating NumPy arrays]]
