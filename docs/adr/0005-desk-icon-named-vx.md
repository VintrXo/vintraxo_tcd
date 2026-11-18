# ADR-0005: Desk icon and workspace sidebar are both named "VX"

- Status: Accepted
- Date: 2026-11-18

## Context
In Frappe v16 the desktop page resolves an icon's route with
`frappe.boot.workspace_sidebar_item[desktop_icon.label.toLowerCase()]`, keyed by the Workspace Sidebar name.
Renaming only the icon label broke the click ("Icon is not correctly configured").

## Decision
Desktop Icon and Workspace Sidebar are both named and labelled "VX"; the workspace keeps the name "VintraXo TCD".
A pre-model-sync patch renames old records before the file sync (which would otherwise hit the unique label).

## Consequences
- Changing the label later requires renaming the sidebar too.
