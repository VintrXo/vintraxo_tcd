# @lesson go-intro
title: Go introduction
summary: What the Go language is, and your first program.
---
**Go** (or Golang) is a language designed at Google: simple, quick to compile and run, and excellent for concurrent programs. It is widely used for servers and the cloud; Docker and Kubernetes are written in it.

```try go
package main

import "fmt"

func main() {
	fmt.Println("Hello, Go")
	fmt.Println(6 * 7)
}
```

- Every file starts with `package`, and an executable program's package is `main`.
- `import "fmt"` is the formatting and printing library.
- The program starts at the `main` function.

:::info Running the examples
Go examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: `go run main.go`.
:::

```quiz
? What is the package name of an executable program?
* main
- app
- go

? Go was designed at Google.
= true
```

# @lesson go-variables
title: Variables and types
summary: var, :=, constants and basic types.
---
```try go
package main

import "fmt"

func main() {
	var age int = 25
	price := 19.99            // short declaration, type inferred
	name := "Sara"
	active := true
	const tax = 0.15
	var count int             // zero value: 0
	fmt.Println(name, age, active, count)
	fmt.Printf("total: %.2f, type: %T\n", price*(1+tax), price)
}
```

```reference go
var x int | Declare a variable | var n int = 5
:= | Short declaration inside functions | name := "Sara"
const | Constant | const pi = 3.14
int / float64 | Numbers | var f float64
string / bool | Text / boolean | ok := true
%v / %T / %.2f | Formatting with Printf | fmt.Printf("%v %T", x, x)
```

:::tip Zero values
An uninitialized variable takes a zero value: `0` for numbers, `""` for strings, `false` for booleans, `nil` for pointers and slices.
:::

```exercise go
? Declare a short variable named city with the value "Riyadh"
city ___ "Riyadh"
= :=
```

```quiz
? What is the zero value of an uninitialized int?
* 0
- nil
- undefined

? A variable declared with := has its type inferred automatically.
= true
```

# @lesson go-control
title: Conditions and loops
summary: if and switch, and the three forms of for.
---
Go has only one loop: `for`, written in several forms:

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
	for n > 0 { // like while
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

- No parentheses around the condition, and curly braces are required.
- `switch` needs no `break`; it stops after the matching case.

```quiz
? How many kinds of loop does Go have?
* Only one: for
- Three: for, while and do
- None

? A switch case in Go needs no break.
= true
```

# @lesson go-slices
title: Slices
summary: Arrays and slices, append and range.
---
A **slice** is a dynamic list, and the most used collection in Go:

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

	names := make([]string, 0, 10) // empty slice with capacity 10
	names = append(names, "Ali", "Mona")
	fmt.Println(names)
}
```

```reference go
[]T{…} | A slice with values | []int{1, 2, 3}
append | Add items | s = append(s, 4)
len / cap | Length / capacity | len(s)
s[a:b] | Part of a slice | s[1:3]
range | Loop with the index | for i, v := range s
make | Create with a size | make([]int, 0, 10)
sort.Ints / sort.Strings | Sorting | sort.Ints(s)
```

```exercise go
? Add the number 4 to the slice
s = ___(s, 4)
= append
```

```quiz
? What does range return on a slice?
* The index and the value
- Only the value
- Only the length

? You must assign the result of append back to the slice.
= true
```

# @lesson go-maps
title: Maps
summary: Keys and values, adding and deleting, and checking presence.
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
	sort.Strings(keys) // map order is random; sort the keys to display
	for _, k := range keys {
		fmt.Println(k, stock[k])
	}
}
```

- `value, ok := m[key]` tells you whether the key exists.
- The order of looping over a map is **random**; sort the keys when you need an order.

```quiz
? How do you check whether a key exists in a map?
* v, ok := m[key]
- m.has(key)
- key in m

? The order of looping over a Go map is always the same.
= false
```

# @lesson go-functions
title: Functions
summary: Parameters, returning several values, and anonymous functions.
---
```try go
package main

import "fmt"

func square(x int) int {
	return x * x
}

func divide(a, b float64) (float64, error) { // returns two values
	if b == 0 {
		return 0, fmt.Errorf("cannot divide by zero")
	}
	return a / b, nil
}

func sum(nums ...int) int { // any number of arguments
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

	double := func(x int) int { return x * 2 } // anonymous function
	fmt.Println(double(21))
}
```

- The type comes after the parameter name: `x int`.
- Functions return **several values**, most often `(result, error)`.

```quiz
? What is the usual way to return errors in Go?
* Return two values: the result and an error
- Throw an exception with throw
- Only print the error

? The _ symbol ignores a value we do not need.
= true
```

# @lesson go-structs
title: Structs and methods
summary: struct, methods on a struct, and pointers.
---
```try go
package main

import "fmt"

type Account struct {
	Owner   string
	Balance float64
}

func (a *Account) Deposit(amount float64) { // pointer receiver: changes the original
	a.Balance += amount
}

func (a Account) String() string { // used automatically when printing
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

- Go has no classes; a `struct` gets methods attached to it.
- A pointer receiver `(a *Account)` changes the original struct.
- Fields that start with a capital letter are **exported** (visible from other packages).

```quiz
? What is a pointer receiver (a *Account) for?
* So the method changes the original struct
- So the method is private
- Nothing

? A field that starts with a capital letter in Go is exported.
= true
```

# @lesson go-interfaces
title: Interfaces
summary: Interfaces are implicit: any type with the required methods satisfies them.
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

There is no `implements` keyword; a type satisfies an interface **automatically** when it has its methods.

```quiz
? How does a type satisfy an interface in Go?
* Automatically, when it defines all its methods
- With the keyword implements
- With the keyword extends

? A slice of an interface type can hold different types.
= true
```

# @lesson go-errors
title: Errors and defer
summary: error, errors.New, defer and panic.
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

- Errors are **ordinary values** you check with `if err != nil`.
- `defer` postpones a line until the function ends (closing a file, releasing a resource).
- `panic` is only for disastrous errors.

```quiz
? When does a line preceded by defer run?
* When the function ends
- At once
- Only when an error happens

? In Go you usually check an error with if err != nil.
= true
```

# @lesson go-goroutines
title: Concurrency: goroutines and channels
summary: Running functions in parallel, talking through channels, and WaitGroup.
---
A **goroutine** is a function running concurrently with the keyword `go`, and a **channel** is a safe way to pass data between them:

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

- `go f()` runs the function in a new goroutine; thousands of them are very light.
- `ch <- v` sends, and `v := <-ch` receives.
- `sync.WaitGroup` waits for a group of goroutines to finish.

:::tip Go's motto
"Do not communicate by sharing memory; share memory by communicating." Channels prevent many concurrency bugs.
:::

```quiz
? Which keyword runs a function concurrently in Go?
* go
- async
- thread

? sync.WaitGroup waits for a group of goroutines to finish.
= true
```

# @lesson go-reference
title: Go reference
summary: The most important keywords and packages with an example for each.
type: Reference
---
Search the table for any keyword.

```reference go
package / import | Packages | import "fmt"
func | Function | func add(a, b int) int { return a + b }
var / := / const | Variables | x := 5
if / switch | Conditions | if err != nil { … }
for / range | The only loop | for i, v := range s { … }
[]T / append | Slices | s = append(s, x)
map[K]V | Maps | m := map[string]int{}
struct | Structs | type P struct { X int }
(r T) Method() | A method on a type | func (p P) Show() {}
interface | Interfaces | type Shape interface { Area() float64 }
error / errors.New | Errors | return errors.New("…")
defer | Postpone to the end of the function | defer f.Close()
go | Goroutine | go worker()
chan / <- | Channels | ch <- 1; v := <-ch
fmt.Println / Printf | Printing | fmt.Printf("%v\n", x)
strconv.Atoi | String to number | n, err := strconv.Atoi("5")
```

:::tip What next?
Install Go and build a small web server with the built-in `net/http` package; you need no external library.
:::
