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

# @lesson intermediate-calculus-reference
title: Intermediate calculus study guide
summary: Review the examples and revisit related lessons.
type: Reference
---
## Examples in this course

- [[intermediate-calculus-en/intermediate-calculus-chain|The chain rule]]
- [[intermediate-calculus-en/intermediate-calculus-substitution|Integration by substitution]]
- [[intermediate-calculus-en/intermediate-calculus-parts|Integration by parts]]
- [[intermediate-calculus-en/intermediate-calculus-partial|Partial derivatives]]
- [[intermediate-calculus-en/intermediate-calculus-gradient|The gradient]]
- [[intermediate-calculus-en/intermediate-calculus-fit|Project: improve a two-parameter model]]

## Related lessons

- [[calculus-en/calculus-power|The power rule]]
- [[applied-statistics-en/applied-statistics-regression|Simple linear regression]]
