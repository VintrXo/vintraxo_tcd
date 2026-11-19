# ADR-0019: Code runner client in Frappe; execution only on an isolated runner

- Status: Accepted (owner: "continue on the internal server"; runner host to be set up with the production server)
- Date: 2026-11-20

## Context
Phase 10 (PHASE10_ISOLATION_DESIGN.md): languages the browser cannot run, and grading that a learner cannot fake.
Ground rule: untrusted code never runs on the Frappe server. No runner host exists yet.

## Decision
- Frappe only talks to a **Judge0-compatible runner** over HTTP (`core/runner.py`); it never executes code. The runner
  is off by default and is configured in TCD Settings (URL, token, CPU/wall/memory limits, runs per minute,
  language → runner id table; defaults are the Judge0 CE ids and "Test Runner" checks them against `/languages`).
- Each request: base64 source, `wait=true`, the limits, `enable_network: false`, no redirects. Output capped at 64 KB,
  code at 64 KB. Every run is logged in **TCD Code Run** (user, language, purpose, status, time, memory, SHA-256 of
  the code — not the code itself); admins only.
- **Practice:** playground blocks and code questions in a runner-only language (java, cpp, c, go, csharp, bash) call
  `api.run_code` (logged-in users, per-user limit per minute).
- **Grading:** a Code question is graded on the runner when its language is runner-only or "Grade on the Code
  Runner" is ticked. The runner's output is stored with the answer at submit time (`server_output`) and used instead
  of the device output; a `server_output` sent by the learner is dropped. If the runner cannot run the code, the
  answer goes to manual review (never marked wrong for an outage). Reviews never re-run code.

## Consequences
- With the runner off nothing changes (browser playgrounds + "Instructor Reviews Code Answers").
- The isolation of execution is the runner host's job (separate VM, gVisor/isolate, no egress) — still to be set
  up; until then the feature stays off. Tested with the runner mocked.
