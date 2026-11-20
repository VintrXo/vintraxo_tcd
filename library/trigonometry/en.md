# @lesson trigonometry-angles
title: Degrees and radians
summary: A full turn is 360 degrees or `2π` radians.
---
A full turn is 360 degrees or `2π` radians. To convert degrees to radians, multiply by `π/180`. Trigonometric functions in `math` expect radians.

For a refresher, see [[geometry-en/geometry-pythagoras|The Pythagorean theorem]].

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

# @lesson trigonometry-reference
title: Trigonometry reference
summary: Core rules and examples for quick review.
type: Reference
---
```reference
Radians | Degrees × π/180 | 90° = π/2
Sine | Opposite ÷ hypotenuse | 3 ÷ 5 = 0.6
Tangent | Opposite ÷ adjacent | 3 ÷ 4 = 0.75
```
