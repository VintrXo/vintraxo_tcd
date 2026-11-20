# @lesson git-intro
title: مقدمة في Git
summary: ما هو نظام إدارة الإصدارات، ولماذا يستخدمه كل المبرمجين.
---
**Git** نظام لإدارة الإصدارات: يحفظ «لقطات» من مشروعك كلما طلبت، فتستطيع الرجوع لأي نسخة سابقة، ومعرفة من غيّر ماذا ومتى، والعمل مع فريق على نفس الملفات دون أن يمسح أحد عمل الآخر.

## مفاهيم أساسية

- **المستودع** (repository): مجلد مشروعك مع تاريخه الكامل.
- **الإيداع** (commit): لقطة محفوظة من الملفات مع رسالة تشرح التغيير.
- **الفرع** (branch): خط عمل مستقل تجرّب فيه دون التأثير على الأصل.
- **المستودع البعيد** (remote): نسخة من المستودع على خادم مثل GitHub أو GitLab.

:::info Git و GitHub
**Git** البرنامج الذي يعمل على جهازك. **GitHub** موقع يستضيف المستودعات لتشاركها مع غيرك. توجد بدائل مثل GitLab و Bitbucket.
:::

```quiz
? ما هو الإيداع commit في Git؟
- ملف جديد
* لقطة محفوظة من المشروع مع رسالة
- خادم على الإنترنت

? موقع GitHub هو نفسه برنامج Git.
= false
> Git برنامج على جهازك، و GitHub موقع يستضيف المستودعات.
```

# @lesson git-config
title: التثبيت والإعداد
summary: تثبيت Git وضبط الاسم والبريد.
---
## التثبيت

- **ويندوز**: نزّل *Git for Windows* من الموقع الرسمي git-scm.com.
- **ماك**: اكتب `git --version` في الطرفية وسيعرض تثبيته.
- **لينكس**: `sudo apt install git` على أوبونتو.

تأكد من التثبيت:

```bash
git --version
```

## عرّف نفسك

كل إيداع يُسجَّل باسمك وبريدك، فاضبطهما مرة واحدة:

```bash
git config --global user.name "سارة أحمد"
git config --global user.email "sara@example.com"
git config --global init.defaultBranch main
git config --list
```

```exercise bash
? أكمل الأمر لضبط بريدك
git config --global user.___ "me@example.com"
= email
```

```quiz
? ماذا يفعل الخيار --global؟
* يطبّق الإعداد على كل مستودعاتك
- يرفع الإعداد إلى GitHub
- يحذف الإعداد القديم

? يُسجَّل اسمك وبريدك في كل إيداع.
= true
```

# @lesson git-init
title: إنشاء مستودع
summary: git init و git status، ومناطق Git الثلاث.
---
ادخل مجلد مشروعك وأنشئ مستودعًا:

```bash
mkdir my-site
cd my-site
git init
git status
```

`git init` ينشئ مجلدًا مخفيًا اسمه `.git` يحتفظ بكل التاريخ. و`git status` يخبرك بحالة الملفات في أي وقت.

## المناطق الثلاث

1. **مجلد العمل**: ملفاتك كما تعدّلها.
2. **منطقة التجهيز** (staging): ما اخترته ليدخل في الإيداع القادم.
3. **المستودع**: الإيداعات المحفوظة.

الملف ينتقل بينها بالأوامر: `git add` إلى التجهيز، و`git commit` إلى المستودع.

:::tip استخدم git status كثيرًا
قبل أي أمر وبعده، `git status` يوضح لك ما الذي تغيّر وما الذي جاهز للحفظ.
:::

```quiz
? أي أمر ينشئ مستودع Git جديدًا؟
* git init
- git start
- git new

? المجلد المخفي .git يحتفظ بتاريخ المستودع.
= true
```

# @lesson git-commit
title: الحفظ: add و commit
summary: تجهيز الملفات وحفظ الإيداعات برسائل واضحة.
---
```bash
echo "<h1>مرحبا</h1>" > index.html
git status
git add index.html
git commit -m "إضافة الصفحة الرئيسية"
```

- `git add ملف` يضيف ملفًا للتجهيز، و`git add .` يضيف كل التغييرات.
- `git commit -m "رسالة"` يحفظ الإيداع.

## رسالة إيداع جيدة

- قصيرة وواضحة: **ماذا** تغيّر **ولماذا**.
- بصيغة الأمر: «إضافة نموذج التواصل» أفضل من «عدّلت أشياء».
- إيداع لكل تغيير منطقي واحد، لا إيداع ضخم لكل شيء.

:::warning لا تحفظ كلمات السر
لا تضف إلى المستودع ملفات فيها كلمات سر أو مفاتيح. لو وصلت إلى GitHub، اعتبرها مسرّبة وغيّرها فورًا.
:::

```exercise bash
? أكمل الأمر لتجهيز كل الملفات المعدّلة
git add ___
= .
```

```quiz
? ما ترتيب الأوامر لحفظ تغيير؟
* git add ثم git commit
- git commit ثم git add
- git save فقط

? الأمر git commit -m يحفظ الإيداع مع رسالة.
= true
```

# @lesson git-log-diff
title: التاريخ والفروقات
summary: git log و git diff و git show.
---
```bash
git log
git log --oneline
git log --oneline --graph --all
```

كل إيداع له **معرّف** (hash) مثل `a1b2c3d`.

## ماذا تغيّر؟

```bash
git diff              # تغييرات لم تُجهَّز بعد
git diff --staged     # ما سيدخل الإيداع القادم
git show a1b2c3d      # تفاصيل إيداع محدد
```

```reference bash
git log | تاريخ الإيداعات | git log -5
git log --oneline | سطر لكل إيداع | git log --oneline
git log -- ملف | تاريخ ملف واحد | git log -- index.html
git diff | الفرق غير المجهّز | git diff
git diff --staged | الفرق المجهّز | git diff --staged
git show | تفاصيل إيداع | git show HEAD
git blame | من كتب كل سطر | git blame index.html
```

```quiz
? أي أمر يعرض كل إيداع في سطر واحد؟
- git log --short
* git log --oneline
- git show --all

? الأمر git diff --staged يعرض التغييرات الجاهزة للإيداع القادم.
= true
```

# @lesson git-undo
title: التراجع
summary: restore و reset و revert و amend.
---
## قبل الإيداع

```bash
git restore index.html           # تجاهل تعديلاتك على الملف
git restore --staged index.html  # إخراج الملف من التجهيز
```

## تعديل آخر إيداع

```bash
git commit --amend -m "رسالة أوضح"
```

## التراجع عن إيداع منشور

`git revert` ينشئ إيداعًا جديدًا يعكس إيداعًا قديمًا، فلا يمسح التاريخ:

```bash
git revert a1b2c3d
```

## reset

`git reset` يرجع الفرع إلى إيداع سابق:

```bash
git reset --soft HEAD~1   # يلغي آخر إيداع ويبقي التغييرات جاهزة
git reset --hard HEAD~1   # يلغي آخر إيداع ويمسح التغييرات
```

:::danger احذر من reset --hard
يمسح التغييرات نهائيًا. ولا تستخدم `reset` على إيداعات شاركتها مع الآخرين؛ استخدم `revert` بدلًا منه.
:::

```quiz
? أي أمر يتراجع عن إيداع منشور دون مسح التاريخ؟
- git reset --hard
* git revert
- git restore

? الأمر git commit --amend يعدّل آخر إيداع.
= true
```

# @lesson git-ignore
title: ملف ‎.gitignore
summary: استبعاد الملفات التي لا مكان لها في المستودع.
---
بعض الملفات لا يجب حفظها: ملفات مؤقتة، مكتبات يمكن تنزيلها، إعدادات فيها كلمات سر. اكتب أنماطها في ملف `.gitignore` في جذر المشروع:

```text
# المكتبات
node_modules/
__pycache__/

# ملفات البيئة وكلمات السر
.env
*.key

# ملفات النظام والمحرر
.DS_Store
.vscode/

# ملفات السجل
*.log
```

- `*` تطابق أي حروف: `*.log` كل ملفات السجل.
- `/` في النهاية تعني مجلدًا.
- `!` تستثني: `!important.log`.

:::warning ملف سبق حفظه
`.gitignore` لا يؤثر على ملف موجود في المستودع بالفعل. أخرجه أولًا: `git rm --cached .env`.
:::

```exercise bash
? أكمل النمط لاستبعاد كل ملفات log
___.log
= *
```

```quiz
? أين يوضع ملف .gitignore عادة؟
* في جذر المشروع
- داخل المجلد .git
- على GitHub فقط

? الملف .gitignore يستبعد تلقائيًا ملفًا سبق حفظه في المستودع.
= false
```

# @lesson git-branches
title: الفروع
summary: إنشاء الفروع والتنقل بينها.
---
**الفرع** يسمح لك بالعمل على ميزة جديدة دون المساس بالنسخة المستقرة في `main`:

```bash
git branch                    # عرض الفروع
git switch -c contact-form    # إنشاء فرع والانتقال إليه
# ... عدّل واحفظ ...
git add .
git commit -m "إضافة نموذج التواصل"
git switch main               # العودة للفرع الرئيسي
```

```reference bash
git branch | عرض الفروع | git branch
git branch اسم | إنشاء فرع | git branch fix-login
git switch اسم | الانتقال لفرع | git switch fix-login
git switch -c اسم | إنشاء وانتقال | git switch -c new-page
git branch -d اسم | حذف فرع مدموج | git branch -d fix-login
git branch -m جديد | إعادة تسمية الفرع | git branch -m main
```

:::tip فرع لكل مهمة
اجعل لكل ميزة أو إصلاح فرعًا باسم واضح مثل `fix-login-error`؛ هكذا يبقى `main` جاهزًا للنشر دائمًا.
:::

```exercise bash
? أنشئ فرعًا اسمه new-page وانتقل إليه
git switch ___ new-page
= -c
```

```quiz
? أي أمر ينقلك إلى فرع موجود؟
* git switch
- git move
- git go

? العمل في فرع جديد لا يغيّر الفرع main حتى تدمجه.
= true
```

# @lesson git-merge
title: الدمج
summary: دمج فرع في main، والدمج السريع والدمج بإيداع.
---
بعد انتهاء الميزة، ادمج فرعها في `main`:

```bash
git switch main
git merge contact-form
git branch -d contact-form
```

## نوعان من الدمج

- **سريع** (fast-forward): إذا لم يتغيّر `main` منذ إنشاء الفرع، يتقدم `main` ببساطة إلى آخر إيداع في الفرع.
- **بإيداع دمج**: إذا تغيّر الفرعان، ينشئ Git إيداعًا جديدًا يجمعهما.

```bash
git log --oneline --graph --all
```

يعرض شكل الفروع والدمج كرسم.

```quiz
? أين تكون عندما تكتب git merge contact-form؟
* في الفرع الذي تريد الدمج فيه (مثل main)
- في الفرع contact-form
- لا يهم

? الدمج السريع fast-forward لا ينشئ إيداع دمج.
= true
```

# @lesson git-conflicts
title: حل التعارضات
summary: لماذا يحدث التعارض وكيف تحله خطوة بخطوة.
---
يحدث **التعارض** عندما يعدّل فرعان نفس السطر بطريقتين مختلفتين، فلا يعرف Git أيهما يأخذ:

```text
<<<<<<< HEAD
<h1>أهلًا بكم</h1>
=======
<h1>مرحبًا بالزوار</h1>
>>>>>>> new-title
```

- ما بين `<<<<<<< HEAD` و `=======` هو نسختك الحالية.
- ما بين `=======` و `>>>>>>>` هو نسخة الفرع الآخر.

## خطوات الحل

1. افتح الملف واختر النسخة الصحيحة أو اجمعهما.
2. احذف علامات `<<<<<<<` و `=======` و `>>>>>>>`.
3. احفظ ثم:

```bash
git add index.html
git commit
```

للإلغاء والعودة لما قبل الدمج: `git merge --abort`.

:::tip قلّل التعارضات
ادمج `main` في فرعك كثيرًا، واجعل الفروع قصيرة العمر، وتواصل مع فريقك عن الملفات التي تعملون عليها.
:::

```quiz
? ماذا تفعل بعد تعديل الملف المتعارض؟
- git merge مرة أخرى
* git add ثم git commit
- git reset --hard

? الأمر git merge --abort يلغي الدمج ويعيدك لما قبله.
= true
```

# @lesson git-remote
title: GitHub والمستودعات البعيدة
summary: clone و push و pull و fetch.
---
## نسخ مستودع موجود

```bash
git clone https://github.com/user/project.git
```

## ربط مستودعك المحلي بـ GitHub

بعد إنشاء مستودع فارغ على GitHub:

```bash
git remote add origin https://github.com/user/my-site.git
git push -u origin main
```

## المزامنة اليومية

```bash
git pull           # جلب تغييرات الآخرين ودمجها
git push           # رفع إيداعاتك
git fetch          # جلب التغييرات دون دمج
```

```reference bash
git clone | نسخ مستودع | git clone URL
git remote -v | عرض المستودعات البعيدة | git remote -v
git remote add | إضافة مستودع بعيد | git remote add origin URL
git push | رفع الإيداعات | git push origin main
git pull | جلب ودمج | git pull
git fetch | جلب دون دمج | git fetch origin
```

:::info الاسم origin
`origin` الاسم المعتاد للمستودع البعيد الرئيسي. يمكنك تسميته كما تشاء، لكن هذا الاسم متعارف عليه.
:::

```exercise bash
? ارفع إيداعاتك إلى الفرع main على origin
git ___ origin main
= push
```

```quiz
? ما الفرق بين git fetch و git pull؟
* fetch يجلب فقط، و pull يجلب ويدمج
- لا فرق
- pull يرفع و fetch يجلب

? الأمر git clone ينسخ مستودعًا بعيدًا إلى جهازك.
= true
```

# @lesson git-workflow
title: العمل مع فريق
summary: الفروع وطلبات الدمج ومراجعة الكود.
---
سير العمل الشائع على GitHub:

1. حدّث `main`: `git switch main` ثم `git pull`.
2. أنشئ فرعًا للمهمة: `git switch -c fix-cart-total`.
3. اعمل واحفظ إيداعات صغيرة واضحة.
4. ارفع الفرع: `git push -u origin fix-cart-total`.
5. افتح **طلب دمج** (Pull Request) على GitHub.
6. يراجع زملاؤك الكود ويعلّقون، فتعدّل وترفع مرة أخرى.
7. بعد الموافقة يُدمج الطلب في `main`، وتحذف الفرع.

## Fork

لمشروع لا تملك صلاحية الكتابة فيه (مشروع مفتوح المصدر مثلًا): انسخه إلى حسابك بـ **Fork**، واعمل عليه، ثم افتح طلب دمج إلى المشروع الأصلي.

:::tip مراجعة الكود
طلب الدمج الصغير يُراجع بسرعة وبدقة. اكتب في وصفه ماذا تغيّر ولماذا وكيف تجرّبه.
:::

```quiz
? ما هو Pull Request؟
- أمر لجلب التغييرات
* طلب لدمج فرعك بعد مراجعته
- نسخة احتياطية

? تستخدم Fork لتساهم في مشروع لا تملك صلاحية الكتابة فيه.
= true
```

# @lesson git-reference
title: مرجع Git
summary: أهم الأوامر مع مثال لكل أمر.
type: Reference
---
ابحث في الجدول عن أي أمر.

```reference bash
git init | إنشاء مستودع | git init
git clone | نسخ مستودع | git clone URL
git status | حالة الملفات | git status
git add | تجهيز التغييرات | git add .
git commit | حفظ إيداع | git commit -m "رسالة"
git log | التاريخ | git log --oneline
git diff | الفروقات | git diff --staged
git show | تفاصيل إيداع | git show HEAD
git restore | تجاهل تعديلات | git restore file
git reset | إرجاع الفرع | git reset --soft HEAD~1
git revert | عكس إيداع | git revert a1b2c3d
git branch | الفروع | git branch -d old
git switch | التنقل بين الفروع | git switch -c new
git merge | الدمج | git merge feature
git stash | تخبئة مؤقتة | git stash / git stash pop
git remote | المستودعات البعيدة | git remote -v
git push | الرفع | git push -u origin main
git pull | الجلب والدمج | git pull
git fetch | الجلب فقط | git fetch
git tag | وسم إصدار | git tag v1.0.0
git config | الإعدادات | git config --global user.name "…"
```

:::tip ماذا بعد؟
أنشئ مستودعًا لأحد مشاريعك من الدورات السابقة، وارفعه على GitHub، وجرّب فرعًا وطلب دمج.
:::
