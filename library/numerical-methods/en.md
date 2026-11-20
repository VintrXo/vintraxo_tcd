# @lesson numerical-methods-error
title: Absolute and relative error
summary: Absolute error is the magnitude of the gap between an approximation and a reference.
---
Absolute error is the magnitude of the gap between an approximation and a reference. Relative error divides that gap by the magnitude of a nonzero reference so errors on different scales can be compared.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
reference = 100
approximation = 98
absolute = abs(approximation - reference)
print(absolute)
print(absolute / abs(reference))
```

```exercise
? For reference 40 and approximation 42, what is the absolute error?
___
= 2
```

```quiz
? When is the usual relative error formula undefined?
* When the reference is zero
- Whenever approximation equals reference
- When absolute error decreases
> The denominator is the magnitude of the reference.
```

# @lesson numerical-methods-bisection
title: Bisection and error bounds
summary: Start with a continuous function and opposite signs at a bracket’s endpoints.
---
Start with a continuous function and opposite signs at a bracket’s endpoints. Test the midpoint each step; if it is not a root, keep the half that brackets a sign change. After k halvings the width is the original width divided by `2^k`, and the midpoint is within half this width of any root in the bracket.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
def f(x):
    return x * x * x - 2

left, right = 1.0, 2.0
for _ in range(8):
    middle = (left + right) / 2
    if f(middle) == 0:
        left = right = middle
        break
    if f(left) * f(middle) < 0:
        right = middle
    else:
        left = middle
print(round((left + right) / 2, 4))
print(round((right - left) / 2, 6))
```

```exercise
? If the bracket starts at width 16, what is its width after three halvings?
___
= 2
```

```quiz
? If the final bracket width is 0.02, what is the midpoint error bound?
- 0.02
* 0.01
- 0.04
> An endpoint is the farthest possible point from the midpoint, half a bracket away.
```

# @lesson numerical-methods-newton
title: Newton’s method
summary: Approximate the function by its tangent at the guess x.
---
Approximate the function by its tangent at the guess x. The tangent’s intercept gives the next guess `x−f(x)/f′(x)`. The derivative must be nonzero at a step. Convergence depends on the function and the starting guess.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
guess = 2.0
for _ in range(3):
    guess -= (guess ** 2 - 2) / (2 * guess)
    print(round(guess, 6))
```

```exercise
? What is the next guess after 2 in the example?
___
= 1.5
```

```quiz
? What happens to the update formula when the derivative is zero at the guess?
- The guess always increases by one
- It gives the relative error
* The update is undefined at that step
> The derivative is the denominator in the update.
```

# @lesson numerical-methods-trapezoid
title: Project: compare trapezoidal approximations
summary: The trapezoidal rule replaces each curve segment by the line between its endpoints.
---
The trapezoidal rule replaces each curve segment by the line between its endpoints. Its area is width times the average endpoint height. Compare estimates for integrating `x²` from 0 to 1 with the exact value 1/3.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
def f(x):
    return x ** 2

for count in (2, 4, 8):
    width = 1 / count
    inside = sum(f(index * width) for index in range(1, count))
    area = width * (inside + (f(0) + f(1)) / 2)
    print(count, round(area, 6), round(abs(area - 1 / 3), 6))
```

```exercise
? What is each width if [0,1] is split into four equal parts?
___
= 0.25
```

```quiz
? What happens to absolute error when going from two to eight parts here?
* It falls
- It rises
- It is unchanged
> The displayed estimates move closer to 1/3.
```

# @lesson numerical-methods-reference
title: Numerical methods study guide
summary: Review the workshop examples and return to the branch map.
type: Reference
---
- [[numerical-methods-en/numerical-methods-error|Absolute and relative error]]
- [[numerical-methods-en/numerical-methods-bisection|Bisection and error bounds]]
- [[numerical-methods-en/numerical-methods-newton|Newton’s method]]
- [[numerical-methods-en/numerical-methods-trapezoid|Project: compare trapezoidal approximations]]

Review the [[math-branches-en/math-branches-numerical|introductory lesson]] or return to the [[math-branches-en/math-branches-map|branch map]].
