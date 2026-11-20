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

# @lesson arith-reference
title: Arithmetic and ratios reference
summary: Quick rules for arithmetic, fractions, ratios and percentages.
type: Reference
---
Use these rules as a quick reference while solving problems.

```reference
Order of operations | Parentheses, then multiplication and division, then addition and subtraction | 3 + 4 × 2 = 11
Adding fractions | Use a common denominator, then add the numerators | 1/2 + 1/4 = 3/4
Unit rate | Divide the total by the number of units | 24 ÷ 3 = 8
Percentage | Divide the part by the whole and multiply by 100 | 18 ÷ 24 × 100 = 75%
Percent change | Subtract the original from the new value, divide by the original, and multiply by 100 | (200 − 250) ÷ 250 × 100 = −20%
```
