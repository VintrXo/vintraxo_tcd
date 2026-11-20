# @lesson java-intro
title: مقدمة في Java
summary: ما هي جافا، وأول برنامج، وكيف يعمل.
---
**Java** لغة برمجة قوية تُستخدم في تطبيقات الشركات والخوادم وتطبيقات أندرويد. شعارها «اكتب مرة، شغّل في أي مكان»: يُترجم الكود إلى صيغة وسيطة تعمل على **آلة جافا الافتراضية** (JVM) في أي نظام.

## أول برنامج

```try java
public class Main {
    public static void main(String[] args) {
        System.out.println("مرحبًا يا جافا");
        System.out.println(3 + 4);
    }
}
```

- كل كود جافا داخل **صنف** (`class`). اسم الصنف هنا `Main`.
- البرنامج يبدأ من الدالة `main`.
- `System.out.println` تطبع سطرًا.
- كل جملة تنتهي بفاصلة منقوطة `;`.

:::info تشغيل الأمثلة
أمثلة جافا تعمل على خادم آمن منفصل. إذا لم يكن مفعّلًا بعد، اقرأ الكود وعدّله وستعمل الأمثلة فور تفعيله. على جهازك: ثبّت JDK ثم `javac Main.java` و `java Main`.
:::

```quiz
? من أين يبدأ تنفيذ برنامج جافا؟
* من الدالة main
- من أول سطر في الملف
- من آخر صنف

? كل جملة في جافا تنتهي بفاصلة منقوطة.
= true
```

# @lesson java-variables
title: المتغيرات وأنواع البيانات
summary: الأنواع الأساسية، و String، و var، والثوابت.
---
جافا لغة **صارمة الأنواع**: تحدد نوع كل متغير عند تعريفه.

```try java
public class Main {
    public static void main(String[] args) {
        int age = 25;
        double price = 19.99;
        boolean active = true;
        char grade = 'A';
        String name = "سارة";
        final double TAX = 0.15;     // ثابت لا يتغير
        var total = price * (1 + TAX);
        System.out.println(name + " " + age + " " + active + " " + grade);
        System.out.println("الإجمالي: " + total);
    }
}
```

```reference java
int | عدد صحيح | int n = 10;
long | عدد صحيح كبير | long big = 9_000_000_000L;
double | عدد عشري | double d = 3.14;
boolean | صح أو خطأ | boolean ok = true;
char | حرف واحد بين ' ' | char c = 'x';
String | نص بين " " | String s = "مرحبا";
final | ثابت | final int MAX = 100;
var | يستنتج النوع | var list = new ArrayList<String>();
```

```exercise java
? عرّف متغيرًا صحيحًا اسمه count قيمته 5
___ count = 5;
= int
```

```quiz
? أي نوع يناسب السعر 19.99؟
- int
* double
- char

? الكلمة final تجعل قيمة المتغير ثابتة.
= true
```

# @lesson java-operators
title: العوامل
summary: الحساب والمقارنة والمنطق، والقسمة الصحيحة.
---
```try java
public class Main {
    public static void main(String[] args) {
        int a = 17, b = 5;
        System.out.println(a + b);
        System.out.println(a / b);        // 3: قسمة صحيحة لأن الاثنين int
        System.out.println(a % b);        // 2: الباقي
        System.out.println((double) a / b);
        System.out.println(a > b && b > 0);
        a += 3;
        a++;
        System.out.println(a);
    }
}
```

```reference java
+ - * / % | الحساب والباقي | 17 % 5 → 2
++ / -- | زيادة / نقص بواحد | i++
+= -= *= | إسناد مع عملية | x += 5
== != | يساوي / لا يساوي | a == b
> < >= <= | المقارنة | a >= 18
&& | و | a > 0 && b > 0
! | النفي | !done
(double) | تحويل النوع | (double) a / b
```

:::warning القسمة الصحيحة
قسمة رقمين `int` تحذف الكسر: `7 / 2` تعطي `3`. حوّل أحدهما إلى `double` لتحصل على `3.5`.
:::

```quiz
? ما ناتج 7 / 2 إذا كان الرقمان int؟
* 3
- 3.5
- 4

? العامل % يعطي باقي القسمة.
= true
```

# @lesson java-strings
title: النصوص
summary: دوال String، والمقارنة بـ equals، و StringBuilder.
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
        System.out.println(String.format("السعر: %.2f", 19.5));

        String a = "abc";
        String b = new String("abc");
        System.out.println(a == b);        // false: يقارن المراجع
        System.out.println(a.equals(b));   // true: يقارن المحتوى
    }
}
```

:::danger قارن النصوص بـ equals
`==` مع النصوص يقارن إن كانا **نفس الكائن** في الذاكرة، لا نفس الحروف. استخدم `equals` دائمًا.
:::

## بناء نص طويل

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
? قارن محتوى النصين بالطريقة الصحيحة
if (name.___("admin")) { … }
= equals
```

```quiz
? ما الطريقة الصحيحة لمقارنة محتوى نصين في جافا؟
- a == b
* a.equals(b)
- a.compare(b)

? الصنف StringBuilder مناسب لبناء نص طويل داخل حلقة.
= true
```

# @lesson java-conditions
title: الشروط
summary: if و else و switch الحديثة.
---
```try java
public class Main {
    public static void main(String[] args) {
        int score = 82;
        if (score >= 90) {
            System.out.println("ممتاز");
        } else if (score >= 75) {
            System.out.println("جيد جدًا");
        } else {
            System.out.println("حاول مرة أخرى");
        }

        String level = score >= 60 ? "ناجح" : "راسب";
        System.out.println(level);

        int day = 5;
        switch (day) {
            case 5:
                System.out.println("الجمعة");
                break;
            case 6:
                System.out.println("السبت");
                break;
            default:
                System.out.println("يوم آخر");
        }
    }
}
```

## switch الحديثة (Java 14 فأحدث)

```java
String name = switch (day) {
    case 5 -> "الجمعة";
    case 6 -> "السبت";
    default -> "يوم آخر";
};
```

`switch` بالسهم `->` لا تحتاج `break` وتعيد قيمة مباشرة. خادم تشغيل الأمثلة يستخدم Java 13، لذلك المثال القابل للتشغيل بالصيغة الكلاسيكية.

```quiz
? ما ميزة switch بالسهم -> الحديثة؟
* لا تحتاج break وتعيد قيمة
- تعمل مع النصوص فقط
- أسرع من if دائمًا

? العامل الثلاثي يكتب if/else بسيطة في سطر واحد.
= true
```

# @lesson java-loops
title: الحلقات
summary: for و while و for-each و break و continue.
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
            System.out.println("العد: " + n);
            n--;
        }

        String[] cities = {"الرياض", "جدة", "الدمام"};
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
? أكمل حلقة for-each على المصفوفة names
for (String n ___ names) { System.out.println(n); }
= :
```

```quiz
? أي حلقة تمر على كل عناصر المصفوفة بأبسط صيغة؟
* for-each: for (String x : arr)
- while
- do-while

? الكلمة continue تتخطى بقية التكرار الحالي.
= true
```

# @lesson java-arrays
title: المصفوفات
summary: إنشاء المصفوفات، والطول، والترتيب، والمصفوفات ثنائية الأبعاد.
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
        System.out.println("المتوسط: " + (double) sum / scores.length);

        int[][] grid = {{1, 2, 3}, {4, 5, 6}};
        System.out.println(grid[1][2]);

        String[] names = new String[3];   // مصفوفة فارغة بطول 3
        names[0] = "علي";
        System.out.println(Arrays.toString(names));
    }
}
```

:::warning الطول ثابت
لا يمكن تغيير طول المصفوفة بعد إنشائها. للقوائم التي تكبر وتصغر استخدم `ArrayList` (درس المجموعات).
:::

```quiz
? كيف تعرف عدد عناصر المصفوفة arr؟
* arr.length
- arr.size()
- len(arr)

? يمكن تغيير طول المصفوفة في جافا بعد إنشائها.
= false
```

# @lesson java-methods
title: الدوال
summary: تعريف الدوال، والمعاملات، والقيمة المرجعة، والتحميل الزائد.
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
        return "أهلًا " + name;
    }

    static String greet(String name, String title) {   // تحميل زائد
        return "أهلًا " + title + " " + name;
    }

    public static void main(String[] args) {
        System.out.println(square(7));
        System.out.println(average(new int[]{4, 8, 15}));
        System.out.println(greet("سارة"));
        System.out.println(greet("عمر", "د."));
    }
}
```

- `static int square(int x)`: نوع القيمة المرجعة ثم الاسم ثم المعاملات بأنواعها.
- `void` إذا لم تُرجع الدالة شيئًا.
- **التحميل الزائد**: نفس الاسم بمعاملات مختلفة.

```exercise java
? دالة لا تُرجع شيئًا
static ___ printLine() { System.out.println("---"); }
= void
```

```quiz
? ماذا يعني void في تعريف الدالة؟
* أنها لا تُرجع قيمة
- أنها خاصة
- أنها ثابتة

? يجوز تعريف دالتين بنفس الاسم إذا اختلفت المعاملات.
= true
```

# @lesson java-classes
title: الأصناف والكائنات
summary: الحقول، والمُنشئ، والدوال، والتغليف بـ private.
---
```try java
public class Main {
    static class Account {
        private final String owner;
        private double balance;

        Account(String owner, double balance) {     // المُنشئ
            this.owner = owner;
            this.balance = balance;
        }

        void deposit(double amount) {
            if (amount <= 0) throw new IllegalArgumentException("مبلغ غير صحيح");
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
        Account acc = new Account("سارة", 100);
        acc.deposit(50);
        System.out.println(acc);
        System.out.println(acc.getBalance());
    }
}
```

- **المُنشئ** له نفس اسم الصنف ويُنفَّذ مع `new`.
- `private` يمنع الوصول للحقل من الخارج؛ نصل إليه عبر دوال مثل `getBalance`. هذا هو **التغليف**.
- `this` يشير إلى الكائن الحالي.

```quiz
? متى يُنفَّذ المُنشئ؟
* عند إنشاء كائن بـ new
- عند طباعة الكائن
- عند حذف الكائن

? الكلمة private تمنع الوصول للحقل من خارج الصنف.
= true
```

# @lesson java-inheritance
title: الوراثة والواجهات
summary: extends و override، و interface، والتعدد الشكلي.
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

- `extends` يرث صنفًا، و`super(...)` يستدعي مُنشئ الأب.
- `interface` عقد يحدد الدوال المطلوبة، و`implements` يلتزم به.
- **التعدد الشكلي**: نتعامل مع كل الأشكال كـ `Shape`، وكل واحد يحسب مساحته بطريقته.

```quiz
? أي كلمة تجعل الصنف يلتزم بواجهة؟
- extends
* implements
- inherits

? الاستدعاء super(...) يستدعي مُنشئ الصنف الأب.
= true
```

# @lesson java-collections
title: المجموعات
summary: ArrayList و HashMap و HashSet، و streams.
---
```try java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>(List.of("سارة", "عمر"));
        names.add("ليلى");
        names.remove("عمر");
        System.out.println(names + " " + names.size());

        Map<String, Integer> stock = new HashMap<>();
        stock.put("قلم", 120);
        stock.put("دفتر", 40);
        stock.merge("قلم", 30, Integer::sum);
        for (var e : stock.entrySet()) {
            System.out.println(e.getKey() + " → " + e.getValue());
        }

        Set<String> tags = new HashSet<>(List.of("جديد", "مميز", "جديد"));
        System.out.println(tags.size());

        List<Integer> prices = List.of(120, 45, 300, 80);
        int total = prices.stream().filter(p -> p > 50).mapToInt(Integer::intValue).sum();
        System.out.println("مجموع ما فوق 50: " + total);
    }
}
```

```reference java
ArrayList | قائمة تكبر وتصغر | list.add(x); list.get(0)
HashMap | مفتاح وقيمة | map.put(k, v); map.get(k)
HashSet | بلا تكرار | set.add(x); set.contains(x)
List.of / Map.of | مجموعات ثابتة | List.of(1, 2, 3)
stream() | معالجة متسلسلة | list.stream().filter(…).map(…)
Collections.sort | الترتيب | Collections.sort(list)
```

```exercise java
? أضف عنصرًا إلى القائمة
names.___("خالد");
= add
```

```quiz
? أي مجموعة تخزن أزواج مفتاح وقيمة؟
- ArrayList
* HashMap
- HashSet

? المجموعة HashSet لا تسمح بالتكرار.
= true
```

# @lesson java-exceptions
title: الاستثناءات
summary: try و catch و finally، و throw و throws.
---
```try java
public class Main {
    static int parseAge(String text) {
        int age = Integer.parseInt(text);           // قد يرمي NumberFormatException
        if (age < 0) throw new IllegalArgumentException("العمر لا يكون سالبًا");
        return age;
    }

    public static void main(String[] args) {
        String[] inputs = {"25", "abc", "-3"};
        for (String in : inputs) {
            try {
                System.out.println("العمر: " + parseAge(in));
            } catch (NumberFormatException e) {
                System.out.println("ليس رقمًا: " + in);
            } catch (IllegalArgumentException e) {
                System.out.println("خطأ: " + e.getMessage());
            } finally {
                System.out.println("---");
            }
        }
    }
}
```

:::info الاستثناءات المفحوصة
بعض الاستثناءات (مثل أخطاء الملفات `IOException`) يجبرك المترجم على التعامل معها بـ `try/catch` أو إعلانها بـ `throws` في توقيع الدالة.
:::

```quiz
? أي جزء يُنفَّذ دائمًا سواء حدث استثناء أم لا؟
- try
- catch
* finally

? الدالة Integer.parseInt("abc") ترمي استثناء NumberFormatException.
= true
```

# @lesson java-project
title: مشروع: إدارة المخزون
summary: برنامج صغير يجمع الأصناف والمجموعات والاستثناءات.
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
            if (p == null) throw new NoSuchElementException("غير موجود: " + name);
            if (count > p.qty()) throw new IllegalStateException("الكمية لا تكفي: " + name);
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
        inv.add(new Product("قلم", 5, 120));
        inv.add(new Product("دفتر", 12, 8));
        inv.add(new Product("حقيبة", 90, 3));
        inv.sell("قلم", 20);
        try {
            inv.sell("حقيبة", 5);
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
        System.out.printf("قيمة المخزون: %.2f%n", inv.totalValue());
        System.out.println("مخزون منخفض: " + inv.lowStock(10));
    }
}
```

في Java 16 فأحدث يمكن اختصار الصنف `Product` كله في سطر واحد: `record Product(String name, double price, int qty) {}`؛ ينشئ `record` المُنشئ والدوال `name()` و`equals` و`toString` تلقائيًا.

```quiz
? ما فائدة record في جافا؟
* صنف مختصر للبيانات ينشئ المُنشئ و toString تلقائيًا
- قاعدة بيانات مدمجة
- نوع من الحلقات

? نستخدم LinkedHashMap للحفاظ على ترتيب الإضافة.
= true
```

# @lesson java-reference
title: مرجع Java
summary: أهم الكلمات والأصناف مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة.

```reference java
class | صنف | public class Main { … }
main | نقطة البداية | public static void main(String[] args)
System.out.println | طباعة سطر | System.out.println("…");
int / double / boolean | أنواع أساسية | int n = 5;
String | نص | String s = "…";
if / else / switch | الشروط | if (x > 0) { … }
for / while / for-each | الحلقات | for (int x : arr) { … }
int[] | مصفوفة | int[] a = {1, 2};
static | تابع للصنف | static int sq(int x)
void | بلا قيمة مرجعة | void print()
new | إنشاء كائن | new Account("…", 0)
private / public | التحكم بالوصول | private double balance;
this / super | الكائن الحالي / الأب | super(w, h);
extends / implements | الوراثة / الواجهات | class A extends B
interface | واجهة | interface Shape { double area(); }
ArrayList / HashMap | المجموعات | new ArrayList<>()
try / catch / finally | الاستثناءات | try { … } catch (Exception e) { … }
throw / throws | رمي استثناء | throw new IllegalArgumentException("…");
record | صنف بيانات | record Point(int x, int y) {}
stream | معالجة المجموعات | list.stream().filter(…)
```

:::tip ماذا بعد؟
ثبّت JDK و IntelliJ IDEA على جهازك، وابنِ مشروعًا صغيرًا، ثم تعرّف على Spring Boot لبناء الخوادم.
:::
