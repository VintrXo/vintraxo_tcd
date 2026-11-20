# @lesson partial-differential-equations-partials
title: Variables and derivatives in the heat equation
summary: In `uₜ=κuₓₓ`, temperature depends on space and time.
---
In `uₜ=κuₓₓ`, temperature depends on space and time. The time derivative gives change at a point, and the second spatial derivative describes the curvature of the profile. The function `u=x²+2κt` satisfies the equation because its second spatial derivative is 2.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
kappa = 3
u_t = 2 * kappa
u_xx = 2
print(u_t, kappa * u_xx, u_t == kappa * u_xx)
```

```exercise
? What is uₓₓ for x²+6t?
___
= 2
```

```quiz
? Which derivative describes change in time at a fixed location?
* uₜ
- uₓₓ
- uₓ
> In uₜ time varies while position is fixed.
```

# @lesson partial-differential-equations-boundary
title: Initial and boundary conditions
summary: The initial profile specifies temperature at t=0.
---
The initial profile specifies temperature at t=0. Boundary conditions specify what happens at the ends over time. On a rod grid, hold the ends at zero and apply the neighbouring second difference only to interior nodes.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
old = [0, 0, 80, 0, 0]
new = old.copy()
for i in range(1, len(old) - 1):
    new[i] += 0.25 * (old[i - 1] - 2 * old[i] + old[i + 1])
print(new)
```

```exercise
? What is the centre temperature after the example step?
___
= 40
```

```quiz
? Which values stay fixed here?
- The centre
* Both endpoints
- All interior points
> The boundary condition holds both ends at zero.
```

# @lesson partial-differential-equations-stability
title: Project: check a diffusion step
summary: For the explicit scheme, `r=κΔt/Δx²`.
---
For the explicit scheme, `r=κΔt/Δx²`. The update gives each neighbour weight r and the centre weight `1−2r`. For `0≤r≤1/2` the weights are nonnegative and sum to one. Try a larger step to see a negative value arise in this example.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
left, centre, right = 0, 80, 0
for ratio in (0.25, 0.75):
    updated = ratio * left + (1 - 2 * ratio) * centre + ratio * right
    print(ratio, updated)
```

```exercise
? What is the centre weight at r=0.25? Enter a decimal.
___
= 0.5
```

```quiz
? Holding κ and Δx fixed, how does increasing Δt affect r?
- It decreases
- It stays fixed
* It increases
> The time step is in the numerator of r.
```

# @lesson partial-differential-equations-reference
title: Partial differential equations study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[partial-differential-equations-en/partial-differential-equations-partials|Variables and derivatives in the heat equation]]
- [[partial-differential-equations-en/partial-differential-equations-boundary|Initial and boundary conditions]]
- [[partial-differential-equations-en/partial-differential-equations-stability|Project: check a diffusion step]]

Review [[advanced-math-en/advanced-math-heat|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
