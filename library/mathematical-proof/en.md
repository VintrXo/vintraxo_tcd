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

# @lesson mathematical-proof-reference
title: Mathematical proof techniques study guide
summary: Review the workshop examples and return to the branch map.
type: Reference
---
- [[mathematical-proof-en/mathematical-proof-direct|Direct proof]]
- [[mathematical-proof-en/mathematical-proof-contrapositive|Contraposition]]
- [[mathematical-proof-en/mathematical-proof-contradiction|Proof by contradiction]]
- [[mathematical-proof-en/mathematical-proof-induction|Mathematical induction]]

Review the [[math-branches-en/math-branches-proof|introductory lesson]] or return to the [[math-branches-en/math-branches-map|branch map]].
