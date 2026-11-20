# @lesson applied-statistics-bayes
title: Conditional probability and Bayes
summary: Conditioning changes the group in the denominator.
---
Conditioning changes the group in the denominator. Of 100 orders, 20 are from branch A. Six orders from A and four others were late. Thus `P(late | A)` is `6/20`, and `P(A | late)` is `6/10`. Bayes reconstructs the second probability by multiplying the first by `P(A)` and dividing by `P(late)`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from fractions import Fraction

p_a = Fraction(20, 100)
p_late_given_a = Fraction(6, 20)
p_late = Fraction(10, 100)
print(p_late_given_a)
print(p_late_given_a * p_a / p_late)
```

```exercise
? Write P(A | late) as a decimal like 0.25.
___
= 0.6
```

```quiz
? Which count goes in the denominator of P(late | A)?
* 20
- 10
- 100
> The condition restricts the group to orders from branch A.
```

# @lesson applied-statistics-binomial
title: The binomial distribution
summary: For n independent trials with the same success probability p, the number of successes is binomial.
---
For n independent trials with the same success probability p, the number of successes is binomial. Exactly k successes has probability `comb(n,k) × p^k × (1−p)^(n−k)`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import comb

n, p = 3, 0.5
for k in range(n + 1):
    print(k, comb(n, k) * p ** k * (1 - p) ** (n - k))
```

```exercise
? How many arrangements have two successes in three trials?
___
= 3
```

```quiz
? What is the chance of three successes in three independent trials with p = 0.5?
- 0.375
* 0.125
- 0.5
> Multiply 0.5 by itself three times.
```

# @lesson applied-statistics-confidence
title: Confidence intervals
summary: For a large independent sample, an approximate 95% Wald interval for a proportion is the observed proportion ± `1.96 × SE`.
---
For a large independent sample, an approximate 95% Wald interval for a proportion is the observed proportion ± `1.96 × SE`. Under suitable conditions, about 95% of repeated intervals cover the true proportion. The approximation can work poorly with small samples or extreme proportions.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import sqrt

successes, n = 60, 100
observed = successes / n
margin = 1.96 * sqrt(observed * (1 - observed) / n)
print(round(observed - margin, 3), round(observed + margin, 3))
```

```exercise
? Find the standard error at p = 0.5 and n = 100. Enter a decimal.
___
= 0.05
```

```quiz
? Keeping the proportion fixed, what happens to the margin when the sample size quadruples?
- It doubles
- It stays the same
* It halves
> The margin is inversely proportional to the square root of sample size.
```

# @lesson applied-statistics-test
title: Hypothesis tests
summary: Assume a coin has heads probability 0.5 and test the alternative that it is higher.
---
Assume a coin has heads probability 0.5 and test the alternative that it is higher. After seven heads in eight tosses, the one-sided p-value is the chance of at least seven heads under the null. Compare it with the prespecified significance level.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from fractions import Fraction
from math import comb

n = 8
observed = 7
p_value = Fraction(sum(comb(n, k) for k in range(observed, n + 1)), 2 ** n)
print(p_value)
print(p_value < Fraction(5, 100))
```

```exercise
? How many of the 256 toss sequences count towards the tail? Enter the numerator.
___
= 9
```

```quiz
? Which outcomes belong to the tail in this example?
* 7 or 8 heads
- Exactly 7 heads
- Zero or one head
> The alternative is greater, so count outcomes at least as large as observed.
```

# @lesson applied-statistics-regression
title: Simple linear regression
summary: A least-squares line chooses slope and intercept to minimize squared prediction errors.
---
A least-squares line chooses slope and intercept to minimize squared prediction errors. Its slope describes the change in prediction per unit of input. Association alone does not establish causation, and extrapolation needs care.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from statistics import linear_regression

visits = [1, 2, 3, 4]
orders = [2, 3, 4, 5]
slope, intercept = linear_regression(visits, orders)
print(slope, intercept)
print(slope * 2.5 + intercept)
```

```exercise
? For prediction line y = 2x + 1, what is the estimate at x = 3?
___
= 7
```

```quiz
? What does a least-squares line minimize?
- Sum of observations
* Sum of squared errors
- Largest input
> Square every observed-minus-predicted difference, then add them.
```

# @lesson applied-statistics-project
title: Project: compare branch delay rates
summary: Each row records a branch, the number of orders, and the number of delays.
---
Each row records a branch, the number of orders, and the number of delays. Sum counts by branch before calculating rates so every order has equal weight. Report group sizes alongside rates because percentages can hide sample size differences.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
import pandas as pd

rows = [('A', 12, 2), ('A', 8, 2), ('B', 20, 1), ('B', 10, 2)]
orders = pd.DataFrame(rows, columns=['branch', 'count', 'late'])
by_branch = orders.groupby('branch')[['count', 'late']].sum()
for branch, row in by_branch.iterrows():
    print(branch, row['count'], f"{row['late'] / row['count']:.0%}")
```

```exercise
? How many delayed orders does branch B have?
___
= 3
```

```quiz
? Why divide total delays by total orders per branch?
- To ignore the number of orders
- To guarantee equal branch rates
* So every order has equal weight
> A direct average of row percentages can overweight individual orders in smaller rows.
```

# @lesson applied-statistics-reference
title: Applied probability and statistics study guide
summary: Revisit the worked examples and follow the connected courses.
type: Reference
---
## Worked examples

- [[applied-statistics-en/applied-statistics-bayes|Conditional probability and Bayes]]
- [[applied-statistics-en/applied-statistics-binomial|The binomial distribution]]
- [[applied-statistics-en/applied-statistics-confidence|Confidence intervals]]
- [[applied-statistics-en/applied-statistics-test|Hypothesis tests]]
- [[applied-statistics-en/applied-statistics-regression|Simple linear regression]]
- [[applied-statistics-en/applied-statistics-project|Project: compare branch delay rates]]

## Related courses

- [[statistics-en/statistics-chance|Probability of an event]]
- [[pandas-en/pd-project|Sales report in Pandas]]
