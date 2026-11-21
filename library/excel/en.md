# @lesson excel-intro
title: Excel introduction
summary: Workbooks, sheets, cells and ranges, and entering data cleanly.
---
**Excel** (and similar tools such as Google Sheets and LibreOffice Calc) organises data in a grid. A file is a **workbook**; it contains **sheets**; each sheet is made of **cells** named by column letter and row number, such as `B3`.

| | A | B | C |
|---|---|---|---|
| **1** | Product | Price | Qty |
| **2** | Tea | 12.5 | 40 |
| **3** | Coffee | 20 | 25 |
| **4** | Cake | 35 | 10 |

- `B3` is the cell in column B, row 3: it holds `20`.
- `A2:C4` is a **range**: every cell from A2 to C4.
- `B:B` is the whole column B; `2:2` is the whole row 2.

:::tip Keep data tidy
One header row, one kind of value per column (numbers stay numbers, dates stay dates), no empty rows in the middle, and no merged cells inside data. Tidy data makes every formula, filter and pivot table easier.
:::

```exercise excel
? Write the range that covers the prices of all three products in the table
=SUM(___)
= B2:B4
```

```quiz
? What does the cell name C2 refer to?
* Column C, row 2
- Row C, column 2
- The second sheet

? A range such as A2:C4 includes every cell between A2 and C4.
= true
```

# @lesson excel-formulas
title: Formulas and operators
summary: Starting with =, arithmetic, order of operations, and joining text.
---
Every formula starts with `=`. It can use numbers, cell references and operators, and it recalculates when the cells change.

| | A | B | C | D |
|---|---|---|---|---|
| **1** | Product | Price | Qty | Total |
| **2** | Tea | 12.5 | 40 | `=B2*C2` → **500** |
| **3** | Coffee | 20 | 25 | `=B3*C3` → **500** |

| Formula | Result | Why |
|---|---|---|
| `=2+3*4` | 14 | Multiplication before addition |
| `=(2+3)*4` | 20 | Brackets first |
| `=10/4` | 2.5 | Division |
| `=2^3` | 8 | Power |
| `=A2&" x "&C2` | Tea x 40 | `&` joins text |
| `=B2*(1+14%)` | 14.25 | Price with 14% tax |

:::tip Fill down instead of retyping
Write the formula once in `D2`, then drag the small square at the cell's corner down (or double-click it). Excel copies the formula and adjusts the row numbers: `=B3*C3`, `=B4*C4`...
:::

```exercise excel
? Calculate the total for row 4 (price times quantity)
=B4___C4
= *
```

```quiz
? What is the result of =2+3*4?
* 14
- 20
- 24

? Every Excel formula starts with an equals sign.
= true
```

# @lesson excel-references
title: Relative and absolute references
summary: What happens when formulas are copied, and when to use $.
---
When you copy a formula, Excel moves its references by the same distance. That is a **relative** reference (`B2`). Sometimes one cell must stay fixed, such as a tax rate: that is an **absolute** reference (`$F$1`).

| | A | B | C | ... | F |
|---|---|---|---|---|---|
| **1** | Product | Price | With tax | | **0.14** (tax rate) |
| **2** | Tea | 12.5 | `=B2*(1+$F$1)` → 14.25 | | |
| **3** | Coffee | 20 | `=B3*(1+$F$1)` → 22.8 | | |

If `C2` were `=B2*(1+F1)`, copying it down would give `=B3*(1+F2)`, and `F2` is empty, so the tax would disappear.

| Reference | When copied down | When copied right |
|---|---|---|
| `B2` | Row changes | Column changes |
| `$B$2` | Fixed | Fixed |
| `B$2` | Row fixed | Column changes |
| `$B2` | Row changes | Column fixed |

:::tip The F4 key
Click a reference inside the formula bar and press **F4** (on a Mac, Cmd+T) to cycle through `B2`, `$B$2`, `B$2`, `$B2`.
:::

```exercise excel
? Make the reference to the tax rate in F1 fixed when the formula is copied
=B2*(1+___)
= $F$1
```

```quiz
? Which reference stays exactly the same when a formula is copied anywhere?
* $F$1
- F1
- F$1
```

# @lesson excel-functions
title: Essential functions
summary: SUM, AVERAGE, MIN, MAX, COUNT, COUNTA, ROUND and the status bar.
---
**Functions** are ready-made formulas: a name, then arguments in brackets.

| | A | B |
|---|---|---|
| **1** | Employee | Sales |
| **2** | Sara | 1200 |
| **3** | Omar | 950 |
| **4** | Lina | (empty) |
| **5** | Karim | 1400 |

| Formula | Result | Meaning |
|---|---|---|
| `=SUM(B2:B5)` | 3550 | Total |
| `=AVERAGE(B2:B5)` | 1183.33 | Average of the numbers (empty cells ignored) |
| `=MIN(B2:B5)` / `=MAX(B2:B5)` | 950 / 1400 | Smallest / largest |
| `=COUNT(B2:B5)` | 3 | How many **numbers** |
| `=COUNTA(A2:A5)` | 4 | How many **non-empty** cells |
| `=COUNTBLANK(B2:B5)` | 1 | Empty cells |
| `=ROUND(AVERAGE(B2:B5), 0)` | 1183 | Round to 0 decimals |

:::tip Quick answers without formulas
Select a range and look at the **status bar** at the bottom of the window: Excel shows the sum, average and count of the selection.
:::

:::info Comma or semicolon?
In some regional settings Excel separates arguments with `;` instead of `,`, for example `=ROUND(B2;0)`. The function names stay in English in the Arabic version of Excel.
:::

```exercise excel
? Count how many cells in B2:B5 contain numbers
=___(B2:B5)
= COUNT
```

```quiz
? What is the difference between COUNT and COUNTA?
* COUNT counts numbers; COUNTA counts every non-empty cell
- They are the same
- COUNTA counts only text

? AVERAGE ignores empty cells.
= true
```

# @lesson excel-logic
title: Decisions with IF, AND and OR
summary: IF, nested conditions, IFS, AND, OR and handling errors with IFERROR.
---
| | A | B | C |
|---|---|---|---|
| **1** | Employee | Score | Result |
| **2** | Sara | 91 | `=IF(B2>=60,"Pass","Fail")` → Pass |
| **3** | Omar | 54 | → Fail |
| **4** | Lina | 75 | → Pass |

| Formula | Result for 91 | Meaning |
|---|---|---|
| `=IF(B2>=60,"Pass","Fail")` | Pass | One condition |
| `=IFS(B2>=90,"A",B2>=75,"B",B2>=60,"C",TRUE,"F")` | A | Several conditions in order |
| `=IF(AND(B2>=60,C2="Yes"),"Certified","Not yet")` | depends | Both must be true |
| `=IF(OR(B2>=90,D2="Manager"),"Fast track","Normal")` | Fast track | At least one must be true |
| `=IFERROR(B2/E2,0)` | 0 if E2 is empty | Replace an error with a value |

- Comparisons: `=`, `<>` (not equal), `>`, `<`, `>=`, `<=`.
- Text in formulas goes in double quotes: `"Pass"`.

:::warning Do not hide every error
`IFERROR` is useful for expected cases such as dividing by an empty cell. Wrapping everything in it can hide real mistakes, such as a wrong range.
:::

```exercise excel
? Show "High" when B2 is above 1000, otherwise "Normal"
=___(B2>1000,"High","Normal")
= IF
```

```quiz
? Which function returns a value instead of an error such as #DIV/0!?
* IFERROR
- IFS
- AND

? In Excel formulas, <> means "not equal to".
= true
```

# @lesson excel-conditional-sums
title: Conditional totals and counts
summary: SUMIF, SUMIFS, COUNTIF, COUNTIFS and AVERAGEIF on a sales table.
---
| | A | B | C | D |
|---|---|---|---|---|
| **1** | Date | Branch | Product | Amount |
| **2** | 2026-01-03 | Cairo | Laptop | 25000 |
| **3** | 2026-01-03 | Giza | Mouse | 450 |
| **4** | 2026-01-10 | Cairo | Monitor | 6000 |
| **5** | 2026-02-02 | Alex | Laptop | 24000 |
| **6** | 2026-02-15 | Cairo | Mouse | 500 |

| Formula | Result | Question |
|---|---|---|
| `=SUMIF(B2:B6,"Cairo",D2:D6)` | 31500 | Total sales in Cairo |
| `=COUNTIF(C2:C6,"Laptop")` | 2 | How many laptop sales |
| `=SUMIFS(D2:D6,B2:B6,"Cairo",D2:D6,">1000")` | 31000 | Cairo sales above 1000 |
| `=COUNTIFS(B2:B6,"Cairo",A2:A6,">="&DATE(2026,2,1))` | 1 | Cairo sales from February |
| `=AVERAGEIF(C2:C6,"Mouse",D2:D6)` | 475 | Average mouse sale |

- `SUMIF(range_to_check, condition, range_to_add)` has **one** condition.
- `SUMIFS(range_to_add, range1, condition1, range2, condition2, ...)` has **many**, and the sum range comes **first**.
- Conditions with operators go in quotes: `">1000"`. To use a cell value, join it: `">="&F1`.

```exercise excel
? Count the rows where column B is "Giza"
=___(B2:B6,"Giza")
= COUNTIF
```

```quiz
? In SUMIFS, which argument comes first?
* The range to add up
- The first condition
- The criteria range
```

# @lesson excel-lookup
title: Looking up values
summary: XLOOKUP, VLOOKUP and INDEX/MATCH to bring data from another table.
---
A **lookup** finds a value in one table and returns related information, for example the price of a product code.

**Products sheet**

| | A | B | C |
|---|---|---|---|
| **1** | Code | Product | Price |
| **2** | P01 | Laptop | 25000 |
| **3** | P02 | Monitor | 6000 |
| **4** | P03 | Mouse | 450 |

| Formula | Result | Notes |
|---|---|---|
| `=XLOOKUP("P02",A2:A4,C2:C4)` | 6000 | Modern: search column, return column |
| `=XLOOKUP("P09",A2:A4,C2:C4,"Not found")` | Not found | Built-in "if not found" |
| `=VLOOKUP("P02",A2:C4,3,FALSE)` | 6000 | Older: column number 3, `FALSE` = exact match |
| `=INDEX(C2:C4,MATCH("P02",A2:A4,0))` | 6000 | Works in every version, any direction |

:::warning Always use an exact match
In `VLOOKUP`, leaving out the last argument or writing `TRUE` means an **approximate** match, which silently returns wrong prices for unsorted codes. Always write `FALSE` (or use `XLOOKUP`, which is exact by default).
:::

:::tip XLOOKUP if you have it
`XLOOKUP` is available in Microsoft 365 and Excel 2021 and later, and in Google Sheets. It can look left, return several columns, and does not break when columns are inserted.
:::

```exercise excel
? Return the price for code P03 from the products table
=___("P03",A2:A4,C2:C4)
= XLOOKUP
```

```quiz
? What does FALSE mean as the last argument of VLOOKUP?
* Exact match only
- Search from the bottom
- Return the first column
```

# @lesson excel-text-dates
title: Text and date functions
summary: Cleaning and combining text, and calculating with dates.
---
| Formula | Result | Use |
|---|---|---|
| `=TRIM("  Sara   Ali ")` | Sara Ali | Remove extra spaces |
| `=PROPER("sara ali")` / `=UPPER(A2)` | Sara Ali / SARA ALI | Change case |
| `=LEFT("INV-2026-0042",3)` | INV | First characters |
| `=RIGHT("INV-2026-0042",4)` | 0042 | Last characters |
| `=TEXTJOIN(", ",TRUE,A2:A4)` | Tea, Coffee, Cake | Join a range with a separator |
| `=TEXT(1234.5,"#,##0.00")` | 1,234.50 | Format a number as text |
| `=TODAY()` | today's date | Changes every day |
| `=DATE(2026,3,1)` | 2026-03-01 | Build a date |
| `=B2-A2` | 45 | Days between two dates |
| `=NETWORKDAYS(A2,B2)` | working days | Excludes weekends |
| `=EDATE(A2,3)` | 3 months later | Contract end dates |
| `=TEXT(A2,"mmmm")` | the month's name | Group by month |

:::info Dates are numbers
Excel stores a date as a number of days, which is why you can subtract dates. If a "date" refuses to calculate, it is probably text: convert it with Data → Text to Columns, or `DATEVALUE`.
:::

:::tip Weekends outside Friday and Saturday?
`NETWORKDAYS.INTL(A2,B2,7)` treats Friday and Saturday as the weekend, as in Egypt and most Gulf countries.
:::

```exercise excel
? Remove the extra spaces from the name in A2
=___(A2)
= TRIM
```

```quiz
? Why can you subtract one date from another in Excel?
* Dates are stored as numbers of days
- Excel converts them to text first
- Only if both dates are in the same month
```

# @lesson excel-tables-filters
title: Tables, sorting, filtering and validation
summary: Excel Tables, sort and filter, data validation drop-downs, and conditional formatting.
---
Turning a range into an **Excel Table** (Ctrl+T, or Insert → Table) gives you filter buttons, banded rows, and formulas that grow automatically with new rows.

| Feature | How | Why it helps |
|---|---|---|
| Table | Ctrl+T | New rows are included in formulas, charts and pivots |
| Structured references | `=SUM(Sales[Amount])` | Readable formulas that use column names |
| Sort | Data → Sort | Order by one or more columns |
| Filter | Data → Filter | Show only rows that match |
| Data validation | Data → Data Validation → List | Drop-down lists, no typing mistakes |
| Conditional formatting | Home → Conditional Formatting | Highlight values, duplicates, top 10, data bars |
| Freeze panes | View → Freeze Panes | Keep the header visible while scrolling |
| Remove duplicates | Data → Remove Duplicates | Clean repeated rows |

:::tip Validation prevents messy data
If people type "Cairo", "cairo" and "Cairo " in the same column, SUMIF will treat them as different. A drop-down list (data validation) keeps the values consistent from the start.
:::

```exercise excel
? Total the Amount column of a table named Sales with a structured reference
=SUM(Sales[___])
= Amount
```

```quiz
? What is the main advantage of formatting a range as a Table?
* Formulas, charts and pivots grow automatically with new rows
- The file becomes smaller
- Formulas are no longer needed
```

# @lesson excel-pivot
title: Pivot tables
summary: Summarising thousands of rows by category and month in a few clicks.
---
A **PivotTable** summarises a table without formulas: you drag fields into **Rows**, **Columns**, **Values** and **Filters**.

Starting from the sales table in the conditional totals lesson:

1. Click inside the data and choose **Insert → PivotTable**.
2. Drag **Branch** to Rows, **Product** to Columns, **Amount** to Values (it becomes "Sum of Amount").
3. Drag **Date** to Rows below Branch and group it by **Months** (right-click → Group).

| Sum of Amount | Laptop | Monitor | Mouse | Total |
|---|---|---|---|---|
| Alex | 24000 | | | 24000 |
| Cairo | 25000 | 6000 | 500 | 31500 |
| Giza | | | 450 | 450 |
| **Total** | **49000** | **6000** | **950** | **55950** |

- Change "Sum" to **Count**, **Average** or **% of total** in Value Field Settings.
- Add **slicers** (PivotTable Analyze → Insert Slicer) for clickable filters.
- When the source data changes, press **Refresh** (Data → Refresh All).

:::tip Start from a Table
Build pivots from an Excel Table. When new rows are added, Refresh includes them automatically; with a plain range you would have to change the source.
:::

```quiz
? After adding new rows to the source data, what must you do to see them in the pivot table?
* Refresh the pivot table
- Rebuild the pivot from scratch
- Nothing, it updates while you type

? A pivot table can summarise data without writing formulas.
= true
```

# @lesson excel-charts
title: Charts and a simple dashboard
summary: Choosing the right chart, building it from a table or pivot, and keeping it readable.
---
| Question | Chart |
|---|---|
| How does a value change over time? | Line chart |
| Which category is largest? | Bar or column chart (sorted) |
| What is the share of each part (2–4 parts)? | Pie or doughnut |
| Is there a relationship between two numbers? | Scatter chart |
| How are values spread? | Histogram or box plot |

Steps: select the data (or click a pivot table) → **Insert** → choose the chart → add a clear title → remove what does not help (gridlines, 3D effects, legends with one series).

**A simple dashboard**: put a pivot table and its **PivotChart** on a separate sheet, add one or two **slicers** connected to all pivots (Report Connections), and a few key numbers at the top with formulas such as `=SUM(Sales[Amount])`.

:::tip Titles that say the finding
"Cairo sells 31,500 EGP, 56% of the total" tells the reader more than "Sales by branch".
:::

```quiz
? Which chart best shows monthly revenue over a year?
* A line chart
- A pie chart
- A scatter chart

? Sorting bars from largest to smallest makes a bar chart easier to read.
= true
```

# @lesson excel-reference
title: Excel quick reference
summary: The most used formulas, shortcuts and habits on one page.
---
| Formula | Use |
|---|---|
| `=SUM / AVERAGE / MIN / MAX / COUNT / COUNTA` | Basic summaries |
| `=ROUND(x,2)` | Round |
| `=IF / IFS / AND / OR / IFERROR` | Decisions |
| `=SUMIFS / COUNTIFS / AVERAGEIFS` | Totals with conditions |
| `=XLOOKUP / INDEX+MATCH / VLOOKUP(…,FALSE)` | Look up values |
| `=TRIM / PROPER / LEFT / RIGHT / TEXTJOIN / TEXT` | Text |
| `=TODAY / DATE / EDATE / NETWORKDAYS.INTL` | Dates |
| `$A$1` / F4 | Absolute references |

| Shortcut | Action |
|---|---|
| Ctrl+T | Make a table |
| Ctrl+Shift+L | Filters on/off |
| Ctrl+Arrow | Jump to the edge of the data |
| Ctrl+Shift+Arrow | Select to the edge |
| Alt+= | AutoSum |
| Ctrl+; | Today's date |
| F2 | Edit the cell |
| F4 | Toggle $ in a reference |

:::tip Where to go next
Take a report you update by hand every month, turn its data into a Table, replace manual totals with SUMIFS or a pivot table, and add a chart with a title that states the finding. Then explore Power Query (Data → Get Data) to import and clean data automatically. For larger analyses, continue with the SQL, pandas and Matplotlib courses in this library.
:::

```quiz
? Which shortcut turns a range into an Excel Table?
* Ctrl+T
- Ctrl+P
- Alt+=
```
