# @lesson game-theory-responses
title: Best responses and Nash equilibrium
summary: A best response maximizes a player’s payoff given the other choice.
---
A best response maximizes a player’s payoff given the other choice. At a Nash equilibrium, each player is best responding to the other. Here check each cell for an equilibrium in pure strategies.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
payoffs = [[(2, 2), (0, 0)], [(0, 0), (1, 1)]]
for i, row in enumerate(payoffs):
    for j, (p, q) in enumerate(row):
        if p == max(r[j][0] for r in payoffs) and q == max(cell[1] for cell in row):
            print(i, j)
```

```exercise
? How many pure equilibria are in the example?
___
= 2
```

```quiz
? When is a cell a Nash equilibrium?
* When both players best respond to each other
- Whenever payoffs are equal
- Whenever both payoffs are zero
> No player can improve by changing alone.
```

# @lesson game-theory-mixed
title: Mixed strategies
summary: A mixed strategy is a probability distribution over actions.
---
A mixed strategy is a probability distribution over actions. In matching pennies, the row player wins one for a match and loses one otherwise. If the opponent picks heads with probability p, heads yields expected payoff `2p−1`, and tails yields `1−2p`.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
for probability in (0.25, 0.5, 0.75):
    print(probability, 2 * probability - 1, 1 - 2 * probability)
```

```exercise
? At what p are the two payoffs equal? Enter a decimal.
___
= 0.5
```

```quiz
? At p=0.75, which action gives the row player a higher payoff?
- Tails
* Heads
- They tie
> Heads yields 0.5, tails −0.5.
```

# @lesson game-theory-minimax
title: Project: compare worst-case payoffs
summary: In a zero-sum game the payoffs sum to zero.
---
In a zero-sum game the payoffs sum to zero. In the row payoff matrix, find each row’s worst payoff and choose the row with the largest minimum. This is the best guarantee among pure rows; mixing can improve it.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
payoffs = [[4, -2], [1, 0]]
guarantees = [min(row) for row in payoffs]
print(guarantees)
print(max(guarantees))
```

```exercise
? What is the first row’s worst payoff?
___
= -2
```

```quiz
? Which row guarantees the higher minimum?
- First
- Equal guarantee
* Second
> The second row’s minimum is zero, compared with −2 for the first.
```

# @lesson game-theory-reference
title: Game theory study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[game-theory-en/game-theory-responses|Best responses and Nash equilibrium]]
- [[game-theory-en/game-theory-mixed|Mixed strategies]]
- [[game-theory-en/game-theory-minimax|Project: compare worst-case payoffs]]

Review [[math-branches-en/math-branches-games|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
