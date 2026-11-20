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

Continue with Graphs in the algorithms course.

# @lesson mathematical-proof-direct
title: Direct proof
summary: To prove two odd integers have an even sum, write them as `2a+1` and `2b+1`.
---
To prove two odd integers have an even sum, write them as `2a+1` and `2b+1`. Their sum is `2(a+b+1)`, twice an integer. The example illustrates the algebra, which applies to every integer pair.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
a, b = 3, -2
left, right = 2 * a + 1, 2 * b + 1
print(left, right, left + right)
print(2 * (a + b + 1))
```

```exercise
? If a = 4, what is 2a+1?
___
= 9
```

```quiz
? Which expression directly shows the sum is even?
* 2(a+b+1)
- a+b+1
- 2a+1
> A factor of two multiplying an integer establishes evenness.
```

## Write a proof

Prove that an even integer plus an odd integer is odd.

:::tip Check your work after trying
Write the integers as `2a` and `2b+1`. Their sum is `2(a+b)+1`, which is odd.
:::

# @lesson mathematical-proof-contrapositive
title: Contraposition
summary: To prove “if n squared is even, then n is even,” show “if n is odd, then n squared is odd.” If `n=2k+1`, its square is `2(2k²+2k)+1`.
---
To prove “if n squared is even, then n is even,” show “if n is odd, then n squared is odd.” If `n=2k+1`, its square is `2(2k²+2k)+1`. Swapping the premise and conclusion alone gives the converse, a separate statement.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
for n in (1, 3, 7):
    print(n, n * n, n * n % 2)
```

```exercise
? What is the remainder when the square of 5 is divided by 2?
___
= 1
```

```quiz
? What is the contrapositive of: if P then Q?
- If Q then P
* If not Q then not P
- If not P then not Q
> Negate both propositions and reverse their roles.
```

## Write a proof

Use contraposition to prove that n is odd if n³ is odd.

:::tip Check your work after trying
If n is even, write it as `2k`. Its cube is `8k³=2(4k³)`, which is even. This is the contrapositive.
:::

# @lesson mathematical-proof-contradiction
title: Proof by contradiction
summary: Assume the negation of the claim and derive a contradiction.
---
Assume the negation of the claim and derive a contradiction. To show there is no largest integer, suppose M is largest. Then `M+1` is an integer larger than M, contradicting the assumption.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
candidate = 1000
counterexample = candidate + 1
print(counterexample)
print(counterexample > candidate)
```

```exercise
? What integer follows 999?
___
= 1000
```

```quiz
? Which assumption leads to the contradiction?
- That integers can be added
- That one is an integer
* That a largest integer exists
> Finding M+1 contradicts the maximality of M.
```

## Write a proof

Use contradiction to prove that there is no smallest integer.

:::tip Check your work after trying
Suppose m is the smallest. Then `m−1` is an integer smaller than m, contradicting the assumption.
:::

# @lesson mathematical-proof-induction
title: Mathematical induction
summary: Prove the first n positive odd integers sum to `n²`.
---
Prove the first n positive odd integers sum to `n²`. The base case n=1 gives one. Assuming the formula at k, add the next odd integer `2k+1` to get `k²+2k+1=(k+1)²`. The base case and step together cover every positive n.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
k = 5
previous_sum = sum(range(1, 2 * k, 2))
next_odd = 2 * k + 1
print(previous_sum, next_odd, previous_sum + next_odd)
```

```exercise
? What is the sum of the first four positive odd integers?
___
= 16
```

```quiz
? What do you add to advance from k to k+1?
* 2k+1
- 2k−1
- k+1
> The kth odd term is 2k−1; the next is two larger.
```

## Write a proof

Use induction to prove that the first n positive even integers sum to `n(n+1)`.

:::tip Check your work after trying
At n=1 the sum is 2. If the kth sum is `k(k+1)`, add `2(k+1)` to obtain `(k+1)(k+2)`.
:::

# @lesson number-theory-division
title: Division and remainders
summary: For `b>0`, every integer `a` is uniquely `a=bq+r` with `0≤r<b`.
---
For `b>0`, every integer `a` is uniquely `a=bq+r` with `0≤r<b`. The divisor b divides a exactly when r is zero. Python’s `divmod(a,b)` returns `(q,r)`.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
for a in (23, -23, 25):
    quotient, remainder = divmod(a, 5)
    print(a, quotient, remainder)
```

```exercise
? What is the remainder of 38 divided by 7?
___
= 3
```

```quiz
? When does 5 divide a?
* When the remainder is zero
- When the quotient is zero
- When the remainder is 5
> A zero remainder means a=5q for an integer q.
```

# @lesson number-theory-primes
title: Primes and factorization
summary: A prime is an integer greater than one with only one and itself as positive divisors.
---
A prime is an integer greater than one with only one and itself as positive divisors. A composite n has a factor no greater than √n, since two larger factors would multiply to more than n. Repeated division extracts prime factors with multiplicity.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
value = 84
factor = 2
factors = []
while factor * factor <= value:
    while value % factor == 0:
        factors.append(factor)
        value //= factor
    factor += 1
if value > 1:
    factors.append(value)
print(factors)
```

```exercise
? What is the smallest prime factor of 35?
___
= 5
```

```quiz
? Which list gives the prime factors of 18 with multiplicity?
- 2, 9
* 2, 3, 3
- 3, 6
> The product is 18 and every listed factor is prime.
```

# @lesson number-theory-euclid
title: Euclid and Bézout’s identity
summary: The gcd of a and b equals the gcd of b and the remainder of a divided by b.
---
The gcd of a and b equals the gcd of b and the remainder of a divided by b. Track coefficients through each step to express the gcd as `sa+tb`, a Bézout identity.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
a, b = 30, 18
old_r, r = a, b
old_s, s = 1, 0
old_t, t = 0, 1
while r:
    quotient = old_r // r
    old_r, r = r, old_r - quotient * r
    old_s, s = s, old_s - quotient * s
    old_t, t = t, old_t - quotient * t
print(old_r, old_s, old_t)
print(old_s * a + old_t * b)
```

```exercise
? Find the gcd of 21 and 14.
___
= 7
```

```quiz
? Which combination gives the gcd of 30 and 18?
- 30−18
- 30+18
* −30+2×18
> −30+36 gives 6, the last nonzero remainder in Euclid’s algorithm.
```

# @lesson number-theory-inverse
title: Congruence and modular inverse
summary: Two values are congruent modulo m when their difference is divisible by m.
---
Two values are congruent modulo m when their difference is divisible by m. The inverse of a satisfies `ax ≡ 1` modulo m. It exists exactly when the gcd of a and m is one, as Bézout’s identity shows.

## Try it yourself

Work out the result first, then run the example and change an input.

```try python
modulus = 7
value = 3
inverses = [x for x in range(modulus) if value * x % modulus == 1]
print(inverses)
```

```exercise
? What is the multiplicative inverse of 2 modulo 5?
___
= 3
```

```quiz
? Does 2 have a multiplicative inverse modulo 6?
* No
- Yes, 2
- Yes, 3
> The gcd is 2, and multiples of 2 remain even modulo 6.
```

# @lesson advanced-math-combinatorics
title: Advanced combinatorics
summary: Inclusion–exclusion corrects repeated counting.
---
Inclusion–exclusion corrects repeated counting. For three sets, add their sizes, subtract the sizes of the pairwise intersections, then add the size of the triple intersection. An object in all three sets then contributes exactly once.

Review the prerequisite idea in [[math-discrete-en/discrete-math-combinations|Permutations and combinations]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
numbers = range(1, 31)
a = {n for n in numbers if n % 2 == 0}
b = {n for n in numbers if n % 3 == 0}
c = {n for n in numbers if n % 5 == 0}
count = len(a) + len(b) + len(c)
count -= len(a & b) + len(a & c) + len(b & c)
count += len(a & b & c)
print(count, len(a | b | c))
```

```exercise
? Two sets have eight and five elements with two shared. How large is their union?
___
= 11
```

```quiz
? What do we do with the triple intersection after subtracting the pairwise intersections?
- Subtract it again
- Always ignore it
* Add it once
> A triple-intersection element was added and subtracted three times, so add it once to count it.
```

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

# @lesson graph-theory-degree
title: Degrees and the handshake lemma
summary: In an undirected loop-free graph, each edge adds one to the degree of both endpoints.
---
In an undirected loop-free graph, each edge adds one to the degree of both endpoints. The degree sum is twice the number of edges. Consequently an even number of vertices have odd degree.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from collections import Counter

edges = [('A', 'B'), ('A', 'C'), ('C', 'D')]
degrees = Counter(vertex for edge in edges for vertex in edge)
print(sorted(degrees.items()))
print(sum(degrees.values()), 2 * len(edges))
```

```exercise
? If the degree sum is 14, how many edges are there?
___
= 7
```

```quiz
? How many vertices have odd degree in the example?
* 2
- 1
- 3
> B and D each have degree one.
```

# @lesson graph-theory-trees
title: Trees and unique paths
summary: A tree is connected and acyclic.
---
A tree is connected and acyclic. It has exactly one simple path between every vertex pair and `n−1` edges for n vertices. Adding an edge between two nonadjacent vertices creates a cycle from the unique path and the new edge.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
path = ['A', 'B', 'C', 'D']
edges = list(zip(path, path[1:]))
print(len(path), len(edges))
print(' -> '.join(path + [path[0]]))
```

```exercise
? How many edges are in a tree on nine vertices?
___
= 8
```

```quiz
? What does adding edge D–A to the path create?
- A new vertex
* A cycle
- A path deletion
> The added edge closes the path from A to D.
```

# @lesson graph-theory-weighted
title: Project: shortest weighted path
summary: The lightest path can use more edges than a direct route.
---
The lightest path can use more edges than a direct route. Dijkstra finalizes the closest tentative vertex and relaxes its outgoing edges when weights are nonnegative. This example finds the distance from A to C.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from heapq import heappop, heappush

graph = {'A': [('B', 2), ('C', 7)], 'B': [('C', 3)], 'C': []}
distances = {'A': 0}
queue = [(0, 'A')]
while queue:
    distance, vertex = heappop(queue)
    if distance != distances[vertex]:
        continue
    for neighbour, weight in graph[vertex]:
        candidate = distance + weight
        if candidate < distances.get(neighbour, float('inf')):
            distances[neighbour] = candidate
            heappush(queue, (candidate, neighbour))
print(distances['C'])
```

```exercise
? What is the weight of the direct route from A to C?
___
= 7
```

```quiz
? Which route has the lowest weight?
- A–C
- B–C
* A–B–C
> A–B–C costs 2+3, less than the direct weight of 7.
```
