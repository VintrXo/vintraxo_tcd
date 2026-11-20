# @lesson email-retention-permission
title: Subscription and recipient expectations
summary: Tell recipients what to expect, retain the subscription record, and provide a clear way to stop marketing emails.
---
Tell recipients what to expect, retain the subscription record, and provide a clear way to stop marketing emails. In this practice sequence, send follow-ups to subscribed recipients and exclude anyone who unsubscribes from later sends.

## Apply it to the Python launch

Draft signup copy describing what subscribers will receive and whether it is a two-email sequence or an ongoing newsletter. Add clear unsubscribe wording.

```quiz
? What should the practice sequence do after an unsubscribe?
* Exclude the recipient from later sends
- Change only the subject line
- Send more reminders
> Subscription status should govern eligibility for follow-up.
```

# @lesson email-retention-welcome
title: A welcome email with one action
summary: Tie the welcome email to the promise that brought learners in.
---
Tie the welcome email to the promise that brought learners in. If they enrolled to try a Python calculation, link directly to the first example. Use a descriptive subject and make the next step easy to identify.

## Apply it to the Python launch

Write a subject, two sentences, and one link. An example subject is “Try your first calculation in Python”, with a link to the relevant lesson.

```quiz
? Which action best matches the welcome message?
- Follow us on every channel
* Try the first example
- Read every lesson now
> One small action fulfils the promise that motivated signup.
```

# @lesson email-retention-segments
title: Follow up based on course activity
summary: Segment subscribers by a clear action.
---
Segment subscribers by a clear action. Someone who has not started can use a direct start link. Someone who started may need the next exercise. Set a review time and an exit rule so a reminder does not go to people who already completed its action.

## Apply it to the Python launch

Outline two branches: started or not started. Exclude anyone unsubscribed and decide what each eligible group should receive.

```quiz
? What signal fits a message with the next exercise?
- The signup page colour
- Number of ad impressions
* An actual first lesson start
> An activity event ties the message to the learner’s current stage.
```

# @lesson email-retention-metrics
title: Measure clicks and seven-day return
summary: For this exercise, click rate is unique clickers divided by delivered emails.
---
For this exercise, click rate is unique clickers divided by delivered emails. Measure seven-day return for a signup cohort only after every member has a full window. Automatic image loads can inflate opens, so compare with on-site activity.

## Apply it to the Python launch

Of 90 deliveries, 18 people clicked. Separately, 25 of 100 cohort members returned in seven days. Calculate both rates using their distinct denominators.

```try python
print(f"{18 / 90:.0%}", f"{25 / 100:.0%}")
```

```quiz
? What is the seven-day return rate?
* 25%
- 20%
- 18%
> Return uses the 100 signups; clicks use the 90 deliveries.
```

# @lesson email-retention-project
title: Project: design a welcome and retention sequence
summary: Design a welcome email after subscription, then a conditional follow-up based on whether the first lesson was started.
---
Design a welcome email after subscription, then a conditional follow-up based on whether the first lesson was started. Record seven-day return and a friction signal such as unsubscribes. Fix the observation window before comparing groups.

## Apply it to the Python launch

Deliver two emails, timing and exit rules, a success measure, and an unsubscribe measure. Example decision: test a direct link to the exercise and compare seven-day return for cohorts with equal observation windows.

```quiz
? When is comparing cohort return appropriate?
- As soon as just one group starts
* After both groups have a full, equal observation window
- After removing anyone who did not return
> Equal observation windows give both groups the same opportunity to return.
```

# @lesson email-retention-sources
title: References and related courses
summary: References for the lessons and links to the launch case.
type: Reference
---
- [Mailchimp open and click rates](https://mailchimp.com/help/about-open-and-click-rates/)
- [Apple Mail Privacy Protection and reporting](https://mailchimp.com/help/apple-privacy-faq/)
- [OpenStax marketing metrics](https://openstax.org/books/principles-marketing/pages/2-4-marketing-plan-progress-using-metrics)

Continue the case from [[paid-campaigns-en/paid-campaigns-project|Advertising and performance measurement]].

The campaign examples and data are synthetic and written for this course.

Continue with [[marketing-experiments-en/marketing-experiments-funnel|Marketing analytics and A/B experiments]] to turn campaign results into a testable decision.
