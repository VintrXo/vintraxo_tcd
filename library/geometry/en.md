# @lesson geometry-rectangles
title: Perimeter and area
summary: A rectangle’s perimeter is the distance around it, twice the sum of its length and width.
---
A rectangle’s perimeter is the distance around it, twice the sum of its length and width. Its area is the region inside, measured by multiplying length by width. Perimeter uses metres and area uses square metres.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
length = 8
width = 5
print(2 * (length + width))
print(length * width)
```

```exercise
? Find the perimeter of a rectangle of length 7 and width 4.
___
= 22
```

```quiz
? What is the area of a 9 m by 3 m rectangle?
* 27 m²
- 24 m²
- 12 m²
> The area is 9 × 3.
```

# @lesson geometry-triangles
title: Triangle area
summary: A triangle’s area is half the product of a base and its perpendicular height.
---
A triangle’s area is half the product of a base and its perpendicular height. A base of 8 and height of 5 give an area of 20. The slanted side alone does not give the height.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
base = 8
height = 5
print(base * height / 2)
```

```exercise
? Find the area of a triangle with base 10 and perpendicular height 6.
___
= 30
```

```quiz
? What happens to the area when the height doubles and the base stays fixed?
- It stays the same
* It doubles
- It quadruples
> With a fixed base, area is proportional to height.
```

# @lesson geometry-circles
title: Circle area and circumference
summary: The diameter is twice the radius.
---
The diameter is twice the radius. Circumference is `2πr` and area is `πr²`. Doubling the radius doubles circumference and quadruples area.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
from math import pi

radius = 3
print(round(2 * pi * radius, 2))
print(round(pi * radius ** 2, 2))
```

```exercise
? What is the radius of a circle with diameter 14?
___
= 7
```

```quiz
? What is the area of a circle of radius 4 in terms of π?
- 8π
- 4π
* 16π
> Square the radius to get 16, then multiply by π.
```

# @lesson geometry-pythagoras
title: The Pythagorean theorem
summary: In a right triangle, the squared hypotenuse equals the sum of the squares of the two perpendicular sides.
---
In a right triangle, the squared hypotenuse equals the sum of the squares of the two perpendicular sides. The hypotenuse is opposite the right angle. The same relation gives straight-line distance from two coordinate differences.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
from math import hypot

print(hypot(3, 4))
print(hypot(9 - 1, 9 - 3))
```

```exercise
? Find the hypotenuse when the perpendicular sides are 5 and 12.
___
= 13
```

```quiz
? What is the distance between (1, 2) and (4, 6)?
* 5
- 7
- 25
> The coordinate differences are 3 and 4, and the square root of their squared sum is 5.
```

# @lesson geometry-volume
title: Volume and unit conversion
summary: A rectangular box has volume equal to its base area times its height.
---
A rectangular box has volume equal to its base area times its height. Convert cubic metres to cubic centimetres by multiplying by `100³`, applying the conversion along all three dimensions.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
length_cm = 50
width_cm = 40
height_cm = 30
volume_cm3 = length_cm * width_cm * height_cm
print(volume_cm3)
print(volume_cm3 / 1000)
```

```exercise
? How many cubic centimetres are in one litre?
___
= 1000
```

```quiz
? What is the volume in cubic metres of a 2 m by 3 m by 4 m box?
- 9
* 24
- 12
> Multiply all three dimensions: 2 × 3 × 4.
```

# @lesson geometry-scale
title: Project: estimate tiles from a floor plan
summary: A 1:50 plan shows a room 8 cm long and 6 cm wide.
---
A 1:50 plan shows a room 8 cm long and 6 cm wide. Convert the dimensions to metres, find the area, then estimate the tile count by tile area. Assume all offcuts can be reused, allow 10% spare, and round up.

## Try it yourself

Predict the output, then change an input and run the example again.

```try python
from fractions import Fraction
from math import ceil

scale = 50
area = Fraction(8 * scale, 100) * Fraction(6 * scale, 100)
tile_side = Fraction(40, 100)
print(float(area))
print(ceil(area / tile_side ** 2 * Fraction(11, 10)))
```

```exercise
? How many metres does a side measuring 10 cm on the same plan represent?
___
= 5
```

```quiz
? What is the room’s area in square metres?
- 24
- 48
* 12
> The plan represents a 4 m by 3 m room.
```

# @lesson geometry-reference
title: Geometry and measurement reference
summary: Key rules with quick examples.
type: Reference
---
```reference
Perimeter | Sum the side lengths | 2 × (8 + 5) = 26
Area | Measure the region in square units | 8 × 5 = 40
Volume | Base area × height | 2 × 3 × 4 = 24
```
