# @lesson differential-geometry-tangent
title: Parametric curves and tangents
summary: The curve `r(t)=(t,t²)` gives a point for each t, and differentiating its coordinates gives the tangent vector `(1,2t)`.
---
The curve `r(t)=(t,t²)` gives a point for each t, and differentiating its coordinates gives the tangent vector `(1,2t)`. When nonzero, this vector gives the tangent line direction.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
t = 2
print((t, t ** 2), (1, 2 * t))
```

```exercise
? What is the second tangent component at t=3?
___
= 6
```

```quiz
? Which vector is tangent at t=0?
* (1, 0)
- (0, 1)
- (0, 0)
> At zero the horizontal derivative is one and the vertical derivative is zero.
```

# @lesson differential-geometry-arc-length
title: Speed and arc length
summary: Speed along a curve is the norm of its derivative.
---
Speed along a curve is the norm of its derivative. Arc length integrates speed. For `r(t)=(R cos t,R sin t)` the derivative has constant norm R, so an arc subtending θ radians has length Rθ.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import pi

radius = 3
print(round(radius * pi / 2, 3))
```

```exercise
? What is the arc length for 2 radians and radius 5?
___
= 10
```

```quiz
? Which quantity is integrated to find arc length?
- The horizontal coordinate
* The norm of the derivative
- The tangent angle alone
> Integrating speed accumulates small distances along the curve.
```

# @lesson differential-geometry-curvature
title: Project: compare curvature on a parabola
summary: For a graph `y=f(x)`, curvature magnitude is `|f″(x)|/(1+f′(x)²)^(3/2)`.
---
For a graph `y=f(x)`, curvature magnitude is `|f″(x)|/(1+f′(x)²)^(3/2)`. On `y=x²` the numerator stays 2 while the denominator grows away from zero. Compare the vertex with two points farther away.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
for x in (0, 1, 2):
    curvature = 2 / (1 + (2 * x) ** 2) ** 1.5
    print(x, round(curvature, 3))
```

```exercise
? What is the curvature of y=x² at x=0?
___
= 2
```

```quiz
? Which sampled point has the largest curvature?
- x=1
- x=2
* x=0
> The denominator is smallest at x=0.
```

# @lesson differential-geometry-reference
title: Introduction to differential geometry study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[differential-geometry-en/differential-geometry-tangent|Parametric curves and tangents]]
- [[differential-geometry-en/differential-geometry-arc-length|Speed and arc length]]
- [[differential-geometry-en/differential-geometry-curvature|Project: compare curvature on a parabola]]

Review [[advanced-math-en/advanced-math-curvature|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
