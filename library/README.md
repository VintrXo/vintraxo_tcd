# Programming library (مكتبة البرمجة)

Original courses in the style of W3Schools-type tutorials, written for this platform in Arabic and English.
The text is ours (not copied from any site), so it belongs to the platform owner.

Load or update on a site:

```bash
bench --site <site> execute vintraxo_tcd.core.library.load_library                       # all courses
bench --site <site> execute vintraxo_tcd.core.library.load_library --kwargs "{'only': ['html']}"
```

A new course becomes two spaces (`<key>-ar`, `<key>-en`) with a menu per chapter, a quiz per lesson that has
questions, and one course with a certificate. Running it again on an existing space refreshes the pages' text only
(learners keep their progress; each change is a new version in the page history).

## Writing a course

`library/<key>/course.json` (spaces, course title, chapters with lesson slugs) and one file per language, `ar.md` and
`en.md`, with the same lesson slugs. Each lesson:

````
# @lesson html-links
title: الروابط
summary: one line shown in lists
type: Lesson            (or Reference)
---
Markdown text: **bold**, `code`, lists, tables, ## headings.

```try html                 "try it yourself" (html, javascript, python, sql)
```try sql shop             ... with hidden setup code "shop" from course.json:
                            "setups": {"shop": {"ar": "@shop_ar.sql", "en": "@shop_en.sql"}}
<a href="#">رابط</a>
```

```exercise html            fill the blanks: ? prompt, code with ___, = answer per blank, ! hint
? أكمل السمة
<a ___="page.html">صفحة</a>
= href
! السمة التي تحدد العنوان
```

```reference html           name | description | example, one per line (searchable table; use " | " with spaces)
<a> | رابط | <a href="x">نص</a>
```

:::tip عنوان الملاحظة       info / tip / warning / danger
النص
:::

```quiz                     ? question, - wrong, * right (several * = multiple choice), = true/false, > explanation
? أي سمة تفتح الرابط في تبويب جديد؟
- href
* target="_blank"
```
````

Tips:
- Write tags in prose inside backticks (`` `<p>` ``), never bare.
- In Arabic questions, start with an Arabic word (not with code), so the line reads right to left.
