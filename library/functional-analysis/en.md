# @lesson functional-analysis-norm
title: Norms and distance
summary: A norm measures vector size, and distance is the norm of the difference.
---
A norm measures vector size, and distance is the norm of the difference. The sum norm adds absolute components; the maximum norm takes the largest. On samples of two functions, the largest gap approximates their uniform distance.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
values = [-2, 3, -1]
print(sum(abs(v) for v in values), max(abs(v) for v in values))
```

```exercise
? What is the maximum norm of (−4, 1, 2)?
___
= 4
```

```quiz
? What is its sum norm?
* 7
- 4
- −1
> Add the absolute components 4, 1, and 2.
```

# @lesson functional-analysis-operator
title: Linear and bounded operators
summary: A linear operator preserves sums and scalar multiplication.
---
A linear operator preserves sums and scalar multiplication. For example, `T(f)=2f` doubles every value. It is bounded in the uniform norm because the output norm is twice the input norm. The bound 2 is attained for any nonzero function.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
samples = [-2, 1, 3]
output = [2 * x for x in samples]
print(max(map(abs, samples)), max(map(abs, output)))
```

```exercise
? If the input norm is 5, what is the norm of T(f)=2f?
___
= 10
```

```quiz
? Which property is part of linearity?
- Adds a constant to every input
* Preserves addition
- Maps every input to 1
> Linearity gives T(f+g)=T(f)+T(g).
```

# @lesson functional-analysis-contraction
title: Project: iteration and fixed points
summary: The map `T(x)=1+x/2` halves distances.
---
The map `T(x)=1+x/2` halves distances. Its fixed point satisfies `T(x)=x` and is 2. Try different starting values and watch the error shrink. The contraction principle generalizes this idea on a complete metric space.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
value = 0.0
for _ in range(3):
    value = 1 + value / 2
    print(value, abs(2 - value))
```

```exercise
? What is the fixed point of T(x)=3+x/2?
___
= 6
```

```quiz
? What is the error contraction factor in the example?
- 2
- 1
* 1/2
> The difference T(x)−T(2) is (x−2)/2.
```

# @lesson functional-analysis-reference
title: Introduction to functional analysis study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[functional-analysis-en/functional-analysis-norm|Norms and distance]]
- [[functional-analysis-en/functional-analysis-operator|Linear and bounded operators]]
- [[functional-analysis-en/functional-analysis-contraction|Project: iteration and fixed points]]

Review [[advanced-math-en/advanced-math-functional|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
