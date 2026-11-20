# @lesson marketing-decision-lab-campaign
title: Signups rose, but lesson starts fell
summary: Examine the campaign metrics and test two decisions over two rounds.
---
You manage the Python course campaign. Signups went from 18 to 26, but first-lesson starts within seven days fell from 12 to nine. You can change the welcome link, name the reporting task in the ad, or increase the current ad’s budget.

Select **Run** to open the lab. Before each round, choose one change and describe the evidence behind your hypothesis and the metric you expect to move. The first change remains in effect during round two. Copy your memo draft before restarting the example.

```try html decision-lab
<script>document.documentElement.lang = "en";</script>
```

:::info Simulation data
The figures are synthetic and the model assigns a fixed effect to each change. Use it to compare tradeoffs and explain how you would verify an effect in a real campaign.
:::

```quiz
? Which metric first describes the problem occurring after signup?
- Ad impressions
* The share of signups starting lesson one within seven days
- The number of ad campaigns
> The start rate shows whether new signups reached the action the campaign promised.
```

# @lesson marketing-decision-lab-memo
title: Write a one-page decision memo
summary: Document evidence, tradeoffs, and a follow-up test.
---
Finish the draft from the lab as a recommendation for the campaign team. Compare the baseline and both rounds, identifying the targets met and missed. Choose one follow-up test and explain which result would change your decision.

## Check the memo before sharing

- **Evidence:** Name a specific observation from the ad, course page, or welcome email.
- **Calculation:** Divide starts by signups for the start rate and spend by signups for cost per signup.
- **Tradeoff:** Explain what improved and what worsened, even if the overall number rose.
- **Verification:** Propose a test with one change, a metric, and an observation window.

Give yourself one point for each completed criterion. Example verification test: randomly assign new signups to either the library index or the first example link, then compare lesson starts within seven days using the same counting rule.

Review [[marketing-capstone-en/marketing-capstone-scorecard|the campaign scorecard]] or [[marketing-experiments-en/marketing-experiments-design|A/B experiment design]] for the measurement steps.

Continue with the [[marketing-retention-lab-en/marketing-retention-lab-case|learner retention lab]] to test decisions after lesson one begins.

```quiz
? If signups increase after raising spend but the start rate falls, what belongs in the memo?
* Report both the signup increase and the decline in start rate
- The campaign met every target
- Spend alone proved what caused the drop
> Signup volume and start rate measure different outcomes and should both be evaluated.
```
