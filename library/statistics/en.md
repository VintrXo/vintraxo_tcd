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

# @lesson statistics-reference
title: Statistics and probability reference
summary: Key rules and quick examples.
type: Reference
---
```reference
Mean | Sum divided by count | (4 + 6 + 8) ÷ 3 = 6
Median | Middle value or mean of the two central values after sorting | The median of 2, 6, 10, and 14 is 8
Probability | Favorable outcomes divided by equally likely outcomes | Chance of an even roll on a fair die is 3/6
```
