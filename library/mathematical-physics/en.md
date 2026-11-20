# @lesson mathematical-physics-oscillation
title: The harmonic oscillator
summary: For an undamped spring, `mx″=−kx`.
---
For an undamped spring, `mx″=−kx`. Starting at maximum displacement A with zero velocity gives `A cos(ωt)`, where `ω=√(k/m)`. With fixed mass, greater stiffness increases angular frequency.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import pi, sqrt

mass, stiffness = 1, 4
omega = sqrt(stiffness / mass)
print(omega, round(2 * pi / omega, 3))
```

```exercise
? What is the angular frequency for k=9 and m=1?
___
= 3
```

```quiz
? If mass quadruples at fixed stiffness, what happens to angular frequency?
* It halves
- It doubles
- It is unchanged
> Mass is in the denominator under the square root.
```

# @lesson mathematical-physics-energy
title: Energy conservation and model checks
summary: For an ideal spring, the derivative of `E=mv²/2+kx²/2` is `v(mv′+kx)=0`.
---
For an ideal spring, the derivative of `E=mv²/2+kx²/2` is `v(mv′+kx)=0`. Conserved energy provides a check on calculations. Small discrepancies can arise from numerical approximation.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import cos, sin

m, k, amplitude, omega = 1, 4, 0.5, 2
for t in (0, 0.5, 1):
    x = amplitude * cos(omega * t)
    v = -amplitude * omega * sin(omega * t)
    print(round((m * v * v + k * x * x) / 2, 6))
```

```exercise
? What is potential energy at x=0?
___
= 0
```

```quiz
? What remains constant in this model?
- Speed at all times
* Total kinetic plus potential energy
- Displacement at all times
> Energy moves between the two forms while the total stays constant.
```

# @lesson mathematical-physics-wave
title: Project: a travelling wave
summary: The wave `u(x,t)=sin(x−ct)` travels right for positive c: the same phase occurs at a larger x later.
---
The wave `u(x,t)=sin(x−ct)` travels right for positive c: the same phase occurs at a larger x later. Check that its value is constant along `x=x₀+ct`. In the ideal wave equation, propagation speed relates the second space and time derivatives.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import sin

speed, start = 2, 1
for t in (0, 1, 2):
    x = start + speed * t
    print(x, round(sin(x - speed * t), 3))
```

```exercise
? With c=2 and phase starting at x=1, where is it at t=3?
___
= 7
```

```quiz
? Which way does the wave travel for positive c?
- Left
- It is stationary
* Right
> For fixed phase, x increases by ct.
```

# @lesson mathematical-physics-reference
title: Mathematical physics study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[mathematical-physics-en/mathematical-physics-oscillation|The harmonic oscillator]]
- [[mathematical-physics-en/mathematical-physics-energy|Energy conservation and model checks]]
- [[mathematical-physics-en/mathematical-physics-wave|Project: a travelling wave]]

Review [[advanced-math-en/advanced-math-physics|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
