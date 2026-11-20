# @lesson advanced-math-measure
title: Measure theory
summary: A measure generalizes length.
---
A measure generalizes length. The interval `[a, b)` has length `b − a`. For disjoint intervals, add their lengths to measure the union. A simple function takes finitely many values, and its integral adds each value times the measure of the region where it occurs.

Review the prerequisite idea in [[math-branches-en/math-branches-analysis|Real analysis]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
pieces = [(0, 2, 3), (2, 5, 4)]
length = sum(right - left for left, right, _ in pieces)
integral = sum((right - left) * value for left, right, value in pieces)
print(length, integral)
```

```exercise
? What is the length of [0, 2) union [4, 7)?
___
= 5
```

```quiz
? A function is 3 on [0, 2) and 4 on [2, 5). What is its integral over [0, 5)?
* 18
- 12
- 20
> Compute 3 × 2 + 4 × 3.
```

# @lesson advanced-math-functional
title: Functional analysis
summary: Functional analysis studies spaces whose vectors can be functions.
---
Functional analysis studies spaces whose vectors can be functions. The supremum norm of a continuous function on a closed interval is the largest `|f(x)|`. The corresponding distance between two functions is the norm of their difference. Here `f(x)=x` and `g(x)=x²` on `[0, 1]`, and their gap peaks at one half.

Review the prerequisite idea in [[linear-algebra-en/linear-algebra-vectors|Vectors and components]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
points = [i / 100 for i in range(101)]
gaps = [(abs(x - x ** 2), x) for x in points]
gap, location = max(gaps)
print(location, gap)
```

```exercise
? What is the supremum norm of the constant function −3? Enter the positive magnitude.
___
= 3
```

```quiz
? What does this distance between two functions measure?
- Average gap
* Largest absolute gap
- Smallest absolute gap
> Take the largest absolute gap on the interval. Here `x − x² = 1/4 − (x − 1/2)²`.
```

# @lesson advanced-math-curvature
title: Differential geometry
summary: Differential geometry studies shapes using calculus.
---
Differential geometry studies shapes using calculus. Curvature measures how quickly the tangent direction changes per unit of arc length. For a circle of radius `r`, curvature is the constant `1/r`: the tangent makes one full turn over a distance `2πr`.

Review the prerequisite idea in [[calculus-en/calculus-rate|Instantaneous rate]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
from math import pi

for radius in (1, 2, 4):
    turn = 2 * pi
    length = 2 * pi * radius
    print(radius, round(turn / length, 2))
```

```exercise
? What is the curvature of a circle of radius 5? Enter a decimal.
___
= 0.2
```

```quiz
? What happens to curvature if the radius doubles?
- It doubles
- It stays the same
* It halves
> Curvature is the reciprocal of the radius.
```

# @lesson advanced-math-heat
title: Partial differential equations
summary: Temperature along a rod depends on position and time.
---
Temperature along a rod depends on position and time. The 1D heat equation relates change over time to the second spatial derivative. On a grid, approximate it by comparing each point with its two neighbours. This example adds one quarter of the second difference per step and fixes both ends at zero.

Review the prerequisite idea in [[math-branches-en/math-branches-differential|Differential equations]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
current = [0, 0, 100, 0, 0]
for _ in range(2):
    updated = current.copy()
    for i in range(1, len(current) - 1):
        difference = current[i - 1] - 2 * current[i] + current[i + 1]
        updated[i] = current[i] + 0.25 * difference
    current = updated
    print(current)
```

```exercise
? In the example, what is the centre value after the first step?
___
= 50
```

```quiz
? Why compute the next step from the old list?
* All points update from the same state
- To ignore neighbours
- To change the boundary values
> Using an already updated value for a neighbour would mix two time levels.
```

# @lesson advanced-math-physics
title: Mathematical physics
summary: In an ideal mass–spring model, the force is `−kx` and friction is absent.
---
In an ideal mass–spring model, the force is `−kx` and friction is absent. Total energy is kinetic energy `mv²/2` plus spring potential energy `kx²/2`. Speed is zero at maximum displacement, while at equilibrium all the energy is kinetic.

Review the prerequisite idea in [[math-branches-en/math-branches-differential|Differential equations]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
from math import sqrt

mass = 1
stiffness = 4
amplitude = 0.5
energy = stiffness * amplitude ** 2 / 2
speed_at_equilibrium = sqrt(2 * energy / mass)
print(energy, speed_at_equilibrium)
```

```exercise
? What is the spring energy at k = 4 and x = 1?
___
= 2
```

```quiz
? What happens to total energy in this model?
- It is zero at equilibrium
* It stays constant
- It doubles every cycle
> With no friction, energy transfers between kinetic and potential forms.
```

# @lesson advanced-math-combinatorics
title: Advanced combinatorics
summary: Inclusion–exclusion corrects repeated counting.
---
Inclusion–exclusion corrects repeated counting. For three sets, add their sizes, subtract the sizes of the pairwise intersections, then add the size of the triple intersection. An object in all three sets then contributes exactly once.

Review the prerequisite idea in [[discrete-math-en/discrete-math-combinations|Permutations and combinations]].

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

# @lesson advanced-math-categories
title: Category theory
summary: Category theory studies objects, arrows, and composition.
---
Category theory studies objects, arrows, and composition. A familiar example has sets as objects and functions as arrows, with an identity function on each set. Composition is associative: for compatible types, `h ∘ (g ∘ f)` equals `(h ∘ g) ∘ f`; both apply f, then g, then h.

Review the prerequisite idea in [[functions-en/functions-rule|Function inputs and outputs]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
def compose(g, f):
    return lambda x: g(f(x))

def f(x):
    return x + 1

def g(x):
    return 2 * x

def h(x):
    return x - 3

left = compose(h, compose(g, f))
right = compose(compose(h, g), f)
print(left(4), right(4))
```

```exercise
? If f(x) = x + 1 and g(x) = 2x, what is (g ∘ f)(3)?
___
= 8
```

```quiz
? Which function is the identity on the integers?
* x ↦ x
- x ↦ x + 1
- x ↦ 0
> The identity returns each input unchanged.
```

# @lesson advanced-math-reference
title: Guide to advanced topics
summary: Review the key idea and revisit each worked example.
type: Reference
---
Each lesson illustrates a starting idea. Use the prerequisite link in each lesson to build the mathematics behind its example.

- [[advanced-math-en/advanced-math-measure|Measure theory]]
- [[advanced-math-en/advanced-math-functional|Functional analysis]]
- [[advanced-math-en/advanced-math-curvature|Differential geometry]]
- [[advanced-math-en/advanced-math-heat|Partial differential equations]]
- [[advanced-math-en/advanced-math-physics|Mathematical physics]]
- [[advanced-math-en/advanced-math-combinatorics|Advanced combinatorics]]
- [[advanced-math-en/advanced-math-categories|Category theory]]

Return to the full [[math-branches-en/math-branches-map|map of mathematical branches]].
