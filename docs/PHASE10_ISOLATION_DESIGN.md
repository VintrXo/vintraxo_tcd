# Phase 10 — Server-side code runner: isolation design (FOR APPROVAL, nothing built)

Status: **Frappe side built (ADR-0019), runner host not set up yet.** The owner chose to continue on the current
server; the runner (Judge0 on an isolated VM, sections 2–3) will be installed with the production server.
Ground rule kept: untrusted code never runs on the Frappe server.

## 1. Why a server runner at all

Today every playground and code question runs in the learner's browser (sandboxed iframe + Web Worker, ADR-0001).
That is safe for the server, but it has limits:

| Need | Browser today | With a runner |
|---|---|---|
| Python (Pyodide), SQL (sql.js), JavaScript, HTML | Yes | Yes |
| Java, C/C++, Go, C#, Bash, Node with packages, Python with native libraries | No | Yes |
| **Trustworthy grading** of code questions | No: the browser reports the output, so a learner can fake it | Yes: hidden test cases stay on the server and the runner's output is compared there |
| Heavier exercises (databases, multi-file projects) | Limited by the device | Yes, within the limits below |

If none of these matter, the right decision is **not to build Phase 10** and keep browser-only execution.

## 2. Architecture

```
Learner browser ──HTTPS──> Frappe (tcd)                      Isolated runner host (separate VM)
                           │ api.run_code: permission, rate   ┌──────────────────────────────────┐
                           │ limit, hidden tests from DB      │ runner API (HTTPS, HMAC-signed)   │
                           │ enqueue job (short queue) ──────>│  per run: new container, --rm     │
                           │ <──── result (stdout, exit, time)│  gVisor runtime, no network       │
                           │ compare with expected output     │  limits: CPU, RAM, PIDs, time,    │
                           │ store TCD Code Run               │  disk, output size                │
                           └──────────────────────────────────└──────────────────────────────────┘
```

- **Frappe never executes code.** It sends `{language, files, stdin, limits}` and a run id, signed with HMAC
  (same scheme as the Phase 8 connectors), and receives `{stdout, stderr, exit_code, time_ms, memory_kb, status}`.
- **The runner is a separate machine** (VM, or at least a separate host) with no route to the Frappe database,
  Redis, file storage or the company network. Firewall: inbound only from the Frappe host on one port; **egress
  denied** (containers also run with `--network none`).
- No secrets on the runner except its own HMAC key. No company data is mounted.

## 3. Isolation of each run

| Control | Value (default, adjustable per language) |
|---|---|
| Container | One fresh container per run, removed afterwards (`--rm`), image pinned by digest, built offline |
| Kernel isolation | **gVisor** (`runsc`) runtime — user-space kernel between the code and the host kernel |
| Network | `--network none` |
| User | non-root uid, `--cap-drop ALL`, `no-new-privileges`, default seccomp profile |
| File system | read-only root; `/work` tmpfs 64 MB; no host mounts |
| CPU | 0.5 core, CPU-time limit 5 s |
| Wall time | 10 s (compile + run), hard kill by a watchdog |
| Memory | 256 MB, no swap |
| Processes | PID limit 64 (stops fork bombs) |
| Output | stdout + stderr capped at 64 KB; files written are discarded |
| Concurrency | runner: number of cores − 1; per user: 1 at a time, 10 runs per minute (enforced in Frappe) |

## 4. Two ways to build it (decision needed)

| | **A. Self-hosted Judge0 CE** (open source) | **B. Our own thin runner** (Docker + gVisor) |
|---|---|---|
| What we write | Only the TCD connector (Frappe side) | Runner API + container driver + connector |
| Languages | 40+ ready | The ones we package (start with Python, Java, C++, Node) |
| Sandbox | `isolate` (namespaces + cgroups) | gVisor per container |
| Risk | Past sandbox-escape CVEs (fixed in 1.13.1+): must pin a patched version and **still** run it on an isolated VM | More code to own and patch, smaller surface |
| Time | Short | Longer |

**Recommendation: A on an isolated VM**, pinned to a patched release, behind the controls in sections 2–3 that
apply outside the container (separate VM, no egress, firewall, rate limits). Move to B only if Judge0 does not fit.

## 5. Data, logs and cleanup

- New DocType **TCD Code Run** (Frappe side): user, question/content, language, SHA-256 of the code, status,
  exit code, time, memory, truncated output, created. The learner sees their own runs; instructors see runs in their
  courses; admins all. Kept 90 days (daily purge), except runs attached to graded submissions.
- Runner logs: run id, language, duration, status — **no code and no output** — kept 14 days.
- Cleanup: containers removed after each run; watchdog kills runs over the wall time; daily pruning of stopped
  containers and dangling images; the runner VM can be rebuilt from its image at any time (no state to keep).

## 6. Threats and answers

| Threat | Answer |
|---|---|
| Escape from the container to the host | gVisor + non-root + no capabilities + seccomp; even then only the runner VM is reached, which holds no data |
| Reaching company data / the internet | `--network none` + egress-deny firewall on the VM + no route to Frappe/DB |
| Crypto-mining, infinite loops | CPU-time and wall-time limits, per-user rate limits |
| Fork bomb, memory or disk exhaustion | PID, memory and tmpfs limits |
| Flooding Frappe | Runs are queued (short queue), per-user and global caps, the request returns a run id |
| Cheating in graded questions | Hidden tests and expected output never leave the server; grading happens in Frappe |
| Stealing other learners' code | Each run in its own container; no shared volumes; outputs only returned to the requester |

## 7. What is needed from the owner

1. Approve this design (or choose browser-only and skip Phase 10).
2. Choose **A (Judge0, recommended)** or **B (own runner)**.
3. Provide a separate VM for the runner (suggested: 4 vCPU, 8 GB RAM, Docker; not this WSL machine — it has no
   Docker and only `bwrap`, which is not enough isolation for untrusted code).
4. The first languages to support.

After approval: an ADR, the runner set-up on the VM, the Frappe connector (`TCD Code Run`, `api.run_code`, server
grading for Code questions), tests with the runner mocked plus an end-to-end test against the VM, and an escape /
limits test list (fork bomb, network access, large output, infinite loop, file write outside /work).
