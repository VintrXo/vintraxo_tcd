# @lesson product-launch-offer
title: From audience to offer
summary: For the Python case, our first test audience is operations staff with a recurring report.
---
For the Python case, our first test audience is operations staff with a recurring report. An offer combines the promised outcome, what the learner gets, access, and any price. In this exercise the first example is free. Compare two follow-up offers: self-paced learning or a course with a review session. Each has different costs and delivery capacity.

## Apply it to the Python launch

Write a card for each offer with the first-lesson outcome, what is included, and one assumption to check before offering it.

```quiz
? What is the first useful evidence for offer fit?
* A learner in the segment runs the example and explains how it fits a report
- A headline with more words
- A higher signup price alone
> That action links the offer to the real task.
```

# @lesson product-launch-pricing
title: Pricing and contribution margin
summary: Start with the pricing objective, then compare customer value, alternatives, and costs.
---
Start with the pricing objective, then compare customer value, alternatives, and costs. In this exercise a paid signup costs the learner 30 units, with variable cost of 12. Contribution is 18 per signup before fixed cost. A setup cost of 180 breaks even at ten paid signups, assuming stable price and cost and no refunds.

## Apply it to the Python launch

Try a second price and recalculate break-even. Explain why a lower break-even quantity at a higher price is insufficient evidence without considering demand.

```try python
from math import ceil

fixed_cost, variable_cost = 180, 12
for price in (24, 30, 36):
    contribution = price - variable_cost
    print(price, contribution, ceil(fixed_cost / contribution))
```

```quiz
? How many paid signups cover fixed costs here?
- 6
* 10
- 15
> Contribution is 30−12=18, so 180÷18 gives ten.
```

# @lesson product-launch-pilot
title: Pilot launch and readiness
summary: A pilot tests the experience at small scale.
---
A pilot tests the experience at small scale. Define who is invited, the window, and how many signups you can support. Walk through signup and the first runnable example before launch. Give each action an owner and date. If an essential step fails, fix it and repeat the check before widening the invitation.

## Apply it to the Python launch

Write three tasks with an owner and deadline: page review, signup test, and delivery of the start email. Specify what to do if enrollment succeeds but no lesson link appears.

```quiz
? What should prevent immediate expansion of the pilot?
- A headline is one word longer
- The pilot list is smaller than the market
* Signup succeeds but the first lesson link is broken
> The lesson link is required to deliver the promised experience.
```

# @lesson product-launch-review
title: Read post-launch metrics
summary: Define metrics before the pilot.
---
Define metrics before the pilot. Our synthetic targets are at least 15 completed signups and at least 60% of signups starting the first lesson within seven days. After the observation window, we have 20 signups and 11 starts. Inspect the post-signup gap before changing the acquisition channel.

## Apply it to the Python launch

Calculate the start rate and write one diagnostic question about the email or lesson link. Keep the denominator and window fixed in the follow-up.

```quiz
? Which target was met?
* Signups only
- Lesson starts only
- Both
> Twenty clears 15, but 11÷20 is 55%, below 60%.
```

# @lesson product-launch-project
title: Project: a one-page launch plan
summary: Combine the offer brief, pricing assumptions, one channel, pilot tasks, and signup and start metrics.
---
Combine the offer brief, pricing assumptions, one channel, pilot tasks, and signup and start metrics. Use the synthetic results to make an explicit decision. For example, keep the current channel for a limited round and test a direct link to the first example in the welcome email before expanding.

## Apply it to the Python launch

Deliver one page with the decision, task owners, review date, and metric thresholds. Give a numeric reason for the next step and state what evidence would change your decision.

```quiz
? What is a suitable next step after the synthetic pilot?
- Increase spend before checking lesson starts
* Test easier access to the first example in a limited round
- Change price, audience, and channel simultaneously
> Lesson starts missed their target; a focused pilot addresses the observed step.
```

# @lesson product-launch-sources
title: References and related courses
summary: Review the sources for offers, pricing, and launch plans.
type: Reference
---
- [Structure of a marketing plan](https://openstax.org/books/principles-marketing/pages/2-3-purpose-and-structure-of-the-marketing-plan)
- [Product development and launch](https://openstax.org/books/principles-marketing/pages/10-2-stages-of-the-new-product-development-process)
- [Establishing pricing policy](https://openstax.org/books/principles-marketing/pages/12-3-the-five-step-procedure-for-establishing-pricing-policy)

- [[brand-messaging-en/brand-messaging-project|The brand messaging project]]
- [[marketing-experiments-en/marketing-experiments-project|The experiment decision memo]]

Campaign figures and offers are synthetic practice material.

Continue with the [[marketing-capstone-en/marketing-capstone-brief|marketing capstone]] to assemble the plan and evaluate the launch targets.
