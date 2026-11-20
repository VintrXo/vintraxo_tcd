# @lesson paid-campaigns-objective
title: Objectives and conversions
summary: Name the success event before setting up a campaign.
---
Name the success event before setting up a campaign. In the Python case it is a completed signup. Document whose signups count, when the event fires, and how repeat events are handled in the exercise report.

## Apply it to the Python launch

Write a conversion definition with a time window and a way to deduplicate people. Choose one diagnostic intermediate event.

```quiz
? What is the final conversion in this case?
* Completed signup
- An impression
- A page visit alone
> Impressions and visits are intermediate steps; signup is the stated goal.
```

# @lesson paid-campaigns-budget
title: Budget a fair comparison
summary: Set a practice budget and allocate it according to the question.
---
Set a practice budget and allocate it according to the question. To compare two headlines for the same audience, hold the landing page and conversion definition fixed. Record allocation and dates upfront. A small difference in a limited sample is tentative.

## Apply it to the Python launch

Allocate 160 units between two variants and state what will vary and what is held constant.

```quiz
? In a headline test, what should vary initially?
- Headline, price, and audience together
* Only the headline
- The signup definition between variants
> Isolating the change helps interpret differences.
```

# @lesson paid-campaigns-metrics
title: Clicks, conversions, and cost
summary: This exercise measures clicks per impression, conversions per click, and spend per conversion.
---
This exercise measures clicks per impression, conversions per click, and spend per conversion. Keep the time window and conversion definition fixed. An ad platform may divide by all eligible interactions; this exercise explicitly uses clicks only.

## Apply it to the Python launch

With 5,000 impressions, 200 clicks, ten signups, and 80 units spent, compute all three metrics. With no signups, the sample cost per signup is undefined.

```try python
impressions, clicks, signups, spend = 5000, 200, 10, 80
print(f"{clicks / impressions:.0%}", f"{signups / clicks:.0%}", spend / signups)
```

```quiz
? What is the cost per signup?
- 0.4
- 10
* 8
> Divide 80 spend units by ten signups.
```

# @lesson paid-campaigns-attribution
title: Attribution and how to read discrepancies
summary: Attribution credits a channel or touchpoint under a rule and time window.
---
Attribution credits a channel or touchpoint under a rule and time window. Platform and course counts can differ because of definitions, timing, or duplicates. Compare both reports using the same event and period before interpreting the gap. Attribution alone does not establish causal impact.

## Apply it to the Python launch

If the ad report lists 12 signups and the course log lists ten, write two checks. For example, are the windows identical, and do both count unique completed signups?

```quiz
? What comes first when interpreting the discrepancy?
* Check event definition and time window
- Add the two counts
- Immediately accept the larger number
> The definition and period determine what each count includes.
```

# @lesson paid-campaigns-project
title: Project: decide the campaign’s next step
summary: Two synthetic variants: A spent 80 and got ten signups; B spent 80 and got 16.
---
Two synthetic variants: A spent 80 and got ten signups; B spent 80 and got 16. Calculate signup costs and compare them against a six-unit ceiling. Decide whether to repeat before increasing spend, particularly with small counts.

## Apply it to the Python launch

Write a four-point report: objective, each cost, what the figures suggest, and the follow-up test. Include a post-signup quality metric such as starting the first lesson.

```quiz
? Which variant is below the ceiling of six in the exercise?
- Only A
* Only B
- Both
> A costs eight and B costs five. This result describes the synthetic test.
```

# @lesson paid-campaigns-sources
title: References and related courses
summary: References for the lessons and links to the launch case.
type: Reference
---
- [Google Ads conversion rate](https://support.google.com/google-ads/answer/2684489?hl=en)
- [Understand conversion tracking data](https://support.google.com/google-ads/answer/6270625?hl=en)
- [Campaign URL parameters](https://support.google.com/analytics/answer/10917952?hl=en)

Continue the case from [[content-seo-en/content-seo-project|Content marketing and search]].

The campaign examples and data are synthetic and written for this course.

Continue with [[email-retention-en/email-retention-permission|Email marketing and retention]].
