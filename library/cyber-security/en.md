# @lesson sec-intro
title: Why security is everyone's job
summary: Confidentiality, integrity and availability, common threats, and the human factor.
---
Security protects three things, often called the **CIA triad**:

| Goal | Means | Broken when... |
|---|---|---|
| **Confidentiality** | Only the right people can see the data | Customer records leak |
| **Integrity** | Data is correct and not secretly changed | Someone edits an invoice's bank account |
| **Availability** | Systems work when needed | Ransomware locks every file |

Most incidents do not start with clever hacking. They start with a **reused password**, a **phishing email**, a **missing update** or **too much access**. That is why this course is for everyone, not only IT.

```try python
# a quick self-check: how many good habits do you already have?
habits = {
    "different password for every account": True,
    "password manager": False,
    "two-factor authentication on email": True,
    "automatic updates on laptop and phone": True,
    "report suspicious emails": False,
}
score = sum(habits.values())
print(f"{score} of {len(habits)} habits")
for habit, done in habits.items():
    print(("  done   " if done else "  to do  ") + habit)
```

Change the `True` / `False` values to match your own habits and run it again.

```quiz
? A criminal changes the bank account number on a supplier invoice. Which goal is broken?
* Integrity
- Confidentiality
- Availability

? Most security incidents start with advanced hacking tools rather than human mistakes.
= false
> Most begin with everyday mistakes: weak or reused passwords, phishing, missing updates.
```

# @lesson sec-passwords
title: Strong passwords and password managers
summary: Why length beats complexity, measuring strength, and never reusing passwords.
---
Attackers do not guess passwords one by one by hand. They use lists of leaked passwords and computers that try **billions** of combinations. What matters most is **length** and **randomness**.

```try python
import math, secrets

def strength_bits(length, alphabet_size):
    return length * math.log2(alphabet_size)        # bits of entropy for a random password

for label, length, alphabet in [
    ("8 chars, letters+digits+symbols", 8, 94),
    ("12 chars, letters+digits", 12, 62),
    ("4 random common words", 4, 7776),             # passphrase from a 7776-word list
    ("6 random common words", 6, 7776),
]:
    bits = strength_bits(length, alphabet)
    years = 2 ** bits / 1e10 / 3600 / 24 / 365       # at 10 billion guesses per second
    print(f"{label:34} {bits:5.0f} bits  ~{years:.1e} years to try all")

words = ["river", "orange", "tiger", "cloud", "pencil", "garden", "planet", "silver", "window", "coffee"]
print("example passphrase:", "-".join(secrets.choice(words) for _ in range(5)))
```

The numbers assume a truly **random** password. "Cairo2024!" looks complex but is easy to guess, because people choose such patterns all the time.

:::tip Use a password manager
A password manager (Bitwarden, 1Password, KeePassXC, or the one in your browser) creates and remembers a long random password for every site. You only memorise one strong passphrase.
:::

:::danger Never reuse passwords
When one site leaks, attackers try the same email and password on email, banking and work systems ("credential stuffing"). A unique password per site stops this.
:::

```quiz
? Which password is the strongest?
* A passphrase of five random words
- Cairo2024!
- P@ssw0rd123

? Using the same strong password on many sites is safe.
= false
> If any one site leaks it, attackers try it everywhere else.
```

# @lesson sec-hashing
title: How systems store passwords: hashing
summary: Hashing versus encryption, salts, and slow hashes such as bcrypt.
---
A well-built system never stores your password. It stores a **hash**: a one-way fingerprint. At login it hashes what you typed and compares fingerprints.

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
stored = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))   # random salt is included
print("bcrypt        :", stored.decode()[:29], "...")
print(f"bcrypt time   : {time.perf_counter() - t:.2f} s per guess, on purpose")
print("login ok      :", bcrypt.checkpw(password, stored))
print("wrong password:", bcrypt.checkpw(b"guess", stored))
print("same password hashed again looks different:", bcrypt.hashpw(password, bcrypt.gensalt(rounds=10)) != stored)
```

| | Hashing | Encryption |
|---|---|---|
| Direction | One way | Two way (with a key) |
| Used for | Passwords, file fingerprints | Data you need to read again |
| Example | bcrypt, Argon2 | AES, HTTPS |

- A **salt** is a random value added to each password before hashing, so two people with the same password get different hashes and pre-computed tables are useless.
- Password hashes must be **slow** (bcrypt, scrypt, Argon2). Fast hashes like SHA-256 are great for files but let attackers try billions of passwords per second.

```quiz
? Why should password hashing be slow?
* To make guessing millions of passwords impractical
- To save disk space
- So users wait less

? A salt makes two identical passwords produce different hashes.
= true
```

# @lesson sec-mfa
title: Two-factor authentication
summary: Something you know plus something you have, and how authenticator codes work.
---
**Two-factor authentication (2FA)** asks for a second proof besides the password. Even if your password leaks, an attacker without your phone or security key cannot log in.

Authenticator apps (Google Authenticator, Microsoft Authenticator, Authy) use **TOTP**: your phone and the server share a secret, and both compute a 6-digit code from that secret and the current time. The code below is the real algorithm (RFC 6238), checked against the standard's own test value:

```try python
import hmac, hashlib, struct, time, base64

def totp(secret_b32, at=None, step=30, digits=6):
    key = base64.b32decode(secret_b32)
    counter = int((time.time() if at is None else at) // step)       # which 30-second window
    mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = mac[-1] & 0x0F
    number = struct.unpack(">I", mac[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(number % 10 ** digits).zfill(digits)

rfc_secret = base64.b32encode(b"12345678901234567890").decode()
print("RFC 6238 test (time 59):", totp(rfc_secret, at=59, digits=8), "(expected 94287082)")

my_secret = "JBSWY3DPEHPK3PXP"                     # the secret inside the QR code you scan
print("code right now         :", totp(my_secret))
print("code 30 seconds later  :", totp(my_secret, at=time.time() + 30))
```

| Method | Protection |
|---|---|
| SMS code | Better than nothing; can be stolen by SIM swap |
| Authenticator app (TOTP) | Good |
| Push approval | Good, but beware of "approve" spam (MFA fatigue) |
| Security key / passkey | Best: resists phishing |

:::warning Never share a code
No real bank, IT team or delivery company will ask you to read out a code you just received. Anyone who asks is trying to log in as you.
:::

```quiz
? Someone calls "from IT" and asks for the 6-digit code you just received. What do you do?
* Refuse, hang up and report it
- Read the code because they are from IT
- Send it by email instead

? A TOTP code changes about every 30 seconds.
= true
```

# @lesson sec-phishing
title: Recognising phishing
summary: The signs of a phishing message, checking links, and what to do.
---
**Phishing** is a message that pretends to be someone you trust to make you click a link, open a file, pay or give a password. It arrives by email, SMS, WhatsApp or phone.

Signs to look for:

1. **Urgency or fear**: "your account will be closed in 24 hours".
2. **A sender address that is almost right**: `support@micros0ft-help.com`.
3. **A link whose real address differs from its text.**
4. **Unexpected attachments**, especially `.zip`, `.html`, `.exe` or Office files that ask to "enable content".
5. **Requests to pay, change bank details or share codes**, often "from the CEO".

The link text below says one thing, but the real destination is another. Move the mouse over a link (or long-press on a phone) to see where it really goes:

```try html
<style>
  body { font: 15px/1.6 system-ui, sans-serif; }
  .mail { border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; max-width: 460px; }
  .from { color: #64748b; font-size: 13px; }
  #where { margin-top: 10px; font-family: monospace; color: #b91c1c; }
</style>
<div class="mail">
  <div class="from">From: IT Service Desk &lt;it-desk@company-support-portal.net&gt;</div>
  <p><b>Urgent: your mailbox is full.</b> Sign in within 2 hours or your email will be deleted.</p>
  <p><a href="https://company-support-portal.net/login.php?u=you" id="link">https://mail.yourcompany.com/login</a></p>
</div>
<p id="where">Hover the link to reveal its real address.</p>
<script>
  const link = document.getElementById("link");
  link.addEventListener("mouseover", () => (document.getElementById("where").textContent = "Real address: " + link.href));
  link.addEventListener("click", (e) => { e.preventDefault(); document.getElementById("where").textContent = "Good thing this is a demo. Real address: " + link.href; });
</script>
```

:::tip What to do
Do not click or reply. Open the real website by typing its address yourself, or call the person on a number you already know. Report the message to IT with the "Report phishing" button or by forwarding it. If you already clicked or typed a password, **tell IT immediately** and change the password: speed matters more than embarrassment.
:::

```quiz
? An email from your "CEO" asks you to urgently pay a new supplier and keep it secret. What is the best action?
* Verify by calling the CEO on a known number before doing anything
- Pay quickly because it is urgent
- Reply to the email to ask if it is real

? Hovering over a link shows its real destination.
= true
```

# @lesson sec-xss
title: Web security: cross-site scripting (XSS)
summary: How unescaped user input becomes code, and how textContent and escaping prevent it.
---
**XSS** happens when a website shows text from a user as HTML. An attacker types a script instead of a comment, and it runs in other visitors' browsers, where it can steal sessions or change the page.

```try html
<style>
  body { font: 15px system-ui, sans-serif; }
  .box { border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; margin: 8px 0; min-height: 24px; }
  .bad { border-color: #fca5a5; } .good { border-color: #86efac; }
</style>
<label>Comment: <input id="c" size="40" value='Nice course! <img src=x onerror="document.body.style.background=`#fecaca`">'></label>
<button id="post">Post</button>
<p><b>Unsafe</b> (innerHTML):</p><div class="box bad" id="unsafe"></div>
<p><b>Safe</b> (textContent):</p><div class="box good" id="safe"></div>
<script>
  document.getElementById("post").addEventListener("click", () => {
    const text = document.getElementById("c").value;
    document.getElementById("unsafe").innerHTML = text;    // runs the attacker's code (the page turns red)
    document.getElementById("safe").textContent = text;    // shows it as harmless text
  });
</script>
```

Press **Post**: the unsafe box runs the hidden code (here it only turns the page red; a real attack would steal data), while the safe box simply shows the text.

```reference html
el.textContent = text | Insert user text as text | comment.textContent = input.value
innerHTML with user data | Dangerous: never with untrusted text | (avoid)
escape on the server | Templates that escape by default | {{ comment }} in Jinja escapes
Content-Security-Policy | Browser rule that blocks injected scripts | script-src 'self'
HttpOnly cookies | Scripts cannot read the session cookie | Set-Cookie: sid=...; HttpOnly
```

:::tip Defence in depth
Escape output (`textContent`, template auto-escaping), validate input on the server, and add a Content-Security-Policy. Each layer stops attacks the others miss.
:::

```exercise javascript
? Show the user's name safely
nameEl.___ = userName;
= textContent
```

```quiz
? Why is innerHTML dangerous with user input?
* Any HTML or script in the input becomes part of the page and can run
- It is slower than textContent
- It cannot display Arabic text
```

# @lesson sec-sql-injection
title: Web security: SQL injection
summary: How building SQL from strings lets attackers rewrite queries, and parameterized queries.
---
**SQL injection** happens when user input is glued into an SQL command. The attacker types SQL instead of data and changes what the query does.

```try python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT, password_hash TEXT, is_admin INT)")
db.executemany("INSERT INTO users VALUES (?, ?, ?)", [("sara", "h1", 1), ("omar", "h2", 0)])

def login_unsafe(name):
    query = f"SELECT name, is_admin FROM users WHERE name = '{name}'"   # DANGEROUS
    print("  query:", query)
    return db.execute(query).fetchall()

def login_safe(name):
    return db.execute("SELECT name, is_admin FROM users WHERE name = ?", (name,)).fetchall()

attack = "x' OR '1'='1"
print("unsafe, normal input :", login_unsafe("omar"))
print("unsafe, attack input :", login_unsafe(attack))      # returns every user!
print("safe,   attack input :", login_safe(attack))         # treated as a strange name: no match
```

With the unsafe version, the input `x' OR '1'='1` turns the condition into "name is x **or 1 equals 1**", which is true for every row. The safe version sends the value separately, so the database never reads it as SQL.

```reference python
cursor.execute(sql, params) | Parameterized query (placeholders) | db.execute("... WHERE id = ?", (user_id,))
f"... '{value}' ..." | String-built SQL: never with user input | (avoid)
ORM (Django, SQLAlchemy, Frappe) | Builds safe queries for you | frappe.get_all("User", filters={"name": n})
least privilege for the DB user | Limit damage if something slips | no DROP rights for the app user
```

:::danger Escaping by hand is not enough
Do not try to "clean" quotes yourself. Always use placeholders (`?`, `%s`, `:name`) or an ORM: they are designed to be correct in every case.
:::

```exercise python
? Complete the safe query with a placeholder
db.execute("SELECT * FROM users WHERE email = ___", (email,))
= ?
```

```quiz
? What reliably prevents SQL injection?
* Parameterized queries (placeholders) or an ORM
- Removing spaces from the input
- Writing SQL keywords in lower case
```

# @lesson sec-encryption
title: Encryption and HTTPS
summary: Symmetric and public-key encryption, what HTTPS protects, and encrypting a file.
---
**Encryption** turns readable data into unreadable data that only the holder of a key can turn back.

- **Symmetric** encryption uses the **same key** to lock and unlock (fast; used for files and disks).
- **Public-key** encryption uses a **pair**: a public key anyone can use to lock, and a private key only the owner has to unlock. It lets strangers agree on a secret safely, which is how HTTPS starts.

```try python
from cryptography.fernet import Fernet, InvalidToken

key = Fernet.generate_key()                 # keep this secret, e.g. in a password manager or vault
box = Fernet(key)

secret = "Salary file: Sara 32000, Omar 21000".encode()
token = box.encrypt(secret)
print("encrypted:", token[:48], b"...")
print("decrypted:", box.decrypt(token).decode())

try:
    Fernet(Fernet.generate_key()).decrypt(token)   # the wrong key
except InvalidToken:
    print("wrong key: cannot decrypt")

tampered = token[:-4] + b"AAAA"
try:
    box.decrypt(tampered)
except InvalidToken:
    print("tampered data is detected and rejected")
```

**HTTPS** (the padlock) encrypts traffic between your browser and the site, and proves the site's identity with a certificate. It protects your data **on the way**, for example on café Wi-Fi. It does **not** mean the site itself is honest: phishing sites use HTTPS too.

:::tip Encrypt devices
Turn on full-disk encryption (BitLocker on Windows, FileVault on macOS, the default on modern phones) so a lost laptop does not mean leaked data.
:::

```quiz
? What does the padlock (HTTPS) in the browser prove?
* The connection is encrypted and the certificate matches the address
- The website is honest and safe to trust
- The website has no viruses

? In symmetric encryption, the same key encrypts and decrypts.
= true
```

# @lesson sec-access
title: Access control and least privilege
summary: Give each person only the access they need, review it, and remove it on time.
---
**Least privilege** means every person and program gets only the access needed for their job, for only as long as needed. If an account is stolen, the damage stays small.

```try python
ROLES = {
    "employee": {"read:own_profile", "read:courses"},
    "manager": {"read:own_profile", "read:courses", "read:team_reports"},
    "hr": {"read:own_profile", "read:courses", "read:all_profiles", "edit:salaries"},
}
users = {"sara": ["manager"], "omar": ["employee"], "nour": ["hr"], "old_intern": ["hr"]}
active = {"sara", "omar", "nour"}                       # old_intern left the company

def can(user, permission):
    return user in active and any(permission in ROLES[r] for r in users.get(user, []))

for user, perm in [("omar", "read:team_reports"), ("sara", "read:team_reports"),
                   ("nour", "edit:salaries"), ("old_intern", "edit:salaries")]:
    print(f"{user:11} {perm:18} -> {'allowed' if can(user, perm) else 'denied'}")

stale = [u for u in users if u not in active]
print("access review: remove roles for", stale)
```

Good habits:

- Give access by **role**, not person by person.
- Use a separate **admin account** only for admin work.
- **Review** access regularly and remove it the day someone changes job or leaves.
- Lock shared folders and documents to the people who need them.

```quiz
? An intern needs to read the training calendar. What access should they get?
* Read access to the training calendar only
- Admin access so they are never blocked
- The same access as their manager

? Access should be removed on the day an employee leaves.
= true
```

# @lesson sec-updates-backups
title: Updates, backups and ransomware
summary: Patching quickly, the 3-2-1 backup rule, and testing restores.
---
**Ransomware** encrypts an organisation's files and demands payment. Two habits defeat most of it: **updating quickly** (attackers use known holes) and **backups that the attacker cannot reach**.

```try python
from datetime import date, timedelta

backups = [
    {"name": "Office NAS", "copy_of": "files", "offline": False, "offsite": False, "last": date(2026, 1, 20), "restore_tested": True},
    {"name": "Cloud backup", "copy_of": "files", "offline": False, "offsite": True, "last": date(2026, 1, 21), "restore_tested": False},
    {"name": "Monthly USB disk", "copy_of": "files", "offline": True, "offsite": False, "last": date(2025, 12, 1), "restore_tested": False},
]
today = date(2026, 1, 21)

copies = 1 + len(backups)                       # the original plus each backup
media = len({b["name"] for b in backups})
print("3 copies:", copies >= 3, "| 2 different media:", media >= 2,
      "| 1 offsite:", any(b["offsite"] for b in backups), "| 1 offline:", any(b["offline"] for b in backups))
for b in backups:
    age = (today - b["last"]).days
    warn = []
    if age > 7: warn.append(f"{age} days old")
    if not b["restore_tested"]: warn.append("restore never tested")
    print(f"{b['name']:17}", "OK" if not warn else "check: " + ", ".join(warn))
```

The **3-2-1 rule**: 3 copies of important data, on 2 different kinds of media, with 1 copy offsite. Today we add: at least one copy **offline or immutable**, so ransomware cannot encrypt it too, and **test restores**, because a backup you cannot restore is not a backup.

:::tip Update everything
Turn on automatic updates for the operating system, browser and apps on laptops and phones. Restart when asked: many updates only take effect after a restart.
:::

```quiz
? What does the "1" in the 3-2-1 backup rule stand for?
* One copy kept offsite
- One backup per year
- One password for all backups

? A backup that has never been test-restored may not work when you need it.
= true
```

# @lesson sec-incident
title: When something goes wrong
summary: Recognise an incident, report it fast, and what not to do.
---
Even careful people click the wrong link. What matters is what happens next. Most organisations lose far more from **late reporting** than from the original mistake.

```try python
signs = {
    "clicked a link and typed my password": "high",
    "laptop is very slow and files have strange names": "high",
    "colleagues receive emails I never sent": "high",
    "a pop-up says I won a prize": "low",
    "lost my work phone": "high",
}
for sign, level in signs.items():
    action = "report to IT NOW, do not wait" if level == "high" else "close it, do not click, mention it to IT"
    print(f"- {sign}\n    -> {action}")

print("\nWhile you wait for IT: disconnect from the network (Wi-Fi off) if files are being encrypted,")
print("do not delete evidence, change the password from ANOTHER device, write down what happened and when.")
```

| Do | Do not |
|---|---|
| Report immediately, even if unsure | Hide it out of embarrassment |
| Disconnect a device that is encrypting files | Turn it off and on repeatedly or wipe it |
| Change passwords from a clean device | Pay a ransom or reply to the attacker |
| Write down times and what you saw | Investigate alone or forward the malware |

```quiz
? You clicked a link and typed your password, then realised it was fake. What first?
* Report to IT immediately and change the password from a clean device
- Wait to see if anything bad happens
- Delete the email and say nothing

? Reporting a mistake quickly usually reduces the damage.
= true
```

# @lesson sec-reference
title: Security quick reference
summary: The habits and technical rules from this course on one page.
---
| Area | Habit |
|---|---|
| Passwords | Long, random, unique per site, in a password manager |
| Logins | Two-factor everywhere, never share codes |
| Email | Check sender and link address, report phishing |
| Devices | Automatic updates, screen lock, disk encryption |
| Data | Least privilege, share only with who needs it |
| Backups | 3-2-1, one offline copy, test restores |
| Incidents | Report fast, disconnect, do not hide |

```reference python
bcrypt.hashpw / checkpw | Store and verify passwords | bcrypt.checkpw(pw, stored)
secrets.token_urlsafe | Random tokens for links and keys | secrets.token_urlsafe(32)
db.execute(sql, params) | Safe SQL with placeholders | db.execute("... = ?", (v,))
el.textContent | Safe text in web pages | el.textContent = comment
Fernet(key).encrypt | Symmetric encryption | Fernet(key).decrypt(token)
hmac.new(key, msg, sha256) | Message authentication | hmac.compare_digest(a, b)
```

:::tip Where to go next
Turn on two-factor authentication for your work and personal email today, install a password manager, and check whether your email appeared in a breach at haveibeenpwned.com. Developers should read the OWASP Top 10.
:::

```quiz
? Which single habit protects you best if one website leaks your password?
* A unique password for every site
- Changing your password every week
- Using a longer email address
```
