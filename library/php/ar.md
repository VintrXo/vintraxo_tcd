# @lesson php-intro
title: مقدمة PHP
summary: ما هي PHP وأين تعمل، وأول برنامج لك.
---
**PHP** لغة تعمل على الخادم: تُنفَّذ على خادم الويب، وتبني الصفحة، ثم ترسل للمتصفح HTML عاديًا. جزء كبير من الويب يعمل بها، ومنها مواقع WordPress و Laravel و Drupal.

```try php
<?php
echo "Hello, PHP\n";
echo 6 * 7, "\n";
```

- يُكتب كود PHP بين `<?php` و `?>`، والملف الذي يحوي PHP فقط يمكنه حذف `?>` في آخره.
- `echo` تطبع نصًا، وكل جملة تنتهي بـ `;`.
- `"\n"` سطر جديد. في صفحة ويب ستطبع HTML مثل `<br>` بدلًا منه.

:::info تشغيل الأمثلة
أمثلة PHP تعمل على خادم تشغيل منفصل وآمن؛ إن لم يكن مفعّلًا بعد فستعمل فور تفعيله. وعلى جهازك: `php file.php`، أو `php -S localhost:8000` لتشغيل مجلد كموقع.
:::

```quiz
? أين يُنفَّذ كود PHP؟
* على الخادم
- في المتصفح
- في قاعدة البيانات

? يمكن للملف الذي يحوي PHP فقط أن يحذف وسم الإغلاق ?> في آخره.
= true
```

# @lesson php-variables
title: المتغيرات والأنواع
summary: المتغيرات بعلامة $، والنصوص والأرقام والقيم المنطقية و null.
---
كل اسم متغير يبدأ بـ `$`، ولا تكتب النوع: PHP تستنتجه من القيمة.

```try php
<?php
$name = "Sara";
$age = 25;
$price = 19.99;
$active = true;
$nothing = null;

echo "Name: $name, age: $age\n";       // متغيرات داخل علامات التنصيص المزدوجة
echo 'No $name here' . "\n";             // المفردة: تؤخذ حرفيًا
echo "Next year: " . ($age + 1) . "\n";  // النقطة تدمج النصوص
var_dump($price, $active, $nothing);
echo gettype($age), "\n";
```

```reference php
$x = 5 | إسناد قيمة لمتغير | $count = 0;
"..." / '...' | المزدوجة تعوّض المتغيرات والمفردة لا | "Hi $name"
. | دمج النصوص | "a" . "b"
var_dump() | عرض النوع والقيمة | var_dump($x);
gettype() | اسم النوع | gettype(3.5)
const / define() | الثوابت | const TAX = 0.15;
```

:::tip مفردة أم مزدوجة؟
استخدم المفردة للنص الثابت، والمزدوجة حين تريد متغيرات داخله. `"Total: {$order['total']}"` تضع عنصر مصفوفة داخل النص بالأقواس المعقوفة.
:::

```exercise php
? ادمج $first و $last بينهما مسافة
$full = $first ___ " " . $last;
= .
```

```quiz
? بأي رمز يبدأ كل اسم متغير في PHP؟
* $
- @
- #

? أي سطر يطبع Hi Sara إذا كانت قيمة $name هي "Sara"؟
* echo "Hi $name";
- echo 'Hi $name';
- echo Hi + $name;
```

# @lesson php-operators
title: العمليات والمقارنة
summary: الحساب، والفرق بين == و ===، والمنطق، وعامل ?? .
---
```try php
<?php
echo 7 / 2, "\n";      // 3.5
echo intdiv(7, 2), "\n"; // 3
echo 7 % 2, "\n";      // 1
echo 2 ** 10, "\n";    // 1024

var_dump(5 == "5");    // true: تُقارن القيم بعد التحويل
var_dump(5 === "5");   // false: النوعان مختلفان
var_dump(5 <=> 9);     // -1 (المقارنة الثلاثية: -1 أو 0 أو 1)

$user = null;
echo $user ?? "guest", "\n";  // القيمة اليسرى ما لم تكن null
$count = 3;
$count += 2;
$count++;
echo $count, "\n";
```

```reference php
+ - * / % ** | الحساب | 2 ** 3
== / === | تساوٍ مرن وتساوٍ صارم | $a === $b
!= / !== | اختلاف مرن واختلاف صارم | $a !== null
&& || ! | و، أو، ليس | $a && !$b
<=> | مقارنة ثلاثية | $a <=> $b
?? | قيمة بديلة عند null | $x ?? "default"
?: | شرط ثلاثي مختصر | $name ?: "anon"
```

:::warning فضّل ===
`==` تحوّل الأنواع قبل المقارنة فتعطي مفاجآت، مثل `"abc" == 0` التي تغيّرت نتيجتها بين الإصدارات. أما `===` فتقارن القيمة والنوع معًا، فتقول بالضبط ما تقصده.
:::

```exercise php
? استخدم عامل التساوي الصارم
if ($status ___ "paid") { echo "ok"; }
= ===
```

```quiz
? ما نتيجة 5 === "5"؟
* false
- true
- خطأ

? ماذا يرجع $x ?? "none" إذا كانت $x تساوي null؟
* none
- null
- نصًا فارغًا
```

# @lesson php-conditions
title: الشروط
summary: if و elseif و else و switch والشرط الثلاثي.
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

:::tip لا تنسَ break
في `switch` يستمر التنفيذ إلى الحالة التالية حتى يقابل `break`. ترك الحالات فارغة عن قصد، مثل `fri` و `sat` في المثال، يجعلها تشترك في نفس الكود.
:::

```exercise php
? أكمل كلمة "وإلا إذا"
if ($n > 0) { echo "positive"; } ___ ($n < 0) { echo "negative"; }
= elseif | else if
```

```quiz
? ماذا يحدث في switch إذا لم تحتوِ الحالة على break؟
* يستمر التنفيذ في الحالة التالية
- تظهر رسالة خطأ
- يتوقف switch

? صيغة الشرط الثلاثي هي condition ? a : b.
= true
```

# @lesson php-loops
title: الحلقات
summary: for و while و do-while و foreach.
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
    if ($i % 2 == 0) continue;  // تخطَّ الأعداد الزوجية
    if ($i > 7) break;          // توقف بعد 7
    echo $i, " ";
}
echo "\n";
```

```reference php
for | حلقة بعدد محدد | for ($i = 0; $i < 5; $i++)
while | كرر ما دام الشرط صحيحًا | while ($n > 0)
do ... while | تعمل مرة واحدة على الأقل | do { } while ($x);
foreach | كل عنصر في مصفوفة | foreach ($a as $k => $v)
break / continue | اخرج من الحلقة / تخطَّ الدورة | if ($x) break;
```

```exercise php
? مرّ على $items وسمِّ كل عنصر $item
foreach ($items ___ $item) { echo $item; }
= as
```

```quiz
? أي حلقة تنفّذ جسمها مرة واحدة على الأقل؟
* do ... while
- while
- for
```

# @lesson php-arrays
title: المصفوفات
summary: المصفوفات المرقّمة والترابطية وأهم دوالها.
---
المصفوفة في PHP قائمة وقاموس في نفس الوقت: المفاتيح يمكن أن تكون أرقامًا أو نصوصًا.

```try php
<?php
$fruits = ["apple", "banana"];
$fruits[] = "cherry";             // إضافة في النهاية
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
count($a) | عدد العناصر | count($list)
$a[] = x | إضافة في النهاية | $list[] = 4;
isset($a[k]) | هل المفتاح موجود (وقيمته ليست null)؟ | isset($u["id"])
sort / rsort / ksort | ترتيب بالقيمة / تنازليًا / بالمفتاح | sort($nums);
array_map | مصفوفة جديدة من دالة | array_map(fn($x) => $x * 2, $a)
array_filter | الإبقاء على العناصر المطابقة | array_filter($a, fn($x) => $x > 0)
implode / explode | مصفوفة إلى نص / نص إلى مصفوفة | implode(", ", $a)
in_array / array_keys | بحث في القيم / قائمة المفاتيح | in_array(3, $a)
```

:::tip print_r و var_dump
`print_r($array)` تطبع المصفوفة بشكل مقروء، و `var_dump` تعرض النوع أيضًا. كلتاهما لتتبع الأخطاء وليستا للصفحة النهائية.
:::

```exercise php
? أضف "kiwi" إلى نهاية $fruits
$fruits___ = "kiwi";
= []
```

```quiz
? أي دالة تدمج عناصر المصفوفة في نص واحد؟
* implode
- explode
- concat

? يمكن أن تكون مفاتيح المصفوفة نصوصًا مثل "name".
= true
```

# @lesson php-functions
title: الدوال
summary: المعاملات والقيم الافتراضية وتحديد الأنواع والدوال السهمية.
---
```try php
<?php
function greet(string $name, string $greeting = "Hello"): string {
    return "$greeting, $name!";
}
echo greet("Sara"), "\n";
echo greet("Omar", "Welcome"), "\n";

function total(float ...$prices): float {   // أي عدد من المعاملات
    return array_sum($prices);
}
echo total(10, 20.5, 4), "\n";

$tax = 0.15;
$withTax = fn($price) => $price * (1 + $tax);   // الدالة السهمية ترى $tax
echo $withTax(100), "\n";

$counter = function () use (&$tax) {            // الإغلاق التقليدي: use()
    $tax = 0.2;
};
$counter();
echo $tax, "\n";
```

```reference php
function f($a) { } | تعريف دالة | function add($a, $b)
$a = 5 | قيمة افتراضية للمعامل | function f($n = 1)
int / string / ?int | تحديد الأنواع (?int تقبل null أيضًا) | function f(int $n): ?string
...$args | أي عدد من المعاملات | function sum(...$n)
fn($x) => expr | دالة سهمية | fn($x) => $x * 2
function () use ($v) | إغلاق يلتقط $v | function () use ($tax)
```

:::tip الأنواع الصارمة
ضع `declare(strict_types=1);` في أول سطر من الملف لتجعل PHP ترفض الأنواع الخاطئة بدلًا من تحويلها بصمت.
:::

```exercise php
? اكتب الكلمة التي تعرّف دالة
___ square($n) { return $n * $n; }
= function
```

```quiz
? ماذا تعني function f($n = 1)؟
* تكون $n تساوي 1 إذا لم يرسلها المستدعي
- يجب أن تكون $n دائمًا 1
- الدالة f ترجع 1

? الدالة السهمية fn($x) => ... تقرأ متغيرات الكود المحيط بدون use().
= true
```

# @lesson php-strings
title: التعامل مع النصوص
summary: الطول والبحث والاستبدال وحالة الأحرف والتنسيق.
---
```try php
<?php
$text = "  Hello World  ";
$clean = trim($text);
echo strlen($clean), "\n";
echo strtoupper($clean), " / ", strtolower($clean), "\n";
echo str_replace("World", "PHP", $clean), "\n";
echo substr($clean, 0, 5), "\n";
var_dump(strpos($clean, "World"));   // 6، أو false إن لم يوجد
echo ucfirst("sara"), "\n";
printf("Price: %.2f, items: %d\n", 9.5, 3);
echo sprintf("%05d", 42), "\n";
echo str_repeat("-", 10), "\n";
echo mb_strlen("مرحبا"), " vs ", strlen("مرحبا"), "\n";
```

```reference php
strlen / mb_strlen | الطول بالبايت / بالحروف | mb_strlen("مرحبا")
trim | حذف المسافات من الطرفين | trim($s)
strtoupper / strtolower | تغيير حالة الأحرف | strtoupper("a")
str_replace | استبدال نص | str_replace("a", "b", $s)
substr | جزء من النص | substr($s, 0, 3)
strpos | موضع نص، أو false | strpos($s, "x") !== false
printf / sprintf | طباعة منسقة / نص منسق | sprintf("%.2f", $x)
```

:::warning النص العربي ودوال mb_
`strlen` تعدّ البايتات، وكل حرف عربي بايتان في UTF-8. استخدم دوال `mb_` (`mb_strlen` و `mb_substr` و `mb_strtoupper`) مع أي لغة غير الإنجليزية.
:::

:::warning قد ترجع strpos صفرًا
إذا كان النص في البداية تمامًا ترجع `strpos` القيمة `0`، وهي تُعامل كـ "خطأ" في الشروط. اختبر دائمًا بـ `!== false`.
:::

```exercise php
? احذف المسافات حول $input
$value = ___($input);
= trim
```

```quiz
? أي دالة تعدّ حروف كلمة عربية بشكل صحيح؟
* mb_strlen
- strlen
- count
```

# @lesson php-forms
title: النماذج و GET و POST
summary: قراءة مدخلات المستخدم بأمان من $_GET و $_POST.
---
حين يرسل المتصفح نموذجًا، تضع PHP القيم في المصفوفتين العامتين `$_GET` (من الرابط) و `$_POST` (من جسم الطلب).

```html
<form method="post" action="hello.php">
  <input name="name">
  <button>Send</button>
</form>
```

المثال التالي يملأ `$_POST` يدويًا ليعمل بدون متصفح:

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
$_GET | قيم من الرابط | $_GET["page"] ?? 1
$_POST | قيم من نموذج مُرسل | $_POST["email"]
$_SERVER["REQUEST_METHOD"] | GET أو POST | if ($_SERVER["REQUEST_METHOD"] === "POST")
htmlspecialchars | تأمين النص قبل طباعته في HTML | htmlspecialchars($name)
filter_var | التحقق من قيمة وتحويلها | filter_var($e, FILTER_VALIDATE_EMAIL)
```

:::danger لا تثق في المدخلات أبدًا
كل ما في `$_GET` و `$_POST` يأتي من المستخدم. تحقّق منه، ومرّره على `htmlspecialchars` قبل طباعته، وإلا استطاع مهاجم حقن سكربتات في صفحتك (XSS).
:::

```exercise php
? أمّن $comment قبل طباعته في الصفحة
echo ___($comment);
= htmlspecialchars
```

```quiz
? لماذا نستدعي htmlspecialchars قبل طباعة مدخلات المستخدم؟
* لمنع حقن HTML والسكربتات (XSS)
- لجعل النص عريضًا
- لحفظه في قاعدة البيانات

? قيم $_POST صحيحة دائمًا لأن النموذج تحقّق منها.
= false
> يستطيع المستخدم إرسال أي طلب بدون نموذجك، لذلك يجب أن يتحقق الخادم من كل شيء.
```

# @lesson php-oop
title: الأصناف والكائنات
summary: الخصائص والمُنشئ والدوال ومستوى الوصول والوراثة.
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

- `$this` هو الكائن الحالي، و `->` توصلك لخصائصه ودواله.
- أعضاء `private` تُرى داخل الصنف فقط، و `public` تُرى من أي مكان، و `protected` تُرى في الصنف وأبنائه.
- `extends` تنشئ صنفًا ابنًا يرث كل ما هو public و protected.

```reference php
class A { } | تعريف صنف | class User { }
new A() | إنشاء كائن | $u = new User("Sara");
__construct | المُنشئ، يعمل مع new | public function __construct($n)
$this->x | خاصية الكائن الحالي | $this->name = $n;
public / protected / private | مستوى الوصول | private int $id;
extends | الوراثة | class Admin extends User
interface / implements | عقد من الدوال | class A implements Countable
static / self:: | تخص الصنف لا الكائن | self::$count++
```

:::tip اختصارات PHP 8
الإصدارات الأحدث تختصر هذا الكود: ترقية المُنشئ (`public function __construct(public string $owner) {}`) والخصائص `readonly` و `enum`. خادم التشغيل هنا يستخدم PHP 7.4، لذلك تستخدم الأمثلة الصيغة الأطول التي تعمل في كل مكان.
:::

```exercise php
? استدعِ الدالة deposit على الكائن $acc
$acc___deposit(50);
= ->
```

```quiz
? من يستطيع قراءة خاصية private؟
* الكود داخل نفس الصنف فقط
- أي كود
- الأصناف الأبناء فقط

? يُعرَّف الصنف الابن بالكلمة extends.
= true
```

# @lesson php-errors
title: الأخطاء والاستثناءات
summary: throw و try و catch و finally واستثناءاتك الخاصة.
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
        echo "Left: ", buy(5, $qty), "\n";
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

- `throw` توقف الدالة وترسل الاستثناء لأعلى حتى يعالجه `catch`.
- `finally` تعمل سواء حدث استثناء أم لا.
- منذ PHP 7 صارت أخطاء كثيرة كائنات `Error` (مثل `DivisionByZeroError` و `TypeError`)، و `catch (Throwable $e)` تلتقط النوعين.

:::warning لا تعرض الأخطاء الخام للزوار
على الموقع الحقيقي أوقف `display_errors` وسجّل الأخطاء في ملف؛ فرسائل الخطأ قد تكشف مسارات الملفات وتفاصيل قاعدة البيانات.
:::

```exercise php
? أكمل الكلمة التي ترمي استثناءً
___ new Exception("Failed");
= throw
```

```quiz
? متى يعمل جزء finally؟
* دائمًا، مع الاستثناء أو بدونه
- بعد الاستثناء فقط
- عند عدم وجود استثناء فقط
```

# @lesson php-files-json
title: الملفات و JSON
summary: قراءة الملفات وكتابتها، والتحويل بين المصفوفات و JSON.
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
$back = json_decode($json, true);       // true: أعطني مصفوفات لا كائنات
echo $back["items"][1], "\n";
echo json_encode(["name" => "سارة"], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT), "\n";
```

```reference php
file_get_contents | قراءة ملف كامل (أو رابط) | file_get_contents("a.txt")
file_put_contents | كتابة ملف | file_put_contents($p, $text, FILE_APPEND)
file | أسطر الملف كمصفوفة | file($p, FILE_IGNORE_NEW_LINES)
file_exists / unlink | فحص ملف / حذفه | unlink($p)
json_encode | مصفوفة إلى نص JSON | json_encode($data)
json_decode | نص JSON إلى مصفوفة | json_decode($json, true)
```

:::tip العربية داخل JSON
افتراضيًا تكتب `json_encode` العربية بصيغة `س...`. أضف `JSON_UNESCAPED_UNICODE` لتبقى مقروءة.
:::

```exercise php
? حوّل نص JSON في $json إلى مصفوفة ترابطية
$data = json_decode($json, ___);
= true
```

```quiz
? أي دالة تحوّل مصفوفة PHP إلى نص JSON؟
* json_encode
- json_decode
- serialize
```

# @lesson php-database
title: قواعد البيانات مع PDO
summary: الاتصال بقاعدة بيانات وتنفيذ استعلامات مُجهّزة آمنة.
---
**PDO** هي الطريقة القياسية في PHP للتعامل مع قواعد البيانات (MySQL و MariaDB و PostgreSQL و SQLite). المثال يستخدم SQLite في الذاكرة فلا يحتاج خادمًا؛ ويعمل إذا كانت PHP في خادم التشغيل تتضمن مشغّل SQLite.

```try php
<?php
$db = new PDO("sqlite::memory:");
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$db->exec("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)");

$insert = $db->prepare("INSERT INTO products (name, price) VALUES (:name, :price)");
foreach ([["Tea", 12.5], ["Coffee", 20], ["Cake", 35]] as [$name, $price]) {
    $insert->execute([":name" => $name, ":price" => $price]);
}

$max = 25;   // تخيّل أنها جاءت من $_GET
$query = $db->prepare("SELECT name, price FROM products WHERE price < ? ORDER BY price");
$query->execute([$max]);
foreach ($query->fetchAll(PDO::FETCH_ASSOC) as $row) {
    echo $row["name"], ": ", $row["price"], "\n";
}
echo "Count: ", $db->query("SELECT COUNT(*) FROM products")->fetchColumn(), "\n";
```

مع MySQL يصبح سطر الاتصال:

```text
$db = new PDO("mysql:host=localhost;dbname=shop;charset=utf8mb4", $user, $password);
```

```reference php
new PDO(dsn, user, pass) | الاتصال | new PDO("sqlite::memory:")
prepare | تجهيز استعلام بعلامات أماكن | $db->prepare("... WHERE id = ?")
execute | تنفيذه بالقيم | $stmt->execute([$id])
fetch / fetchAll | صف واحد / كل الصفوف | $stmt->fetchAll(PDO::FETCH_ASSOC)
fetchColumn | أول عمود من الصف التالي | $stmt->fetchColumn()
lastInsertId | رقم الصف المضاف | $db->lastInsertId()
```

:::danger حقن SQL
لا تلصق مدخلات المستخدم داخل SQL أبدًا، مثل `"... WHERE name = '$name'"`. استخدم علامات الأماكن (`?` أو `:name`) مع `prepare` و `execute`؛ فتعامل قاعدة البيانات المدخلات كبيانات وليس كأوامر SQL.
:::

```exercise php
? نفّذ الاستعلام المُجهّز بالقيمة $id
$stmt->___([$id]);
= execute
```

```quiz
? ما الذي يحمي الاستعلام من حقن SQL؟
* الاستعلامات المُجهّزة بعلامات أماكن
- وضع المدخلات بين علامتي تنصيص مزدوجتين
- استخدام SELECT * بدلًا منها

? تستطيع PDO العمل مع أكثر من نوع من قواعد البيانات.
= true
```

# @lesson php-reference
title: مرجع PHP السريع
summary: أكثر الصيغ والدوال استخدامًا في صفحة واحدة.
---
```reference php
echo / print | طباعة نص | echo "Hi";
$x = 1 | متغير | $name = "Sara";
. / .= | دمج / إلحاق بنص | $s .= "!";
=== / !== | مقارنة صارمة | $a === $b
?? | قيمة بديلة عند null | $_GET["p"] ?? 1
if / elseif / else | الشروط | if ($x) { } elseif ($y) { }
foreach ($a as $k => $v) | المرور على مصفوفة | foreach ($u as $k => $v)
function f(int $x): int | دالة بأنواع محددة | function sq(int $x): int
fn($x) => ... | دالة سهمية | array_map(fn($x) => $x * 2, $a)
count / in_array / array_map | دوال مصفوفات شائعة | count($a)
trim / str_replace / mb_strlen | دوال نصوص شائعة | trim($s)
class / new / -> | الكائنات | $u->name
try / catch / finally | الاستثناءات | catch (Exception $e)
json_encode / json_decode | JSON | json_decode($j, true)
htmlspecialchars | تأمين المخرجات | htmlspecialchars($s)
PDO prepare / execute | استعلامات آمنة | $st->execute([$id])
```

:::tip الخطوة التالية
ابنِ مشروعًا صغيرًا: سجل زوار يحفظ الرسائل في SQLite عبر PDO، ويتحقق من النموذج، ويؤمّن كل رسالة قبل طباعتها. بعدها تعرّف على إطار عمل مثل Laravel أو Symfony.
:::

```quiz
? أي ثنائي يحمي صفحة PHP من XSS وحقن SQL؟
* htmlspecialchars للمخرجات والاستعلامات المُجهّزة لقاعدة البيانات
- echo و var_dump
- json_encode و json_decode
```
