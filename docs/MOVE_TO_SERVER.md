# النقل من السيرفر الداخلي إلى السيرفر الحقيقي

الهدف: السيرفر الحقيقي يبقى نسخة من `erpnext.localhost` بكل بياناته (المحتوى، الدورات، المستخدمين، الإعدادات)، من غير ما نعيد بناء حاجة.
كل الأدوات في فولدر `apps/vintraxo_tcd/deploy/` (القرار في `docs/adr/0034-move-kit-and-keys-file.md`).

**الملخص: 4 أوامر + ملف مفاتيح واحد.**

| الخطوة | فين | الأمر |
|---|---|---|
| 1 | السيرفر الداخلي | `bash apps/vintraxo_tcd/deploy/export_internal.sh erpnext.localhost` |
| 2 | السيرفر الجديد (مرة واحدة) | `bash install_prereqs.sh` ثم `sudo mariadb-secure-installation` |
| 3 | السيرفر الجديد | املا `keys.json` من `keys.example.json` |
| 4 | السيرفر الجديد | `setup_server.sh <الحزمة> <الدومين> keys.json --production` |

## 1) على السيرفر الداخلي: اعمل الحزمة
من فولدر `frappe-bench`:
```bash
bash apps/vintraxo_tcd/deploy/export_internal.sh erpnext.localhost ~/vintraxo-move --dry-run   # يعرض بس
bash apps/vintraxo_tcd/deploy/export_internal.sh erpnext.localhost ~/vintraxo-move
```
بيطلع ملف واحد `~/vintraxo-move/vintraxo-move-<التاريخ>.tar.gz` فيه:
- `manifest.tsv`: كل تطبيق برابطه وفرعه والـ commit بالظبط، فالسيرفر الجديد بيبقى مطابق.
- `apps/`: تطبيقاتكم (`vintraxo_*`) زي ما هي على الجهاز، بـ `.git` والشغل اللي ما اتعملوش commit. فـ `vintraxo_restaurant` و`vintraxo_pos` و`vintraxo_arabic` بيتنقلوا حتى لو مش على GitHub.
- `patches/`: التعديلات المحلية جوه التطبيقات الأصلية (ترجمات `ar.po` في frappe وerpnext وhrms، و`pdf_on_submit`، و`arabic_translations`)، وبتترجع على السيرفر أوتوماتيك.
- `backup/`: قاعدة البيانات، الملفات العامة والخاصة، و`site_config_backup.json` (فيه `encryption_key`).

**الحزمة فيها قاعدة البيانات ومفتاح التشفير: متبعتهاش بالإيميل.** انقلها بـ `scp` بس:
```bash
scp ~/vintraxo-move/vintraxo-move-*.tar.gz <user>@<server>:~/
scp apps/vintraxo_tcd/deploy/{install_prereqs.sh,setup_server.sh,keys.example.json} <user>@<server>:~/
```

## 2) على السيرفر الجديد: البرامج الأساسية (مرة واحدة)
السيرفر: Ubuntu 24.04 LTS، 4 أنوية و8 جيجا رام على الأقل، 80 جيجا مساحة، ودومين موجّه لـ IP السيرفر (مثلًا `erp.vintraxo.com`).
ادخل بمستخدم عادي عنده sudo (مش root):
```bash
bash install_prereqs.sh            # MariaDB 10.11, Redis, nginx, supervisor, Node 24, Python 3.14, bench
sudo mariadb-secure-installation   # حدد كلمة سر root لقاعدة البيانات
```
اخرج وادخل تاني بعدها.

## 3) ملف المفاتيح
```bash
cp keys.example.json keys.json && chmod 600 keys.json && nano keys.json
```
املا اللي عندك بس. أي قيمة فاضية أو لسه بتبدأ بـ `REPLACE` بتتساب، فتقدر تكمّل الملف بعدين وتشغله تاني.

| القسم | لازمته |
|---|---|
| `email` | البريد الصادر (Gmail: `smtp.gmail.com` و587 وApp Password) |
| `ai` | مفتاح الذكاء الاصطناعي (Anthropic) والموديل والميزانية الشهرية |
| `runner` | سيرفر Judge0 للغات Java وC# وغيرهم (اختياري، `PHASE10_ISOLATION_DESIGN.md`) |
| `zoom` أو `google_meet` | الاجتماعات الأونلاين |
| `payment` | اسم بوابة الدفع. مفاتيح البوابة نفسها تتحط في `documents` |
| `github` | مزامنة صفحات مساحة مع مستودع GitHub (لكل مساحة) |
| `documents` | أي إعدادات لتطبيق تاني بأسماء الحقول اللي في الديسك (مثلًا Stripe Settings وGoogle Settings) |
| `trial_accounts` | `"disable"` بيقفل حسابات التجربة (learner1..3، author، instructor) |

السكربت بيكتب أسماء الحقول اللي اتحطت، ومش بيكتب قيمها. كلمات السر بتتحفظ مشفّرة.

## 4) بناء السيرفر
```bash
DB_ROOT_PASSWORD='<كلمة سر root بتاعة MariaDB>' ADMIN_PASSWORD='<كلمة سر قوية جديدة للأدمن>' \
  bash setup_server.sh vintraxo-move-<التاريخ>.tar.gz erp.vintraxo.com keys.json --production
```
السكربت بيعمل لوحده، وبيقف عند أول خطأ:
1. `bench init` بنفس commit بتاع Frappe.
2. كل تطبيق على الـ commit بتاعه، أو بيتفك من الحزمة، والتعديلات المحلية بترجع. بعدها `bench setup requirements` و`build` و`setup-chrome` (لطباعة الشهادات PDF).
3. موقع جديد، ونقل `encryption_key` وباقي إعدادات `site_config` (ماعدا بيانات دخول قاعدة البيانات)، واسترجاع النسخة، و`migrate`.
4. `host_name` و`developer_mode 0`، وتشغيل الـ scheduler، وكلمة سر جديدة للأدمن.
5. تطبيق `keys.json` وبعده فحص الجاهزية.
6. مع `--production`: nginx وsupervisor، ونسخ احتياطية أوتوماتيك (cron)، وشهادة SSL من Let's Encrypt.

لو عايز تغيّر مفتاح بعدين، عدّل `keys.json` وشغّل:
```bash
cd ~/frappe-bench
bench --site erp.vintraxo.com execute vintraxo_tcd.core.server_keys.apply_keys --kwargs "{'path': '/home/<user>/keys.json'}"
```

## 5) بعد التشغيل
1. من الديسك: **إعدادات التعلّم ← فحص الجاهزية**. لازم مفيش «مشكلة» حمرا.
2. تجربة سريعة: تسجيل دخول متعلم، `/learn`، درس فيه محرر أكواد، الاستوديو لمؤلف، شهادة ورابط التحقق `/verify/...`، طباعة PDF للشهادة.
3. احفظ الحزمة في مكان آمن (مش على السيرفر)، وبعدين امسحها من السيرفر.

## 6) تحديثات بعد كده
```bash
cd ~/frappe-bench
git -C apps/vintraxo_tcd pull        # محتاج deploy key للمستودع الخاص
bench --site erp.vintraxo.com backup
bench --site erp.vintraxo.com migrate
bench build --app vintraxo_tcd
sudo supervisorctl restart all
```

## مُستحسن (مش شرط للنقل)
الحزمة بتنقل كل حاجة حتى من غير الخطوات دي، بس هي بتسهّل التحديثات بعدين:
- اعمل مستودعات خاصة لـ `vintraxo_restaurant` و`vintraxo_pos`، واعمل commit للشغل اللي في `vintraxo_arabic`.
- انقل ترجمات `ar.po` من frappe وerpnext وhrms لتطبيق ترجمة خاص بيكم (زي `vintraxo_arabic`)، عشان أي `bench update` بيمسحها. لحد ما ده يحصل، `export_internal.sh` بيشيلها كـ patches.
- `vintraxo_smart_cart` مش متسطّب على أي موقع (مش في `apps.txt`)، فمش داخل في النقل.
