# @lesson marketing-retention-lab-case
title: More learners started and fewer returned
summary: Test two decisions to improve return after lesson one.
---
Python lesson-one starters increased from 18 to 24, but seven-day returns fell from 11 to eight. Here a return means opening a subsequent lesson in a later visit within seven days of starting. Each cohort has a full, equal follow-up window.

Select **Run**. Choose among highlighting the next exercise, a targeted reminder to inactive starters, and a general newsletter. Write the evidence and your prediction before each round. The first change remains in effect in round two. Messages are simulated and sent only to eligible subscribers in the scenario.

```try html decision-lab
<script>document.documentElement.lang = "en"; document.documentElement.dataset.scenario = "retention";</script>
```

```quiz
? What is the baseline return rate?
- About 46%
* About 33%
- About 61%
> Eight out of 24 starters returned within the week.
```

# @lesson marketing-retention-lab-memo
title: Write the retention decision memo
summary: Compare return and cost, then define a follow-up test.
---
Copy the lab draft and compare its results with the baseline. Report returns, returns per starter, and follow-up cost per starter. Explain each decision’s tradeoff and what might differ in a real campaign. The figures are synthetic, with fixed effects for each decision.

Propose a randomized test of a targeted reminder for people who have not returned by day two, measuring return within seven days of initial start. Define eligibility and include unsubscribes as a guardrail before rollout. Review [[email-retention-en/email-retention-project|the email and retention project]] or [[marketing-decision-lab-en/marketing-decision-lab-campaign|the signup and lesson-start case]].

```quiz
? Which denominator measures return in this lab?
* Everyone in the cohort who started lesson one
- Everyone who opened the email
- Only those who returned
> The denominator is the cohort of lesson starters with a complete observation window.
```
