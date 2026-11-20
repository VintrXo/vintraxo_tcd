# @lesson differential-equations-initial
title: Equations and initial conditions
summary: The equation `y′=2t` determines the slope at each time.
---
The equation `y′=2t` determines the slope at each time. Every function `y=t²+C` has that slope. The initial condition `y(0)=3` picks the member with C=3.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
initial = 3
for time in (0, 1, 2):
    value = time ** 2 + initial
    print(time, value)
```

```exercise
? If y′=2t and y(0)=5, find y(2).
___
= 9
```

```quiz
? Why is the initial condition needed here?
* To determine the integration constant
- To change the slope
- To eliminate time
> Many solutions share a derivative and differ by a constant.
```

# @lesson differential-equations-growth
title: Exponential growth and decay
summary: A rate proportional to the current value gives `y′=ky`.
---
A rate proportional to the current value gives `y′=ky`. The solution starting at y₀ is `y₀ exp(kt)`. A positive initial value with negative k decreases over time.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
from math import exp

for time in (0, 1, 2):
    print(time, round(100 * exp(-0.5 * time), 2))
```

```exercise
? Find y at t=0 for y=80 exp(−0.2t).
___
= 80
```

```quiz
? What happens to a positive value in y′=−0.5y as time increases?
- It increases
* It decreases
- It stays constant
> The derivative is negative while y is positive.
```

# @lesson differential-equations-separation
title: Separation of variables
summary: For `y′=−ty` and `y(0)=4`, separate variables where y is nonzero.
---
For `y′=−ty` and `y(0)=4`, separate variables where y is nonzero. Integrating `dy/y=−t dt` gives `ln|y|=−t²/2+C`. The positive initial condition gives `y=4 exp(−t²/2)`. The zero solution also solves the equation but does not satisfy that condition.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
from math import exp

for time in (0, 1, 2):
    print(round(4 * exp(-time ** 2 / 2), 3))
```

```exercise
? What is y(0) for y=7 exp(−t²/2)?
___
= 7
```

```quiz
? Which solution must be checked separately after dividing by y?
- y=1
- y=t
* y=0
> Dividing by y excludes zero from the separation steps.
```

# @lesson differential-equations-euler
title: Project: compare Euler step sizes
summary: Euler’s method updates y using the current slope over a short step.
---
Euler’s method updates y using the current slope over a short step. For `y′=−y` from 0 to 1 with initial value one, compare four and twenty steps against `exp(−1)`. A smaller step reduces error in this example.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
from math import exp

exact = exp(-1)
for steps in (4, 20):
    step = 1 / steps
    y = 1.0
    for _ in range(steps):
        y -= step * y
    print(steps, round(y, 4), round(abs(exact - y), 4))
```

```exercise
? What is the step size for ten equal steps from zero to one?
___
= 0.1
```

```quiz
? Which approximation is closer to the exact solution in the example?
* 20 steps
- 4 steps
- The errors are equal
> The absolute error with twenty steps is smaller in this example.
```

# @lesson differential-equations-reference
title: Ordinary differential equations study guide
summary: Review the workshop examples and return to the branch map.
type: Reference
---
- [[differential-equations-en/differential-equations-initial|Equations and initial conditions]]
- [[differential-equations-en/differential-equations-growth|Exponential growth and decay]]
- [[differential-equations-en/differential-equations-separation|Separation of variables]]
- [[differential-equations-en/differential-equations-euler|Project: compare Euler step sizes]]

Review the [[math-branches-en/math-branches-differential|introductory lesson]] or return to the [[math-branches-en/math-branches-map|branch map]].
