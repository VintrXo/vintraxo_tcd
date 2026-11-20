# @lesson vector-integral-theorems-green
title: Green’s theorem
summary: For a suitable planar region with counterclockwise boundary, Green’s theorem equates circulation around the boundary with the area integral of `Qₓ−Pᵧ`.
---
For a suitable planar region with counterclockwise boundary, Green’s theorem equates circulation around the boundary with the area integral of `Qₓ−Pᵧ`. For `F=(0,x)` on a square of side 2, only the upward right edge contributes, and the curl inside is 1.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
side = 2
right_edge = side * side
area = side ** 2
print(right_edge, 1 * area)
```

```exercise
? What is the integral of constant curl 1 over a square of side 3?
___
= 9
```

```quiz
? What happens to the line integral if the boundary direction reverses?
* Its sign reverses
- It doubles
- It always stays fixed
> Reversal flips the tangent and therefore the sign of the dot product.
```

# @lesson vector-integral-theorems-stokes
title: Stokes’ theorem and surface integrals
summary: Stokes’ theorem equates the flux of `∇×F` through an oriented surface with the circulation of F around its right-hand-oriented boundary.
---
Stokes’ theorem equates the flux of `∇×F` through an oriented surface with the circulation of F around its right-hand-oriented boundary. Flux integrates the dot product with the unit normal. For an upward-facing disk and `F=(−y,x,0)`, normal curl is 2, and the dot product along its angle-parameterized circular edge is `r²`.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import pi, tau

radius = 3
surface_flux = 2 * pi * radius ** 2
boundary_circulation = radius ** 2 * tau
print(round(surface_flux, 3), round(boundary_circulation, 3))
```

```exercise
? What is the vertical curl component in this example?
___
= 2
```

```quiz
? How is the boundary traversed when viewed from above the upward-facing disk?
- Clockwise
* Counterclockwise
- With no orientation
> With the right thumb upward, the curled fingers indicate the positive direction.
```

# @lesson vector-integral-theorems-gauss
title: Project: calculate flux out of a box
summary: The divergence theorem equates outward flux across a closed surface with the volume integral of divergence.
---
The divergence theorem equates outward flux across a closed surface with the volume integral of divergence. For `F=(x,2y,3z)` on a box from the origin with side lengths `(2,3,4)`, the coordinate-zero faces contribute nothing. Compute the opposite faces and compare with divergence times volume.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
x, y, z = 2, 3, 4
face_fluxes = [x * y * z, 2 * y * x * z, 3 * z * x * y]
volume = x * y * z
print(face_fluxes)
print(sum(face_fluxes), (1 + 2 + 3) * volume)
```

```exercise
? What is the divergence of the project field?
___
= 6
```

```quiz
? Why does the face x=0 contribute zero flux?
- The face has zero area
- Because the box is open
* The normal component of the field is zero
> The face normal lies on the x-axis and the field’s x component vanishes there.
```

# @lesson vector-integral-theorems-reference
title: Integral theorems in vector calculus study guide
summary: Revisit the examples and review the prerequisite.
type: Reference
---
- [[vector-integral-theorems-en/vector-integral-theorems-green|Green’s theorem]]
- [[vector-integral-theorems-en/vector-integral-theorems-stokes|Stokes’ theorem and surface integrals]]
- [[vector-integral-theorems-en/vector-integral-theorems-gauss|Project: calculate flux out of a box]]

Review [[vector-calculus-en/vector-calculus-work|the prerequisite lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
