# @lesson discrete-math-logic
title: Logic and truth tables
summary: A proposition has a truth value.
---
A proposition has a truth value. `A and B` is true when both are true, while `A or B` is true when at least one is true. `not` reverses the truth value.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from itertools import product

for a, b in product((False, True), repeat=2):
    print(a, b, a and b, a or b)
```

```exercise
? In how many rows is A or B true?
___
= 3
```

```quiz
? How many rows make A and B true?
* 1
- 2
- 3
> Only the row with both values true qualifies.
```

# @lesson discrete-math-sets
title: Sets
summary: A set contains distinct elements.
---
A set contains distinct elements. A union combines members of either set, an intersection keeps common members, and a difference keeps members of the first that do not occur in the second.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
a = {1, 2, 3}
b = {2, 4}
print(sorted(a.union(b)))
print(sorted(a.intersection(b)))
print(sorted(a.difference(b)))
```

```exercise
? How many elements are in the union of {1, 2} and {2, 3}?
___
= 3
```

```quiz
? Which element is shared by {1, 2, 3} and {3, 4}?
- 1
* 3
- 4
> The element 3 occurs in both sets.
```

# @lesson discrete-math-counting
title: The multiplication principle
summary: If each of three colours comes in the same number of sizes, say two, there are `3 × 2` choices.
---
If each of three colours comes in the same number of sizes, say two, there are `3 × 2` choices. If the number of available sizes varies by colour, add the number of sizes for each colour.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from itertools import product

colours = ['red', 'green', 'blue']
sizes = ['S', 'M']
choices = list(product(colours, sizes))
print(choices)
print(len(choices))
```

```exercise
? How many one-dish, one-drink meals can you make from 4 dishes and 3 drinks?
___
= 12
```

```quiz
? Red comes in two sizes and blue in one. How many choices are there?
- 2
- 4
* 3
> Add 2 + 1 because the numbers of sizes differ.
```

# @lesson discrete-math-combinations
title: Permutations and combinations
summary: Order matters for permutations, such as choosing first and second place.
---
Order matters for permutations, such as choosing first and second place. Combinations only depend on which elements are chosen, such as two committee members without roles. These examples select without repetition.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import comb, perm

print(perm(4, 2))
print(comb(4, 2))
```

```exercise
? How many ways can you pick two students from five for a committee with no roles?
___
= 10
```

```quiz
? How many ways can four entrants fill first and second place?
* 12
- 6
- 8
> There are four choices for first place and then three for second.
```

# @lesson discrete-math-modulo
title: Remainders and cycles
summary: A remainder locates a position inside a cycle.
---
A remainder locates a position inside a cycle. On a 24-hour clock, 5 hours after 22:00 is `(22 + 5) % 24 = 3`. The same idea works for weekdays.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
current = 22
for hours in (1, 2, 5):
    print((current + hours) % 24)
```

```exercise
? What is the remainder when dividing 29 by 7?
___
= 1
```

```quiz
? What hour is it 8 hours after 19:00 on a 24-hour clock?
- 8
* 3
- 27
> The sum is 27; one full 24-hour cycle leaves 3.
```

# @lesson discrete-math-graphs
title: Vertices and edges
summary: A graph is a network of vertices joined by edges.
---
A graph is a network of vertices joined by edges. An undirected edge can be traversed in either direction. A vertex’s degree counts incident edges. These examples have no loops or repeated edges.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
graph = {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
for vertex, neighbours in graph.items():
    print(vertex, len(neighbours))
```

```exercise
? How many edges are there if B and C are connected only to A?
___
= 2
```

```quiz
? What is the degree of A in the example?
- 1
- 3
* 2
> A has two neighbours, B and C.
```

# @lesson discrete-math-routes
title: Project: fewest stops
summary: Represent stops as vertices and connections as edges.
---
Represent stops as vertices and connections as edges. If every connection has equal cost, search by layers: visit nearby stops first, then the next layer. Record each stop’s first distance to avoid revisits when a cycle exists.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from collections import deque

network = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D'], 'D': ['B', 'C', 'E'], 'E': ['D']}
distance = {'A': 0}
queue = deque(['A'])
while queue:
    current = queue.popleft()
    for neighbour in network[current]:
        if neighbour not in distance:
            distance[neighbour] = distance[current] + 1
            queue.append(neighbour)

print(distance['E'])
```

```exercise
? How many connections are needed along a shortest route from A to D?
___
= 2
```

```quiz
? Why record each stop’s first distance?
* To avoid revisiting it when there is a cycle
- To remove all short routes
- To make the graph directed
> Layer-by-layer search first discovers each stop using the fewest connections.
```

Continue with [[dsa-en/dsa-graphs|Graphs in the algorithms course]].

# @lesson discrete-math-reference
title: Discrete mathematics reference
summary: Quick rules and a route through maths for programming and data.
type: Reference
---
```reference
Intersection | Members shared by both sets | {1, 2} ∩ {2, 3} = {2}
Combination | Choose without order | Choose 2 from 4 in 6 ways
Remainder | Locate a position in a cycle | 27 % 24 = 3
```

## Maths for programming and data

For data analysis, start with the foundations below and then apply vectors and matrices in NumPy. For algorithms, continue from the shortest routes project to the graphs lesson in the algorithms course.

1. [[arithmetic-en/arith-ratios|Arithmetic and ratios]]
2. [[algebra-en/algebra-equations|Algebra foundations]]
3. [[functions-en/functions-rule|Functions and graphs]]
4. [[statistics-en/statistics-mean|Statistics and probability]]
5. [[linear-algebra-en/linear-algebra-vectors|Linear algebra]]
6. [[numpy-en/np-arrays|Working with arrays in NumPy]]
