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

# @lesson trigonometry-angles
title: Degrees and radians
summary: A full turn is 360 degrees or `2π` radians.
---
A full turn is 360 degrees or `2π` radians. To convert degrees to radians, multiply by `π/180`. Trigonometric functions in `math` expect radians.

For a refresher, see [[math-geometry-en/geometry-pythagoras|The Pythagorean theorem]].

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
from math import degrees, pi, radians

print(round(radians(60) / pi, 6))
print(degrees(pi / 2))
```

```exercise
? How many degrees are in π radians?
___
= 180
```

```quiz
? What is 90 degrees in radians?
* π/2
- π
- 2π
> Multiply 90 by π/180 to get π/2.
```

# @lesson trigonometry-ratios
title: Sine, cosine, and tangent
summary: For an acute angle in a right triangle, sine is opposite over hypotenuse, cosine is adjacent over hypotenuse, and tangent is opposite over adjacent.
---
For an acute angle in a right triangle, sine is opposite over hypotenuse, cosine is adjacent over hypotenuse, and tangent is opposite over adjacent. Changing to the other acute angle swaps the opposite and adjacent legs.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
opposite = 3
adjacent = 4
hypotenuse = 5
print(opposite / hypotenuse)
print(adjacent / hypotenuse)
print(opposite / adjacent)
```

```exercise
? If the adjacent side is 12 and the hypotenuse is 13, enter cosine as a fraction like 4/5.
___
= 12/13
```

```quiz
? If the opposite side is 5 and the adjacent side is 12, what is tangent?
- 5/13
* 5/12
- 12/5
> Tangent compares the opposite side to the adjacent side.
```

# @lesson trigonometry-circle
title: The unit circle
summary: The unit circle is centred at the origin and has radius one.
---
The unit circle is centred at the origin and has radius one. Measure positive angles counterclockwise from the positive horizontal axis. The horizontal coordinate is cosine and the vertical coordinate is sine, extending the ratios beyond 90 degrees.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
from math import cos, radians, sin

for angle in (0, 90, 180, 270):
    theta = radians(angle)
    print(angle, (round(cos(theta)), round(sin(theta))))
```

```exercise
? What is the sine of 90 degrees?
___
= 1
```

```quiz
? Where is the point at 180 degrees?
- (1, 0)
- (0, −1)
* (−1, 0)
> A half turn puts the point at the left end of the horizontal axis.
```

# @lesson trigonometry-period
title: Sine and periodicity
summary: Sine repeats after one full turn.
---
Sine repeats after one full turn. For example, `sin(30°)` equals `sin(390°)`. For `sin(2x)`, half a turn in `x` is enough to complete one full cycle of the output.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
from math import radians, sin

for angle in (30, 390, 750):
    print(angle, round(sin(radians(angle)), 4))
```

```exercise
? How many degrees are in one full period of sin(x)?
___
= 360
```

```quiz
? What is the period of sin(2x), in degrees?
* 180
- 360
- 720
> When x increases by 180, 2x increases by 360.
```

# @lesson trigonometry-inverse
title: Finding an angle from a ratio
summary: If you know the opposite and adjacent sides of an acute angle, divide them and take the inverse tangent.
---
If you know the opposite and adjacent sides of an acute angle, divide them and take the inverse tangent. Python’s `atan` returns radians; use `degrees` to convert the result.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
from math import atan, degrees

rise = 3
run = 4
print(round(degrees(atan(rise / run)), 2))
```

```exercise
? In degrees, what is the acute angle when the opposite and adjacent sides are equal?
___
= 45
```

```quiz
? Which operation recovers the angle from opposite over adjacent?
- Sine
* Inverse tangent
- Cosine
> Opposite over adjacent is tangent, so use its inverse.
```

# @lesson trigonometry-height
title: Project: estimate a tower’s height
summary: On level ground, you stand 20 metres horizontally from a tower.
---
On level ground, you stand 20 metres horizontally from a tower. The angle from eye level to the top is 30 degrees, and your eye is 1.6 metres above the ground. Use tangent to find the rise above your eye, then add eye height. Change the angle to explore measurement error.

## Try it yourself

Predict the output, run the example, then change a value and compare.

```try python
from math import radians, tan

distance = 20
eye_height = 1.6
for angle in (29, 30, 31):
    height = distance * tan(radians(angle)) + eye_height
    print(angle, round(height, 2))
```

```exercise
? If the elevation angle is 45 degrees and the horizontal distance is 10 m, how far above eye level is the top?
___
= 10
```

```quiz
? Why add 1.6 metres to the result?
- To correct the angle measurement
- To convert degrees to radians
* To convert the rise above eye level to height above ground
> Tangent gives the rise above the horizontal line at eye level.
```
