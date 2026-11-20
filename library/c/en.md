# @lesson c-intro
title: C introduction
summary: What the C language is, and your first program.
---
**C** is one of the oldest and most influential programming languages. Operating systems (Linux and parts of Windows), databases, embedded devices and the Python interpreter itself are written in it. Learning it shows you how memory and the computer really work.

```try c
#include <stdio.h>

int main(void) {
    printf("Hello, C\n");
    printf("%d\n", 6 * 7);
    return 0;
}
```

- `#include <stdio.h>` is the input/output library.
- The program starts at `main`.
- `printf` prints, and `\n` is a new line.

:::info Running the examples
C examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: `gcc main.c -o main`, then `./main`.
:::

```quiz
? Which library contains printf?
* stdio.h
- string.h
- math.h

? \n means a new line.
= true
```

# @lesson c-variables
title: Variables and printf
summary: Basic types, format specifiers, and const.
---
```try c
#include <stdio.h>

int main(void) {
    int age = 25;
    float height = 1.65f;
    double price = 19.99;
    char grade = 'A';
    const int MAX = 100;
    printf("age=%d height=%.2f price=%.2f grade=%c max=%d\n", age, height, price, grade, MAX);
    printf("size of int: %zu bytes\n", sizeof(int));
    return 0;
}
```

```reference c
%d | Whole number int | printf("%d", 5)
%f / %.2f | Decimal (with two places) | printf("%.2f", 3.14159)
%c | One character | printf("%c", 'x')
%s | String | printf("%s", "hi")
%zu | A sizeof size | printf("%zu", sizeof(int))
%x | Hexadecimal | printf("%x", 255)
```

:::info No built-in string or boolean type
A string in C is an array of characters. Booleans are numbers: `0` is false and anything else is true (you can use `bool` from `stdbool.h`).
:::

```exercise c
? Print a decimal number with two places
printf("___", price);
= %.2f
```

```quiz
? Which format specifier prints a whole number?
* %d
- %s
- %c

? In C the value 0 means "false" in conditions.
= true
```

# @lesson c-operators
title: Operators
summary: Arithmetic, integer division, comparison and logic.
---
```try c
#include <stdio.h>

int main(void) {
    int a = 17, b = 5;
    printf("%d %d %d\n", a + b, a / b, a % b);
    printf("%.2f\n", (double)a / b);
    printf("%d %d\n", a > b, a == b);
    printf("%d\n", (a > 0) && (b > 0));
    a += 3;
    a++;
    printf("%d\n", a);
    return 0;
}
```

```reference c
+ - * / % | Arithmetic and remainder | 17 % 5 → 2
++ / -- | Increment / decrement | i++
+= -= | Assign with an operation | x += 2
== != > < | Comparison (1 or 0) | a == b
&& || ! | Logic | a && b
(double) | Type cast | (double)a / b
```

```quiz
? What is 17 / 5 in C when both numbers are int?
* 3
- 3.4
- 4

? The comparison a > b gives 1 when it is true.
= true
```

# @lesson c-conditions-loops
title: Conditions and loops
summary: if, switch, for, while and do-while.
---
```try c
#include <stdio.h>

int main(void) {
    int score = 82;
    if (score >= 90) printf("Excellent\n");
    else if (score >= 75) printf("Very good\n");
    else printf("Try again\n");

    for (int i = 1; i <= 5; i++) printf("%d ", i);
    printf("\n");

    int n = 3;
    while (n > 0) {
        printf("count %d\n", n);
        n--;
    }

    int k = 0;
    do {
        printf("runs at least once: k=%d\n", k);
    } while (k > 0);

    switch (score / 10) {
        case 9: printf("A\n"); break;
        case 8: printf("B\n"); break;
        default: printf("C or less\n");
    }
    return 0;
}
```

`do … while` runs its block at least once before checking the condition.

```quiz
? Which loop runs at least once?
- for
- while
* do-while

? In a switch, break stops the following cases from running.
= true
```

# @lesson c-arrays-strings
title: Arrays and strings
summary: Arrays, strings as character arrays, and string.h functions.
---
```try c
#include <stdio.h>
#include <string.h>

int main(void) {
    int scores[] = {88, 72, 95, 60};
    int count = sizeof(scores) / sizeof(scores[0]);
    int sum = 0;
    for (int i = 0; i < count; i++) sum += scores[i];
    printf("count=%d avg=%.1f\n", count, (double)sum / count);

    char name[20] = "Sara";
    printf("%s has %zu letters\n", name, strlen(name));
    strcat(name, " Ahmed");
    printf("%s\n", name);
    printf("%d\n", strcmp("abc", "abd") < 0);

    char copy[20];
    strcpy(copy, name);
    copy[0] = 'Z';
    printf("%s / %s\n", name, copy);
    return 0;
}
```

- A string is an array of characters ending with the special character `'\0'`.
- `strlen` is the length, `strcpy` copies, `strcat` joins, `strcmp` compares.

:::danger Beware of going past the end
C does not check array bounds. Writing outside an array (such as a string longer than 20 characters in `name[20]`) corrupts memory and causes security holes.
:::

```exercise c
? Get the length of the string
size_t n = ___(name);
= strlen
```

```quiz
? Which character ends a string in C?
* '\0'
- '\n'
- ' '

? C checks array bounds automatically.
= false
```

# @lesson c-functions
title: Functions
summary: Definitions, prototypes, passing by value, and recursion.
---
```try c
#include <stdio.h>

int square(int x);                 /* prototype: declares the function before its definition */
long factorial(int n);
void swap(int *a, int *b);

int main(void) {
    printf("%d\n", square(7));
    printf("%ld\n", factorial(10));
    int x = 1, y = 2;
    swap(&x, &y);
    printf("x=%d y=%d\n", x, y);
    return 0;
}

int square(int x) { return x * x; }

long factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }

void swap(int *a, int *b) {        /* through pointers, to change the originals */
    int t = *a;
    *a = *b;
    *b = t;
}
```

- C always passes arguments **by value**; to change the caller's variable, pass its address (a pointer).
- `void` is a function that returns nothing.

```quiz
? How do you let a function change a variable from outside it in C?
* Pass its address as a pointer
- With the keyword ref
- It cannot be done

? A prototype declares a function before its full definition.
= true
```

# @lesson c-pointers
title: Pointers
summary: Address and value, pointers and arrays, and NULL.
---
```try c
#include <stdio.h>

int main(void) {
    int x = 10;
    int *p = &x;
    printf("value=%d via pointer=%d\n", x, *p);
    *p = 25;
    printf("x=%d\n", x);

    int nums[] = {10, 20, 30};
    int *q = nums;                  /* an array's name is the address of its first item */
    printf("%d %d %d\n", *q, *(q + 1), q[2]);

    int *none = NULL;
    if (none == NULL) printf("pointer is NULL\n");
    return 0;
}
```

```reference c
&x | Address of x | int *p = &x;
*p | The value at the address | *p = 5;
p + 1 | The next item | *(p + 1)
NULL | Empty pointer | int *p = NULL;
-> | Struct member through a pointer | ptr->name
```

:::warning Never use a null pointer
Reading `*p` while `p` is `NULL` crashes the program (segmentation fault). Always check before use.
:::

```quiz
? What does *(q + 1) give when q points to the first item of an array?
* The second item
- The address of the array
- The first item plus one

? An array's name in C works as the address of its first item.
= true
```

# @lesson c-structs
title: Structs
summary: Grouping related data, typedef, and pointers to structs.
---
```try c
#include <stdio.h>
#include <string.h>

typedef struct {
    char name[30];
    int age;
    double salary;
} Employee;

void raise_salary(Employee *e, double percent) {
    e->salary *= 1 + percent / 100;
}

int main(void) {
    Employee team[2] = {{"Ali", 30, 8000}, {"Mona", 27, 9500}};
    strcpy(team[0].name, "Ali Hassan");
    raise_salary(&team[1], 10);
    for (int i = 0; i < 2; i++) {
        printf("%-12s %d %.0f\n", team[i].name, team[i].age, team[i].salary);
    }
    return 0;
}
```

- `.` reaches a member of a struct, and `->` does it through a pointer.
- `typedef` gives the struct a short name.

```exercise c
? Reach the salary member through the pointer e
e___salary = 0;
= ->
```

```quiz
? When do we use -> instead of a dot?
* When reaching a member through a pointer to a struct
- Only with arrays
- With functions

? typedef gives a type a new name.
= true
```

# @lesson c-memory
title: Dynamic memory
summary: malloc, calloc, realloc and free.
---
When you do not know the size in advance, allocate memory while the program runs:

```try c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 5;
    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) return 1;              /* allocation failed */
    for (int i = 0; i < n; i++) arr[i] = (i + 1) * 10;

    n = 8;
    int *bigger = realloc(arr, n * sizeof(int));   /* grow */
    if (bigger == NULL) { free(arr); return 1; }
    arr = bigger;
    for (int i = 5; i < n; i++) arr[i] = 0;

    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    free(arr);                               /* do not forget to free */
    arr = NULL;
    return 0;
}
```

```reference c
malloc(size) | Allocate memory (uninitialized) | malloc(n * sizeof(int))
calloc(n, size) | Allocate zeroed memory | calloc(n, sizeof(int))
realloc(p, size) | Resize | realloc(p, 2 * size)
free(p) | Free the memory | free(p); p = NULL;
```

:::danger Memory rules
Every `malloc` is matched by exactly one `free`. Never use memory after freeing it, and never free it twice. These mistakes are the most common causes of security holes in C programs.
:::

```quiz
? What must you do with all memory allocated with malloc?
* Free it with free when done
- Nothing; it is freed automatically
- Delete it with delete

? calloc allocates memory filled with zeros.
= true
```

# @lesson c-files
title: Files
summary: fopen, fprintf, fgets and fclose.
---
```try c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("notes.txt", "w");
    if (f == NULL) { perror("open"); return 1; }
    fprintf(f, "line one\nline two\n");
    fclose(f);

    f = fopen("notes.txt", "r");
    if (f == NULL) { perror("open"); return 1; }
    char line[100];
    int n = 0;
    while (fgets(line, sizeof line, f)) {
        printf("%d: %s", ++n, line);
    }
    fclose(f);
    return 0;
}
```

```reference c
fopen(name, "r") | Open for reading | fopen("a.txt", "r")
fopen(name, "w") | Open for writing (erases old content) | fopen("a.txt", "w")
fopen(name, "a") | Append at the end | fopen("a.txt", "a")
fprintf | Formatted writing | fprintf(f, "%d\n", x)
fgets | Read a line | fgets(buf, sizeof buf, f)
fclose | Close the file | fclose(f)
```

```quiz
? What does fopen return if the file cannot be opened?
* NULL
- Always 0
- -1

? You must close a file with fclose when done.
= true
```

# @lesson c-reference
title: C reference
summary: The most important keywords and functions with an example for each.
type: Reference
---
Search the table for any keyword.

```reference c
#include | Add a library | #include <stdio.h>
main | Entry point | int main(void) { return 0; }
printf / scanf | Output / input | printf("%d\n", x);
int / double / char | Types | int n = 0;
const | Constant | const int MAX = 10;
if / switch | Conditions | if (x > 0) { … }
for / while / do | Loops | for (int i = 0; i < n; i++)
int a[10] | Array | int a[3] = {1, 2, 3};
char s[] | String | char s[] = "hi";
strlen / strcpy / strcmp | String functions | strlen(s)
& / * | Address / value | int *p = &x;
struct / typedef | Structs | typedef struct { int x; } P;
-> | Member through a pointer | p->x
malloc / free | Dynamic memory | int *a = malloc(n * sizeof *a);
fopen / fclose | Files | FILE *f = fopen("a", "r");
sizeof | Size of a type | sizeof(int)
NULL | Empty pointer | if (p == NULL)
```

:::tip What next?
After C, learning C++ is easy, and you understand deeply how languages such as Python and Java work inside.
:::
