# @lesson java-intro
title: Java introduction
summary: What Java is, your first program, and how it runs.
---
**Java** is a powerful programming language used for enterprise applications, servers and Android apps. Its motto is "write once, run anywhere": code is compiled to an intermediate form that runs on the **Java Virtual Machine** (JVM) on any system.

## Your first program

```try java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java");
        System.out.println(3 + 4);
    }
}
```

- All Java code lives inside a **class**. Here the class is called `Main`.
- The program starts at the `main` method.
- `System.out.println` prints a line.
- Every statement ends with a semicolon `;`.

:::info Running the examples
Java examples run on a separate, secure server. If it is not enabled yet, read and edit the code; the examples run as soon as it is. On your computer: install a JDK, then `javac Main.java` and `java Main`.
:::

```quiz
? Where does a Java program start running?
* At the main method
- At the first line of the file
- At the last class

? Every statement in Java ends with a semicolon.
= true
```

# @lesson java-variables
title: Variables and data types
summary: Primitive types, String, var, and constants.
---
Java is **statically typed**: you give every variable a type when you declare it.

```try java
public class Main {
    public static void main(String[] args) {
        int age = 25;
        double price = 19.99;
        boolean active = true;
        char grade = 'A';
        String name = "Sara";
        final double TAX = 0.15;     // a constant that never changes
        var total = price * (1 + TAX);
        System.out.println(name + " " + age + " " + active + " " + grade);
        System.out.println("Total: " + total);
    }
}
```

```reference java
int | Whole number | int n = 10;
long | Large whole number | long big = 9_000_000_000L;
double | Decimal number | double d = 3.14;
boolean | True or false | boolean ok = true;
char | One character in ' ' | char c = 'x';
String | Text in " " | String s = "hello";
final | Constant | final int MAX = 100;
var | Infers the type | var list = new ArrayList<String>();
```

```exercise java
? Declare a whole-number variable named count with the value 5
___ count = 5;
= int
```

```quiz
? Which type suits the price 19.99?
- int
* double
- char

? final makes a variable's value constant.
= true
```

# @lesson java-operators
title: Operators
summary: Arithmetic, comparison, logic, and integer division.
---
```try java
public class Main {
    public static void main(String[] args) {
        int a = 17, b = 5;
        System.out.println(a + b);
        System.out.println(a / b);        // 3: integer division, both are int
        System.out.println(a % b);        // 2: the remainder
        System.out.println((double) a / b);
        System.out.println(a > b && b > 0);
        a += 3;
        a++;
        System.out.println(a);
    }
}
```

```reference java
+ - * / % | Arithmetic and remainder | 17 % 5 → 2
++ / -- | Add / subtract one | i++
+= -= *= | Assign with an operation | x += 5
== != | Equal / not equal | a == b
> < >= <= | Comparison | a >= 18
&& | And | a > 0 && b > 0
! | Not | !done
(double) | Type cast | (double) a / b
```

:::warning Integer division
Dividing two `int` values drops the fraction: `7 / 2` gives `3`. Cast one of them to `double` to get `3.5`.
:::

```quiz
? What is 7 / 2 when both numbers are int?
* 3
- 3.5
- 4

? The % operator gives the remainder of a division.
= true
```

# @lesson java-strings
title: Strings
summary: String methods, comparing with equals, and StringBuilder.
---
```try java
public class Main {
    public static void main(String[] args) {
        String s = "Hello Java";
        System.out.println(s.length());
        System.out.println(s.toUpperCase());
        System.out.println(s.contains("Java"));
        System.out.println(s.substring(0, 5));
        System.out.println(s.replace("Java", "World"));
        System.out.println(String.format("Price: %.2f", 19.5));

        String a = "abc";
        String b = new String("abc");
        System.out.println(a == b);        // false: compares references
        System.out.println(a.equals(b));   // true: compares the content
    }
}
```

:::danger Compare strings with equals
`==` on strings checks whether they are **the same object** in memory, not the same letters. Always use `equals`.
:::

## Building a long string

```try java
public class Main {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= 5; i++) {
            sb.append(i).append(i < 5 ? ", " : "");
        }
        System.out.println(sb.toString());
    }
}
```

```exercise java
? Compare the content of the two strings the right way
if (name.___("admin")) { … }
= equals
```

```quiz
? What is the right way to compare the content of two strings in Java?
- a == b
* a.equals(b)
- a.compare(b)

? StringBuilder is suited to building a long string inside a loop.
= true
```

# @lesson java-conditions
title: Conditions
summary: if, else, and the modern switch.
---
```try java
public class Main {
    public static void main(String[] args) {
        int score = 82;
        if (score >= 90) {
            System.out.println("Excellent");
        } else if (score >= 75) {
            System.out.println("Very good");
        } else {
            System.out.println("Try again");
        }

        String level = score >= 60 ? "pass" : "fail";
        System.out.println(level);

        int day = 5;
        switch (day) {
            case 5:
                System.out.println("Friday");
                break;
            case 6:
                System.out.println("Saturday");
                break;
            default:
                System.out.println("Another day");
        }
    }
}
```

## The modern switch (Java 14 and later)

```java
String name = switch (day) {
    case 5 -> "Friday";
    case 6 -> "Saturday";
    default -> "Another day";
};
```

`switch` with arrows `->` needs no `break` and returns a value directly. The example server runs Java 13, so the runnable example uses the classic form.

```quiz
? What is the advantage of the modern switch with ->?
* No break needed, and it returns a value
- It only works with strings
- It is always faster than if

? The ternary operator writes a simple if/else on one line.
= true
```

# @lesson java-loops
title: Loops
summary: for, while, for-each, break and continue.
---
```try java
public class Main {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.print(i + " ");
        }
        System.out.println();

        int n = 3;
        while (n > 0) {
            System.out.println("Count: " + n);
            n--;
        }

        String[] cities = {"Riyadh", "Jeddah", "Dammam"};
        for (String city : cities) {
            System.out.println(city);
        }

        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) continue;
            if (i > 7) break;
            System.out.print(i + " ");
        }
    }
}
```

```exercise java
? Complete the for-each loop over the array names
for (String n ___ names) { System.out.println(n); }
= :
```

```quiz
? Which loop goes over every item of an array in the simplest form?
* for-each: for (String x : arr)
- while
- do-while

? continue skips the rest of the current pass.
= true
```

# @lesson java-arrays
title: Arrays
summary: Creating arrays, length, sorting, and two-dimensional arrays.
---
```try java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] scores = {88, 72, 95, 60};
        System.out.println(scores[0] + " / " + scores.length);
        Arrays.sort(scores);
        System.out.println(Arrays.toString(scores));

        int sum = 0;
        for (int s : scores) sum += s;
        System.out.println("Average: " + (double) sum / scores.length);

        int[][] grid = {{1, 2, 3}, {4, 5, 6}};
        System.out.println(grid[1][2]);

        String[] names = new String[3];   // an empty array of length 3
        names[0] = "Ali";
        System.out.println(Arrays.toString(names));
    }
}
```

:::warning Fixed length
An array's length cannot change after it is created. For lists that grow and shrink use `ArrayList` (the collections lesson).
:::

```quiz
? How do you get the number of items in the array arr?
* arr.length
- arr.size()
- len(arr)

? A Java array's length can change after it is created.
= false
```

# @lesson java-methods
title: Methods
summary: Defining methods, parameters, return values and overloading.
---
```try java
public class Main {
    static int square(int x) {
        return x * x;
    }

    static double average(int[] nums) {
        int sum = 0;
        for (int n : nums) sum += n;
        return (double) sum / nums.length;
    }

    static String greet(String name) {
        return "Hello " + name;
    }

    static String greet(String name, String title) {   // overloading
        return "Hello " + title + " " + name;
    }

    public static void main(String[] args) {
        System.out.println(square(7));
        System.out.println(average(new int[]{4, 8, 15}));
        System.out.println(greet("Sara"));
        System.out.println(greet("Omar", "Dr."));
    }
}
```

- `static int square(int x)`: the return type, then the name, then the parameters with their types.
- `void` when the method returns nothing.
- **Overloading**: the same name with different parameters.

```exercise java
? A method that returns nothing
static ___ printLine() { System.out.println("---"); }
= void
```

```quiz
? What does void mean in a method declaration?
* It returns no value
- It is private
- It is constant

? Two methods may share a name if their parameters differ.
= true
```

# @lesson java-classes
title: Classes and objects
summary: Fields, the constructor, methods, and encapsulation with private.
---
```try java
public class Main {
    static class Account {
        private final String owner;
        private double balance;

        Account(String owner, double balance) {     // the constructor
            this.owner = owner;
            this.balance = balance;
        }

        void deposit(double amount) {
            if (amount <= 0) throw new IllegalArgumentException("Invalid amount");
            balance += amount;
        }

        double getBalance() {
            return balance;
        }

        @Override
        public String toString() {
            return owner + ": " + balance;
        }
    }

    public static void main(String[] args) {
        Account acc = new Account("Sara", 100);
        acc.deposit(50);
        System.out.println(acc);
        System.out.println(acc.getBalance());
    }
}
```

- The **constructor** has the class's name and runs with `new`.
- `private` blocks access to a field from outside; we reach it through methods such as `getBalance`. This is **encapsulation**.
- `this` refers to the current object.

```quiz
? When does the constructor run?
* When an object is created with new
- When the object is printed
- When the object is deleted

? private blocks access to a field from outside the class.
= true
```

# @lesson java-inheritance
title: Inheritance and interfaces
summary: extends and override, interface, and polymorphism.
---
```try java
public class Main {
    interface Shape {
        double area();
    }

    static class Circle implements Shape {
        private final double r;
        Circle(double r) { this.r = r; }
        public double area() { return Math.PI * r * r; }
    }

    static class Rectangle implements Shape {
        protected final double w, h;
        Rectangle(double w, double h) { this.w = w; this.h = h; }
        public double area() { return w * h; }
    }

    static class Square extends Rectangle {
        Square(double side) { super(side, side); }
    }

    public static void main(String[] args) {
        Shape[] shapes = {new Circle(1), new Rectangle(2, 3), new Square(4)};
        for (Shape s : shapes) {
            System.out.printf("%s: %.2f%n", s.getClass().getSimpleName(), s.area());
        }
    }
}
```

- `extends` inherits a class, and `super(...)` calls the parent's constructor.
- An `interface` is a contract naming the methods required, and `implements` fulfils it.
- **Polymorphism**: we treat every shape as a `Shape`, and each computes its area its own way.

```quiz
? Which keyword makes a class fulfil an interface?
- extends
* implements
- inherits

? super(...) calls the parent class's constructor.
= true
```

# @lesson java-collections
title: Collections
summary: ArrayList, HashMap and HashSet, and streams.
---
```try java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>(List.of("Sara", "Omar"));
        names.add("Layla");
        names.remove("Omar");
        System.out.println(names + " " + names.size());

        Map<String, Integer> stock = new HashMap<>();
        stock.put("pen", 120);
        stock.put("notebook", 40);
        stock.merge("pen", 30, Integer::sum);
        for (var e : stock.entrySet()) {
            System.out.println(e.getKey() + " → " + e.getValue());
        }

        Set<String> tags = new HashSet<>(List.of("new", "featured", "new"));
        System.out.println(tags.size());

        List<Integer> prices = List.of(120, 45, 300, 80);
        int total = prices.stream().filter(p -> p > 50).mapToInt(Integer::intValue).sum();
        System.out.println("Total above 50: " + total);
    }
}
```

```reference java
ArrayList | A list that grows and shrinks | list.add(x); list.get(0)
HashMap | Key and value | map.put(k, v); map.get(k)
HashSet | No repeats | set.add(x); set.contains(x)
List.of / Map.of | Fixed collections | List.of(1, 2, 3)
stream() | Pipeline processing | list.stream().filter(…).map(…)
Collections.sort | Sorting | Collections.sort(list)
```

```exercise java
? Add an item to the list
names.___("Khaled");
= add
```

```quiz
? Which collection stores key-value pairs?
- ArrayList
* HashMap
- HashSet

? HashSet does not allow repeats.
= true
```

# @lesson java-exceptions
title: Exceptions
summary: try, catch and finally, throw and throws.
---
```try java
public class Main {
    static int parseAge(String text) {
        int age = Integer.parseInt(text);           // may throw NumberFormatException
        if (age < 0) throw new IllegalArgumentException("Age cannot be negative");
        return age;
    }

    public static void main(String[] args) {
        String[] inputs = {"25", "abc", "-3"};
        for (String in : inputs) {
            try {
                System.out.println("Age: " + parseAge(in));
            } catch (NumberFormatException e) {
                System.out.println("Not a number: " + in);
            } catch (IllegalArgumentException e) {
                System.out.println("Error: " + e.getMessage());
            } finally {
                System.out.println("---");
            }
        }
    }
}
```

:::info Checked exceptions
Some exceptions (such as file errors, `IOException`) must be handled with `try/catch` or declared with `throws` in the method signature; the compiler insists.
:::

```quiz
? Which part always runs, whether or not an exception happens?
- try
- catch
* finally

? Integer.parseInt("abc") throws a NumberFormatException.
= true
```

# @lesson java-project
title: Project: inventory management
summary: A small program that combines classes, collections and exceptions.
---
```try java
import java.util.*;
import java.util.stream.Collectors;

public class Main {
    static class Product {
        final String name;
        final double price;
        final int qty;
        Product(String name, double price, int qty) { this.name = name; this.price = price; this.qty = qty; }
        String name() { return name; }
        double price() { return price; }
        int qty() { return qty; }
        double value() { return price * qty; }
        @Override public String toString() { return name + " (" + qty + ")"; }
    }

    static class Inventory {
        private final Map<String, Product> items = new LinkedHashMap<>();

        void add(Product p) { items.put(p.name(), p); }

        void sell(String name, int count) {
            Product p = items.get(name);
            if (p == null) throw new NoSuchElementException("Not found: " + name);
            if (count > p.qty()) throw new IllegalStateException("Not enough stock: " + name);
            items.put(name, new Product(name, p.price(), p.qty() - count));
        }

        double totalValue() {
            return items.values().stream().mapToDouble(Product::value).sum();
        }

        List<Product> lowStock(int limit) {
            return items.values().stream().filter(p -> p.qty() < limit).collect(Collectors.toList());
        }
    }

    public static void main(String[] args) {
        Inventory inv = new Inventory();
        inv.add(new Product("pen", 5, 120));
        inv.add(new Product("notebook", 12, 8));
        inv.add(new Product("bag", 90, 3));
        inv.sell("pen", 20);
        try {
            inv.sell("bag", 5);
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
        System.out.printf("Stock value: %.2f%n", inv.totalValue());
        System.out.println("Low stock: " + inv.lowStock(10));
    }
}
```

In Java 16 and later the whole `Product` class shrinks to one line: `record Product(String name, double price, int qty) {}`; a `record` creates the constructor, the `name()` accessors, `equals` and `toString` automatically.

```quiz
? What is a record for in Java?
* A short data class that creates the constructor and toString automatically
- A built-in database
- A kind of loop

? We use LinkedHashMap to keep the order of insertion.
= true
```

# @lesson java-reference
title: Java reference
summary: The most important keywords and classes with an example for each.
type: Reference
---
Search the table for any keyword.

```reference java
class | Class | public class Main { … }
main | Entry point | public static void main(String[] args)
System.out.println | Print a line | System.out.println("…");
int / double / boolean | Primitive types | int n = 5;
String | Text | String s = "…";
if / else / switch | Conditions | if (x > 0) { … }
for / while / for-each | Loops | for (int x : arr) { … }
int[] | Array | int[] a = {1, 2};
static | Belongs to the class | static int sq(int x)
void | No return value | void print()
new | Create an object | new Account("…", 0)
private / public | Access control | private double balance;
this / super | Current object / parent | super(w, h);
extends / implements | Inheritance / interfaces | class A extends B
interface | Interface | interface Shape { double area(); }
ArrayList / HashMap | Collections | new ArrayList<>()
try / catch / finally | Exceptions | try { … } catch (Exception e) { … }
throw / throws | Throw an exception | throw new IllegalArgumentException("…");
record | Data class | record Point(int x, int y) {}
stream | Process collections | list.stream().filter(…)
```

:::tip What next?
Install a JDK and IntelliJ IDEA on your computer, build a small project, then explore Spring Boot for building servers.
:::
