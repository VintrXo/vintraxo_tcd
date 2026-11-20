#!/usr/bin/env bash
# Install or update VintraXo TCD on a server that ALREADY runs a site with its own apps
# (no restore: nothing on that site is overwritten). Run from the bench folder on the server:
#
#   bash apps/vintraxo_tcd/deploy/install_on_existing.sh <site> [keys.json] [spaces-dir]
#   (first time, before the app is on the server: copy this file anywhere and run it from the bench folder)
#
#   1. backup of the site
#   2. app fetched (first time) or pulled, its Python packages installed (defusedxml, anthropic)
#   3. install-app (first time) or migrate, assets built
#   4. keys.json applied (optional), spaces imported from export_spaces (optional), readiness check
set -euo pipefail

SITE="${1:?site name}"; KEYS="${2:-}"; SPACES="${3:-}"
REPO="${TCD_REPO:-git@github.com:VintrXo/vintraxo_tcd.git}"; BRANCH="${TCD_BRANCH:-vintraxo}"
[ -f sites/apps.txt ] || { echo "Run this from the bench folder (frappe-bench)."; exit 1; }
[ -d "sites/$SITE" ] || { echo "Site $SITE not found."; exit 1; }
step() { echo; echo "=== $*"; }

step "1) backup"
bench --site "$SITE" backup --with-files

step "2) app code"
if [ -d apps/vintraxo_tcd ]; then
  git -C apps/vintraxo_tcd pull --ff-only
else
  bench get-app --skip-assets --branch "$BRANCH" "$REPO"
fi
bench setup requirements --python vintraxo_tcd
./env/bin/python -c "import defusedxml, anthropic" || { echo "Python packages missing after install."; exit 1; }

step "3) install / migrate"
if bench --site "$SITE" list-apps 2>/dev/null | grep -q '^vintraxo_tcd'; then
  bench --site "$SITE" migrate
else
  bench --site "$SITE" install-app vintraxo_tcd
fi
bench build --app vintraxo_tcd
bench --site "$SITE" clear-cache

step "4) keys, content, readiness"
if [ -n "$KEYS" ]; then
  bench --site "$SITE" execute vintraxo_tcd.core.server_keys.apply_keys --kwargs "{'path': '$(realpath "$KEYS")'}"
fi
if [ -n "$SPACES" ]; then
  bench --site "$SITE" execute vintraxo_tcd.core.move.import_spaces --kwargs "{'in_dir': '$(realpath "$SPACES")'}"
fi
bench --site "$SITE" execute vintraxo_tcd.core.ops.print_readiness
echo
echo "Restart the server processes now:  bench restart   (production: sudo supervisorctl restart all)"
