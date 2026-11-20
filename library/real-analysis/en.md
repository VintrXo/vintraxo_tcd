# @lesson real-analysis-sequences
title: Convergence of sequences
summary: A sequence `aₙ` converges to L when for every positive ε there is an N such that `|aₙ−L|<ε` for all `n≥N`.
---
A sequence `aₙ` converges to L when for every positive ε there is an N such that `|aₙ−L|<ε` for all `n≥N`. For `aₙ=2/n`, choose `N>2/ε`, which makes the bound hold thereafter.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
from fractions import Fraction

epsilon = Fraction(1, 10)
cutoff = 2 // epsilon + 1
print(cutoff)
print(Fraction(2, cutoff) < epsilon)
```

```exercise
? What is the smallest N with 2/n<0.2 for every n≥N?
___
= 11
```

```quiz
? Which terms must satisfy the convergence bound?
* Every n≥N
- Only the term at N
- One term above N
> The condition holds throughout the entire tail.
```

# @lesson real-analysis-continuity
title: Epsilon–delta continuity
summary: A function f is continuous at a if `|f(x)−f(a)|<ε` holds whenever `|x−a|<δ` for some positive δ for each positive ε.
---
A function f is continuous at a if `|f(x)−f(a)|<ε` holds whenever `|x−a|<δ` for some positive δ for each positive ε. For `f(x)=3x+2`, the output gap is three times the input gap, so choose `δ=ε/3`.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
from fractions import Fraction

a = 2
epsilon = Fraction(3, 10)
delta = epsilon / 3
x = a + delta / 2
print(delta)
print(abs((3 * x + 2) - (3 * a + 2)) < epsilon)
```

```exercise
? For ε=0.6 in the example, what is δ under the given rule? Enter a decimal.
___
= 0.2
```

```quiz
? What happens to the output gap when the input gap is less than δ?
- It always equals ε
* It is below ε
- It is above ε
> The output gap is three times the input gap, hence below 3δ=ε.
```

# @lesson real-analysis-supremum
title: The least upper bound
summary: An upper bound is at least as large as every element.
---
An upper bound is at least as large as every element. The supremum is the least such bound. The interval `(0, 1)` has supremum 1 even though it excludes 1, because any smaller number leaves some interval point above it.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
from fractions import Fraction

for denominator in (10, 100, 1000):
    point = 1 - Fraction(1, denominator)
    print(point, point < 1)
```

```exercise
? What is the supremum of (0, 5)?
___
= 5
```

```quiz
? Does (0, 1) have a largest element?
- Yes, 1
- Yes, 0
* No
> For every x in the interval, (x+1)/2 is inside and larger.
```

# @lesson real-analysis-uniform
title: Pointwise and uniform convergence
summary: Uniform convergence uses one N for all inputs at a given tolerance.
---
Uniform convergence uses one N for all inputs at a given tolerance. On `[0,1]`, `fₙ(x)=x/n` converges uniformly to zero because the error is at most `1/n` everywhere. The grid illustrates the bound; the inequality proves it for every input.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
grid = [i / 10 for i in range(11)]
for n in (2, 10, 100):
    print(n, max(x / n for x in grid))
```

```exercise
? At n=20, what is the largest error on [0,1]? Enter a decimal.
___
= 0.05
```

```quiz
? What must be shared by all x for uniform convergence?
* The cutoff N at a fixed tolerance
- The value of fₙ(x)
- All x must be equal
> The uniform cutoff is independent of x.
```

# @lesson real-analysis-reference
title: Introduction to real analysis study guide
summary: Review the workshop examples and return to the branch map.
type: Reference
---
- [[real-analysis-en/real-analysis-sequences|Convergence of sequences]]
- [[real-analysis-en/real-analysis-continuity|Epsilon–delta continuity]]
- [[real-analysis-en/real-analysis-supremum|The least upper bound]]
- [[real-analysis-en/real-analysis-uniform|Pointwise and uniform convergence]]

Review the [[math-branches-en/math-branches-analysis|introductory lesson]] or return to the [[math-branches-en/math-branches-map|branch map]].
