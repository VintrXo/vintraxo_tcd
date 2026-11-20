# @lesson algebra-variables
title: Variables and substitution
summary: A variable stands for a value.
---
A variable stands for a value. Replace it with a number and follow the order of operations. For example, `3x + 2` is 14 at `x = 4`.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
x = 4
print(3 * x + 2)
```

```exercise
? Evaluate 2x + 1 at x = 5.
___
= 11
```

```quiz
? Evaluate 3x + 2 at x = −2.
- 8
* -4
- -8
> Three times negative two is negative six, then add two.
```

# @lesson algebra-terms
title: Like terms
summary: In `3x + 2x − 4`, the first two terms have the same variable and exponent.
---
In `3x + 2x − 4`, the first two terms have the same variable and exponent. Add their coefficients to get `5x − 4`. The constant stays separate.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
x = 3
print(3 * x + 2 * x - 4)
print(5 * x - 4)
```

```exercise
? What is the coefficient of x after simplifying 7x − 3x?
___
= 4
```

```quiz
? Which expression equals 4x + 3 + 2x?
- 9x
- 6x
* 6x + 3
> Add the coefficients of x and keep the constant 3.
```

# @lesson algebra-distribute
title: Distributive property
summary: Multiply every term inside the parentheses by the factor outside.
---
Multiply every term inside the parentheses by the factor outside. For instance, `−2(x + 3) = −2x − 6`. Apply the sign of the factor to each term.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
x = 5
print(-2 * (x + 3))
print(-2 * x - 6)
```

```exercise
? What is the constant after expanding 4(x + 2)?
___
= 8
```

```quiz
? Which expression equals −3(x − 2)?
* −3x + 6
- −3x − 6
- −3x + 2
> Negative three times negative two is positive six.
```

# @lesson algebra-equations
title: Linear equations
summary: An equation balances two sides.
---
An equation balances two sides. To solve `3x + 2 = 14`, subtract 2 from both sides and divide both sides by 3. Substitute the answer to check both sides.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
x = (14 - 2) / 3
print(x)
print(3 * x + 2 == 14)
```

```exercise
? Find x in 2x + 5 = 17.
___
= 6
```

```quiz
? Find x in 4x − 3 = 9.
- 1.5
* 3
- 6
> Add 3 to both sides to get 4x = 12.
```

# @lesson algebra-inequalities
title: Inequalities
summary: Add or subtract the same quantity on both sides.
---
Add or subtract the same quantity on both sides. Multiplying or dividing by a negative number reverses the inequality, so `−2x > 6` means `x < −3`.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
for x in (-5, -3, 0):
    print(x, -2 * x > 6, x < -3)
```

```exercise
? What is the boundary in the solution to x + 2 < 7?
___
= 5
```

```quiz
? Which statement is equivalent to −4x ≤ 8?
- x ≤ −2
- x ≥ 2
* x ≥ −2
> Division by −4 reverses the symbol and gives −2.
```

# @lesson algebra-budget
title: Project: plan a trip budget
summary: A trip costs 30 upfront plus 8 per person.
---
A trip costs 30 upfront plus 8 per person. The budget is 70. Set up `30 + 8n ≤ 70`, find the largest whole number that works, and verify that one more person exceeds the budget.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
budget = 70
fixed_cost = 30
per_person = 8
people = (budget - fixed_cost) // per_person
print(people)
print(fixed_cost + (people + 1) * per_person)
```

```exercise
? How many people fit if the budget changes to 62?
___
= 4
```

```quiz
? What is the maximum group size with a budget of 69?
* 4
- 5
- 3
> After the fixed cost, 39 remains. Five people would cost 40.
```

# @lesson algebra-reference
title: Algebra foundations reference
summary: Key rules and quick examples.
type: Reference
---
```reference
Substitution | Replace the variable with its value | 3x + 2 = 14 at x = 4
Distribution | Multiply every term in parentheses | 2(x + 3) = 2x + 6
Inequality | Reverse the sign when dividing by a negative | −2x > 6 ⇔ x < −3
```
