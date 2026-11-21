# @lesson php-intro
title: PHP introduction
summary: What PHP is, where it runs, and your first script.
---
**PHP** is a server-side language: it runs on the web server, builds the page, and sends the browser plain HTML. A large share of the web runs on it, including WordPress, Laravel and Drupal sites.

```try php
<?php
echo "Hello, PHP\n";
echo 6 * 7, "\n";
```

- PHP code lives between `<?php` and `?>`; a file that is only PHP can leave out the closing `?>`.
- `echo` prints text. Every statement ends with `;`.
- `"\n"` is a new line. In a web page you would print HTML such as `<br>` instead.

:::info Running the examples
PHP examples run on a separate, secure server; if it is not enabled yet they run as soon as it is. On your computer: `php file.php`, or `php -S localhost:8000` to serve a folder.
:::

```quiz
? Where does PHP code run?
* On the server
- In the browser
- In the database

? A file that contains only PHP may leave out the closing ?> tag.
= true
```

# @lesson php-variables
title: Variables and types
summary: $variables, strings, numbers, booleans and null.
---
Every variable name starts with `$`. You do not declare a type: PHP works it out from the value.

```try php
<?php
$name = "Sara";
$age = 25;
$price = 19.99;
$active = true;
$nothing = null;

echo "Name: $name, age: $age\n";       // variables inside double quotes
echo 'No $name here' . "\n";             // single quotes: taken literally
echo "Next year: " . ($age + 1) . "\n";  // . joins strings
var_dump($price, $active, $nothing);
echo gettype($age), "\n";
```

```reference php
$x = 5 | Assign a variable | $count = 0;
"..." / '...' | Double quotes expand variables, single quotes do not | "Hi $name"
. | Join strings | "a" . "b"
var_dump() | Show type and value | var_dump($x);
gettype() | Name of the type | gettype(3.5)
const / define() | Constants | const TAX = 0.15;
```

:::tip Single or double quotes?
Use single quotes for fixed text and double quotes when you want variables inside. `"Total: {$order['total']}"` puts an array item inside a string with braces.
:::

```exercise php
? Join $first and $last with a space between them
$full = $first ___ " " . $last;
= .
```

```quiz
? Which character starts every variable name in PHP?
* $
- @
- #

? Which line prints Hi Sara when $name is "Sara"?
* echo "Hi $name";
- echo 'Hi $name';
- echo Hi + $name;
```

# @lesson php-operators
title: Operators and comparison
summary: Arithmetic, == versus ===, logic and the null coalescing operator.
---
```try php
<?php
echo 7 / 2, "\n";      // 3.5
echo intdiv(7, 2), "\n"; // 3
echo 7 % 2, "\n";      // 1
echo 2 ** 10, "\n";    // 1024

var_dump(5 == "5");    // true: values compared after conversion
var_dump(5 === "5");   // false: the types differ
var_dump(5 <=> 9);     // -1 (spaceship: -1, 0 or 1)

$user = null;
echo $user ?? "guest", "\n";  // the left value unless it is null
$count = 3;
$count += 2;
$count++;
echo $count, "\n";
```

```reference php
+ - * / % ** | Arithmetic | 2 ** 3
== / === | Loose and strict equality | $a === $b
!= / !== | Loose and strict difference | $a !== null
&& || ! | And, or, not | $a && !$b
<=> | Three-way comparison | $a <=> $b
?? | Null coalescing | $x ?? "default"
?: | Short ternary | $name ?: "anon"
```

:::warning Prefer ===
`==` converts types before comparing, which gives surprises such as `"abc" == 0` behaving differently between versions. `===` compares value and type, so it says exactly what you mean.
:::

```exercise php
? Use the strict equality operator
if ($status ___ "paid") { echo "ok"; }
= ===
```

```quiz
? What does 5 === "5" give?
* false
- true
- An error

? What does $x ?? "none" return when $x is null?
* none
- null
- An empty string
```

# @lesson php-conditions
title: Conditions
summary: if, elseif, else, switch and the ternary operator.
---
```try php
<?php
$score = 78;

if ($score >= 90) {
    echo "Excellent\n";
} elseif ($score >= 70) {
    echo "Good\n";
} else {
    echo "Keep practising\n";
}

$day = "fri";
switch ($day) {
    case "fri":
    case "sat":
        echo "Weekend\n";
        break;
    default:
        echo "Working day\n";
}

$age = 20;
echo $age >= 18 ? "Adult\n" : "Minor\n";
```

:::tip Do not forget break
In a `switch`, execution falls through to the next `case` until it meets `break`. Leaving cases empty on purpose, as with `fri` and `sat` above, lets them share code.
:::

```exercise php
? Complete the else-if keyword
if ($n > 0) { echo "positive"; } ___ ($n < 0) { echo "negative"; }
= elseif | else if
```

```quiz
? What happens in a switch when a case has no break?
* Execution continues into the next case
- PHP raises an error
- The switch stops

? The ternary operator has the form condition ? a : b.
= true
```

# @lesson php-loops
title: Loops
summary: for, while, do-while and foreach.
---
```try php
<?php
for ($i = 1; $i <= 3; $i++) {
    echo "Round $i\n";
}

$n = 3;
while ($n > 0) {
    echo $n, " ";
    $n--;
}
echo "go!\n";

$colors = ["red", "green", "blue"];
foreach ($colors as $color) {
    echo $color, "\n";
}
foreach ($colors as $index => $color) {
    echo "$index: $color\n";
}

for ($i = 1; $i <= 10; $i++) {
    if ($i % 2 == 0) continue;  // skip even numbers
    if ($i > 7) break;          // stop after 7
    echo $i, " ";
}
echo "\n";
```

```reference php
for | Counted loop | for ($i = 0; $i < 5; $i++)
while | Repeat while true | while ($n > 0)
do ... while | Runs at least once | do { } while ($x);
foreach | Each item of an array | foreach ($a as $k => $v)
break / continue | Leave the loop / skip a round | if ($x) break;
```

```exercise php
? Loop over $items and give each element the name $item
foreach ($items ___ $item) { echo $item; }
= as
```

```quiz
? Which loop runs its body at least once?
* do ... while
- while
- for
```

# @lesson php-arrays
title: Arrays
summary: Indexed arrays, associative arrays and the most useful functions.
---
A PHP array is both a list and a dictionary: keys can be numbers or strings.

```try php
<?php
$fruits = ["apple", "banana"];
$fruits[] = "cherry";             // append
echo count($fruits), " ", $fruits[0], "\n";

$user = ["name" => "Sara", "age" => 25];
$user["city"] = "Cairo";
foreach ($user as $key => $value) {
    echo "$key = $value\n";
}
echo isset($user["email"]) ? "has email\n" : "no email\n";

$nums = [5, 3, 8, 1];
sort($nums);
echo implode(", ", $nums), "\n";
echo array_sum($nums), " ", max($nums), "\n";
$squares = array_map(fn($n) => $n * $n, $nums);
$big = array_filter($nums, fn($n) => $n > 2);
print_r($squares);
print_r(array_values($big));
echo in_array(8, $nums) ? "found 8\n" : "no 8\n";
print_r(explode(",", "a,b,c"));
```

```reference php
count($a) | Number of items | count($list)
$a[] = x | Append | $list[] = 4;
isset($a[k]) | Does the key exist (and is not null)? | isset($u["id"])
sort / rsort / ksort | Sort by value / descending / by key | sort($nums);
array_map | New array from a function | array_map(fn($x) => $x * 2, $a)
array_filter | Keep matching items | array_filter($a, fn($x) => $x > 0)
implode / explode | Array to string / string to array | implode(", ", $a)
in_array / array_keys | Search values / list keys | in_array(3, $a)
```

:::tip print_r and var_dump
`print_r($array)` prints an array readably; `var_dump` also shows each type. Both are for debugging, not for the final page.
:::

```exercise php
? Add "kiwi" to the end of $fruits
$fruits___ = "kiwi";
= []
```

```quiz
? Which function joins array items into one string?
* implode
- explode
- concat

? An array can have string keys such as "name".
= true
```

# @lesson php-functions
title: Functions
summary: Parameters, default values, type declarations and arrow functions.
---
```try php
<?php
function greet(string $name, string $greeting = "Hello"): string {
    return "$greeting, $name!";
}
echo greet("Sara"), "\n";
echo greet("Omar", "Welcome"), "\n";

function total(float ...$prices): float {   // any number of arguments
    return array_sum($prices);
}
echo total(10, 20.5, 4), "\n";

$tax = 0.15;
$withTax = fn($price) => $price * (1 + $tax);   // arrow function sees $tax
echo $withTax(100), "\n";

$counter = function () use (&$tax) {            // classic closure: use()
    $tax = 0.2;
};
$counter();
echo $tax, "\n";
```

```reference php
function f($a) { } | Declare a function | function add($a, $b)
$a = 5 | Default parameter value | function f($n = 1)
int / string / ?int | Type declarations (?int also allows null) | function f(int $n): ?string
...$args | Any number of arguments | function sum(...$n)
fn($x) => expr | Arrow function | fn($x) => $x * 2
function () use ($v) | Closure that captures $v | function () use ($tax)
```

:::tip Strict types
Put `declare(strict_types=1);` on the first line of a file to make PHP refuse wrong types instead of converting them silently.
:::

```exercise php
? Write the keyword that declares a function
___ square($n) { return $n * $n; }
= function
```

```quiz
? What does function f($n = 1) mean?
* $n is 1 when the caller leaves it out
- $n must always be 1
- f returns 1

? An arrow function fn($x) => ... can read variables from the surrounding code without use().
= true
```

# @lesson php-strings
title: Working with strings
summary: Length, search, replace, case and formatting.
---
```try php
<?php
$text = "  Hello World  ";
$clean = trim($text);
echo strlen($clean), "\n";
echo strtoupper($clean), " / ", strtolower($clean), "\n";
echo str_replace("World", "PHP", $clean), "\n";
echo substr($clean, 0, 5), "\n";
var_dump(strpos($clean, "World"));   // 6, or false when not found
echo ucfirst("sara"), "\n";
printf("Price: %.2f, items: %d\n", 9.5, 3);
echo sprintf("%05d", 42), "\n";
echo str_repeat("-", 10), "\n";
echo count(preg_split("//u", "مرحبا", -1, PREG_SPLIT_NO_EMPTY)), " vs ", strlen("مرحبا"), "\n";   // characters, like mb_strlen (this runner's PHP has no mbstring extension)
```

```reference php
strlen / mb_strlen | Length in bytes / in characters | mb_strlen("مرحبا")
trim | Remove surrounding spaces | trim($s)
strtoupper / strtolower | Change case | strtoupper("a")
str_replace | Replace text | str_replace("a", "b", $s)
substr | Part of a string | substr($s, 0, 3)
strpos | Position of text, or false | strpos($s, "x") !== false
printf / sprintf | Formatted output / formatted string | sprintf("%.2f", $x)
```

:::warning Arabic text and mb_ functions
`strlen` counts bytes, and every Arabic letter is two bytes in UTF-8. Use the `mb_` functions (`mb_strlen`, `mb_substr`, `mb_strtoupper`) for text in any language beyond English.
:::

:::warning strpos can return 0
If the text is at the very start, `strpos` returns `0`, which is "falsy". Always test with `!== false`.
:::

```exercise php
? Remove the spaces around $input
$value = ___($input);
= trim
```

```quiz
? Which function counts the characters of an Arabic word correctly?
* mb_strlen
- strlen
- count
```

# @lesson php-forms
title: Forms, GET and POST
summary: Reading user input safely with $_GET and $_POST.
---
When a browser submits a form, PHP puts the values in the superglobal arrays `$_GET` (from the URL) and `$_POST` (from the request body).

```html
<form method="post" action="hello.php">
  <input name="name">
  <button>Send</button>
</form>
```

The example below fills `$_POST` by hand so it can run without a browser:

```try php
<?php
$_POST = ["name" => "<b>Sara</b>", "age" => "25x"];

$name = trim($_POST["name"] ?? "");
$age = filter_var($_POST["age"] ?? "", FILTER_VALIDATE_INT);

if ($name === "") {
    echo "Name is required\n";
} else {
    echo "Hello, " . htmlspecialchars($name) . "\n";
}
echo $age === false ? "Age must be a whole number\n" : "Age: $age\n";
```

```reference php
$_GET | Values from the URL query string | $_GET["page"] ?? 1
$_POST | Values from a submitted form | $_POST["email"]
$_SERVER["REQUEST_METHOD"] | GET or POST | if ($_SERVER["REQUEST_METHOD"] === "POST")
htmlspecialchars | Escape text before printing it in HTML | htmlspecialchars($name)
filter_var | Validate and convert a value | filter_var($e, FILTER_VALIDATE_EMAIL)
```

:::danger Never trust input
Everything in `$_GET` and `$_POST` comes from the user. Validate it, and pass it through `htmlspecialchars` before you print it, or an attacker can inject scripts into your page (XSS).
:::

```exercise php
? Escape $comment before printing it in a page
echo ___($comment);
= htmlspecialchars
```

```quiz
? Why do we call htmlspecialchars before printing user input?
* To stop injected HTML and scripts (XSS)
- To make the text bold
- To save it in the database

? Values in $_POST are always valid because the form checked them.
= false
> A user can send any request without your form, so the server must validate everything.
```

# @lesson php-oop
title: Classes and objects
summary: Properties, constructors, methods, visibility and inheritance.
---
```try php
<?php
class Account {
    public string $owner;
    private float $balance = 0;

    public function __construct(string $owner) {
        $this->owner = $owner;
    }

    public function deposit(float $amount): void {
        if ($amount <= 0) {
            throw new InvalidArgumentException("Amount must be positive");
        }
        $this->balance += $amount;
    }

    public function balance(): float {
        return $this->balance;
    }
}

class SavingsAccount extends Account {
    public function addInterest(float $rate): void {
        $this->deposit($this->balance() * $rate);
    }
}

$acc = new SavingsAccount("Sara");
$acc->deposit(1000);
$acc->addInterest(0.05);
echo $acc->owner, ": ", $acc->balance(), "\n";
```

- `$this` is the current object, and `->` reaches its properties and methods.
- `private` members are visible only inside the class; `public` members are visible everywhere; `protected` members are visible in the class and its children.
- `extends` makes a child class that inherits everything public and protected.

```reference php
class A { } | Declare a class | class User { }
new A() | Create an object | $u = new User("Sara");
__construct | Constructor, runs on new | public function __construct($n)
$this->x | Property of the current object | $this->name = $n;
public / protected / private | Visibility | private int $id;
extends | Inheritance | class Admin extends User
interface / implements | A contract of methods | class A implements Countable
static / self:: | Belongs to the class, not to an object | self::$count++
```

:::tip PHP 8 shortcuts
Newer PHP versions shorten this code: constructor promotion (`public function __construct(public string $owner) {}`), `readonly` properties and `enum`. The runner here uses PHP 7.4, so the examples use the longer form that works everywhere.
:::

```exercise php
? Call the deposit method on the $acc object
$acc___deposit(50);
= ->
```

```quiz
? Who can read a private property?
* Only code inside the same class
- Any code
- Only child classes

? A child class is declared with the keyword extends.
= true
```

# @lesson php-errors
title: Errors and exceptions
summary: throw, try, catch, finally and your own exception classes.
---
```try php
<?php
class OutOfStock extends Exception {}

function buy(int $stock, int $qty): int {
    if ($qty <= 0) {
        throw new InvalidArgumentException("Quantity must be positive");
    }
    if ($qty > $stock) {
        throw new OutOfStock("Only $stock left");
    }
    return $stock - $qty;
}

foreach ([2, 10, 0] as $qty) {
    try {
        $left = buy(5, $qty);
        echo "Left: $left\n";
    } catch (OutOfStock $e) {
        echo "Sorry: ", $e->getMessage(), "\n";
    } catch (InvalidArgumentException $e) {
        echo "Bad input: ", $e->getMessage(), "\n";
    } finally {
        echo "-- checked $qty\n";
    }
}

try {
    echo intdiv(1, 0);
} catch (DivisionByZeroError $e) {
    echo "Error: ", $e->getMessage(), "\n";
}
```

- `throw` stops the function and sends the exception up until a `catch` handles it.
- `finally` runs whether or not an exception happened.
- Since PHP 7, many engine errors are `Error` objects (such as `DivisionByZeroError` and `TypeError`), and `catch (Throwable $e)` catches both kinds.

:::warning Do not show raw errors to visitors
On a live site, turn `display_errors` off and log errors instead; error messages can reveal file paths and database details.
:::

```exercise php
? Complete the keyword that raises an exception
___ new Exception("Failed");
= throw
```

```quiz
? When does a finally block run?
* Always, with or without an exception
- Only after an exception
- Only when there is no exception
```

# @lesson php-files-json
title: Files and JSON
summary: Reading and writing files, and converting between arrays and JSON.
---
```try php
<?php
$path = sys_get_temp_dir() . "/notes.txt";
file_put_contents($path, "first line\n");
file_put_contents($path, "second line\n", FILE_APPEND);
echo file_get_contents($path);
foreach (file($path, FILE_IGNORE_NEW_LINES) as $n => $line) {
    echo $n + 1, ": $line\n";
}
echo file_exists($path) ? "exists\n" : "missing\n";
unlink($path);

$order = ["id" => 7, "items" => ["tea", "cake"], "paid" => true];
$json = json_encode($order);
echo $json, "\n";
$back = json_decode($json, true);       // true: give arrays, not objects
echo $back["items"][1], "\n";
echo json_encode(["name" => "سارة"], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT), "\n";
```

```reference php
file_get_contents | Read a whole file (or URL) | file_get_contents("a.txt")
file_put_contents | Write a file | file_put_contents($p, $text, FILE_APPEND)
file | Lines of a file as an array | file($p, FILE_IGNORE_NEW_LINES)
file_exists / unlink | Check / delete a file | unlink($p)
json_encode | Array to JSON text | json_encode($data)
json_decode | JSON text to array | json_decode($json, true)
```

:::tip Arabic in JSON
By default `json_encode` writes Arabic as `س...`. Add `JSON_UNESCAPED_UNICODE` to keep it readable.
:::

```exercise php
? Turn the JSON text $json into an associative array
$data = json_decode($json, ___);
= true
```

```quiz
? Which function turns a PHP array into JSON text?
* json_encode
- json_decode
- serialize
```

# @lesson php-database
title: Databases with PDO
summary: Connecting to a database and running safe, prepared queries.
---
**PDO** is PHP's standard way to talk to databases (MySQL, MariaDB, PostgreSQL, SQLite). The example uses SQLite in memory so it needs no server; it runs if the runner's PHP includes the SQLite driver.

```try php
<?php
$db = new PDO("sqlite::memory:");
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$db->exec("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)");

$insert = $db->prepare("INSERT INTO products (name, price) VALUES (:name, :price)");
foreach ([["Tea", 12.5], ["Coffee", 20], ["Cake", 35]] as [$name, $price]) {
    $insert->execute([":name" => $name, ":price" => $price]);
}

$max = 25;   // imagine this came from $_GET
$query = $db->prepare("SELECT name, price FROM products WHERE price < ? ORDER BY price");
$query->execute([$max]);
foreach ($query->fetchAll(PDO::FETCH_ASSOC) as $row) {
    echo $row["name"], ": ", $row["price"], "\n";
}
echo "Count: ", $db->query("SELECT COUNT(*) FROM products")->fetchColumn(), "\n";
```

For MySQL the connection line becomes:

```text
$db = new PDO("mysql:host=localhost;dbname=shop;charset=utf8mb4", $user, $password);
```

```reference php
new PDO(dsn, user, pass) | Connect | new PDO("sqlite::memory:")
prepare | Prepare a query with placeholders | $db->prepare("... WHERE id = ?")
execute | Run it with values | $stmt->execute([$id])
fetch / fetchAll | One row / all rows | $stmt->fetchAll(PDO::FETCH_ASSOC)
fetchColumn | First column of the next row | $stmt->fetchColumn()
lastInsertId | ID of the inserted row | $db->lastInsertId()
```

:::danger SQL injection
Never glue user input into SQL, as in `"... WHERE name = '$name'"`. Use placeholders (`?` or `:name`) with `prepare` and `execute`; the database then treats the input as data, never as SQL.
:::

```exercise php
? Run the prepared statement with the value $id
$stmt->___([$id]);
= execute
```

```quiz
? What protects a query from SQL injection?
* Prepared statements with placeholders
- Putting the input in double quotes
- Using SELECT * instead

? PDO can work with several database systems.
= true
```

# @lesson php-reference
title: PHP quick reference
summary: The most used syntax and functions on one page.
---
```reference php
echo / print | Print text | echo "Hi";
$x = 1 | Variable | $name = "Sara";
. / .= | Join / append to a string | $s .= "!";
=== / !== | Strict comparison | $a === $b
?? | Default when null | $_GET["p"] ?? 1
if / elseif / else | Conditions | if ($x) { } elseif ($y) { }
foreach ($a as $k => $v) | Loop over an array | foreach ($u as $k => $v)
function f(int $x): int | Typed function | function sq(int $x): int
fn($x) => ... | Arrow function | array_map(fn($x) => $x * 2, $a)
count / in_array / array_map | Common array functions | count($a)
trim / str_replace / mb_strlen | Common string functions | trim($s)
class / new / -> | Objects | $u->name
try / catch / finally | Exceptions | catch (Exception $e)
json_encode / json_decode | JSON | json_decode($j, true)
htmlspecialchars | Escape output | htmlspecialchars($s)
PDO prepare / execute | Safe database queries | $st->execute([$id])
```

:::tip Where to go next
Build a small project: a guest book that saves messages in SQLite with PDO, validates the form, and escapes every message before printing it. Then look at a framework such as Laravel or Symfony.
:::

```quiz
? Which pair keeps a PHP page safe from XSS and SQL injection?
* htmlspecialchars for output and prepared statements for queries
- echo and var_dump
- json_encode and json_decode
```
