# @lesson calculus-limits
title: The idea of a limit
summary: A limit describes the value a function approaches as its input approaches a point.
---
A limit describes the value a function approaches as its input approaches a point. The expression `(x² − 1)/(x − 1)` equals `x + 1` for `x ≠ 1`, so the limit at 1 is 2 even though the original expression is undefined there.

For a refresher, see [[functions-en/functions-slope|Slope and intercept]].

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
for x in (0.9, 0.99, 1.01, 1.1):
    print(x, round((x ** 2 - 1) / (x - 1), 4))
```

```exercise
? What does x + 4 approach as x approaches 2?
___
= 6
```

```quiz
? Why can’t we substitute x = 1 directly into the fraction?
* The denominator becomes zero
- The numerator becomes one
- The limit has to be zero
> We examine the expression near 1, where the denominator is nonzero.
```

# @lesson calculus-rate
title: From average to instantaneous rate
summary: A secant slope divides the change in output by the change in input.
---
A secant slope divides the change in output by the change in input. As the points approach one another, the secant slope can approach the tangent slope. This limit, when it exists, is the derivative at that point.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
def f(x):
    return x ** 2

x = 2
for h in (0.1, 0.01, 0.001):
    print(round((f(x + h) - f(x)) / h, 6))
```

```exercise
? What is the average rate of change of f(x) = x² from x = 1 to x = 3?
___
= 4
```

```quiz
? What does the slope approach at x = 2 in the example?
- 2
* 4
- 8
> The difference quotient simplifies to 4 + h and approaches 4.
```

# @lesson calculus-power
title: The power rule
summary: For polynomials, the derivative of `xⁿ` for positive integer `n` is `n × xⁿ⁻¹`.
---
For polynomials, the derivative of `xⁿ` for positive integer `n` is `n × xⁿ⁻¹`. Differentiate each term separately and retain its coefficient. A constant has derivative zero because it does not change with input.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
def derivative(x):
    # Derivative of 3x² + 2x + 5
    return 6 * x + 2

for x in (0, 1, 2):
    print(x, derivative(x))
```

```exercise
? What is the derivative of x³ at x = 2?
___
= 12
```

```quiz
? What is the derivative of 4x³ − 2x + 7?
- 4x² − 2
- 12x² − 2x + 7
* 12x² − 2
> The term derivatives are 12x², −2, and zero.
```

# @lesson calculus-optimize
title: Finding a maximum
summary: If a derivative changes from positive to negative at an interior point, the function rises and then falls.
---
If a derivative changes from positive to negative at an interior point, the function rises and then falls. For a maximum on a closed interval, also check its endpoints. A rectangle of perimeter 20 has area `w(10 − w)` with derivative `10 − 2w`.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
def area(width):
    return width * (10 - width)

for width in (0, 4, 5, 6, 10):
    print(width, area(width))
```

```exercise
? What width maximizes the rectangle’s area?
___
= 5
```

```quiz
? What is the maximum area of a rectangle of perimeter 20?
* 25
- 24
- 20
> The derivative is zero at 5, giving 5 × 5; the endpoint areas are zero.
```

# @lesson calculus-integral
title: Integration as a sum of areas
summary: For a positive function, approximate the area under the curve by summing narrow rectangles.
---
For a positive function, approximate the area under the curve by summing narrow rectangles. This example uses each subinterval’s right endpoint. Increasing the number of rectangles takes the sum closer to the definite integral, which is 1/2 for `f(x) = x` from 0 to 1.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
for count in (4, 10, 100):
    width = 1 / count
    area = sum((index * width) * width for index in range(1, count + 1))
    print(count, round(area, 4))
```

```exercise
? What is the area under the constant function f(x) = 3 from x = 0 to x = 4?
___
= 12
```

```quiz
? Why do right-endpoint rectangles overestimate the area under x?
- The rectangles are wider than the full interval
* The right endpoint has the highest value in each interval
- The function is decreasing
> The function increases, so the rectangle uses the greatest height in its subinterval.
```

# @lesson calculus-distance
title: Project: find distance from speed
summary: An object moves at `2t + 1` metres per second from 0 to 4 seconds.
---
An object moves at `2t + 1` metres per second from 0 to 4 seconds. Integrate speed to obtain distance. The derivative of `t² + t` is `2t + 1`, so evaluate it at both endpoints and subtract. Compare the exact distance with a rectangle estimate.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
def speed(time):
    return 2 * time + 1

def antiderivative(time):
    return time ** 2 + time

end = 4
count = 100
width = end / count
estimate = sum(speed(i * width) * width for i in range(1, count + 1))
print(antiderivative(end) - antiderivative(0))
print(round(estimate, 2))
```

```exercise
? How far does the object travel from time 0 to time 3, in metres?
___
= 12
```

```quiz
? What is the unit when integrating metres per second over seconds?
- Metre per second
- Square metre
* Metre
> Multiply the unit of speed by the unit of time to get length.
```

# @lesson calculus-reference
title: Introduction to calculus reference
summary: Core rules and examples for quick review.
type: Reference
---
```reference
Limit | Track output near an input | x + 1 approaches 2 at x = 1
Derivative | Instantaneous slope | The derivative of x² is 2x
Definite integral | Accumulate a rate over an interval | Integrating speed gives distance
```
