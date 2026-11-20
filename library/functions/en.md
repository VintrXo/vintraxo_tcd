# @lesson functions-rule
title: Function inputs and outputs
summary: A function gives each allowed input exactly one output.
---
A function gives each allowed input exactly one output. In `f(x) = 2x + 1`, the input 3 maps to 7. Different inputs may share an output.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
def f(x):
    return 2 * x + 1

for x in (-1, 0, 3):
    print(x, f(x))
```

```exercise
? Evaluate f(4) for f(x) = 2x + 1.
___
= 9
```

```quiz
? If one input has two different outputs, is the relation a function?
- Yes
* No
- Only if both are positive
> A single input must have exactly one output.
```

# @lesson functions-points
title: Coordinates and tables
summary: A point `(x, y)` moves horizontally by `x` and vertically by `y`.
---
A point `(x, y)` moves horizontally by `x` and vertically by `y`. Evaluate the function at each input and plot the resulting pair. The point `(1, 3)` lies on `y = x + 2`.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
for x in range(-2, 3):
    print((x, x + 2))
```

```exercise
? What is the vertical coordinate at x = −1 on y = x + 2?
___
= 1
```

```quiz
? Which point is on y = 2x − 1?
- (3, 2)
- (0, 1)
* (2, 3)
> At x = 2, y = 2 × 2 − 1 = 3.
```

# @lesson functions-slope
title: Slope and intercept
summary: In `y = mx + b`, `m` is the change in `y` for each unit increase in `x`, and `b` is `y` at `x = 0`.
---
In `y = mx + b`, `m` is the change in `y` for each unit increase in `x`, and `b` is `y` at `x = 0`. Change the slope in the plot and observe the line.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
m = -2
b = 3
print(b)
print((m * 2 + b) - (m * 1 + b))
```

```try html
<html lang="en" dir="ltr">
<label>Slope <input id="slope" type="range" min="-3" max="3" value="1" step="0.5"></label>
<output id="equation" dir="ltr"></output>
<canvas id="graph" width="360" height="220" style="display:block;max-width:100%;background:#f1f5f9" aria-label="Graph of the linear function"></canvas>
<script>
const slope = document.querySelector('#slope');
const canvas = document.querySelector('#graph');
const ctx = canvas.getContext('2d');
function draw() {
  const m = Number(slope.value);
  document.querySelector('#equation').textContent = 'y = ' + m + 'x + 1';
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(0, 110);
  ctx.lineTo(360, 110);
  ctx.moveTo(180, 0);
  ctx.lineTo(180, 220);
  ctx.stroke();
  ctx.strokeStyle = '#2563eb';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(0, 110 - 20 * (m * -9 + 1));
  ctx.lineTo(360, 110 - 20 * (m * 9 + 1));
  ctx.stroke();
  ctx.fillStyle = '#2563eb';
  ctx.beginPath();
  ctx.arc(180, 90, 4, 0, Math.PI * 2);
  ctx.fill();
}
slope.addEventListener('input', draw);
draw();
</script>
</html>
```

```exercise
? Enter the vertical intercept in y = 5x − 4.
___
= -4
```

```quiz
? Find the slope between (1, 2) and (3, 8).
* 3
- 6
- 2
> The vertical change is 6 and the horizontal change is 2. Slope is 6 ÷ 2.
```

# @lesson functions-domain
title: Domains and constraints
summary: The domain consists of allowed inputs.
---
The domain consists of allowed inputs. Zero is excluded from `1/x`. A model that counts books takes nonnegative integers because the input represents a real quantity.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
for x in (-2, -1, 0, 1, 2):
    if x == 0:
        print(x, 'undefined')
    else:
        print(x, 1 / x)
```

```exercise
? Which value is excluded from 1/(x − 3)?
___
= 3
```

```quiz
? Which input is unsuitable for a function that computes the cost of a number of books?
- 0
* 2.5
- 3
> A count of books is a whole number. 2.5 is not.
```

# @lesson functions-quadratic
title: Quadratic functions
summary: The graph of `y = x²` is a curve.
---
The graph of `y = x²` is a curve. Opposite inputs give the same result, so the graph is symmetric about the vertical axis.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
for x in range(-3, 4):
    print(x, x ** 2)
```

```exercise
? Find y at x = −4 on y = x².
___
= 16
```

```quiz
? What is the minimum value of y = x² + 2?
- 0
- -2
* 2
> A real square is nonnegative and reaches zero at x = 0.
```

# @lesson functions-plans
title: Project: compare subscription plans
summary: Plan A costs 20 upfront plus 5 per use.
---
Plan A costs 20 upfront plus 5 per use. Plan B costs 8 per use with no upfront fee. Write both functions and try different counts to find the first whole number of uses where plan A is cheaper.

## Try it yourself

Predict the output, run the example, then change a value and run it again.

```try python
def plan_a(uses):
    return 20 + 5 * uses

def plan_b(uses):
    return 8 * uses

for uses in range(5, 9):
    print(uses, plan_a(uses), plan_b(uses))
```

```exercise
? What does plan A cost for 6 uses?
___
= 50
```

```quiz
? At what whole number of uses does plan A first become cheaper?
* 7
- 6
- 8
> At 6 uses the costs are 50 and 48. At 7 they are 55 and 56.
```

# @lesson functions-reference
title: Functions and graphs reference
summary: Key rules and quick examples.
type: Reference
---
```reference
Function | Exactly one output for every allowed input | f(3) = 7 for f(x) = 2x + 1
Slope | Vertical change divided by horizontal change | 6 ÷ 2 = 3
Vertical intercept | The value of y at x = 0 | In y = 2x + 1 the intercept is 1
```
