# @lesson arith-order
title: Order of operations
summary: Parentheses and the priority of arithmetic operations.
---
Evaluate parentheses first, then multiplication and division from left to right, then addition and subtraction from left to right. `3 + 4 × 2` is 11, while `(3 + 4) × 2` is 14.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
print(3 + 4 * 2)
print((3 + 4) * 2)
```

```exercise
? What is 20 ÷ 5 × 3?
___
= 12
! Start with 20 ÷ 5, then multiply by 3.
```

```quiz
? What is 18 ÷ 3 × 2?
- 3
* 12
- 6
> Division and multiplication have the same priority, so start with 18 ÷ 3.
```

# @lesson arith-signed
title: Negative numbers
summary: Use a number line to understand adding and subtracting.
---
Numbers to the left of zero are negative. Subtract a positive number to move left, and subtract a negative number to move right. If the temperature starts at −3 and rises by 5 degrees, it reaches 2.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
start = -3
change = 5
print(start + change)
print(start - change)
```

```exercise
? The temperature is 2 degrees and falls by 5. What is it now?
___
= -3
! Move five steps left from 2.
```

```quiz
? Your balance is −4. What is it after adding 7?
- −11
- 11
* 3
> Move 7 steps right from −4, ending three steps past zero.
```

# @lesson arith-fractions
title: Fractions
summary: Add fractions using a common denominator.
---
In `3/4`, 3 is the numerator and 4 is the denominator. To add `1/2 + 1/4`, rewrite one half as `2/4`, giving `3/4`. Use parts of the same size before adding.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
from fractions import Fraction
first = Fraction(1, 2)
second = Fraction(1, 4)
print(first + second)
```

```exercise
? What is one quarter plus one half? Write a simplified fraction like 1/2.
___
= 3/4
! One half equals two quarters.
```

```quiz
? What is one third plus one sixth?
- 2/9
* 1/2
- 1/6
> One third equals two sixths. Three sixths equal one half.
```

# @lesson arith-decimals
title: Decimals and rounding
summary: Place value and rounding to the nearest hundredth.
---
Each place to the right of the decimal point is one tenth of the previous place. `0.75` is `75/100`. To round `2.378` to the nearest hundredth, look at the third decimal digit and round to `2.38`.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
from decimal import Decimal, ROUND_HALF_UP
value = Decimal('2.378')
print(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
```

```exercise
? Round 3.176 to the nearest hundredth.
___
= 3.18
! The third digit is 6, so increase the hundredths digit by one.
```

```quiz
? Round 4.263 to the nearest hundredth.
- 4.27
- 4.3
* 4.26
> The third digit is 3, so the hundredths digit stays the same.
```

# @lesson arith-ratios
title: Ratios
summary: Compare two quantities and scale a ratio.
---
A ratio compares two quantities in order. A juice-to-water ratio of `2:3` means two parts juice to three parts water. Double both quantities to double the recipe.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
juice = 2
water = 3
batches = 2
print(juice * batches, water * batches)
```

```exercise
? You have 4 cups of juice and need a juice-to-water ratio of 2 to 3. How many cups of water do you need?
___
= 6
! Double both quantities.
```

```quiz
? With 6 cups of juice at a juice-to-water ratio of 2 to 3, how many cups of water do you need?
- 4
* 9
- 6
> The juice went from 2 to 6, so multiply the water by 3 as well.
```

# @lesson arith-rates
title: Unit rates
summary: Calculate the price per item and compare offers.
---
A unit rate gives the amount per one unit. If 3 notebooks cost 24, divide 24 by 3 to get the price per notebook. Compare packages of different sizes using the same unit.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
price = 24
notebooks = 3
print(price / notebooks)
```

```exercise
? Four notebooks cost 28. What is the price per notebook?
___
= 7
! Divide 28 by 4.
```

```quiz
? Which offer has the lower price per notebook?
- 3 notebooks for 24
- Same price
* 5 notebooks for 35
> Five for 35 costs 7 per notebook. Three for 24 costs 8 per notebook.
```

# @lesson arith-percent
title: Percentages
summary: Express a part of a whole as a percentage.
---
Percent means per hundred. To find `15%` of 200, multiply 200 by `15/100`. To find the percentage itself, divide the part by the whole and multiply by 100.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
whole = 200
percent = 15
print(whole * percent / 100)
```

```exercise
? Find 20 percent of 150.
___
= 30
! Multiply 150 by 20 and divide by 100.
```

```quiz
? If you answer 18 out of 24 questions correctly, what percentage is that?
- 18%
* 75%
- 80%
> Divide 18 by 24, then multiply by 100.
```

# @lesson arith-discount
title: Discounts and percent change
summary: Use the original value to calculate discounts and increases.
---
Measure a discount relative to the original price. If the price drops from 250 to 200, the discount is 50 and the rate is `50 ÷ 250 × 100 = 20%`. For signed percent change, subtract the original from the new value and divide by the original, then multiply by 100.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
original = 250
new_price = 200
change = (new_price - original) / original * 100
print(f'{change:+.1f}%')
```

```exercise
? A price fell from 80 to 60. Enter the discount rate with a percent sign.
___
= 25%
! The discount is 20 and the original price is 80.
```

```quiz
? If the price rises from 200 to 250, what is the percent increase?
- 20%
- 50%
* 25%
> The starting value is 200 this time. Divide the increase of 50 by 200 and multiply by 100.
```

# @lesson arith-project
title: Project: compare shopping offers
summary: Use percentages and unit prices to compare two offers.
---
Compare two notebook offers. One sells 3 notebooks for 30 before a 20% discount. The other sells 5 for 35. Calculate the final price of each offer, then compare the price per notebook. Change the discount until the two unit prices match.

## Try it yourself

Run the example, change one value, and predict the result before running it again.

```try python
first_total = 30
first_count = 3
discount = 20
second_total = 35
second_count = 5
first_unit = first_total * (1 - discount / 100) / first_count
second_unit = second_total / second_count
print(f'A: {first_unit:.2f}')
print(f'B: {second_unit:.2f}')
```

```quiz
? At what discount on the first offer do the unit prices match?
- 20%
* 30%
- 10%
> The second offer costs 7 per notebook. The first offer must drop from 10 to 7 per notebook.
```

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

# @lesson intermediate-algebra-systems
title: Systems of equations
summary: In `x + y = 10` and `2x + y = 16`, subtract the first equation from the second to eliminate y.
---
In `x + y = 10` and `2x + y = 16`, subtract the first equation from the second to eliminate y. Substitute x back into the first. A solution must satisfy both equations.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
x = 16 - 10
y = 10 - x
print(x, y)
print(x + y == 10 and 2 * x + y == 16)
```

```exercise
? Find x when x + y = 7 and 2x + y = 11.
___
= 4
```

```quiz
? What is y in the worked example?
* 4
- 6
- 10
> With x equal to 6, the sum of 10 leaves 4.
```

# @lesson intermediate-algebra-factoring
title: Factoring
summary: Expansion turns products into sums; factoring reverses it.
---
Expansion turns products into sums; factoring reverses it. For `x² + 5x + 6`, find two numbers with sum 5 and product 6, giving `(x + 2)(x + 3)`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
for x in (-3, -2, 0, 1):
    expanded = x ** 2 + 5 * x + 6
    factored = (x + 2) * (x + 3)
    print(x, expanded, factored)
```

```exercise
? One of the numbers used to factor x² + 7x + 10 is 2. What is the other?
___
= 5
```

```quiz
? Which factorization equals x² − 9?
- (x − 9)(x + 1)
* (x − 3)(x + 3)
- (x − 3)²
> A difference of squares factors as the product of the difference and sum.
```

# @lesson intermediate-algebra-quadratics
title: Quadratic equations
summary: For `ax² + bx + c = 0` with `a ≠ 0`, the discriminant `D = b² − 4ac` determines the real roots.
---
For `ax² + bx + c = 0` with `a ≠ 0`, the discriminant `D = b² − 4ac` determines the real roots. Positive D gives two roots `(-b ± √D)/(2a)`, zero gives one repeated root, and negative D gives no real roots.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import sqrt

a, b, c = 1, -5, 6
discriminant = b * b - 4 * a * c
if discriminant < 0:
    print('No real roots')
else:
    roots = {(-b + sign * sqrt(discriminant)) / (2 * a) for sign in (-1, 1)}
    print(sorted(roots))
```

```exercise
? Find the repeated root of x² − 4x + 4 = 0.
___
= 2
```

```quiz
? How many real roots does x² + 1 = 0 have?
- 1
- 2
* 0
> The discriminant is −4.
```

# @lesson intermediate-algebra-exponents
title: Exponents and logarithms
summary: For a positive base `b ≠ 1`, `log_b(x) = y` means `bʸ = x`, with `x > 0`.
---
For a positive base `b ≠ 1`, `log_b(x) = y` means `bʸ = x`, with `x > 0`. For example, `log₂(8) = 3`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import log2

for exponent in (-2, 0, 3):
    value = 2 ** exponent
    print(value, log2(value))
```

```exercise
? What is log₂(32)?
___
= 5
```

```quiz
? What is two raised to the power −3?
* 1/8
- −8
- 8
> A negative exponent gives the reciprocal of the positive power.
```

# @lesson intermediate-algebra-sequences
title: Sequences and series
summary: An arithmetic sequence adds a fixed difference; a geometric sequence multiplies by a fixed ratio.
---
An arithmetic sequence adds a fixed difference; a geometric sequence multiplies by a fixed ratio. A series sums the terms. Starting at a with ratio r gives term n as `a × r^(n−1)`.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
arithmetic = [3 + 2 * i for i in range(4)]
geometric = [3 * 2 ** i for i in range(4)]
print(arithmetic, sum(arithmetic))
print(geometric, sum(geometric))
```

```exercise
? What is the fourth term in 2, 6, 18, …?
___
= 54
```

```quiz
? What is the sum of the first four terms in 3, 6, 12, 24, …?
- 24
* 45
- 48
> The series adds the four terms.
```

# @lesson intermediate-algebra-project
title: Project: recover a workshop setup cost
summary: A workshop costs 120 to set up and 15 per attendee.
---
A workshop costs 120 to set up and 15 per attendee. Tickets cost 25. Define revenue and cost, find the smallest attendance that covers the cost, then check what happens if tickets drop to 23.

## Try it yourself

Predict the output. Run the example, change an input, and see what changes.

```try python
from math import ceil

fixed = 120
variable = 15
for price in (25, 23):
    attendees = ceil(fixed / (price - variable))
    profit = attendees * price - (fixed + variable * attendees)
    print(price, attendees, profit)
```

```exercise
? What is the break-even attendance if tickets cost 30?
___
= 8
```

```quiz
? What is the minimum attendance if tickets cost 23?
- 12
- 18
* 15
> Each attendee contributes 8 toward fixed cost, and 120 ÷ 8 is 15.
```
