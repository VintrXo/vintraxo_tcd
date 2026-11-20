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

# @lesson matrix-decompositions-reference
title: Least squares, SVD, and PCA study guide
summary: Revisit the examples and review the prerequisite.
type: Reference
---
- [[matrix-decompositions-en/matrix-decompositions-least-squares|Matrix least squares]]
- [[matrix-decompositions-en/matrix-decompositions-svd|Singular value decomposition]]
- [[matrix-decompositions-en/matrix-decompositions-pca|Project: reduce two features to one component]]

Review [[applied-linear-algebra-en/applied-linear-algebra-projection|the prerequisite lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
