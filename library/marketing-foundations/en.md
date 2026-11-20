# @lesson marketing-foundations-value
title: Marketing starts with a need
summary: Define the problem and desired outcome before choosing a channel.
---
Marketing starts by understanding who has a problem, shaping an offer they value, and communicating it clearly. Our project promotes the library’s Python course. The working assumption is that some office workers repeat spreadsheet calculations and want a step-by-step way to learn.

## Apply it to the Python course

Write one sentence in the learner’s voice: “I add the same numbers by hand every week, and I don’t know where to start with programming.” Then name an outcome learners can observe after the first lesson. Mark any assumptions you still need to check.

```quiz
? What is the first decision in this case?
* Identify the problem and audience
- Choose the advertisement colour
- Increase the budget
> The need shapes the offer and informs how to reach people.
```

# @lesson marketing-foundations-segment
title: Segmentation and targeting
summary: Turn a broad audience into a testable segment.
---
Segmentation groups people by a shared need or behaviour. Targeting chooses whom to serve first. Compare workers seeking to reduce manual calculations with students exploring programming more broadly. Consider clarity of need, reachability, and whether the current lessons fit.

## Apply it to the Python course

Choose one segment and identify where you could speak to people in it. Ask when they last did the calculations manually, how long it took, and what alternative they used. Use the answers to refine the hypothesis.

```quiz
? Which segment is more specific for a first test?
- Everyone who uses the internet
* Operations staff who repeat weekly calculations
- Anyone who likes technology
> The first segment has an observable behaviour linked to the offer.
```

# @lesson marketing-foundations-positioning
title: Value proposition and positioning
summary: Tie a concrete benefit to an alternative the customer already uses.
---
A value proposition identifies who benefits and what outcome they can expect. Positioning frames the offer against an alternative. For people doing calculations manually, offer an introduction to Python in the browser, with an editable example to demonstrate it. Make claims a learner can verify in the lesson.

## Apply it to the Python course

Write a headline and one proof point. For example, “Start Python with a simple calculation in your browser,” followed by a sample that sums three values. Compare this with “Beginner Python course” and decide which better serves the segment.

```quiz
? What supports the claim that a learner can try a calculation immediately?
- A guaranteed result for every learner
- A large headline
* An editable browser example
> The example directly demonstrates the capability.
```

# @lesson marketing-foundations-mix
title: Marketing mix and channel choice
summary: Review product, price, place, and promotion together.
---
The marketing mix links product, price, place, and promotion. In our Python case the product is the learning experience, price is any fee charged, place is how learners access the course, and promotion could be a message in a professional newsletter the segment reads.

## Apply it to the Python course

Choose one channel for the test and explain why the audience uses it. Then describe what visitors can do after landing. Check that the page headline and call to action match the promise in the message.

```quiz
? Which element of the mix is the newsletter message?
* Promotion
- Price
- Product
> The newsletter communicates the offer and invites people to the page.
```

# @lesson marketing-foundations-measurement
title: Measuring signups and cost per signup
summary: Define conversion, tag links, and compare performance on explicit denominators.
---
Here a conversion is a completed signup. Signup rate is signups divided by landing-page visits for the same period and channel. Cost per signup is campaign spend divided by attributed signups. Use `utm_source` for the source, `utm_medium` for the channel type, and `utm_campaign` for the campaign. Keep naming consistent and personal data out of URLs.

## Apply it to the Python course

In the synthetic data, the newsletter brought 20 signups from 250 visits at a cost of 60 units. Calculate the rate and cost before running the example. If signups are zero, record cost per signup as undefined for the sample.

Sample tagged link: `https://example.com/python?utm_source=operations_newsletter&utm_medium=email&utm_campaign=python_launch`. Change the source if you try another newsletter, keeping the campaign name consistent.

```try python
visits = 250
signups = 20
spend = 60
print(f"{signups / visits:.1%}")
print(f"{spend / signups:.2f}")
```

```quiz
? What is the signup rate in the example?
- 12%
* 8%
- 30%
> Twenty divided by 250 is 0.08, or 8%.
```

# @lesson marketing-foundations-project
title: Project: a Python course launch plan
summary: Draft a page and small campaign, then decide what to do using synthetic data.
---
Write a one-page plan. State the segment, problem, and existing alternative. Draft a headline, proof point, and one call to sign up. Choose a channel and prepare a tagged link. Before reading results, set a hypothetical target: at least 15 signups at no more than 4 cost units each.

## Apply it to the Python course

Use the sample results: 20 signups for 60 cost units. Write a two-sentence decision: did the test meet its target, and what is the one change you would test next? Sample: “Signups exceeded the threshold at 3 units each. Next, I’ll test a clearer page headline on the same channel.”

- The segment is specific and the proof is available in the product.
- The promise and signup action are clear.
- The plan states the target, calculation, and decision.

```quiz
? Did the synthetic results meet the test target?
- No, the target was 25 signups
- No, each signup cost 6
* Yes, 20 signups at 3 each
> Twenty exceeds 15, and 60 divided by 20 is 3, below the ceiling of 4.
```

# @lesson marketing-foundations-sources
title: References and further reading
summary: Primary references for the course and the Python example.
type: Reference
---
## Marketing principles

- American Marketing Association — [AMA definition of marketing](https://www.ama.org/the-definition-of-marketing-what-is-marketing/)
- OpenStax — [The marketing process and value proposition](https://openstax.org/books/principles-marketing/pages/1-1-marketing-and-the-marketing-process)
- OpenStax — [Market segmentation](https://openstax.org/books/principles-marketing/pages/5-1-market-segmentation-and-consumer-markets)
- OpenStax — [Selecting target markets](https://openstax.org/books/principles-marketing/pages/5-5-selecting-target-markets)
- OpenStax — [Marketing plan and mix](https://openstax.org/books/principles-marketing/pages/2-3-purpose-and-structure-of-the-marketing-plan)

## Measuring the campaign

- [Google Analytics campaign tagging](https://support.google.com/analytics/answer/10917952?hl=en)

## Course used in the project

- [[python-en/py-intro|Introduction to Python]]

The launch case, copy, exercises, and example campaign figures were written for this course. The figures are synthetic.

Continue with [[market-research-en/market-research-brief|Market research and customer behaviour]] to test your audience assumptions before a campaign.
