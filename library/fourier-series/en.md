# @lesson fourier-series-synthesis
title: Signal reconstruction
summary: A Fourier series combines a constant, sines, and cosines.
---
A Fourier series combines a constant, sines, and cosines. A partial sum keeps only finitely many harmonics. For `f(x)=1+2cos(x)+sin(3x)`, stopping at harmonic one drops the last term. Compare two inputs, since the error may vanish at a particular point.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import cos, pi, sin

for x in (0, pi / 2):
    partial = 1 + 2 * cos(x)
    full = partial + sin(3 * x)
    print(round(partial, 3), round(full, 3))
```

```exercise
? What is the partial sum at x=0?
___
= 3
```

```quiz
? Which term restores the full value in the example?
* sin(3x)
- cos(3x)
- sin(x)
> Stopping at the first harmonic omits the third.
```

# @lesson fourier-series-sine-series
title: Sine series on an interval
summary: On `[0,L]`, each `sin(nπx/L)` vanishes at both ends.
---
On `[0,L]`, each `sin(nπx/L)` vanishes at both ends. Its coefficient is `2/L` times the integral of the function multiplied by that mode. The example estimates the first coefficients of a two-mode profile using midpoint quadrature.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import pi, sin

length = 1
count = 128
width = length / count
points = [(index + 0.5) * width for index in range(count)]
for mode in (1, 3):
    integral = sum((sin(pi * x) + 0.5 * sin(3 * pi * x)) * sin(mode * pi * x)
                   for x in points) * width
    print(mode, round(2 * integral / length, 6))
```

```exercise
? What is the third mode coefficient? Enter a decimal.
___
= 0.5
```

```quiz
? What is the value of each sine mode at x=L?
- 1
* 0
- L
> For integer n, sin(nπ) is zero.
```

# @lesson fourier-series-heat
title: Project: cool a rod with two modes
summary: For a rod with both ends fixed at zero, mode `sin(nπx/L)` decays by `exp(−κ(nπ/L)²t)` in the heat equation.
---
For a rod with both ends fixed at zero, mode `sin(nπx/L)` decays by `exp(−κ(nπ/L)²t)` in the heat equation. Split the starting profile into two modes, apply their decay factors, and add them. Mode three has nine times mode one’s exponential decay rate.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import exp, pi, sin

length, diffusivity = 1, 1 / pi ** 2
x = 0.5
for time in (0, 0.25, 1):
    first = exp(-diffusivity * (pi / length) ** 2 * time)
    third = 0.5 * exp(-diffusivity * (3 * pi / length) ** 2 * time)
    temperature = first * sin(pi * x / length) + third * sin(3 * pi * x / length)
    print(time, round(temperature, 3))
```

```exercise
? How many times faster is the decay rate of mode three than mode one?
___
= 9
```

```quiz
? Which mode persists longer?
- Third
- They decay at the same rate
* First
> The decay rate is proportional to the square of the mode number.
```

# @lesson fourier-series-reference
title: Fourier series and the heat equation study guide
summary: Revisit the examples and review the prerequisite.
type: Reference
---
- [[fourier-series-en/fourier-series-synthesis|Signal reconstruction]]
- [[fourier-series-en/fourier-series-sine-series|Sine series on an interval]]
- [[fourier-series-en/fourier-series-heat|Project: cool a rod with two modes]]

Review [[fourier-analysis-en/fourier-analysis-coefficients|the prerequisite lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
