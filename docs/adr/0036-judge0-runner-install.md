# ADR-0036: Installing the code runner (Judge0 CE) on its own server

- Status: Accepted (owner: "prepare it"); implements option A of docs/PHASE10_ISOLATION_DESIGN.md
- Date: 2026-11-20

## Decision
`deploy/judge0/install_judge0.sh` on a separate Ubuntu 22.04 / 24.04 server (never the Frappe server):
- Judge0 CE **v1.13.1**, pinned (release of 2024-04-18 that fixes the three critical vulnerabilities of <= 1.13.0;
  latest release when checked on 2026-11-20). Official procedure: cgroup v1 through GRUB
  (`systemd.unified_cgroup_hierarchy=0`, reboot), Docker + Compose, `db redis` first, then the rest.
- Random `REDIS_PASSWORD`, `POSTGRES_PASSWORD` and `AUTHN_TOKEN` (kept on rerun); `judge0.conf` is chmod 600.
- `ENABLE_NETWORK=false` and `ALLOW_ENABLE_NETWORK=false`: a submission can never reach the network.
- Limits: defaults CPU 5 s / wall 10 s / 256 MB, maxima CPU 15 s / wall 30 s / 1024 MB = the clamps in TCD Settings,
  so a request the app allows is never refused by the runner.
- The API is published on 127.0.0.1 only (Docker bypasses ufw for public ports); Caddy in front gives HTTPS with a
  domain (Let's Encrypt) or HTTP on 8443 without one; ufw allows SSH from anywhere and the runner port only from the
  Frappe server's IP. Request bodies are capped at 1 MB (the app sends at most 64 KB of code).
- Smoke test compiles and runs Java (language id 62) and checks that calls without the token are refused; the script
  prints the `runner` lines for `keys.json`. Language ids are checked from the Desk with "Test Runner".

## Consequences
- Not run here (WSL has no Docker and runs cgroup v2). The config edits were run against the real v1.13.1 zip:
  every setting exists, the port line was rewritten to 127.0.0.1, a rerun keeps the token.
- gVisor (option B) stays a later hardening step if Judge0 is not enough.
