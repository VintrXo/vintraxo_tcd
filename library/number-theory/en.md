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

# @lesson number-theory-reference
title: Number theory study guide
summary: Review the workshop examples and return to the branch map.
type: Reference
---
- [[number-theory-en/number-theory-division|Division and remainders]]
- [[number-theory-en/number-theory-primes|Primes and factorization]]
- [[number-theory-en/number-theory-euclid|Euclid and Bézout’s identity]]
- [[number-theory-en/number-theory-inverse|Congruence and modular inverse]]

Review the [[math-branches-en/math-branches-numbers|introductory lesson]] or return to the [[math-branches-en/math-branches-map|branch map]].
