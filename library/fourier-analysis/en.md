# @lesson fourier-analysis-harmonics
title: Periods and harmonics
summary: Harmonic n over a `2π` cycle, such as `sin(nx)`, completes n oscillations per cycle.
---
Harmonic n over a `2π` cycle, such as `sin(nx)`, completes n oscillations per cycle. Adding harmonics produces a more complex periodic signal. The aim is to describe that signal by the amplitudes and phases of its waves.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import pi, sin

for angle in (0, pi / 4, pi / 2):
    print(round(sin(angle), 3), round(sin(2 * angle), 3))
```

```exercise
? How many oscillations does sin(4x) complete from 0 to 2π?
___
= 4
```

```quiz
? What is the period of sin(2x)?
* π
- 2π
- 4π
> The inner angle doubles, so x only needs to increase by π.
```

# @lesson fourier-analysis-orthogonality
title: Orthogonality of harmonics
summary: Over a full cycle, the integral of `sin(mx)sin(nx)` is zero for distinct positive integers m and n.
---
Over a full cycle, the integral of `sin(mx)sin(nx)` is zero for distinct positive integers m and n. It is π when m=n. This isolates each frequency’s contribution. The example uses sample averages to illustrate the difference.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import sin, tau

points = [tau * index / 64 for index in range(64)]
for harmonic in (1, 2):
    average = sum(sin(x) * sin(harmonic * x) for x in points) / len(points)
    print(harmonic, f'{round(average, 6) + 0.0:.6f}')
```

```exercise
? What is the full-cycle average of sin²(x)? Enter a decimal.
___
= 0.5
```

```quiz
? What is the full-cycle integral of sin(x)sin(3x)?
- π
* 0
- 2π
> The harmonics are distinct, so the positive and negative contributions cancel.
```

# @lesson fourier-analysis-coefficients
title: Fourier coefficients
summary: For `f(x)=1+2cos(x)+3sin(2x)`, its full-period mean gives the constant term.
---
For `f(x)=1+2cos(x)+3sin(2x)`, its full-period mean gives the constant term. Twice the mean of f times the chosen sine or cosine gives that harmonic’s coefficient. Its squared mean is one half, while its mean product with the other harmonics is zero.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import cos, sin, tau

count = 64
points = [tau * index / count for index in range(count)]
values = [1 + 2 * cos(x) + 3 * sin(2 * x) for x in points]
constant = sum(values) / count
cos_one = 2 * sum(y * cos(x) for x, y in zip(points, values, strict=True)) / count
sin_two = 2 * sum(y * sin(2 * x) for x, y in zip(points, values, strict=True)) / count
print(*(round(value, 4) for value in (constant, cos_one, sin_two)))
```

```exercise
? What is the coefficient of cos(x) in 4 + 5cos(x)?
___
= 5
```

```quiz
? What is the signal’s full-cycle mean in the example?
- 2
- 3
* 1
> The sine and cosine average to zero, leaving the constant 1.
```

# @lesson fourier-analysis-spectrum
title: Project: detect two signal frequencies
summary: The discrete transform compares samples against complex exponentials at different frequencies.
---
The discrete transform compares samples against complex exponentials at different frequencies. Here scan four positive candidate frequencies in a two-tone signal and compare coefficient magnitudes. Change one wave’s amplitude and observe its matching frequency bin.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from cmath import exp
from math import sin, tau

count = 32
signal = [sin(tau * i / count) + 0.5 * sin(tau * 3 * i / count)
          for i in range(count)]
for frequency in range(1, 5):
    coeff = sum(value * exp(-1j * tau * frequency * i / count)
                for i, value in enumerate(signal))
    print(frequency, round(2 * abs(coeff) / count, 3))
```

```exercise
? What is the amplitude of frequency three in the example? Enter a decimal.
___
= 0.5
```

```quiz
? Which two frequencies are present in the signal?
* 1 and 3
- 1 and 2
- 2 and 4
> Among the frequencies scanned, only bins 1 and 3 have nonzero magnitude.
```

# @lesson fourier-analysis-reference
title: Introduction to Fourier analysis study guide
summary: Revisit the examples and review related lessons.
type: Reference
---
## Worked examples

- [[fourier-analysis-en/fourier-analysis-harmonics|Periods and harmonics]]
- [[fourier-analysis-en/fourier-analysis-orthogonality|Orthogonality of harmonics]]
- [[fourier-analysis-en/fourier-analysis-coefficients|Fourier coefficients]]
- [[fourier-analysis-en/fourier-analysis-spectrum|Project: detect two signal frequencies]]

## Related lessons

- [[trigonometry-en/trigonometry-period|Sine and periodicity]]
- [[partial-differential-equations-en/partial-differential-equations-partials|The heat equation]]
