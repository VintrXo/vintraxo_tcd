#!/usr/bin/env bash
# Code runner for Java / C# / C++ / C / Go / Bash lessons: Judge0 CE on its OWN server (never on the Frappe
# server: learner code is untrusted). Design: docs/PHASE10_ISOLATION_DESIGN.md, ADR-0036.
#
# Fresh Ubuntu 22.04 (recommended by Judge0) or 24.04, 2 cores / 4 GB is enough to start. As a sudo user:
#
#   FRAPPE_IP=<public IP of the Frappe server> [DOMAIN=runner.example.com] bash install_judge0.sh
#
# Run it twice: the first run switches the kernel to cgroup v1 (Judge0 requires it) and asks for a reboot;
# the second run installs. What you get:
#   - Judge0 CE v1.13.1 (fixes the three critical sandbox CVEs of <= 1.13.0), pinned
#   - API token required on every call (AUTHN_TOKEN), network disabled for submissions (cannot be turned on)
#   - Judge0 listens on 127.0.0.1 only; Caddy in front: HTTPS on 443 with DOMAIN, or HTTP on 8443 without
#   - firewall: only SSH from anywhere, the runner port only from FRAPPE_IP
#   - a smoke test that compiles and runs Java, and the lines to paste into keys.json
set -euo pipefail
VERSION=1.13.1
: "${FRAPPE_IP:?set FRAPPE_IP to the Frappe server public IP}"
DOMAIN="${DOMAIN:-}"
DIR="$HOME/judge0-v$VERSION"
[ "$(id -u)" != 0 ] || { echo "Run as a normal user with sudo, not root."; exit 1; }
step() { echo; echo "=== $*"; }

step "1) cgroup v1 (required by Judge0's isolate sandbox)"
if [ "$(stat -fc %T /sys/fs/cgroup)" = "cgroup2fs" ]; then
  if ! grep -q "systemd.unified_cgroup_hierarchy=0" /etc/default/grub; then
    sudo sed -i 's/^GRUB_CMDLINE_LINUX="\(.*\)"/GRUB_CMDLINE_LINUX="\1 systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
  fi
  echo "Kernel switched to cgroup v1 on next boot. Run:  sudo reboot   then run this script again."
  exit 0
fi
if ! awk '$1=="memory" && $4==1 {found=1} END {exit !found}' /proc/cgroups; then
  echo "This kernel ($(uname -r)) has no cgroup v1 memory controller (CONFIG_MEMCG_V1 off, common from"
  echo "kernel 6.11 on). Judge0 cannot limit memory without it. Use Ubuntu 22.04, or Ubuntu 24.04 with its"
  echo "standard 6.8 kernel (not the HWE kernel), then run this script again."
  exit 1
fi
echo "  cgroup v1 active, memory controller present"

step "2) packages"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io docker-compose-v2 unzip curl openssl ufw caddy
sudo systemctl enable --now docker

step "3) Judge0 v$VERSION"
if [ ! -d "$DIR" ]; then
  cd "$HOME"
  curl -fsSLO "https://github.com/judge0/judge0/releases/download/v$VERSION/judge0-v$VERSION.zip"
  unzip -q "judge0-v$VERSION.zip"
fi
cd "$DIR"
CONF=judge0.conf
setconf() { if grep -q "^$1=" "$CONF"; then sed -i "s|^$1=.*|$1=$2|" "$CONF"; else echo "$1=$2" >> "$CONF"; fi; }
if ! grep -q "^AUTHN_TOKEN=..*" "$CONF"; then
  setconf REDIS_PASSWORD "$(openssl rand -hex 16)"
  setconf POSTGRES_PASSWORD "$(openssl rand -hex 16)"
  setconf AUTHN_TOKEN "$(openssl rand -hex 24)"
fi
# limits match what the app may ask for (TCD Settings clamps: CPU <= 15 s, wall <= 30 s, memory <= 1024 MB)
setconf ENABLE_NETWORK false
setconf ALLOW_ENABLE_NETWORK false
setconf ENABLE_WAIT_RESULT true
setconf CPU_TIME_LIMIT 5
setconf MAX_CPU_TIME_LIMIT 15
setconf WALL_TIME_LIMIT 10
setconf MAX_WALL_TIME_LIMIT 30
setconf MEMORY_LIMIT 262144
setconf MAX_MEMORY_LIMIT 1048576
setconf MAX_PROCESSES_AND_OR_THREADS 60
setconf MAX_QUEUE_SIZE 100
chmod 600 "$CONF"
TOKEN="$(grep '^AUTHN_TOKEN=' "$CONF" | cut -d= -f2)"
# publish the API on localhost only (Docker would bypass the firewall for a public port)
sed -i -E 's/^(\s*-\s*)"?(0\.0\.0\.0:)?2358:2358"?/\1"127.0.0.1:2358:2358"/' docker-compose.yml
grep -q '127.0.0.1:2358:2358' docker-compose.yml || { echo "Could not bind port 2358 to localhost in docker-compose.yml"; exit 1; }
sudo docker compose up -d db redis
sleep 10
sudo docker compose up -d
sleep 5

step "4) Caddy in front + firewall"
if [ -n "$DOMAIN" ]; then
  SITE="$DOMAIN"; PORT=443; URL="https://$DOMAIN"
else
  SITE=":8443"; PORT=8443; URL="http://$(curl -fsS https://api.ipify.org || hostname -I | cut -d' ' -f1):8443"
fi
sudo tee /etc/caddy/Caddyfile >/dev/null <<CADDY
$SITE {
	request_body {
		max_size 1MB
	}
	reverse_proxy 127.0.0.1:2358
}
CADDY
sudo systemctl reload caddy || sudo systemctl restart caddy
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
[ -n "$DOMAIN" ] && sudo ufw allow 80/tcp   # Let's Encrypt certificate (Caddy redirects to HTTPS)
sudo ufw allow from "$FRAPPE_IP" to any port "$PORT" proto tcp
sudo ufw --force enable

step "5) smoke test (Java)"
for i in $(seq 1 30); do curl -fsS -H "X-Auth-Token: $TOKEN" http://127.0.0.1:2358/about >/dev/null 2>&1 && break; sleep 2; done
SRC=$(printf 'public class Main { public static void main(String[] a) { System.out.println("ok " + (6*7)); } }' | base64 -w0)
OUT=$(curl -fsS -X POST "http://127.0.0.1:2358/submissions?base64_encoded=true&wait=true" \
  -H "Content-Type: application/json" -H "X-Auth-Token: $TOKEN" \
  -d "{\"source_code\":\"$SRC\",\"language_id\":62}")
echo "$OUT" | grep -q "$(printf 'ok 42\n' | base64 -w0)" && echo "  Java ran: ok 42" || { echo "  Smoke test FAILED: $OUT"; exit 1; }
NOAUTH=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:2358/about)
[ "$NOAUTH" = 401 ] && echo "  calls without the token are refused (401)" || echo "  WARNING: /about without token returned $NOAUTH"

echo
echo "Done. Put these in keys.json on the Frappe server (section \"runner\"), then apply keys:"
echo "  \"runner\": {\"url\": \"$URL\", \"token\": \"$TOKEN\"}"
echo "Then in the Desk: Learning Settings -> Test Runner (checks the language ids)."
