# Odoo 18 documentation → two TCD spaces (English + Arabic)

Content: Odoo 18.0 user documentation, © Odoo S.A., **CC BY-SA 4.0** (github.com/odoo/documentation).
Every imported page keeps a source line with the original link and the licence. Decision: `docs/adr/0037-*.md`.

The tools only read data: Odoo's own Sphinx build is never run (it executes Python from the downloaded repo).

```bash
W=~/odoo-import && mkdir -p $W && cd $W
git clone --depth 1 --branch 18.0 https://github.com/odoo/documentation.git docs   # images (~800 MB)
T=~/frappe-bench/apps/vintraxo_tcd/deploy/odoo_docs
~/frappe-bench/env/bin/python -I $T/fetch.py $W          # article HTML from odoo.com, EN + AR (~1.5 h, polite)
~/frappe-bench/env/bin/python -I $T/fix_encoding.py $W/html   # only for pages saved before the UTF-8 fix
~/frappe-bench/env/bin/python -I $T/convert.py $W        # -> pages_en.json, pages_ar.json, images.json
cd ~/frappe-bench
export ODOO_LOAD="{\"root\": \"$W\", \"spaces\": {\"en\": \"odoo-en\", \"ar\": \"odoo-ar\"}}"
echo "exec(open('$T/load.py').read(), {'__name__': '__main__'})" | bench --site <site> console
```

Then one course per app (chapters = the app's sections, in Odoo's order; self-enrollment, progress tracked):

```bash
echo "exec(open('$HOME/frappe-bench/apps/vintraxo_tcd/deploy/odoo_docs/courses.py').read(), {'__name__': '__main__'})" | bench --site <site> console
```

Add `"only": ["applications/sales"]` to `ODOO_LOAD` for a trial with one area. A space that already exists is
skipped. To another server, move the spaces with `vintraxo_tcd.core.move.export_spaces` / `import_spaces` (the
images travel with them).
