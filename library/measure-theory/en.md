# @lesson measure-theory-sigma
title: Sigma algebras
summary: A sigma algebra specifies which sets are measurable.
---
A sigma algebra specifies which sets are measurable. It contains the whole space and is closed under complements and countable unions, so it also contains the empty set. On a finite partition, unions of its blocks give a sigma algebra.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from itertools import combinations

blocks = [{'a', 'b'}, {'c'}]
sets = {frozenset().union(*chosen) for size in range(len(blocks) + 1)
        for chosen in combinations(blocks, size)}
print(len(sets))
print(frozenset({'a'}) in sets)
```

```exercise
? How many unions of blocks come from a partition into three nonempty blocks?
___
= 8
```

```quiz
? Why is {a} absent from the example sigma algebra?
* Because a and b belong to one indivisible block
- Because singletons are never measurable
- Because the empty set is disallowed
> The example sets are unions of whole partition blocks.
```

# @lesson measure-theory-additivity
title: Measures and disjoint additivity
summary: A measure sends the empty set to zero and adds measures over countable pairwise disjoint unions.
---
A measure sends the empty set to zero and adds measures over countable pairwise disjoint unions. On a finite space, choose a nonnegative weight per point and sum the weights of the set’s members. Overlapping sets cannot simply be added because shared points would count twice.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
weights = {'a': 2, 'b': 3, 'c': 5}

def measure(points):
    return sum(weights[point] for point in points)

left, right = {'a', 'b'}, {'b', 'c'}
print(measure(left), measure(right))
print(measure(left | right), measure(left & right))
```

```exercise
? Under the example weights, what is the measure of {a,c}?
___
= 7
```

```quiz
? What do we subtract from the sum of measures for the overlapping union here?
- The measure of the empty set
* The measure of the intersection
- The measure of the union
> Each set measure includes the intersection, so subtract one copy.
```

# @lesson measure-theory-functions
title: Measurable functions
summary: A real-valued function is measurable if each interval `(-∞,t]` has a measurable preimage.
---
A real-valued function is measurable if each interval `(-∞,t]` has a measurable preimage. In a space with the sigma algebra of partition unions, a function constant on each block passes every threshold test. Distinguishing two points in a block yields a threshold with a nonmeasurable preimage.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
outputs = {'a': 2, 'b': 2, 'c': 5}
for cutoff in (1, 2, 5):
    preimage = [point for point, value in outputs.items() if value <= cutoff]
    print(cutoff, preimage)
```

```exercise
? How many points are in the preimage at threshold 2?
___
= 2
```

```quiz
? If a and b share a block but f(a)=2 and f(b)=4, which threshold separates them?
- 1
- 5
* 3
> The value 2 is at or below threshold 3, while value 4 is above it.
```

# @lesson measure-theory-integral
title: Integrating simple functions
summary: A simple function takes finitely many values.
---
A simple function takes finitely many values. Integrate it by multiplying each value by the measure of its level set and adding. For disjoint intervals with length measure this sums rectangles. On a finite probability space, the integral equals expectation.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from fractions import Fraction

terms = [(2, Fraction(1, 4)), (6, Fraction(3, 4))]
print(sum(weight for _, weight in terms))
print(sum(value * weight for value, weight in terms))
```

```exercise
? If value 8 has weight 0.5, what does it contribute to the integral?
___
= 4
```

```quiz
? What is the expectation in the example?
* 5
- 4
- 8
> Compute 2×(1/4)+6×(3/4).
```

# @lesson measure-theory-approximation
title: Project: approximate an integral with simple functions
summary: Approximate `f(x)=x` on `[0,1]` from below by splitting it into `2^k` equal pieces and taking each left endpoint’s value.
---
Approximate `f(x)=x` on `[0,1]` from below by splitting `[0,1)` into `2^k` equal intervals closed on the left and open on the right. Take each left endpoint’s value on its interval, and set the approximation to 1 at endpoint 1. Under repeated halving the simple functions increase pointwise to x, and the integrals tend to 1/2. The endpoint contributes zero to the integral because a point has zero length.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from fractions import Fraction

for count in (2, 4, 8):
    width = Fraction(1, count)
    lower = sum(index * width * width for index in range(count))
    print(count, lower, Fraction(1, 2) - lower)
```

```exercise
? Write the shortfall from 1/2 with 8 pieces as a fraction like 1/2.
___
= 1/16
```

```quiz
? Why is this a lower approximation?
- The left endpoint has the largest value
* x is increasing, so the left endpoint has the lowest value
- Points have negative measure
> The function x increases, so the rectangle stays below the graph on each piece.
```

# @lesson measure-theory-reference
title: Introduction to measure theory study guide
summary: Revisit the examples and related lessons.
type: Reference
---
## Worked examples

- [[measure-theory-en/measure-theory-sigma|Sigma algebras]]
- [[measure-theory-en/measure-theory-additivity|Measures and disjoint additivity]]
- [[measure-theory-en/measure-theory-functions|Measurable functions]]
- [[measure-theory-en/measure-theory-integral|Integrating simple functions]]
- [[measure-theory-en/measure-theory-approximation|Project: approximate an integral with simple functions]]

## Related lessons

- [[advanced-math-en/advanced-math-measure|Measure theory overview]]
- [[calculus-en/calculus-integral|Integration as a sum of areas]]
