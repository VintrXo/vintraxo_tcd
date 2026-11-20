#!/usr/bin/env bash
# Build the real server from the bundle made by export_internal.sh. Run as the normal user, in $HOME:
#
#   DB_ROOT_PASSWORD='...' ADMIN_PASSWORD='...' \
#     bash setup_server.sh vintraxo-move-XXXX.tar.gz erp.your-domain.com [keys.json] [--production]
#
# What it does (each step prints a title; it stops on the first error):
#   1. bench init with Frappe at the SAME commit as the internal server
#   2. every app at its commit (git) or unpacked from the bundle (our own apps), local edits re-applied
#   3. new site, encryption_key + extra settings copied, backup restored, migrate
#   4. host_name, developer_mode off, scheduler on, new Administrator password
#   5. keys.json applied (if given) + readiness check
#   6. with --production: nginx + supervisor, cron backups, SSL (Let's Encrypt)
set -euo pipefail

BUNDLE="${1:?bundle .tar.gz}"; DOMAIN="${2:?domain, e.g. erp.example.com}"
KEYS=""; PROD=0
for a in "${@:3}"; do
  case "$a" in --production) PROD=1 ;; *) KEYS="$(realpath "$a")" ;; esac
done
: "${DB_ROOT_PASSWORD:?set DB_ROOT_PASSWORD}"; : "${ADMIN_PASSWORD:?set ADMIN_PASSWORD}"
BENCH="${BENCH_DIR:-$HOME/frappe-bench}"
export PATH="$HOME/.local/bin:$PATH"
step() { echo; echo "=== $*"; }

step "Unpack bundle"
SRC="$(mktemp -d "$HOME/vintraxo-move.XXXX")"
tar -C "$SRC" -xzf "$BUNDLE"
SRC="$(echo "$SRC"/vintraxo-move-*)"
M="$SRC/manifest.tsv"
[ -f "$M" ] || { echo "manifest.tsv missing: not a bundle from export_internal.sh"; exit 1; }

pin() {  # app dir, branch, commit
  [ -n "$3" ] || return 0
  git -C "$1" fetch -q --depth 1 "$(git -C "$1" remote | head -1)" "$3"
  git -C "$1" checkout -q -B "$2" "$3"
}

step "1) bench init (Frappe pinned)"
IFS=$'\t' read -r _ _ furl fbranch fcommit < <(grep -P '^frappe\t' "$M")
if [ ! -d "$BENCH" ]; then
  bench init "$BENCH" --frappe-path "$furl" --frappe-branch "$fbranch" \
    --python "$(uv python find 3.14)" --skip-assets
fi
cd "$BENCH"
pin apps/frappe "$fbranch" "$fcommit"
[ -f "$SRC/patches/frappe.diff" ] && git -C apps/frappe apply --whitespace=nowarn "$SRC/patches/frappe.diff"

step "2) apps"
while IFS=$'\t' read -r app mode url branch commit; do
  [ "$app" = frappe ] && continue
  if [ -d "apps/$app" ]; then echo "  $app already here"; continue; fi
  if [ "$mode" = git ]; then
    echo "  $app <- $url ($branch @ ${commit:0:7})"
    bench get-app --skip-assets --branch "$branch" "$url"
    pin "apps/$app" "$branch" "$commit"
    [ -f "$SRC/patches/$app.diff" ] && git -C "apps/$app" apply --whitespace=nowarn "$SRC/patches/$app.diff"
  else
    echo "  $app <- bundle"
    tar -C apps -xzf "$SRC/apps/$app.tar.gz"
    grep -qx "$app" sites/apps.txt || echo "$app" >> sites/apps.txt
  fi
done < "$M"
bench setup requirements
bench build
bench setup-chrome || echo "  (setup-chrome failed: certificate PDFs need Chrome; run 'bench setup-chrome' later)"

step "3) site + restore"
OLD="$(cat "$SRC/site.txt")"
B="$SRC/backup"
DB="$(ls "$B"/*-database.sql.gz)"; PUB="$(ls "$B"/*-files.tar | grep -v private-files)"; PRIV="$(ls "$B"/*-private-files.tar)"
CONF="$(ls "$B"/*-site_config_backup.json)"
if [ ! -d "sites/$DOMAIN" ]; then
  bench new-site "$DOMAIN" --db-root-password "$DB_ROOT_PASSWORD" --admin-password "$ADMIN_PASSWORD"
fi
# keep the new database login; carry everything else (encryption_key first of all)
./env/bin/python - "$CONF" "sites/$DOMAIN/site_config.json" <<'PY'
import json, sys
old = json.load(open(sys.argv[1])); path = sys.argv[2]; new = json.load(open(path))
skip = {"db_name", "db_password", "db_type", "db_host", "db_port", "db_user", "db_socket",
        "host_name", "developer_mode", "maintenance_mode", "pause_scheduler", "allow_tests"}
carried = sorted(k for k in old if k not in skip)
new.update({k: old[k] for k in carried})
json.dump(new, open(path, "w"), indent=1, sort_keys=True)
print("  carried site settings:", ", ".join(carried))
PY
grep -q '"encryption_key"' "sites/$DOMAIN/site_config.json" || { echo "encryption_key missing!"; exit 1; }
bench --site "$DOMAIN" restore "$DB" --with-public-files "$PUB" --with-private-files "$PRIV" \
  --db-root-password "$DB_ROOT_PASSWORD"
bench --site "$DOMAIN" migrate

step "4) production settings"
bench --site "$DOMAIN" set-config host_name "https://$DOMAIN"
bench --site "$DOMAIN" set-config developer_mode 0
bench --site "$DOMAIN" enable-scheduler
bench --site "$DOMAIN" set-admin-password "$ADMIN_PASSWORD"
bench use "$DOMAIN"
echo "  old site was: $OLD"

step "5) keys + readiness"
if [ -n "$KEYS" ]; then
  bench --site "$DOMAIN" execute vintraxo_tcd.core.server_keys.apply_keys --kwargs "{'path': '$KEYS'}"
else
  bench --site "$DOMAIN" execute vintraxo_tcd.core.ops.print_readiness
fi

if [ $PROD = 1 ]; then
  step "6) nginx + supervisor + backups + SSL"
  bench config dns_multitenant on
  sudo env PATH="$PATH" bench setup production "$USER" --yes
  bench setup backups
  sudo env PATH="$PATH" bench setup lets-encrypt "$DOMAIN"
fi

rm -rf "$(dirname "$SRC")"
echo
echo "Done: https://$DOMAIN  (keep the bundle file somewhere safe, then delete it from this server)"
