# @lesson cpp-intro
title: مقدمة في C++
summary: ما هي سي بلس بلس، وأول برنامج.
---
**C++** لغة سريعة جدًا تتحكم في الذاكرة والعتاد بدقة. تُستخدم في محركات الألعاب، والمتصفحات، وأنظمة التشغيل، والتطبيقات التي تحتاج أداءً عاليًا، والبرمجة التنافسية.

```try cpp
#include <iostream>
using namespace std;

int main() {
    cout << "مرحبًا يا C++" << endl;
    cout << 6 * 7 << endl;
    return 0;
}
```

- `#include <iostream>` يضيف مكتبة الإدخال والإخراج.
- البرنامج يبدأ من الدالة `main`.
- `cout << …` يطبع، و`endl` ينهي السطر.
- `return 0;` يعني أن البرنامج انتهى بنجاح.

:::info تشغيل الأمثلة
أمثلة C++ تعمل على خادم آمن منفصل؛ إذا لم يكن مفعّلًا بعد ستعمل فور تفعيله. على جهازك: `g++ main.cpp -o main` ثم `./main`.
:::

```quiz
? أي مكتبة نحتاجها لاستخدام cout؟
* iostream
- stdio
- string

? تُترجم برامج C++ إلى برنامج تنفيذي قبل التشغيل.
= true
```

# @lesson cpp-variables
title: المتغيرات والأنواع
summary: int و double و char و bool و string و auto و const.
---
```try cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int age = 25;
    double price = 19.99;
    char grade = 'A';
    bool active = true;
    string name = "Sara";
    const double TAX = 0.15;
    auto total = price * (1 + TAX);
    cout << name << " " << age << " " << grade << " " << active << endl;
    cout << "Total: " << total << endl;
    return 0;
}
```

```reference cpp
int | عدد صحيح | int n = 10;
long long | عدد صحيح كبير | long long big = 9000000000LL;
double | عدد عشري | double d = 3.14;
char | حرف واحد | char c = 'x';
bool | صح أو خطأ (يُطبع 1 أو 0) | bool ok = true;
string | نص (يحتاج <string>) | string s = "hi";
auto | يستنتج النوع | auto x = 3.5;
const | ثابت | const int MAX = 100;
```

```exercise cpp
? عرّف ثابتًا صحيحًا اسمه MAX
___ int MAX = 100;
= const
```

```quiz
? ماذا تطبع cout << true؟
* 1
- true
- yes

? الكلمة auto تجعل المترجم يستنتج نوع المتغير.
= true
```

# @lesson cpp-strings
title: النصوص والعمليات
summary: string ودوالها، والعمليات الحسابية، والقسمة الصحيحة.
---
```try cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "Hello C++";
    cout << s.length() << endl;
    cout << s.substr(0, 5) << endl;
    cout << s.find("C++") << endl;
    s += " world";
    cout << s << endl;
    cout << to_string(42) + "!" << endl;

    int a = 17, b = 5;
    cout << a / b << " " << a % b << " " << (double)a / b << endl;
    return 0;
}
```

```reference cpp
length() / size() | طول النص | s.length()
substr(pos, n) | جزء من النص | s.substr(0, 3)
find() | موضع أول ظهور | s.find("x")
+ / += | دمج النصوص | s += "!"
to_string() | رقم إلى نص | to_string(5)
stoi() / stod() | نص إلى رقم | stoi("42")
% | باقي القسمة | 17 % 5
```

:::warning القسمة الصحيحة
`17 / 5` بين رقمين صحيحين تعطي `3`. حوّل أحدهما: `(double)17 / 5` تعطي `3.4`.
:::

```quiz
? ما ناتج 17 / 5 إذا كان الرقمان int؟
* 3
- 3.4
- 4

? الدالة stoi تحوّل نصًا إلى رقم صحيح.
= true
```

# @lesson cpp-conditions-loops
title: الشروط والحلقات
summary: if و switch و for و while و حلقة النطاق.
---
```try cpp
#include <iostream>
using namespace std;

int main() {
    int score = 82;
    if (score >= 90) cout << "Excellent" << endl;
    else if (score >= 75) cout << "Very good" << endl;
    else cout << "Try again" << endl;

    for (int i = 1; i <= 5; i++) cout << i << " ";
    cout << endl;

    int n = 3;
    while (n > 0) {
        cout << "count " << n << endl;
        n--;
    }

    int nums[] = {4, 8, 15, 16};
    int sum = 0;
    for (int x : nums) sum += x;
    cout << "sum = " << sum << endl;

    switch (score / 10) {
        case 10: case 9: cout << "A" << endl; break;
        case 8: cout << "B" << endl; break;
        default: cout << "C or less" << endl;
    }
    return 0;
}
```

```exercise cpp
? أكمل حلقة النطاق على المصفوفة nums
for (int x ___ nums) { cout << x; }
= :
```

```quiz
? ماذا يحدث في switch إذا نسيت break؟
* يكمل تنفيذ الحالات التالية
- يتوقف البرنامج
- لا يحدث شيء

? الصيغة for (int x : nums) تمر على كل عناصر المصفوفة.
= true
```

# @lesson cpp-vectors
title: المتجهات vector
summary: مصفوفة ديناميكية: الإضافة والوصول والترتيب.
---
`vector` مصفوفة تكبر وتصغر تلقائيًا، وهي الأكثر استخدامًا في C++:

```try cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> v = {5, 2, 9, 1};
    v.push_back(7);
    cout << "size: " << v.size() << ", first: " << v[0] << ", last: " << v.back() << endl;
    sort(v.begin(), v.end());
    for (int x : v) cout << x << " ";
    cout << endl;
    v.pop_back();
    cout << "max: " << *max_element(v.begin(), v.end()) << endl;

    vector<vector<int>> grid(2, vector<int>(3, 0));   // 2×3 أصفار
    grid[1][2] = 5;
    cout << grid[1][2] << endl;
    return 0;
}
```

```reference cpp
push_back() | إضافة في النهاية | v.push_back(4)
pop_back() | حذف الأخير | v.pop_back()
size() | العدد | v.size()
v[i] / at(i) | الوصول (at يتحقق من الحدود) | v.at(2)
front() / back() | الأول / الأخير | v.back()
sort(begin, end) | الترتيب | sort(v.begin(), v.end())
empty() | هل فارغ؟ | v.empty()
```

```exercise cpp
? أضف 10 في نهاية المتجه
v.___(10);
= push_back
```

```quiz
? ما الفرق بين المصفوفة العادية و vector؟
* vector يكبر ويصغر تلقائيًا
- لا فرق
- vector للنصوص فقط

? الدالة at(i) تتحقق من أن الفهرس داخل الحدود.
= true
```

# @lesson cpp-functions
title: الدوال
summary: التعريف، والمعاملات بالقيمة وبالمرجع، والقيم الافتراضية، والتحميل الزائد.
---
```try cpp
#include <iostream>
#include <string>
using namespace std;

int square(int x) { return x * x; }

void doubleIt(int &x) { x *= 2; }          // بالمرجع: يغيّر الأصل

string greet(string name, string title = "") {
    return "Hello " + (title.empty() ? "" : title + " ") + name;
}

double area(double r) { return 3.14159 * r * r; }
double area(double w, double h) { return w * h; }   // تحميل زائد

int main() {
    cout << square(7) << endl;
    int n = 5;
    doubleIt(n);
    cout << n << endl;
    cout << greet("Sara") << " | " << greet("Omar", "Dr.") << endl;
    cout << area(1) << " " << area(2, 3) << endl;
    return 0;
}
```

- **بالقيمة** (`int x`): الدالة تعمل على نسخة.
- **بالمرجع** (`int &x`): الدالة تعمل على المتغير الأصلي.
- `const string &s` لتمرير النصوص الكبيرة دون نسخ ودون تعديل.

```exercise cpp
? مرّر المتغير بالمرجع ليتغير الأصل
void reset(int ___x) { x = 0; }
= &
```

```quiz
? ماذا يحدث عند تمرير متغير بالمرجع &؟
* تعدّل الدالة المتغير الأصلي
- تعمل الدالة على نسخة
- يُحذف المتغير

? يمكن تعريف دالتين بنفس الاسم إذا اختلفت المعاملات.
= true
```

# @lesson cpp-pointers
title: المراجع والمؤشرات
summary: العنوان &، والمؤشر *، و nullptr، والمؤشرات الذكية.
---
**المؤشر** متغير يحفظ **عنوان** متغير آخر في الذاكرة:

```try cpp
#include <iostream>
#include <memory>
using namespace std;

int main() {
    int x = 10;
    int *p = &x;          // p يشير إلى x
    cout << "address: " << p << endl;
    cout << "value: " << *p << endl;
    *p = 25;              // التغيير عبر المؤشر
    cout << "x = " << x << endl;

    int &ref = x;         // مرجع: اسم آخر لنفس المتغير
    ref++;
    cout << "x = " << x << endl;

    int *nothing = nullptr;
    if (nothing == nullptr) cout << "pointer is empty" << endl;

    unique_ptr<int> smart(new int(99));   // يحرر الذاكرة تلقائيًا
    cout << *smart << endl;
    return 0;
}
```

```reference cpp
&x | عنوان المتغير | int *p = &x;
*p | القيمة في العنوان | cout << *p;
int &r = x | مرجع (اسم آخر) | r = 5;
nullptr | مؤشر فارغ | int *p = nullptr;
new / delete | حجز وتحرير الذاكرة يدويًا | int *a = new int[5]; delete[] a;
unique_ptr | مؤشر ذكي يحرر الذاكرة | unique_ptr<int> p(new int(1));
```

:::danger تجنّب new و delete اليدويين
نسيان `delete` يسبب تسريب الذاكرة. استخدم `vector` و `string` والمؤشرات الذكية؛ تحرر الذاكرة تلقائيًا.
:::

```quiz
? ماذا يعطي الرمز & قبل اسم المتغير مثل &x؟
* عنوان المتغير في الذاكرة
- قيمة المتغير
- نسخة من المتغير

? المؤشر الذكي unique_ptr يحرر الذاكرة تلقائيًا.
= true
```

# @lesson cpp-classes
title: الأصناف
summary: الحقول والدوال والمُنشئ و public و private.
---
```try cpp
#include <iostream>
#include <string>
#include <stdexcept>
using namespace std;

class Account {
private:
    string owner;
    double balance;

public:
    Account(string o, double b) : owner(o), balance(b) {}

    void deposit(double amount) {
        if (amount <= 0) throw invalid_argument("invalid amount");
        balance += amount;
    }

    double getBalance() const { return balance; }
    string getOwner() const { return owner; }
};

int main() {
    Account acc("Sara", 100);
    acc.deposit(50);
    cout << acc.getOwner() << ": " << acc.getBalance() << endl;
    try {
        acc.deposit(-5);
    } catch (const invalid_argument &e) {
        cout << "error: " << e.what() << endl;
    }
    return 0;
}
```

- `private`: لا يصل إليه إلا الصنف نفسه. `public`: متاح للجميع.
- `: owner(o), balance(b)` قائمة التهيئة في المُنشئ.
- `const` بعد الدالة: لا تغيّر الكائن.

```quiz
? ما فائدة جعل الحقول private؟
* حماية البيانات وإجبار التعامل عبر دوال الصنف
- تسريع البرنامج
- إخفاء الصنف كله

? الكلمة const بعد اسم الدالة تعني أنها لا تغيّر الكائن.
= true
```

# @lesson cpp-inheritance
title: الوراثة والدوال الافتراضية
summary: الوراثة، و virtual، والتعدد الشكلي.
---
```try cpp
#include <iostream>
#include <vector>
#include <memory>
using namespace std;

class Shape {
public:
    virtual double area() const = 0;      // دالة مجردة
    virtual ~Shape() {}
};

class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
};

class Rect : public Shape {
protected:
    double w, h;
public:
    Rect(double w, double h) : w(w), h(h) {}
    double area() const override { return w * h; }
};

class Square : public Rect {
public:
    Square(double s) : Rect(s, s) {}
};

int main() {
    vector<unique_ptr<Shape>> shapes;
    shapes.push_back(unique_ptr<Shape>(new Circle(1)));
    shapes.push_back(unique_ptr<Shape>(new Rect(2, 3)));
    shapes.push_back(unique_ptr<Shape>(new Square(4)));
    for (const auto &s : shapes) cout << s->area() << endl;
    return 0;
}
```

- `virtual` يجعل الاستدعاء يختار دالة الصنف الفعلي (التعدد الشكلي).
- `= 0` دالة مجردة: يجب على الأبناء تعريفها.
- `override` يتأكد المترجم أنك تعيد تعريف دالة موجودة فعلًا.

```quiz
? ما الكلمة التي تسمح بالتعدد الشكلي في C++؟
* virtual
- static
- inline

? الصنف الذي فيه دالة = 0 لا يمكن إنشاء كائن منه مباشرة.
= true
```

# @lesson cpp-stl
title: مكتبة STL
summary: map و set و algorithm و lambda.
---
```try cpp
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <algorithm>
#include <numeric>
#include <string>
using namespace std;

int main() {
    map<string, int> stock;
    stock["pen"] = 120;
    stock["notebook"] = 40;
    stock["pen"] += 30;
    for (const auto &item : stock) cout << item.first << " -> " << item.second << endl;

    set<int> unique = {5, 1, 5, 3, 1};
    for (int x : unique) cout << x << " ";
    cout << endl;

    vector<int> v = {7, 2, 9, 4, 1};
    sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // تنازلي
    int total = accumulate(v.begin(), v.end(), 0);
    int evens = count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    cout << v[0] << " " << total << " " << evens << endl;
    return 0;
}
```

```reference cpp
map | مفتاح وقيمة مرتبة | map<string,int> m; m["a"] = 1;
unordered_map | مفتاح وقيمة أسرع، بلا ترتيب | unordered_map<int,int> m;
set | قيم مرتبة بلا تكرار | set<int> s; s.insert(3);
sort | الترتيب | sort(v.begin(), v.end())
find | البحث | find(v.begin(), v.end(), x)
accumulate | المجموع | accumulate(v.begin(), v.end(), 0)
count_if | العد بشرط | count_if(b, e, pred)
lambda | دالة مختصرة | [](int a) { return a * 2; }
```

```quiz
? أي حاوية تخزن قيمًا مرتبة بلا تكرار؟
- vector
* set
- map

? الصيغة [](int x) { return x * 2; } دالة lambda.
= true
```

# @lesson cpp-project
title: مشروع: إحصاءات الدرجات
summary: برنامج يجمع المتجهات والدوال والخوارزميات.
---
```try cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <iomanip>
using namespace std;

struct Student {
    string name;
    vector<int> grades;
    double average() const {
        return grades.empty() ? 0 : (double)accumulate(grades.begin(), grades.end(), 0) / grades.size();
    }
};

int main() {
    vector<Student> students = {
        {"Sara", {95, 88, 92}},
        {"Omar", {70, 65, 80}},
        {"Layla", {85, 90, 78}},
    };
    sort(students.begin(), students.end(),
         [](const Student &a, const Student &b) { return a.average() > b.average(); });
    cout << fixed << setprecision(1);
    for (const auto &s : students) {
        cout << setw(6) << s.name << " : " << s.average()
             << (s.average() >= 75 ? "  pass" : "  needs help") << endl;
    }
    return 0;
}
```

- `struct` مثل `class` لكن أعضاؤه `public` افتراضيًا.
- `fixed` و `setprecision(1)` لعرض رقم عشري واحد، و`setw` لمحاذاة الأعمدة.

```quiz
? ما الفرق الأساسي بين struct و class في C++؟
* أعضاء struct عامة public افتراضيًا
- struct لا تقبل الدوال
- لا يمكن ترتيب struct

? الأداة setprecision تتحكم في عدد الأرقام العشرية المطبوعة.
= true
```

# @lesson cpp-reference
title: مرجع C++
summary: أهم الكلمات والمكتبات مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة.

```reference cpp
#include | إضافة مكتبة | #include <vector>
main | نقطة البداية | int main() { return 0; }
cout / cin | الإخراج / الإدخال | cout << x << endl;
int / double / bool / char | أنواع أساسية | int n = 0;
string | نص | string s = "hi";
auto / const | الاستنتاج / الثبات | const auto x = 5;
if / switch | الشروط | if (a > b) { … }
for / while | الحلقات | for (int x : v) { … }
vector | مصفوفة ديناميكية | vector<int> v;
map / set | حاويات | map<string,int> m;
& | مرجع / عنوان | void f(int &x)
* | مؤشر / القيمة | int *p = &x;
class / struct | أصناف | class A { public: … };
virtual / override | التعدد الشكلي | virtual double area() const = 0;
unique_ptr | مؤشر ذكي | unique_ptr<A> p(new A());
try / catch / throw | الاستثناءات | throw runtime_error("…");
sort / find | الخوارزميات | sort(v.begin(), v.end())
lambda | دالة مختصرة | [](int a) { return a + 1; }
```

:::tip ماذا بعد؟
ثبّت مترجم g++ أو Visual Studio، وتدرّب على مسائل البرمجة التنافسية؛ C++ هي اللغة الأشهر هناك.
:::
