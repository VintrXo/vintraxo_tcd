# @lesson bash-intro
title: Bash introduction
summary: What the shell is, what Bash is, and your first commands.
---
A **shell** is the program that reads the commands you type in a terminal and runs them. **Bash** is the most common shell on Linux servers, and it is also a scripting language: a file of commands that you can run again and again.

```try bash
echo "Hello, Bash"
echo "Today is $(date +%A)"
whoami
pwd
```

- `echo` prints text.
- `$(command)` runs a command and puts its output in place.
- `whoami` shows the current user; `pwd` shows the current folder.

:::info Running the examples
Bash examples run in a separate, secure sandbox; if it is not enabled yet they run as soon as it is. On your computer: open a terminal on Linux or macOS, or use WSL or Git Bash on Windows.
:::

```quiz
? What is a shell?
* A program that reads and runs your commands
- A text editor
- A web browser

? A Bash script is a file of commands that can be run many times.
= true
```

# @lesson bash-files
title: Files and folders
summary: ls, cd, mkdir, touch, cp, mv, rm and paths.
---
```try bash
cd "$(mktemp -d)"            # work in an empty temporary folder
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
ls / ls -la | List files / with details and hidden files | ls -la /etc
cd dir / cd .. / cd ~ | Change folder / up one / home | cd ~/projects
pwd | Current folder | pwd
mkdir -p a/b | Make folders (with parents) | mkdir -p logs/2026
touch f | Create an empty file | touch notes.txt
cp / cp -r | Copy a file / a folder | cp -r src backup
mv | Move or rename | mv old.txt new.txt
rm / rm -r | Delete a file / a folder | rm -r build
```

:::danger rm has no recycle bin
`rm` deletes immediately and for good. Double-check paths, especially with `-r` and wildcards, and never run `rm -rf` on a path built from a variable that might be empty.
:::

```exercise bash
? Create the folders logs/2026 in one command, including logs
mkdir ___ logs/2026
= -p
```

```quiz
? Which command renames a file?
* mv
- cp
- rn

? A path that starts with / is an absolute path.
= true
```

# @lesson bash-variables
title: Variables and quoting
summary: Assigning variables, $VAR, quotes, and command substitution.
---
```try bash
name="Sara"                  # no spaces around =
age=25
echo "Name: $name, age: $age"
echo 'Single quotes: $name stays as text'
echo "Braces: ${name}_backup"

files=$(ls / | wc -l)
echo "The root folder has $files entries"

greeting="hello world"
echo "${#greeting} characters"
echo "${greeting^^}"         # upper case
echo "${greeting/world/Bash}"

readonly PI=3.14
echo "$PI"
echo "Home folder: $HOME, shell: $SHELL"
```

```reference bash
x=value | Assign (no spaces) | city="Cairo"
$x / ${x} | Read a variable | echo "${city}s"
"..." / '...' | Double quotes expand $, single quotes do not | echo "$x" '$x'
$(cmd) | Command output as a value | now=$(date)
${#x} | Length | echo ${#name}
${x^^} / ${x,,} | Upper / lower case | echo ${name^^}
${x/a/b} | Replace first match | echo ${path/home/root}
${x:-default} | Value, or a default if empty | echo ${PORT:-8000}
export X | Make it visible to programs you start | export PATH="$PATH:~/bin"
```

:::warning Always quote variables
Write `"$file"`, not `$file`. Without quotes, a value with spaces is split into several words, and an empty value disappears, which breaks commands in surprising ways.
:::

```exercise bash
? Store the output of the date command in now
now=___(date)
= $
```

```quiz
? Which line assigns a variable correctly?
* city="Cairo"
- city = "Cairo"
- $city="Cairo"

? Variables inside single quotes are expanded.
= false
> Only double quotes expand $variables; single quotes keep the text exactly.
```

# @lesson bash-pipes
title: Pipes and redirection
summary: >, >>, <, |, and the standard streams.
---
Every command has three streams: **stdin** (input), **stdout** (output) and **stderr** (errors). You can send them to files or to other commands.

```try bash
cd "$(mktemp -d)"
echo "first" > log.txt         # write (replaces the file)
echo "second" >> log.txt       # append
cat log.txt
wc -l < log.txt                # read input from a file

printf "banana\napple\ncherry\napple\n" > fruits.txt
sort fruits.txt | uniq          # | sends the output to the next command
sort fruits.txt | uniq -c | sort -rn | head -1

ls missing-file 2> errors.txt   # 2> sends errors to a file
echo "errors saved: $(cat errors.txt | wc -l) line(s)"
ls missing-file > all.txt 2>&1  # output and errors together
echo "exit code of the last command: $?"
```

```reference bash
cmd > f | Write output to a file (replace) | ls > files.txt
cmd >> f | Append output | echo ok >> log.txt
cmd < f | Read input from a file | sort < names.txt
a|b | Pipe: output of a into b | cat log | grep error
2> f | Write errors to a file | find / 2> /dev/null
> f 2>&1 | Output and errors to one file | ./run.sh > out.log 2>&1
/dev/null | Throw output away | cmd > /dev/null
$? | Exit code of the last command (0 = success) | echo $?
```

:::tip The Unix idea
Small tools that each do one thing, joined with pipes, can answer big questions: `cut`, `sort`, `uniq -c` and `head` together give you a "top 10" of any log.
:::

```exercise bash
? Add the line to log.txt without deleting what is there
echo "done" ___ log.txt
= >>
```

```quiz
? What does the exit code 0 mean?
* The command succeeded
- The command failed
- The command printed nothing
```

# @lesson bash-text
title: Working with text
summary: cat, grep, head, tail, wc, cut, sort, sed and awk.
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
grep -c "2026-01-03" sales.csv          # count matching lines
grep -v "Cairo" sales.csv | tail -n +2  # lines without Cairo, skip header
cut -d, -f2 sales.csv | tail -n +2 | sort -u
sed 's/Alex/Alexandria/' sales.csv | grep Alexandria
awk -F, 'NR > 1 { total += $3 } END { print "total:", total }' sales.csv
awk -F, 'NR > 1 && $3 > 1000 { print $2, $3 }' sales.csv
```

```reference bash
cat f | Print a file | cat notes.txt
head -n N / tail -n N | First / last N lines | tail -n 20 app.log
tail -f | Follow a growing file | tail -f /var/log/syslog
grep pat f | Lines that match | grep -i error app.log
grep -v / -c / -r | Not matching / count / in folders | grep -r TODO src/
wc -l | Count lines | wc -l < file
cut -d, -fN | Column N of a delimited file | cut -d: -f1 /etc/passwd
sort / sort -n / uniq -c | Sort / numerically / count repeats | sort | uniq -c
sed 's/a/b/' | Replace text | sed 's/http:/https:/g'
awk '{ print $2 }' | Columns and small calculations | awk -F, '{s+=$3} END {print s}'
```

:::tip Here documents
`cat > file <<'EOF' ... EOF` writes several lines to a file in one go. With quotes around `'EOF'`, nothing inside is expanded.
:::

```exercise bash
? Show only lines containing ERROR from app.log
___ "ERROR" app.log
= grep
```

```quiz
? Which command shows the last 5 lines of a file?
* tail -n 5 file
- head -n 5 file
- last 5 file
```

# @lesson bash-conditions
title: Conditions and tests
summary: if, [[ ]], comparing numbers and strings, testing files, and case.
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
if [[ c ]]; then ... fi | Condition | if [[ -f $f ]]; then echo ok; fi
-eq -ne -lt -le -gt -ge | Compare numbers | [[ $n -gt 10 ]]
== / != | Compare strings | [[ $s == "yes" ]]
-z / -n | Empty / not empty string | [[ -z $name ]]
-f / -d / -e | Is a file / a folder / exists | [[ -d logs ]]
&& / || | And / or | [[ $a && $b ]]
(( a > b )) | Arithmetic comparison | (( count >= 3 ))
case ... esac | Choose by pattern | case $x in y*) ... ;; esac
```

:::warning Spaces matter
`[[ $a == $b ]]` needs a space after `[[` and before `]]`. Writing `[[$a==$b]]` gives a "command not found" error.
:::

```exercise bash
? Test whether the number n is greater than 10
if [[ $n ___ 10 ]]; then echo big; fi
= -gt
```

```quiz
? Which test is true when a file exists and is a regular file?
* -f
- -d
- -z

? case blocks end with esac.
= true
```

# @lesson bash-loops
title: Loops
summary: for over lists, files and ranges, while and read.
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
for x in a b c; do ... done | Loop over words | for h in web1 web2; do ssh $h uptime; done
{1..10} | Range of numbers | for i in {1..3}
for (( i=0; i<n; i++ )) | C-style loop | for (( i=0; i<5; i++ ))
for f in *.log | Loop over matching files | for f in *.csv
while cond; do ... done | Repeat while true | while [[ -f lock ]]; do sleep 1; done
while read -r line | Read a file line by line | while read -r l; do echo $l; done < f
break / continue | Leave / skip | [[ $x == stop ]] && break
```

:::tip Read files with while read
`for line in $(cat file)` splits on every space, not on lines. `while read -r line; do ...; done < file` reads one whole line at a time.
:::

```exercise bash
? Loop over the numbers 1 to 3 with brace expansion
for i in ___; do echo $i; done
= {1..3}
```

```quiz
? Which loop reads a file one line at a time?
* while read -r line; do ... done < file
- for line in file
- repeat file
```

# @lesson bash-functions
title: Scripts and functions
summary: The shebang, arguments, functions, return values and exit codes.
---
A script is a text file that starts with a **shebang** line naming the interpreter:

```text
#!/usr/bin/env bash
set -euo pipefail
echo "Hello from a script"
```

Save it as `hello.sh`, make it executable with `chmod +x hello.sh`, and run `./hello.sh`.

```try bash
greet() {
    local name="$1"                # first argument; local = only in the function
    local greeting="${2:-Hello}"   # second argument, or a default
    echo "$greeting, $name!"
}

greet "Sara"
greet "Omar" "Welcome"

is_even() {
    (( $1 % 2 == 0 ))              # the exit code is the result
}
for n in 3 8; do
    if is_even "$n"; then echo "$n is even"; else echo "$n is odd"; fi
done

sum() {
    local total=0
    for n in "$@"; do              # "$@": all arguments
        (( total += n ))
    done
    echo "$total"                  # "return" text by printing it
}
result=$(sum 4 5 6)
echo "sum = $result"

set -- alpha beta                  # set the script's own arguments for the demo
echo "script got $# arguments: $1 and $2"
```

```reference bash
#!/usr/bin/env bash | Shebang: run with Bash | first line of the script
chmod +x f | Make a script executable | chmod +x deploy.sh
$1 $2 ... | Arguments | echo "file: $1"
$@ / $# | All arguments / how many | for a in "$@"
f() { ... } | Define a function | log() { echo "[$(date +%T)] $*"; }
local | Variable only inside the function | local count=0
return N / exit N | Exit code of a function / the script | exit 1
set -euo pipefail | Stop on errors and unset variables | top of every script
```

:::tip set -euo pipefail
Put it at the top of scripts: `-e` stops at the first failing command, `-u` stops on an unset variable, and `pipefail` makes a pipe fail when any part of it fails. Bugs then stop the script instead of quietly running on.
:::

```exercise bash
? Read the first argument passed to the function
local file="___"
= $1
```

```quiz
? What does "$@" hold?
* All the arguments, each kept as its own word
- The number of arguments
- The script name

? exit 0 means the script finished successfully.
= true
```

# @lesson bash-arrays
title: Arrays and arithmetic
summary: Indexed and associative arrays, and $(( )) arithmetic.
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

declare -A price               # associative array (key -> value)
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
arr=(a b c) | Create an array | ports=(80 443)
${arr[i]} | One item | echo ${ports[0]}
"${arr[@]}" | All items, each quoted | for p in "${ports[@]}"
${#arr[@]} | Number of items | echo ${#ports[@]}
arr+=(x) | Append | ports+=(8080)
declare -A m | Associative array | m[key]=value
${!m[@]} | All keys | for k in "${!m[@]}"
$(( expr )) | Integer arithmetic | echo $(( 7 * 6 ))
```

:::warning Only whole numbers
Bash arithmetic works with integers: `$(( 7 / 2 ))` is `3`. Use `awk` or `bc` when you need decimals.
:::

```exercise bash
? Print the number of items in the array servers
echo ${___servers[@]}
= #
```

```quiz
? What does $(( 7 / 2 )) give in Bash?
* 3
- 3.5
- 4
```

# @lesson bash-processes
title: Processes, permissions and scheduling
summary: ps, kill, background jobs, chmod, sudo and cron.
---
```try bash
sleep 2 &                     # & runs a command in the background
pid=$!
echo "started background job $pid"
ps -o pid,cmd -p "$pid"
wait "$pid"
echo "background job finished"

cd "$(mktemp -d)"
echo 'echo "I can run"' > tool.sh
ls -l tool.sh
chmod u+x tool.sh             # give the owner permission to execute
ls -l tool.sh
./tool.sh
chmod 640 tool.sh             # rw- r-- --- in numbers
stat -c "%A %a %n" tool.sh

echo "running as $(id -un), groups: $(id -Gn)"
```

```reference bash
ps aux / top | Running processes | ps aux | grep nginx
cmd & / jobs / fg | Background job / list / bring back | ./build.sh &
$! / wait | PID of the last background job / wait for it | wait $!
kill PID / kill -9 PID | Ask to stop / force stop | kill 1234
chmod u+x / chmod 755 | Change permissions | chmod 600 key.pem
chown user:group f | Change owner | sudo chown www-data site/
sudo cmd | Run as administrator | sudo systemctl restart nginx
crontab -e | Schedule commands | 0 2 * * * /opt/backup.sh
```

The five fields of a cron line are: minute, hour, day of month, month, day of week. `0 2 * * *` means "every day at 02:00".

:::danger Be careful with sudo and kill -9
`sudo` gives a command full control of the machine, and `kill -9` stops a program without letting it save its work. Try the gentle form (`kill PID`) first.
:::

```exercise bash
? Make deploy.sh executable for its owner
chmod ___ deploy.sh
= u+x | +x | 755 | 744 | 700
```

```quiz
? What does & at the end of a command do?
* Runs it in the background
- Runs it as administrator
- Runs it twice

? In chmod 640, the owner can read and write the file.
= true
> 6 = read (4) + write (2) for the owner, 4 = read for the group, 0 = nothing for others.
```

# @lesson bash-project
title: Project: a log report script
summary: Combine everything into a script that summarises a web server log.
---
This script builds a small sample log, then reports the number of requests, the error rate, and the busiest pages, using only the tools from this course.

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

:::tip Try it yourself
Add a line that prints the busiest IP address, or make the script take the log file name as its first argument (`$1`) with `access.log` as the default.
:::

```quiz
? Which part of the script prints an error message to stderr?
* echo "log not found" >&2
- echo "Requests: $total"
- sort -rn
```

# @lesson bash-reference
title: Bash quick reference
summary: The most used commands and syntax on one page.
---
```reference bash
ls / cd / pwd | Move around | cd /var/log
mkdir -p / cp -r / mv / rm -r | Manage files | cp -r src backup
cat / head / tail -f | Read files | tail -f app.log
grep / cut / sort / uniq -c | Filter text | grep -c ERROR app.log
sed / awk | Edit and compute | awk '{s+=$2} END {print s}'
>, >>, |, 2>&1 | Redirect and pipe | cmd > out.log 2>&1
x="v" / "$x" / $(cmd) | Variables | now=$(date +%F)
if [[ ]]; then; fi | Conditions | [[ -f $f ]]
for / while read | Loops | for f in *.csv
f() { local x="$1"; } | Functions | greet "Sara"
arr=(a b) / declare -A | Arrays | "${arr[@]}"
$(( )) | Integer arithmetic | $(( a + b ))
chmod / sudo / ps / kill | System | chmod +x run.sh
set -euo pipefail | Safe scripts | top of every script
```

:::tip Where to go next
Automate a real task: a backup script that compresses a folder with `tar`, names it with the date, keeps the last seven copies, and runs every night from cron.
:::

```quiz
? Which line belongs at the top of a safe Bash script?
* set -euo pipefail
- rm -rf /
- exit 0
```
