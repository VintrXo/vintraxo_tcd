# @lesson statistics-mean
title: Arithmetic mean
summary: The mean shares the total equally among the observations.
---
The mean shares the total equally among the observations. The mean of 8, 10, and 12 is 10. An unusually large value can raise the mean even when most values stay unchanged.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
values = [8, 10, 12]
print(sum(values) / len(values))
values.append(30)
print(sum(values) / len(values))
```

```exercise
? Find the mean of 4, 6, and 8.
___
= 6
```

```quiz
? Find the mean of 5, 5, and 20.
- 5
* 10
- 15
> The total is 30 and there are 3 observations.
```

# @lesson statistics-median
title: Median and mode
summary: Sort the observations to find the median.
---
Sort the observations to find the median. For an even number of observations, average the two middle values. A mode is a value with the highest frequency, and several values can tie.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
from statistics import median, multimode

values = [12, 8, 8, 20]
print(median(values))
print(multimode(values))
```

```exercise
? Find the median of 12, 4, and 8.
___
= 8
```

```quiz
? Find the median of 2, 6, 10, and 14.
- 6
- 10
* 8
> The middle values are 6 and 10, and their average is 8.
```

# @lesson statistics-spread
title: Range and outliers
summary: The range is the maximum minus the minimum.
---
The range is the maximum minus the minimum. It is a quick measure of spread and depends on the extremes. Compare how adding 100 changes the range and the median.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
from statistics import median

values = [5, 6, 7]
for sample in (values, values + [100]):
    print(max(sample) - min(sample), median(sample))
```

```exercise
? Find the range of 3, 7, and 11.
___
= 8
```

```quiz
? Which typically changes less when an extremely large value is added: the median or range?
* Median
- Range
- They always change by the same amount
> Range directly uses the maximum. The median uses the middle observations.
```

# @lesson statistics-frequency
title: Frequency and relative frequency
summary: Frequency counts how often a category occurs.
---
Frequency counts how often a category occurs. Relative frequency divides that count by the total. If one branch has 3 of 8 orders, its share is `3/8 = 37.5%`.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
from collections import Counter

branches = ['A', 'A', 'B', 'A', 'B']
for branch, count in Counter(branches).items():
    print(branch, count, f'{count / len(branches):.0%}')
```

```exercise
? A choice appears 4 times out of 20. Enter its share with a percent sign.
___
= 20%
```

```quiz
? What do relative frequencies add up to when categories partition the data?
- 50%
* 100%
- The number of categories
> Every observation is counted in exactly one category, so the combined numerator equals the denominator.
```

# @lesson statistics-chance
title: Probability of an event
summary: When outcomes are equally likely, divide the number of favorable outcomes by the total.
---
When outcomes are equally likely, divide the number of favorable outcomes by the total. For a fair die, the chance of an even roll is `3/6`. The complement has probability one minus the event probability.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
from fractions import Fraction

outcomes = range(1, 7)
favorable = [n for n in outcomes if n % 2 == 0]
print(Fraction(len(favorable), len(outcomes)))
```

```exercise
? Write the probability of rolling 6 on a fair die as a fraction like 1/2.
___
= 1/6
```

```quiz
? What is the probability of rolling more than 4 on a fair die?
- 1/2
- 2/3
* 1/3
> The favorable outcomes are 5 and 6 out of 6, so 2/6 = 1/3.
```

# @lesson statistics-independence
title: Independent events and simulation
summary: With two independent fair coin tosses, the chance of heads on the second is still `1/2` regardless of the first.
---
With two independent fair coin tosses, the chance of heads on the second is still `1/2` regardless of the first. The probability of two heads is `1/2 × 1/2`. Repeated simulation yields an estimate that may differ from the theoretical result.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
from random import Random

rng = Random(7)
trials = 1000
hits = sum(rng.choice('HT') + rng.choice('HT') == 'HH' for _ in range(trials))
print(round(hits / trials, 3))
```

```exercise
? Enter the probability of two consecutive heads as a fraction like 1/2.
___
= 1/4
```

```quiz
? What is the chance of rolling two sixes in two independent rolls of a fair die?
* 1/36
- 1/12
- 1/6
> Multiply the chances for the two rolls: 1/6 × 1/6.
```

# @lesson statistics-report
title: Project: summarize sales data
summary: You have five order values for a day.
---
You have five order values for a day. Compute the mean, median, range, and share of orders worth at least 30. Then explain in one sentence why the median better describes a typical order in this example.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
from statistics import mean, median

orders = [18, 20, 22, 24, 116]
print(mean(orders), median(orders))
print(max(orders) - min(orders))
print(f'{sum(amount >= 30 for amount in orders) / len(orders):.0%}')
```

```exercise
? How many orders in the sample are worth at least 30?
___
= 1
```

```quiz
? Which result best describes a typical order in this sample?
- Mean of 40
* Median of 22
- Range of 98
> The order worth 116 pulls the mean up. A median of 22 sits in the middle of these observations.
```

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

# @lesson statistical-models-normal
title: The normal distribution
summary: A normal distribution is symmetric about its mean.
---
A normal distribution is symmetric about its mean. Use `z=(x−μ)/σ` to express distance from the mean in standard deviations. The example computes the probability within one standard deviation.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from statistics import NormalDist

normal = NormalDist(100, 15)
print((130 - 100) / 15)
print(round(normal.cdf(115) - normal.cdf(85), 4))
```

```exercise
? What is the z-score of 115 in the example?
___
= 1
```

```quiz
? Where does half the probability lie in a normal distribution?
* Below the mean
- Above two standard deviations
- At the mean alone
> Symmetry divides the area in half; a single point has probability zero.
```

# @lesson statistical-models-poisson
title: The Poisson distribution
summary: Poisson models event counts in an interval, such as independent arrivals at a constant rate.
---
Poisson models event counts in an interval, such as independent arrivals at a constant rate. With mean count λ, exactly k events has probability `exp(−λ) × λ^k/k!`. Multiply the rate by the interval length to find λ.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from math import exp, factorial

average = 2
for count in (0, 1, 2):
    print(count, round(exp(-average) * average ** count / factorial(count), 4))
```

```exercise
? At three orders per hour, what is the mean count over two hours?
___
= 6
```

```quiz
? Which expression is the probability of zero events when λ=2?
- 2×exp(−2)
* exp(−2)
- 1
> The zeroth power and zero factorial both equal one.
```

# @lesson statistical-models-sampling
title: Law of large numbers and central limit theorem
summary: For independent identically distributed observations, the sample mean approaches the population mean in probability under the law’s conditions.
---
For independent identically distributed observations, the sample mean approaches the population mean in probability under the law’s conditions. With finite nonzero variance, standardized sample means approach a normal distribution. This example compares the spread of coin-toss means at two sample sizes.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
from random import Random
from statistics import mean, pstdev

random = Random(12)
spreads = []
for size in (10, 100):
    averages = [mean(random.randrange(2) for _ in range(size)) for _ in range(500)]
    spreads.append(pstdev(averages))
print(spreads[1] < spreads[0])
```

```exercise
? What is the population mean of a fair coin coded zero and one? Enter a decimal.
___
= 0.5
```

```quiz
? What approaches a normal distribution under the central limit theorem here?
- The individual toss outcomes
- Each sample mean by itself
* The distribution of standardized sample means
> Tosses are still zero or one; the limit describes the distribution of their averages.
```

# @lesson statistical-models-regression
title: Project: multiple regression
summary: Use a column per feature and a column of ones for the intercept.
---
Use a column per feature and a column of ones for the intercept. In these synthetic data, sales rise by two per extra visit and three per extra promotion, holding the other feature fixed. With real data, such coefficients describe conditional associations and may not be causal.

## Try it yourself

Predict the result, then run the example and change an input.

```try python
import numpy as np

features = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
sales = np.array([5, 7, 8, 10])
design = np.column_stack((np.ones(len(features)), features))
coefficients = np.linalg.lstsq(design, sales, rcond=None)[0]
print(np.round(coefficients, 3).tolist())
```

```exercise
? What is predicted for two visits and one promotion?
___
= 12
```

```quiz
? What does the promotions coefficient describe here?
* Change in prediction with more promotions at fixed visits
- The sample’s visit count
- The predicted value at zero inputs
> Five is the intercept; three is the prediction change per extra promotion.
```

# @lesson stochastic-processes-transition
title: Transition matrices
summary: A discrete-time Markov chain uses transition probabilities from each current state to the next.
---
A discrete-time Markov chain uses transition probabilities from each current state to the next. Put initial states in rows, each summing to one. Multiplying today’s row distribution by the matrix gives tomorrow’s distribution.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
matrix = [[0.8, 0.2], [0.4, 0.6]]
distribution = [0.5, 0.5]
next_day = [sum(distribution[i] * matrix[i][j] for i in range(2)) for j in range(2)]
print([round(p, 2) for p in next_day])
```

```exercise
? What is the probability of moving from the first state to the second? Enter a decimal.
___
= 0.2
```

```quiz
? What is the sum of each row?
* 1
- 0.5
- 2
> Each row distributes all probability over the possible next states.
```

# @lesson stochastic-processes-stationary
title: Stationary distributions
summary: A distribution π is stationary when `πP=π`.
---
A distribution π is stationary when `πP=π`. With probability 0.2 of entering state two from state one and 0.4 of leaving it, stationary mass p solves `p=0.2(1−p)+0.6p`, giving `p=1/3`. Stationarity describes the distribution; individual states can still change.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from fractions import Fraction

enter, leave = Fraction(1, 5), Fraction(2, 5)
p = enter / (enter + leave)
print(p, (1 - p) * enter + p * (1 - leave))
```

```exercise
? If entry and exit probabilities are equal and positive, what is stationary mass in state two? Use a fraction like 1/3.
___
= 1/2
```

```quiz
? What happens to a stationary distribution after one transition?
- It becomes a single state
* It stays the same
- It doubles
> By definition the transition returns the same distribution.
```

# @lesson stochastic-processes-walk
title: Project: calculate a random walk distribution
summary: Start at zero and take independent equally likely ±1 steps.
---
Start at zero and take independent equally likely ±1 steps. Store each site's probability, then move half of it to each neighbour. After three steps only odd positions are possible because every step flips parity.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from collections import defaultdict
from fractions import Fraction

distribution = {0: Fraction(1)}
for _ in range(3):
    next_step = defaultdict(Fraction)
    for position, probability in distribution.items():
        next_step[position - 1] += probability / 2
        next_step[position + 1] += probability / 2
    distribution = next_step
print([(position, str(probability)) for position, probability in sorted(distribution.items())])
```

```exercise
? What is the probability of position 3 after three steps? Use a fraction like 1/2.
___
= 1/8
```

```quiz
? Which location cannot be reached after three steps?
- 1
- −3
* 0
> Parity flips at each step, so the position is odd after three moves.
```
