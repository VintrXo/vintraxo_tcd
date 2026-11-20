# @lesson marketing-experiments-funnel
title: Measure the signup funnel
summary: Compare ordered stages for the same visitors in a fixed window: landing on the course page, starting signup, and finishing.
---
Compare ordered stages for the same visitors in a fixed window: landing on the course page, starting signup, and finishing. A step rate uses the previous stage as its denominator; overall conversion uses all initial visitors. Define the counting unit before analysis so repeat visits do not get mixed with people.

## Apply it to the Python launch

Of 500 unique visitors, 100 began signup and 40 completed it. Calculate each step rate and overall conversion. Suggest what to inspect in the form if many people start and fail to finish.

```try python
visitors, started, completed = 500, 100, 40
print(f"{started / visitors:.0%}", f"{completed / started:.0%}", f"{completed / visitors:.0%}")
```

```quiz
? What is the completion rate among people who started signup?
* 40%
- 8%
- 20%
> 40 ÷ 100 measures completion; 40 ÷ 500 measures overall conversion.
```

# @lesson marketing-experiments-design
title: Design an A/B experiment
summary: To test a signup headline, show the existing A and proposed B to the same audience during the same period.
---
To test a signup headline, show the existing A and proposed B to the same audience during the same period. Randomly assign visitors and keep each visitor in their assigned variant on later visits. Before starting, specify allocation, a primary metric, the smallest effect that matters, sample size, and measurement window.

## Apply it to the Python launch

State a hypothesis, designate signups per assigned visitor as primary and first-lesson starts per assigned visitor as a guardrail. Write an ending rule in advance so the first favourable fluctuation does not decide when the test ends.

```quiz
? What is the unit of random assignment in the project?
- Each page load
* The visitor, who keeps the same variant
- Only completed signups
> Stable visitor assignment avoids exposing the same person to both experiences.
```

# @lesson marketing-experiments-quality
title: Check allocation and measurement
summary: Before interpreting a conversion gap, compare observed visitor counts with the planned allocation.
---
Before interpreting a conversion gap, compare observed visitor counts with the planned allocation. A 50/50 test of 2,000 visitors expects roughly 1,000 per arm. A large discrepancy may indicate assignment, logging, or exclusion issues. Use a sample-ratio diagnostic to flag discrepancies for investigation.

## Apply it to the Python launch

If the report has 1,200 in A and 800 in B, check whether repeat visitors were deduplicated consistently and whether assignment was logged before rendering either variant. Treat this as a quality check and inspect logs before trusting the experimental outcome.

```quiz
? What is the first step when allocation differs greatly from the plan?
- Immediately choose the larger arm
- Divide signups by the other arm’s signup count
* Investigate allocation and measurement
> Unexpected allocation can expose a fault before estimating the headline’s effect.
```

# @lesson marketing-experiments-lift
title: Conversion lift and uncertainty
summary: In this exercise A records 80 of 1,000 signups and B records 100 of 1,000.
---
In this exercise A records 80 of 1,000 signups and B records 100 of 1,000. The absolute difference is two percentage points, or 25% relative to A. The example computes an approximate 95% interval for the difference under independent visitor outcomes and sufficiently many successes and failures. If the interval includes zero, the direction is unresolved at that level.

## Apply it to the Python launch

Report both rates, both group sizes, and absolute and relative lift. After running the example, explain why a rollout decision needs more than a point estimate.

```try python
from math import sqrt

a, b = 80 / 1000, 100 / 1000
difference = b - a
margin = 1.96 * sqrt(a * (1 - a) / 1000 + b * (1 - b) / 1000)
print(f"{100 * difference:.1f} pp, {difference / a:.0%}")
print(f"{100 * (difference - margin):.2f} to {100 * (difference + margin):.2f} pp")
```

```quiz
? What is the absolute difference between 8% and 10%?
* Two percentage points
- 25 percentage points
- 0.2 percentage points
> 10% minus 8% is two points. 25% is the relative change against A.
```

# @lesson marketing-experiments-project
title: Project: write a Python launch decision memo
summary: Prepare a decision memo for the synthetic test: what changed, who was assigned, and the primary metric.
---
Prepare a decision memo for the synthetic test: what changed, who was assigned, and the primary metric. Use 80 and 100 signups in two arms of 1,000. If 56 visitors in A and 54 in B start the first lesson, report that guardrail using everyone assigned in each arm and choose the next action.

## Apply it to the Python launch

Deliver one page with the hypothesis, quality check, signup estimate and interval, first-lesson starts, and decision. Example: “Signups rose in the estimate, but the interval spans zero and lesson starts did not improve. Review post-signup activity and retest a specific headline before rollout.”

```quiz
? Which decision fits the synthetic results?
- Roll out B based on signups alone
* Review lesson starts before rollout
- Declare that the headline cannot have any effect
> Use the guardrail and uncertainty alongside the conversion estimate before rollout.
```

# @lesson marketing-experiments-sources
title: References and related courses
summary: Read the measurement references and revisit earlier campaign work.
type: Reference
---
- [Marketing metrics and KPIs](https://openstax.org/books/principles-marketing/pages/2-4-marketing-plan-progress-using-metrics)
- [Funnel exploration](https://support.google.com/analytics/answer/9355964?hl=en)
- [Diagnosing sample ratio mismatch](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- [Pitfalls in experiment metric interpretation](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)

- [[email-retention-en/email-retention-project|The welcome and retention project]]
- [[paid-campaigns-en/paid-campaigns-project|The advertising and measurement project]]

The exercises and figures are synthetic and written for this course.

Continue with [[brand-messaging-en/brand-messaging-promise|Brand strategy and marketing messaging]] to develop the promise you want to test across channels.
