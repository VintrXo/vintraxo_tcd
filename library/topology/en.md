# @lesson topology-open-sets
title: Open sets
summary: On the real line, a set is open if every point in it has a small interval entirely inside the set.
---
On the real line, a set is open if every point in it has a small interval entirely inside the set. The interval `(0,1)` is open because an interior point is a positive distance from both ends. The set `[0,1]` is not open in the real line because every interval about zero includes negative numbers.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from fractions import Fraction

x = Fraction(1, 4)
radius = min(x, 1 - x) / 2
print(radius)
print(0 < x - radius < x + radius < 1)
```

```exercise
? On the real line, how far is 0.75 from endpoint 1? Enter a decimal.
___
= 0.25
```

```quiz
? Why is [0,1] not open in the real line?
* Every interval about zero leaves the set
- It has no interior points
- Because its length is one
> Openness requires a neighbourhood staying inside the set at every point, including zero if it belongs.
```

# @lesson topology-finite-spaces
title: Topology on a finite set
summary: A topology is a family of open sets containing the empty set and whole space, closed under arbitrary unions and finite intersections.
---
A topology is a family of open sets containing the empty set and whole space, closed under arbitrary unions and finite intersections. On a finite space it is enough to check pairwise unions and intersections and the two required sets.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
space = frozenset({'a', 'b', 'c'})
empty = frozenset()
family = {empty, frozenset({'a'}), frozenset({'a', 'b'}), space}
closed = all(a | b in family and a & b in family for a in family for b in family)
print(len(family), empty in family and space in family and closed)
```

```exercise
? How many points are in the open set {a,b}?
___
= 2
```

```quiz
? Which operation must stay in the family for an arbitrary collection of open sets?
- Complement
* Union
- Set difference
> Closure under unions includes infinite unions.
```

# @lesson topology-continuity
title: Continuity via preimages
summary: A map is continuous if the preimage of every open set in the target is open in the source.
---
A map is continuous if the preimage of every open set in the target is open in the source. A preimage collects all inputs whose outputs lie in the chosen set. For `f(x)=2x+1`, the preimage of `(3,7)` is `(1,3)` because `3<2x+1<7` is equivalent to `1<x<3`.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from fractions import Fraction

for endpoint in (3, 7):
    print(Fraction(endpoint - 1, 2))
```

```exercise
? For f(x)=2x+1, which input maps to 9?
___
= 4
```

```quiz
? Which set must be open in the source when testing continuity?
- The image of any source open set
- The preimage of every set
* The preimage of any target open set
> Continuity pulls open sets back from target to source.
```

# @lesson topology-connectedness
title: Connectedness and separation
summary: A space is connected if it cannot be partitioned into two disjoint nonempty relatively open sets.
---
A space is connected if it cannot be partitioned into two disjoint nonempty relatively open sets. Intervals of the real line are connected. For the union of `[0,1]` and `[2,3]`, intersecting with `(-∞,1.5)` and `(1.5,∞)` gives two relatively open sets witnessing a separation.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
first, second = (0, 1), (2, 3)
separator = (first[1] + second[0]) / 2
print(separator)
print(first[1] < separator < second[0])
```

```exercise
? How wide is the gap between [0,1] and [2,3]?
___
= 1
```

```quiz
? How many connected components does the union of [0,1] and [2,3] have?
* 2
- 1
- 3
> Each interval is connected, and the gap separates the two.
```

# @lesson topology-compactness
title: Compactness and open covers
summary: A space is compact if every open cover has a finite subcover.
---
A space is compact if every open cover has a finite subcover. On the real line, closed bounded sets are compact. The sets `(1/n,1)` for all n≥2 cover `(0,1)`, but a finite choice has a largest n and leaves points nearer zero uncovered.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from fractions import Fraction

chosen = [2, 5, 10]
smallest_left_endpoint = Fraction(1, max(chosen))
missed = smallest_left_endpoint / 2
print(smallest_left_endpoint, missed)
print(any(Fraction(1, n) < missed < 1 for n in chosen))
```

```exercise
? What is the denominator of the smallest left endpoint in the example?
___
= 10
```

```quiz
? Which set is compact in the real line?
- (0,1)
* [0,1]
- [0,∞)
> The interval [0,1] is closed and bounded, so Heine–Borel applies.
```

# @lesson topology-reference
title: Introduction to topology study guide
summary: Revisit the examples and related lessons.
type: Reference
---
## Worked examples

- [[topology-en/topology-open-sets|Open sets]]
- [[topology-en/topology-finite-spaces|Topology on a finite set]]
- [[topology-en/topology-continuity|Continuity via preimages]]
- [[topology-en/topology-connectedness|Connectedness and separation]]
- [[topology-en/topology-compactness|Compactness and open covers]]

## Related lessons

- [[math-branches-en/math-branches-topology|Topology overview]]
- [[real-analysis-en/real-analysis-continuity|Epsilon–delta continuity]]
