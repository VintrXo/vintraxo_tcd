# @lesson cpp-intro
title: C++ introduction
summary: What C++ is, and your first program.
---
**C++** is a very fast language with precise control over memory and hardware. It is used for game engines, browsers, operating systems, high-performance applications and competitive programming.

```try cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, C++" << endl;
    cout << 6 * 7 << endl;
    return 0;
}
```

- `#include <iostream>` adds the input/output library.
- The program starts at the `main` function.
- `cout << …` prints, and `endl` ends the line.
- `return 0;` means the program finished successfully.

:::info Running the examples
C++ examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: `g++ main.cpp -o main`, then `./main`.
:::

```quiz
? Which library do we need to use cout?
* iostream
- stdio
- string

? C++ programs are compiled into an executable before they run.
= true
```

# @lesson cpp-variables
title: Variables and types
summary: int, double, char, bool, string, auto and const.
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
int | Whole number | int n = 10;
long long | Large whole number | long long big = 9000000000LL;
double | Decimal number | double d = 3.14;
char | One character | char c = 'x';
bool | True or false (prints 1 or 0) | bool ok = true;
string | Text (needs <string>) | string s = "hi";
auto | Infers the type | auto x = 3.5;
const | Constant | const int MAX = 100;
```

```exercise cpp
? Declare a constant whole number named MAX
___ int MAX = 100;
= const
```

```quiz
? What does cout << true print?
* 1
- true
- yes

? auto makes the compiler infer a variable's type.
= true
```

# @lesson cpp-strings
title: Strings and operators
summary: string and its methods, arithmetic, and integer division.
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
length() / size() | Length of the string | s.length()
substr(pos, n) | Part of the string | s.substr(0, 3)
find() | Position of the first match | s.find("x")
+ / += | Join strings | s += "!"
to_string() | Number to string | to_string(5)
stoi() / stod() | String to number | stoi("42")
% | Remainder | 17 % 5
```

:::warning Integer division
`17 / 5` between two whole numbers gives `3`. Cast one of them: `(double)17 / 5` gives `3.4`.
:::

```quiz
? What is 17 / 5 when both numbers are int?
* 3
- 3.4
- 4

? stoi turns a string into a whole number.
= true
```

# @lesson cpp-conditions-loops
title: Conditions and loops
summary: if, switch, for, while and the range loop.
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
? Complete the range loop over the array nums
for (int x ___ nums) { cout << x; }
= :
```

```quiz
? What happens in a switch if you forget break?
* It goes on running the following cases
- The program stops
- Nothing happens

? for (int x : nums) goes over every item of the array.
= true
```

# @lesson cpp-vectors
title: Vectors
summary: A dynamic array: adding, reading and sorting.
---
`vector` is an array that grows and shrinks by itself, and the most used container in C++:

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

    vector<vector<int>> grid(2, vector<int>(3, 0));   // 2×3 zeros
    grid[1][2] = 5;
    cout << grid[1][2] << endl;
    return 0;
}
```

```reference cpp
push_back() | Add at the end | v.push_back(4)
pop_back() | Remove the last | v.pop_back()
size() | Count | v.size()
v[i] / at(i) | Access (at checks bounds) | v.at(2)
front() / back() | First / last | v.back()
sort(begin, end) | Sort | sort(v.begin(), v.end())
empty() | Is it empty? | v.empty()
```

```exercise cpp
? Add 10 at the end of the vector
v.___(10);
= push_back
```

```quiz
? What is the difference between a plain array and a vector?
* A vector grows and shrinks by itself
- There is no difference
- A vector is only for text

? at(i) checks that the index is within bounds.
= true
```

# @lesson cpp-functions
title: Functions
summary: Definition, passing by value and by reference, default values, and overloading.
---
```try cpp
#include <iostream>
#include <string>
using namespace std;

int square(int x) { return x * x; }

void doubleIt(int &x) { x *= 2; }          // by reference: changes the original

string greet(string name, string title = "") {
    return "Hello " + (title.empty() ? "" : title + " ") + name;
}

double area(double r) { return 3.14159 * r * r; }
double area(double w, double h) { return w * h; }   // overloading

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

- **By value** (`int x`): the function works on a copy.
- **By reference** (`int &x`): the function works on the original variable.
- `const string &s` passes large strings without copying and without changing them.

```exercise cpp
? Pass the variable by reference so the original changes
void reset(int ___x) { x = 0; }
= &
```

```quiz
? What happens when a variable is passed by reference &?
* The function changes the original variable
- The function works on a copy
- The variable is deleted

? Two functions may share a name if their parameters differ.
= true
```

# @lesson cpp-pointers
title: References and pointers
summary: The address &, the pointer *, nullptr, and smart pointers.
---
A **pointer** is a variable that holds the **address** of another variable in memory:

```try cpp
#include <iostream>
#include <memory>
using namespace std;

int main() {
    int x = 10;
    int *p = &x;          // p points to x
    cout << "address: " << p << endl;
    cout << "value: " << *p << endl;
    *p = 25;              // change through the pointer
    cout << "x = " << x << endl;

    int &ref = x;         // a reference: another name for the same variable
    ref++;
    cout << "x = " << x << endl;

    int *nothing = nullptr;
    if (nothing == nullptr) cout << "pointer is empty" << endl;

    unique_ptr<int> smart(new int(99));   // frees the memory automatically
    cout << *smart << endl;
    return 0;
}
```

```reference cpp
&x | Address of the variable | int *p = &x;
*p | The value at the address | cout << *p;
int &r = x | Reference (another name) | r = 5;
nullptr | Empty pointer | int *p = nullptr;
new / delete | Manual allocation and freeing | int *a = new int[5]; delete[] a;
unique_ptr | Smart pointer that frees memory | unique_ptr<int> p(new int(1));
```

:::danger Avoid manual new and delete
Forgetting `delete` leaks memory. Use `vector`, `string` and smart pointers; they free memory automatically.
:::

```quiz
? What does & before a variable name, as in &x, give?
* The variable's address in memory
- The variable's value
- A copy of the variable

? unique_ptr frees the memory automatically.
= true
```

# @lesson cpp-classes
title: Classes
summary: Fields, methods, the constructor, public and private.
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

- `private`: only the class itself can reach it. `public`: open to everyone.
- `: owner(o), balance(b)` is the constructor's initializer list.
- `const` after a method: it does not change the object.

```quiz
? Why make fields private?
* To protect the data and force access through the class's methods
- To speed the program up
- To hide the whole class

? const after a method name means it does not change the object.
= true
```

# @lesson cpp-inheritance
title: Inheritance and virtual functions
summary: Inheritance, virtual, and polymorphism.
---
```try cpp
#include <iostream>
#include <vector>
#include <memory>
using namespace std;

class Shape {
public:
    virtual double area() const = 0;      // pure virtual
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

- `virtual` makes a call pick the function of the actual class (polymorphism).
- `= 0` is a pure virtual function: children must define it.
- `override` has the compiler check that you really redefine an existing function.

```quiz
? Which keyword enables polymorphism in C++?
* virtual
- static
- inline

? A class with a function = 0 cannot be instantiated directly.
= true
```

# @lesson cpp-stl
title: The STL
summary: map, set, algorithm and lambdas.
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
    sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // descending
    int total = accumulate(v.begin(), v.end(), 0);
    int evens = count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    cout << v[0] << " " << total << " " << evens << endl;
    return 0;
}
```

```reference cpp
map | Sorted key and value | map<string,int> m; m["a"] = 1;
unordered_map | Faster key and value, unsorted | unordered_map<int,int> m;
set | Sorted values without repeats | set<int> s; s.insert(3);
sort | Sort | sort(v.begin(), v.end())
find | Search | find(v.begin(), v.end(), x)
accumulate | Total | accumulate(v.begin(), v.end(), 0)
count_if | Count with a condition | count_if(b, e, pred)
lambda | Short function | [](int a) { return a * 2; }
```

```quiz
? Which container keeps sorted values without repeats?
- vector
* set
- map

? [](int x) { return x * 2; } is a lambda function.
= true
```

# @lesson cpp-project
title: Project: grade statistics
summary: A program that combines vectors, functions and algorithms.
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

- `struct` is like `class`, but its members are `public` by default.
- `fixed` and `setprecision(1)` show one decimal place, and `setw` lines up columns.

```quiz
? What is the main difference between struct and class in C++?
* struct members are public by default
- struct cannot have functions
- A struct cannot be sorted

? setprecision controls how many decimals are printed.
= true
```

# @lesson cpp-reference
title: C++ reference
summary: The most important keywords and libraries with an example for each.
type: Reference
---
Search the table for any keyword.

```reference cpp
#include | Add a library | #include <vector>
main | Entry point | int main() { return 0; }
cout / cin | Output / input | cout << x << endl;
int / double / bool / char | Basic types | int n = 0;
string | Text | string s = "hi";
auto / const | Inference / constant | const auto x = 5;
if / switch | Conditions | if (a > b) { … }
for / while | Loops | for (int x : v) { … }
vector | Dynamic array | vector<int> v;
map / set | Containers | map<string,int> m;
& | Reference / address | void f(int &x)
* | Pointer / value | int *p = &x;
class / struct | Classes | class A { public: … };
virtual / override | Polymorphism | virtual double area() const = 0;
unique_ptr | Smart pointer | unique_ptr<A> p(new A());
try / catch / throw | Exceptions | throw runtime_error("…");
sort / find | Algorithms | sort(v.begin(), v.end())
lambda | Short function | [](int a) { return a + 1; }
```

:::tip What next?
Install g++ or Visual Studio, and practise competitive programming problems; C++ is the most popular language there.
:::
