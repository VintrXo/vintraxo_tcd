# @lesson abstract-algebra-groups
title: Group axioms
summary: A group has a closed associative operation, an identity, and an inverse for every element.
---
A group has a closed associative operation, an identity, and an inverse for every element. The residues `0` to `5` under addition modulo 6 form a group with identity zero. Associativity follows from ordinary addition and is preserved when reducing modulo 6.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
modulus = 6
for value in range(modulus):
    inverse = (-value) % modulus
    print(value, inverse, (value + inverse) % modulus)
```

```exercise
? What is the additive inverse of 1 modulo 6?
___
= 5
```

```quiz
? What is the additive identity in the example?
* 0
- 1
- 5
> Adding zero leaves every element unchanged.
```

# @lesson abstract-algebra-cyclic
title: Cyclic groups and element order
summary: An element's order in an additive group is the smallest positive number of repeated additions returning to zero.
---
An element's order in an additive group is the smallest positive number of repeated additions returning to zero. It generates the whole group if those multiples visit all residues. Modulo 6, 2 generates `{0,2,4}`, while 5 generates the whole group.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from math import gcd

modulus = 6
for value in (0, 2, 5):
    order = modulus // gcd(value, modulus)
    multiples = [(i * value) % modulus for i in range(order)]
    print(value, order, multiples)
```

```exercise
? What is the additive order of 3 modulo 6?
___
= 2
```

```quiz
? Which option generates all residues modulo 6?
- 2
* 5
- 3
> The gcd of 5 and 6 is one, so 5 has order six.
```

# @lesson abstract-algebra-subgroups
title: Subgroups and cosets
summary: A subgroup is a group inside a larger group using the same operation.
---
A subgroup is a group inside a larger group using the same operation. For `H={0,2,4}` under addition modulo 6, a coset `a+H` shifts each element by a. The distinct cosets partition the group into equal-sized parts, here the even and odd residues.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
subgroup = (0, 2, 4)
cosets = {tuple(sorted((a + h) % 6 for h in subgroup)) for a in range(6)}
for coset in sorted(cosets):
    print(coset)
```

```exercise
? How many elements are in each coset in the example?
___
= 3
```

```quiz
? What is the coset 1+H?
- {0, 2, 4}
- {1, 2, 3}
* {1, 3, 5}
> Shifting the even residues in H by one gives the odd residues.
```

# @lesson abstract-algebra-homomorphism
title: Homomorphisms and kernels
summary: An additive homomorphism satisfies `f(a+b)=f(a)+f(b)` using the operations in the respective groups.
---
An additive homomorphism satisfies `f(a+b)=f(a)+f(b)` using the operations in the respective groups. Reducing a residue modulo 6 to its parity preserves addition because 2 divides 6. The kernel consists of inputs mapped to the identity, here `{0,2,4}`.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
def parity(value):
    return value % 2

kernel = [x for x in range(6) if parity(x) == 0]
preserves = all(parity((a + b) % 6) == (parity(a) + parity(b)) % 2
                for a in range(6) for b in range(6))
print(kernel)
print(preserves)
```

```exercise
? How many elements are in the kernel of reduction from modulo 6 to modulo 2?
___
= 3
```

```quiz
? Which element maps to the identity?
* 4
- 1
- 5
> The target identity is zero, and 4 is even.
```

# @lesson abstract-algebra-fields
title: Rings and fields
summary: A ring has addition and multiplication linked by distributivity.
---
A ring has addition and multiplication linked by distributivity. In a field every nonzero element has a multiplicative inverse. Residues modulo a prime form a field. Modulo 6, 2 has no inverse, since its multiples have even remainders.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
for modulus in (5, 6):
    units = [a for a in range(1, modulus)
             if any(a * b % modulus == 1 for b in range(1, modulus))]
    print(modulus, units)
```

```exercise
? What is the multiplicative inverse of 3 modulo 5?
___
= 2
```

```quiz
? Does every nonzero residue modulo 6 have a multiplicative inverse?
- Yes
* No
- Only if we exclude zero
> The nonzero residue 2 cannot be multiplied to obtain 1 modulo 6.
```

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

# @lesson complex-analysis-polar
title: Polar form
summary: A nonzero complex number has polar form `r(cos θ+i sin θ)`, with magnitude r and angle θ defined modulo a full turn.
---
A nonzero complex number has polar form `r(cos θ+i sin θ)`, with magnitude r and angle θ defined modulo a full turn. Multiplication multiplies magnitudes and adds angles, explaining why multiplication by i rotates.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from cmath import phase
from math import degrees

for z in (1 + 1j, (1 + 1j) * 1j):
    print(round(abs(z), 3), round(degrees(phase(z))))
```

```exercise
? What is the angle in degrees of 1+i from the positive real axis?
___
= 45
```

```quiz
? What does multiplying by i do to the magnitude?
* It stays the same
- It doubles
- It becomes zero
> The magnitude of i is one.
```

# @lesson complex-analysis-roots
title: Roots of unity
summary: Solutions of `zⁿ=1` have magnitude one and angles `2πk/n`, for k from zero through n−1.
---
Solutions of `zⁿ=1` have magnitude one and angles `2πk/n`, for k from zero through n−1. They are equally spaced on the unit circle. The fourth roots give four points, two on each axis.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from cmath import rect
from math import tau

count = 4
for k in range(count):
    root = rect(1, tau * k / count)
    print(round(root.real), round(root.imag), abs(root ** count - 1) < 1e-9)
```

```exercise
? How many distinct complex solutions does z⁶=1 have?
___
= 6
```

```quiz
? How many degrees separate adjacent fourth roots of unity?
- 45
* 90
- 180
> Divide a full turn into four equal angles.
```

# @lesson complex-analysis-derivative
title: Complex derivatives and approach directions
summary: A complex derivative requires the same limit of difference quotients from every step direction.
---
A complex derivative requires the same limit of difference quotients from every step direction. For `z²` the quotient simplifies to `2z+h`. For conjugation it is `conj(h)/h`, giving 1 for real steps and −1 for imaginary steps, so no complex derivative exists.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
z = 1 + 2j
for h in (0.01, 0.01j):
    quotient = ((z + h) ** 2 - z ** 2) / h
    print(round(quotient.real, 2), round(quotient.imag, 2))
    print(round((h.conjugate() / h).real))
```

```exercise
? What is the real part of the derivative of z² at z=1+2i?
___
= 2
```

```quiz
? Why does conjugation lack a complex derivative?
- It requires only real inputs
- The function is always zero
* The quotient depends on direction
> Horizontal steps give 1 and vertical steps give −1.
```

# @lesson complex-analysis-cauchy-riemann
title: Cauchy–Riemann equations
summary: Write `f=u+iv`.
---
Write `f=u+iv`. Complex differentiability requires `uₓ=vᵧ` and `uᵧ=−vₓ`. If the partials are continuous near a point and the equations hold there, they suffice for complex differentiability at that point. For `f(z)=z²`, `u=x²−y²` and `v=2xy`.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
x, y = 2, 3
u_x, u_y = 2 * x, -2 * y
v_x, v_y = 2 * y, 2 * x
print(u_x, u_y, v_x, v_y)
print(u_x == v_y, u_y == -v_x)
```

```exercise
? Evaluate uₓ at x=3 for u=x²−y².
___
= 6
```

```quiz
? Which relation must hold between uᵧ and vₓ?
* uᵧ=−vₓ
- uᵧ=vₓ
- uᵧ=vᵧ
> Comparing the two directions gives the minus sign from division by i.
```

# @lesson complex-analysis-contours
title: Project: integrate around a circle
summary: For the counterclockwise unit circle, put `z(t)=exp(it)` from 0 to `2π`.
---
For the counterclockwise unit circle, put `z(t)=exp(it)` from 0 to `2π`. For `1/z`, the integrand becomes `z′(t)/z(t)=i`, so the integral is `2πi`. Compare with integrating `z` along the same path, which gives zero because `z²/2` is an antiderivative.

## Try it yourself

Predict the output, then run the example and change one input.

```try python
from cmath import exp
from math import tau

count = 128
step = tau / count
points = [exp(1j * (i + 0.5) * step) for i in range(count)]
for function in (lambda z: 1 / z, lambda z: z):
    integral = sum(function(z) * (1j * z) * step for z in points)
    print(round(abs(integral), 6))
```

```exercise
? What is the real part of 2πi?
___
= 0
```

```quiz
? What is the integral of z around the circle?
- 2πi
* 0
- 1
> The curve is closed, so the antiderivative has identical values at its endpoints.
```

# @lesson complex-residues-cauchy
title: Cauchy’s theorem and integral formula
summary: For a function holomorphic on and inside a circle, its contour integral is zero.
---
For a function holomorphic on and inside a circle, its contour integral is zero. With `z−a` in the denominator and a inside, Cauchy’s formula gives `∮ f(z)/(z−a) dz = 2πi f(a)`. Compare the two cases for `z²` with a=0.5.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from cmath import exp
from math import tau

count = 128
step = tau / count
points = [exp(1j * index * step) for index in range(count)]
for f in (lambda z: z ** 2, lambda z: z ** 2 / (z - 0.5)):
    integral = sum(f(z) * 1j * z * step for z in points)
    print(round(abs(integral), 3))
```

```exercise
? What is f(a) for f(z)=z² and a=0.5? Enter a decimal.
___
= 0.25
```

```quiz
? What does the denominator z−a introduce when f(a) is nonzero?
* A simple pole at a
- A zero at a
- Only a real constant
> The denominator vanishes linearly at a while the numerator does not vanish.
```

# @lesson complex-residues-laurent
title: Laurent series
summary: On an annulus, a Laurent series permits negative as well as nonnegative powers.
---
On an annulus, a Laurent series permits negative as well as nonnegative powers. For example `1/[z(1−z)] = 1/z + 1 + z + z² + …` for `0<|z|<1`. The region matters because the geometric series in z requires magnitude below one.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
z = 0.5
exact = 1 / (z * (1 - z))
for count in (2, 8):
    partial = 1 / z + sum(z ** k for k in range(count))
    print(round(partial, 4), exact)
```

```exercise
? What is the coefficient of 1/z in the example?
___
= 1
```

```quiz
? Does this expansion converge at z=2?
- Yes
* No
- Only because z is real
> The geometric terms do not tend to zero at z=2.
```

# @lesson complex-residues-residue
title: Project: compute an integral using residues
summary: The residue at a point is the coefficient of `(z−a)⁻¹` in the Laurent expansion.
---
The residue at a point is the coefficient of `(z−a)⁻¹` in the Laurent expansion. A positively oriented contour enclosing poles has integral `2πi` times the sum of enclosed residues. For `1/(z−1)+2/(z−3)`, a radius-two circle about zero encloses only the first pole.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
poles = [(1, 1), (3, 2)]
for radius in (2, 4):
    total = sum(residue for location, residue in poles if abs(location) < radius)
    print(radius, total)  # coefficient of 2πi
```

```exercise
? What is the coefficient of 2πi for radius four?
___
= 3
```

```quiz
? Which pole is excluded by the radius-two circle?
- z=1
- Both
* z=3
> The point 3 is farther from zero than the radius.
```

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

# @lesson integration-spaces-convergence
title: Monotone and dominated convergence
summary: For nonnegative measurable functions increasing pointwise, monotone convergence lets us exchange limit and integral.
---
For nonnegative measurable functions increasing pointwise, monotone convergence lets us exchange limit and integral. Dominated convergence permits that for almost-everywhere convergence when one integrable function bounds all absolute values. On `[0,1]`, `xⁿ` is bounded by one and converges to zero except at endpoint one.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from fractions import Fraction

for n in (1, 4, 9):
    print(n, Fraction(1, n + 1))  # exact integral of x**n on [0, 1]
```

```exercise
? What is the integral of x⁴ over [0,1]? Enter a fraction like 1/2.
___
= 1/5
```

```quiz
? Which integrable function dominates every xⁿ here?
* 1
- x² for every n
- Zero
> On [0,1], every power lies between zero and one, whose integral is finite.
```

# @lesson integration-spaces-banach
title: Completeness and Banach spaces
summary: A Banach space is a complete normed space: each Cauchy sequence has a limit in the space.
---
A Banach space is a complete normed space: each Cauchy sequence has a limit in the space. Continuous functions on a closed interval with the uniform norm are an example. Polynomials in that norm can converge uniformly to a non-polynomial, as the partial sums for exp(x) do on `[0,1]`.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from math import exp, factorial

for degree in (1, 3, 6):
    value_at_one = sum(1 / factorial(k) for k in range(degree + 1))
    print(degree, round(exp(1) - value_at_one, 6))
```

```exercise
? What is the degree-one partial sum at x=1?
___
= 2
```

```quiz
? What does a Banach space require in addition to a norm?
- Finite dimension
* Completeness
- Only numerical elements
> Every Cauchy sequence converges to an element inside the space.
```

# @lesson integration-spaces-hilbert
title: Project: projection in L²
summary: A Hilbert space is complete in the norm induced by an inner product.
---
A Hilbert space is complete in the norm induced by an inner product. In real `L²` on `[0,1]`, the inner product integrates a product, and functions equal almost everywhere are one element. Project x onto the constants by taking its mean, 1/2; the residual then has integral zero.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from fractions import Fraction

count = 16
samples = [Fraction(2 * i + 1, 2 * count) for i in range(count)]
projection = sum(samples) / count
print(projection)
print(sum(x - projection for x in samples) / count)
```

```exercise
? What is the constant projection of 2x on [0,1]?
___
= 1
```

```quiz
? What is the residual’s inner product with constant function 1 after projection?
- 1/2
- 1
* 0
> Orthogonal projection leaves a residual perpendicular to the constants.
```

# @lesson advanced-math-functional
title: Functional analysis
summary: Functional analysis studies spaces whose vectors can be functions.
---
Functional analysis studies spaces whose vectors can be functions. The supremum norm of a continuous function on a closed interval is the largest `|f(x)|`. The corresponding distance between two functions is the norm of their difference. Here `f(x)=x` and `g(x)=x²` on `[0, 1]`, and their gap peaks at one half.

Review the prerequisite idea in [[math-linear-algebra-en/linear-algebra-vectors|Vectors and components]].

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

# @lesson functional-analysis-norm
title: Norms and distance
summary: A norm measures vector size, and distance is the norm of the difference.
---
A norm measures vector size, and distance is the norm of the difference. The sum norm adds absolute components; the maximum norm takes the largest. On samples of two functions, the largest gap approximates their uniform distance.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
values = [-2, 3, -1]
print(sum(abs(v) for v in values), max(abs(v) for v in values))
```

```exercise
? What is the maximum norm of (−4, 1, 2)?
___
= 4
```

```quiz
? What is its sum norm?
* 7
- 4
- −1
> Add the absolute components 4, 1, and 2.
```

# @lesson functional-analysis-operator
title: Linear and bounded operators
summary: A linear operator preserves sums and scalar multiplication.
---
A linear operator preserves sums and scalar multiplication. For example, `T(f)=2f` doubles every value. It is bounded in the uniform norm because the output norm is twice the input norm. The bound 2 is attained for any nonzero function.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
samples = [-2, 1, 3]
output = [2 * x for x in samples]
print(max(map(abs, samples)), max(map(abs, output)))
```

```exercise
? If the input norm is 5, what is the norm of T(f)=2f?
___
= 10
```

```quiz
? Which property is part of linearity?
- Adds a constant to every input
* Preserves addition
- Maps every input to 1
> Linearity gives T(f+g)=T(f)+T(g).
```

# @lesson functional-analysis-contraction
title: Project: iteration and fixed points
summary: The map `T(x)=1+x/2` halves distances.
---
The map `T(x)=1+x/2` halves distances. Its fixed point satisfies `T(x)=x` and is 2. Try different starting values and watch the error shrink. The contraction principle generalizes this idea on a complete metric space.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
value = 0.0
for _ in range(3):
    value = 1 + value / 2
    print(value, abs(2 - value))
```

```exercise
? What is the fixed point of T(x)=3+x/2?
___
= 6
```

```quiz
? What is the error contraction factor in the example?
- 2
- 1
* 1/2
> The difference T(x)−T(2) is (x−2)/2.
```

# @lesson advanced-math-categories
title: Category theory
summary: Category theory studies objects, arrows, and composition.
---
Category theory studies objects, arrows, and composition. A familiar example has sets as objects and functions as arrows, with an identity function on each set. Composition is associative: for compatible types, `h ∘ (g ∘ f)` equals `(h ∘ g) ∘ f`; both apply f, then g, then h.

Review the prerequisite idea in [[math-functions-trig-en/functions-rule|Function inputs and outputs]].

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

# @lesson category-theory-composition
title: Objects, arrows, and composition
summary: In the category of sets, an arrow is a function between sets.
---
In the category of sets, an arrow is a function between sets. Compose `g∘f` when the target of f is the source of g, applying f first. The identity fixes every element. Composition in any category is associative.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
def f(x):
    return x + 1

def g(x):
    return 2 * x

print(g(f(3)), f(g(3)))
```

```exercise
? What is g(f(4)) in the example?
___
= 10
```

```quiz
? In g∘f, which function is applied first?
* f
- g
- The identity
> The output of f becomes the input to g.
```

# @lesson category-theory-isomorphism
title: Isomorphisms and inverse arrows
summary: An isomorphism has a two-sided inverse whose two compositions give the appropriate identity arrows.
---
An isomorphism has a two-sided inverse whose two compositions give the appropriate identity arrows. In sets, a bijection is an isomorphism. A map sending two elements to one output cannot be inverted to recover both inputs.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
forward = {'a': 1, 'b': 2}
backward = {value: key for key, value in forward.items()}
print(backward[forward['b']])
print(forward[backward[1]])
```

```exercise
? If f(a)=1 and f(b)=2, what does the inverse return at 2? Enter a or b.
___
= b
```

```quiz
? What does composing an arrow and its inverse yield?
- An arbitrary new arrow
* The identity arrow
- Always a constant arrow
> The two compositions giving identities are part of the definition.
```

# @lesson category-theory-functor
title: Project: a functor preserves composition
summary: A functor maps objects and arrows while preserving identities and composition.
---
A functor maps objects and arrows while preserving identities and composition. The covariant power-set functor sends a set to its subsets and a function to its direct-image map. The direct image under `g∘f` equals the image under f followed by the image under g.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
def image(function, subset):
    return {function(value) for value in subset}

subset = {1, 2}
f = lambda x: x + 1
g = lambda x: 2 * x
separate = image(g, image(f, subset))
composed = image(lambda x: g(f(x)), subset)
print(sorted(separate), separate == composed)
```

```exercise
? How many elements are in the image of {1,2} under x ↦ 2x?
___
= 2
```

```quiz
? Which properties does a functor preserve?
- Always numerical order
- Every set size
* Identities and composition
> A functor maps an identity to an identity and a composite to the corresponding composite.
```
