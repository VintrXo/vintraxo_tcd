# @lesson cs-intro
title: C# introduction
summary: What C# is, and your first program.
---
**C#** (said "C sharp") is a Microsoft language that runs on the **.NET** platform. It is used for enterprise applications, web servers with ASP.NET, Windows apps, and games with the **Unity** engine.

```try csharp
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, C#");
        Console.WriteLine(6 * 7);
    }
}
```

- `using System;` lets you use `Console` directly.
- The program starts at the `Main` method.
- `Console.WriteLine` prints a line.

:::info Running the examples
C# examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: install the .NET SDK, then `dotnet new console` and `dotnet run`.
:::

```quiz
? Where does a C# program start running?
* At the Main method
- At the first class
- At the last line

? C# is used to program games with the Unity engine.
= true
```

# @lesson cs-variables
title: Variables and types
summary: int, double, decimal, bool, string, var and const.
---
```try csharp
using System;

class Program
{
    static void Main()
    {
        int age = 25;
        double height = 1.65;
        decimal price = 19.99m;      // decimal for money
        bool active = true;
        char grade = 'A';
        string name = "Sara";
        const decimal Tax = 0.15m;
        var total = price * (1 + Tax);
        Console.WriteLine($"{name} {age} {height} {active} {grade}");
        Console.WriteLine($"Total: {total:0.00}");
    }
}
```

```reference csharp
int / long | Whole numbers | int n = 5;
double | Decimal number | double d = 3.14;
decimal | Exact, for money (suffix m) | decimal p = 9.99m;
bool | True or false | bool ok = true;
char / string | Character / text | string s = "hi";
var | Infers the type | var list = new List<int>();
const | Constant | const int Max = 10;
$"…{x}…" | Values inside text | $"Age: {age}"
```

:::tip decimal for money
`double` can give `0.1 + 0.2 = 0.30000000000000004`. Use `decimal` for prices and financial calculations.
:::

```exercise csharp
? Put the variable name inside the text
Console.WriteLine(___"Hello {name}");
= $
```

```quiz
? Which type suits money amounts best?
- double
* decimal
- float

? var makes the compiler infer the type.
= true
```

# @lesson cs-strings
title: Strings and operators
summary: string methods, comparison, and integer division.
---
```try csharp
using System;

class Program
{
    static void Main()
    {
        string s = "Hello C#";
        Console.WriteLine(s.Length);
        Console.WriteLine(s.ToUpper());
        Console.WriteLine(s.Contains("C#"));
        Console.WriteLine(s.Substring(0, 5));
        Console.WriteLine(s.Replace("C#", "World"));
        Console.WriteLine(string.Join(", ", s.Split(' ')));
        Console.WriteLine("abc" == "abc");            // in C#, == compares string content

        int a = 17, b = 5;
        Console.WriteLine($"{a / b} {a % b} {(double)a / b}");
    }
}
```

```reference csharp
Length | Length | s.Length
ToUpper / ToLower | Change case | s.ToUpper()
Contains / StartsWith | Searching | s.Contains("x")
Substring | Part of the string | s.Substring(0, 3)
Replace | Replace | s.Replace("a", "b")
Split / string.Join | Split and join | s.Split(',')
Trim | Remove spaces | s.Trim()
int.Parse / int.TryParse | String to number | int.TryParse("5", out var n)
```

:::info Unlike Java
In C#, `==` between two strings compares their **content**, so you do not need `Equals` in normal cases.
:::

```quiz
? What is 17 / 5 when both numbers are int?
* 3
- 3.4
- 4

? In C#, "abc" == "abc" is true.
= true
```

# @lesson cs-control
title: Conditions and loops
summary: if, switch, for, while and foreach.
---
```try csharp
using System;

class Program
{
    static void Main()
    {
        int score = 82;
        if (score >= 90) Console.WriteLine("Excellent");
        else if (score >= 75) Console.WriteLine("Very good");
        else Console.WriteLine("Try again");

        string level = score >= 60 ? "pass" : "fail";
        Console.WriteLine(level);

        for (int i = 1; i <= 5; i++) Console.Write(i + " ");
        Console.WriteLine();

        int n = 3;
        while (n > 0) { Console.WriteLine("count " + n); n--; }

        string[] cities = { "Riyadh", "Jeddah", "Dammam" };
        foreach (var city in cities) Console.WriteLine(city);

        switch (score / 10)
        {
            case 9: Console.WriteLine("A"); break;
            case 8: Console.WriteLine("B"); break;
            default: Console.WriteLine("C or less"); break;
        }
    }
}
```

:::info break in switch
In C# every case must end with `break` (or `return`); falling through to the next case is not allowed.
:::

```exercise csharp
? Complete the loop over the array cities
___ (var city in cities) { Console.WriteLine(city); }
= foreach
```

```quiz
? Which loop goes over every item of a collection in the simplest form?
* foreach
- do-while
- switch

? In C# every switch case must end with break or return.
= true
```

# @lesson cs-arrays-lists
title: Arrays and lists
summary: Arrays, List, and Dictionary.
---
```try csharp
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        int[] scores = { 88, 72, 95, 60 };
        Array.Sort(scores);
        Console.WriteLine(string.Join(", ", scores) + " | length " + scores.Length);

        var names = new List<string> { "Sara", "Omar" };
        names.Add("Layla");
        names.Remove("Omar");
        Console.WriteLine(string.Join(", ", names) + " | count " + names.Count);

        var stock = new Dictionary<string, int> { ["pen"] = 120, ["notebook"] = 40 };
        stock["pen"] += 30;
        if (stock.TryGetValue("bag", out int bags)) Console.WriteLine(bags);
        else Console.WriteLine("no bags");
        foreach (var item in stock) Console.WriteLine($"{item.Key} -> {item.Value}");
    }
}
```

```reference csharp
int[] | Fixed-length array | int[] a = { 1, 2 };
List<T> | A list that grows and shrinks | var l = new List<int>(); l.Add(1);
Dictionary<K,V> | Key and value | d["a"] = 1;
TryGetValue | Safe read | d.TryGetValue(k, out var v)
Count / Length | Count | list.Count
HashSet<T> | No repeats | new HashSet<int>()
```

```exercise csharp
? Add an item to the list
names.___("Khaled");
= Add
```

```quiz
? What is the difference between an array and a List in C#?
* A List grows and shrinks; an array has a fixed length
- There is no difference
- Arrays are only for text

? TryGetValue reads from a Dictionary without an error when the key is missing.
= true
```

# @lesson cs-methods
title: Methods
summary: Definitions, optional and named arguments, out, and overloading.
---
```try csharp
using System;

class Program
{
    static int Square(int x) => x * x;

    static string Greet(string name, string title = "")
        => title == "" ? $"Hello {name}" : $"Hello {title} {name}";

    static bool TryDivide(double a, double b, out double result)
    {
        if (b == 0) { result = 0; return false; }
        result = a / b;
        return true;
    }

    static double Area(double r) => Math.PI * r * r;
    static double Area(double w, double h) => w * h;     // overloading

    static void Main()
    {
        Console.WriteLine(Square(7));
        Console.WriteLine(Greet("Sara"));
        Console.WriteLine(Greet(title: "Dr.", name: "Omar"));   // named arguments
        if (TryDivide(10, 4, out double r)) Console.WriteLine(r);
        Console.WriteLine($"{Area(1):0.00} {Area(2, 3)}");
    }
}
```

- `=>` is a short form for a one-line method.
- `out` lets a method return an extra value.

```quiz
? What does out do on a method parameter?
* Lets the method return an extra value through the parameter
- Makes the parameter optional
- Stops the parameter from changing

? Arguments can be passed by name, as in title: "Dr.".
= true
```

# @lesson cs-classes
title: Classes and properties
summary: Fields, properties and the constructor.
---
```try csharp
using System;

class Account
{
    public string Owner { get; }               // read-only property
    public decimal Balance { get; private set; }

    public Account(string owner, decimal balance)
    {
        Owner = owner;
        Balance = balance;
    }

    public void Deposit(decimal amount)
    {
        if (amount <= 0) throw new ArgumentException("Invalid amount");
        Balance += amount;
    }

    public override string ToString() => $"{Owner}: {Balance:0.00}";
}

class Program
{
    static void Main()
    {
        var acc = new Account("Sara", 100m);
        acc.Deposit(50m);
        Console.WriteLine(acc);
        Console.WriteLine(acc.Balance);
    }
}
```

- A **property** `{ get; private set; }`: everyone can read it, only the class can change it.
- `override ToString` decides how the object prints.

```exercise csharp
? A property everyone can read and only the class can change
public decimal Balance { get; ___ set; }
= private
```

```quiz
? What is private set on a property for?
* Everyone can read it; only code inside the class can change it
- It hides the property completely
- It makes it constant forever

? Overriding ToString decides how the object prints.
= true
```

# @lesson cs-inheritance
title: Inheritance and interfaces
summary: Inheritance, abstract, interface, and polymorphism.
---
```try csharp
using System;
using System.Collections.Generic;

interface IShape
{
    double Area();
}

abstract class Shape : IShape
{
    public abstract double Area();
    public override string ToString() => $"{GetType().Name}: {Area():0.00}";
}

class Circle : Shape
{
    private readonly double r;
    public Circle(double r) { this.r = r; }
    public override double Area() => Math.PI * r * r;
}

class Rect : Shape
{
    protected readonly double W, H;
    public Rect(double w, double h) { W = w; H = h; }
    public override double Area() => W * H;
}

class Square : Rect
{
    public Square(double s) : base(s, s) { }
}

class Program
{
    static void Main()
    {
        var shapes = new List<IShape> { new Circle(1), new Rect(2, 3), new Square(4) };
        foreach (var s in shapes) Console.WriteLine(s);
    }
}
```

- `:` is used for inheritance and implementing interfaces, and `base(...)` calls the parent's constructor.
- An `abstract` method has no body; children must define it with `override`.
- Interface names usually start with the letter `I`.

```quiz
? How do you call the parent class's constructor in C#?
- super(...)
* base(...)
- parent(...)

? An abstract method must be defined by the child class with override.
= true
```

# @lesson cs-linq
title: LINQ
summary: Querying collections: Where, Select, OrderBy, Sum and GroupBy.
---
**LINQ** lets you query data inside your code, much like SQL:

```try csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main()
    {
        var products = new List<(string Name, string Category, decimal Price)>
        {
            ("Laptop", "Electronics", 3500m),
            ("Pen", "Stationery", 5m),
            ("Phone", "Electronics", 2200m),
            ("Notebook", "Stationery", 15m),
        };

        var expensive = products.Where(p => p.Price > 100).OrderByDescending(p => p.Price).Select(p => p.Name);
        Console.WriteLine(string.Join(", ", expensive));
        Console.WriteLine(products.Sum(p => p.Price));
        foreach (var g in products.GroupBy(p => p.Category))
            Console.WriteLine($"{g.Key}: {g.Count()} items, {g.Sum(p => p.Price)}");
        Console.WriteLine(products.Any(p => p.Price < 10));
    }
}
```

```reference csharp
Where | Filter | list.Where(x => x > 0)
Select | Transform | list.Select(x => x.Name)
OrderBy / OrderByDescending | Sort | list.OrderBy(x => x.Price)
Sum / Average / Count | Aggregate | list.Sum(x => x.Price)
GroupBy | Group by a key | list.GroupBy(x => x.Category)
First / FirstOrDefault | First item | list.FirstOrDefault(x => x.Id == 3)
Any / All | Do some / all pass? | list.Any(x => x < 0)
ToList | To a list | query.ToList()
```

```exercise csharp
? Keep the positive numbers
var positive = nums.___(n => n > 0);
= Where
```

```quiz
? Which LINQ method turns each item into a new value?
- Where
* Select
- Any

? GroupBy groups items by a key.
= true
```

# @lesson cs-exceptions
title: Exceptions
summary: try, catch, finally, throw and using.
---
```try csharp
using System;

class Program
{
    static int ParseAge(string text)
    {
        int age = int.Parse(text);               // may throw FormatException
        if (age < 0) throw new ArgumentException("Age cannot be negative");
        return age;
    }

    static void Main()
    {
        foreach (var input in new[] { "25", "abc", "-3" })
        {
            try
            {
                Console.WriteLine("Age: " + ParseAge(input));
            }
            catch (FormatException)
            {
                Console.WriteLine("Not a number: " + input);
            }
            catch (ArgumentException e)
            {
                Console.WriteLine("Error: " + e.Message);
            }
            finally
            {
                Console.WriteLine("---");
            }
        }
    }
}
```

:::tip using for resources
`using (var file = File.OpenRead("a.txt")) { … }` closes the file automatically, even when an exception happens.
:::

```quiz
? Which part always runs?
- try
- catch
* finally

? int.Parse("abc") throws a FormatException.
= true
```

# @lesson cs-project
title: Project: inventory management
summary: A program that combines classes, lists, LINQ and exceptions.
---
```try csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Product
{
    public string Name { get; }
    public decimal Price { get; }
    public int Qty { get; set; }
    public Product(string name, decimal price, int qty) { Name = name; Price = price; Qty = qty; }
    public decimal Value => Price * Qty;
}

class Inventory
{
    private readonly Dictionary<string, Product> items = new Dictionary<string, Product>();

    public void Add(Product p) => items[p.Name] = p;

    public void Sell(string name, int count)
    {
        if (!items.TryGetValue(name, out var p)) throw new KeyNotFoundException("Not found: " + name);
        if (count > p.Qty) throw new InvalidOperationException("Not enough stock: " + name);
        p.Qty -= count;
    }

    public decimal TotalValue => items.Values.Sum(p => p.Value);
    public IEnumerable<string> LowStock(int limit) => items.Values.Where(p => p.Qty < limit).Select(p => p.Name);
}

class Program
{
    static void Main()
    {
        var inv = new Inventory();
        inv.Add(new Product("pen", 5m, 120));
        inv.Add(new Product("notebook", 12m, 8));
        inv.Add(new Product("bag", 90m, 3));
        inv.Sell("pen", 20);
        try { inv.Sell("bag", 5); }
        catch (InvalidOperationException e) { Console.WriteLine(e.Message); }
        Console.WriteLine($"Stock value: {inv.TotalValue:0.00}");
        Console.WriteLine("Low stock: " + string.Join(", ", inv.LowStock(10)));
    }
}
```

```quiz
? What kind of member is Value in the Product class?
* A property computed from price and quantity
- A stored field
- A static method

? LINQ's Sum adds up the items' values.
= true
```

# @lesson cs-reference
title: C# reference
summary: The most important keywords and types with an example for each.
type: Reference
---
Search the table for any keyword.

```reference csharp
using | Import a namespace | using System.Linq;
class / Main | Class and entry point | static void Main() { }
Console.WriteLine | Print | Console.WriteLine("…");
int / decimal / string | Types | decimal p = 9.5m;
var / const | Inference / constant | var x = 5;
$"…" | Text with values | $"Total: {t}"
if / switch | Conditions | if (x > 0) { }
for / foreach / while | Loops | foreach (var x in list) { }
List / Dictionary | Collections | new List<int>()
=> | Short method | int Sq(int x) => x * x;
out | Extra return value | int.TryParse(s, out var n)
{ get; set; } | Properties | public int Age { get; set; }
: / base | Inheritance | class B : A { }
interface / abstract | Interfaces and abstraction | interface IShape { }
override | Redefine | public override string ToString()
LINQ | Querying | list.Where(…).Select(…)
try / catch / finally | Exceptions | try { } catch (Exception e) { }
throw | Throw an exception | throw new ArgumentException("…");
```

:::tip What next?
Install the .NET SDK and Visual Studio Code, and try ASP.NET Core to build APIs, or Unity to build a small game.
:::
