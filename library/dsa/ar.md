# @lesson dsa-intro
title: مقدمة وتعقيد الخوارزميات
summary: ما هي الخوارزمية، وكيف نقيس سرعتها بـ Big O.
---
**الخوارزمية** خطوات واضحة لحل مشكلة. و**هيكل البيانات** طريقة لتنظيم البيانات في الذاكرة. اختيار الهيكل والخوارزمية الصحيحين قد يجعل برنامجك أسرع ألف مرة.

## Big O

يصف كيف يزيد وقت التنفيذ عندما يكبر حجم البيانات `n`:

```reference python
O(1) | ثابت: لا يتأثر بالحجم | الوصول لعنصر: a[5]
O(log n) | لوغاريتمي: ينصّف المشكلة كل خطوة | البحث الثنائي
O(n) | خطي: يمر على كل عنصر | البحث الخطي، sum(a)
O(n log n) | الترتيب السريع الجيد | ترتيب الدمج، sorted()
O(n²) | تربيعي: حلقة داخل حلقة | ترتيب الفقاعة
```

```try python
import time

def count_pairs(n):          # O(n²)
    c = 0
    for i in range(n):
        for j in range(n):
            c += 1
    return c

for n in [100, 200, 400]:
    t = time.perf_counter()
    count_pairs(n)
    print(n, "→", round((time.perf_counter() - t) * 1000, 1), "مللي ثانية")
```

لاحظ: مضاعفة `n` تضاعف الوقت **أربع مرات** تقريبًا؛ هذه علامة O(n²).

```quiz
? ما تعقيد الوصول لعنصر في قائمة بموضعه a[5]؟
* O(1)
- O(n)
- O(n²)

? حلقة داخل حلقة على نفس البيانات تعطي غالبًا تعقيد O(n²).
= true
```

# @lesson dsa-recursion
title: الاستدعاء الذاتي
summary: دالة تستدعي نفسها، وحالة التوقف، والذاكرة المؤقتة.
---
**الاستدعاء الذاتي** دالة تحل المشكلة بحل نسخة أصغر منها، حتى تصل لحالة بسيطة تتوقف عندها:

```try python
def factorial(n):
    if n <= 1:          # حالة التوقف
        return 1
    return n * factorial(n - 1)

print(factorial(5))
```

## فيبوناتشي والذاكرة المؤقتة

الحل المباشر يكرر نفس الحسابات كثيرًا. نحفظ النتائج لنتجنب التكرار:

```try python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
print(fib(80))
```

:::warning لا تنسَ حالة التوقف
بدونها تستدعي الدالة نفسها إلى الأبد حتى يحدث `RecursionError`.
:::

```exercise python
? أكمل حالة التوقف
def countdown(n):
    if n == ___:
        print("انطلق!")
        return
    print(n)
    countdown(n - 1)
= 0
```

```quiz
? ما أهم جزء في أي دالة ذاتية الاستدعاء؟
* حالة التوقف
- الحلقة for
- المتغير العام

? الأداة lru_cache تحفظ النتائج لتجنب إعادة الحساب.
= true
```

# @lesson dsa-search
title: البحث الخطي والثنائي
summary: البحث في كل العناصر، والبحث بالتنصيف في البيانات المرتبة.
---
## البحث الخطي O(n)

```try python
def linear_search(items, target):
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1

print(linear_search([7, 3, 9, 1], 9))
```

## البحث الثنائي O(log n)

يعمل فقط على بيانات **مرتبة**: يقارن بالعنصر الأوسط ويتخلص من النصف الخطأ كل مرة:

```try python
def binary_search(items, target):
    low, high = 0, len(items) - 1
    steps = 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if items[mid] == target:
            return mid, steps
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps

data = list(range(0, 1_000_000, 3))
print(binary_search(data, 999_999))
```

ثلث مليون عنصر تقريبًا في حوالي 20 خطوة فقط!

```exercise python
? أكمل حساب موضع المنتصف
mid = (low + high) ___ 2
= //
```

```quiz
? ما شرط استخدام البحث الثنائي؟
* أن تكون البيانات مرتبة
- أن تكون البيانات أرقامًا فردية
- أن تكون صغيرة

? تعقيد البحث الثنائي O(log n).
= true
```

# @lesson dsa-simple-sorts
title: خوارزميات الترتيب البسيطة
summary: الفقاعة والاختيار والإدراج.
---
## ترتيب الفقاعة O(n²)

يقارن كل عنصرين متجاورين ويبدّلهما إن كانا بترتيب خطأ:

```try python
def bubble_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:      # مرتبة بالفعل
            break
    return a

print(bubble_sort([5, 2, 9, 1, 7]))
```

## ترتيب الإدراج O(n²)

يبني الجزء المرتب عنصرًا عنصرًا، كترتيب أوراق اللعب في اليد:

```try python
def insertion_sort(a):
    a = a[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

print(insertion_sort([8, 4, 6, 2, 9]))
```

:::info متى تفيد؟
الخوارزميات البسيطة سهلة الفهم ومناسبة للقوائم الصغيرة أو شبه المرتبة. للقوائم الكبيرة استخدم الخوارزميات السريعة في الدرس التالي.
:::

```quiz
? ما تعقيد ترتيب الفقاعة في أسوأ حالة؟
- O(n)
- O(log n)
* O(n²)

? ترتيب الإدراج سريع جدًا على القوائم شبه المرتبة.
= true
```

# @lesson dsa-fast-sorts
title: الترتيب السريع وترتيب الدمج
summary: فرّق تسد: الدمج والترتيب السريع بتعقيد n log n.
---
## ترتيب الدمج O(n log n)

يقسم القائمة نصفين، يرتب كل نصف، ثم يدمجهما:

```try python
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

## الترتيب السريع

يختار عنصرًا «محوريًا» ويضع الأصغر قبله والأكبر بعده:

```try python
def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    return (quick_sort([x for x in a if x < pivot])
            + [x for x in a if x == pivot]
            + quick_sort([x for x in a if x > pivot]))

print(quick_sort([3, 6, 8, 10, 1, 2, 1]))
```

:::tip في الواقع
دالة بايثون `sorted()` تستخدم خوارزمية **Timsort** المحسّنة، وهي أسرع من أي ترتيب تكتبه بنفسك. تعلّم الخوارزميات لتفهم، واستخدم `sorted` في عملك.
:::

```quiz
? ما فكرة «فرّق تسد»؟
* تقسيم المشكلة إلى أجزاء أصغر وحل كل جزء ثم الجمع
- تجربة كل الحلول الممكنة
- الترتيب من البداية للنهاية مرة واحدة

? تعقيد ترتيب الدمج O(n log n).
= true
```

# @lesson dsa-stack-queue
title: المكدس والطابور
summary: آخر داخل أول خارج، وأول داخل أول خارج.
---
## المكدس (Stack): آخر داخل أول خارج

مثل كومة الأطباق. يُستخدم في التراجع (Undo) وتتبع الاستدعاءات وفحص الأقواس:

```try python
def balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

print(balanced("(a[b]{c})"), balanced("(a[b)]"))
```

## الطابور (Queue): أول داخل أول خارج

مثل طابور البنك. `deque` تضيف وتحذف من الطرفين بسرعة O(1):

```try python
from collections import deque

queue = deque()
queue.append("عميل 1")
queue.append("عميل 2")
queue.append("عميل 3")
print("يُخدم:", queue.popleft())
print("المتبقي:", list(queue))
```

:::warning لا تستخدم list.pop(0) للطوابير
حذف أول عنصر من القائمة O(n) لأن كل العناصر تتحرك. `deque.popleft()` O(1).
:::

```quiz
? أي هيكل يعمل بمبدأ «آخر داخل أول خارج»؟
* المكدس Stack
- الطابور Queue
- القاموس

? الدالة deque.popleft تحذف من بداية الطابور بسرعة O(1).
= true
```

# @lesson dsa-linked-list
title: القوائم المترابطة
summary: عقد مرتبطة بمؤشرات، ومقارنتها بالمصفوفة.
---
**القائمة المترابطة** سلسلة من **العقد**؛ كل عقدة تحمل قيمة ومؤشرًا للعقدة التالية:

```try python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def push_front(self, value):       # O(1)
        node = Node(value)
        node.next = self.head
        self.head = node

    def find(self, value):              # O(n)
        cur = self.head
        while cur:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def __str__(self):
        out, cur = [], self.head
        while cur:
            out.append(str(cur.value))
            cur = cur.next
        return " → ".join(out)

lst = LinkedList()
for v in [3, 2, 1]:
    lst.push_front(v)
print(lst, lst.find(2))
```

```reference python
الوصول بالموضع | مصفوفة O(1) / مترابطة O(n) | a[5]
الإضافة في البداية | مصفوفة O(n) / مترابطة O(1) | push_front
البحث | الاثنتان O(n) | find
الذاكرة | المترابطة تحتاج مساحة للمؤشرات | node.next
```

```quiz
? ما الذي تحمله كل عقدة في القائمة المترابطة؟
* قيمة ومؤشرًا للعقدة التالية
- قيمة فقط
- رقم موضعها

? الإضافة في بداية القائمة المترابطة O(1).
= true
```

# @lesson dsa-hash
title: جداول التجزئة
summary: القاموس والمجموعة: بحث وإضافة بسرعة O(1).
---
**جدول التجزئة** يحوّل المفتاح إلى رقم (تجزئة) يحدد مكان القيمة مباشرة، فيصبح البحث والإضافة O(1) في المتوسط. في بايثون: `dict` و `set`.

```try python
words = "تفاح موز تفاح برتقال موز تفاح".split()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)

from collections import Counter
print(Counter(words).most_common(2))
```

## مثال كلاسيكي: مجموع رقمين

أوجد رقمين مجموعهما يساوي الهدف، في O(n) بدل O(n²):

```try python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None

print(two_sum([2, 7, 11, 15], 18))
```

:::tip قاعدة ذهبية
إذا وجدت نفسك تبحث في قائمة داخل حلقة (`if x in my_list`)، فكّر في تحويلها إلى `set` أو `dict`.
:::

```quiz
? ما متوسط تعقيد البحث في القاموس dict؟
* O(1)
- O(n)
- O(n log n)

? البحث في set أسرع من البحث في list للبيانات الكبيرة.
= true
```

# @lesson dsa-trees
title: الأشجار
summary: الشجرة الثنائية، وشجرة البحث الثنائية، والمرور على العقد.
---
**الشجرة** عقد مرتبة هرميًا: جذر واحد، ولكل عقدة أبناء. في **شجرة البحث الثنائية** (BST): كل ما في اليسار أصغر من العقدة، وكل ما في اليمين أكبر:

```try python
class Node:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

def in_order(root):          # يسار، جذر، يمين → مرتب
    return in_order(root.left) + [root.key] + in_order(root.right) if root else []

def contains(root, key):
    while root:
        if key == root.key:
            return True
        root = root.left if key < root.key else root.right
    return False

root = None
for k in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, k)
print(in_order(root))
print(contains(root, 60), contains(root, 65))
```

:::info التوازن
في الشجرة المتوازنة يكون البحث O(log n). إذا أُدخلت بيانات مرتبة أصبحت الشجرة «سلسلة» وصار البحث O(n)؛ لذلك توجد أشجار تتوازن تلقائيًا مثل AVL.
:::

```quiz
? في شجرة البحث الثنائية، أين توضع القيم الأصغر من العقدة؟
* في الفرع الأيسر
- في الفرع الأيمن
- في الجذر

? المرور in-order على شجرة البحث الثنائية يعطي القيم مرتبة.
= true
```

# @lesson dsa-graphs
title: الرسوم البيانية
summary: تمثيل الرسم، والبحث بالعرض BFS، والبحث بالعمق DFS.
---
**الرسم البياني** عقد (رؤوس) وروابط (حواف): مدن وطرق، أشخاص وصداقات، صفحات وروابط. نمثله بقاموس قوائم الجيران:

```try python
from collections import deque

graph = {
    "الرياض": ["جدة", "الدمام"],
    "جدة": ["الرياض", "مكة"],
    "الدمام": ["الرياض", "الخبر"],
    "مكة": ["جدة"],
    "الخبر": ["الدمام"],
}

def bfs(start, goal):          # أقصر طريق بعدد الحواف
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for nxt in graph[path[-1]]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + [nxt])

def dfs(node, seen=None):      # زيارة كل ما يمكن الوصول إليه
    seen = seen if seen is not None else []
    seen.append(node)
    for nxt in graph[node]:
        if nxt not in seen:
            dfs(nxt, seen)
    return seen

print(" → ".join(bfs("مكة", "الخبر")))
print(dfs("الرياض"))
```

- **BFS** يستكشف طبقة طبقة بطابور؛ يجد أقصر طريق في الرسوم غير الموزونة.
- **DFS** يتعمق في فرع حتى النهاية بمكدس أو استدعاء ذاتي.

```quiz
? أي خوارزمية تجد أقصر طريق بعدد الحواف في رسم غير موزون؟
* BFS
- DFS
- ترتيب الفقاعة

? الخوارزمية BFS تستخدم طابورًا.
= true
```

# @lesson dsa-reference
title: مرجع هياكل البيانات
summary: الهياكل والخوارزميات وتعقيدها في جدول واحد.
type: Reference
---
ابحث في الجدول عن أي هيكل أو خوارزمية.

```reference python
list | مصفوفة ديناميكية: وصول O(1)، إضافة في النهاية O(1) | a.append(x)
dict | جدول تجزئة: بحث وإضافة O(1) | d[key] = v
set | مجموعة: هل يوجد؟ O(1) | x in s
deque | طابور: إضافة وحذف من الطرفين O(1) | q.popleft()
heapq | كومة: أصغر عنصر O(1)، إضافة O(log n) | heapq.heappush(h, x)
stack | مكدس بقائمة: append و pop | s.append(x); s.pop()
linked list | إضافة في البداية O(1) | node.next = head
BST | بحث O(log n) إذا كانت متوازنة | contains(root, k)
linear search | O(n) | for x in items
binary search | O(log n) على بيانات مرتبة | bisect.bisect_left(a, x)
bubble / insertion sort | O(n²) | للقوائم الصغيرة
merge / quick sort | O(n log n) | فرّق تسد
sorted() | Timsort: O(n log n) | sorted(a)
BFS | أقصر طريق بعدد الحواف | deque
DFS | استكشاف عميق | استدعاء ذاتي
```

:::tip ماذا بعد؟
تدرّب على مسائل حقيقية في مواقع التدريب البرمجي، وابدأ بالمسائل «السهلة» في المصفوفات والقواميس.
:::
