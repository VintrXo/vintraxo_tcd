# ADR-0001: Learner code runs only in the browser

- Status: Accepted
- Date: 2026-11-18

## Context
Tutorials need runnable Python, SQL, JavaScript and HTML. Running untrusted code on the Frappe server would
expose company data and the server process.

## Decision
Every run creates an `<iframe sandbox="allow-scripts">` (opaque origin: no cookies, no access to the page or the
Frappe API as the learner) with a Web Worker inside. Python uses Pyodide, SQL uses sql.js with a fresh in-memory
database, JavaScript runs in the worker, HTML renders in a sandboxed preview. A time limit terminates the worker;
the parent removes the iframe as a last resort. Runtime URLs are settings so sites can self-host them.

## Consequences
- No server load or server risk from learner code; verified in Chromium (loops killed, fetch to the site blocked).
- Code exercises that need real data or server APIs are not possible until Phase 10, which requires an approved
  isolation design.
