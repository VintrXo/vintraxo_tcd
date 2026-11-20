# @lesson r-intro
title: R introduction
summary: What R is used for, and your first commands.
---
**R** is a language built for statistics and data analysis. Researchers, analysts and data scientists use it to clean data, compute statistics, fit models and draw charts. It has thousands of free packages on CRAN for almost every kind of analysis.

```try r
print("Hello, R")
6 * 7
sqrt(144)
mean(c(4, 8, 15, 16, 23, 42))
```

- Typing an expression shows its value; `print()` does the same inside scripts and functions.
- `c(...)` combines values into a **vector**, R's basic data structure.
- Comments start with `#`.

:::info Running the examples
R examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: install R from CRAN and RStudio (or Positron), then run code in the console or in a script.
:::

```quiz
? What is R mainly designed for?
* Statistics and data analysis
- Building mobile apps
- Writing operating systems

? c(1, 2, 3) creates a vector.
= true
```

# @lesson r-variables
title: Variables and types
summary: Assignment with <-, numeric, character, logical, and checking types.
---
```try r
name <- "Sara"          # <- is the usual assignment in R
age <- 25
height = 1.68           # = also works
active <- TRUE
nothing <- NA           # a missing value

cat("Name:", name, "- age:", age, "\n")
class(age)
class(name)
class(active)
is.na(nothing)
age_next <- age + 1L    # L makes an integer
class(age_next)
as.numeric("3.5") * 2
paste("Hello", name)
```

```reference r
x <- 5 | Assign a value | total <- 0
numeric / integer | Numbers (5 / 5L) | n <- 10L
character | Text | city <- "Cairo"
logical | TRUE / FALSE | ok <- TRUE
NA / NULL | Missing value / nothing | is.na(x)
class(x) | Type of a value | class(3.14)
as.numeric / as.character | Convert types | as.numeric("7")
cat / print | Show values | cat("x =", x, "\n")
```

:::tip <- or =?
Both assign, but `<-` is the standard style in R code and books. Keep `=` for naming arguments inside function calls, as in `round(x, digits = 2)`.
:::

```exercise r
? Assign 100 to the variable budget with R's usual operator
budget ___ 100
= <-
```

```quiz
? How is a missing value written in R?
* NA
- null
- None

? class("abc") returns "character".
= true
```

# @lesson r-vectors
title: Vectors
summary: Creating vectors, indexing, vectorised maths and logical filtering.
---
In R, most operations work on whole vectors at once, with no loop needed.

```try r
prices <- c(12.5, 20, 35, 8)
names(prices) <- c("tea", "coffee", "cake", "water")
prices
prices[2]                 # indexing starts at 1
prices["cake"]
prices[c(1, 3)]
prices[-1]                # everything except the first

prices * 1.15             # every price with tax
sum(prices); length(prices); max(prices)
prices[prices > 10]       # logical filtering
which(prices > 10)

1:5
seq(0, 1, by = 0.25)
rep("x", 3)
sort(c(5, 2, 9), decreasing = TRUE)
```

```reference r
c(a, b, c) | Combine into a vector | v <- c(1, 2, 3)
v[i] | Item i (starts at 1) | v[1]
v[-i] | Everything except item i | v[-1]
v[v > x] | Filter with a condition | v[v %% 2 == 0]
a:b / seq() / rep() | Sequences and repeats | seq(1, 10, by = 2)
length / sum / mean | Size and totals | mean(v)
sort / order / rev | Sorting | v[order(v)]
names(v) | Labels for items | names(v) <- c("a", "b")
```

:::warning Indexing starts at 1
Unlike most languages, the first item is `v[1]`, not `v[0]`.
:::

```exercise r
? Keep only the values of v greater than 10
v[v ___ 10]
= >
```

```quiz
? What does c(1, 2, 3) * 2 give?
* 2 4 6
- 1 2 3 1 2 3
- An error

? prices[1] is the first element of prices.
= true
```

# @lesson r-conditions
title: Operators and conditions
summary: Arithmetic, comparison, logic, if, else and ifelse.
---
```try r
7 / 2         # 3.5
7 %/% 2       # integer division: 3
7 %% 2        # remainder: 1
2 ^ 10

score <- 78
if (score >= 90) {
  grade <- "A"
} else if (score >= 70) {
  grade <- "B"
} else {
  grade <- "C"
}
grade

scores <- c(95, 72, 40, 88)
ifelse(scores >= 50, "pass", "fail")      # vectorised condition

x <- 5
x > 3 & x < 10
x < 3 | x == 5
!TRUE
3 %in% c(1, 2, 3)

day <- "fri"
switch(day, fri = , sat = "weekend", "working day")
```

```reference r
+ - * / ^ | Arithmetic | 2 ^ 3
%/% / %% | Integer division / remainder | 10 %% 3
== != < > <= >= | Comparison | x != 0
&, |, ! | And / or / not (vectorised) | x > 0 & x < 5
&& / || | And / or for single values in if | if (a && b)
if / else if / else | Condition | if (x > 0) { } else { }
ifelse(cond, a, b) | Condition over a whole vector | ifelse(v > 0, "+", "-")
%in% | Is it in the set? | "tea" %in% menu
switch() | Choose by value | switch(x, a = 1, b = 2)
```

```exercise r
? Get the remainder of 17 divided by 5
17 ___ 5
= %%
```

```quiz
? Which function applies a condition to every element of a vector?
* ifelse
- if
- switch
```

# @lesson r-loops-functions
title: Loops and functions
summary: for, while, writing functions, default arguments and return values.
---
```try r
for (i in 1:3) {
  cat("Round", i, "\n")
}

fruits <- c("apple", "banana", "cherry")
for (f in fruits) print(toupper(f))

n <- 3
while (n > 0) {
  cat(n, "")
  n <- n - 1
}
cat("go!\n")

area <- function(width, height = width) {   # height defaults to width
  width * height                            # the last value is returned
}
area(3, 4)
area(5)

describe <- function(x) {
  if (length(x) == 0) return("empty")
  list(mean = mean(x), sd = round(sd(x), 2), n = length(x))
}
describe(c(2, 4, 4, 4, 5, 5, 7, 9))
describe(c())

square <- function(x) x^2
square(1:5)              # works on whole vectors too
```

```reference r
for (x in v) { } | Loop over a vector | for (i in 1:10)
while (cond) { } | Repeat while true | while (n > 0)
break / next | Leave / skip a round | if (x < 0) next
f <- function(a, b = 1) { } | Define a function | add <- function(a, b) a + b
last expression | The value returned | function(x) x * 2
return(x) | Return early | if (bad) return(NA)
f(b = 2, a = 1) | Named arguments | round(x, digits = 1)
```

:::tip Think in vectors
In R, a loop is often not needed: `square(1:5)` or `prices * 1.15` already work on every element and are faster than a `for` loop.
:::

```exercise r
? Write the keyword that creates a function
double <- ___(x) x * 2
= function
```

```quiz
? What does a function return if it has no return() call?
* The value of its last expression
- NULL always
- An error
```

# @lesson r-lists
title: Lists and factors
summary: Lists of mixed values, $ access, and factors for categories.
---
A **vector** holds values of one type. A **list** can hold anything, even other lists.

```try r
order <- list(id = 7, customer = "Sara", items = c("tea", "cake"), paid = TRUE)
order$customer
order[["items"]]
order$items[2]
order$total <- 47.5          # add an element
names(order)
str(order)                   # compact summary of the structure

sizes <- factor(c("small", "large", "medium", "small", "large", "small"),
                levels = c("small", "medium", "large"))
sizes
levels(sizes)
table(sizes)                 # count per category
as.integer(sizes)
```

```reference r
list(a = 1, b = "x") | Create a list | p <- list(name = "A", age = 3)
l$name / l[["name"]] | One element | p$age
l["name"] | A smaller list | p["age"]
l$new <- v | Add or change an element | p$city <- "Cairo"
str(x) | Show the structure | str(p)
factor(v, levels) | Categories with a fixed order | factor(sizes, levels = c("S", "M"))
levels / table | Categories / counts | table(colors)
```

```exercise r
? Read the element named customer from the list order
order___customer
= $
```

```quiz
? What is the difference between a vector and a list?
* A vector holds one type; a list can hold different types
- A list is faster
- They are the same

? table() counts how many times each category appears.
= true
```

# @lesson r-dataframes
title: Data frames
summary: Tables of data: creating, selecting, filtering, sorting and adding columns.
---
A **data frame** is a table: each column is a vector, each row is one record.

```try r
sales <- data.frame(
  branch = c("Cairo", "Alex", "Cairo", "Giza", "Alex"),
  month  = c("Jan", "Jan", "Feb", "Feb", "Feb"),
  amount = c(1200, 800, 1500, 400, 950)
)
sales
nrow(sales); ncol(sales)
summary(sales$amount)

sales$amount                            # one column
sales[sales$amount > 900, ]             # rows by condition
sales[order(-sales$amount), c("branch", "amount")]
subset(sales, branch == "Alex", select = c(month, amount))

sales$tax <- sales$amount * 0.14        # new column
head(sales, 3)

aggregate(amount ~ branch, data = sales, FUN = sum)   # total per branch
tapply(sales$amount, sales$month, mean)
```

```reference r
data.frame(a = .., b = ..) | Create a table | df <- data.frame(x = 1:3)
df$col | One column | df$amount
df[rows, cols] | Select rows and columns | df[1:2, c("a", "b")]
df[df$x > 5, ] | Filter rows | df[df$branch == "Cairo", ]
df[order(df$x), ] | Sort rows | df[order(-df$amount), ]
subset(df, cond, select) | Filter and select | subset(df, x > 1, select = y)
head / nrow / summary | Quick look | summary(df)
aggregate(y ~ g, df, FUN) | Group and summarise | aggregate(amount ~ branch, df, sum)
read.csv / write.csv | Files | df <- read.csv("sales.csv")
```

:::tip The comma matters
`df[rows, cols]`: the part before the comma picks rows, the part after picks columns. `df[df$amount > 900, ]` keeps all columns because nothing is after the comma.
:::

```exercise r
? Count the rows of the data frame sales
___(sales)
= nrow
```

```quiz
? What does sales[sales$amount > 900, ] return?
* Every column of the rows where amount is above 900
- Only the amount column
- The number of rows
```

# @lesson r-apply
title: The apply family
summary: sapply, lapply, apply and Map instead of loops.
---
```try r
nums <- list(a = 1:5, b = c(10, 20), c = c(2, 4, 6, 8))
lapply(nums, mean)              # returns a list
sapply(nums, mean)              # simplifies to a vector
sapply(nums, function(v) max(v) - min(v))

words <- c("tea", "coffee", "cake")
sapply(words, nchar)
vapply(words, toupper, character(1))   # like sapply, with a fixed result type

m <- matrix(1:6, nrow = 2)
m
apply(m, 1, sum)                # 1 = per row
apply(m, 2, max)                # 2 = per column

Map(function(x, y) x * y, 1:3, 4:6)
Reduce(`+`, 1:5, accumulate = TRUE)
Filter(function(x) x %% 2 == 0, 1:10)
```

```reference r
lapply(x, f) | Apply f to each item, return a list | lapply(files, read.csv)
sapply(x, f) | Same, simplify to a vector | sapply(df, class)
vapply(x, f, type) | Same, with a checked type | vapply(x, nchar, integer(1))
apply(m, 1 / 2, f) | Over matrix rows / columns | apply(m, 2, mean)
Map(f, a, b) | Pair up several vectors | Map(paste, a, b)
Filter / Reduce | Keep matching / fold | Reduce(`+`, v)
```

```exercise r
? Compute the mean of each element of the list nums as a simple vector
___(nums, mean)
= sapply
```

```quiz
? What is the difference between lapply and sapply?
* lapply always returns a list; sapply simplifies when it can
- sapply only works on numbers
- lapply is for data frames only
```

# @lesson r-strings
title: Working with text
summary: paste, sprintf, nchar, substr, toupper, grepl, sub and strsplit.
---
```try r
first <- "Sara"
last <- "Ali"
paste(first, last)
paste0(first, "_", last)
sprintf("%s has %d orders worth %.2f", first, 3L, 125.5)
nchar("hello")
toupper("cairo"); tolower("GIZA")
substr("TypeScript", 1, 4)
trimws("   spaces   ")

emails <- c("sara@example.com", "omar.at.example", "lina@test.org")
grepl("@", emails)                       # which contain @
sub("@.*", "", emails)                   # remove from @ to the end
gsub("a", "A", "banana")
strsplit("tea,coffee,cake", ",")[[1]]
format(1234567.891, big.mark = ",", nsmall = 2)
```

```reference r
paste / paste0 | Join text (with / without spaces) | paste0("id_", 1:3)
sprintf | Formatted text | sprintf("%.1f%%", 12.34)
nchar | Number of characters | nchar("مرحبا")
substr(x, start, stop) | Part of a string | substr(s, 1, 3)
toupper / tolower / trimws | Case and spaces | trimws(x)
grepl(pattern, x) | Does it match? (TRUE/FALSE) | grepl("^A", names)
sub / gsub | Replace first / all | gsub(" ", "_", x)
strsplit(x, sep) | Split into pieces | strsplit("a b", " ")
```

```exercise r
? Join "id_" and 1:3 without spaces
___("id_", 1:3)
= paste0
```

```quiz
? Which function checks whether each string contains a pattern?
* grepl
- sub
- nchar
```

# @lesson r-stats
title: Statistics and charts
summary: Summary statistics, correlation, a linear model, and base R charts.
---
```try r
set.seed(1)                                   # same random numbers every run
hours <- c(2, 3, 5, 6, 8, 9, 10, 12)
score <- c(55, 60, 65, 70, 78, 80, 85, 92)

mean(score); median(score); sd(score)
quantile(score)
cor(hours, score)                             # correlation

model <- lm(score ~ hours)                    # fit a straight line
coef(model)
round(summary(model)$r.squared, 3)
predict(model, data.frame(hours = 7))

sample(1:6, 5, replace = TRUE)                # roll a die five times
round(rnorm(3, mean = 100, sd = 15))          # random normal values
t.test(score, mu = 60)$p.value < 0.05
```

Charts open in a plot window in RStudio (they cannot be shown in this text output):

```text
plot(hours, score, main = "Study time and score", xlab = "Hours", ylab = "Score")
abline(model, col = "red")
hist(score, breaks = 5)
barplot(table(c("A", "B", "A", "C")))
boxplot(amount ~ branch, data = sales)
```

```reference r
mean / median / sd / var | Centre and spread | sd(x)
quantile / summary | Quartiles / overview | quantile(x, 0.9)
cor(x, y) | Correlation | cor(df$a, df$b)
lm(y ~ x) | Linear regression | model <- lm(price ~ size, data = df)
predict(model, newdata) | Predict new values | predict(model, data.frame(size = 90))
set.seed / sample / rnorm | Random numbers | sample(1:10, 3)
t.test | Compare means | t.test(a, b)
plot / hist / barplot / boxplot | Base charts | hist(df$age)
```

:::tip ggplot2 for publication charts
The package **ggplot2** builds charts in layers: `ggplot(df, aes(hours, score)) + geom_point() + geom_smooth(method = "lm")`. Install it with `install.packages("ggplot2")`.
:::

```exercise r
? Fit a linear model of score on hours
model <- ___(score ~ hours)
= lm
```

```quiz
? What does set.seed(1) do?
* Makes the random numbers repeat the same way every run
- Removes randomness completely
- Sets the first value of a vector

? cor(x, y) close to 1 means a strong positive relationship.
= true
```

# @lesson r-reference
title: R quick reference
summary: The most used syntax and functions on one page.
---
```reference r
x <- v | Assign | n <- 10
c() / 1:n / seq() | Vectors | v <- c(2, 4, 6)
v[1] / v[v > 2] | Index (from 1) / filter | v[-1]
if / else / ifelse | Conditions | ifelse(v > 0, "+", "-")
for / while | Loops | for (i in 1:n) { }
f <- function(x) { } | Functions | sq <- function(x) x^2
list() / $ | Lists | p$name
factor() / table() | Categories and counts | table(df$city)
data.frame() / df[r, c] | Tables | df[df$age > 30, ]
subset / aggregate / order | Filter, group, sort | aggregate(y ~ g, df, mean)
sapply / lapply / apply | Apply a function | sapply(df, mean)
paste0 / sprintf / gsub | Text | sprintf("%.2f", x)
mean / sd / cor / lm | Statistics | lm(y ~ x, data = df)
read.csv / write.csv | Files | read.csv("data.csv")
```

:::tip Where to go next
Load a real CSV file with `read.csv`, explore it with `summary` and `table`, and answer one question with `aggregate` and a chart. Then learn the tidyverse (`dplyr`, `ggplot2`) for a modern data workflow.
:::

```quiz
? Which structure is best for a table of data with named columns?
* A data frame
- A single vector
- A factor
```
