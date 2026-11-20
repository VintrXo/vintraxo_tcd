# @lesson vector-calculus-direction
title: Directional derivatives
summary: To find the rate of change of a scalar field in a unit direction u, take `∇f·u`.
---
To find the rate of change of a scalar field in a unit direction u, take `∇f·u`. At `(1,2)`, the gradient of `f(x,y)=x²+y²` is `(2,4)`. Moving along the positive x-axis gives a rate of 2.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
gradient = (2, 4)
for direction in ((1, 0), (0, 1), (-1, 0)):
    print(sum(a * b for a, b in zip(gradient, direction, strict=True)))
```

```exercise
? What is the rate of change in direction (0,1) in the example?
___
= 4
```

```quiz
? What is the directional derivative in direction (−1,0) at the same point?
* −2
- 2
- −4
> Reversing the x direction negates the first component.
```

# @lesson vector-calculus-divergence
title: Divergence and net outflow
summary: For `F=(P,Q)`, divergence is `∂P/∂x + ∂Q/∂y`.
---
For `F=(P,Q)`, divergence is `∂P/∂x + ∂Q/∂y`. It measures local net outward flux per unit area. For `F=(x,2y)`, divergence is 3, which can be checked by computing flux across the unit square’s sides.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
left, right = 0, 1
bottom, top = 0, 2
outflow = left + right + bottom + top
print(outflow)
print(outflow / 1)  # unit square area
```

```exercise
? What is the divergence of (2x,3y)?
___
= 5
```

```quiz
? How much outward flux comes from the top edge y=1 in the example?
- 1
* 2
- 0
> The vertical component is 2 along the whole edge, of length 1.
```

# @lesson vector-calculus-curl
title: Curl in the plane
summary: For a planar field `F=(P,Q)`, the perpendicular component of curl is `∂Q/∂x − ∂P/∂y`.
---
For a planar field `F=(P,Q)`, the perpendicular component of curl is `∂Q/∂x − ∂P/∂y`. For `F=(−y,x)`, it is 2. At `(1,0)`, the field points upward, consistent with counterclockwise rotation.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
partial_q_x = 1
partial_p_y = -1
print(partial_q_x - partial_p_y)
for x, y in ((1, 0), (0, 1), (-1, 0)):
    print((x, y), (-y, x))
```

```exercise
? What is the planar curl of (−2y,2x)?
___
= 4
```

```quiz
? Where does the field (−y,x) point at (0,1)?
- Up
- Right
* Left
> At this point the field equals (−1,0).
```

# @lesson vector-calculus-work
title: Project: compare work along two paths
summary: Work along `r(t)` integrates `F(r(t))·r′(t)`.
---
Work along `r(t)` integrates `F(r(t))·r′(t)`. For `F=(0,x)`, compare two edge paths from `(0,0)` to `(1,1)`. Horizontal segments contribute zero. Each vertical segment contributes its fixed x value times its vertical displacement.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
paths = [[(0, 0), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 1)]]
for points in paths:
    work = sum(x * (next_y - y) for (x, y), (_, next_y) in zip(points, points[1:]))
    print(work)
```

```exercise
? What is the work on the vertical segment from (2,0) to (2,3)?
___
= 6
```

```quiz
? Do the two endpoints alone determine work in this example?
* No
- Yes
- Only because horizontal work is zero
> The paths share endpoints, but their vertical segments have different x values.
```

# @lesson vector-calculus-reference
title: Vector calculus study guide
summary: Revisit the examples and review related lessons.
type: Reference
---
## Worked examples

- [[vector-calculus-en/vector-calculus-direction|Directional derivatives]]
- [[vector-calculus-en/vector-calculus-divergence|Divergence and net outflow]]
- [[vector-calculus-en/vector-calculus-curl|Curl in the plane]]
- [[vector-calculus-en/vector-calculus-work|Project: compare work along two paths]]

## Related lessons

- [[intermediate-calculus-en/intermediate-calculus-gradient|The gradient]]
- [[differential-geometry-en/differential-geometry-tangent|Curves and tangents]]
