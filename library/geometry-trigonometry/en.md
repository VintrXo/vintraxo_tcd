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

# @lesson geometry-trigonometry-reference
title: Intermediate geometry and trigonometry study guide
summary: Review the examples and revisit related lessons.
type: Reference
---
## Examples in this course

- [[geometry-trigonometry-en/geometry-trigonometry-congruence|Triangle congruence]]
- [[geometry-trigonometry-en/geometry-trigonometry-similarity|Similarity of triangles]]
- [[geometry-trigonometry-en/geometry-trigonometry-identity|The Pythagorean identity]]
- [[geometry-trigonometry-en/geometry-trigonometry-sine|The sine rule]]
- [[geometry-trigonometry-en/geometry-trigonometry-cosine|The cosine rule]]
- [[geometry-trigonometry-en/geometry-trigonometry-survey|Project: measure the gap between landmarks]]

## Related lessons

- [[geometry-en/geometry-pythagoras|The Pythagorean theorem]]
- [[trigonometry-en/trigonometry-circle|The unit circle]]
