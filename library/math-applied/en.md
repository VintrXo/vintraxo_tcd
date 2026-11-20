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

# @lesson algorithmic-algebra-horner
title: Horner’s method
summary: Store coefficients from highest degree to lowest, including zeros.
---
Store coefficients from highest degree to lowest, including zeros. Evaluate `2x²−3x+4` as `(2x−3)x+4`. Start at zero, then multiply the accumulator by x and add each coefficient.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
def evaluate(coefficients, x):
    result = 0
    for coefficient in coefficients:
        result = result * x + coefficient
    return result

for x in (0, 2, -1):
    print(x, evaluate([2, -3, 4], x))
```

```exercise
? What is 3x²+2 at x=2?
___
= 14
```

```quiz
? Which list represents x²+3?
* [1, 0, 3]
- [1, 3]
- [3, 0, 1]
> The zero preserves the position of the x coefficient.
```

# @lesson algorithmic-algebra-division
title: Synthetic division
summary: When dividing by `x−a`, Horner’s recurrence gives quotient coefficients in all but the last accumulated value.
---
When dividing by `x−a`, Horner’s recurrence gives quotient coefficients in all but the last accumulated value. The last value is the remainder `p(a)`. A zero remainder means `x−a` is a factor.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
coefficients = [1, -3, 2]
a = 1
accumulated = [coefficients[0]]
for coefficient in coefficients[1:]:
    accumulated.append(a * accumulated[-1] + coefficient)
print(accumulated[:-1], accumulated[-1])
```

```exercise
? What is the remainder when dividing x²+1 by x−2?
___
= 5
```

```quiz
? What is the quotient in the example?
- x−1
* x−2
- x²−2
> The coefficients [1,−2] represent x−2.
```

# @lesson algorithmic-algebra-gcd
title: Polynomial greatest common divisor
summary: Over rational coefficients, divide and replace the pair with the divisor and remainder until the remainder is zero.
---
Over rational coefficients, divide and replace the pair with the divisor and remainder until the remainder is zero. Normalize the last nonzero polynomial by its leading coefficient to obtain the monic gcd. The code here stores coefficients in ascending degree order to simplify shifted subtraction.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
from fractions import Fraction

def remainder(dividend, divisor):
    result = dividend.copy()
    while result and len(result) >= len(divisor):
        shift = len(result) - len(divisor)
        multiple = result[-1] / divisor[-1]
        for index, coefficient in enumerate(divisor):
            result[index + shift] -= multiple * coefficient
        while result and result[-1] == 0:
            result.pop()
    return result

a = list(map(Fraction, [-1, 0, 1]))
b = list(map(Fraction, [-1, 0, 0, 1]))
while b:
    a, b = b, remainder(a, b)
print([str(coefficient / a[-1]) for coefficient in a])
```

```exercise
? What is the degree of x³−1?
___
= 3
```

```quiz
? What is the monic gcd in the example?
- x+1
- x²−1
* x−1
> In ascending order [−1,1] represents x−1.
```

# @lesson algorithmic-algebra-interpolation
title: Lagrange interpolation project
summary: Exactly one polynomial of degree less than n fits n distinct inputs.
---
Exactly one polynomial of degree less than n fits n distinct inputs. For each point, use a basis polynomial equal to one at its own input and zero at all the others, multiply by the corresponding output, then add. Check that the original observations are reproduced before trying a new input.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
from fractions import Fraction
from math import prod

points = [(0, 1), (1, 2), (2, 5)]

def interpolate(x):
    return sum(y * prod(Fraction(x - other, own - other)
                        for other, _ in points if other != own)
               for own, y in points)

print([str(interpolate(x)) for x, _ in points])
print(interpolate(Fraction(3, 2)))
```

```exercise
? What value does the interpolant return at input 2?
___
= 5
```

```quiz
? Why must inputs be distinct?
* To avoid a zero denominator
- To make every value positive
- To force degree n
> The basis denominators are differences of inputs.
```

# @lesson convex-optimization-convexity
title: Convex sets and functions
summary: A convex set contains the segment joining any two points in it.
---
A convex set contains the segment joining any two points in it. A convex function lies below or on its chords. For `f(x)=x²`, the midpoint value is no greater than the average endpoint value.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
x, y = -1, 3
midpoint = (x + y) / 2
print(midpoint ** 2, (x ** 2 + y ** 2) / 2)
```

```exercise
? What is x² at the midpoint of −1 and 3?
___
= 1
```

```quiz
? Where does a convex function lie relative to its chord?
* Below or on it
- Always above it
- Always on it
> Convexity bounds the value by a weighted average of the endpoint values.
```

# @lesson convex-optimization-gradient
title: Gradients and optimality
summary: For a differentiable convex function on an open convex domain, a zero gradient suffices for a global minimum.
---
For a differentiable convex function on an open convex domain, a zero gradient suffices for a global minimum. For `f(x)=(x−3)²`, the derivative is `2(x−3)`, so x=3 minimizes it.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
for x in (2, 3, 4):
    print(x, (x - 3) ** 2, 2 * (x - 3))
```

```exercise
? What is the derivative of (x−3)² at x=5?
___
= 4
```

```quiz
? Where is the global minimum in the example?
- x=2
* x=3
- x=4
> The derivative vanishes at 3 and the function is convex.
```

# @lesson convex-optimization-projection
title: Project: projected gradient descent
summary: After a descent step, projection returns the point to the feasible set.
---
After a descent step, projection returns the point to the feasible set. To minimize `(x−3)²` under `0≤x≤2`, clip each step to the interval. The solution is 2 because the objective decreases as feasible points approach 3.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
x = 0.0
for _ in range(3):
    candidate = x - 0.25 * 2 * (x - 3)
    x = min(2, max(0, candidate))
    print(x, round((x - 3) ** 2, 3))
```

```exercise
? If a proposed step lands at 2.25, where is its projection onto [0,2]?
___
= 2
```

```quiz
? Why is 3 not a feasible solution to the constrained problem?
- It maximizes the objective
- The derivative is not zero there
* It lies outside the feasible interval
> The constraint excludes values above 2.
```

# @lesson operations-research-linear
title: Modelling and linear programming
summary: Specify decision variables, constraints, and the objective.
---
Specify decision variables, constraints, and the objective. With `x+y≤4`, `x≤2`, and `x,y≥0`, maximize `3x+2y`. The bounded feasible polygon has a vertex attaining the maximum. Check vertices formed by active constraints.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
vertices = [(0, 0), (2, 0), (2, 2), (0, 4)]
value, point = max((3 * x + 2 * y, (x, y)) for x, y in vertices)
print(value, point)
```

```exercise
? What is the objective at (0,4)?
___
= 8
```

```quiz
? Which feasible point attains the maximum?
* (2, 2)
- (0, 4)
- (3, 1)
> The point (2,2) is feasible and gives 10.
```

# @lesson operations-research-integer
title: Integer decisions and linear relaxation
summary: A box count must be an integer.
---
A box count must be an integer. Dropping that requirement enlarges the feasible set and gives an upper bound on a maximization problem. For `2x≤5` and objective `3x`, the continuous optimum is x=2.5, while the best integer is x=2.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
capacity, weight, value = 5, 2, 3
print(value * capacity / weight)
print(value * (capacity // weight))
```

```exercise
? What is the largest integer count of weight-2 boxes in capacity 7?
___
= 3
```

```quiz
? What does a relaxation give for an integer maximization problem?
- Always a lower bound
* An upper bound
- Always an integer solution
> A relaxation retains every original option and may add better ones.
```

# @lesson operations-research-assignment
title: Project: assign jobs to workers
summary: Each worker has a job-dependent cost.
---
Each worker has a job-dependent cost. Assign exactly one worker to each job and one job per worker. For this small example compare all permutations, showing why the first worker’s cheapest job can leave a costly job for the other.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from itertools import permutations

costs = [[1, 3], [2, 9]]
options = [(sum(costs[i][job] for i, job in enumerate(jobs)), jobs)
           for jobs in permutations(range(2))]
print(sorted(options))
```

```exercise
? What is the total cost if each worker takes the job with the same index?
___
= 10
```

```quiz
? What is the minimum total cost?
- 3
- 10
* 5
> The first worker takes the second job for 3, and the second takes the first for 2.
```

# @lesson game-theory-responses
title: Best responses and Nash equilibrium
summary: A best response maximizes a player’s payoff given the other choice.
---
A best response maximizes a player’s payoff given the other choice. At a Nash equilibrium, each player is best responding to the other. Here check each cell for an equilibrium in pure strategies.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
payoffs = [[(2, 2), (0, 0)], [(0, 0), (1, 1)]]
for i, row in enumerate(payoffs):
    for j, (p, q) in enumerate(row):
        if p == max(r[j][0] for r in payoffs) and q == max(cell[1] for cell in row):
            print(i, j)
```

```exercise
? How many pure equilibria are in the example?
___
= 2
```

```quiz
? When is a cell a Nash equilibrium?
* When both players best respond to each other
- Whenever payoffs are equal
- Whenever both payoffs are zero
> No player can improve by changing alone.
```

# @lesson game-theory-mixed
title: Mixed strategies
summary: A mixed strategy is a probability distribution over actions.
---
A mixed strategy is a probability distribution over actions. In matching pennies, the row player wins one for a match and loses one otherwise. If the opponent picks heads with probability p, heads yields expected payoff `2p−1`, and tails yields `1−2p`.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
for probability in (0.25, 0.5, 0.75):
    print(probability, 2 * probability - 1, 1 - 2 * probability)
```

```exercise
? At what p are the two payoffs equal? Enter a decimal.
___
= 0.5
```

```quiz
? At p=0.75, which action gives the row player a higher payoff?
- Tails
* Heads
- They tie
> Heads yields 0.5, tails −0.5.
```

# @lesson game-theory-minimax
title: Project: compare worst-case payoffs
summary: In a zero-sum game the payoffs sum to zero.
---
In a zero-sum game the payoffs sum to zero. In the row payoff matrix, find each row’s worst payoff and choose the row with the largest minimum. This is the best guarantee among pure rows; mixing can improve it.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
payoffs = [[4, -2], [1, 0]]
guarantees = [min(row) for row in payoffs]
print(guarantees)
print(max(guarantees))
```

```exercise
? What is the first row’s worst payoff?
___
= -2
```

```quiz
? Which row guarantees the higher minimum?
- First
- Equal guarantee
* Second
> The second row’s minimum is zero, compared with −2 for the first.
```

# @lesson information-theory-entropy
title: Entropy and information
summary: An event of probability p carries `−log₂(p)` bits of information.
---
An event of probability p carries `−log₂(p)` bits of information. Entropy is the probability-weighted average. Zero-probability terms contribute zero.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import log2

for probabilities in ([0.5, 0.5], [0.75, 0.25]):
    print(round(-sum(p * log2(p) for p in probabilities if p), 4))
```

```exercise
? How many bits of information does a probability-1/4 outcome carry?
___
= 2
```

```quiz
? Which coin has higher entropy here?
* Fair
- Biased
- Neither, they tie
> Equal probabilities maximize uncertainty here.
```

# @lesson information-theory-conditional
title: Conditional entropy
summary: Conditional entropy `H(Y|X)` averages the remaining entropy of Y after each possible X is known.
---
Conditional entropy `H(Y|X)` averages the remaining entropy of Y after each possible X is known. If X determines Y, none remains. The difference `H(Y)−H(Y|X)` is mutual information.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
h_y = 1.0
conditional_entropy = {0: 0.0, 1: 0.0}
h_given_x = sum(0.5 * entropy for entropy in conditional_entropy.values())
print(h_given_x, h_y - h_given_x)
```

```exercise
? If Y equals X, what is H(Y|X)?
___
= 0
```

```quiz
? If X and Y are independent and H(Y)=1, what is H(Y|X)?
- 0
* 1
- 2
> Under independence, knowing X leaves Y’s distribution unchanged.
```

# @lesson information-theory-prefix
title: Project: compare two codes
summary: In a prefix-free code, no codeword begins with another full codeword, so the stream can be split unambiguously.
---
In a prefix-free code, no codeword begins with another full codeword, so the stream can be split unambiguously. Compare two fixed bits per symbol with `0,10,11`, which assigns the shortest word to the most frequent symbol.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from fractions import Fraction

probabilities = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
for codes in (['00', '01', '10'], ['0', '10', '11']):
    print(sum(p * len(code) for p, code in zip(probabilities, codes, strict=True)))
```

```exercise
? What average length does the variable code give? Enter a fraction like 1/2.
___
= 3/2
```

```quiz
? Can 0 and 01 coexist in a prefix-free code?
- Yes
- Only if 01 has even length
* No
> The word 0 is a prefix of 01.
```
