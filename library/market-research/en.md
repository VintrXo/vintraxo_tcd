# @lesson market-research-brief
title: The research question
summary: Name the decision before collecting data.
---
Name the decision before collecting data. Continuing the Python launch case, choose an audience for the first signup-page test. Ask about the last repetitive calculation someone faced and the method they used.

## Apply it to the Python course

Write one decision and one question about a real past experience.

```quiz
? Which question gathers behavioural evidence?
* How did you finish your last weekly report?
- You like Python, right?
- Would you like a blue logo?
> A past event reveals what the person actually did.
```

# @lesson market-research-sample
title: Research method and sample
summary: Desk research uses existing information, such as published offers.
---
Desk research uses existing information, such as published offers. Primary research gathers new evidence through methods such as interviews. Interviews help explore reasons; estimating their prevalence requires a sample that suits the target population.

## Apply it to the Python course

Review three alternatives and define recruitment criteria for two segments. If people all come from your own team, document that limitation.

```quiz
? Which method best explores reasons for hesitating to sign up?
- Count page colours
* Open interviews
- Read traffic counts alone
> Follow-up questions can reveal reasons traffic counts alone cannot show.
```

# @lesson market-research-interviews
title: Interviews and neutral questions
summary: Explain the interview purpose and obtain consent before recording.
---
Explain the interview purpose and obtain consent before recording. Ask about a real experience and use neutral follow-ups. Separate what the person said from your interpretation.

## Apply it to the Python course

Rewrite “A practical course would solve it, right?” Try “Tell me about the last time you tried to make report preparation faster. What happened next?”

```quiz
? Which follow-up is least leading?
- Time was definitely the problem?
- Why didn’t you choose our better course?
* What happened next?
> The first follow-up does not suggest a reason.
```

# @lesson market-research-journey
title: Alternatives and the decision journey
summary: Another Python course is a direct competitor; a spreadsheet template that does the job is an indirect substitute.
---
Another Python course is a direct competitor; a spreadsheet template that does the job is an indirect substitute. Map the journey from need through search, comparison, and trial. Note stopping points and repeated steps. The same person can follow different sequences in different situations.

## Apply it to the Python course

Compare a free video, spreadsheet template, and interactive course. For each, list a reason for choosing it and a barrier, identifying what you observed and what needs testing.

```quiz
? What is an indirect substitute for learning Python here?
* A template that automates the report steps
- Another Python course
- The signup page title
> The template satisfies the need by a different route.
```

# @lesson market-research-evidence
title: Summarise notes without overstating the sample
summary: Tag notes with themes such as time and alternatives.
---
Tag notes with themes such as time and alternatives. Count one person once even if they mention a barrier twice. State the sample size and look for counterexamples. Small interview samples can guide a next test; broader estimates require an appropriate sampling design.

## Apply it to the Python course

In the synthetic example, compare the count of time-barrier notes with the number of distinct people mentioning it. Write a one-sentence finding with the participant count.

```try python
notes = [('P1', 'time'), ('P1', 'time'), ('P2', 'template'), ('P3', 'time')]
people = {person for person, theme in notes if theme == 'time'}
print(len(people), sorted(people))
```

```quiz
? How many distinct people mentioned limited time?
- 3
* 2
- 4
> P1 mentioned it twice and P3 once, so the count is two.
```

# @lesson market-research-project
title: Project: choose the first audience to test
summary: In the synthetic case, two operations workers described recurring reports and a third was satisfied with a template.
---
In the synthetic case, two operations workers described recurring reports and a third was satisfied with a template. Two students described general interest in Python without a current task. Compare the evidence and clarity of need, then pick a small test that gathers more evidence.

## Apply it to the Python course

Write a memo with the decision, participants per segment, supporting and contrary evidence, one limitation, and a test metric. For example, show operations staff a page with a reporting exercise and measure the share who start it. One participant is satisfied with a template, and the sample is small.

```quiz
? Which conclusion does the synthetic evidence support?
- All operations staff will sign up
- Students never need Python
* Operations staff are a reasonable first test audience
> The observations support a test decision; generalizing to either population needs more evidence.
```

# @lesson market-research-sources
title: References and further reading
summary: Sources for research, customer decisions, and interviews.
type: Reference
---
- [Marketing research plan](https://openstax.org/books/principles-marketing/pages/6-3-steps-in-a-successful-marketing-research-plan)
- [Consumer decision process](https://openstax.org/books/principles-marketing/pages/3-3-the-consumer-purchasing-decision-process)
- [Using in-depth interviews](https://www.gov.uk/service-manual/user-research/using-in-depth-interviews)
- [Analysing a research session](https://www.gov.uk/service-manual/user-research/analyse-a-research-session)

Continue the case from [[marketing-foundations-en/marketing-foundations-project|Marketing foundations]].

The examples and interview notes were written for practice and use synthetic data.

Continue with [[content-seo-en/content-seo-intent|Content marketing and search]].
