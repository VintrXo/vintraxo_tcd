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

# @lesson geometry-trigonometry-congruence
title: Triangle congruence
summary: Congruent triangles have the same shape and size.
---
Congruent triangles have the same shape and size. The side–side–side criterion says that three matching side lengths suffice. First check the triangle inequality to rule out lengths that cannot form a triangle.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
def valid_triangle(sides):
    a, b, c = sorted(sides)
    return a > 0 and a + b > c

first = (3, 4, 5)
second = (5, 3, 4)
print(valid_triangle(first) and sorted(first) == sorted(second))
print(valid_triangle((2, 3, 5)))
```

```exercise
? What is the sum of the shorter two sides of a 2, 3, 4 triangle?
___
= 5
```

```quiz
? Why do the lengths 2, 3, and 5 fail to form a triangle?
* The shorter sides sum to the longest
- All sides must be equal
- The longest side is odd
> The shorter sides must sum to more than the third to enclose an area.
```

# @lesson geometry-trigonometry-similarity
title: Similarity of triangles
summary: Two pairs of equal corresponding angles imply similarity because the remaining angles also agree.
---
Two pairs of equal corresponding angles imply similarity because the remaining angles also agree. If lengths scale by k, areas scale by `k²`.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
scale = 3
base, height = 4, 2
original_area = base * height / 2
scaled_area = (scale * base) * (scale * height) / 2
print(original_area, scaled_area)
```

```exercise
? How long is a side of length 7 after scaling lengths by 2?
___
= 14
```

```quiz
? By what factor does area grow when lengths triple?
- 3
* 9
- 6
> The base and height each triple, multiplying area by 3 × 3.
```

# @lesson geometry-trigonometry-identity
title: The Pythagorean identity
summary: A point on the unit circle has coordinates `cos(θ)` and `sin(θ)`.
---
A point on the unit circle has coordinates `cos(θ)` and `sin(θ)`. Its distance from the origin is one, so the Pythagorean theorem gives `sin²(θ) + cos²(θ) = 1`. One value determines the magnitude of the other; the quadrant determines the sign.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from math import cos, radians, sin

for angle in (30, 120, 225):
    theta = radians(angle)
    print(angle, round(sin(theta) ** 2 + cos(theta) ** 2, 8))
```

```exercise
? If sin(θ) = 0.6, what is the magnitude of cos(θ) as a decimal?
___
= 0.8
```

```quiz
? What is the sign of cosine in the second quadrant?
- Positive
- Always zero
* Negative
> In the second quadrant the point is left of the vertical axis, so its horizontal coordinate is negative.
```

# @lesson geometry-trigonometry-sine
title: The sine rule
summary: Each side a has an opposite angle A.
---
Each side a has an opposite angle A. The sine rule states `a/sin(A) = b/sin(B) = c/sin(C)`. Equating two expressions for a triangle's height gives these ratios. A known side and its opposite angle, together with a second angle, determine that angle's opposite side.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from math import radians, sin

a, angle_a, angle_b = 6, 30, 60
b = a * sin(radians(angle_b)) / sin(radians(angle_a))
print(round(b, 2))
```

```exercise
? If two opposite angles are equal and one corresponding side is 8, how long is the other?
___
= 8
```

```quiz
? Which angle's sine is paired with side b?
* The angle opposite b
- Either adjacent angle
- Always the largest angle
> Pair each side with its opposite angle.
```

# @lesson geometry-trigonometry-cosine
title: The cosine rule
summary: With sides a and b and included angle C, the opposite side satisfies `c² = a² + b² − 2ab cos(C)`.
---
With sides a and b and included angle C, the opposite side satisfies `c² = a² + b² − 2ab cos(C)`. At a right angle the final term vanishes, giving the Pythagorean theorem.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from math import cos, radians, sqrt

a, b = 3, 4
for angle in (60, 90, 120):
    c = sqrt(a * a + b * b - 2 * a * b * cos(radians(angle)))
    print(angle, round(c, 2))
```

```exercise
? If a = b = 5 and the included angle is 60 degrees, how long is the opposite side?
___
= 5
```

```quiz
? With a and b fixed, what happens to the third side as the angle increases from 60 to 120 degrees?
- It shortens
* It lengthens
- It stays the same
> Cosine decreases, making the subtracted term smaller and the squared side larger.
```

# @lesson geometry-trigonometry-survey
title: Project: measure the gap between landmarks
summary: Two landmarks are 30 and 40 metres from where you stand.
---
Two landmarks are 30 and 40 metres from where you stand. The angle between your lines of sight is 60 degrees. Sketch the triangle, identify the opposite side, and calculate its length. Repeat with 65 degrees to see the effect of an angle measurement error.

## Try it yourself

Predict the result, run the example, then change one input and compare.

```try python
from math import cos, radians, sqrt

for angle in (60, 65):
    distance = sqrt(30 ** 2 + 40 ** 2 - 2 * 30 * 40 * cos(radians(angle)))
    print(angle, round(distance, 1))
```

```exercise
? How far apart are the landmarks if the sight lines form a right angle?
___
= 50
```

```quiz
? Which rule directly uses the two distances from you and the included angle?
- Sine rule
- Circle area formula
* Cosine rule
> The known quantities are two sides and their included angle, and the unknown is the opposite side.
```

# @lesson computational-geometry-orientation
title: Orientation of three points
summary: The determinant of AB and AC tells which way the points turn.
---
The determinant of AB and AC tells which way the points turn. Positive is counterclockwise, negative clockwise, and zero means collinear. Its absolute value is twice the area of the triangle.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
def turn(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))

for point in ((1, 2), (1, -2), (1, 0)):
    print(turn((0, 0), (3, 0), point))
```

```exercise
? What is the area when the determinant magnitude is 10?
___
= 5
```

```quiz
? What does a zero determinant mean?
* The points are collinear
- The triangle is equilateral
- The turn is counterclockwise
> The vectors are linearly dependent and the area is zero.
```

# @lesson computational-geometry-segments
title: Segment intersection
summary: If each segment’s endpoints are on opposite sides of the other line, the interiors intersect.
---
If each segment’s endpoints are on opposite sides of the other line, the interiors intersect. When a determinant is zero, check whether that point is between the corresponding endpoints. This handles endpoint contact and collinear overlap.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
def turn(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))

def between(a, b, point):
    return all(min(x, y) <= value <= max(x, y)
               for x, y, value in zip(a, b, point, strict=True))

def intersects(a, b, c, d):
    first, second = turn(a, b, c), turn(a, b, d)
    third, fourth = turn(c, d, a), turn(c, d, b)
    crosses = first * second < 0 and third * fourth < 0
    touching = (
        first == 0 and between(a, b, c)
        or second == 0 and between(a, b, d)
        or third == 0 and between(c, d, a)
        or fourth == 0 and between(c, d, b)
    )
    return crosses or touching

for c, d in [((0, 2), (2, 0)), ((2, 2), (4, 4)), ((3, 3), (4, 4))]:
    print(intersects((0, 0), (2, 2), c, d))
```

```exercise
? How many points are shared if two segments meet only at one endpoint?
___
= 1
```

```quiz
? Why is a zero determinant alone insufficient?
- Endpoints cannot touch
* The point may be on the line outside the segment
- Zero indicates a positive turn
> Zero refers to the entire line; the bounds test restricts it to the segment.
```

# @lesson computational-geometry-hull
title: Convex hull
summary: The convex hull is the smallest convex set containing the points.
---
The convex hull is the smallest convex set containing the points. Sort the points and build a lower and upper chain. Pop the last point when adding the next would cause a nonpositive turn, retaining extreme vertices and dropping points between the ends of a straight edge.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
def turn(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))

def chain(points):
    boundary = []
    for point in points:
        while len(boundary) >= 2 and turn(boundary[-2], boundary[-1], point) <= 0:
            boundary.pop()
        boundary.append(point)
    return boundary

def hull(points):
    ordered = sorted(set(points))
    if len(ordered) <= 1:
        return ordered
    return chain(ordered)[:-1] + chain(reversed(ordered))[:-1]

print(hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (1, 0)]))
```

```exercise
? How many hull vertices are in the example?
___
= 4
```

```quiz
? What happens to (1,0)?
- It lies outside the hull
- It becomes the only vertex
* It is on an edge and not listed as a vertex
> The point is between the bottom edge’s two corners.
```

# @lesson computational-geometry-area
title: Polygon area project
summary: Order a simple polygon’s vertices along its boundary.
---
Order a simple polygon’s vertices along its boundary. Sum `xᵢyᵢ₊₁−yᵢxᵢ₊₁` for each edge, closing the polygon from last to first. The area is half the absolute sum, and reversing the order flips the sign.

## Try it yourself

Predict the output, run the example, then change an input.

```try python
from fractions import Fraction

def double_signed_area(vertices):
    following = vertices[1:] + vertices[:1]
    return sum(x * ny - y * nx for (x, y), (nx, ny) in zip(vertices, following, strict=True))

polygon = [(1, 1), (4, 1), (4, 3), (1, 3)]
forward = double_signed_area(polygon)
print(forward, double_signed_area(polygon[::-1]))
print(Fraction(abs(forward), 2))
```

```exercise
? What is the area of a rectangle of width three and height two?
___
= 6
```

```quiz
? What stays the same after reversing vertex order?
* Area
- The sign of the sum
- The traversal order
> Absolute value preserves the area despite the sign reversal.
```
