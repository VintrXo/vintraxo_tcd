#!/usr/bin/env bash
# Fresh Ubuntu 24.04 server: install what Frappe v16 needs. Run ONCE as a sudo user (not root):
#
#   bash install_prereqs.sh
#
# Same versions as the internal server: MariaDB 10.11 and Redis 7 (Ubuntu 24.04 packages), Node 24,
# Python 3.14 (through uv), bench 5.x.
set -euo pipefail
[ "$(id -u)" != 0 ] || { echo "Run as a normal user with sudo, not root."; exit 1; }

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git curl ca-certificates build-essential pkg-config cron file \
  mariadb-server mariadb-client libmariadb-dev \
  redis-server nginx supervisor \
  python3-pip python3-venv pipx \
  xvfb fontconfig fonts-noto-core fonts-noto-color-emoji

# MariaDB settings Frappe expects
sudo tee /etc/mysql/mariadb.conf.d/99-frappe.cnf >/dev/null <<'CNF'
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
CNF
sudo systemctl restart mariadb

# Node 24 + yarn
if ! node --version 2>/dev/null | grep -q '^v24'; then
  curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi
sudo npm install -g yarn

# uv + Python 3.14 + bench
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.14
pipx install frappe-bench
pipx ensurepath

echo
echo "Done. Now set the MariaDB root password (answer the questions):"
echo "  sudo mariadb-secure-installation"
echo "Then log out and in again, and run setup_server.sh."
