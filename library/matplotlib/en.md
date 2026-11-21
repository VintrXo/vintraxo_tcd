# @lesson mpl-intro
title: Matplotlib introduction
summary: What Matplotlib is, the pyplot interface, and your first line chart.
---
**Matplotlib** is Python's best-known charting library. With a few lines you can turn numbers into line charts, bar charts, histograms and more, and save them as images for reports. pandas and many other libraries use it underneath.

```try python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
visitors = [820, 940, 1100, 1050, 1300, 1490]

plt.plot(months, visitors)
plt.title("Website visitors")
plt.xlabel("Month")
plt.ylabel("Visitors")
print("chart ready")
```

- `import matplotlib.pyplot as plt` is the standard way to import it.
- `plt.plot(x, y)` draws a line; `title`, `xlabel` and `ylabel` add text.
- Here the chart appears under the output. In a script on your computer you would call `plt.show()` to open a window, or `plt.savefig("chart.png")` to save a file.

:::info Running the examples
Charts are drawn in your browser by Python itself. The first run downloads Matplotlib, which can take a few seconds.
:::

```quiz
? Which import is the usual way to use Matplotlib?
* import matplotlib.pyplot as plt
- import matplotlib as plot
- from charts import plt

? plt.savefig("chart.png") saves the chart as an image file.
= true
```

# @lesson mpl-line
title: Line charts
summary: Several lines, markers, line styles, colors, legends and grids.
---
```try python
import matplotlib.pyplot as plt

months = range(1, 13)
cairo = [14, 16, 19, 23, 27, 29, 30, 30, 28, 25, 20, 16]
alex = [13, 14, 16, 19, 22, 25, 26, 27, 26, 23, 19, 15]

plt.figure(figsize=(7, 3.5))
plt.plot(months, cairo, marker="o", color="#b45309", label="Cairo")
plt.plot(months, alex, marker="s", linestyle="--", color="#0e7490", label="Alexandria")
plt.title("Average temperature by month")
plt.xlabel("Month")
plt.ylabel("°C")
plt.xticks(list(months))
plt.grid(alpha=0.3)
plt.legend()
print("two lines, one legend")
```

```reference python
plt.plot(x, y) | Line chart | plt.plot(days, sales)
marker="o" | Point markers (o s ^ x .) | marker="s"
linestyle="--" | Line style (- -- : -.) | linestyle=":"
color="..." / label="..." | Color and legend name | color="#4338ca", label="2025"
plt.legend() / plt.grid() | Legend / grid lines | plt.grid(alpha=0.3)
plt.figure(figsize=(w, h)) | Size in inches | plt.figure(figsize=(8, 4))
plt.xticks(...) / plt.ylim(a, b) | Axis ticks / range | plt.ylim(0, 100)
```

```exercise python
? Show the names given with label=... on the chart
plt.___()
= legend
```

```quiz
? Which argument draws a dashed line?
* linestyle="--"
- marker="--"
- color="dashed"
```

# @lesson mpl-bar
title: Bar charts
summary: Vertical and horizontal bars, sorting, value labels and grouped bars.
---
```try python
import matplotlib.pyplot as plt
import numpy as np

branches = ["Cairo", "Giza", "Alex", "Tanta", "Aswan"]
sales = [420, 310, 365, 140, 95]

order = np.argsort(sales)                      # sort so the chart is easy to read
plt.figure(figsize=(6, 3))
bars = plt.barh(np.array(branches)[order], np.array(sales)[order], color="#6366f1")
plt.bar_label(bars, padding=3)                 # numbers at the end of each bar
plt.title("Sales by branch (thousand EGP)")
plt.xlim(0, 480)

plt.figure(figsize=(6, 3))
quarters = np.arange(4)
width = 0.38
plt.bar(quarters - width / 2, [120, 150, 170, 210], width, label="2024", color="#94a3b8")
plt.bar(quarters + width / 2, [140, 165, 200, 260], width, label="2025", color="#4338ca")
plt.xticks(quarters, ["Q1", "Q2", "Q3", "Q4"])
plt.title("Revenue by quarter")
plt.legend()
print("two charts drawn")
```

Each `plt.figure()` starts a new chart, so this example produces two images.

```reference python
plt.bar(x, heights) | Vertical bars | plt.bar(names, values)
plt.barh(y, widths) | Horizontal bars (good for long names) | plt.barh(names, values)
plt.bar_label(bars) | Value labels on bars | plt.bar_label(bars, fmt="%.0f")
width / offsets | Grouped bars side by side | plt.bar(x - w/2, a, w)
np.argsort(values) | Order for sorting | order = np.argsort(values)
```

:::tip Bars start at zero
Bar length is read as size, so the value axis of a bar chart should start at zero. Line charts may zoom in on a range.
:::

```exercise python
? Draw horizontal bars
plt.___(names, values)
= barh
```

```quiz
? When are horizontal bars a better choice?
* When category names are long or there are many categories
- Only for negative numbers
- When there are two categories
```

# @lesson mpl-scatter
title: Scatter plots
summary: Relationships between two numbers, color and size encodings, and a trend line.
---
```try python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
hours = rng.uniform(1, 12, 60)
score = 40 + 4.5 * hours + rng.normal(0, 6, 60)
team = rng.integers(0, 3, 60)

plt.figure(figsize=(6, 4))
points = plt.scatter(hours, score, c=team, cmap="viridis", s=40, alpha=0.8)
slope, intercept = np.polyfit(hours, score, 1)          # straight line that fits best
xs = np.linspace(1, 12, 50)
plt.plot(xs, slope * xs + intercept, color="crimson", label=f"trend: +{slope:.1f} per hour")
plt.colorbar(points, label="team")
plt.xlabel("Training hours")
plt.ylabel("Test score")
plt.legend()
print("correlation:", round(np.corrcoef(hours, score)[0, 1], 2))
```

```reference python
plt.scatter(x, y) | Scatter plot | plt.scatter(age, salary)
c=values, cmap="..." | Color by a value | c=team, cmap="viridis"
s=size / alpha | Point size / transparency | s=20, alpha=0.5
plt.colorbar() | Color scale legend | plt.colorbar(points)
np.polyfit(x, y, 1) | Fit a straight line | slope, b = np.polyfit(x, y, 1)
```

```exercise python
? Make points half transparent
plt.scatter(x, y, ___=0.5)
= alpha
```

```quiz
? What does a scatter plot show best?
* The relationship between two numeric variables
- Parts of a whole
- Change in one value over time only
```

# @lesson mpl-distribution
title: Histograms and box plots
summary: How values are spread: bins, comparing groups, and outliers.
---
```try python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
cairo = rng.normal(28, 4, 300)                 # delivery time in minutes
giza = rng.normal(35, 7, 300)

fig, (left, right) = plt.subplots(1, 2, figsize=(9, 3.5))
left.hist(cairo, bins=20, alpha=0.7, label="Cairo", color="#4338ca")
left.hist(giza, bins=20, alpha=0.7, label="Giza", color="#f59e0b")
left.set_title("Delivery time (minutes)")
left.legend()

right.boxplot([cairo, giza], labels=["Cairo", "Giza"])
right.set_title("Same data as box plots")
print("medians:", round(float(np.median(cairo)), 1), round(float(np.median(giza)), 1))
```

- A **histogram** splits values into ranges (`bins`) and shows how many fall into each.
- A **box plot** shows the median (line), the middle half of the data (box), the spread (whiskers) and outliers (dots).

```reference python
plt.hist(values, bins=n) | Histogram | plt.hist(ages, bins=10)
plt.boxplot([a, b], labels=[...]) | Box plots side by side | plt.boxplot([x, y])
fig, (a, b) = plt.subplots(1, 2) | Two charts in one figure | fig, axes = plt.subplots(2, 2)
ax.set_title / ax.legend | Methods on one chart (axes) | ax.set_xlabel("min")
```

```exercise python
? Split the values into 30 ranges
plt.hist(values, ___=30)
= bins
```

```quiz
? Which chart shows outliers as separate dots?
* A box plot
- A pie chart
- A line chart
```

# @lesson mpl-pie
title: Pie and donut charts, and when not to use them
summary: Parts of a whole, percentages, and why bars are often better.
---
```try python
import matplotlib.pyplot as plt

channels = ["Search", "Social", "Email", "Direct"]
signups = [420, 260, 180, 140]

fig, (left, right) = plt.subplots(1, 2, figsize=(9, 3.5))
left.pie(signups, labels=channels, autopct="%1.0f%%", startangle=90,
         wedgeprops={"width": 0.45})                        # width makes a donut
left.set_title("Signups by channel")

right.barh(channels[::-1], signups[::-1], color="#6366f1")
right.set_title("The same data as bars")
print("largest share:", channels[signups.index(max(signups))])
```

:::tip Pies only for a few parts
People compare lengths much better than angles. Use a pie or donut only for 2 to 4 parts of one whole, when the message is "this part is about half". For anything else, a sorted bar chart is clearer.
:::

```reference python
plt.pie(values, labels=...) | Pie chart | plt.pie(shares, labels=names)
autopct="%1.0f%%" | Show percentages | autopct="%1.1f%%"
startangle=90 | Start at the top | startangle=90
wedgeprops={"width": w} | Donut hole | wedgeprops={"width": 0.4}
```

```quiz
? Why is a bar chart often clearer than a pie chart?
* People compare lengths more accurately than angles
- Pie charts cannot show percentages
- Bar charts use more colors
```

# @lesson mpl-subplots
title: Figures, axes and subplots
summary: The object-oriented interface: fig and ax, grids of charts, and shared axes.
---
For anything beyond one quick chart, use the **object-oriented** style: `fig` is the whole image, and each `ax` is one chart inside it.

```try python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
fig, axes = plt.subplots(2, 2, figsize=(8, 5), sharex=True)
axes[0, 0].plot(x, np.sin(x), color="#4338ca")
axes[0, 0].set_title("sin(x)")
axes[0, 1].plot(x, np.cos(x), color="#0e7490")
axes[0, 1].set_title("cos(x)")
axes[1, 0].fill_between(x, np.sin(x) ** 2, color="#f59e0b", alpha=0.6)
axes[1, 0].set_title("sin²(x)")
axes[1, 1].plot(x, np.sin(x) * np.exp(-x / 3), color="#be185d")
axes[1, 1].set_title("damped wave")
for ax in axes.flat:
    ax.grid(alpha=0.3)
fig.suptitle("Four charts, one figure")
fig.tight_layout()
print("charts in the figure:", len(axes.flat))
```

```reference python
fig, ax = plt.subplots() | One chart, object-oriented | ax.plot(x, y)
plt.subplots(rows, cols) | A grid of charts | fig, axes = plt.subplots(2, 3)
axes[r, c] / axes.flat | One chart / all charts | for ax in axes.flat: ...
ax.set_title / set_xlabel / set_ylim | Methods instead of plt.title... | ax.set_ylim(0, 1)
sharex=True / sharey=True | Same axis range | plt.subplots(2, 1, sharex=True)
fig.suptitle / fig.tight_layout() | Overall title / fix overlaps | fig.tight_layout()
```

```exercise python
? Create a grid of 2 rows and 3 columns of charts
fig, axes = plt.___(2, 3)
= subplots
```

```quiz
? In the object-oriented style, what is ax?
* One chart (axes) inside the figure
- The whole image file
- The x axis only
```

# @lesson mpl-customize
title: Annotations and styling
summary: Annotate important points, format axes, use styles and colors that work for everyone.
---
```try python
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.style.use("ggplot")
days = list(range(1, 15))
users = [120, 135, 150, 148, 160, 158, 300, 290, 310, 305, 320, 330, 335, 350]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(days, users, color="#4338ca", linewidth=2.5)
ax.annotate("Launch campaign", xy=(7, 300), xytext=(2.5, 320),
            arrowprops={"arrowstyle": "->", "color": "#334155"})
ax.axvline(7, color="#94a3b8", linestyle=":")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f} users"))
ax.set_title("Daily active users", loc="left", fontsize=13, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Day")
print("styles available:", len(plt.style.available))
```

```reference python
ax.annotate(text, xy, xytext, arrowprops) | Point at something important | ax.annotate("Peak", xy=(5, 90))
ax.axvline / ax.axhline | Reference lines | ax.axhline(target, linestyle="--")
plt.style.use("...") | A ready-made look | plt.style.use("ggplot")
FuncFormatter | Custom tick labels | FuncFormatter(lambda v, _: f"{v:.0%}")
ax.spines[...].set_visible(False) | Remove chart borders | ax.spines[["top", "right"]].set_visible(False)
cmap="viridis" | Color maps that work for color-blind readers | plt.scatter(x, y, c=v, cmap="viridis")
```

:::tip A chart should say one thing
Put the main message in the title ("Users doubled after the campaign"), highlight the one line or bar that matters, and remove decoration that does not help the reader.
:::

```exercise python
? Add a horizontal reference line at the target value
ax.___(target, linestyle="--")
= axhline
```

```quiz
? What is annotate() used for?
* Adding a label and arrow that point to an important spot
- Saving the chart
- Changing the chart type
```

# @lesson mpl-pandas
title: Plotting pandas data
summary: DataFrame.plot, grouping before plotting, and saving images.
---
```try python
import pandas as pd
import matplotlib.pyplot as plt

orders = pd.DataFrame({
    "month": ["2025-01", "2025-01", "2025-02", "2025-02", "2025-03", "2025-03", "2025-04", "2025-04"],
    "channel": ["Online", "Store"] * 4,
    "revenue": [120, 200, 150, 190, 210, 185, 260, 180],
})

table = orders.pivot_table(index="month", columns="channel", values="revenue", aggfunc="sum")
print(table)

ax = table.plot(kind="bar", figsize=(6, 3.5), color=["#4338ca", "#94a3b8"], rot=0)
ax.set_title("Revenue by channel")
ax.set_ylabel("thousand EGP")

ax2 = table.sum(axis=1).plot(kind="line", marker="o", figsize=(6, 3), color="#0e7490")
ax2.set_title("Total revenue")

plt.gcf().savefig("total_revenue.png", dpi=80)        # save to a file
print("saved total_revenue.png")
```

```reference python
df.plot(kind="line" / "bar" / "barh" / "hist" / "scatter") | Plot straight from a DataFrame | df.plot(kind="bar", x="name", y="sales")
df.pivot_table(index, columns, values, aggfunc) | Reshape before plotting | df.pivot_table(index="month", columns="channel", values="rev")
series.plot() | Plot one column | df["sales"].plot()
rot=0 | Keep tick labels horizontal | df.plot(kind="bar", rot=0)
fig.savefig("file.png", dpi=...) | Save the image | fig.savefig("chart.png", dpi=150)
```

```exercise python
? Draw the DataFrame as a bar chart
df.plot(kind="___")
= bar
```

```quiz
? What does df.plot() return, so you can keep customising?
* An axes (ax) object
- A new DataFrame
- An image file
```

# @lesson mpl-project
title: Project: a one-page sales dashboard
summary: Four charts that answer four questions, in one figure.
---
```try python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
days = pd.date_range("2025-01-01", periods=90, freq="D")
df = pd.DataFrame({
    "day": np.tile(days, 3),
    "branch": np.repeat(["Cairo", "Giza", "Alex"], 90),
})
base = df["branch"].map({"Cairo": 52, "Giza": 38, "Alex": 44})
trend = np.tile(np.linspace(0, 12, 90), 3)
df["orders"] = (base + trend + rng.normal(0, 6, len(df))).round().clip(lower=0)
df["avg_value"] = rng.normal(180, 25, len(df)).round()

fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
fig.suptitle("Q1 sales dashboard", fontsize=15, fontweight="bold")

daily = df.groupby("day")["orders"].sum()
axes[0, 0].plot(daily.index, daily.rolling(7).mean(), color="#4338ca")
axes[0, 0].set_title("1. Are orders growing? (7-day average)")
axes[0, 0].tick_params(axis="x", labelrotation=30)

by_branch = df.groupby("branch")["orders"].sum().sort_values()
bars = axes[0, 1].barh(by_branch.index, by_branch.values, color="#0e7490")
axes[0, 1].bar_label(bars, fmt="%.0f", padding=3)
axes[0, 1].set_title("2. Which branch sells most?")

axes[1, 0].hist(df["avg_value"], bins=20, color="#f59e0b")
axes[1, 0].set_title("3. How big is a typical order? (EGP)")

weekday = df.assign(wd=df["day"].dt.day_name().str[:3]).groupby("wd")["orders"].mean()
weekday = weekday.reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
axes[1, 1].bar(weekday.index, weekday.values, color="#be185d")
axes[1, 1].set_title("4. Which weekday is busiest?")

for ax in axes.flat:
    ax.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(hspace=0.5, wspace=0.3)
print("total orders:", int(df["orders"].sum()), "| best branch:", by_branch.index[-1])
```

:::tip Make it yours
Replace the generated data with a CSV from your own work (`pd.read_csv`), keep the four questions, and change the titles into answers, for example "Cairo sells 30% more than Giza".
:::

```quiz
? Why does each chart title in the project ask a question?
* So each chart has a clear purpose for the reader
- Because Matplotlib requires titles
- To make the figure larger
```

# @lesson mpl-reference
title: Matplotlib quick reference
summary: Chart types, the main settings and good practice on one page.
---
```reference python
plt.plot / ax.plot | Line chart | ax.plot(x, y, marker="o")
plt.bar / plt.barh | Bar charts | ax.barh(names, values)
plt.scatter | Scatter plot | ax.scatter(x, y, c=v, cmap="viridis")
plt.hist / plt.boxplot | Distributions | ax.hist(values, bins=20)
plt.pie | Parts of a whole (few parts only) | ax.pie(shares, autopct="%1.0f%%")
fig, axes = plt.subplots(r, c) | Several charts | axes[0, 1].plot(...)
title / xlabel / ylabel / legend | Text | ax.set_title("Sales")
annotate / axhline | Highlight | ax.axhline(100, linestyle="--")
plt.style.use / spines | Look and feel | plt.style.use("ggplot")
df.plot(kind=...) | From pandas | df.plot(kind="bar")
savefig("file.png", dpi=...) | Save | fig.savefig("out.png", dpi=150)
```

:::tip Where to go next
Recreate one chart from a report at work, then improve it: a title that states the finding, sorted bars, fewer colors. For interactive charts on the web, look at Plotly; for statistical charts with less code, at seaborn.
:::

```quiz
? Which call places several charts in one figure?
* plt.subplots
- plt.legend
- plt.savefig
```
