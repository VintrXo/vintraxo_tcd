# @lesson intermediate-algebra-systems
title: Systems of equations
summary: In `x + y = 10` and `2x + y = 16`, subtract the first equation from the second to eliminate y.
---
In `x + y = 10` and `2x + y = 16`, subtract the first equation from the second to eliminate y. Substitute x back into the first. A solution must satisfy both equations.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
x = 16 - 10
y = 10 - x
print(x, y)
print(x + y == 10 and 2 * x + y == 16)
```

```exercise
? Find x when x + y = 7 and 2x + y = 11.
___
= 4
```

```quiz
? What is y in the worked example?
* 4
- 6
- 10
> With x equal to 6, the sum of 10 leaves 4.
```

# @lesson intermediate-algebra-factoring
title: Factoring
summary: Expansion turns products into sums; factoring reverses it.
---
Expansion turns products into sums; factoring reverses it. For `x² + 5x + 6`, find two numbers with sum 5 and product 6, giving `(x + 2)(x + 3)`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
for x in (-3, -2, 0, 1):
    expanded = x ** 2 + 5 * x + 6
    factored = (x + 2) * (x + 3)
    print(x, expanded, factored)
```

```exercise
? One of the numbers used to factor x² + 7x + 10 is 2. What is the other?
___
= 5
```

```quiz
? Which factorization equals x² − 9?
- (x − 9)(x + 1)
* (x − 3)(x + 3)
- (x − 3)²
> A difference of squares factors as the product of the difference and sum.
```

# @lesson intermediate-algebra-quadratics
title: Quadratic equations
summary: For `ax² + bx + c = 0` with `a ≠ 0`, the discriminant `D = b² − 4ac` determines the real roots.
---
For `ax² + bx + c = 0` with `a ≠ 0`, the discriminant `D = b² − 4ac` determines the real roots. Positive D gives two roots `(-b ± √D)/(2a)`, zero gives one repeated root, and negative D gives no real roots.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import sqrt

a, b, c = 1, -5, 6
discriminant = b * b - 4 * a * c
if discriminant < 0:
    print('No real roots')
else:
    roots = {(-b + sign * sqrt(discriminant)) / (2 * a) for sign in (-1, 1)}
    print(sorted(roots))
```

```exercise
? Find the repeated root of x² − 4x + 4 = 0.
___
= 2
```

```quiz
? How many real roots does x² + 1 = 0 have?
- 1
- 2
* 0
> The discriminant is −4.
```

# @lesson intermediate-algebra-exponents
title: Exponents and logarithms
summary: For a positive base `b ≠ 1`, `log_b(x) = y` means `bʸ = x`, with `x > 0`.
---
For a positive base `b ≠ 1`, `log_b(x) = y` means `bʸ = x`, with `x > 0`. For example, `log₂(8) = 3`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import log2

for exponent in (-2, 0, 3):
    value = 2 ** exponent
    print(value, log2(value))
```

```exercise
? What is log₂(32)?
___
= 5
```

```quiz
? What is two raised to the power −3?
* 1/8
- −8
- 8
> A negative exponent gives the reciprocal of the positive power.
```

# @lesson intermediate-algebra-sequences
title: Sequences and series
summary: An arithmetic sequence adds a fixed difference; a geometric sequence multiplies by a fixed ratio.
---
An arithmetic sequence adds a fixed difference; a geometric sequence multiplies by a fixed ratio. A series sums the terms. Starting at a with ratio r gives term n as `a × r^(n−1)`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
arithmetic = [3 + 2 * i for i in range(4)]
geometric = [3 * 2 ** i for i in range(4)]
print(arithmetic, sum(arithmetic))
print(geometric, sum(geometric))
```

```exercise
? What is the fourth term in 2, 6, 18, …?
___
= 54
```

```quiz
? What is the sum of the first four terms in 3, 6, 12, 24, …?
- 24
* 45
- 48
> The series adds the four terms.
```

# @lesson intermediate-algebra-project
title: Project: recover a workshop setup cost
summary: A workshop costs 120 to set up and 15 per attendee.
---
A workshop costs 120 to set up and 15 per attendee. Tickets cost 25. Define revenue and cost, find the smallest attendance that covers the cost, then check what happens if tickets drop to 23.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import ceil

fixed = 120
variable = 15
for price in (25, 23):
    attendees = ceil(fixed / (price - variable))
    profit = attendees * price - (fixed + variable * attendees)
    print(price, attendees, profit)
```

```exercise
? What is the break-even attendance if tickets cost 30?
___
= 8
```

```quiz
? What is the minimum attendance if tickets cost 23?
- 12
- 18
* 15
> Each attendee contributes 8 toward fixed cost, and 120 ÷ 8 is 15.
```

# @lesson intermediate-algebra-reference
title: Intermediate algebra study guide
summary: Revisit the worked examples and follow the connected courses.
type: Reference
---
## Worked examples

- [[intermediate-algebra-en/intermediate-algebra-systems|Systems of equations]]
- [[intermediate-algebra-en/intermediate-algebra-factoring|Factoring]]
- [[intermediate-algebra-en/intermediate-algebra-quadratics|Quadratic equations]]
- [[intermediate-algebra-en/intermediate-algebra-exponents|Exponents and logarithms]]
- [[intermediate-algebra-en/intermediate-algebra-sequences|Sequences and series]]
- [[intermediate-algebra-en/intermediate-algebra-project|Project: recover a workshop setup cost]]

## Related courses

- [[algebra-en/algebra-equations|Linear equations]]
- [[calculus-en/calculus-limits|The idea of a limit]]
