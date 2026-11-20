# @lesson cs-intro
title: مقدمة في C#
summary: ما هي سي شارب، وأول برنامج.
---
**C#** (تُنطق «سي شارب») لغة من Microsoft تعمل على منصة **.NET**. تُستخدم في تطبيقات الشركات، وخوادم الويب بـ ASP.NET، وتطبيقات ويندوز، والألعاب بمحرك **Unity**.

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

- `using System;` يتيح استخدام `Console` مباشرة.
- البرنامج يبدأ من الدالة `Main`.
- `Console.WriteLine` تطبع سطرًا.

:::info تشغيل الأمثلة
أمثلة C# تعمل على خادم آمن منفصل؛ إذا لم يكن مفعّلًا بعد ستعمل فور تفعيله. على جهازك: ثبّت .NET SDK ثم `dotnet new console` و `dotnet run`.
:::

```quiz
? من أين يبدأ تنفيذ برنامج C#؟
* من الدالة Main
- من أول صنف
- من آخر سطر

? لغة C# تُستخدم لبرمجة الألعاب بمحرك Unity.
= true
```

# @lesson cs-variables
title: المتغيرات والأنواع
summary: int و double و decimal و bool و string و var و const.
---
```try csharp
using System;

class Program
{
    static void Main()
    {
        int age = 25;
        double height = 1.65;
        decimal price = 19.99m;      // decimal للمبالغ المالية
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
int / long | أعداد صحيحة | int n = 5;
double | عدد عشري | double d = 3.14;
decimal | دقيق للمال (لاحقة m) | decimal p = 9.99m;
bool | صح أو خطأ | bool ok = true;
char / string | حرف / نص | string s = "hi";
var | يستنتج النوع | var list = new List<int>();
const | ثابت | const int Max = 10;
$"…{x}…" | إدراج قيم في النص | $"Age: {age}"
```

:::tip decimal للمال
`double` قد يعطي `0.1 + 0.2 = 0.30000000000000004`. استخدم `decimal` للأسعار والحسابات المالية.
:::

```exercise csharp
? أدرج المتغير name في النص
Console.WriteLine(___"Hello {name}");
= $
```

```quiz
? أي نوع أنسب للمبالغ المالية؟
- double
* decimal
- float

? الكلمة var تجعل المترجم يستنتج النوع.
= true
```

# @lesson cs-strings
title: النصوص والعمليات
summary: دوال string، والمقارنة، والقسمة الصحيحة.
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
        Console.WriteLine("abc" == "abc");            // في C# تقارن == محتوى النصوص

        int a = 17, b = 5;
        Console.WriteLine($"{a / b} {a % b} {(double)a / b}");
    }
}
```

```reference csharp
Length | الطول | s.Length
ToUpper / ToLower | تغيير الحالة | s.ToUpper()
Contains / StartsWith | البحث | s.Contains("x")
Substring | جزء من النص | s.Substring(0, 3)
Replace | الاستبدال | s.Replace("a", "b")
Split / string.Join | التقسيم والدمج | s.Split(',')
Trim | حذف المسافات | s.Trim()
int.Parse / int.TryParse | نص إلى رقم | int.TryParse("5", out var n)
```

:::info على عكس Java
في C# العامل `==` بين نصين يقارن **المحتوى**، فلا تحتاج `Equals` للحالات العادية.
:::

```quiz
? ما ناتج 17 / 5 إذا كان الرقمان int؟
* 3
- 3.4
- 4

? في C# المقارنة "abc" == "abc" تعطي true.
= true
```

# @lesson cs-control
title: الشروط والحلقات
summary: if و switch و for و while و foreach.
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

:::info break في switch
في C# كل حالة يجب أن تنتهي بـ `break` (أو `return`)؛ لا يُسمح بالانتقال الضمني للحالة التالية.
:::

```exercise csharp
? أكمل حلقة المرور على المصفوفة cities
___ (var city in cities) { Console.WriteLine(city); }
= foreach
```

```quiz
? أي حلقة تمر على كل عناصر مجموعة بأبسط صيغة؟
* foreach
- do-while
- switch

? في C# يجب أن تنتهي كل حالة في switch بـ break أو return.
= true
```

# @lesson cs-arrays-lists
title: المصفوفات والقوائم
summary: المصفوفات، و List، و Dictionary.
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
int[] | مصفوفة بطول ثابت | int[] a = { 1, 2 };
List<T> | قائمة تكبر وتصغر | var l = new List<int>(); l.Add(1);
Dictionary<K,V> | مفتاح وقيمة | d["a"] = 1;
TryGetValue | قراءة آمنة | d.TryGetValue(k, out var v)
Count / Length | العدد | list.Count
HashSet<T> | بلا تكرار | new HashSet<int>()
```

```exercise csharp
? أضف عنصرًا إلى القائمة
names.___("Khaled");
= Add
```

```quiz
? ما الفرق بين المصفوفة و List في C#؟
* List تكبر وتصغر، والمصفوفة طولها ثابت
- لا فرق
- المصفوفة للنصوص فقط

? الدالة TryGetValue تقرأ من Dictionary دون خطأ إذا لم يوجد المفتاح.
= true
```

# @lesson cs-methods
title: الدوال
summary: التعريف، والمعاملات الاختيارية والمسماة، و out، والتحميل الزائد.
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
    static double Area(double w, double h) => w * h;     // تحميل زائد

    static void Main()
    {
        Console.WriteLine(Square(7));
        Console.WriteLine(Greet("Sara"));
        Console.WriteLine(Greet(title: "Dr.", name: "Omar"));   // معاملات مسماة
        if (TryDivide(10, 4, out double r)) Console.WriteLine(r);
        Console.WriteLine($"{Area(1):0.00} {Area(2, 3)}");
    }
}
```

- `=>` صيغة مختصرة لدالة من سطر واحد.
- `out` تسمح للدالة بإرجاع قيمة إضافية.

```quiz
? ماذا تفعل الكلمة out في معاملات الدالة؟
* تسمح للدالة بإرجاع قيمة إضافية عبر المعامل
- تجعل المعامل اختياريًا
- تمنع تعديل المعامل

? يمكن تمرير المعاملات بأسمائها مثل title: "Dr.".
= true
```

# @lesson cs-classes
title: الأصناف والخصائص
summary: الحقول والخصائص properties والمُنشئ.
---
```try csharp
using System;

class Account
{
    public string Owner { get; }               // خاصية للقراءة فقط
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

- **الخاصية** `{ get; private set; }`: يقرأها الجميع، ويعدّلها الصنف فقط.
- `override ToString` يحدد كيف يُطبع الكائن.

```exercise csharp
? خاصية يقرأها الجميع ويعدّلها الصنف فقط
public decimal Balance { get; ___ set; }
= private
```

```quiz
? ما فائدة private set في الخاصية؟
* تسمح بالقراءة للجميع والتعديل من داخل الصنف فقط
- تخفي الخاصية تمامًا
- تجعلها ثابتة لا تتغير أبدًا

? إعادة تعريف ToString تحدد كيف يُطبع الكائن.
= true
```

# @lesson cs-inheritance
title: الوراثة والواجهات
summary: الوراثة، و abstract، و interface، والتعدد الشكلي.
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

- `:` للوراثة وتحقيق الواجهات، و`base(...)` يستدعي مُنشئ الأب.
- `abstract` دالة بلا تنفيذ يجب على الأبناء تعريفها بـ `override`.
- أسماء الواجهات تبدأ عادة بالحرف `I`.

```quiz
? كيف تستدعي مُنشئ الصنف الأب في C#؟
- super(...)
* base(...)
- parent(...)

? الدالة abstract يجب أن يعرّفها الصنف الابن بـ override.
= true
```

# @lesson cs-linq
title: LINQ
summary: الاستعلام عن المجموعات: Where و Select و OrderBy و Sum و GroupBy.
---
**LINQ** طريقة لاستعلام البيانات داخل الكود، تشبه SQL:

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
Where | تصفية | list.Where(x => x > 0)
Select | تحويل | list.Select(x => x.Name)
OrderBy / OrderByDescending | الترتيب | list.OrderBy(x => x.Price)
Sum / Average / Count | التجميع | list.Sum(x => x.Price)
GroupBy | التجميع حسب مفتاح | list.GroupBy(x => x.Category)
First / FirstOrDefault | أول عنصر | list.FirstOrDefault(x => x.Id == 3)
Any / All | هل بعضها/كلها يحقق الشرط؟ | list.Any(x => x < 0)
ToList | إلى قائمة | query.ToList()
```

```exercise csharp
? صفِّ الأرقام الموجبة
var positive = nums.___(n => n > 0);
= Where
```

```quiz
? أي دالة في LINQ تحوّل كل عنصر إلى قيمة جديدة؟
- Where
* Select
- Any

? الدالة GroupBy تجمع العناصر حسب مفتاح.
= true
```

# @lesson cs-exceptions
title: الاستثناءات
summary: try و catch و finally و throw و using.
---
```try csharp
using System;

class Program
{
    static int ParseAge(string text)
    {
        int age = int.Parse(text);               // قد يرمي FormatException
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

:::tip using للموارد
`using (var file = File.OpenRead("a.txt")) { … }` يغلق الملف تلقائيًا حتى لو حدث استثناء.
:::

```quiz
? أي جزء يُنفَّذ دائمًا؟
- try
- catch
* finally

? الدالة int.Parse("abc") ترمي FormatException.
= true
```

# @lesson cs-project
title: مشروع: إدارة المخزون
summary: برنامج يجمع الأصناف والقوائم و LINQ والاستثناءات.
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
? ما نوع الخاصية Value في الصنف Product؟
* خاصية محسوبة من السعر والكمية
- حقل مخزّن
- دالة ثابتة

? الدالة Sum في LINQ تجمع قيم العناصر.
= true
```

# @lesson cs-reference
title: مرجع C#
summary: أهم الكلمات والأصناف مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة.

```reference csharp
using | استيراد مساحة أسماء | using System.Linq;
class / Main | الصنف ونقطة البداية | static void Main() { }
Console.WriteLine | طباعة | Console.WriteLine("…");
int / decimal / string | الأنواع | decimal p = 9.5m;
var / const | الاستنتاج / الثابت | var x = 5;
$"…" | نص بقيم | $"Total: {t}"
if / switch | الشروط | if (x > 0) { }
for / foreach / while | الحلقات | foreach (var x in list) { }
List / Dictionary | المجموعات | new List<int>()
=> | دالة مختصرة | int Sq(int x) => x * x;
out | قيمة إضافية | int.TryParse(s, out var n)
{ get; set; } | الخصائص | public int Age { get; set; }
: / base | الوراثة | class B : A { }
interface / abstract | الواجهات والتجريد | interface IShape { }
override | إعادة التعريف | public override string ToString()
LINQ | الاستعلام | list.Where(…).Select(…)
try / catch / finally | الاستثناءات | try { } catch (Exception e) { }
throw | رمي استثناء | throw new ArgumentException("…");
```

:::tip ماذا بعد؟
ثبّت .NET SDK و Visual Studio Code، وجرّب ASP.NET Core لبناء واجهات API، أو Unity لبناء لعبة صغيرة.
:::
