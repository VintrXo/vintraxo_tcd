# النقل من السيرفر الداخلي إلى السيرفر الحقيقي

الهدف: السيرفر الحقيقي يبقى نسخة من `erpnext.localhost` بكل بياناته (المحتوى، الدورات، المستخدمين، الإعدادات)، من غير ما نعيد بناء حاجة.
الطريقة: نبني bench جديد بنفس التطبيقات ونفس الإصدارات، ثم نسترجع نسخة احتياطية كاملة من الموقع.

> آخر تحديث للقائمة: 2026-11-20 (من `bench version` على السيرفر الداخلي).

## 0) قبل أي حاجة — مشاكل لازم تتحل على السيرفر الداخلي

| المشكلة | ليه مهمة | الحل |
|---|---|---|
| `vintraxo_restaurant` و `vintraxo_smart_cart` **مش في git** | مفيش طريقة نجيبهم على السيرفر الجديد بـ `get-app` | اعمل لكل واحد مستودع خاص على GitHub وارفعه (`git init` → commit → push) |
| `vintraxo_pos` **ملوش remote** | نفس المشكلة | اربطه بمستودع وارفع الفرع `Vintraxo` |
| `vintraxo_arabic` فيه **138 تعديل مش متعمّل لهم commit** | هيضيعوا | commit + push |
| تعديلات محلية على `ar.po` في frappe و erpnext و hrms | الترجمات دي هتضيع مع أي تحديث | انقلها لتطبيق ترجمة خاص بيكم (زي `vintraxo_arabic`) بدل تعديل التطبيقات الأصلية |
| `pdf_on_submit/hooks.py` و `arabic_translations/commands.py` متعدّلين | تعديل في كود تطبيق خارجي | يا إما fork بمستودع خاص، يا إما ننقل التعديل لتطبيق بتاعكم |

باقي الفروقات (yarn.lock، node_modules، ملفات frontend مبنية) ملهاش تأثير ومش محتاجة نقل.

## 1) مواصفات السيرفر
- Ubuntu 24.04 LTS، 4 أنوية و 8 جيجا رام على الأقل (السيرفر عليه ERPNext + HRMS + LMS + Wiki + Helpdesk + Insights…)، 80 جيجا مساحة.
- دومين موجّه للسيرفر (مثلًا `erp.vintraxo.com`) عشان شهادة SSL.
- (اختياري) سيرفر منفصل صغير لـ Judge0 لتشغيل أكواد Java/C#… — التصميم في `PHASE10_ISOLATION_DESIGN.md`.

## 2) تجهيز bench على السيرفر
اتبع خطوات تثبيت Frappe v16 الرسمية بنفس إصدارات السيرفر الداخلي: Ubuntu 24.04، MariaDB 10.11، Redis 7، Node 24، Python 3.14 (شهادات TCD بتتطبع بـ Chrome، فمش محتاجة wkhtmltopdf). بعدها:

```bash
bench init frappe-bench --frappe-branch version-16
cd frappe-bench
```

## 3) جلب التطبيقات بنفس الإصدارات
نفس الفرع، وبعدها نثبت على نفس الـ commit عشان السيرفر يطابق الداخلي بالظبط:

| التطبيق | المصدر | الفرع | commit |
|---|---|---|---|
| erpnext | https://github.com/frappe/erpnext | version-16 | 4048fb7 |
| hrms | https://github.com/frappe/hrms | version-16 | a4768b4 |
| payments | https://github.com/frappe/payments | version-16 | cca07d9 |
| lending | https://github.com/frappe/lending | version-16 | 06fc075 |
| banking | https://github.com/alyf-de/banking | version-16 | 0540e61 |
| education | https://github.com/frappe/education | version-16 | 22e0910 |
| healthcare | https://github.com/frappe/healthcare | version-16 | dda107b |
| ecommerce_integrations | https://github.com/frappe/ecommerce_integrations | version-16 | 0f6b39b |
| frappe_slack_connector | https://github.com/rtCamp/frappe-slack-connector | version-16 | f2b8b7c |
| posawesome | https://github.com/WaleedAboHashima/POSAWESOME-16 | version-16 | 2ae40dd |
| lms | https://github.com/frappe/lms | develop | f4f546b |
| wiki | https://github.com/frappe/wiki | develop | 5bba767 |
| builder | https://github.com/frappe/builder | develop | deae7bb |
| crm | https://github.com/frappe/crm | develop | 79aaaca |
| helpdesk | https://github.com/frappe/helpdesk | develop | c0017a4 |
| insights | https://github.com/frappe/insights | develop | 8bff1a9 |
| gameplan | https://github.com/frappe/gameplan | develop | 99fb377 |
| telephony | https://github.com/frappe/telephony | develop | 039cf39 |
| whatsapp | https://github.com/frappe/whatsapp | develop | cd2b324 |
| webshop | https://github.com/frappe/webshop | develop | 1a5239d |
| erpnext_shipping | https://github.com/frappe/erpnext-shipping | develop | 6e0dc47 |
| ask_alyf | https://github.com/alyf-de/ask_alyf | develop | 2f8eef0 |
| pdf_on_submit | https://github.com/alyf-de/pdf_on_submit | develop | 70c2540 |
| ksa_compliance | https://github.com/lavaloon-eg/ksa_compliance | master | 24968b4 |
| storage_integration | https://github.com/frappe/storage_integration | master | bf9ec39 |
| arabic_translations | https://github.com/ibrahim317/erpnext-arabic-full-translation | develop | 7168aaf |
| vintraxo_arabic | https://github.com/abdulhamed100/vintraxo_arabic | main | d836e1a (+ التعديلات غير المحفوظة) |
| **vintraxo_tcd** | git@github.com:VintrXo/vintraxo_tcd.git | vintraxo | آخر commit |
| vintraxo_pos / vintraxo_restaurant / vintraxo_smart_cart | **لازم مستودعات أولًا (بند 0)** | | |

مثال لكل تطبيق:
```bash
bench get-app --branch version-16 https://github.com/frappe/erpnext
git -C apps/erpnext checkout 4048fb7
```
التطبيقات الخاصة (vintraxo_*) محتاجة مفتاح SSH للسيرفر (deploy key) على كل مستودع.

## 4) نسخة احتياطية كاملة من السيرفر الداخلي
```bash
bench --site erpnext.localhost backup --with-files
```
هتطلع 4 ملفات في `sites/erpnext.localhost/private/backups/`: قاعدة البيانات، الملفات العامة، الملفات الخاصة، و `site_config_backup.json`. انقلهم للسيرفر (scp).

## 5) إنشاء الموقع واسترجاع النسخة
```bash
bench new-site erp.vintraxo.com --admin-password '<كلمة سر قوية جديدة>'
bench --site erp.vintraxo.com restore <database.sql.gz> \
  --with-public-files <files.tar> --with-private-files <private-files.tar>
```
**مهم جدًا:** انسخ قيمة `encryption_key` من `site_config_backup.json` إلى `sites/erp.vintraxo.com/site_config.json` قبل أي حاجة؛ من غيرها كل كلمات السر والمفاتيح المحفوظة (البريد، Zoom، GitHub، الذكاء الاصطناعي، Judge0) مش هتتقري.
وانقل كمان مفاتيح vintraxo_* الخاصة بالمطعم و Firebase من نفس الملف لو محتاجها.

```bash
bench --site erp.vintraxo.com migrate
bench --site erp.vintraxo.com set-config host_name https://erp.vintraxo.com
bench --site erp.vintraxo.com set-config developer_mode 0
bench --site erp.vintraxo.com enable-scheduler
bench --site erp.vintraxo.com set-admin-password '<كلمة سر قوية>'
```

## 6) وضع الإنتاج
```bash
sudo bench setup production <user>     # nginx + supervisor (web, workers, scheduler)
bench setup backups                     # نسخ احتياطية تلقائية كل 6 ساعات (cron)
sudo bench setup lets-encrypt erp.vintraxo.com   # SSL
```

## 7) بعد التشغيل
1. من الديسك: **إعدادات التعلّم ← فحص الجاهزية**. لازم مفيش «مشكلة» حمرا. (أو `bench --site erp.vintraxo.com execute vintraxo_tcd.core.ops.print_readiness`)
2. حساب البريد الصادر (Email Account).
3. المفاتيح الاختيارية: الذكاء الاصطناعي، Zoom/Google، بوابة الدفع، GitHub، Judge0.
4. تجربة سريعة: تسجيل دخول متعلم، `/learn`، درس فيه محرر أكواد، الاستوديو لمؤلف، شهادة ورابط التحقق `/verify/...`، طباعة PDF للشهادة.
5. غيّر كلمات سر حسابات التجربة أو عطّلها (learner1..3, author, instructor).

## 8) تحديثات بعد كده
```bash
cd frappe-bench
git -C apps/vintraxo_tcd pull
bench --site erp.vintraxo.com backup
bench --site erp.vintraxo.com migrate
bench build --app vintraxo_tcd
sudo supervisorctl restart all
```
