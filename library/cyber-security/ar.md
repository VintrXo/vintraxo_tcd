# @lesson sec-intro
title: لماذا الأمن مسؤولية الجميع
summary: السرية والسلامة والتوافر، والتهديدات الشائعة، والعامل البشري.
---
يحمي الأمن ثلاثة أشياء تُسمى غالبًا **مثلث CIA**:

| الهدف | المعنى | يُكسر عندما... |
|---|---|---|
| **السرية** | لا يرى البيانات إلا الأشخاص المناسبون | تتسرب سجلات العملاء |
| **السلامة** | البيانات صحيحة ولم تُغيَّر سرًا | يغيّر شخص رقم الحساب البنكي في فاتورة |
| **التوافر** | الأنظمة تعمل وقت الحاجة | يقفل برنامج فدية كل الملفات |

معظم الحوادث لا تبدأ باختراق ذكي، بل تبدأ بـ **كلمة مرور مكررة**، أو **رسالة تصيّد**، أو **تحديث لم يُثبَّت**، أو **صلاحيات أكثر من اللازم**. ولهذا فهذه الدورة للجميع وليست لقسم تقنية المعلومات فقط.

```try python
# فحص سريع: كم عادة جيدة لديك بالفعل؟
habits = {
    "كلمة مرور مختلفة لكل حساب": True,
    "مدير كلمات مرور": False,
    "التحقق بخطوتين للبريد": True,
    "تحديثات تلقائية للحاسوب والهاتف": True,
    "الإبلاغ عن الرسائل المشبوهة": False,
}
score = sum(habits.values())
print(f"{score} من {len(habits)} عادات")
for habit, done in habits.items():
    print(("  ✔ تم       " if done else "  ✘ للتنفيذ  ") + habit)
```

غيّر قيم `True` و `False` لتطابق عاداتك وشغّل الكود مرة أخرى.

```quiz
? غيّر مجرم رقم الحساب البنكي في فاتورة مورّد. أي هدف كُسر؟
* السلامة
- السرية
- التوافر

? تبدأ معظم الحوادث الأمنية بأدوات اختراق متقدمة لا بأخطاء بشرية.
= false
> معظمها يبدأ بأخطاء يومية: كلمات مرور ضعيفة أو مكررة، والتصيّد، والتحديثات الناقصة.
```

# @lesson sec-passwords
title: كلمات المرور القوية ومديرو كلمات المرور
summary: لماذا يتفوق الطول على التعقيد، وقياس القوة، وعدم تكرار كلمة المرور أبدًا.
---
لا يخمّن المهاجمون كلمات المرور واحدة واحدة يدويًا، بل يستخدمون قوائم كلمات مرور مسرّبة وحواسيب تجرّب **مليارات** التركيبات. والأهم هو **الطول** و**العشوائية**.

```try python
import math, secrets

def strength_bits(length, alphabet_size):
    return length * math.log2(alphabet_size)        # عدد بتات العشوائية لكلمة مرور عشوائية

for label, length, alphabet in [
    ("8 chars, letters+digits+symbols", 8, 94),
    ("12 chars, letters+digits", 12, 62),
    ("4 random common words", 4, 7776),             # عبارة مرور من قائمة 7776 كلمة
    ("6 random common words", 6, 7776),
]:
    bits = strength_bits(length, alphabet)
    years = 2 ** bits / 1e10 / 3600 / 24 / 365       # بمعدل 10 مليارات تخمين في الثانية
    print(f"{label:34} {bits:5.0f} bits  ~{years:.1e} years to try all")

words = ["river", "orange", "tiger", "cloud", "pencil", "garden", "planet", "silver", "window", "coffee"]
print("example passphrase:", "-".join(secrets.choice(words) for _ in range(5)))
```

تفترض الأرقام كلمة مرور **عشوائية** فعلًا. أما "Cairo2024!" فتبدو معقدة لكن تخمينها سهل لأن الناس يختارون هذه الأنماط باستمرار.

:::tip استخدم مدير كلمات مرور
مدير كلمات المرور (Bitwarden أو 1Password أو KeePassXC أو المدمج في متصفحك) ينشئ كلمة مرور طويلة عشوائية لكل موقع ويتذكرها. وأنت تحفظ عبارة مرور قوية واحدة فقط.
:::

:::danger لا تكرر كلمة المرور أبدًا
عندما يتسرب موقع، يجرّب المهاجمون نفس البريد وكلمة المرور على البريد والبنك وأنظمة العمل ("حشو بيانات الدخول"). وكلمة مرور فريدة لكل موقع توقف ذلك.
:::

```quiz
? أي كلمة مرور هي الأقوى؟
* عبارة من خمس كلمات عشوائية
- Cairo2024!
- P@ssw0rd123

? استخدام نفس كلمة المرور القوية في مواقع كثيرة آمن.
= false
> إذا سرّبها أي موقع منها يجرّبها المهاجمون في كل مكان.
```

# @lesson sec-hashing
title: كيف تحفظ الأنظمة كلمات المرور: التجزئة
summary: التجزئة مقابل التشفير، والملح، ودوال التجزئة البطيئة مثل bcrypt.
---
النظام المبني جيدًا لا يحفظ كلمة مرورك أبدًا، بل يحفظ **تجزئتها (hash)**: بصمة باتجاه واحد. وعند الدخول يجزّئ ما كتبته ويقارن البصمتين.

```try python
import hashlib, time, bcrypt

password = b"correct horse battery staple"

fast = hashlib.sha256(password).hexdigest()
print("SHA-256       :", fast[:32], "...")
print("same input    :", hashlib.sha256(password).hexdigest() == fast)
print("one char off  :", hashlib.sha256(b"correct horse battery stapla").hexdigest()[:32], "...")

t = time.perf_counter()
for _ in range(20000):
    hashlib.sha256(password).digest()
per_sec = 20000 / (time.perf_counter() - t)
print(f"SHA-256 speed : ~{per_sec:,.0f} guesses per second here (attackers' GPUs: billions)")

t = time.perf_counter()
stored = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))   # الملح العشوائي مضمَّن
print("bcrypt        :", stored.decode()[:29], "...")
print(f"bcrypt time   : {time.perf_counter() - t:.2f} s per guess, on purpose")
print("login ok      :", bcrypt.checkpw(password, stored))
print("wrong password:", bcrypt.checkpw(b"guess", stored))
print("same password hashed again looks different:", bcrypt.hashpw(password, bcrypt.gensalt(rounds=10)) != stored)
```

| | التجزئة | التشفير |
|---|---|---|
| الاتجاه | باتجاه واحد | باتجاهين (بمفتاح) |
| يُستخدم لـ | كلمات المرور وبصمات الملفات | بيانات تحتاج قراءتها مرة أخرى |
| مثال | bcrypt و Argon2 | AES و HTTPS |

- **الملح (salt)** قيمة عشوائية تُضاف لكل كلمة مرور قبل التجزئة، فيحصل شخصان بنفس كلمة المرور على تجزئتين مختلفتين، وتفقد الجداول المحسوبة مسبقًا قيمتها.
- يجب أن تكون تجزئة كلمات المرور **بطيئة** (bcrypt و scrypt و Argon2). أما التجزئة السريعة مثل SHA-256 فممتازة للملفات لكنها تتيح للمهاجم تجربة مليارات كلمات المرور في الثانية.

```quiz
? لماذا يجب أن تكون تجزئة كلمات المرور بطيئة؟
* لجعل تخمين ملايين كلمات المرور غير عملي
- لتوفير مساحة القرص
- ليقل انتظار المستخدمين

? يجعل الملح كلمتي مرور متطابقتين تعطيان تجزئتين مختلفتين.
= true
```

# @lesson sec-mfa
title: التحقق بخطوتين
summary: شيء تعرفه وشيء تملكه، وكيف تعمل رموز تطبيقات المصادقة.
---
**التحقق بخطوتين (2FA)** يطلب دليلًا ثانيًا إلى جانب كلمة المرور. فحتى لو تسربت كلمة مرورك، لا يستطيع مهاجم بلا هاتفك أو مفتاح الأمان الدخول.

تطبيقات المصادقة (Google Authenticator و Microsoft Authenticator و Authy) تستخدم **TOTP**: يتشارك هاتفك والخادم سرًا، ويحسب كل منهما رمزًا من 6 أرقام من هذا السر والوقت الحالي. الكود التالي هو الخوارزمية الحقيقية (RFC 6238)، مع فحصها بقيمة الاختبار في المعيار نفسه:

```try python
import hmac, hashlib, struct, time, base64

def totp(secret_b32, at=None, step=30, digits=6):
    key = base64.b32decode(secret_b32)
    counter = int((time.time() if at is None else at) // step)       # أي نافذة من 30 ثانية
    mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = mac[-1] & 0x0F
    number = struct.unpack(">I", mac[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(number % 10 ** digits).zfill(digits)

rfc_secret = base64.b32encode(b"12345678901234567890").decode()
print("RFC 6238 test (time 59):", totp(rfc_secret, at=59, digits=8), "(expected 94287082)")

my_secret = "JBSWY3DPEHPK3PXP"                     # السر داخل رمز QR الذي تمسحه
print("code right now         :", totp(my_secret))
print("code 30 seconds later  :", totp(my_secret, at=time.time() + 30))
```

| الطريقة | الحماية |
|---|---|
| رمز SMS | أفضل من لا شيء؛ ويمكن سرقته بتبديل شريحة الهاتف |
| تطبيق مصادقة (TOTP) | جيدة |
| موافقة بإشعار | جيدة، لكن احذر من سيل طلبات "موافق" |
| مفتاح أمان / مفتاح مرور (passkey) | الأفضل: يقاوم التصيّد |

:::warning لا تشارك رمزًا أبدًا
لا يطلب منك أي بنك أو فريق تقنية أو شركة توصيل حقيقية أن تقرأ رمزًا وصلك للتو. ومن يطلبه يحاول الدخول باسمك.
:::

```quiz
? اتصل بك شخص "من قسم التقنية" وطلب الرمز المكوّن من 6 أرقام الذي وصلك للتو. ماذا تفعل؟
* أرفض وأنهي المكالمة وأبلغ عنها
- أقرأ الرمز لأنه من قسم التقنية
- أرسله بالبريد بدلًا من ذلك

? يتغير رمز TOTP كل 30 ثانية تقريبًا.
= true
```

# @lesson sec-phishing
title: التعرّف على التصيّد
summary: علامات رسائل التصيّد، وفحص الروابط، وماذا تفعل.
---
**التصيّد (Phishing)** رسالة تتظاهر بأنها من جهة تثق بها لتجعلك تنقر رابطًا، أو تفتح ملفًا، أو تدفع، أو تعطي كلمة مرور. وتصل بالبريد أو SMS أو واتساب أو الهاتف.

العلامات التي تنتبه لها:

1. **الاستعجال أو التخويف**: "سيُغلق حسابك خلال 24 ساعة".
2. **عنوان مرسل شبه صحيح**: `support@micros0ft-help.com`.
3. **رابط يختلف عنوانه الحقيقي عن نصه.**
4. **مرفقات غير متوقعة**، خاصة `.zip` و `.html` و `.exe` أو ملفات Office تطلب "تفعيل المحتوى".
5. **طلبات دفع أو تغيير بيانات بنكية أو مشاركة رموز**، وغالبًا "من المدير العام".

نص الرابط التالي يقول شيئًا، لكن وجهته الحقيقية شيء آخر. مرّر الفأرة على الرابط (أو اضغط مطولًا على الجوال) لترى أين يذهب فعلًا:

```try html
<style>
  body { font: 15px/1.6 system-ui, sans-serif; }
  .mail { border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; max-width: 460px; }
  .from { color: #64748b; font-size: 13px; }
  #where { margin-top: 10px; font-family: monospace; color: #b91c1c; }
</style>
<div class="mail">
  <div class="from">من: مكتب الدعم الفني &lt;it-desk@company-support-portal.net&gt;</div>
  <p><b>عاجل: صندوق بريدك ممتلئ.</b> سجّل الدخول خلال ساعتين وإلا سيُحذف بريدك.</p>
  <p><a href="https://company-support-portal.net/login.php?u=you" id="link">https://mail.yourcompany.com/login</a></p>
</div>
<p id="where">مرّر الفأرة على الرابط لتظهر وجهته الحقيقية.</p>
<script>
  const link = document.getElementById("link");
  link.addEventListener("mouseover", () => (document.getElementById("where").textContent = "العنوان الحقيقي: " + link.href));
  link.addEventListener("click", (e) => { e.preventDefault(); document.getElementById("where").textContent = "لحسن الحظ هذه تجربة. العنوان الحقيقي: " + link.href; });
</script>
```

:::tip ماذا تفعل
لا تنقر ولا ترد. افتح الموقع الحقيقي بكتابة عنوانه بنفسك، أو اتصل بالشخص على رقم تعرفه مسبقًا. وأبلغ قسم التقنية بزر "الإبلاغ عن تصيّد" أو بإعادة توجيه الرسالة. وإذا نقرت بالفعل أو كتبت كلمة مرور فـ **أبلغ قسم التقنية فورًا** وغيّر كلمة المرور: السرعة أهم من الإحراج.
:::

```quiz
? وصلك بريد من "المدير العام" يطلب دفع مبلغ لمورّد جديد بسرعة وبسرية. ما أفضل تصرف؟
* التحقق بالاتصال بالمدير على رقم معروف قبل أي شيء
- الدفع بسرعة لأن الأمر عاجل
- الرد على البريد للسؤال إن كان حقيقيًا

? يُظهر تمرير الفأرة على الرابط وجهته الحقيقية.
= true
```

# @lesson sec-xss
title: أمن الويب: حقن السكربتات (XSS)
summary: كيف تتحول مدخلات المستخدم غير المؤمّنة إلى كود، وكيف يمنعها textContent والهروب.
---
يحدث **XSS** عندما يعرض موقع نصًا من مستخدم على أنه HTML. فيكتب المهاجم سكربتًا بدل التعليق، ويعمل في متصفحات الزوار الآخرين حيث يستطيع سرقة الجلسات أو تغيير الصفحة.

```try html
<style>
  body { font: 15px system-ui, sans-serif; }
  .box { border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; margin: 8px 0; min-height: 24px; }
  .bad { border-color: #fca5a5; } .good { border-color: #86efac; }
</style>
<label>تعليق: <input id="c" size="40" value='دورة رائعة! <img src=x onerror="document.body.style.background=`#fecaca`">'></label>
<button id="post">Post</button>
<p><b>غير آمن</b> (innerHTML):</p><div class="box bad" id="unsafe"></div>
<p><b>آمن</b> (textContent):</p><div class="box good" id="safe"></div>
<script>
  document.getElementById("post").addEventListener("click", () => {
    const text = document.getElementById("c").value;
    document.getElementById("unsafe").innerHTML = text;    // يشغّل كود المهاجم (تصبح الصفحة حمراء)
    document.getElementById("safe").textContent = text;    // يعرضه كنص غير ضار
  });
</script>
```

اضغط **Post**: الصندوق غير الآمن يشغّل الكود المخفي (هنا يجعل الصفحة حمراء فقط؛ والهجوم الحقيقي يسرق البيانات)، بينما الصندوق الآمن يعرض النص فقط.

```reference html
el.textContent = text | إدراج نص المستخدم كنص | comment.textContent = input.value
innerHTML مع بيانات المستخدم | خطير: لا تستخدمه مع نص غير موثوق | (تجنّبه)
الهروب على الخادم | قوالب تهرّب افتراضيًا | {{ comment }} في Jinja يهرّب
Content-Security-Policy | قاعدة في المتصفح تمنع السكربتات المحقونة | script-src 'self'
HttpOnly cookies | لا تستطيع السكربتات قراءة ملف الجلسة | Set-Cookie: sid=...; HttpOnly
```

:::tip الدفاع بطبقات
هرّب المخرجات (`textContent` والهروب التلقائي في القوالب)، وتحقّق من المدخلات على الخادم، وأضف Content-Security-Policy. كل طبقة توقف هجمات تفوت الأخرى.
:::

```exercise javascript
? اعرض اسم المستخدم بأمان
nameEl.___ = userName;
= textContent
```

```quiz
? لماذا تُعد innerHTML خطيرة مع مدخلات المستخدم؟
* لأن أي HTML أو سكربت في المدخلات يصبح جزءًا من الصفحة وقد يعمل
- لأنها أبطأ من textContent
- لأنها لا تعرض النص العربي
```

# @lesson sec-sql-injection
title: أمن الويب: حقن SQL
summary: كيف يتيح بناء SQL من النصوص للمهاجم إعادة كتابة الاستعلام، والاستعلامات ذات المعاملات.
---
يحدث **حقن SQL** عندما تُلصق مدخلات المستخدم داخل أمر SQL. فيكتب المهاجم SQL بدل البيانات ويغيّر ما يفعله الاستعلام.

```try python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT, password_hash TEXT, is_admin INT)")
db.executemany("INSERT INTO users VALUES (?, ?, ?)", [("sara", "h1", 1), ("omar", "h2", 0)])

def login_unsafe(name):
    query = f"SELECT name, is_admin FROM users WHERE name = '{name}'"   # خطير
    print("  query:", query)
    return db.execute(query).fetchall()

def login_safe(name):
    return db.execute("SELECT name, is_admin FROM users WHERE name = ?", (name,)).fetchall()

attack = "x' OR '1'='1"
print("unsafe, normal input :", login_unsafe("omar"))
print("unsafe, attack input :", login_unsafe(attack))      # يرجع كل المستخدمين!
print("safe,   attack input :", login_safe(attack))         # يُعامل كاسم غريب: لا تطابق
```

في النسخة غير الآمنة، تحوّل المدخلات `x' OR '1'='1` الشرط إلى "الاسم هو x **أو 1 يساوي 1**"، وهذا صحيح لكل الصفوف. أما النسخة الآمنة فترسل القيمة منفصلة، فلا تقرؤها قاعدة البيانات كـ SQL أبدًا.

```reference python
cursor.execute(sql, params) | استعلام بمعاملات (علامات أماكن) | db.execute("... WHERE id = ?", (user_id,))
f"... '{value}' ..." | SQL مبني من نص: لا تستخدمه مع مدخلات المستخدم | (تجنّبه)
ORM (Django و SQLAlchemy و Frappe) | يبني استعلامات آمنة نيابة عنك | frappe.get_all("User", filters={"name": n})
أقل صلاحيات لمستخدم قاعدة البيانات | تقليل الضرر إن تسرب شيء | لا صلاحية DROP لمستخدم التطبيق
```

:::danger الهروب اليدوي لا يكفي
لا تحاول "تنظيف" علامات التنصيص بنفسك. استخدم دائمًا علامات الأماكن (`?` و `%s` و `:name`) أو ORM: فهي مصممة لتكون صحيحة في كل الحالات.
:::

```exercise python
? أكمل الاستعلام الآمن بعلامة مكان
db.execute("SELECT * FROM users WHERE email = ___", (email,))
= ?
```

```quiz
? ما الذي يمنع حقن SQL بشكل موثوق؟
* الاستعلامات ذات المعاملات (علامات الأماكن) أو ORM
- حذف المسافات من المدخلات
- كتابة كلمات SQL بأحرف صغيرة
```

# @lesson sec-encryption
title: التشفير و HTTPS
summary: التشفير المتماثل والتشفير بالمفتاح العام، وما يحميه HTTPS، وتشفير ملف.
---
**التشفير** يحوّل البيانات المقروءة إلى بيانات غير مقروءة لا يعيدها إلا من يملك المفتاح.

- **التشفير المتماثل** يستخدم **المفتاح نفسه** للقفل والفتح (سريع؛ يُستخدم للملفات والأقراص).
- **التشفير بالمفتاح العام** يستخدم **زوجًا**: مفتاح عام يستطيع أي شخص القفل به، ومفتاح خاص لا يملكه إلا صاحبه للفتح. ويتيح لغرباء الاتفاق على سر بأمان، وهكذا يبدأ HTTPS.

```try python
from cryptography.fernet import Fernet, InvalidToken

key = Fernet.generate_key()                 # احفظه سرًا، مثلًا في مدير كلمات مرور أو خزنة
box = Fernet(key)

secret = "Salary file: Sara 32000, Omar 21000".encode()
token = box.encrypt(secret)
print("encrypted:", token[:48], b"...")
print("decrypted:", box.decrypt(token).decode())

try:
    Fernet(Fernet.generate_key()).decrypt(token)   # المفتاح الخاطئ
except InvalidToken:
    print("wrong key: cannot decrypt")

tampered = token[:-4] + b"AAAA"
try:
    box.decrypt(tampered)
except InvalidToken:
    print("tampered data is detected and rejected")
```

**HTTPS** (القفل) يشفّر الاتصال بين متصفحك والموقع، ويثبت هوية الموقع بشهادة. وهو يحمي بياناتك **في الطريق**، مثلًا على شبكة مقهى. لكنه **لا** يعني أن الموقع نفسه صادق: مواقع التصيّد تستخدم HTTPS أيضًا.

:::tip شفّر الأجهزة
فعّل تشفير القرص بالكامل (BitLocker في Windows و FileVault في macOS، وهو افتراضي في الهواتف الحديثة) حتى لا يعني فقدان حاسوب محمول تسرب البيانات.
:::

```quiz
? ماذا يثبت القفل (HTTPS) في المتصفح؟
* أن الاتصال مشفّر وأن الشهادة تطابق العنوان
- أن الموقع صادق وجدير بالثقة
- أن الموقع بلا فيروسات

? في التشفير المتماثل يشفّر المفتاح نفسه ويفك التشفير.
= true
```

# @lesson sec-access
title: التحكم في الصلاحيات ومبدأ أقل صلاحية
summary: أعطِ كل شخص الصلاحيات التي يحتاجها فقط، وراجعها، وألغِها في وقتها.
---
**مبدأ أقل صلاحية** يعني أن كل شخص وكل برنامج يحصل فقط على الصلاحيات اللازمة لعمله، وللمدة اللازمة فقط. فإذا سُرق حساب يبقى الضرر صغيرًا.

```try python
ROLES = {
    "employee": {"read:own_profile", "read:courses"},
    "manager": {"read:own_profile", "read:courses", "read:team_reports"},
    "hr": {"read:own_profile", "read:courses", "read:all_profiles", "edit:salaries"},
}
users = {"sara": ["manager"], "omar": ["employee"], "nour": ["hr"], "old_intern": ["hr"]}
active = {"sara", "omar", "nour"}                       # old_intern غادر الشركة

def can(user, permission):
    return user in active and any(permission in ROLES[r] for r in users.get(user, []))

for user, perm in [("omar", "read:team_reports"), ("sara", "read:team_reports"),
                   ("nour", "edit:salaries"), ("old_intern", "edit:salaries")]:
    print(f"{user:11} {perm:18} -> {'مسموح' if can(user, perm) else 'مرفوض'}")

stale = [u for u in users if u not in active]
print("مراجعة الصلاحيات: ألغِ أدوار", stale)
```

عادات جيدة:

- امنح الصلاحيات حسب **الدور** لا شخصًا شخصًا.
- استخدم **حساب مسؤول** منفصلًا لأعمال الإدارة فقط.
- **راجع** الصلاحيات دوريًا وألغِها في يوم تغيير الوظيفة أو المغادرة.
- اقصر المجلدات والمستندات المشتركة على من يحتاجها.

```quiz
? متدرب يحتاج قراءة تقويم التدريب. ما الصلاحية التي يجب أن يحصل عليها؟
* قراءة تقويم التدريب فقط
- صلاحية مسؤول حتى لا يُمنع أبدًا
- نفس صلاحيات مديره

? يجب إلغاء صلاحيات الموظف في يوم مغادرته.
= true
```

# @lesson sec-updates-backups
title: التحديثات والنسخ الاحتياطي وبرامج الفدية
summary: التحديث السريع، وقاعدة 3-2-1 للنسخ الاحتياطي، واختبار الاسترجاع.
---
**برامج الفدية (Ransomware)** تشفّر ملفات المؤسسة وتطلب دفع مبلغ. وعادتان تهزمان معظمها: **التحديث السريع** (يستغل المهاجمون ثغرات معروفة)، و**نسخ احتياطية لا يصل إليها المهاجم**.

```try python
from datetime import date, timedelta

backups = [
    {"name": "Office NAS", "copy_of": "files", "offline": False, "offsite": False, "last": date(2026, 1, 20), "restore_tested": True},
    {"name": "Cloud backup", "copy_of": "files", "offline": False, "offsite": True, "last": date(2026, 1, 21), "restore_tested": False},
    {"name": "Monthly USB disk", "copy_of": "files", "offline": True, "offsite": False, "last": date(2025, 12, 1), "restore_tested": False},
]
today = date(2026, 1, 21)

copies = 1 + len(backups)                       # الأصل إضافة إلى كل نسخة احتياطية
media = len({b["name"] for b in backups})
print("3 نسخ:", copies >= 3, "| وسيطان مختلفان:", media >= 2,
      "| نسخة خارج الموقع:", any(b["offsite"] for b in backups), "| نسخة غير متصلة:", any(b["offline"] for b in backups))
for b in backups:
    age = (today - b["last"]).days
    warn = []
    if age > 7: warn.append(f"عمرها {age} يومًا")
    if not b["restore_tested"]: warn.append("لم يُختبر استرجاعها")
    print(f"{b['name']:17}", "سليمة" if not warn else "راجع: " + "، ".join(warn))
```

**قاعدة 3-2-1**: ثلاث نسخ من البيانات المهمة، على نوعين مختلفين من وسائط التخزين، ونسخة واحدة خارج الموقع. واليوم نضيف: نسخة واحدة على الأقل **غير متصلة أو غير قابلة للتعديل** حتى لا يشفّرها برنامج الفدية أيضًا، و**اختبار الاسترجاع**، لأن النسخة التي لا تستطيع استرجاعها ليست نسخة احتياطية.

:::tip حدّث كل شيء
فعّل التحديثات التلقائية لنظام التشغيل والمتصفح والتطبيقات على الحواسيب والهواتف، وأعد التشغيل عندما يُطلب منك: فكثير من التحديثات لا تعمل إلا بعده.
:::

```quiz
? إلامَ يرمز الرقم "1" في قاعدة 3-2-1 للنسخ الاحتياطي؟
* نسخة واحدة خارج الموقع
- نسخة احتياطية واحدة في السنة
- كلمة مرور واحدة لكل النسخ

? النسخة الاحتياطية التي لم يُختبر استرجاعها قد لا تعمل وقت الحاجة.
= true
```

# @lesson sec-incident
title: عندما يحدث خطأ
summary: التعرّف على الحادثة، والإبلاغ بسرعة، وما يجب ألا تفعله.
---
حتى الحريصون ينقرون رابطًا خاطئًا أحيانًا. والمهم ما يحدث بعدها. فمعظم المؤسسات تخسر من **التأخر في الإبلاغ** أكثر بكثير من الخطأ الأصلي.

```try python
signs = {
    "نقرت رابطًا وكتبت كلمة مروري": "high",
    "الحاسوب بطيء جدًا وأسماء الملفات غريبة": "high",
    "يتلقى زملائي رسائل لم أرسلها": "high",
    "نافذة منبثقة تقول إنني ربحت جائزة": "low",
    "فقدت هاتف العمل": "high",
}
for sign, level in signs.items():
    action = "أبلغ قسم التقنية الآن ولا تنتظر" if level == "high" else "أغلقها ولا تنقر، وأخبر قسم التقنية"
    print(f"- {sign}\n    -> {action}")

print("\nإلى أن يصل قسم التقنية: افصل الشبكة (أطفئ Wi-Fi) إذا كانت الملفات تُشفَّر،")
print("ولا تحذف الأدلة، وغيّر كلمة المرور من جهاز آخر، واكتب ما حدث ومتى.")
```

| افعل | لا تفعل |
|---|---|
| أبلغ فورًا حتى لو لم تكن متأكدًا | لا تخفِه بسبب الإحراج |
| افصل الجهاز الذي يشفّر الملفات عن الشبكة | لا تطفئه وتشغّله مرارًا ولا تمسحه |
| غيّر كلمات المرور من جهاز سليم | لا تدفع فدية ولا ترد على المهاجم |
| اكتب الأوقات وما رأيته | لا تحقق وحدك ولا تعيد توجيه البرنامج الخبيث |

```quiz
? نقرت رابطًا وكتبت كلمة مرورك ثم اكتشفت أنه مزيف. ماذا تفعل أولًا؟
* أبلغ قسم التقنية فورًا وغيّر كلمة المرور من جهاز سليم
- أنتظر لأرى إن حدث شيء سيئ
- أحذف البريد ولا أقول شيئًا

? الإبلاغ السريع عن الخطأ يقلل الضرر غالبًا.
= true
```

# @lesson sec-reference
title: مرجع الأمن السريع
summary: العادات والقواعد التقنية من هذه الدورة في صفحة واحدة.
---
| المجال | العادة |
|---|---|
| كلمات المرور | طويلة وعشوائية وفريدة لكل موقع، في مدير كلمات مرور |
| الدخول | تحقق بخطوتين في كل مكان، ولا تشارك الرموز أبدًا |
| البريد | افحص المرسل وعنوان الرابط، وأبلغ عن التصيّد |
| الأجهزة | تحديثات تلقائية، وقفل الشاشة، وتشفير القرص |
| البيانات | أقل صلاحية، والمشاركة مع من يحتاج فقط |
| النسخ الاحتياطي | 3-2-1، ونسخة غير متصلة، واختبار الاسترجاع |
| الحوادث | أبلغ بسرعة، وافصل الجهاز، ولا تخفِ شيئًا |

```reference python
bcrypt.hashpw / checkpw | حفظ كلمات المرور والتحقق منها | bcrypt.checkpw(pw, stored)
secrets.token_urlsafe | رموز عشوائية للروابط والمفاتيح | secrets.token_urlsafe(32)
db.execute(sql, params) | SQL آمن بعلامات الأماكن | db.execute("... = ?", (v,))
el.textContent | نص آمن في صفحات الويب | el.textContent = comment
Fernet(key).encrypt | تشفير متماثل | Fernet(key).decrypt(token)
hmac.new(key, msg, sha256) | التحقق من سلامة الرسائل | hmac.compare_digest(a, b)
```

:::tip الخطوة التالية
فعّل التحقق بخطوتين لبريد العمل والبريد الشخصي اليوم، وثبّت مدير كلمات مرور، وافحص إن ظهر بريدك في تسريب عبر موقع haveibeenpwned.com. وعلى المطورين قراءة OWASP Top 10.
:::

```quiz
? أي عادة واحدة تحميك أكثر إذا سرّب موقع كلمة مرورك؟
* كلمة مرور فريدة لكل موقع
- تغيير كلمة المرور كل أسبوع
- استخدام عنوان بريد أطول
```
