#!/usr/bin/env bash
# Pack everything the real server needs into ONE file (run on the internal server, from the bench folder).
#
#   bash apps/vintraxo_tcd/deploy/export_internal.sh [site] [out-dir] [--dry-run]
#
# The bundle holds:
#   manifest.tsv    every app: how to get it (git url + branch + commit, or the packed folder)
#   apps/*.tar.gz   our own apps (vintraxo_*) and any app without a remote, packed as they are on disk
#                   (with .git and uncommitted work), so nothing is lost even if it was never pushed
#   patches/*.diff  local edits inside upstream apps (e.g. ar.po translations), re-applied on the server
#   backup/         database + public files + private files + site_config_backup.json (encryption_key)
#   site.txt        the old site name
# The bundle contains the database and the encryption key: keep it private (chmod 600, never e-mail it).
set -euo pipefail

SITE="${1:-erpnext.localhost}"
OUT="${2:-$HOME/vintraxo-move}"
DRY=0
for a in "$@"; do [ "$a" = "--dry-run" ] && DRY=1; done
[ -f sites/apps.txt ] || { echo "Run this from the bench folder (frappe-bench)."; exit 1; }
[ -d "sites/$SITE" ] || { echo "Site $SITE not found."; exit 1; }

# files that only change when assets are built: never carried over
EXCLUDE=(':(exclude)*yarn.lock' ':(exclude)*package-lock.json' ':(exclude)*node_modules*'
         ':(exclude)*components.d.ts' ':(exclude)*/public/frontend/*' ':(exclude)*.pyc')

STAMP="$(date +%Y%m%d_%H%M%S)"
WORK="$OUT/vintraxo-move-$STAMP"
[ $DRY = 1 ] || mkdir -p "$WORK/apps" "$WORK/patches" "$WORK/backup"
MANIFEST="$WORK/manifest.tsv"
[ $DRY = 1 ] && MANIFEST=/dev/stdout
[ $DRY = 1 ] || : > "$MANIFEST"

for app in $(cat sites/apps.txt); do
  dir="apps/$app"
  remote=""; url=""; branch=""; commit=""; pushed=0
  if [ "$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" = "$(cd "$dir" && pwd)" ]; then
    remote="$(git -C "$dir" remote | head -1)"
    [ -n "$remote" ] && url="$(git -C "$dir" remote get-url "$remote")"
    branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD)"
    commit="$(git -C "$dir" rev-parse HEAD)"
    [ -n "$remote" ] && [ "$(git -C "$dir" branch -r --contains HEAD 2>/dev/null | wc -l)" -gt 0 ] && pushed=1
  fi
  if [[ "$app" == vintraxo_* ]] || [ $pushed = 0 ]; then
    printf '%s\tpacked\t%s\t%s\t%s\n' "$app" "$url" "$branch" "$commit" >> "$MANIFEST"
    [ $DRY = 1 ] || tar -C apps -czf "$WORK/apps/$app.tar.gz" \
      --exclude=node_modules --exclude=__pycache__ --exclude='*.pyc' --exclude='*.egg-info' "$app"
  else
    printf '%s\tgit\t%s\t%s\t%s\n' "$app" "$url" "$branch" "$commit" >> "$MANIFEST"
    changed="$(git -C "$dir" diff --name-only HEAD -- . "${EXCLUDE[@]}")"
    if [ -n "$changed" ]; then
      echo "  local edits kept as a patch for $app: $(echo "$changed" | tr '\n' ' ')" >&2
      [ $DRY = 1 ] || git -C "$dir" diff --binary HEAD -- . "${EXCLUDE[@]}" > "$WORK/patches/$app.diff"
    fi
  fi
done

if [ $DRY = 1 ]; then echo "(dry run: no backup, nothing written)"; exit 0; fi

echo "$SITE" > "$WORK/site.txt"
bench --site "$SITE" backup --with-files --backup-path "$WORK/backup"
chmod -R go-rwx "$WORK"
tar -C "$OUT" -czf "$OUT/vintraxo-move-$STAMP.tar.gz" "vintraxo-move-$STAMP"
chmod 600 "$OUT/vintraxo-move-$STAMP.tar.gz"
rm -rf "$WORK"
echo
echo "Bundle: $OUT/vintraxo-move-$STAMP.tar.gz ($(du -h "$OUT/vintraxo-move-$STAMP.tar.gz" | cut -f1))"
echo "Copy it to the server:  scp $OUT/vintraxo-move-$STAMP.tar.gz <user>@<server>:~/"
