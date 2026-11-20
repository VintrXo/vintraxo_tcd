# @lesson go-intro
title: مقدمة في Go
summary: ما هي لغة Go، وأول برنامج.
---
**Go** (أو Golang) لغة صممتها Google: بسيطة، سريعة الترجمة والتشغيل، وممتازة في البرامج المتزامنة. تُستخدم بكثرة في الخوادم والسحابة؛ Docker و Kubernetes مكتوبان بها.

```try go
package main

import "fmt"

func main() {
	fmt.Println("Hello, Go")
	fmt.Println(6 * 7)
}
```

- كل ملف يبدأ بـ `package`، والبرنامج التنفيذي حزمته `main`.
- `import "fmt"` مكتبة التنسيق والطباعة.
- البرنامج يبدأ من الدالة `main`.

:::info تشغيل الأمثلة
أمثلة Go تعمل على خادم آمن منفصل؛ إذا لم يكن مفعّلًا بعد ستعمل فور تفعيله. على جهازك: `go run main.go`.
:::

```quiz
? ما اسم الحزمة في البرنامج التنفيذي؟
* main
- app
- go

? لغة Go صممتها شركة Google.
= true
```

# @lesson go-variables
title: المتغيرات والأنواع
summary: var و := والثوابت والأنواع الأساسية.
---
```try go
package main

import "fmt"

func main() {
	var age int = 25
	price := 19.99            // تعريف مختصر يستنتج النوع
	name := "Sara"
	active := true
	const tax = 0.15
	var count int             // القيمة الصفرية: 0
	fmt.Println(name, age, active, count)
	fmt.Printf("total: %.2f, type: %T\n", price*(1+tax), price)
}
```

```reference go
var x int | تعريف متغير | var n int = 5
:= | تعريف مختصر داخل الدوال | name := "Sara"
const | ثابت | const pi = 3.14
int / float64 | أعداد | var f float64
string / bool | نص / منطقي | ok := true
%v / %T / %.2f | التنسيق مع Printf | fmt.Printf("%v %T", x, x)
```

:::tip القيمة الصفرية
المتغير غير المهيأ يأخذ قيمة صفرية: `0` للأرقام، `""` للنصوص، `false` للمنطقي، `nil` للمؤشرات والشرائح.
:::

```exercise go
? عرّف متغيرًا مختصرًا اسمه city قيمته "Riyadh"
city ___ "Riyadh"
= :=
```

```quiz
? ما القيمة الصفرية لمتغير int غير مهيأ؟
* 0
- nil
- undefined

? المتغير المعرّف بـ := يُستنتج نوعه تلقائيًا.
= true
```

# @lesson go-control
title: الشروط والحلقات
summary: if و switch، و for بأشكالها الثلاثة.
---
Go فيها حلقة واحدة فقط: `for`، تُكتب بعدة أشكال:

```try go
package main

import "fmt"

func main() {
	score := 82
	if score >= 90 {
		fmt.Println("Excellent")
	} else if score >= 75 {
		fmt.Println("Very good")
	} else {
		fmt.Println("Try again")
	}

	for i := 1; i <= 5; i++ {
		fmt.Print(i, " ")
	}
	fmt.Println()

	n := 3
	for n > 0 { // مثل while
		fmt.Println("count", n)
		n--
	}

	switch day := 5; day {
	case 5:
		fmt.Println("Friday")
	case 6, 7:
		fmt.Println("Weekend")
	default:
		fmt.Println("Weekday")
	}
}
```

- لا أقواس حول الشرط، والأقواس المعقوفة إلزامية.
- `switch` لا تحتاج `break`؛ تتوقف تلقائيًا بعد الحالة المطابقة.

```quiz
? كم نوعًا من الحلقات في Go؟
* واحدة فقط: for
- ثلاثة: for و while و do
- لا توجد حلقات

? الحالة في switch في Go لا تحتاج break.
= true
```

# @lesson go-slices
title: الشرائح slices
summary: المصفوفات والشرائح و append و range.
---
**الشريحة** قائمة ديناميكية، وهي الأكثر استخدامًا في Go:

```try go
package main

import (
	"fmt"
	"sort"
)

func main() {
	nums := []int{5, 2, 9, 1}
	nums = append(nums, 7)
	fmt.Println(nums, len(nums))
	fmt.Println(nums[1:3])

	sort.Ints(nums)
	fmt.Println(nums)

	total := 0
	for i, v := range nums {
		fmt.Println("index", i, "value", v)
		total += v
	}
	fmt.Println("total:", total)

	names := make([]string, 0, 10) // شريحة فارغة بسعة 10
	names = append(names, "Ali", "Mona")
	fmt.Println(names)
}
```

```reference go
[]T{…} | شريحة بقيم | []int{1, 2, 3}
append | إضافة | s = append(s, 4)
len / cap | الطول / السعة | len(s)
s[a:b] | جزء من الشريحة | s[1:3]
range | المرور مع الفهرس | for i, v := range s
make | إنشاء بحجم | make([]int, 0, 10)
sort.Ints / sort.Strings | الترتيب | sort.Ints(s)
```

```exercise go
? أضف الرقم 4 إلى الشريحة
s = ___(s, 4)
= append
```

```quiz
? ماذا تعيد range على شريحة؟
* الفهرس والقيمة
- القيمة فقط
- الطول فقط

? يجب إسناد ناتج append للشريحة مرة أخرى.
= true
```

# @lesson go-maps
title: الخرائط maps
summary: مفتاح وقيمة، والإضافة والحذف، والتحقق من الوجود.
---
```try go
package main

import (
	"fmt"
	"sort"
)

func main() {
	stock := map[string]int{"pen": 120, "notebook": 40}
	stock["bag"] = 5
	stock["pen"] += 30
	delete(stock, "notebook")

	if qty, ok := stock["bag"]; ok {
		fmt.Println("bag:", qty)
	}
	if _, ok := stock["ruler"]; !ok {
		fmt.Println("no ruler")
	}

	keys := make([]string, 0, len(stock))
	for k := range stock {
		keys = append(keys, k)
	}
	sort.Strings(keys) // ترتيب الخريطة غير ثابت؛ نرتب المفاتيح للعرض
	for _, k := range keys {
		fmt.Println(k, stock[k])
	}
}
```

- `value, ok := m[key]` يخبرك إن كان المفتاح موجودًا.
- ترتيب المرور على الخريطة **عشوائي**؛ رتّب المفاتيح إن احتجت ترتيبًا.

```quiz
? كيف تعرف إن كان مفتاح موجودًا في الخريطة؟
* v, ok := m[key]
- m.has(key)
- key in m

? ترتيب المرور على الخريطة في Go ثابت دائمًا.
= false
```

# @lesson go-functions
title: الدوال
summary: المعاملات، وإرجاع عدة قيم، والدوال المجهولة.
---
```try go
package main

import "fmt"

func square(x int) int {
	return x * x
}

func divide(a, b float64) (float64, error) { // إرجاع قيمتين
	if b == 0 {
		return 0, fmt.Errorf("cannot divide by zero")
	}
	return a / b, nil
}

func sum(nums ...int) int { // عدد غير محدد من المعاملات
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func main() {
	fmt.Println(square(7))
	if r, err := divide(10, 4); err == nil {
		fmt.Println(r)
	}
	if _, err := divide(1, 0); err != nil {
		fmt.Println("error:", err)
	}
	fmt.Println(sum(1, 2, 3, 4))

	double := func(x int) int { return x * 2 } // دالة مجهولة
	fmt.Println(double(21))
}
```

- النوع بعد اسم المعامل: `x int`.
- الدوال تُرجع **عدة قيم**، وأشهرها `(نتيجة, error)`.

```quiz
? ما النمط الشائع لإرجاع الأخطاء في Go؟
* إرجاع قيمتين: النتيجة و error
- رمي استثناء بـ throw
- طباعة الخطأ فقط

? الرمز _ يتجاهل قيمة لا نحتاجها.
= true
```

# @lesson go-structs
title: الهياكل والدوال المرتبطة
summary: struct، والدوال على الهيكل، والمؤشرات.
---
```try go
package main

import "fmt"

type Account struct {
	Owner   string
	Balance float64
}

func (a *Account) Deposit(amount float64) { // مستقبِل بمؤشر: يعدّل الأصل
	a.Balance += amount
}

func (a Account) String() string { // يُستخدم تلقائيًا عند الطباعة
	return fmt.Sprintf("%s: %.2f", a.Owner, a.Balance)
}

func main() {
	acc := Account{Owner: "Sara", Balance: 100}
	acc.Deposit(50)
	fmt.Println(acc)

	p := &acc
	p.Deposit(25)
	fmt.Println(acc.Balance)
}
```

- لا أصناف في Go؛ الهيكل `struct` مع دوال مرتبطة به.
- المستقبِل بمؤشر `(a *Account)` يعدّل الهيكل الأصلي.
- الحقول التي تبدأ بحرف كبير **عامة** (تُرى من حزم أخرى).

```quiz
? ما فائدة المستقبِل بمؤشر (a *Account)؟
* أن تعدّل الدالة الهيكل الأصلي
- أن تكون الدالة خاصة
- لا فائدة

? الحقل الذي يبدأ بحرف كبير في Go يكون عامًا.
= true
```

# @lesson go-interfaces
title: الواجهات
summary: الواجهة ضمنية: أي نوع فيه الدوال المطلوبة يحققها.
---
```try go
package main

import (
	"fmt"
	"math"
)

type Shape interface {
	Area() float64
}

type Circle struct{ R float64 }
type Rect struct{ W, H float64 }

func (c Circle) Area() float64 { return math.Pi * c.R * c.R }
func (r Rect) Area() float64   { return r.W * r.H }

func total(shapes []Shape) float64 {
	sum := 0.0
	for _, s := range shapes {
		sum += s.Area()
	}
	return sum
}

func main() {
	shapes := []Shape{Circle{1}, Rect{2, 3}}
	for _, s := range shapes {
		fmt.Printf("%T: %.2f\n", s, s.Area())
	}
	fmt.Printf("total: %.2f\n", total(shapes))
}
```

لا توجد كلمة `implements`؛ يحقق النوع الواجهة **تلقائيًا** إذا كانت فيه دوالها.

```quiz
? كيف يحقق النوع واجهة في Go؟
* تلقائيًا إذا عرّف كل دوالها
- بكلمة implements
- بكلمة extends

? يمكن وضع أنواع مختلفة في شريحة من نوع الواجهة.
= true
```

# @lesson go-errors
title: الأخطاء و defer
summary: error، و errors.New، و defer، و panic.
---
```try go
package main

import (
	"errors"
	"fmt"
	"strconv"
)

var ErrNegative = errors.New("age cannot be negative")

func parseAge(text string) (int, error) {
	n, err := strconv.Atoi(text)
	if err != nil {
		return 0, fmt.Errorf("not a number %q: %w", text, err)
	}
	if n < 0 {
		return 0, ErrNegative
	}
	return n, nil
}

func main() {
	defer fmt.Println("done (defer runs last)")
	for _, in := range []string{"25", "abc", "-3"} {
		age, err := parseAge(in)
		switch {
		case errors.Is(err, ErrNegative):
			fmt.Println("negative:", in)
		case err != nil:
			fmt.Println("error:", err)
		default:
			fmt.Println("age:", age)
		}
	}
}
```

- الأخطاء **قيم عادية** تفحصها بـ `if err != nil`.
- `defer` يؤجل تنفيذ سطر حتى نهاية الدالة (إغلاق ملف، تحرير مورد).
- `panic` للأخطاء الكارثية فقط.

```quiz
? متى يُنفَّذ السطر الذي يسبقه defer؟
* عند انتهاء الدالة
- فورًا
- عند حدوث خطأ فقط

? في Go نفحص الخطأ عادة بـ if err != nil.
= true
```

# @lesson go-goroutines
title: التزامن goroutines و channels
summary: تشغيل دوال بالتوازي، والتواصل بالقنوات، و WaitGroup.
---
**goroutine** دالة تعمل بالتوازي بكلمة `go`، و**القناة** طريقة آمنة لتبادل البيانات بينها:

```try go
package main

import (
	"fmt"
	"sync"
)

func square(n int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	results <- n * n
}

func main() {
	results := make(chan int, 5)
	var wg sync.WaitGroup
	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go square(i, results, &wg)
	}
	wg.Wait()
	close(results)

	sum := 0
	for r := range results {
		sum += r
	}
	fmt.Println("sum of squares:", sum)
}
```

- `go f()` يشغّل الدالة في goroutine جديدة؛ آلاف منها خفيفة جدًا.
- `ch <- v` يرسل، و`v := <-ch` يستقبل.
- `sync.WaitGroup` ينتظر انتهاء مجموعة goroutines.

:::tip شعار Go
«لا تتواصل بمشاركة الذاكرة؛ شارك الذاكرة بالتواصل». القنوات تمنع كثيرًا من أخطاء التزامن.
:::

```quiz
? أي كلمة تشغّل دالة بالتوازي في Go؟
* go
- async
- thread

? الأداة sync.WaitGroup تنتظر انتهاء مجموعة goroutines.
= true
```

# @lesson go-reference
title: مرجع Go
summary: أهم الكلمات والحزم مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة.

```reference go
package / import | الحزم | import "fmt"
func | دالة | func add(a, b int) int { return a + b }
var / := / const | المتغيرات | x := 5
if / switch | الشروط | if err != nil { … }
for / range | الحلقة الوحيدة | for i, v := range s { … }
[]T / append | الشرائح | s = append(s, x)
map[K]V | الخرائط | m := map[string]int{}
struct | الهياكل | type P struct { X int }
(r T) Method() | دالة على نوع | func (p P) Show() {}
interface | الواجهات | type Shape interface { Area() float64 }
error / errors.New | الأخطاء | return errors.New("…")
defer | التأجيل لنهاية الدالة | defer f.Close()
go | goroutine | go worker()
chan / <- | القنوات | ch <- 1; v := <-ch
fmt.Println / Printf | الطباعة | fmt.Printf("%v\n", x)
strconv.Atoi | نص إلى رقم | n, err := strconv.Atoi("5")
```

:::tip ماذا بعد؟
ثبّت Go، وابنِ خادم ويب صغيرًا بحزمة `net/http` المدمجة؛ لا تحتاج أي مكتبة خارجية.
:::
