# @lesson combinatorics-inclusion
title: Inclusion–exclusion
summary: The size of a two-set union adds the sizes and subtracts the intersection.
---
The size of a two-set union adds the sizes and subtracts the intersection. For three sets, subtract the pairwise intersections and add back the triple one. This corrects each element's count according to how many sets contain it.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
values = range(1, 21)
a = {n for n in values if n % 2 == 0}
b = {n for n in values if n % 3 == 0}
print(len(a), len(b), len(a & b), len(a | b))
```

```exercise
? Given |A|=10, |B|=6 and |A∩B|=3, what is the union size?
___
= 13
```

```quiz
? Why subtract the intersection once?
* Each shared element was counted twice
- Each shared element was counted zero times
- The union contains only the intersection
> Subtracting one copy leaves one occurrence of each shared element.
```

# @lesson combinatorics-pigeonhole
title: The pigeonhole principle
summary: Placing `n` items in `k` boxes forces some box to have at least `ceil(n/k)` items.
---
Placing `n` items in `k` boxes forces some box to have at least `ceil(n/k)` items. If every box had fewer, the total capacity would be below n. The example groups integers by their remainder modulo 3.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from collections import Counter

counts = Counter(value % 3 for value in range(10))
print(sorted(counts.items()))
print(max(counts.values()))
```

```exercise
? With 13 items and 4 boxes, what count is guaranteed in at least one box?
___
= 4
```

```quiz
? Can 8 items fit in 3 boxes with at most 2 per box?
- Yes
* No
- Only if boxes are equal
> The proposed limit allows only six items.
```

# @lesson combinatorics-recurrence
title: Project: count staircase routes
summary: Allow steps of one or two stairs.
---
Allow steps of one or two stairs. Every route to stair n ends from n−1 or n−2. These cases are disjoint, so add their counts. There is one empty route to stair zero and one route to stair one.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
ways = [1, 1]
for n in range(2, 7):
    ways.append(ways[n - 1] + ways[n - 2])
print(ways)
print(ways[6])
```

```exercise
? How many routes lead to stair four?
___
= 5
```

```quiz
? Which two stairs can immediately precede stair six?
- 3 and 4
- 5 and 6
* 4 and 5
> The final move advances by one or two stairs.
```

# @lesson combinatorics-reference
title: Combinatorics study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[combinatorics-en/combinatorics-inclusion|Inclusion–exclusion]]
- [[combinatorics-en/combinatorics-pigeonhole|The pigeonhole principle]]
- [[combinatorics-en/combinatorics-recurrence|Project: count staircase routes]]

Review [[advanced-math-en/advanced-math-combinatorics|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
