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

# @lesson stochastic-processes-reference
title: Stochastic processes study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[stochastic-processes-en/stochastic-processes-transition|Transition matrices]]
- [[stochastic-processes-en/stochastic-processes-stationary|Stationary distributions]]
- [[stochastic-processes-en/stochastic-processes-walk|Project: calculate a random walk distribution]]

Review [[math-branches-en/math-branches-stochastic|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
