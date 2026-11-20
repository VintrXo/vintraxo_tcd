# @lesson fourier-analysis-harmonics
title: Periods and harmonics
summary: Harmonic n over a `2π` cycle, such as `sin(nx)`, completes n oscillations per cycle.
---
Harmonic n over a `2π` cycle, such as `sin(nx)`, completes n oscillations per cycle. Adding harmonics produces a more complex periodic signal. The aim is to describe that signal by the amplitudes and phases of its waves.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import pi, sin

for angle in (0, pi / 4, pi / 2):
    print(round(sin(angle), 3), round(sin(2 * angle), 3))
```

```exercise
? How many oscillations does sin(4x) complete from 0 to 2π?
___
= 4
```

```quiz
? What is the period of sin(2x)?
* π
- 2π
- 4π
> The inner angle doubles, so x only needs to increase by π.
```

# @lesson fourier-analysis-orthogonality
title: Orthogonality of harmonics
summary: Over a full cycle, the integral of `sin(mx)sin(nx)` is zero for distinct positive integers m and n.
---
Over a full cycle, the integral of `sin(mx)sin(nx)` is zero for distinct positive integers m and n. It is π when m=n. This isolates each frequency’s contribution. The example uses sample averages to illustrate the difference.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import sin, tau

points = [tau * index / 64 for index in range(64)]
for harmonic in (1, 2):
    average = sum(sin(x) * sin(harmonic * x) for x in points) / len(points)
    print(harmonic, f'{round(average, 6) + 0.0:.6f}')
```

```exercise
? What is the full-cycle average of sin²(x)? Enter a decimal.
___
= 0.5
```

```quiz
? What is the full-cycle integral of sin(x)sin(3x)?
- π
* 0
- 2π
> The harmonics are distinct, so the positive and negative contributions cancel.
```

# @lesson fourier-analysis-coefficients
title: Fourier coefficients
summary: For `f(x)=1+2cos(x)+3sin(2x)`, its full-period mean gives the constant term.
---
For `f(x)=1+2cos(x)+3sin(2x)`, its full-period mean gives the constant term. Twice the mean of f times the chosen sine or cosine gives that harmonic’s coefficient. Its squared mean is one half, while its mean product with the other harmonics is zero.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from math import cos, sin, tau

count = 64
points = [tau * index / count for index in range(count)]
values = [1 + 2 * cos(x) + 3 * sin(2 * x) for x in points]
constant = sum(values) / count
cos_one = 2 * sum(y * cos(x) for x, y in zip(points, values, strict=True)) / count
sin_two = 2 * sum(y * sin(2 * x) for x, y in zip(points, values, strict=True)) / count
print(*(round(value, 4) for value in (constant, cos_one, sin_two)))
```

```exercise
? What is the coefficient of cos(x) in 4 + 5cos(x)?
___
= 5
```

```quiz
? What is the signal’s full-cycle mean in the example?
- 2
- 3
* 1
> The sine and cosine average to zero, leaving the constant 1.
```

# @lesson fourier-analysis-spectrum
title: Project: detect two signal frequencies
summary: The discrete transform compares samples against complex exponentials at different frequencies.
---
The discrete transform compares samples against complex exponentials at different frequencies. Here scan four positive candidate frequencies in a two-tone signal and compare coefficient magnitudes. Change one wave’s amplitude and observe its matching frequency bin.

## Try it yourself

Predict the output, then run the example and change an input.

```try python
from cmath import exp
from math import sin, tau

count = 32
signal = [sin(tau * i / count) + 0.5 * sin(tau * 3 * i / count)
          for i in range(count)]
for frequency in range(1, 5):
    coeff = sum(value * exp(-1j * tau * frequency * i / count)
                for i, value in enumerate(signal))
    print(frequency, round(2 * abs(coeff) / count, 3))
```

```exercise
? What is the amplitude of frequency three in the example? Enter a decimal.
___
= 0.5
```

```quiz
? Which two frequencies are present in the signal?
* 1 and 3
- 1 and 2
- 2 and 4
> Among the frequencies scanned, only bins 1 and 3 have nonzero magnitude.
```

# @lesson fourier-series-synthesis
title: Signal reconstruction
summary: A Fourier series combines a constant, sines, and cosines.
---
A Fourier series combines a constant, sines, and cosines. A partial sum keeps only finitely many harmonics. For `f(x)=1+2cos(x)+sin(3x)`, stopping at harmonic one drops the last term. Compare two inputs, since the error may vanish at a particular point.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import cos, pi, sin

for x in (0, pi / 2):
    partial = 1 + 2 * cos(x)
    full = partial + sin(3 * x)
    print(round(partial, 3), round(full, 3))
```

```exercise
? What is the partial sum at x=0?
___
= 3
```

```quiz
? Which term restores the full value in the example?
* sin(3x)
- cos(3x)
- sin(x)
> Stopping at the first harmonic omits the third.
```

# @lesson fourier-series-sine-series
title: Sine series on an interval
summary: On `[0,L]`, each `sin(nπx/L)` vanishes at both ends.
---
On `[0,L]`, each `sin(nπx/L)` vanishes at both ends. Its coefficient is `2/L` times the integral of the function multiplied by that mode. The example estimates the first coefficients of a two-mode profile using midpoint quadrature.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import pi, sin

length = 1
count = 128
width = length / count
points = [(index + 0.5) * width for index in range(count)]
for mode in (1, 3):
    integral = sum((sin(pi * x) + 0.5 * sin(3 * pi * x)) * sin(mode * pi * x)
                   for x in points) * width
    print(mode, round(2 * integral / length, 6))
```

```exercise
? What is the third mode coefficient? Enter a decimal.
___
= 0.5
```

```quiz
? What is the value of each sine mode at x=L?
- 1
* 0
- L
> For integer n, sin(nπ) is zero.
```

# @lesson fourier-series-heat
title: Project: cool a rod with two modes
summary: For a rod with both ends fixed at zero, mode `sin(nπx/L)` decays by `exp(−κ(nπ/L)²t)` in the heat equation.
---
For a rod with both ends fixed at zero, mode `sin(nπx/L)` decays by `exp(−κ(nπ/L)²t)` in the heat equation. Split the starting profile into two modes, apply their decay factors, and add them. Mode three has nine times mode one’s exponential decay rate.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import exp, pi, sin

length, diffusivity = 1, 1 / pi ** 2
x = 0.5
for time in (0, 0.25, 1):
    first = exp(-diffusivity * (pi / length) ** 2 * time)
    third = 0.5 * exp(-diffusivity * (3 * pi / length) ** 2 * time)
    temperature = first * sin(pi * x / length) + third * sin(3 * pi * x / length)
    print(time, round(temperature, 3))
```

```exercise
? How many times faster is the decay rate of mode three than mode one?
___
= 9
```

```quiz
? Which mode persists longer?
- Third
- They decay at the same rate
* First
> The decay rate is proportional to the square of the mode number.
```

# @lesson fourier-waves-standing
title: Standing modes on a string
summary: Standing modes on a string.
---
For `uₜₜ=c²uₓₓ` on a string of length L with fixed ends, `sin(nπx/L)` vanishes at both endpoints. Its angular frequency is `ωₙ=cnπ/L`. Unlike the heat model, this ideal mode oscillates without a decay factor.

## Try it yourself

```try python
from math import pi, sin

length, speed, mode = 2, 4, 3
omega = speed * mode * pi / length
print(round(omega / pi))
print(round(sin(mode * pi * length / length), 6) + 0.0)
```

```exercise
? What is ω₁/π if L=2 and c=4?
___
= 2
```

```quiz
? What is the displacement at either fixed end?
* 0
- 1
- L
> Zero displacement is the boundary condition.
```

# @lesson fourier-waves-initial
title: Initial displacement and velocity
summary: Initial displacement and velocity.
---
For each mode, the time factor is `A cos(ωt)+B sin(ωt)`. At zero, modal displacement equals A and modal velocity equals `ωB`. Start from rest by setting B=0 in every mode. For a velocity impulse from equilibrium, set A=0 and divide modal velocity by ω to find B.

## Try it yourself

```try python
from math import cos, pi, sin

omega, displacement, velocity = 2, 0, 3
coefficient = velocity / omega
for time in (0, pi / 4):
    print(round(displacement * cos(omega * time) + coefficient * sin(omega * time), 3))
```

```exercise
? If ω=2 and initial modal velocity is 4, what is B?
___
= 2
```

```quiz
? Which coefficient is fixed by initial modal displacement?
- B
* A
- ω
> At zero cosine is one and sine is zero, leaving A.
```

# @lesson fourier-waves-superposition
title: Project: superpose two string modes
summary: Project: superpose two string modes.
---
Use a string of length one and wave speed one, with initial displacement `sin(πx)+0.5sin(3πx)` and zero initial velocity. Multiply each displacement coefficient by the cosine of its angular frequency times time. Compare the centre over time, then set x to an endpoint to check the fixed boundary.

## Try it yourself

```try python
from math import cos, pi, sin

modes = [(1, 1.0), (3, 0.5)]
x = 0.5
for time in (0, 0.5, 1):
    value = sum(amplitude * sin(n * pi * x) * cos(n * pi * time)
                for n, amplitude in modes)
    print(time, round(value, 6) + 0.0)
```

```exercise
? What is the initial centre displacement? Enter a decimal.
___
= 0.5
```

```quiz
? What determines the difference between the two frequencies?
- Initial displacement amplitude
- Only the measurement position
* The mode number n
> In this model the angular frequency is proportional to n.
```

# @lesson advanced-math-heat
title: Partial differential equations
summary: Temperature along a rod depends on position and time.
---
Temperature along a rod depends on position and time. The 1D heat equation relates change over time to the second spatial derivative. On a grid, approximate it by comparing each point with its two neighbours. This example adds one quarter of the second difference per step and fixes both ends at zero.

Review the prerequisite idea in [[math-branches-en/math-branches-differential|Differential equations]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
current = [0, 0, 100, 0, 0]
for _ in range(2):
    updated = current.copy()
    for i in range(1, len(current) - 1):
        difference = current[i - 1] - 2 * current[i] + current[i + 1]
        updated[i] = current[i] + 0.25 * difference
    current = updated
    print(current)
```

```exercise
? In the example, what is the centre value after the first step?
___
= 50
```

```quiz
? Why compute the next step from the old list?
* All points update from the same state
- To ignore neighbours
- To change the boundary values
> Using an already updated value for a neighbour would mix two time levels.
```

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

# @lesson advanced-math-physics
title: Mathematical physics
summary: In an ideal mass–spring model, the force is `−kx` and friction is absent.
---
In an ideal mass–spring model, the force is `−kx` and friction is absent. Total energy is kinetic energy `mv²/2` plus spring potential energy `kx²/2`. Speed is zero at maximum displacement, while at equilibrium all the energy is kinetic.

Review the prerequisite idea in [[math-branches-en/math-branches-differential|Differential equations]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
from math import sqrt

mass = 1
stiffness = 4
amplitude = 0.5
energy = stiffness * amplitude ** 2 / 2
speed_at_equilibrium = sqrt(2 * energy / mass)
print(energy, speed_at_equilibrium)
```

```exercise
? What is the spring energy at k = 4 and x = 1?
___
= 2
```

```quiz
? What happens to total energy in this model?
- It is zero at equilibrium
* It stays constant
- It doubles every cycle
> With no friction, energy transfers between kinetic and potential forms.
```

# @lesson mathematical-physics-oscillation
title: The harmonic oscillator
summary: For an undamped spring, `mx″=−kx`.
---
For an undamped spring, `mx″=−kx`. Starting at maximum displacement A with zero velocity gives `A cos(ωt)`, where `ω=√(k/m)`. With fixed mass, greater stiffness increases angular frequency.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import pi, sqrt

mass, stiffness = 1, 4
omega = sqrt(stiffness / mass)
print(omega, round(2 * pi / omega, 3))
```

```exercise
? What is the angular frequency for k=9 and m=1?
___
= 3
```

```quiz
? If mass quadruples at fixed stiffness, what happens to angular frequency?
* It halves
- It doubles
- It is unchanged
> Mass is in the denominator under the square root.
```

# @lesson mathematical-physics-energy
title: Energy conservation and model checks
summary: For an ideal spring, the derivative of `E=mv²/2+kx²/2` is `v(mv′+kx)=0`.
---
For an ideal spring, the derivative of `E=mv²/2+kx²/2` is `v(mv′+kx)=0`. Conserved energy provides a check on calculations. Small discrepancies can arise from numerical approximation.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import cos, sin

m, k, amplitude, omega = 1, 4, 0.5, 2
for t in (0, 0.5, 1):
    x = amplitude * cos(omega * t)
    v = -amplitude * omega * sin(omega * t)
    print(round((m * v * v + k * x * x) / 2, 6))
```

```exercise
? What is potential energy at x=0?
___
= 0
```

```quiz
? What remains constant in this model?
- Speed at all times
* Total kinetic plus potential energy
- Displacement at all times
> Energy moves between the two forms while the total stays constant.
```

# @lesson mathematical-physics-wave
title: Project: a travelling wave
summary: The wave `u(x,t)=sin(x−ct)` travels right for positive c: the same phase occurs at a larger x later.
---
The wave `u(x,t)=sin(x−ct)` travels right for positive c: the same phase occurs at a larger x later. Check that its value is constant along `x=x₀+ct`. In the ideal wave equation, propagation speed relates the second space and time derivatives.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import sin

speed, start = 2, 1
for t in (0, 1, 2):
    x = start + speed * t
    print(x, round(sin(x - speed * t), 3))
```

```exercise
? With c=2 and phase starting at x=1, where is it at t=3?
___
= 7
```

```quiz
? Which way does the wave travel for positive c?
- Left
- It is stationary
* Right
> For fixed phase, x increases by ct.
```

# @lesson vector-integral-theorems-green
title: Green’s theorem
summary: For a suitable planar region with counterclockwise boundary, Green’s theorem equates circulation around the boundary with the area integral of `Qₓ−Pᵧ`.
---
For a suitable planar region with counterclockwise boundary, Green’s theorem equates circulation around the boundary with the area integral of `Qₓ−Pᵧ`. For `F=(0,x)` on a square of side 2, only the upward right edge contributes, and the curl inside is 1.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
side = 2
right_edge = side * side
area = side ** 2
print(right_edge, 1 * area)
```

```exercise
? What is the integral of constant curl 1 over a square of side 3?
___
= 9
```

```quiz
? What happens to the line integral if the boundary direction reverses?
* Its sign reverses
- It doubles
- It always stays fixed
> Reversal flips the tangent and therefore the sign of the dot product.
```

# @lesson vector-integral-theorems-stokes
title: Stokes’ theorem and surface integrals
summary: Stokes’ theorem equates the flux of `∇×F` through an oriented surface with the circulation of F around its right-hand-oriented boundary.
---
Stokes’ theorem equates the flux of `∇×F` through an oriented surface with the circulation of F around its right-hand-oriented boundary. Flux integrates the dot product with the unit normal. For an upward-facing disk and `F=(−y,x,0)`, normal curl is 2, and the dot product along its angle-parameterized circular edge is `r²`.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
from math import pi, tau

radius = 3
surface_flux = 2 * pi * radius ** 2
boundary_circulation = radius ** 2 * tau
print(round(surface_flux, 3), round(boundary_circulation, 3))
```

```exercise
? What is the vertical curl component in this example?
___
= 2
```

```quiz
? How is the boundary traversed when viewed from above the upward-facing disk?
- Clockwise
* Counterclockwise
- With no orientation
> With the right thumb upward, the curled fingers indicate the positive direction.
```

# @lesson vector-integral-theorems-gauss
title: Project: calculate flux out of a box
summary: The divergence theorem equates outward flux across a closed surface with the volume integral of divergence.
---
The divergence theorem equates outward flux across a closed surface with the volume integral of divergence. For `F=(x,2y,3z)` on a box from the origin with side lengths `(2,3,4)`, the coordinate-zero faces contribute nothing. Compute the opposite faces and compare with divergence times volume.

## Try it yourself

Predict the result, then run the example and vary one input.

```try python
x, y, z = 2, 3, 4
face_fluxes = [x * y * z, 2 * y * x * z, 3 * z * x * y]
volume = x * y * z
print(face_fluxes)
print(sum(face_fluxes), (1 + 2 + 3) * volume)
```

```exercise
? What is the divergence of the project field?
___
= 6
```

```quiz
? Why does the face x=0 contribute zero flux?
- The face has zero area
- Because the box is open
* The normal component of the field is zero
> The face normal lies on the x-axis and the field’s x component vanishes there.
```

# @lesson advanced-math-curvature
title: Differential geometry
summary: Differential geometry studies shapes using calculus.
---
Differential geometry studies shapes using calculus. Curvature measures how quickly the tangent direction changes per unit of arc length. For a circle of radius `r`, curvature is the constant `1/r`: the tangent makes one full turn over a distance `2πr`.

Review the prerequisite idea in [[math-calculus-en/calculus-rate|Instantaneous rate]].

## Try it yourself

Predict the result, then run the example and change one input.

```try python
from math import pi

for radius in (1, 2, 4):
    turn = 2 * pi
    length = 2 * pi * radius
    print(radius, round(turn / length, 2))
```

```exercise
? What is the curvature of a circle of radius 5? Enter a decimal.
___
= 0.2
```

```quiz
? What happens to curvature if the radius doubles?
- It doubles
- It stays the same
* It halves
> Curvature is the reciprocal of the radius.
```

# @lesson differential-geometry-tangent
title: Parametric curves and tangents
summary: The curve `r(t)=(t,t²)` gives a point for each t, and differentiating its coordinates gives the tangent vector `(1,2t)`.
---
The curve `r(t)=(t,t²)` gives a point for each t, and differentiating its coordinates gives the tangent vector `(1,2t)`. When nonzero, this vector gives the tangent line direction.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
t = 2
print((t, t ** 2), (1, 2 * t))
```

```exercise
? What is the second tangent component at t=3?
___
= 6
```

```quiz
? Which vector is tangent at t=0?
* (1, 0)
- (0, 1)
- (0, 0)
> At zero the horizontal derivative is one and the vertical derivative is zero.
```

# @lesson differential-geometry-arc-length
title: Speed and arc length
summary: Speed along a curve is the norm of its derivative.
---
Speed along a curve is the norm of its derivative. Arc length integrates speed. For `r(t)=(R cos t,R sin t)` the derivative has constant norm R, so an arc subtending θ radians has length Rθ.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
from math import pi

radius = 3
print(round(radius * pi / 2, 3))
```

```exercise
? What is the arc length for 2 radians and radius 5?
___
= 10
```

```quiz
? Which quantity is integrated to find arc length?
- The horizontal coordinate
* The norm of the derivative
- The tangent angle alone
> Integrating speed accumulates small distances along the curve.
```

# @lesson differential-geometry-curvature
title: Project: compare curvature on a parabola
summary: For a graph `y=f(x)`, curvature magnitude is `|f″(x)|/(1+f′(x)²)^(3/2)`.
---
For a graph `y=f(x)`, curvature magnitude is `|f″(x)|/(1+f′(x)²)^(3/2)`. On `y=x²` the numerator stays 2 while the denominator grows away from zero. Compare the vertex with two points farther away.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
for x in (0, 1, 2):
    curvature = 2 / (1 + (2 * x) ** 2) ** 1.5
    print(x, round(curvature, 3))
```

```exercise
? What is the curvature of y=x² at x=0?
___
= 2
```

```quiz
? Which sampled point has the largest curvature?
- x=1
- x=2
* x=0
> The denominator is smallest at x=0.
```
