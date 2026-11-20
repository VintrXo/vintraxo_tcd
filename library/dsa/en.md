# @lesson dsa-intro
title: Introduction and complexity
summary: What an algorithm is, and how to measure its speed with Big O.
---
An **algorithm** is a clear set of steps to solve a problem. A **data structure** is a way of organizing data in memory. Choosing the right structure and algorithm can make your program a thousand times faster.

## Big O

It describes how running time grows as the data size `n` grows:

```reference python
O(1) | Constant: not affected by size | Reading an item: a[5]
O(log n) | Logarithmic: halves the problem each step | Binary search
O(n) | Linear: visits every item | Linear search, sum(a)
O(n log n) | A good fast sort | Merge sort, sorted()
O(n²) | Quadratic: a loop inside a loop | Bubble sort
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
    print(n, "→", round((time.perf_counter() - t) * 1000, 1), "ms")
```

Notice: doubling `n` makes the time about **four times** longer; that is the sign of O(n²).

```quiz
? What is the complexity of reading a list item by position, a[5]?
* O(1)
- O(n)
- O(n²)

? A loop inside a loop over the same data is usually O(n²).
= true
```

# @lesson dsa-recursion
title: Recursion
summary: A function that calls itself, the base case, and caching.
---
**Recursion** is a function that solves a problem by solving a smaller copy of it, until it reaches a simple case where it stops:

```try python
def factorial(n):
    if n <= 1:          # the base case
        return 1
    return n * factorial(n - 1)

print(factorial(5))
```

## Fibonacci and caching

The direct solution repeats the same work many times. We save results to avoid repeating:

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

:::warning Do not forget the base case
Without it the function calls itself forever until a `RecursionError` happens.
:::

```exercise python
? Complete the base case
def countdown(n):
    if n == ___:
        print("Go!")
        return
    print(n)
    countdown(n - 1)
= 0
```

```quiz
? What is the most important part of any recursive function?
* The base case
- A for loop
- A global variable

? lru_cache saves results to avoid computing them again.
= true
```

# @lesson dsa-search
title: Linear and binary search
summary: Checking every item, and searching by halving sorted data.
---
## Linear search O(n)

```try python
def linear_search(items, target):
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1

print(linear_search([7, 3, 9, 1], 9))
```

## Binary search O(log n)

It only works on **sorted** data: it compares with the middle item and throws away the wrong half each time:

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

About a third of a million items in only around 20 steps!

```exercise python
? Complete the calculation of the middle position
mid = (low + high) ___ 2
= //
```

```quiz
? What does binary search require?
* The data must be sorted
- The data must be odd numbers
- The data must be small

? Binary search is O(log n).
= true
```

# @lesson dsa-simple-sorts
title: Simple sorting algorithms
summary: Bubble, selection and insertion sort.
---
## Bubble sort O(n²)

Compares each pair of neighbors and swaps them if they are in the wrong order:

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
        if not swapped:      # already sorted
            break
    return a

print(bubble_sort([5, 2, 9, 1, 7]))
```

## Insertion sort O(n²)

Builds the sorted part one item at a time, like sorting playing cards in your hand:

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

:::info When are they useful?
Simple algorithms are easy to understand and fine for small or nearly sorted lists. For large lists use the fast algorithms of the next lesson.
:::

```quiz
? What is bubble sort's worst-case complexity?
- O(n)
- O(log n)
* O(n²)

? Insertion sort is very fast on nearly sorted lists.
= true
```

# @lesson dsa-fast-sorts
title: Merge sort and quick sort
summary: Divide and conquer: merge and quick sort in n log n.
---
## Merge sort O(n log n)

Splits the list in two, sorts each half, then merges them:

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

## Quick sort

Picks a "pivot" item and puts smaller items before it and larger ones after:

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

:::tip In practice
Python's `sorted()` uses the optimized **Timsort** algorithm, faster than any sort you write yourself. Learn the algorithms to understand them, and use `sorted` at work.
:::

```quiz
? What is the idea of "divide and conquer"?
* Split the problem into smaller parts, solve each, then combine
- Try every possible solution
- Sort from start to end in one pass

? Merge sort is O(n log n).
= true
```

# @lesson dsa-stack-queue
title: Stacks and queues
summary: Last in, first out; and first in, first out.
---
## Stack: last in, first out

Like a pile of plates. Used for undo, tracking function calls and checking brackets:

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

## Queue: first in, first out

Like a line at the bank. `deque` adds and removes at both ends in O(1):

```try python
from collections import deque

queue = deque()
queue.append("customer 1")
queue.append("customer 2")
queue.append("customer 3")
print("Serving:", queue.popleft())
print("Waiting:", list(queue))
```

:::warning Do not use list.pop(0) for queues
Removing the first item of a list is O(n) because every item moves. `deque.popleft()` is O(1).
:::

```quiz
? Which structure works as "last in, first out"?
* Stack
- Queue
- Dictionary

? deque.popleft removes from the front of a queue in O(1).
= true
```

# @lesson dsa-linked-list
title: Linked lists
summary: Nodes joined by pointers, compared with arrays.
---
A **linked list** is a chain of **nodes**; each node holds a value and a pointer to the next node:

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
Access by position | Array O(1) / linked O(n) | a[5]
Insert at the front | Array O(n) / linked O(1) | push_front
Search | Both O(n) | find
Memory | Linked lists need room for pointers | node.next
```

```quiz
? What does each node of a linked list hold?
* A value and a pointer to the next node
- Only a value
- Its position number

? Inserting at the front of a linked list is O(1).
= true
```

# @lesson dsa-hash
title: Hash tables
summary: Dictionaries and sets: lookup and insert in O(1).
---
A **hash table** turns a key into a number (a hash) that says directly where the value lives, so lookup and insert are O(1) on average. In Python: `dict` and `set`.

```try python
words = "apple banana apple orange banana apple".split()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)

from collections import Counter
print(Counter(words).most_common(2))
```

## A classic: two sum

Find two numbers that add up to a target, in O(n) instead of O(n²):

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

:::tip A golden rule
If you find yourself searching a list inside a loop (`if x in my_list`), think about turning it into a `set` or `dict`.
:::

```quiz
? What is the average complexity of a lookup in a dict?
* O(1)
- O(n)
- O(n log n)

? Searching a set is faster than searching a list for large data.
= true
```

# @lesson dsa-trees
title: Trees
summary: Binary trees, binary search trees, and walking the nodes.
---
A **tree** is nodes arranged in a hierarchy: one root, and each node has children. In a **binary search tree** (BST), everything on the left is smaller than the node and everything on the right is larger:

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

def in_order(root):          # left, root, right → sorted
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

:::info Balance
In a balanced tree search is O(log n). If sorted data is inserted, the tree becomes a "chain" and search becomes O(n); that is why self-balancing trees such as AVL exist.
:::

```quiz
? In a binary search tree, where do values smaller than a node go?
* In the left branch
- In the right branch
- At the root

? An in-order walk of a binary search tree gives the values sorted.
= true
```

# @lesson dsa-graphs
title: Graphs
summary: Representing a graph, breadth-first search BFS and depth-first search DFS.
---
A **graph** is nodes (vertices) and links (edges): cities and roads, people and friendships, pages and links. We represent it as a dictionary of neighbor lists:

```try python
from collections import deque

graph = {
    "Riyadh": ["Jeddah", "Dammam"],
    "Jeddah": ["Riyadh", "Mecca"],
    "Dammam": ["Riyadh", "Khobar"],
    "Mecca": ["Jeddah"],
    "Khobar": ["Dammam"],
}

def bfs(start, goal):          # shortest path by number of edges
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

def dfs(node, seen=None):      # visit everything reachable
    seen = seen if seen is not None else []
    seen.append(node)
    for nxt in graph[node]:
        if nxt not in seen:
            dfs(nxt, seen)
    return seen

print(" → ".join(bfs("Mecca", "Khobar")))
print(dfs("Riyadh"))
```

- **BFS** explores layer by layer with a queue; it finds the shortest path in unweighted graphs.
- **DFS** goes deep down one branch to the end, with a stack or recursion.

```quiz
? Which algorithm finds the shortest path by number of edges in an unweighted graph?
* BFS
- DFS
- Bubble sort

? BFS uses a queue.
= true
```

# @lesson dsa-reference
title: Data structures reference
summary: Structures, algorithms and their complexity in one table.
type: Reference
---
Search the table for any structure or algorithm.

```reference python
list | Dynamic array: access O(1), append O(1) | a.append(x)
dict | Hash table: lookup and insert O(1) | d[key] = v
set | Set: membership O(1) | x in s
deque | Queue: add and remove at both ends O(1) | q.popleft()
heapq | Heap: smallest item O(1), push O(log n) | heapq.heappush(h, x)
stack | Stack with a list: append and pop | s.append(x); s.pop()
linked list | Insert at the front O(1) | node.next = head
BST | Search O(log n) when balanced | contains(root, k)
linear search | O(n) | for x in items
binary search | O(log n) on sorted data | bisect.bisect_left(a, x)
bubble / insertion sort | O(n²) | For small lists
merge / quick sort | O(n log n) | Divide and conquer
sorted() | Timsort: O(n log n) | sorted(a)
BFS | Shortest path by edges | deque
DFS | Deep exploration | Recursion
```

:::tip What next?
Practise on real problems on coding practice sites, starting with the "easy" problems on arrays and dictionaries.
:::
