# @lesson math-branches-map
title: Map of mathematical branches
summary: Choose a starting point and see how the branches connect.
type: Reference
---
Use the linked courses to build foundations. Then explore one idea in each of the thirteen introductory lessons in this survey.

## Courses in the library

- [[math-arithmetic-algebra-en/arith-order|Arithmetic and ratios]]
- [[math-arithmetic-algebra-en/algebra-variables|Algebra foundations]]
- [[math-functions-trig-en/functions-rule|Functions and graphs]]
- [[math-geometry-en/geometry-rectangles|Geometry]]
- [[math-functions-trig-en/trigonometry-angles|Trigonometry]]
- [[math-calculus-en/calculus-limits|Calculus]]
- [[math-linear-algebra-en/linear-algebra-vectors|Linear algebra]]
- [[math-statistics-en/statistics-mean|Statistics and probability]]
- [[math-discrete-en/discrete-math-logic|Discrete mathematics]]
- [[math-arithmetic-algebra-en/intermediate-algebra-systems|Intermediate algebra]]
- [[math-statistics-en/applied-statistics-bayes|Applied probability and statistics]]
- [[math-linear-algebra-en/applied-linear-algebra-elimination|Applied linear algebra]]
- [[math-geometry-en/geometry-trigonometry-congruence|Intermediate geometry and trigonometry]]
- [[math-calculus-en/intermediate-calculus-chain|Intermediate calculus]]
- [[math-discrete-en/mathematical-proof-direct|Mathematical proof techniques]]
- [[math-discrete-en/number-theory-division|Number theory]]
- [[math-pure-en/real-analysis-sequences|Introduction to real analysis]]
- [[math-calculus-en/differential-equations-initial|Ordinary differential equations]]
- [[math-applied-en/numerical-methods-error|Numerical methods]]
- [[math-pure-en/abstract-algebra-groups|Abstract algebra]]
- [[math-pure-en/complex-analysis-polar|Introduction to complex analysis]]
- [[math-pure-en/topology-open-sets|Introduction to topology]]
- [[math-pure-en/measure-theory-sigma|Introduction to measure theory]]

## Specialist courses

- [[math-pure-en/functional-analysis-norm|Functional analysis]]
- [[math-physics-en/differential-geometry-tangent|Differential geometry]]
- [[math-physics-en/partial-differential-equations-partials|Partial differential equations]]
- [[math-physics-en/mathematical-physics-oscillation|Mathematical physics]]
- [[math-discrete-en/combinatorics-inclusion|Combinatorics]]
- [[math-pure-en/category-theory-composition|Category theory]]
- [[math-applied-en/operations-research-linear|Optimization and operations research]]
- [[math-statistics-en/stochastic-processes-transition|Stochastic processes]]
- [[math-applied-en/information-theory-entropy|Information theory]]
- [[math-applied-en/game-theory-responses|Game theory]]
- [[math-calculus-en/vector-calculus-direction|Vector calculus]]
- [[math-physics-en/fourier-analysis-harmonics|Introduction to Fourier analysis]]
- [[math-physics-en/fourier-series-synthesis|Fourier series and the heat equation]]
- [[math-physics-en/vector-integral-theorems-green|Integral theorems in vector calculus]]
- [[math-linear-algebra-en/matrix-decompositions-least-squares|Least squares, SVD, and PCA]]
- [[math-statistics-en/statistical-models-normal|Statistical distributions and models]]
- [[math-pure-en/complex-residues-cauchy|Cauchy, Laurent series, and residues]]
- [[math-pure-en/integration-spaces-convergence|Convergence theorems, Banach and Hilbert spaces]]
- [[math-discrete-en/graph-theory-degree|Graph theory]]
- [[math-applied-en/convex-optimization-convexity|Convex optimization]]
- [[math-physics-en/fourier-waves-standing|Fourier series and the wave equation]]
- [[math-applied-en/algorithmic-algebra-horner|Algorithmic algebra]]
- [[math-geometry-en/computational-geometry-orientation|Computational geometry]]

## Choose a direction

For proofs, start with logic and number theory, then try abstract algebra and real analysis. For modelling, learn calculus before differential equations, then try numerical methods and optimization. For data, start with descriptive statistics and probability before inference and stochastic models.

## Topics for deeper study

After this survey, open the guide to advanced topics to try examples in measure theory, functional analysis, differential geometry, partial differential equations, mathematical physics, advanced combinatorics, and category theory.

# @lesson math-branches-numbers
title: Number theory
summary: Euclid’s algorithm repeatedly replaces the pair with the divisor and remainder, preserving the greatest common divisor until the remainder is zero.
---
Euclid’s algorithm repeatedly replaces the pair with the divisor and remainder, preserving the greatest common divisor until the remainder is zero.

## Try it yourself

```try python
a, b = 84, 30
while b:
    a, b = b, a % b
print(a)
```

```exercise
? Find the gcd of 12 and 30.
___
= 6
```

```quiz
? What is the gcd of 18 and 24?
* 6
- 2
- 12
> Six divides both numbers, and no larger divisor of 18 divides 24.
```

# @lesson math-branches-proof
title: Logic and proof
summary: One counterexample refutes a universal claim.
---
One counterexample refutes a universal claim. To prove the square of any even integer is even, write it as `2k`; its square `4k²` is divisible by two.

## Try it yourself

```try python
for n in (2, 3, 5, 7):
    if n % 2 == 0:
        print(n)
```

```exercise
? Give the smallest positive counterexample to the claim that all multiples of three are even.
___
= 3
```

```quiz
? Which number refutes the claim that every prime is odd?
- 3
* 2
- 7
> Two is prime and even.
```

# @lesson math-branches-abstract
title: Abstract algebra
summary: Addition modulo five gives an example of a group: the operation is closed and associative, zero is the identity, and each element has an inverse.
---
Addition modulo five gives an example of a group: the operation is closed and associative, zero is the identity, and each element has an inverse. The inverse of two is three because their sum is zero modulo five.

## Try it yourself

```try python
for x in range(5):
    print(x, (-x) % 5)
```

```exercise
? What is the identity for addition modulo five?
___
= 0
```

```quiz
? What is the additive inverse of one modulo five?
- 0
- 1
* 4
> The sum of one and four is divisible by five.
```

# @lesson math-branches-analysis
title: Real analysis
summary: The sequence `1/n` converges to zero.
---
The sequence `1/n` converges to zero. For any positive tolerance `ε`, choose an integer `N > 1/ε`. Then `1/n < ε` for every `n ≥ N`, however small the tolerance.

## Try it yourself

```try python
from fractions import Fraction

for tolerance in (Fraction(1, 10), Fraction(1, 100)):
    n = int(1 / tolerance) + 1
    print(n, Fraction(1, n) < tolerance)
```

```exercise
? Find the smallest positive integer n with 1/n < 0.1.
___
= 11
```

```quiz
? What is the smallest positive integer n satisfying 1/n < 0.01?
* 101
- 100
- 99
> At 100 there is equality, but the inequality is strict.
```

# @lesson math-branches-complex
title: Complex numbers
summary: Represent `a + bi` by the point `(a, b)`, with `i² = −1`.
---
Represent `a + bi` by the point `(a, b)`, with `i² = −1`. Multiplying by `i` maps `(a, b)` to `(−b, a)`, a 90-degree counterclockwise rotation. This arithmetic is preparation for complex analysis.

## Try it yourself

```try python
print((2 + 3j) * 1j)
print(abs(3 + 4j))
```

```exercise
? What is the imaginary part of (2 + 3i) × i? Enter the coefficient of i.
___
= 2
```

```quiz
? What is the magnitude of 3 + 4i?
- 7
* 5
- 25
> Take the square root of the squared sum.
```

# @lesson math-branches-topology
title: Topology
summary: Topology studies properties preserved by continuous deformation without cutting or gluing.
---
Topology studies properties preserved by continuous deformation without cutting or gluing. On a number line, one interval is connected, while two intervals separated by a gap give two connected components.

## Try it yourself

```try python
def connected(first, second):
    left, right = sorted((first, second))
    return left[1] >= right[0]

print(connected((0, 1), (1, 2)))
print(connected((0, 1), (2, 3)))
```

```exercise
? How many connected components are in [0, 1] union [2, 3]?
___
= 2
```

```quiz
? How many connected components are in the union of the closed intervals [0, 1] and [1, 2]?
- 2
- 3
* 1
> They meet at 1 and their union is [0, 2].
```

# @lesson math-branches-differential
title: Differential equations
summary: A differential equation relates a function to its rate of change.
---
A differential equation relates a function to its rate of change. In `y′ = −0.2y` the quantity decreases at a rate proportional to its value. Euler’s method estimates the next value by adding the current rate times the step size.

## Try it yourself

```try python
y = 100
for _ in range(3):
    y += -0.2 * y * 0.5
    print(round(y, 2))
```

```exercise
? Start at 50 with rate −10 and step 0.5. Find the next estimate.
___
= 45
```

```quiz
? If the initial value is 100, the rate is −20, and the step is 0.5, what is the next estimate?
* 90
- 80
- 110
> Add −20 × 0.5 to 100.
```

# @lesson math-branches-numerical
title: Numerical methods
summary: Bisection brackets a root of a continuous function between endpoints of opposite signs.
---
Bisection brackets a root of a continuous function between endpoints of opposite signs. Evaluate the midpoint and keep the half with opposite signs, or stop if the midpoint is a root.

## Try it yourself

```try python
def f(x):
    return x * x - 2

left, right = 1, 2
for _ in range(12):
    middle = (left + right) / 2
    if f(middle) > 0:
        right = middle
    else:
        left = middle
print(round((left + right) / 2, 3))
```

```exercise
? What is the midpoint of the interval from one to three?
___
= 2
```

```quiz
? An interval has length eight. What is its length after two halvings?
- 4
* 2
- 1
> Divide by two twice.
```

# @lesson math-branches-optimization
title: Optimization and operations research
summary: Optimization chooses a feasible decision with the best objective value.
---
Optimization chooses a feasible decision with the best objective value. Item A uses two units of space and is worth four. B uses three units and is worth seven. Enumerate choices that fit in capacity seven.

## Try it yourself

```try python
choices = []
for a in range(4):
    for b in range(3):
        if 2 * a + 3 * b <= 7:
            choices.append((4 * a + 7 * b, a, b))
print(max(choices))
```

```exercise
? How much capacity do two A items and one B item use?
___
= 7
```

```quiz
? What is the highest attainable value in the example?
- 14
- 21
* 15
> Two of A and one of B use all the capacity and yield 15.
```

# @lesson math-branches-inference
title: Statistical inference
summary: We use a sample to estimate population characteristics.
---
We use a sample to estimate population characteristics. With independent observations, the estimated standard error of a proportion is the square root of `p(1 − p)/n`, where `p` is the sample proportion. A larger sample reduces variability but does not cure bias.

## Try it yourself

```try python
from math import sqrt

p = 0.6
for size in (100, 400):
    print(round(sqrt(p * (1 - p) / size), 4))
```

```exercise
? Write 30 successes out of 100 as a decimal like 0.25.
___
= 0.3
```

```quiz
? With the proportion fixed, by what factor must sample size grow to halve standard error?
* 4
- 2
- 8
> The square root of four is two.
```

# @lesson math-branches-stochastic
title: Stochastic models
summary: In a Markov model, the distribution of the next state depends on the current state.
---
In a Markov model, the distribution of the next state depends on the current state. Here rain tomorrow has probability 0.2 after a dry day and 0.6 after rain. Weight each transition by the probability of today’s state.

## Try it yourself

```try python
rain = 0.0
for _ in range(3):
    rain = 0.2 * (1 - rain) + 0.6 * rain
    print(round(rain, 3))
```

```exercise
? Write tomorrow’s rain probability as a decimal if it rains today with certainty.
___
= 0.6
```

```quiz
? What is tomorrow’s probability of rain if today’s is 0.5?
- 0.2
* 0.4
- 0.6
> Compute 0.5 × 0.2 + 0.5 × 0.6.
```

# @lesson math-branches-information
title: Information theory
summary: Shannon entropy measures uncertainty before an outcome is known.
---
Shannon entropy measures uncertainty before an outcome is known. A fair coin has one bit of entropy. A certain outcome has zero. Sum `−p × log₂(p)` for every positive probability.

## Try it yourself

```try python
from math import log2

def entropy(probabilities):
    return -sum(p * log2(p) for p in probabilities if p > 0)

print(entropy([0.5, 0.5]))
print(round(entropy([0.75, 0.25]), 4))
```

```exercise
? How many bits of entropy does a fair coin have?
___
= 1
```

```quiz
? How many bits of entropy does a certain outcome have?
- 1
- 2
* 0
> A certain outcome has probability one, whose logarithm is zero.
```

# @lesson math-branches-games
title: Game theory
summary: In a two-player game, a player's payoff can depend on their opponent’s decision.
---
In a two-player game, a player's payoff can depend on their opponent’s decision. A strictly dominant strategy beats every alternative for every opposing choice. This example lists one player's payoffs for two strategies against two columns.

## Try it yourself

```try python
a = [3, 4]
b = [1, 5]
for payoff_a, payoff_b in zip(a, b, strict=True):
    print('A' if payoff_a > payoff_b else 'B')
```

```exercise
? What is the best response to the first column? Enter A or B.
___
= A
```

```quiz
? What is the player's best response to the second column?
* B
- A
- A or B
> In the second column B pays five, compared with four for A.
```
