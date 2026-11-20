# @lesson c-intro
title: مقدمة في C
summary: ما هي لغة C، وأول برنامج.
---
**C** من أقدم لغات البرمجة وأكثرها تأثيرًا. كُتبت بها أنظمة التشغيل (لينكس وأجزاء من ويندوز)، وقواعد البيانات، والأجهزة المدمجة، ومفسّر بايثون نفسه. تعلّمها يجعلك تفهم كيف تعمل الذاكرة والحاسوب.

```try c
#include <stdio.h>

int main(void) {
    printf("Hello, C\n");
    printf("%d\n", 6 * 7);
    return 0;
}
```

- `#include <stdio.h>` مكتبة الإدخال والإخراج.
- البرنامج يبدأ من `main`.
- `printf` تطبع، و`\n` سطر جديد.

:::info تشغيل الأمثلة
أمثلة C تعمل على خادم آمن منفصل؛ إذا لم يكن مفعّلًا بعد ستعمل فور تفعيله. على جهازك: `gcc main.c -o main` ثم `./main`.
:::

```quiz
? أي مكتبة تحتوي الدالة printf؟
* stdio.h
- string.h
- math.h

? الرمز \n يعني سطرًا جديدًا.
= true
```

# @lesson c-variables
title: المتغيرات و printf
summary: الأنواع الأساسية، ومحددات التنسيق، و const.
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
%d | عدد صحيح int | printf("%d", 5)
%f / %.2f | عدد عشري (برقمين بعد الفاصلة) | printf("%.2f", 3.14159)
%c | حرف واحد | printf("%c", 'x')
%s | نص | printf("%s", "hi")
%zu | حجم sizeof | printf("%zu", sizeof(int))
%x | ست عشري | printf("%x", 255)
```

:::info لا يوجد نوع نصي ولا منطقي أصلي
النص في C مصفوفة حروف. والقيم المنطقية أرقام: `0` خطأ وغيره صحيح (يمكن استخدام `bool` من `stdbool.h`).
:::

```exercise c
? اطبع عددًا عشريًا برقمين بعد الفاصلة
printf("___", price);
= %.2f
```

```quiz
? أي محدد تنسيق يطبع عددًا صحيحًا؟
* %d
- %s
- %c

? في لغة C القيمة 0 تعني «خطأ» في الشروط.
= true
```

# @lesson c-operators
title: العوامل
summary: الحساب والقسمة الصحيحة والمقارنة والمنطق.
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
+ - * / % | الحساب والباقي | 17 % 5 → 2
++ / -- | زيادة / نقص | i++
+= -= | إسناد مع عملية | x += 2
== != > < | المقارنة (1 أو 0) | a == b
&& || ! | المنطق | a && b
(double) | تحويل النوع | (double)a / b
```

```quiz
? ما ناتج 17 / 5 في C إذا كان الرقمان int؟
* 3
- 3.4
- 4

? المقارنة a > b تعطي 1 إذا كانت صحيحة.
= true
```

# @lesson c-conditions-loops
title: الشروط والحلقات
summary: if و switch و for و while و do-while.
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

`do … while` تنفّذ الكتلة مرة واحدة على الأقل قبل فحص الشرط.

```quiz
? أي حلقة تنفّذ مرة واحدة على الأقل؟
- for
- while
* do-while

? في switch تمنع break تنفيذ الحالات التالية.
= true
```

# @lesson c-arrays-strings
title: المصفوفات والنصوص
summary: المصفوفات، والنصوص كمصفوفات حروف، ودوال string.h.
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

- النص مصفوفة حروف تنتهي بالحرف الخاص `'\0'`.
- `strlen` الطول، `strcpy` النسخ، `strcat` الدمج، `strcmp` المقارنة.

:::danger احذر تجاوز الحدود
C لا تتحقق من حدود المصفوفة. الكتابة خارجها (مثل نص أطول من 20 حرفًا في `name[20]`) تخرّب الذاكرة وتسبب ثغرات أمنية.
:::

```exercise c
? احسب طول النص
size_t n = ___(name);
= strlen
```

```quiz
? بأي حرف ينتهي النص في C؟
* '\0'
- '\n'
- ' '

? لغة C تتحقق تلقائيًا من حدود المصفوفات.
= false
```

# @lesson c-functions
title: الدوال
summary: التعريف والنموذج الأولي والتمرير بالقيمة والاستدعاء الذاتي.
---
```try c
#include <stdio.h>

int square(int x);                 /* نموذج أولي: يعلن عن الدالة قبل تعريفها */
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

void swap(int *a, int *b) {        /* بالمؤشر لتغيير الأصل */
    int t = *a;
    *a = *b;
    *b = t;
}
```

- C تمرر المعاملات **بالقيمة** دائمًا؛ لتغيير متغير الأصل مرّر عنوانه (مؤشر).
- `void` دالة لا تُرجع شيئًا.

```quiz
? كيف تجعل الدالة تغيّر متغيرًا من خارجها في C؟
* بتمرير عنوانه كمؤشر
- بكلمة ref
- لا يمكن ذلك

? النموذج الأولي يعلن عن الدالة قبل تعريفها الكامل.
= true
```

# @lesson c-pointers
title: المؤشرات
summary: العنوان والقيمة، والمؤشرات والمصفوفات، و NULL.
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
    int *q = nums;                  /* اسم المصفوفة عنوان أول عنصر */
    printf("%d %d %d\n", *q, *(q + 1), q[2]);

    int *none = NULL;
    if (none == NULL) printf("pointer is NULL\n");
    return 0;
}
```

```reference c
&x | عنوان x | int *p = &x;
*p | القيمة في العنوان | *p = 5;
p + 1 | العنصر التالي | *(p + 1)
NULL | مؤشر فارغ | int *p = NULL;
-> | عضو في هيكل عبر مؤشر | ptr->name
```

:::warning لا تستخدم مؤشرًا فارغًا
قراءة `*p` و `p` قيمته `NULL` توقف البرنامج (Segmentation fault). تحقق دائمًا قبل الاستخدام.
:::

```quiz
? ماذا يعطي *(q + 1) إذا كان q يشير لأول عنصر في مصفوفة؟
* العنصر الثاني
- عنوان المصفوفة
- العنصر الأول زائد واحد

? اسم المصفوفة في C يعمل كعنوان أول عنصر فيها.
= true
```

# @lesson c-structs
title: الهياكل struct
summary: تجميع بيانات مترابطة، و typedef، والمؤشر إلى هيكل.
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

- `.` للوصول لعضو في هيكل، و`->` عبر مؤشر.
- `typedef` يعطي الهيكل اسمًا مختصرًا.

```exercise c
? صل لعضو salary عبر المؤشر e
e___salary = 0;
= ->
```

```quiz
? متى نستخدم -> بدل النقطة؟
* عند الوصول لعضو عبر مؤشر إلى هيكل
- مع المصفوفات فقط
- مع الدوال

? الكلمة typedef تعطي النوع اسمًا جديدًا.
= true
```

# @lesson c-memory
title: الذاكرة الديناميكية
summary: malloc و calloc و realloc و free.
---
عندما لا تعرف الحجم مسبقًا، احجز الذاكرة أثناء التشغيل:

```try c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 5;
    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) return 1;              /* فشل الحجز */
    for (int i = 0; i < n; i++) arr[i] = (i + 1) * 10;

    n = 8;
    int *bigger = realloc(arr, n * sizeof(int));   /* تكبير */
    if (bigger == NULL) { free(arr); return 1; }
    arr = bigger;
    for (int i = 5; i < n; i++) arr[i] = 0;

    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    free(arr);                               /* لا تنسَ التحرير */
    arr = NULL;
    return 0;
}
```

```reference c
malloc(size) | حجز ذاكرة (غير مهيأة) | malloc(n * sizeof(int))
calloc(n, size) | حجز ذاكرة مصفّرة | calloc(n, sizeof(int))
realloc(p, size) | تغيير الحجم | realloc(p, 2 * size)
free(p) | تحرير الذاكرة | free(p); p = NULL;
```

:::danger قواعد الذاكرة
كل `malloc` يقابله `free` واحد. لا تستخدم الذاكرة بعد تحريرها، ولا تحررها مرتين. هذه الأخطاء أشهر أسباب الثغرات في برامج C.
:::

```quiz
? ماذا يجب أن تفعل بكل ذاكرة حجزتها بـ malloc؟
* تحررها بـ free عند الانتهاء
- لا شيء؛ تُحرر تلقائيًا
- تحذفها بـ delete

? الدالة calloc تحجز ذاكرة قيمها أصفار.
= true
```

# @lesson c-files
title: الملفات
summary: fopen و fprintf و fgets و fclose.
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
fopen(name, "r") | فتح للقراءة | fopen("a.txt", "r")
fopen(name, "w") | فتح للكتابة (يمسح القديم) | fopen("a.txt", "w")
fopen(name, "a") | الإضافة في النهاية | fopen("a.txt", "a")
fprintf | كتابة منسقة | fprintf(f, "%d\n", x)
fgets | قراءة سطر | fgets(buf, sizeof buf, f)
fclose | إغلاق الملف | fclose(f)
```

```quiz
? ماذا تعيد fopen إذا فشل فتح الملف؟
* NULL
- 0 دائمًا
- -1

? يجب إغلاق الملف بـ fclose بعد الانتهاء.
= true
```

# @lesson c-reference
title: مرجع C
summary: أهم الكلمات والدوال مع مثال لكل منها.
type: Reference
---
ابحث في الجدول عن أي كلمة.

```reference c
#include | إضافة مكتبة | #include <stdio.h>
main | نقطة البداية | int main(void) { return 0; }
printf / scanf | الإخراج / الإدخال | printf("%d\n", x);
int / double / char | الأنواع | int n = 0;
const | ثابت | const int MAX = 10;
if / switch | الشروط | if (x > 0) { … }
for / while / do | الحلقات | for (int i = 0; i < n; i++)
int a[10] | مصفوفة | int a[3] = {1, 2, 3};
char s[] | نص | char s[] = "hi";
strlen / strcpy / strcmp | دوال النصوص | strlen(s)
& / * | العنوان / القيمة | int *p = &x;
struct / typedef | الهياكل | typedef struct { int x; } P;
-> | عضو عبر مؤشر | p->x
malloc / free | الذاكرة الديناميكية | int *a = malloc(n * sizeof *a);
fopen / fclose | الملفات | FILE *f = fopen("a", "r");
sizeof | حجم النوع | sizeof(int)
NULL | مؤشر فارغ | if (p == NULL)
```

:::tip ماذا بعد؟
بعد C يصبح تعلم C++ سهلًا، وتفهم بعمق كيف تعمل لغات مثل بايثون وجافا من الداخل.
:::
