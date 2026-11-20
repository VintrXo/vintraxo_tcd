# @lesson marketing-capstone-brief
title: Launch brief and targets
summary: Plan a practice launch of the Python course for operations staff who repeatedly prepare reports.
---
Plan a practice launch of the Python course for operations staff who repeatedly prepare reports. Offer an initial browser-based calculation. Set signup, quality, and cost targets before opening the data. Evaluate each round after every eligible signup has had its full seven-day follow-up window.

## Project task

Write your decision, target segment, and testable assumption. Use three practice targets: at least 15 completed signups, at least 60% of signups starting lesson one, and at most 4 cost units per signup. Count each eligible account completing signup once per round.

```quiz
? What is the lesson-start metric in this project?
* Signups starting within seven days divided by completed signups
- Clicks divided by impressions
- Spend divided by signups
> The denominator is signups with the same full observation window.
```

# @lesson marketing-capstone-package
title: Assemble the offer, messaging, and channels
summary: Link a research finding to the ad promise, a proof point on the signup page, and an action in the welcome email.
---
Link a research finding to the ad promise, a proof point on the signup page, and an action in the welcome email. For example, the ad invites a simple sum, the page shows the example, and the email links directly to lesson one. Assign each task an owner and review time, then check signup and the link before sending invitations.

## Project task

Prepare an offer brief, landing headline and proof point, one ad, a welcome email, and a practice tagged link. Set a synthetic budget per round. Specify what to do if signup works but the example link fails.

```quiz
? Which issue should stop the rollout from expanding?
- The email is shorter than the ad
* The first-lesson link fails after signup
- All channels carry the same offer
> Lesson one delivers the promise, so fix the link and retest the journey.
```

# @lesson marketing-capstone-scorecard
title: Score two rounds on fixed definitions
summary: In synthetic data, round one has 20 signups, 11 lesson starts, and spend of 60.
---
In synthetic data, round one has 20 signups, 11 lesson starts, and spend of 60. In round two the welcome link goes directly to the example; there are 24 signups, 16 starts, and spend of 84. Calculate start rate and cost per signup. The channel and metric definitions stayed fixed, but the rounds happened at different times.

## Project task

Count target hits in each round before running the example. Explain the difference between observing an improvement and showing that the link caused it.

```try python
rounds = [('Round 1', 20, 11, 60), ('Round 2', 24, 16, 84)]
for label, signups, starts, spend in rounds:
    start_rate = starts / signups
    cost_per_signup = spend / signups
    targets = [signups >= 15, start_rate >= 0.60, cost_per_signup <= 4]
    print(f"{label}: {signups} signups, {start_rate:.1%} starts, "
          f"{cost_per_signup:.2f} per signup, {sum(targets)}/3 targets")
```

```quiz
? Which round met all three targets?
- Round one only
- Both rounds
* Round two only
> Round one meets signup and cost targets but 11÷20 is 55%. Round two records 24 signups, about 66.7% starts, and cost of 3.5.
```

# @lesson marketing-capstone-memo
title: Project: submit the decision memo
summary: Deliver the launch plan and a one-page decision memo.
---
Deliver the launch plan and a one-page decision memo. Example: “Round two meets all three practice targets. Run a randomized comparison of two welcome links and measure starts within seven days before deciding on rollout.” Explain how timing or audience changes could affect a before-after comparison.

## Project task

Score your submission on four equal criteria: evidence for audience choice, consistent promise across assets, correct calculations and denominators, and a decision stating evidence limits and a verification step. Award one point per completed criterion and explain how you would fix any gap.

```quiz
? What do the synthetic results support?
* Round two met the targets; an experiment is needed to attribute the difference to the link
- The link’s causal effect is proven by this comparison alone
- Every future campaign will achieve the same result
> Target attainment is measurable; attributing the change requires a stronger design.
```

# @lesson marketing-capstone-guide
title: Marketing project map
summary: Revisit the eight practice projects feeding the capstone.
type: Reference
---
- [[marketing-foundations-en/marketing-foundations-project|Marketing foundations]]
- [[market-research-en/market-research-project|Market research]]
- [[content-seo-en/content-seo-project|Content and search]]
- [[paid-campaigns-en/paid-campaigns-project|Advertising and measurement]]
- [[email-retention-en/email-retention-project|Email and retention]]
- [[marketing-experiments-en/marketing-experiments-project|Analytics and A/B experiments]]
- [[brand-messaging-en/brand-messaging-project|Brand and messaging]]
- [[product-launch-en/product-launch-project|Product marketing and launch]]

Return to [[marketing-capstone-en/marketing-capstone-memo|the final decision memo]].

The case and results are synthetic. The linked courses list their references for research, messaging, launch, and measurement.

Continue with the [[marketing-decision-lab-en/marketing-decision-lab-campaign|marketing decision lab]] to test two decisions after campaign performance changes.
