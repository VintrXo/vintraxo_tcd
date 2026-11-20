# @lesson operations-research-linear
title: Modelling and linear programming
summary: Specify decision variables, constraints, and the objective.
---
Specify decision variables, constraints, and the objective. With `x+y≤4`, `x≤2`, and `x,y≥0`, maximize `3x+2y`. The bounded feasible polygon has a vertex attaining the maximum. Check vertices formed by active constraints.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
vertices = [(0, 0), (2, 0), (2, 2), (0, 4)]
value, point = max((3 * x + 2 * y, (x, y)) for x, y in vertices)
print(value, point)
```

```exercise
? What is the objective at (0,4)?
___
= 8
```

```quiz
? Which feasible point attains the maximum?
* (2, 2)
- (0, 4)
- (3, 1)
> The point (2,2) is feasible and gives 10.
```

# @lesson operations-research-integer
title: Integer decisions and linear relaxation
summary: A box count must be an integer.
---
A box count must be an integer. Dropping that requirement enlarges the feasible set and gives an upper bound on a maximization problem. For `2x≤5` and objective `3x`, the continuous optimum is x=2.5, while the best integer is x=2.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
capacity, weight, value = 5, 2, 3
print(value * capacity / weight)
print(value * (capacity // weight))
```

```exercise
? What is the largest integer count of weight-2 boxes in capacity 7?
___
= 3
```

```quiz
? What does a relaxation give for an integer maximization problem?
- Always a lower bound
* An upper bound
- Always an integer solution
> A relaxation retains every original option and may add better ones.
```

# @lesson operations-research-assignment
title: Project: assign jobs to workers
summary: Each worker has a job-dependent cost.
---
Each worker has a job-dependent cost. Assign exactly one worker to each job and one job per worker. For this small example compare all permutations, showing why the first worker’s cheapest job can leave a costly job for the other.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from itertools import permutations

costs = [[1, 3], [2, 9]]
options = [(sum(costs[i][job] for i, job in enumerate(jobs)), jobs)
           for jobs in permutations(range(2))]
print(sorted(options))
```

```exercise
? What is the total cost if each worker takes the job with the same index?
___
= 10
```

```quiz
? What is the minimum total cost?
- 3
- 10
* 5
> The first worker takes the second job for 3, and the second takes the first for 2.
```

# @lesson operations-research-reference
title: Optimization and operations research study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[operations-research-en/operations-research-linear|Modelling and linear programming]]
- [[operations-research-en/operations-research-integer|Integer decisions and linear relaxation]]
- [[operations-research-en/operations-research-assignment|Project: assign jobs to workers]]

Review [[math-branches-en/math-branches-optimization|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
