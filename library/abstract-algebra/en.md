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

# @lesson abstract-algebra-reference
title: Abstract algebra study guide
summary: Review the examples and connect them with other courses.
type: Reference
---
## Worked examples

- [[abstract-algebra-en/abstract-algebra-groups|Group axioms]]
- [[abstract-algebra-en/abstract-algebra-cyclic|Cyclic groups and element order]]
- [[abstract-algebra-en/abstract-algebra-subgroups|Subgroups and cosets]]
- [[abstract-algebra-en/abstract-algebra-homomorphism|Homomorphisms and kernels]]
- [[abstract-algebra-en/abstract-algebra-fields|Rings and fields]]

## Related lessons

- [[number-theory-en/number-theory-inverse|Modular inverses]]
- [[math-branches-en/math-branches-abstract|Abstract algebra overview]]
