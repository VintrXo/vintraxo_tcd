# @lesson complex-analysis-polar
title: Polar form
summary: A nonzero complex number has polar form `r(cos θ+i sin θ)`, with magnitude r and angle θ defined modulo a full turn.
---
A nonzero complex number has polar form `r(cos θ+i sin θ)`, with magnitude r and angle θ defined modulo a full turn. Multiplication multiplies magnitudes and adds angles, explaining why multiplication by i rotates.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from cmath import phase
from math import degrees

for z in (1 + 1j, (1 + 1j) * 1j):
    print(round(abs(z), 3), round(degrees(phase(z))))
```

```exercise
? What is the angle in degrees of 1+i from the positive real axis?
___
= 45
```

```quiz
? What does multiplying by i do to the magnitude?
* It stays the same
- It doubles
- It becomes zero
> The magnitude of i is one.
```

# @lesson complex-analysis-roots
title: Roots of unity
summary: Solutions of `zⁿ=1` have magnitude one and angles `2πk/n`, for k from zero through n−1.
---
Solutions of `zⁿ=1` have magnitude one and angles `2πk/n`, for k from zero through n−1. They are equally spaced on the unit circle. The fourth roots give four points, two on each axis.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from cmath import rect
from math import tau

count = 4
for k in range(count):
    root = rect(1, tau * k / count)
    print(round(root.real), round(root.imag), abs(root ** count - 1) < 1e-9)
```

```exercise
? How many distinct complex solutions does z⁶=1 have?
___
= 6
```

```quiz
? How many degrees separate adjacent fourth roots of unity?
- 45
* 90
- 180
> Divide a full turn into four equal angles.
```

# @lesson complex-analysis-derivative
title: Complex derivatives and approach directions
summary: A complex derivative requires the same limit of difference quotients from every step direction.
---
A complex derivative requires the same limit of difference quotients from every step direction. For `z²` the quotient simplifies to `2z+h`. For conjugation it is `conj(h)/h`, giving 1 for real steps and −1 for imaginary steps, so no complex derivative exists.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
z = 1 + 2j
for h in (0.01, 0.01j):
    quotient = ((z + h) ** 2 - z ** 2) / h
    print(round(quotient.real, 2), round(quotient.imag, 2))
    print(round((h.conjugate() / h).real))
```

```exercise
? What is the real part of the derivative of z² at z=1+2i?
___
= 2
```

```quiz
? Why does conjugation lack a complex derivative?
- It requires only real inputs
- The function is always zero
* The quotient depends on direction
> Horizontal steps give 1 and vertical steps give −1.
```

# @lesson complex-analysis-cauchy-riemann
title: Cauchy–Riemann equations
summary: Write `f=u+iv`.
---
Write `f=u+iv`. Complex differentiability requires `uₓ=vᵧ` and `uᵧ=−vₓ`. If the partials are continuous near a point and the equations hold there, they suffice for complex differentiability at that point. For `f(z)=z²`, `u=x²−y²` and `v=2xy`.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
x, y = 2, 3
u_x, u_y = 2 * x, -2 * y
v_x, v_y = 2 * y, 2 * x
print(u_x, u_y, v_x, v_y)
print(u_x == v_y, u_y == -v_x)
```

```exercise
? Evaluate uₓ at x=3 for u=x²−y².
___
= 6
```

```quiz
? Which relation must hold between uᵧ and vₓ?
* uᵧ=−vₓ
- uᵧ=vₓ
- uᵧ=vᵧ
> Comparing the two directions gives the minus sign from division by i.
```

# @lesson complex-analysis-contours
title: Project: integrate around a circle
summary: For the counterclockwise unit circle, put `z(t)=exp(it)` from 0 to `2π`.
---
For the counterclockwise unit circle, put `z(t)=exp(it)` from 0 to `2π`. For `1/z`, the integrand becomes `z′(t)/z(t)=i`, so the integral is `2πi`. Compare with integrating `z` along the same path, which gives zero because `z²/2` is an antiderivative.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from cmath import exp
from math import tau

count = 128
step = tau / count
points = [exp(1j * (i + 0.5) * step) for i in range(count)]
for function in (lambda z: 1 / z, lambda z: z):
    integral = sum(function(z) * (1j * z) * step for z in points)
    print(round(abs(integral), 6))
```

```exercise
? What is the real part of 2πi?
___
= 0
```

```quiz
? What is the integral of z around the circle?
- 2πi
* 0
- 1
> The curve is closed, so the antiderivative has identical values at its endpoints.
```

# @lesson complex-analysis-reference
title: Introduction to complex analysis study guide
summary: Review the examples and connect them with other courses.
type: Reference
---
## Worked examples

- [[complex-analysis-en/complex-analysis-polar|Polar form]]
- [[complex-analysis-en/complex-analysis-roots|Roots of unity]]
- [[complex-analysis-en/complex-analysis-derivative|Complex derivatives and approach directions]]
- [[complex-analysis-en/complex-analysis-cauchy-riemann|Cauchy–Riemann equations]]
- [[complex-analysis-en/complex-analysis-contours|Project: integrate around a circle]]

## Related lessons

- [[math-branches-en/math-branches-complex|Complex numbers]]
- [[real-analysis-en/real-analysis-continuity|Continuity in real analysis]]
