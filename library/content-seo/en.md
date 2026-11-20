# @lesson content-seo-intent
title: Search intent
summary: A query hints at a task.
---
A query hints at a task. “Python example to add numbers” calls for a runnable explanation; “beginner Python course” calls for a syllabus, cost, and a way to start. Treat intent as a hypothesis and check it against query wording and the results.

## Apply it to the Python launch

Write two queries an operations worker might use. Propose a different page for each.

```quiz
? What best helps a person searching for a sum example?
* A short runnable example
- Only a course price
- A company history
> The example serves the task expressed in the query.
```

# @lesson content-seo-plan
title: Build a content plan
summary: Start with one repeated problem.
---
Start with one repeated problem. Build a practical tutorial and a course page showing the scope, linked with descriptive text. Give each piece an audience, a question it answers, proof of usefulness, and a review date.

## Apply it to the Python launch

Draft two plan entries: a column-summing tutorial and a course page. Name each page’s question before writing its title.

```quiz
? Which link text best describes the destination?
- Click here
* Try summing a column with Python
- Number 1
> The text gives readers a clear expectation of the destination.
```

# @lesson content-seo-landing
title: Landing pages and search visibility
summary: Use a descriptive page title and a matching main heading.
---
Use a descriptive page title and a matching main heading. Add proof, a clear signup action, and useful section headings. If public search visibility is a goal, check that the public landing page opens without login and can be reached by crawlable links. Discoverability does not guarantee indexing.

## Apply it to the Python launch

Draft a title, a simple calculation example, and a “Start the first lesson” action. Specify what happens after the click.

```quiz
? Which title best describes a number-summing tutorial?
- The best content on the internet
- Python Python Python
* Sum report numbers with Python
> The title describes the page and its benefit in natural language.
```

# @lesson content-seo-metrics
title: Measure the reader’s next step
summary: Choose a measure tied to the page’s goal.
---
Choose a measure tied to the page’s goal. For a free tutorial, measure example starts divided by tutorial visits. Track final signups separately to distinguish engagement with the example from enrolment.

## Apply it to the Python launch

If 30 of 150 visitors start the example, compute the rate. If nine sign up, compute signups per visit to the same page.

```try python
visits = 150
for count in (30, 9):
    print(f"{count / visits:.0%}")
```

```quiz
? What is the example-start rate?
* 20%
- 6%
- 30%
> 30 ÷ 150 = 0.20. The signup rate is separately 6%.
```

# @lesson content-seo-project
title: Project: plan content and draft a signup page
summary: Use the weekly report from the Python case.
---
Use the weekly report from the Python case. Produce one worked tutorial and a signup page with a short syllabus and first-lesson outcome. Connect them, choose one metric for each step in advance, and document both versions when testing a headline change.

## Apply it to the Python launch

Deliver two queries with their intents, two page drafts, the link text, and start and signup metrics. Name one change to try if many start the example but few proceed to the course.

```quiz
? Which single change best tests the transition to the course?
- Change channel, copy, and price together
* Test the course link wording while keeping the tutorial fixed
- Stop measuring
> One controlled change makes the result easier to interpret.
```

# @lesson content-seo-sources
title: References and related courses
summary: References for the lessons and links to the launch case.
type: Reference
---
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google Search Essentials](https://developers.google.com/search/docs/essentials)

Continue the case from [[market-research-en/market-research-project|Market research and customer behaviour]].

The campaign examples and data are synthetic and written for this course.

Continue with [[paid-campaigns-en/paid-campaigns-objective|Advertising and performance measurement]].
