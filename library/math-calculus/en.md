# @lesson calculus-limits
title: The idea of a limit
summary: A limit describes the value a function approaches as its input approaches a point.
---
A limit describes the value a function approaches as its input approaches a point. The expression `(x² − 1)/(x − 1)` equals `x + 1` for `x ≠ 1`, so the limit at 1 is 2 even though the original expression is undefined there.

For a refresher, see [[math-functions-trig-en/functions-slope|Slope and intercept]].

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

# @lesson intermediate-calculus-chain
title: The chain rule
summary: For `y = f(g(x))`, multiply the outer derivative at `g(x)` by the inner derivative.
---
For `y = f(g(x))`, multiply the outer derivative at `g(x)` by the inner derivative. For `(3x+1)²`, multiply `2(3x+1)` by 3.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
def derivative(x):
    return 2 * (3 * x + 1) * 3

for x in (0, 1, 2):
    print(x, derivative(x))
```

```exercise
? What is the derivative of (2x + 1)² at x = 1?
___
= 12
```

```quiz
? What is the derivative of (3x + 1)²?
* 6(3x + 1)
- 2(3x + 1)
- 6x
> The factor of three comes from the inner derivative.
```

# @lesson intermediate-calculus-substitution
title: Integration by substitution
summary: Substitution reverses the chain rule.
---
Substitution reverses the chain rule. For `2x(1+x²)`, choose `u = 1+x²`, giving `du = 2x dx`. In a definite integral, convert both limits to u as well. The interval x = 0 to 1 becomes u = 1 to 2.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
def antiderivative(u):
    return u ** 2 / 2

print(antiderivative(2) - antiderivative(1))
```

```exercise
? If u = 1 + x², what is u when x = 2?
___
= 5
```

```quiz
? What is the integral in the example?
- 2
* 1.5
- 0.5
> An antiderivative of u is u²/2. Its values at 2 and 1 differ by 1.5.
```

# @lesson intermediate-calculus-parts
title: Integration by parts
summary: The product rule gives `∫u dv = uv − ∫v du`.
---
The product rule gives `∫u dv = uv − ∫v du`. For `x·exp(x)`, choose `u=x` and `dv=exp(x)dx`, obtaining `(x−1)exp(x)` as an antiderivative. Differentiate it to check.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from math import exp

def antiderivative(x):
    return (x - 1) * exp(x)

print(antiderivative(1) - antiderivative(0))
```

```exercise
? Evaluate the definite integral of x·exp(x) from zero to one.
___
= 1
```

```quiz
? Why is u = x a useful choice here?
- Its derivative is zero
- Because exp(x) is constant
* Its derivative is one, simplifying the integral
> The remaining integral is just the integral of exp(x).
```

# @lesson intermediate-calculus-partial
title: Partial derivatives
summary: For a function of two variables, a partial derivative changes one variable while holding the other fixed.
---
For a function of two variables, a partial derivative changes one variable while holding the other fixed. For `f(x,y) = x² + xy + y²`, the partial derivatives are `2x+y` with respect to x and `x+2y` with respect to y.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
x, y = 2, 3
partial_x = 2 * x + y
partial_y = x + 2 * y
print(partial_x, partial_y)
```

```exercise
? Evaluate the x partial derivative at (1, 2) in the example.
___
= 4
```

```quiz
? What is the y partial derivative of xy with x fixed?
* x
- y
- xy
> With x fixed, xy is linear in y with coefficient x.
```

# @lesson intermediate-calculus-gradient
title: The gradient
summary: The gradient is the vector of partial derivatives.
---
The gradient is the vector of partial derivatives. When nonzero it points in the direction of steepest local increase. A small step in the opposite direction is expected to reduce the function. Choose a suitable step and check the result.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
def loss(x, y):
    return x ** 2 + y ** 2

x, y = 2, 3
step = 0.1
print(loss(x, y))
print(round(loss(x - step * 2 * x, y - step * 2 * y), 2))
```

```exercise
? What is the first component of the gradient of x² + y² at (2, 3)?
___
= 4
```

```quiz
? Which direction is used for a small descent step?
- Along the gradient
* Opposite the gradient
- Always a fixed direction
> The gradient points toward local increase; its opposite gives local decrease.
```

# @lesson intermediate-calculus-fit
title: Project: improve a two-parameter model
summary: A model predicts y as `m*x+b`.
---
A model predicts y as `m*x+b`. Measure the mean squared error and compute its partial derivatives with respect to slope and intercept. Start with both parameters zero, then take two steps against the gradient and compare the errors.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
points = [(0, 1), (1, 3), (2, 5)]
slope = intercept = 0
for _ in range(3):
    errors = [(x, slope * x + intercept - y) for x, y in points]
    print(round(sum(error ** 2 for _, error in errors) / len(points), 3))
    d_slope = 2 * sum(x * error for x, error in errors) / len(points)
    d_intercept = 2 * sum(error for _, error in errors) / len(points)
    slope -= 0.1 * d_slope
    intercept -= 0.1 * d_intercept
```

```exercise
? If the model is y = 2x + 1, what does it predict at x = 2?
___
= 5
```

```quiz
? Why calculate both derivatives before updating either parameter?
- So that error is always zero
- So that the intercept stays fixed
* So both components describe the same point
> The gradient is evaluated at one parameter pair before taking a single step.
```

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
