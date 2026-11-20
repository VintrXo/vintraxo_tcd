# @lesson information-theory-entropy
title: Entropy and information
summary: An event of probability p carries `−log₂(p)` bits of information.
---
An event of probability p carries `−log₂(p)` bits of information. Entropy is the probability-weighted average. Zero-probability terms contribute zero.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import log2

for probabilities in ([0.5, 0.5], [0.75, 0.25]):
    print(round(-sum(p * log2(p) for p in probabilities if p), 4))
```

```exercise
? How many bits of information does a probability-1/4 outcome carry?
___
= 2
```

```quiz
? Which coin has higher entropy here?
* Fair
- Biased
- Neither, they tie
> Equal probabilities maximize uncertainty here.
```

# @lesson information-theory-conditional
title: Conditional entropy
summary: Conditional entropy `H(Y|X)` averages the remaining entropy of Y after each possible X is known.
---
Conditional entropy `H(Y|X)` averages the remaining entropy of Y after each possible X is known. If X determines Y, none remains. The difference `H(Y)−H(Y|X)` is mutual information.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
h_y = 1.0
conditional_entropy = {0: 0.0, 1: 0.0}
h_given_x = sum(0.5 * entropy for entropy in conditional_entropy.values())
print(h_given_x, h_y - h_given_x)
```

```exercise
? If Y equals X, what is H(Y|X)?
___
= 0
```

```quiz
? If X and Y are independent and H(Y)=1, what is H(Y|X)?
- 0
* 1
- 2
> Under independence, knowing X leaves Y’s distribution unchanged.
```

# @lesson information-theory-prefix
title: Project: compare two codes
summary: In a prefix-free code, no codeword begins with another full codeword, so the stream can be split unambiguously.
---
In a prefix-free code, no codeword begins with another full codeword, so the stream can be split unambiguously. Compare two fixed bits per symbol with `0,10,11`, which assigns the shortest word to the most frequent symbol.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from fractions import Fraction

probabilities = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
for codes in (['00', '01', '10'], ['0', '10', '11']):
    print(sum(p * len(code) for p, code in zip(probabilities, codes, strict=True)))
```

```exercise
? What average length does the variable code give? Enter a fraction like 1/2.
___
= 3/2
```

```quiz
? Can 0 and 01 coexist in a prefix-free code?
- Yes
- Only if 01 has even length
* No
> The word 0 is a prefix of 01.
```

# @lesson information-theory-reference
title: Information theory study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[information-theory-en/information-theory-entropy|Entropy and information]]
- [[information-theory-en/information-theory-conditional|Conditional entropy]]
- [[information-theory-en/information-theory-prefix|Project: compare two codes]]

Review [[math-branches-en/math-branches-information|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
