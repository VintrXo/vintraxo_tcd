# @lesson r-intro
title: مقدمة R
summary: فيمَ تُستخدم R، وأول أوامرك.
---
**R** لغة صُممت للإحصاء وتحليل البيانات. يستخدمها الباحثون والمحللون وعلماء البيانات لتنظيف البيانات وحساب الإحصاءات وبناء النماذج ورسم المخططات. ولها آلاف الحزم المجانية على CRAN لكل أنواع التحليل تقريبًا.

```try r
print("Hello, R")
6 * 7
sqrt(144)
mean(c(4, 8, 15, 16, 23, 42))
```

- كتابة تعبير تعرض قيمته، و `print()` تفعل ذلك داخل السكربتات والدوال.
- `c(...)` تجمع القيم في **متجه (vector)**، وهو البنية الأساسية في R.
- التعليقات تبدأ بـ `#`.

:::info تشغيل الأمثلة
أمثلة R تعمل على خادم تشغيل منفصل وآمن؛ إن لم يكن مفعّلًا بعد فستعمل فور تفعيله. وعلى جهازك: ثبّت R من CRAN و RStudio (أو Positron)، ثم شغّل الكود في الطرفية أو في سكربت.
:::

```quiz
? فيمَ صُممت R أساسًا؟
* الإحصاء وتحليل البيانات
- بناء تطبيقات الجوال
- كتابة أنظمة التشغيل

? ينشئ c(1, 2, 3) متجهًا.
= true
```

# @lesson r-variables
title: المتغيرات والأنواع
summary: الإسناد بـ <-، والأرقام والنصوص والقيم المنطقية، ومعرفة الأنواع.
---
```try r
name <- "Sara"          # <- هو الإسناد المعتاد في R
age <- 25
height = 1.68           # = تعمل أيضًا
active <- TRUE
nothing <- NA           # قيمة ناقصة

cat("Name:", name, "- age:", age, "\n")
class(age)
class(name)
class(active)
is.na(nothing)
age_next <- age + 1L    # L تجعله عددًا صحيحًا
class(age_next)
as.numeric("3.5") * 2
paste("Hello", name)
```

```reference r
x <- 5 | إسناد قيمة | total <- 0
numeric / integer | الأرقام (5 / 5L) | n <- 10L
character | النص | city <- "Cairo"
logical | TRUE / FALSE | ok <- TRUE
NA / NULL | قيمة ناقصة / لا شيء | is.na(x)
class(x) | نوع القيمة | class(3.14)
as.numeric / as.character | تحويل الأنواع | as.numeric("7")
cat / print | عرض القيم | cat("x =", x, "\n")
```

:::tip <- أم =؟
كلاهما يُسند، لكن `<-` هو الأسلوب المعتاد في كود R وكتبها. واترك `=` لتسمية المعاملات داخل استدعاء الدوال، مثل `round(x, digits = 2)`.
:::

```exercise r
? أسند 100 إلى المتغير budget بالعامل المعتاد في R
budget ___ 100
= <-
```

```quiz
? كيف تُكتب القيمة الناقصة في R؟
* NA
- null
- None

? ترجع class("abc") القيمة "character".
= true
```

# @lesson r-vectors
title: المتجهات
summary: إنشاء المتجهات، والفهرسة، والحساب على المتجه كله، والتصفية بالشروط.
---
في R تعمل معظم العمليات على المتجه كله دفعة واحدة، بدون حلقة.

```try r
prices <- c(12.5, 20, 35, 8)
names(prices) <- c("tea", "coffee", "cake", "water")
prices
prices[2]                 # الفهرسة تبدأ من 1
prices["cake"]
prices[c(1, 3)]
prices[-1]                # كل شيء عدا الأول

prices * 1.15             # كل سعر مع الضريبة
sum(prices); length(prices); max(prices)
prices[prices > 10]       # التصفية المنطقية
which(prices > 10)

1:5
seq(0, 1, by = 0.25)
rep("x", 3)
sort(c(5, 2, 9), decreasing = TRUE)
```

```reference r
c(a, b, c) | الجمع في متجه | v <- c(1, 2, 3)
v[i] | العنصر i (يبدأ من 1) | v[1]
v[-i] | كل شيء عدا العنصر i | v[-1]
v[v > x] | التصفية بشرط | v[v %% 2 == 0]
a:b / seq() / rep() | المتتاليات والتكرار | seq(1, 10, by = 2)
length / sum / mean | الحجم والمجاميع | mean(v)
sort / order / rev | الترتيب | v[order(v)]
names(v) | أسماء العناصر | names(v) <- c("a", "b")
```

:::warning الفهرسة تبدأ من 1
على عكس معظم اللغات، العنصر الأول هو `v[1]` وليس `v[0]`.
:::

```exercise r
? أبقِ فقط قيم v الأكبر من 10
v[v ___ 10]
= >
```

```quiz
? ما ناتج c(1, 2, 3) * 2؟
* 2 4 6
- 1 2 3 1 2 3
- خطأ

? العنصر prices[1] هو أول عنصر في prices.
= true
```

# @lesson r-conditions
title: العمليات والشروط
summary: الحساب والمقارنة والمنطق و if و else و ifelse.
---
```try r
7 / 2         # 3.5
7 %/% 2       # قسمة صحيحة: 3
7 %% 2        # الباقي: 1
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
ifelse(scores >= 50, "pass", "fail")      # شرط على المتجه كله

x <- 5
x > 3 & x < 10
x < 3 | x == 5
!TRUE
3 %in% c(1, 2, 3)

day <- "fri"
switch(day, fri = , sat = "weekend", "working day")
```

```reference r
+ - * / ^ | الحساب | 2 ^ 3
%/% / %% | القسمة الصحيحة / الباقي | 10 %% 3
== != < > <= >= | المقارنة | x != 0
&, |, ! | و / أو / ليس (على المتجه كله) | x > 0 & x < 5
&& / || | و / أو لقيمة واحدة داخل if | if (a && b)
if / else if / else | شرط | if (x > 0) { } else { }
ifelse(cond, a, b) | شرط على متجه كامل | ifelse(v > 0, "+", "-")
%in% | هل هو ضمن المجموعة؟ | "tea" %in% menu
switch() | الاختيار حسب القيمة | switch(x, a = 1, b = 2)
```

```exercise r
? احسب باقي قسمة 17 على 5
17 ___ 5
= %%
```

```quiz
? أي دالة تطبّق شرطًا على كل عنصر في متجه؟
* ifelse
- if
- switch
```

# @lesson r-loops-functions
title: الحلقات والدوال
summary: for و while وكتابة الدوال والمعاملات الافتراضية والقيم المرجعة.
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

area <- function(width, height = width) {   # height افتراضيًا تساوي width
  width * height                            # تُرجَع آخر قيمة
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
square(1:5)              # تعمل على متجهات كاملة أيضًا
```

```reference r
for (x in v) { } | المرور على متجه | for (i in 1:10)
while (cond) { } | كرر ما دام الشرط صحيحًا | while (n > 0)
break / next | اخرج / تخطَّ الدورة | if (x < 0) next
f <- function(a, b = 1) { } | تعريف دالة | add <- function(a, b) a + b
آخر تعبير | القيمة المرجعة | function(x) x * 2
return(x) | إرجاع مبكر | if (bad) return(NA)
f(b = 2, a = 1) | معاملات بالاسم | round(x, digits = 1)
```

:::tip فكّر بالمتجهات
في R غالبًا لا تحتاج حلقة: `square(1:5)` أو `prices * 1.15` تعمل على كل العناصر وهي أسرع من حلقة `for`.
:::

```exercise r
? اكتب الكلمة التي تنشئ دالة
double <- ___(x) x * 2
= function
```

```quiz
? ماذا ترجع الدالة إذا لم يكن فيها استدعاء return()؟
* قيمة آخر تعبير فيها
- NULL دائمًا
- خطأ
```

# @lesson r-lists
title: القوائم والعوامل
summary: قوائم بقيم مختلفة، والوصول بـ $، والعوامل (factors) للفئات.
---
**المتجه** يحمل قيمًا من نوع واحد، أما **القائمة (list)** فتحمل أي شيء، حتى قوائم أخرى.

```try r
order <- list(id = 7, customer = "Sara", items = c("tea", "cake"), paid = TRUE)
order$customer
order[["items"]]
order$items[2]
order$total <- 47.5          # أضف عنصرًا
names(order)
str(order)                   # ملخص مختصر للبنية

sizes <- factor(c("small", "large", "medium", "small", "large", "small"),
                levels = c("small", "medium", "large"))
sizes
levels(sizes)
table(sizes)                 # العدد لكل فئة
as.integer(sizes)
```

```reference r
list(a = 1, b = "x") | إنشاء قائمة | p <- list(name = "A", age = 3)
l$name / l[["name"]] | عنصر واحد | p$age
l["name"] | قائمة أصغر | p["age"]
l$new <- v | إضافة أو تغيير عنصر | p$city <- "Cairo"
str(x) | عرض البنية | str(p)
factor(v, levels) | فئات بترتيب ثابت | factor(sizes, levels = c("S", "M"))
levels / table | الفئات / الأعداد | table(colors)
```

```exercise r
? اقرأ العنصر المسمى customer من القائمة order
order___customer
= $
```

```quiz
? ما الفرق بين المتجه والقائمة؟
* المتجه يحمل نوعًا واحدًا والقائمة تحمل أنواعًا مختلفة
- القائمة أسرع
- لا فرق بينهما

? تعدّ table() مرات ظهور كل فئة.
= true
```

# @lesson r-dataframes
title: إطارات البيانات
summary: جداول البيانات: الإنشاء والاختيار والتصفية والترتيب وإضافة الأعمدة.
---
**إطار البيانات (data frame)** جدول: كل عمود متجه، وكل صف سجل واحد.

```try r
sales <- data.frame(
  branch = c("Cairo", "Alex", "Cairo", "Giza", "Alex"),
  month  = c("Jan", "Jan", "Feb", "Feb", "Feb"),
  amount = c(1200, 800, 1500, 400, 950)
)
sales
nrow(sales); ncol(sales)
summary(sales$amount)

sales$amount                            # عمود واحد
sales[sales$amount > 900, ]             # صفوف حسب شرط
sales[order(-sales$amount), c("branch", "amount")]
subset(sales, branch == "Alex", select = c(month, amount))

sales$tax <- sales$amount * 0.14        # عمود جديد
head(sales, 3)

aggregate(amount ~ branch, data = sales, FUN = sum)   # الإجمالي لكل فرع
tapply(sales$amount, sales$month, mean)
```

```reference r
data.frame(a = .., b = ..) | إنشاء جدول | df <- data.frame(x = 1:3)
df$col | عمود واحد | df$amount
df[rows, cols] | اختيار صفوف وأعمدة | df[1:2, c("a", "b")]
df[df$x > 5, ] | تصفية الصفوف | df[df$branch == "Cairo", ]
df[order(df$x), ] | ترتيب الصفوف | df[order(-df$amount), ]
subset(df, cond, select) | تصفية واختيار | subset(df, x > 1, select = y)
head / nrow / summary | نظرة سريعة | summary(df)
aggregate(y ~ g, df, FUN) | التجميع والتلخيص | aggregate(amount ~ branch, df, sum)
read.csv / write.csv | الملفات | df <- read.csv("sales.csv")
```

:::tip الفاصلة مهمة
في `df[rows, cols]` ما قبل الفاصلة يختار الصفوف وما بعدها يختار الأعمدة. و `df[df$amount > 900, ]` تُبقي كل الأعمدة لأنه لا شيء بعد الفاصلة.
:::

```exercise r
? عُدّ صفوف إطار البيانات sales
___(sales)
= nrow
```

```quiz
? ماذا يرجع sales[sales$amount > 900, ]؟
* كل أعمدة الصفوف التي فيها amount أكبر من 900
- عمود amount فقط
- عدد الصفوف
```

# @lesson r-apply
title: عائلة apply
summary: sapply و lapply و apply و Map بدل الحلقات.
---
```try r
nums <- list(a = 1:5, b = c(10, 20), c = c(2, 4, 6, 8))
lapply(nums, mean)              # ترجع قائمة
sapply(nums, mean)              # تبسّط إلى متجه
sapply(nums, function(v) max(v) - min(v))

words <- c("tea", "coffee", "cake")
sapply(words, nchar)
vapply(words, toupper, character(1))   # مثل sapply مع نوع نتيجة ثابت

m <- matrix(1:6, nrow = 2)
m
apply(m, 1, sum)                # 1 = لكل صف
apply(m, 2, max)                # 2 = لكل عمود

Map(function(x, y) x * y, 1:3, 4:6)
Reduce(`+`, 1:5, accumulate = TRUE)
Filter(function(x) x %% 2 == 0, 1:10)
```

```reference r
lapply(x, f) | طبّق f على كل عنصر وأرجع قائمة | lapply(files, read.csv)
sapply(x, f) | نفس الشيء مع التبسيط إلى متجه | sapply(df, class)
vapply(x, f, type) | نفس الشيء مع نوع مفحوص | vapply(x, nchar, integer(1))
apply(m, 1 / 2, f) | على صفوف / أعمدة المصفوفة | apply(m, 2, mean)
Map(f, a, b) | مزاوجة عدة متجهات | Map(paste, a, b)
Filter / Reduce | الإبقاء على المطابق / الطيّ | Reduce(`+`, v)
```

```exercise r
? احسب متوسط كل عنصر في القائمة nums كمتجه بسيط
___(nums, mean)
= sapply
```

```quiz
? ما الفرق بين lapply و sapply؟
* lapply ترجع قائمة دائمًا و sapply تبسّط النتيجة عندما تستطيع
- sapply تعمل مع الأرقام فقط
- lapply لإطارات البيانات فقط
```

# @lesson r-strings
title: التعامل مع النصوص
summary: paste و sprintf و nchar و substr و toupper و grepl و sub و strsplit.
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
grepl("@", emails)                       # أيها يحتوي @
sub("@.*", "", emails)                   # احذف من @ حتى النهاية
gsub("a", "A", "banana")
strsplit("tea,coffee,cake", ",")[[1]]
format(1234567.891, big.mark = ",", nsmall = 2)
```

```reference r
paste / paste0 | دمج النصوص (بمسافات / بدونها) | paste0("id_", 1:3)
sprintf | نص منسق | sprintf("%.1f%%", 12.34)
nchar | عدد الحروف | nchar("مرحبا")
substr(x, start, stop) | جزء من النص | substr(s, 1, 3)
toupper / tolower / trimws | حالة الأحرف والمسافات | trimws(x)
grepl(pattern, x) | هل يطابق؟ (TRUE/FALSE) | grepl("^A", names)
sub / gsub | استبدال الأول / الكل | gsub(" ", "_", x)
strsplit(x, sep) | التقسيم إلى أجزاء | strsplit("a b", " ")
```

```exercise r
? ادمج "id_" مع 1:3 بدون مسافات
___("id_", 1:3)
= paste0
```

```quiz
? أي دالة تفحص هل يحتوي كل نص على نمط معين؟
* grepl
- sub
- nchar
```

# @lesson r-stats
title: الإحصاء والمخططات
summary: إحصاءات التلخيص والارتباط ونموذج خطي ومخططات R الأساسية.
---
```try r
set.seed(1)                                   # نفس الأرقام العشوائية في كل تشغيل
hours <- c(2, 3, 5, 6, 8, 9, 10, 12)
score <- c(55, 60, 65, 70, 78, 80, 85, 92)

mean(score); median(score); sd(score)
quantile(score)
cor(hours, score)                             # الارتباط

model <- lm(score ~ hours)                    # ارسم خطًا مستقيمًا مناسبًا
coef(model)
round(summary(model)$r.squared, 3)
predict(model, data.frame(hours = 7))

sample(1:6, 5, replace = TRUE)                # ارمِ النرد خمس مرات
round(rnorm(3, mean = 100, sd = 15))          # قيم عشوائية طبيعية التوزيع
t.test(score, mu = 60)$p.value < 0.05
```

تفتح المخططات في نافذة الرسم في RStudio (ولا يمكن عرضها في هذا الناتج النصي):

```text
plot(hours, score, main = "Study time and score", xlab = "Hours", ylab = "Score")
abline(model, col = "red")
hist(score, breaks = 5)
barplot(table(c("A", "B", "A", "C")))
boxplot(amount ~ branch, data = sales)
```

```reference r
mean / median / sd / var | المركز والتشتت | sd(x)
quantile / summary | الربيعيات / نظرة عامة | quantile(x, 0.9)
cor(x, y) | الارتباط | cor(df$a, df$b)
lm(y ~ x) | الانحدار الخطي | model <- lm(price ~ size, data = df)
predict(model, newdata) | توقع قيم جديدة | predict(model, data.frame(size = 90))
set.seed / sample / rnorm | الأرقام العشوائية | sample(1:10, 3)
t.test | مقارنة المتوسطات | t.test(a, b)
plot / hist / barplot / boxplot | المخططات الأساسية | hist(df$age)
```

:::tip ggplot2 للمخططات الاحترافية
تبني حزمة **ggplot2** المخططات على طبقات: `ggplot(df, aes(hours, score)) + geom_point() + geom_smooth(method = "lm")`. ثبّتها بـ `install.packages("ggplot2")`.
:::

```exercise r
? ابنِ نموذجًا خطيًا لـ score بدلالة hours
model <- ___(score ~ hours)
= lm
```

```quiz
? ماذا تفعل set.seed(1)؟
* تجعل الأرقام العشوائية تتكرر بنفس الشكل في كل تشغيل
- تلغي العشوائية تمامًا
- تضبط أول قيمة في متجه

? قيمة cor(x, y) القريبة من 1 تعني علاقة طردية قوية.
= true
```

# @lesson r-reference
title: مرجع R السريع
summary: أكثر الصيغ والدوال استخدامًا في صفحة واحدة.
---
```reference r
x <- v | الإسناد | n <- 10
c() / 1:n / seq() | المتجهات | v <- c(2, 4, 6)
v[1] / v[v > 2] | الفهرسة (من 1) / التصفية | v[-1]
if / else / ifelse | الشروط | ifelse(v > 0, "+", "-")
for / while | الحلقات | for (i in 1:n) { }
f <- function(x) { } | الدوال | sq <- function(x) x^2
list() / $ | القوائم | p$name
factor() / table() | الفئات والأعداد | table(df$city)
data.frame() / df[r, c] | الجداول | df[df$age > 30, ]
subset / aggregate / order | التصفية والتجميع والترتيب | aggregate(y ~ g, df, mean)
sapply / lapply / apply | تطبيق دالة | sapply(df, mean)
paste0 / sprintf / gsub | النصوص | sprintf("%.2f", x)
mean / sd / cor / lm | الإحصاء | lm(y ~ x, data = df)
read.csv / write.csv | الملفات | read.csv("data.csv")
```

:::tip الخطوة التالية
حمّل ملف CSV حقيقيًا بـ `read.csv`، واستكشفه بـ `summary` و `table`، وأجب عن سؤال واحد بـ `aggregate` ومخطط. ثم تعلّم tidyverse (`dplyr` و `ggplot2`) لأسلوب عمل حديث مع البيانات.
:::

```quiz
? أي بنية هي الأنسب لجدول بيانات بأعمدة مسماة؟
* إطار البيانات (data frame)
- متجه واحد
- عامل (factor)
```
