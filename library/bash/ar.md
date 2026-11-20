# @lesson bash-intro
title: مقدمة Bash
summary: ما هي الطرفية (shell)، وما هي Bash، وأول أوامرك.
---
**الـ shell** هو البرنامج الذي يقرأ الأوامر التي تكتبها في الطرفية وينفّذها. و **Bash** أشهر shell على خوادم Linux، وهي أيضًا لغة سكربتات: ملف أوامر يمكنك تشغيله مرة بعد مرة.

```try bash
echo "Hello, Bash"
echo "Today is $(date +%A)"
whoami
pwd
```

- `echo` تطبع نصًا.
- `$(command)` تنفّذ أمرًا وتضع ناتجه مكانها.
- `whoami` تعرض المستخدم الحالي، و `pwd` تعرض المجلد الحالي.

:::info تشغيل الأمثلة
أمثلة Bash تعمل في بيئة تشغيل منفصلة وآمنة؛ إن لم تكن مفعّلة بعد فستعمل فور تفعيلها. وعلى جهازك: افتح الطرفية في Linux أو macOS، أو استخدم WSL أو Git Bash على Windows.
:::

```quiz
? ما هو الـ shell؟
* برنامج يقرأ أوامرك وينفّذها
- محرر نصوص
- متصفح ويب

? سكربت Bash ملف أوامر يمكن تشغيله مرات كثيرة.
= true
```

# @lesson bash-files
title: الملفات والمجلدات
summary: ls و cd و mkdir و touch و cp و mv و rm والمسارات.
---
```try bash
cd "$(mktemp -d)"            # اعمل داخل مجلد مؤقت فارغ
mkdir -p project/src
touch project/README.md project/src/app.sh
ls -l project
cp project/README.md project/NOTES.md
mv project/NOTES.md project/notes.txt
ls project
cd project
pwd
cd ..
rm -r project
ls
```

```reference bash
ls / ls -la | عرض الملفات / بالتفاصيل والملفات المخفية | ls -la /etc
cd dir / cd .. / cd ~ | تغيير المجلد / للأعلى / المجلد الرئيسي | cd ~/projects
pwd | المجلد الحالي | pwd
mkdir -p a/b | إنشاء مجلدات (مع الآباء) | mkdir -p logs/2026
touch f | إنشاء ملف فارغ | touch notes.txt
cp / cp -r | نسخ ملف / مجلد | cp -r src backup
mv | نقل أو إعادة تسمية | mv old.txt new.txt
rm / rm -r | حذف ملف / مجلد | rm -r build
```

:::danger لا توجد سلة محذوفات مع rm
`rm` تحذف فورًا وبلا رجعة. راجع المسارات جيدًا، خاصة مع `-r` والأنماط مثل `*`، ولا تشغّل `rm -rf` أبدًا على مسار مبني من متغير قد يكون فارغًا.
:::

```exercise bash
? أنشئ المجلدين logs/2026 بأمر واحد، بما فيهما logs
mkdir ___ logs/2026
= -p
```

```quiz
? أي أمر يعيد تسمية ملف؟
* mv
- cp
- rn

? المسار الذي يبدأ بـ / مسار مطلق.
= true
```

# @lesson bash-variables
title: المتغيرات وعلامات التنصيص
summary: إسناد المتغيرات و $VAR وعلامات التنصيص وإحلال الأوامر.
---
```try bash
name="Sara"                  # بدون مسافات حول =
age=25
echo "Name: $name, age: $age"
echo 'Single quotes: $name stays as text'
echo "Braces: ${name}_backup"

files=$(ls / | wc -l)
echo "The root folder has $files entries"

greeting="hello world"
echo "${#greeting} characters"
echo "${greeting^^}"         # أحرف كبيرة
echo "${greeting/world/Bash}"

readonly PI=3.14
echo "$PI"
echo "Home folder: $HOME, shell: $SHELL"
```

```reference bash
x=value | إسناد (بدون مسافات) | city="Cairo"
$x / ${x} | قراءة متغير | echo "${city}s"
"..." / '...' | المزدوجة تعوّض $ والمفردة لا | echo "$x" '$x'
$(cmd) | ناتج أمر كقيمة | now=$(date)
${#x} | الطول | echo ${#name}
${x^^} / ${x,,} | أحرف كبيرة / صغيرة | echo ${name^^}
${x/a/b} | استبدال أول تطابق | echo ${path/home/root}
${x:-default} | القيمة أو قيمة افتراضية إن كانت فارغة | echo ${PORT:-8000}
export X | إظهاره للبرامج التي تشغّلها | export PATH="$PATH:~/bin"
```

:::warning ضع المتغيرات دائمًا بين علامتي تنصيص
اكتب `"$file"` لا `$file`. بدون علامات التنصيص تُقسَّم القيمة التي فيها مسافات إلى عدة كلمات، وتختفي القيمة الفارغة، فتتعطل الأوامر بطرق مفاجئة.
:::

```exercise bash
? خزّن ناتج الأمر date في now
now=___(date)
= $
```

```quiz
? أي سطر يُسند متغيرًا بشكل صحيح؟
* city="Cairo"
- city = "Cairo"
- $city="Cairo"

? المتغيرات داخل علامات التنصيص المفردة تُعوَّض بقيمها.
= false
> علامات التنصيص المزدوجة فقط تعوّض $المتغيرات؛ والمفردة تُبقي النص كما هو تمامًا.
```

# @lesson bash-pipes
title: الأنابيب وإعادة التوجيه
summary: > و >> و < و | والتدفقات القياسية.
---
لكل أمر ثلاثة تدفقات: **stdin** (المدخلات) و **stdout** (المخرجات) و **stderr** (الأخطاء). يمكنك إرسالها إلى ملفات أو إلى أوامر أخرى.

```try bash
cd "$(mktemp -d)"
echo "first" > log.txt         # كتابة (تستبدل الملف)
echo "second" >> log.txt       # إلحاق
cat log.txt
wc -l < log.txt                # قراءة المدخلات من ملف

printf "banana\napple\ncherry\napple\n" > fruits.txt
sort fruits.txt | uniq          # ترسل | المخرجات إلى الأمر التالي
sort fruits.txt | uniq -c | sort -rn | head -1

ls missing-file 2> errors.txt   # ترسل 2> الأخطاء إلى ملف
echo "errors saved: $(cat errors.txt | wc -l) line(s)"
ls missing-file > all.txt 2>&1  # المخرجات والأخطاء معًا
echo "exit code of the last command: $?"
```

```reference bash
cmd > f | كتابة المخرجات في ملف (استبدال) | ls > files.txt
cmd >> f | إلحاق المخرجات | echo ok >> log.txt
cmd < f | قراءة المدخلات من ملف | sort < names.txt
a|b | أنبوب: مخرجات a تدخل إلى b | cat log | grep error
2> f | كتابة الأخطاء في ملف | find / 2> /dev/null
> f 2>&1 | المخرجات والأخطاء في ملف واحد | ./run.sh > out.log 2>&1
/dev/null | التخلص من المخرجات | cmd > /dev/null
$? | رمز خروج آخر أمر (0 = نجاح) | echo $?
```

:::tip فكرة Unix
أدوات صغيرة تؤدي كل منها مهمة واحدة، وتُربط بالأنابيب، تجيب عن أسئلة كبيرة: `cut` و `sort` و `uniq -c` و `head` معًا تعطيك "أعلى 10" من أي سجل.
:::

```exercise bash
? أضف السطر إلى log.txt بدون حذف ما فيه
echo "done" ___ log.txt
= >>
```

```quiz
? ماذا يعني رمز الخروج 0؟
* نجح الأمر
- فشل الأمر
- لم يطبع الأمر شيئًا
```

# @lesson bash-text
title: التعامل مع النصوص
summary: cat و grep و head و tail و wc و cut و sort و sed و awk.
---
```try bash
cd "$(mktemp -d)"
cat > sales.csv <<'EOF'
date,branch,amount
2026-01-03,Cairo,1200
2026-01-03,Alex,800
2026-01-04,Cairo,1500
2026-01-05,Giza,400
EOF

head -n 2 sales.csv
tail -n 1 sales.csv
grep "Cairo" sales.csv
grep -c "2026-01-03" sales.csv          # عدّ الأسطر المطابقة
grep -v "Cairo" sales.csv | tail -n +2  # الأسطر بدون Cairo، مع تخطي العنوان
cut -d, -f2 sales.csv | tail -n +2 | sort -u
sed 's/Alex/Alexandria/' sales.csv | grep Alexandria
awk -F, 'NR > 1 { total += $3 } END { print "total:", total }' sales.csv
awk -F, 'NR > 1 && $3 > 1000 { print $2, $3 }' sales.csv
```

```reference bash
cat f | طباعة ملف | cat notes.txt
head -n N / tail -n N | أول / آخر N سطر | tail -n 20 app.log
tail -f | متابعة ملف يكبر | tail -f /var/log/syslog
grep pat f | الأسطر المطابقة | grep -i error app.log
grep -v / -c / -r | غير المطابقة / العدد / داخل المجلدات | grep -r TODO src/
wc -l | عدّ الأسطر | wc -l < file
cut -d, -fN | العمود N من ملف بفواصل | cut -d: -f1 /etc/passwd
sort / sort -n / uniq -c | ترتيب / رقميًا / عدّ التكرار | sort | uniq -c
sed 's/a/b/' | استبدال نص | sed 's/http:/https:/g'
awk '{ print $2 }' | الأعمدة والحسابات الصغيرة | awk -F, '{s+=$3} END {print s}'
```

:::tip مستندات here
`cat > file <<'EOF' ... EOF` تكتب عدة أسطر في ملف دفعة واحدة. ومع علامات التنصيص حول `'EOF'` لا يُعوَّض أي شيء بداخلها.
:::

```exercise bash
? اعرض فقط الأسطر التي فيها ERROR من app.log
___ "ERROR" app.log
= grep
```

```quiz
? أي أمر يعرض آخر 5 أسطر من ملف؟
* tail -n 5 file
- head -n 5 file
- last 5 file
```

# @lesson bash-conditions
title: الشروط والاختبارات
summary: if و [[ ]] ومقارنة الأرقام والنصوص واختبار الملفات و case.
---
```try bash
age=20
if [[ $age -ge 18 ]]; then
    echo "Adult"
else
    echo "Minor"
fi

name="sara"
if [[ $name == "sara" && $age -lt 30 ]]; then
    echo "Hi Sara"
fi
if [[ -z "$missing" ]]; then
    echo "missing is empty"
fi

file="/etc/hostname"
if [[ -f $file ]]; then
    echo "$file exists"
elif [[ -d $file ]]; then
    echo "$file is a folder"
else
    echo "$file not found"
fi

(( age > 18 )) && echo "arithmetic test works too"

day="fri"
case $day in
    fri|sat) echo "Weekend" ;;
    *)       echo "Working day" ;;
esac
```

```reference bash
if [[ c ]]; then ... fi | شرط | if [[ -f $f ]]; then echo ok; fi
-eq -ne -lt -le -gt -ge | مقارنة الأرقام | [[ $n -gt 10 ]]
== / != | مقارنة النصوص | [[ $s == "yes" ]]
-z / -n | نص فارغ / غير فارغ | [[ -z $name ]]
-f / -d / -e | ملف / مجلد / موجود | [[ -d logs ]]
&& / || | و / أو | [[ $a && $b ]]
(( a > b )) | مقارنة حسابية | (( count >= 3 ))
case ... esac | الاختيار حسب النمط | case $x in y*) ... ;; esac
```

:::warning المسافات مهمة
تحتاج `[[ $a == $b ]]` إلى مسافة بعد `[[` وقبل `]]`. كتابة `[[$a==$b]]` تعطي خطأ "command not found".
:::

```exercise bash
? اختبر هل الرقم n أكبر من 10
if [[ $n ___ 10 ]]; then echo big; fi
= -gt
```

```quiz
? أي اختبار يكون صحيحًا عندما يوجد الملف وهو ملف عادي؟
* -f
- -d
- -z

? تنتهي كتل case بالكلمة esac.
= true
```

# @lesson bash-loops
title: الحلقات
summary: for على القوائم والملفات والنطاقات، و while و read.
---
```try bash
for fruit in apple banana cherry; do
    echo "I like $fruit"
done

for i in {1..5}; do
    echo -n "$i "
done
echo

for (( i = 10; i > 0; i -= 3 )); do
    echo -n "$i "
done
echo

cd "$(mktemp -d)"
touch report1.txt report2.txt photo.png
for f in *.txt; do
    echo "text file: $f"
done

count=3
while (( count > 0 )); do
    echo "countdown $count"
    (( count-- ))
done

printf "Sara 25\nOmar 31\n" > people.txt
while read -r name age; do
    echo "$name is $age"
done < people.txt
```

```reference bash
for x in a b c; do ... done | المرور على كلمات | for h in web1 web2; do ssh $h uptime; done
{1..10} | نطاق أرقام | for i in {1..3}
for (( i=0; i<n; i++ )) | حلقة بأسلوب C | for (( i=0; i<5; i++ ))
for f in *.log | المرور على الملفات المطابقة | for f in *.csv
while cond; do ... done | كرر ما دام الشرط صحيحًا | while [[ -f lock ]]; do sleep 1; done
while read -r line | قراءة ملف سطرًا سطرًا | while read -r l; do echo $l; done < f
break / continue | اخرج / تخطَّ | [[ $x == stop ]] && break
```

:::tip اقرأ الملفات بـ while read
`for line in $(cat file)` تقسّم عند كل مسافة لا عند الأسطر. أما `while read -r line; do ...; done < file` فتقرأ سطرًا كاملًا في كل مرة.
:::

```exercise bash
? مرّ على الأرقام من 1 إلى 3 بتوسيع الأقواس
for i in ___; do echo $i; done
= {1..3}
```

```quiz
? أي حلقة تقرأ ملفًا سطرًا سطرًا؟
* while read -r line; do ... done < file
- for line in file
- repeat file
```

# @lesson bash-functions
title: السكربتات والدوال
summary: سطر shebang والمعاملات والدوال وقيم الإرجاع ورموز الخروج.
---
السكربت ملف نصي يبدأ بسطر **shebang** يحدد المفسّر:

```text
#!/usr/bin/env bash
set -euo pipefail
echo "Hello from a script"
```

احفظه باسم `hello.sh`، واجعله قابلًا للتنفيذ بـ `chmod +x hello.sh`، ثم شغّله بـ `./hello.sh`.

```try bash
greet() {
    local name="$1"                # أول معامل؛ local = داخل الدالة فقط
    local greeting="${2:-Hello}"   # ثاني معامل، أو قيمة افتراضية
    echo "$greeting, $name!"
}

greet "Sara"
greet "Omar" "Welcome"

is_even() {
    (( $1 % 2 == 0 ))              # رمز الخروج هو النتيجة
}
for n in 3 8; do
    if is_even "$n"; then echo "$n is even"; else echo "$n is odd"; fi
done

sum() {
    local total=0
    for n in "$@"; do              # "$@": كل المعاملات
        (( total += n ))
    done
    echo "$total"                  # "أرجِع" النص بطباعته
}
result=$(sum 4 5 6)
echo "sum = $result"

set -- alpha beta                  # اضبط معاملات السكربت نفسه للتجربة
echo "script got $# arguments: $1 and $2"
```

```reference bash
#!/usr/bin/env bash | shebang: التشغيل بـ Bash | أول سطر في السكربت
chmod +x f | جعل السكربت قابلًا للتنفيذ | chmod +x deploy.sh
$1 $2 ... | المعاملات | echo "file: $1"
$@ / $# | كل المعاملات / عددها | for a in "$@"
f() { ... } | تعريف دالة | log() { echo "[$(date +%T)] $*"; }
local | متغير داخل الدالة فقط | local count=0
return N / exit N | رمز خروج الدالة / السكربت | exit 1
set -euo pipefail | التوقف عند الأخطاء والمتغيرات غير المعرّفة | أول كل سكربت
```

:::tip set -euo pipefail
ضعها في أول السكربتات: `-e` توقف عند أول أمر يفشل، و `-u` توقف عند متغير غير معرّف، و `pipefail` تجعل الأنبوب يفشل إذا فشل أي جزء منه. فتوقف الأخطاء السكربت بدل أن يستمر بصمت.
:::

```exercise bash
? اقرأ أول معامل مُرسل إلى الدالة
local file="___"
= $1
```

```quiz
? ماذا يحمل "$@"؟
* كل المعاملات، كل منها كلمة مستقلة
- عدد المعاملات
- اسم السكربت

? تعني exit 0 أن السكربت انتهى بنجاح.
= true
```

# @lesson bash-arrays
title: المصفوفات والحساب
summary: المصفوفات المرقّمة والترابطية، والحساب بـ $(( )).
---
```try bash
servers=("web1" "web2" "db1")
servers+=("cache1")
echo "first: ${servers[0]}"
echo "all: ${servers[*]}"
echo "count: ${#servers[@]}"
for s in "${servers[@]}"; do
    echo "checking $s"
done

declare -A price               # مصفوفة ترابطية (مفتاح -> قيمة)
price[tea]=12
price[coffee]=20
for item in "${!price[@]}"; do
    echo "$item costs ${price[$item]}"
done | sort

a=17
b=5
echo "sum $(( a + b )), product $(( a * b ))"
echo "integer division $(( a / b )), remainder $(( a % b ))"
(( a++ ))
echo "a is now $a"
echo "decimals need bc or awk: $(awk "BEGIN { printf \"%.2f\", $a / $b }")"
```

```reference bash
arr=(a b c) | إنشاء مصفوفة | ports=(80 443)
${arr[i]} | عنصر واحد | echo ${ports[0]}
"${arr[@]}" | كل العناصر، كل منها بين علامتي تنصيص | for p in "${ports[@]}"
${#arr[@]} | عدد العناصر | echo ${#ports[@]}
arr+=(x) | إلحاق | ports+=(8080)
declare -A m | مصفوفة ترابطية | m[key]=value
${!m[@]} | كل المفاتيح | for k in "${!m[@]}"
$(( expr )) | حساب بالأعداد الصحيحة | echo $(( 7 * 6 ))
```

:::warning أعداد صحيحة فقط
الحساب في Bash بالأعداد الصحيحة: `$(( 7 / 2 ))` تساوي `3`. استخدم `awk` أو `bc` عند الحاجة إلى الكسور.
:::

```exercise bash
? اطبع عدد عناصر المصفوفة servers
echo ${___servers[@]}
= #
```

```quiz
? ما ناتج $(( 7 / 2 )) في Bash؟
* 3
- 3.5
- 4
```

# @lesson bash-processes
title: العمليات والصلاحيات والجدولة
summary: ps و kill والمهام في الخلفية و chmod و sudo و cron.
---
```try bash
sleep 2 &                     # تشغّل & الأمر في الخلفية
pid=$!
echo "started background job $pid"
ps -o pid,cmd -p "$pid"
wait "$pid"
echo "background job finished"

cd "$(mktemp -d)"
echo 'echo "I can run"' > tool.sh
ls -l tool.sh
chmod u+x tool.sh             # أعطِ المالك صلاحية التنفيذ
ls -l tool.sh
./tool.sh
chmod 640 tool.sh             # rw- r-- --- بالأرقام
stat -c "%A %a %n" tool.sh

echo "running as $(id -un), groups: $(id -Gn)"
```

```reference bash
ps aux / top | العمليات الجارية | ps aux | grep nginx
cmd & / jobs / fg | مهمة في الخلفية / عرضها / إرجاعها | ./build.sh &
$! / wait | رقم آخر مهمة في الخلفية / انتظارها | wait $!
kill PID / kill -9 PID | طلب الإيقاف / إيقاف بالقوة | kill 1234
chmod u+x / chmod 755 | تغيير الصلاحيات | chmod 600 key.pem
chown user:group f | تغيير المالك | sudo chown www-data site/
sudo cmd | تشغيل كمسؤول | sudo systemctl restart nginx
crontab -e | جدولة أوامر | 0 2 * * * /opt/backup.sh
```

حقول سطر cron الخمسة هي: الدقيقة، الساعة، يوم الشهر، الشهر، يوم الأسبوع. `0 2 * * *` تعني "كل يوم الساعة 02:00".

:::danger انتبه مع sudo و kill -9
`sudo` تعطي الأمر تحكمًا كاملًا في الجهاز، و `kill -9` توقف البرنامج دون أن تتيح له حفظ عمله. جرّب الصيغة اللطيفة (`kill PID`) أولًا.
:::

```exercise bash
? اجعل deploy.sh قابلًا للتنفيذ لمالكه
chmod ___ deploy.sh
= u+x | +x | 755 | 744 | 700
```

```quiz
? ماذا تفعل & في نهاية الأمر؟
* تشغّله في الخلفية
- تشغّله كمسؤول
- تشغّله مرتين

? في chmod 640 يستطيع المالك قراءة الملف والكتابة فيه.
= true
> 6 = قراءة (4) + كتابة (2) للمالك، و 4 = قراءة للمجموعة، و 0 = لا شيء للآخرين.
```

# @lesson bash-project
title: مشروع: سكربت تقرير سجلات
summary: اجمع كل ما تعلمته في سكربت يلخّص سجل خادم ويب.
---
يبني هذا السكربت سجلًا صغيرًا كمثال، ثم يعرض عدد الطلبات ونسبة الأخطاء وأكثر الصفحات زيارة، باستخدام أدوات هذه الدورة فقط.

```try bash
set -euo pipefail
cd "$(mktemp -d)"
cat > access.log <<'EOF'
10.0.0.1 GET /home 200
10.0.0.2 GET /login 200
10.0.0.1 POST /login 401
10.0.0.3 GET /home 200
10.0.0.4 GET /products 500
10.0.0.2 GET /home 200
10.0.0.3 GET /products 200
EOF

report() {
    local log="$1"
    local total errors
    total=$(wc -l < "$log")
    errors=$(awk '$4 >= 400' "$log" | wc -l)
    echo "Requests: $total"
    echo "Errors:   $errors ($(( errors * 100 / total ))%)"
    echo "Unique visitors: $(cut -d' ' -f1 "$log" | sort -u | wc -l)"
    echo "Top pages:"
    awk '{ print $3 }' "$log" | sort | uniq -c | sort -rn | head -n 2
}

if [[ ! -f access.log ]]; then
    echo "log not found" >&2
    exit 1
fi
report access.log
```

:::tip جرّب بنفسك
أضف سطرًا يطبع أكثر عنوان IP نشاطًا، أو اجعل السكربت يأخذ اسم ملف السجل كأول معامل (`$1`) مع `access.log` كقيمة افتراضية.
:::

```quiz
? أي جزء في السكربت يطبع رسالة خطأ إلى stderr؟
* echo "log not found" >&2
- echo "Requests: $total"
- sort -rn
```

# @lesson bash-reference
title: مرجع Bash السريع
summary: أكثر الأوامر والصيغ استخدامًا في صفحة واحدة.
---
```reference bash
ls / cd / pwd | التنقل | cd /var/log
mkdir -p / cp -r / mv / rm -r | إدارة الملفات | cp -r src backup
cat / head / tail -f | قراءة الملفات | tail -f app.log
grep / cut / sort / uniq -c | تصفية النصوص | grep -c ERROR app.log
sed / awk | التعديل والحساب | awk '{s+=$2} END {print s}'
>, >>, |, 2>&1 | إعادة التوجيه والأنابيب | cmd > out.log 2>&1
x="v" / "$x" / $(cmd) | المتغيرات | now=$(date +%F)
if [[ ]]; then; fi | الشروط | [[ -f $f ]]
for / while read | الحلقات | for f in *.csv
f() { local x="$1"; } | الدوال | greet "Sara"
arr=(a b) / declare -A | المصفوفات | "${arr[@]}"
$(( )) | حساب بالأعداد الصحيحة | $(( a + b ))
chmod / sudo / ps / kill | النظام | chmod +x run.sh
set -euo pipefail | سكربتات آمنة | أول كل سكربت
```

:::tip الخطوة التالية
أتمِت مهمة حقيقية: سكربت نسخ احتياطي يضغط مجلدًا بـ `tar`، ويسمّيه بالتاريخ، ويحتفظ بآخر سبع نسخ، ويعمل كل ليلة من cron.
:::

```quiz
? أي سطر يوضع في أول سكربت Bash آمن؟
* set -euo pipefail
- rm -rf /
- exit 0
```
