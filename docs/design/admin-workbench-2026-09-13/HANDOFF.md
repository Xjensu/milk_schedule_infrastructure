# Administrator design handoff

Updated: 2026-09-13 after authenticated Playwright MCP inspection and the focused UI pass. Existing UI implementation is partial and already present in the dirty worktrees. Read the current status below before the preserved historical entries.

## 2026-09-21 — Retry live browser acceptance

- Status: public schedule read-only evidence refreshed; staff administrator mutation/read-back remains pending.
- Browser evidence: Playwright opened `/schedule?group=1` at a 390×844 viewport. The rendered page exposed the date field and “По дате” action, weekday links, subgroup and week selectors, the event card, print action, and the disabled “Переносы 0” state. The page returned no console errors.
- Administrator access: navigating to `/admin/workload` redirected to `/?auth=1` and showed the normal login dialog. No credentials were entered and no business mutation was sent.
- Source/runtime context: Rails and Hanami containers remain healthy; the public route exercised the current running Rails revision. This evidence does not certify the staff-only B00/B02 journey, resource CRUD, calendar mutations or account read-back.
- API read-back: the running Hanami service returned HTTP 200 for `/public/groups/1/schedule?date=2026-09-20` with `meta.anchor_date = 2026-09-20`, one semester descriptor, seven occurrences, and explicit `transfers` and `holidays` arrays.
- Next action: obtain an already authenticated staff browser session, then execute the documented workload → assignment → placement → edit → reload journey before claiming final acceptance.

## 2026-09-21 — Reconcile F01 source status

- The older `docs/TZ_COMPLIANCE_AUDIT_2026-09-20.md` was written before the aggregate schedule slice and still describes faculty/department schedules as missing. That file is preserved as historical audit evidence.
- Current source status: Hanami exposes staff-protected date-resolved reads at `GET /admin/faculties/:faculty_id/schedule/occurrences` and `GET /admin/kafedras/:kafedra_id/schedule/occurrences`; both use the shared occurrence query with semester clipping, transfers, cancellations and holidays. Rails routes these through `AggregateScheduleGateway`, `AggregateSchedule` operation/presenter and `/admin/aggregate_schedule`, with a selected-date print path.
- Assessment: F01 is source-complete and runtime-liveness verified, while authenticated scope, dated transfer/cancellation read-back and print evidence remain pending. The old audit must not be used as proof that the feature is still absent.

## 2026-09-21 — Remove aggregate print shell gap

- Finding: aggregate print CSS hid the sidebar and context panels but left the two-column admin shell active, which could reserve an empty sidebar track in print output.
- Behavior: the aggregate print rule now switches `.admin-shell` and `.admin-main` to a block print layout with no viewport minimum height. The selected-date report table, columns and transfer/cancellation styling remain unchanged.
- Rails revision: `e8f9f65`.
- Verification: Docker image rebuild, forced `schedule_web` recreation, Rails Zeitwerk check and internal `/up` HTTP 200 passed. Authenticated print preview remains pending.

## 2026-09-21 — Verify public selected-date print state

- Playwright emulated print media on `/schedule?group=1&date=2026-09-15`.
- The schedule table remained displayed, the mobile agenda was hidden, the date input/navigation controls were suppressed by print CSS, and the rendered date field still held `2026-09-15` before print. No console errors were reported.
- This verifies the public group print contract only; authenticated aggregate print preview remains pending.

## 2026-09-21 — Collapse aggregate context picker

- Finding: the aggregate faculty/department catalog was permanently expanded above the report, creating an unnecessary tall context wall after a scope had already been selected.
- Behavior: the catalog is now inside an accessible native `<details>` disclosure. The summary keeps the selected Russian scope label visible; opening it exposes the existing scope tabs, search field and bounded option list. Report columns, URL parameters and API identity remain unchanged.
- Rails revision: `ce75c66`.
- Verification: Docker build, forced `schedule_web` recreation, Rails Zeitwerk check, internal `/up` HTTP 200 and `git diff --check` passed. Authenticated computed-height and keyboard evidence remain pending.

## 2026-09-21 — Bound Schedule inspector assignment pickers

- Finding: the Schedule inspector’s teacher and room checkbox catalogs were unbounded inside the sticky editor, so a large result set could push the confirmation action below a long scroll.
- Behavior: `.planner-assignment-choices` now has a labelled, keyboard-reachable 248px scrolling region with readable 40px options and hover/focus states. The search fields, checked values, form names and server operations are unchanged; the existing sticky submit remains available.
- Rails revision: `200d149`.
- Verification: Docker build, forced `schedule_web` recreation, Rails Zeitwerk check, internal `/up` HTTP 200 and `git diff --check` passed. Authenticated computed-height and save/read-back evidence remain pending.

## 2026-09-21 — Add aggregate disclosure focus state

- The aggregate context disclosure summary now has an explicit visible keyboard focus ring and hover state using the shared velvet focus treatment.
- Rails revision: `b29b4fa`.
- Verification: `git diff --check` passed; Docker image rebuilt and `schedule_web` recreated; Zeitwerk and `/up` passed; the served fingerprinted workspace CSS contains the focus rule. The rule is scoped to the aggregate administrator control and does not affect public UI.

## Current continuation — browser evidence takes precedence

### 2026-09-20 — Preserve batch Notice workload context

- Status: source-complete; authenticated batch PDF queue/read-back evidence remains pending.
- Finding: the department batch Notice export returned to a reduced workload URL containing only department and semester, dropping faculty, selected groups and the workload query.
- Behavior: batch export forms and status/return links now preserve faculty, selected group IDs and the bounded workload query while keeping the existing department/semester/period contract for the API job.
- Files changed: `apps/schedule_web/app/controllers/admin/notice/exports_controller.rb`, `apps/schedule_web/app/views/admin/workload/show/show.html.erb`.
- Source revision: Rails `b81b8bf`.
- Runtime/source verification: container Ruby syntax, Workload ERB compilation, Rails Zeitwerk and `git diff --check` passed.
- Routes, role, context, viewport: Workload department mode and `/admin/notice/export_batch`, staff administrator, selected faculty/groups/query/semester; authenticated batch export status remains pending.
- Next action: rebuild `schedule_web`, then verify queue failure and completion return to the same department workload context.

### 2026-09-20 — Preserve Notice export search context

- Status: source-complete; authenticated PDF queue/read-back evidence remains pending.
- Finding: the Notice PDF action submitted teacher and semester IDs but dropped the active teacher search query. A queue failure or export status return could therefore lose the operator’s current context.
- Behavior: individual Notice export requests and status/return links now carry the bounded Russian teacher query alongside teacher, semester and period parameters. Report rows, period restrictions and batch export behavior remain unchanged.
- Files changed: `apps/schedule_web/app/controllers/admin/notice/exports_controller.rb`, `apps/schedule_web/app/views/admin/notice/show/show.html.erb`.
- Source revision: Rails `6d28d2d`.
- Runtime/source verification: container Ruby syntax, Notice ERB compilation, Rails Zeitwerk and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/notice`, staff administrator, selected teacher/search/semester/period; authenticated export and status read-back remain pending.
- Next action: rebuild `schedule_web`, then verify PDF queue failure/success returns to the same Notice context.

### 2026-09-20 — Align Schedule group search control

- Status: source-complete; authenticated computed-size evidence remains pending.
- Finding: the Schedule group selector search field retained a 36px legacy height while the shared administrator control contract requires 40px ordinary controls.
- Behavior: the group search field now uses the same 40px height as the surrounding context controls. Group filtering, checkbox selection and URL parameters are unchanged.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `15681ee`.
- Runtime/source verification: Rails Zeitwerk, `git diff --check`, Docker build, Propshaft precompile, `schedule_web` recreation and `/up` health response passed.
- Routes, role, context, viewport: `/admin/schedule`, staff administrator, selected faculty/group context; authenticated desktop and narrow measurements remain pending.
- Next action: measure the Schedule context controls and complete the core authenticated read-back journey.

### 2026-09-20 — Align searchable administrator controls

- Status: source-complete; computed-size browser evidence remains pending.
- Finding: several searchable catalog fields and Calendar reservation row actions still used 36px controls, below the shared 40px default target.
- Behavior: Accounts, Calendar, Resources and Workload search controls now use 40px fields; reservation row actions also use 40px. Table row density, schemas and primary touch actions remain unchanged.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`, `app/assets/stylesheets/components/_admin_calendar.css`, `app/assets/stylesheets/components/_admin_resources.css`, `app/assets/stylesheets/components/_admin_workload.css`.
- Source revision: Rails `f4d4402`.
- Runtime/source verification: Rails Zeitwerk and `git diff --check` passed. Docker/Propshaft deployment and authenticated computed-size verification remain pending.
- Next action: rebuild `schedule_web`, then measure the focused search and reservation controls in the authenticated browser.

### 2026-09-20 — Remove legacy account disclosure styles

- Status: source-complete; authenticated modal geometry evidence remains pending.
- Finding: obsolete `<details>` account-editor rules remained in shared and Accounts CSS after editors moved to native dialogs. Those rules duplicated positioning, padding and open-state layout and could override the common sheet contract.
- Behavior: the former disclosure rules are removed. Native account dialogs now use the shared sheet styles plus the scoped fixed-position guard; account table columns, actions and form contracts are unchanged.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`, `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revision: Rails `22380ad`.
- Runtime/source verification: Rails Zeitwerk and `git diff --check` passed; a fresh Docker/Propshaft build remains the deployment check for this CSS-only slice.
- Routes, role, context, viewport: `/admin/accounts`, staff account manager, existing account row; desktop and narrow sheet geometry remain pending without authenticated browser access.
- Next action: rebuild `schedule_web`, then verify the editor’s computed modal geometry and internal scroll.

### 2026-09-20 — Preserve reservation filters across pagination

- Status: source-complete; authenticated reservation pagination evidence remains pending.
- Finding: Room Reservations pagination links retained only room/date filters. Moving between pages silently dropped the active room search, teacher search and Calendar context.
- Behavior: previous/next reservation links now carry the existing room, teacher, date and Calendar context parameters while changing only the page number. Reservation columns and API contracts are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`.
- Source revision: Rails `7157d7d`.
- Runtime/source verification: Reservation ERB compilation, Rails Zeitwerk and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/room_reservations`, staff schedule writer, active search/date filters; browser pagination read-back remains pending.
- Next action: verify that a filtered page transition preserves the visible query and selected context in the authenticated browser.

### 2026-09-20 — Keep account editors in native modal sheets

- Status: source-complete; authenticated overlap/read-back evidence remains pending.
- Finding: the legacy `.account-editor { position: relative; }` rule still matched the new native account `<dialog>` editors. That allowed the editor to inherit table-layout positioning and reproduced the Accounts overlap risk from V07.
- Behavior: account editors now explicitly use fixed positioning inside the shared modal-sheet contract. The six-column account table, row actions, role scopes and password handling are unchanged.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revision: Rails `3c81c35`.
- Runtime/source verification: Rails Zeitwerk, Accounts ERB compilation, `git diff --check`, Docker image build, Propshaft precompile and `schedule_web` recreation passed.
- Routes, role, context, viewport: `/admin/accounts`, staff account manager, existing account row; desktop and narrow modal geometry remain pending without an authenticated browser session.
- Next action: verify the account editor's computed position, internal scroll and Escape/focus return in the authenticated browser, then continue the remaining reservation dependency read-back.

### 2026-09-18 — academic-structure catalogs added to the Rails checkout (runtime verification pending)

The current schedule-filling handoff identified the missing administrative path for the reference data that precedes group creation and workload allocation. Source tracing confirmed that Hanami already exposes authorized CRUD actions and contracts for faculties, departments (`kafedras`) and specialities, while Rails had no routes or resource tabs for them. Existing subject, activity-type, time-slot, week-type and student-group catalog tabs already cover the other required reference data. Curriculum streams were deliberately not surfaced as a new catalog: the current workload workflow creates and manages schedule load requirements directly, and the schedule-filling handoff does not require manual stream creation.

The Rails checkout now contains `Справочники → Факультеты`, `Кафедры` and `Специальности`. The three pages share one scoped controller and ERB form partial, use the existing `TeachersWorkspaceGateway` with the actual `/admin/faculties`, `/admin/kafedras` and `/admin/specialities` envelopes, retain safe drafts after recoverable failures, and select related faculties by name and short name rather than raw ID input. The resource switcher and page CSS preserve the existing square table/sheet system and local table scrolling.

Validation: Ruby syntax passed for the controller, gateway and routes; `bundle exec rails routes -g 'faculties|kafedras|specialities'` listed all twelve routes; `bundle exec rails zeitwerk:check` passed; ERB compilation source generated; scoped whitespace checks passed. On 2026-09-18, `schedule_web` was rebuilt and recreated through the normal Compose path. The running container's controller, view and CSS SHA-256 values match the checkout; `/up` and the fingerprinted application/resource CSS both return HTTP 200; unauthenticated requests to all three routes correctly redirect to sign-in; its logs contain no startup or request error after recreation.

Authenticated browser, mutation, and read-back evidence remains pending. Playwright MCP cannot start because the local Chrome binary is absent; its documented installation command failed with a registry proxy-authentication error. Do not claim this slice is visually or operationally accepted until an authenticated browser session is available. The next action is to restore the browser dependency/proxy path, then verify each page with a super-admin session, including create, validation retention, reload and relationship read-back.

Read [BROWSER_AUDIT.md](BROWSER_AUDIT.md) for measurements, exact reproduction, 17 screenshots, partial runtime provenance and untested behavior. The copy-ready next execution task is [BROWSER_BASED_CONTINUATION_PROMPT.md](BROWSER_BASED_CONTINUATION_PROMPT.md); the complete initiative prompt remains [IMPLEMENTATION_PROMPT.md](IMPLEMENTATION_PROMPT.md).

Playwright MCP successfully opened the local application and normal administrator sign-in succeeded. No account insertion or business mutation was performed. Do not store the supplied credentials or rerun the account-creation snippet. The old browser-unavailable reports below are historical.

Preserve existing implementation: token/component/domain CSS loads; Workload keeps its five columns in a labelled narrow scroll region; account person labels and searched edit fields render. No batch is fully accepted from these observations. Existing account failure-retention and schedule drag code must be inspected and exercised, not blindly rewritten or accepted.

Focused continuation: the user narrowed implementation to Resources, Calendar and Accounts and asked to restore continuation-only Schedule/Workload changes. Those Schedule/Workload changes were reverted; their historical browser measurements remain evidence only. The current pass is UI/UX focused: table-first create disclosures, coherent calendar/resource navigation, scoped square surfaces and preserved table schemas. Functional mutation journeys remain unverified because the user reports existing functionality is working and this pass did not perform business writes.

The historical sections 3–4 below describe the initial source audit. Later appended entries record intermediate source work and sometimes contradict one another about runtime deployment/search support. Use this current section and the browser audit for observed state; inspect touched source for anything not runtime-tested. Never interpret the last appended source claim as a completed acceptance gate.

## 1. Read this first

The user asks for a consistent administrator design system and much better UX while preserving the accepted Schedule/Workload character and all required table structures. They now say functionality works. This supersedes older notes telling agents to assume workload/schedule creation is broken. Future implementation still verifies those flows and fixes any reproduced regression first.

Work directly. No sub-agents or review ceremonies. No new tests/test files. English communication/docs, Russian UI. Preserve all dirty work in root and nested repositories. Do not change runtime data or deploy for a documentation-only request.

## 2. Package and authority

| File | Purpose |
| --- | --- |
| [AUDIT.md](AUDIT.md) | Historical source findings, architecture and contract evidence |
| [BROWSER_AUDIT.md](BROWSER_AUDIT.md) | Current rendered findings V01–V08, screenshots and evidence limits |
| [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) | Fixed token/type/control/layout/drag/editor decisions |
| [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | Ordered batches, target files and acceptance gates |
| [IMPLEMENTATION_PROMPT.md](IMPLEMENTATION_PROMPT.md) | Copy the entire file to start implementation |
| [BROWSER_BASED_CONTINUATION_PROMPT.md](BROWSER_BASED_CONTINUATION_PROMPT.md) | Copy the entire file to resume the existing partial implementation |
| Root `AGENTS.md` | Workspace constraints and latest priority |
| `apps/schedule_web/AGENTS.md` | Detailed Rails implementation rules |
| `apps/api_geteway/AGENTS.md` | API contract/identity/integrity guardrails |

This package overrides conflicting older design plans, mandatory reviewer-agent instructions and old broken-flow assumptions for this initiative. Preserve other architecture/security/data rules. Older Rails `docs/handoff/OPERATIONS.md`, `ASTRA_WORKING_SETUP.md`, `MEMORY_INDEX.md` and `VISUAL_CONTRACT.md` are useful references but must not reopen unrelated platform tasks. The package is intentionally model-independent; a less capable implementation model should execute the specified decisions rather than invent its own aesthetic.

## 3. Initial source audit history (superseded where noted above)

- Inspected Rails routes, admin layout/sidebar, shared tokens/reset/imports, admin/workload CSS, Schedule/Workload/Teachers/Notice/resource/calendar/account views, selected controllers, operations, gateways and Stimulus controllers.
- Inspected API routes, search query contract, schedule update action/contract/lock, assignment replacement contract/action/repository and notification transaction context.
- Read selected prior working/visual handoffs and local specification text. The DOCX has zero native table elements and no embedded media; no explicit table-layout appendix was found. Do not certify schema parity from it.
- Rails source at audit: `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43`; clean before docs edits.
- API source at audit: `0065358a53af0d80917fb9ea400727297b83c181`; substantial pre-existing dirty changes. Preserve all of them, including existing untracked specs; do not add more tests.
- Root has many unrelated dirty/untracked/deleted files. No global add/reset/cleanup.
- Local Rails `/up` responded HTTP 200 with explicit localhost proxy bypass.
- Browser setup returned no available browser; browser list was empty. No authenticated screenshots, computed-style results, live admin mutations or running-revision proof were obtained in this audit.
- W3C dragging and modal-dialog references were consulted for interaction requirements; links are in DESIGN_SYSTEM.md. Modern web guidance was queried; no browser-support claim or speculative containment optimization was adopted from it.
- Final documentation checks passed: all local Markdown links resolve, code fences are balanced, no Unicode replacement characters were found, and scoped Git whitespace checks reported no errors. Rechecked that all four reported undefined CSS tokens have no definitions in the inspected stylesheets. Rails status after writing contains only its AGENTS.md modification; UI source remains unchanged.

The source audit confirms partial CSS and undefined tokens, not literal absence of all styling. If continuing, avoid repeating the earlier preliminary missing-styles interpretation. Determine whether the reported runtime appearance also involves stale or failed assets.

## 4. Initial source findings (read current V01–V08 before acting)

1. `_admin_workspace.css` uses undefined `--admin-display`, `--muted`, `--paper-muted`, `--accent`; generic heading scale differs sharply from Schedule/Workload.
2. Partial resource/account/calendar styles live inside the shared workspace file, with inconsistent gutters, control coverage and row grids.
3. Five-field weekday-transfer rows use a generic three-column grid; several resource header and nested form tracks differ. Preserve schemas while fixing geometry.
4. Workload narrow CSS turns tables into cards; resource/account narrow CSS collapses row tracks; audit narrow CSS hides a column. These conflict with the user's current table-preservation rule.
5. Account edit/calendar fallbacks/weekday transfers/reservation edit expose raw IDs. Replace with readable searches using the correct semantic identity.
6. Accounts and period mutations redirect on failure, losing safe draft fields; several errors are generic/backend symbols. Repair within the relevant page batch.
7. Existing planner drag selects a load and opens a destination link. It does not move events or save directly. Extend staged operation semantics, not optimistic destructive DOM moves.
8. Assignment PUT replaces complete membership/room sets. A dropped item must be unioned with retained selected values, not sent alone.
9. Schedule update outer placement-lock transaction includes notification. Do not “fix” atomicity by misunderstanding its inner transaction.
10. Scope/identity and concurrency guarantees require real contract reading. A lock is not proof of stale-browser-draft rejection.

## 5. Identifier cheat sheet

| UI concept | Identity to retain | Frequent mistake |
| --- | --- | --- |
| Schedule/workload selected group | Student group semester | Sending a base student group ID because the local parameter is named group_id |
| Weekday transfer optional group | Base student group | Reusing planner group-semester ID |
| Teacher account / reservation teacher | Person/teacher ID | Sending department membership |
| Workload or event teacher | teacher_on_kafedra membership ID | Sending a person ID from generic teacher search |
| Existing event | Event ID, with same load requirement | Delete/create or changing requirement to simulate move |
| Room | Room ID, with building/name as display context | Trusting displayed room number as globally unique ID |

Read back omitted/empty/null semantics when editing. Do not clear unloaded relationships. API account paths live under `/auth/accounts`. API period write is POST upsert. Rails route names differ.

## 6. Implementation state

| Batch | Status | Next work |
| --- | --- | --- |
| Planning/docs | Updated with authenticated browser evidence | Use the continuation prompt |
| B00 baseline | Core workload → assignment → placement → recurring edit → reload/read-back journey verified on disposable data (2026-09-21); focused schedule regressions rechecked on 2026-09-28 | Keep the core journey as regression evidence; finish only remaining scoped-role and batch-specific acceptance |
| B01 shared system | Schedule/Workload roles retained; compact Schedule entry point and context verified at desktop/mobile widths (2026-09-30) | Continue only on reproduced acceptance gaps; full cross-page/zoom matrix remains open |
| B02 workbench journey | Core workload → assignment → placement → recurring edit journey verified on 2026-09-21; dated-transfer create/read-back/undo verified; faculty sandbox progress, inactivity age, stop, terminal proposal, conflict resolution, row-selection gate and blank active-group rendering verified (2026-09-30) | Investigate the 3/5 faculty-run plateau; verify recommendation placement and remaining failure paths; successful publication remains intentionally unattempted |
| B03 Resources | Catalog CRUD/validation journeys, Student Group create/failed-edit/successful-edit/reload/delete, dependency-blocked deletion, group-semester failure retention, name-catalog failed edits, Semester/Group Semester/Curriculum Stream API deletion guards, Faculty/Department/Specialty, Buildings, Rooms, Room Types, Building Types, Activity Types, Week Types, Time Slots, Posts, Academic Titles and Academic Degrees dependency-blocked deletion, and scoped-role denial verified (2026-09-30); broader cross-resource acceptance remains open | Continue remaining B03 family acceptance, including blocked-dependency feedback on other entities |
| B04 Calendar | All four period upserts, invalid-date retention, schedule read-back, reservation create/edit/conflict handling and occupancy overlay, dated-transfer create/read-back/undo, holiday and weekday-rule create/delete with global-vs-group scope, and labelled keyboard-scrollable tables verified | No remaining B04 acceptance blocker; continue B05/B06 gates and final core journey |
| B05 Accounts | Six-column report, shared modal sheet, role-specific searchable selectors, login suggestion/manual override, and safe create-validation failure retention verified in the running app (2026-09-30) | Verify successful role-specific create/edit and scoped-account read-back when a removable non-admin fixture is available; protect the sole working super-admin |
| B06 final QA | Focused Teachers, transfer, Notice-print, public-route and narrow/keyboard checks recorded below; full matrix remains open | Finish scoped-role coverage, true 200% zoom where available, remaining profile/failure paths and final journey |

## 7. Exact next session opening

1. Read root AGENTS.md and nested Rails AGENTS.md; read BROWSER_AUDIT.md, DESIGN_SYSTEM.md and the B00/B01 plan sections.
2. Capture independent Git status; do not assume the audit HEADs still apply.
3. Read current runtime runbook and verify localhost source/asset provenance. Do not dump env/config/session files or process command lines.
4. Use Playwright MCP and the authorized session if it remains valid; otherwise normal sign-in. The browser worked in this audit. Record only a newly reproduced access/tooling blocker. Do not bypass sign-in by extracting tokens from old artifacts.
5. Complete B00 evidence and core-flow baseline on safe data. If a regression is reproduced, fix only that blocker before styling.
6. Complete B01 on Schedule/Workload using existing primitives and the browser-derived decisions, preserving tables and prior changes. Fix a reproduced core blocker before visual work if B00 exposes one. Capture comparison evidence, update this current state table, then continue B02. Do not jump to a later source-only batch to avoid unfinished acceptance.

If the browser remains unavailable, say exactly which acceptance items are pending. Safe source work can continue but must remain source-complete/unverified. Do not mark B00 or any UI batch runtime-verified from `/up` or Ruby syntax.

## 8. How to keep this handoff useful

Append concise evidence entries using IMPLEMENTATION_PLAN.md's format and update batch status. Record new decisions only if an actual constraint invalidates a prescribed decision; explain the source and narrow deviation. Do not reproduce the whole transcript, add generic reviews or announce the same blocker as progress.

Do not overwrite this evidence history or mark skipped work complete. Final implementation delivery must report changed behavior, checks, remaining visual/runtime limitations and exact documentation links. A later model should be able to identify the next unfinished slice without reopening the full repository history.

## 9. Implementation evidence — 2026-09-13

### Focused UI pass — Resources, Calendar and Accounts

- Scope: implementation was narrowed by the user to the three administrator tabs above; Schedule and Workload continuation-only changes were reverted before this pass.
- Attributable Rails files: `app/views/admin/accounts/index.html.erb`, the four resource index views under `app/views/admin/resources/`, `app/views/admin/semesters/index.html.erb`, `app/views/admin/holidays/index.html.erb`, `app/views/admin/weekday_transfers/index.html.erb`, `app/views/admin/room_reservations/index.html.erb`, and the scoped component stylesheets `_admin_components.css`, `_admin_accounts.css`, `_admin_resources.css`, `_admin_calendar.css`.
- UI behavior: create forms are keyboard-accessible native disclosure sections, so table-first browsing is the default while existing form fields, Turbo frames and endpoints remain in place. Account report columns remain six columns. Calendar weekday transfers retain five columns. Resource inline form fields now participate in their report row tracks; Save/Delete remain in the existing action column.
- Control correction: following the user's explicit direction, visible native dropdowns were removed from the focused Accounts, Calendar and Resources views. Accounts now uses visible radio choice groups for role, status and faculty scope. Calendar uses visible choice groups for faculty, semester, group, weekday, room, teacher and time slot. Resource relationship fields use visible choice groups. Long choice groups scroll inside their own bounded region; values and existing hidden picker targets keep the current request identity.
- Runtime provenance: changed Rails source was copied into the running `schedule_web` container, `bundle exec rails assets:precompile` completed, and the service was restarted. Served fingerprints included `application-d611f14b.css` and `components/_admin_resources-56fd3a50.css`.
- Browser checks: authenticated super-admin session; `/admin/accounts`, `/admin/posts`, `/admin/operations?faculty_id=1&semester_id=8`, `/admin/weekday_transfers?faculty_id=1&semester_id=8`, and `/admin/schedule?faculty_id=1&semester_id=9`; 1280×900 and 390×844. Accounts create disclosure was opened by keyboard-capable native summary interaction; account editor opened as a bounded right sheet with no document overflow. At 390px, Accounts had document width 375px and table scroll width 940px; weekday transfers had document width 375px and table scroll width 860px; both had no page overflow. Posts computed row fields aligned at x=269 and x=695, with actions in the final column. No browser console errors were returned, and the changed CSS assets returned HTTP 200.
- No-dropdown check: the rendered Accounts, Posts and Calendar period routes reported zero `<select>` elements and no document overflow at the tested desktop viewport. Calendar period choice groups were bounded to 176px and the route rendered without console errors.
- Evidence: authenticated browser snapshots are in `.playwright-mcp/page-2026-09-13T13-44-36-900Z.yml`, `.playwright-mcp/page-2026-09-13T13-44-37-809Z.yml`, `.playwright-mcp/page-2026-09-13T13-44-05-292Z.yml`, and `.playwright-mcp/page-2026-09-13T13-42-29-925Z.yml`; the non-sensitive narrow Accounts viewport capture is `admin-accounts-table-first-390.png`.
- Verification limits: no business mutation was performed in this UI pass. The shared real modal sheet, searched Calendar group picker, reservation data dependency, and full create/edit/failure read-back journeys remain pending. `erb` standalone syntax piping is unsuitable for these Rails templates because existing inline ERB control expressions are not valid as raw Ruby; actual Rails rendering of all sampled routes succeeded.
- Next action: replace the Accounts row `details` editor with the existing real modal/dialog shell or a shared admin sheet controller while preserving its search and draft contract; then finish the Calendar reservation diagnosis and representative resource/account failure-state checks.

Batch/slice: B00 baseline / B01 shared system foundation
Status: B00 blocked on supported browser connection; B01 source-complete
Files changed (attributable): `apps/schedule_web/app/assets/stylesheets/application.css`, `app/assets/stylesheets/components/_admin_tokens.css`, `app/assets/stylesheets/components/_admin_components.css`, `app/assets/stylesheets/components/_admin_workspace.css`, `app/assets/stylesheets/components/_admin_workload.css`, `app/views/admin/schedules/show/show.html.erb`, `app/views/admin/workload/show/show.html.erb`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43`; root `8b5b7ae143b23cce251a969708b6bd2ef256443c`; API `0065358a53af0d80917fb9ea400727297b83c181`. Rails already had the user-owned `AGENTS.md` modification; only the listed Rails UI files were touched for this slice. Root/API changes predate this slice and were preserved.
Runtime source/asset verification method: Source imports use the existing Propshaft-compatible `@import url(...)` convention. `bin/rails zeitwerk:check` and a Rails runner view-path load check passed. The supported browser client could not be connected because its installed `browser-client.mjs` module was missing; no screenshot, computed-style, asset-network, or authenticated mutation evidence was captured.
Routes, role, safe selected context, viewport: Not runtime-verified. Source targets are admin Schedule and Workload at the existing routes; no role, selected data, or viewport claim is made.
Checks and exact results: `bin/rails zeitwerk:check` passed; Rails runner view-path check exited 0; `git diff --check` reported no whitespace errors; Impeccable detector returned `[]`; no unresolved uses of the previously undefined `--muted`, `--paper-muted`, or `--accent` aliases remain. Schedule table source remains one time column plus the existing weekday columns. Workload remains five columns in the order `Кафедра`, `Дисциплина и группа`, `Вид занятия`, `Часы`, `Назначение`.
Browser/mutation/read-back evidence paths: None available in this session. `/up` liveness is not used as proof of the core journey.
Table inventory comparison: No columns, order, grouping, row meaning, axes, totals, or report semantics changed. Workload narrow presentation now retains the semantic table and exposes a labelled horizontal scrolling region; Schedule builder scrolling is explicitly labelled and keyboard focusable.
Known remaining issue: B00 functional anchor and all visual/runtime evidence remain pending. B02 assignment selection, typed drag staging, placement, and existing event move/edit verification has not started.
Next concrete action: establish a supported browser connection or record the tooling blocker again, then inspect the current B02 contracts and complete the workload assignment slice before broadening to Resources.

Batch/slice: B02a shared entity selection and assignment editor
Status: source-complete; runtime and mutation verification pending
Files changed (attributable): `apps/schedule_web/app/javascript/controllers/assignment_picker_controller.js`, `app/views/admin/workload/show/_assignment.html.erb`, `app/assets/stylesheets/components/_admin_workload.css`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the B01 UI files listed above; API contract/action/repository inspected at `0065358a53af0d80917fb9ea400727297b83c181` with pre-existing dirty changes preserved.
Runtime source/asset verification method: `node --check` passed for the new Stimulus controller; `bin/rails zeitwerk:check` passed; the Impeccable detector returned `[]`. No supported browser client was available for route rendering or interaction evidence.
Routes, role, safe selected context, viewport: Source targets the existing workload assignment route and preserves `teacher_on_kafedra_ids[]` and `room_ids[]`; role/context/viewport remain unverified.
Checks and exact results: Teacher and room options retain their existing checkbox names and selected state. Search filters the complete server-provided option list within the open editor. Typed drag payloads are accepted only for the matching picker kind and only check an existing option. Duplicate drops are harmless. The final form submits all checked teachers and rooms together, matching the API replace-all contract and its up-to-20 validation.
Browser/mutation/read-back evidence paths: None available; no assignment PUT was sent.
Table inventory comparison: No table markup or report semantics changed.
Known remaining issue: This slice has not been proven against a live authenticated assignment save, failure retention, or reload/read-back. B02b placement and B02c existing lesson movement remain source-unimplemented.
Next concrete action: reconnect a supported browser and verify assignment save/failure/search retention, then implement staged workload-to-slot placement through the existing create operation.

Batch/slice: B02b typed workload-to-slot drag guard
Status: source-complete; runtime verification pending
Files changed (attributable): `apps/schedule_web/app/javascript/controllers/planner_drag_controller.js`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the earlier attributable UI files; existing Rails dirty state was preserved.
Runtime source/asset verification method: `node --check app/javascript/controllers/planner_drag_controller.js` passed. No browser connection was available.
Routes, role, safe selected context, viewport: Existing Schedule planner route and authorized administrator context only; runtime details unverified.
Checks and exact results: The controller now writes and accepts only `application/x-load-requirement`; arbitrary external `text/plain` drops are rejected. Click/tap remains available through the existing cell link and the drop still stages `selected_load` through the existing destination flow. No direct save or optimistic DOM move was introduced.
Browser/mutation/read-back evidence paths: None available; no placement mutation was sent.
Table inventory comparison: Schedule time plus weekday columns remain unchanged.
Known remaining issue: Full placement preview/cancel/invalid-target behavior and authoritative read-back remain unverified; existing event-to-cell move semantics are still pending B02c.
Next concrete action: Verify the typed drag and click paths in an authenticated browser, then inspect and implement the existing event move/edit operation without changing event identity.

Batch/slice: B02b/B02c staged schedule drag and existing-event editor
Status: source-complete for typed staging; runtime and failure-retention verification pending
Files changed (attributable): `apps/schedule_web/app/javascript/controllers/planner_drag_controller.js`, `app/views/admin/schedules/show/show.html.erb`, `app/assets/stylesheets/components/_admin_workspace.css`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the earlier attributable UI files; API update action/contract/repository inspected at `0065358a53af0d80917fb9ea400727297b83c181` with existing dirty state preserved.
Runtime source/asset verification method: Both changed JavaScript controllers pass `node --check`; `bin/rails zeitwerk:check` passes; the detector returns `[]`. The browser client remains unavailable, so no authenticated route or mutation was exercised.
Routes, role, safe selected context, viewport: Existing admin Schedule route, authorized administrator context, and existing event PATCH route; runtime role/context/viewport unverified.
Checks and exact results: Event drag now uses `application/x-schedule-event`, opens the existing inspector with target day/time staged from the destination cell, and does not submit on drop. The PATCH form keeps the same event ID and does not expose a load requirement change. Recurring edit remains separate from the dated transfer and atomic swap forms. External text drops remain rejected.
Browser/mutation/read-back evidence paths: None available; no event PATCH or transfer/swap mutation was sent.
Table inventory comparison: Schedule retains the existing time column and weekday columns. No table markup or event relationships were changed.
Known remaining issue: The existing update controller redirects after failure, so safe submitted teacher/room/date values and staged destinations have not yet been proven to survive 422/409/network failure. Two-session stale-draft behavior remains unverified.
Next concrete action: Repair the Schedule failure path to retain safe draft input in the inspector, then move to the shared Resources batch after live browser access is restored or the runtime limitation is recorded again.

Batch/slice: B03 resource navigation and table geometry foundation
Status: source-complete for shared navigation and narrow table geometry; CRUD/editor runtime verification pending
Files changed (attributable): `apps/schedule_web/app/views/admin/resources/_navigation.html.erb`, resource index views, `app/views/admin/student_groups/index.html.erb`, `app/views/admin/student_groups/semesters.html.erb`, `app/assets/stylesheets/components/_admin_resources.css`, `app/assets/stylesheets/components/_admin_workspace.css`, `app/assets/stylesheets/application.css`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43`; API `0065358a53af0d80917fb9ea400727297b83c181` before the attributable reservation/account changes below. Existing nested dirty files were preserved.
Runtime source/asset verification method: Rails Zeitwerk check and Ruby syntax checks pass; UI detector returned `[]`. No supported browser is available (`agent.browsers.list()` returned `[]`), so route rendering, loaded asset fingerprints, and CRUD read-back remain unverified.
Routes, role, safe selected context, viewport: Existing super-admin resource routes and student-group routes; role, context, and viewport unverified.
Checks and exact results: Resource and student-group pages now use the same complete navigation partial with active state. Resource cards retain table-first composition. The narrow CSS no longer collapses resource/account rows to a one-column layout; dense content remains horizontally accessible inside the resource table card. No resource table column schemas were changed.
Browser/mutation/read-back evidence paths: None available; no resource mutation was sent.
Table inventory comparison: Existing resource and group-semester table columns remain in place. The group-semester identifier display remains a documented identity issue pending readable catalog projections.
Known remaining issue: Resource create/edit forms are still inline and redirect-on-failure; relationship selectors and group-semester raw identifiers remain to be migrated under the full B03 acceptance gate.
Next concrete action: Repair resource failure re-render and searchable relationship selectors, then verify one complete resource CRUD flow with authoritative reload/read-back.

Batch/slice: B04 reservation identity projection / B05 account identity labels
Status: source-complete for removing visible raw teacher IDs in these editors; searchable edit scopes and runtime verification pending
Files changed (attributable): `apps/api_geteway/slices/admin/relations/room_reservations.rb`, `slices/admin/repos/room_reservation_repo.rb`, `slices/admin/serializers/room_reservation_serializer.rb`, `slices/authentication/serializers/account_serializer.rb`, `slices/authentication/actions/accounts/index.rb`, `apps/schedule_web/app/lib/gateways/admin/accounts_gateway.rb`, `app/views/admin/accounts/index.html.erb`, `app/views/admin/room_reservations/index.html.erb`
Source revision + dirty-scope identifier: API `0065358a53af0d80917fb9ea400727297b83c181` plus existing dirty state; Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the attributable UI changes. No tests were added.
Runtime source/asset verification method: API and Rails Ruby syntax checks pass; Rails Zeitwerk check passes; UI detector returned `[]`. Browser availability remains empty.
Routes, role, safe selected context, viewport: Existing account and room-reservation admin routes; role/context/viewport unverified.
Checks and exact results: Account list serialization now carries a safe teacher name projection and the edit view uses it with a hidden teacher identity. Existing scope identities are retained in hidden fields while labels are shown. Reservation edit no longer presents a numeric teacher input; it uses the searched labelled options and retains the current person selection. Teacher account/reservation identity remains person ID; workload/event identity remains teacher-on-kafedra membership ID.
Browser/mutation/read-back evidence paths: None available; no account or reservation mutation was sent.
Table inventory comparison: Account six-column row meaning and reservation columns remain unchanged.
Known remaining issue: Account edit scope additions still lack a searched selector, reservation edit still needs a live searched replacement for changing teacher, and redirect-on-failure draft retention is not fixed. API projection behavior is syntax-checked but not runtime-read back.
Next concrete action: Implement searched edit selectors with retained current values, then verify account and reservation failure/conflict/reload behavior in an authenticated browser.

Batch/slice: Compose runtime provenance and compatibility correction
Status: affected services rebuilt and healthy; authenticated browser verification remains blocked
Files changed (attributable): `apps/schedule_web/app/views/admin/accounts/index.html.erb`, `apps/api_geteway/slices/authentication/actions/accounts/index.rb`
Runtime source/asset verification method: The project runs from the root `docker-compose.yml`. `schedule_web` and `api_geteway` have no application bind mounts, so both images were rebuilt and recreated. Propshaft precompiled the new admin CSS and Stimulus bundles. Host and container SHA-256 values matched for the inspected Rails and API files. `docker compose ps` reported both services healthy; `GET http://localhost:3000/up` returned 200.
Checks and exact results: The first rebuilt run exposed `Array#compact_blank` incompatibility in the Hanami account projection and the account teacher search template. Both uses were replaced with Ruby-compatible `compact.join(...).strip` handling; API `ruby -c` passed, the API image was rebuilt, and the service was recreated. Subsequent unauthenticated requests to the account and reservation routes reached Rails and returned the expected authentication redirect; no new API 500 appeared in the post-fix log window.
Known remaining issue: The supported in-app browser is unavailable (`agent.browsers.list()` returned `[]`), and direct HTTP checks lack the authorized administrator session. No authenticated visual, mutation, or read-back acceptance evidence is claimed. The stack contains pre-existing observability orphan warnings and remains running.
Next concrete action: Restore an authorized browser session, verify the full core journey and failure retention, then complete searched edit scopes and remaining B03–B06 source slices.

Follow-up build note: After correcting the Rails template's second `compact_blank` use, `docker compose build schedule_web` and a direct `docker build --pull=false` retry both stopped at Docker Hub `ruby:3.4.2` metadata resolution timeout before executing build steps. The source fix is present in the Rails worktree but is not yet in the running image; retry the image build when registry access is available, then recreate `schedule_web`.

Resolution: Registry-free rebuild from the existing `milk_schedule-schedule_web:latest` image completed successfully. The temporary Dockerfile was removed, `schedule_web` was recreated, and host/container hashes matched for the changed account and reservation controllers/templates. `GET http://localhost:3000/up` returned 200 and Compose reports `schedule_web` healthy.

Batch/slice: B05 account edit search and retained scope selection
Status: source-complete for edit search staging; runtime interaction and mutation verification pending
Files changed (attributable): `apps/schedule_web/app/controllers/admin/accounts_controller.rb`, `app/views/admin/accounts/index.html.erb`, `app/javascript/controllers/account_scope_picker_controller.js`, `app/assets/stylesheets/components/_admin_accounts.css`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the attributable changes above; pre-existing nested dirty files preserved.
Runtime source/asset verification method: The current Rails source was copied into a registry-free image derived from the existing `milk_schedule-schedule_web:latest`; Propshaft precompile completed, the service was recreated, host/container hashes matched for the changed files, and Compose reports `schedule_web` healthy.
Routes, role, safe selected context, viewport: Existing `/admin/accounts` route; role, selected account and viewport remain unverified without an authorized browser session.
Checks and exact results: Account edit now has isolated teacher and department search frames that preserve list filters. Teacher selection updates the existing hidden person identity. Scope selection appends a deduplicated `faculty_id` or `kafedra_id` hidden input to the same PATCH collection, preserving existing scopes. No nested search form remains inside the PATCH form. `node --check`, Ruby syntax, Rails Zeitwerk and `git diff --check` passed.
Browser/mutation/read-back evidence paths: None; direct unauthenticated HTTP only proves the liveness endpoint and cannot exercise the protected editor.
Table inventory comparison: The six account columns and their order remain unchanged.
Known remaining issue: Search result click, scope deduplication, failed PATCH re-render and authoritative account read-back need authenticated browser verification. Faculty scope additions still use the same picker infrastructure but currently require the existing short faculty control where available.
Next concrete action: Restore supported browser access and verify the account search/edit flow, then continue B04 calendar searchable reservation editing and B06 final consistency checks.

Batch/slice: B04 reservation room search
Status: source-complete for create-side room search; edit-side search and runtime interaction verification pending
Files changed (attributable): `apps/schedule_web/app/lib/gateways/admin/teachers_workspace_gateway.rb`, `app/controllers/admin/room_reservations_controller.rb`, `app/views/admin/room_reservations/index.html.erb`, `app/javascript/controllers/reservation_room_picker_controller.js`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43`; API room search action/route/repository already existed in the preserved API worktree. No unrelated files were staged or reset.
Runtime source/asset verification method: Rails was rebuilt from the current local application image, Propshaft precompile completed, and `schedule_web` was recreated through Compose. Ruby/JS syntax and Rails Zeitwerk passed; the service reports healthy.
Routes, role, safe selected context, viewport: Existing `/admin/room_reservations` route, super-admin-only behavior and current calendar context; role and viewport remain unverified in the unavailable browser.
Checks and exact results: The gateway calls the existing authorized `GET /admin/search/rooms?q=...` contract. Search results are shown in a labelled frame and selecting one stages the existing room select; no write is sent. The native room list remains available. Table columns remain unchanged.
Browser/mutation/read-back evidence paths: None; direct requests lack an authorized session and no reservation mutation was sent.
Table inventory comparison: Reservation table retains its existing five columns and order.
Known remaining issue: Reservation edit rows still need the same searched room/person replacement flow; authenticated conflict/read-back and narrow layout verification remain pending.
Next concrete action: Add isolated edit-row room/person search while preserving the original row, then verify the complete Calendar acceptance matrix in an authorized browser.

Batch/slice: B04 reservation edit search
Status: source-complete; runtime endpoint/provenance verified; authenticated interaction and mutation verification pending
Files changed (attributable): `apps/schedule_web/app/controllers/admin/room_reservations_controller.rb`, `app/views/admin/room_reservations/index.html.erb`, `app/javascript/controllers/reservation_teacher_picker_controller.js`, `app/javascript/controllers/reservation_room_picker_controller.js`, `app/assets/stylesheets/components/_admin_calendar.css`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the attributable files above; API route/action/repository were pre-existing preserved worktree changes.
Runtime source/asset verification method: The current Rails image was rebuilt from the local running image base with Propshaft precompile, the temporary build file was removed, and `schedule_web` was recreated via Compose. Container hashes matched the current Rails source. The existing API `GET /admin/search/rooms?q=abc` route was reached inside `api_geteway` and returned 401 without an authorization token, confirming route reachability without exposing credentials.
Routes, role, safe selected context, viewport: Existing `/admin/room_reservations`; edit-row search retains room/date filters and uses the existing super-admin route guard. Role and viewport remain unverified in the unavailable browser.
Checks and exact results: Each reservation row now groups room/person search inside a disclosure, keeping the existing table row geometry and five-column schema. Results are isolated by reservation ID; choosing a room or person updates only that row's existing PATCH select and does not submit. Ruby/JS syntax, Rails Zeitwerk, undefined-admin-token scan and `git diff --check` passed. Compose reports `schedule_web` and `api_geteway` healthy; `/up` returned 200.
Browser/mutation/read-back evidence paths: None; no credentialed mutation was sent and no authenticated browser session is available.
Table inventory comparison: Reservation table remains five columns in the existing order; search tools are contained in the existing action area disclosure.
Known remaining issue: Full Calendar acceptance still needs authenticated search selection, conflict retention, successful update, authoritative reload/read-back, and narrow/responsive inspection. B03 resource CRUD and B06 final verification remain unfinished.
Next concrete action: Reconnect a supported authorized browser, run the core workload-to-schedule journey and Calendar mutation matrix, then close the remaining B03/B06 gates.

Batch/slice: B04/B05 safe failure drafts
Status: source-complete for account and reservation create/update re-render paths; runtime verification pending
Files changed (attributable): `apps/schedule_web/app/controllers/admin/accounts_controller.rb`, `app/controllers/admin/room_reservations_controller.rb`, `app/views/admin/accounts/index.html.erb`, `app/views/admin/room_reservations/index.html.erb`
Source revision + dirty-scope identifier: Rails `cbafbb2a887dd989dbe5b5fc2441cd1efee26c43` plus the attributable UI/API changes already listed; unrelated nested dirty files preserved.
Runtime source/asset verification method: Source-only after the Compose image rebuild was blocked by registry metadata timeout. No mutation was sent. Password and generated-password fields are excluded from account drafts.
Routes, role, safe selected context, viewport: Existing `/admin/accounts` and `/admin/room_reservations` routes; administrator role, context and viewport remain unverified without the supported browser session.
Checks and exact results: Account create/update failures now re-render the existing list with safe email, role, status, teacher identity and scope values retained; reservation create/update failures re-render the same page with submitted room, teacher, date, time slot and purpose values, while the original row remains authoritative for an update failure. Russian failure messages distinguish conflict, forbidden and validation outcomes. Rails controller syntax passes and no `compact_blank` use remains in the touched account path.
Browser/mutation/read-back evidence paths: None; the new Rails image could not be rebuilt after the final template change, and browser discovery remains empty.
Table inventory comparison: Account six columns and reservation five columns remain unchanged.
Known remaining issue: Re-rendered drafts need authenticated 422/409/network verification. Account edit scope additions and reservation teacher replacement are still not fully searchable in the edit forms.
Next concrete action: Rebuild `schedule_web` when Docker registry access recovers, then verify these failure states and implement searched edit selectors with preserved existing values.

Batch/slice: B00 baseline / B01 continuation fixes
Status: source-complete; authenticated runtime and mutation verification pending
Files changed (attributable): `apps/schedule_web/app/views/admin/schedules/show/show.html.erb`, `app/views/admin/weekday_transfers/index.html.erb`, `app/assets/stylesheets/components/_admin_components.css`, `app/assets/stylesheets/components/_admin_workspace.css`, `app/assets/stylesheets/components/_admin_calendar.css`, `app/assets/stylesheets/components/_admin_accounts.css`
Source revision + dirty-scope identifier: Rails current dirty worktree on branch `main`; all listed files already contained pre-existing user changes, and this continuation preserved those changes while adding only the scoped history, control, heading, transfer-grid and account-sheet adjustments.
Runtime source/asset verification method: Current host source was inspected; the supported Playwright browser reached `http://localhost:3000` and `/up` returned 200. The protected admin route redirected to the public sign-in dialog. No credentials, cookies or old auth artifacts were inspected.
Routes, role, safe selected context, viewport: Public `/up` and protected `/admin/schedule?faculty_id=1&semester_id=9`; authenticated role, selected context and target viewports remain pending because the current browser session is unauthenticated.
Checks and exact results: Ruby syntax passed for touched controllers; `node --check` passed for the touched Stimulus controllers; Rails loading command exited 0; `git diff --check` found no whitespace errors; Impeccable detector returned `[]`. Schedule now uses Turbo history advancement on its shell frame, the heading is 24/32 desktop and 20/28 narrow, admin form controls inherit the 40px role, weekday transfer rows declare five tracks, and the Accounts editor is bounded as a full-height sheet. No table columns or order were changed.
Browser/mutation/read-back evidence paths: Browser snapshot is in the session output at `.playwright-mcp/page-2026-09-13T12-38-39-214Z.yml`; no authenticated screenshot or mutation/read-back evidence exists for this continuation.
Table inventory comparison: Schedule time plus weekday columns, Workload five columns and Accounts six columns remain unchanged; weekday transfer content now has five layout tracks including actions.
Known remaining issue: B00 core workload → assignment → placement → edit → reload journey, V03 URL/reload proof, computed-size acceptance, real modal semantics, resource table-form alignment, reservation availability, and full B03–B06 browser gates remain unfinished.
Next concrete action: Resume with an authorized authenticated browser session, capture B00 baseline and run the safe core journey before accepting B01 or starting further UI batches.

Batch/slice: B00/B01 authenticated runtime continuation
Status: runtime-verified for Schedule context history and compact shared roles; core mutation and populated narrow-table gates pending
Files changed (attributable): `apps/schedule_web/app/views/admin/schedules/show/show.html.erb`, `app/views/admin/workload/show/show.html.erb`, `app/assets/stylesheets/components/_admin_workspace.css`, `app/assets/stylesheets/components/_admin_workload.css`, plus the scoped B01 files listed in the preceding entry.
Source revision + dirty-scope identifier: Rails current dirty worktree on branch `main`; runtime was updated by documented registry-free file copy and asset precompile because `docker compose build schedule_web` could not resolve `ruby:3.4.2` metadata from Docker Hub.
Runtime source/asset verification method: `schedule_web` was restarted after precompilation. Served assets returned 200 with current fingerprints `application-b5c9d21a.css`, `_admin_workspace-854a1010.css` and `_admin_workload-818ab648.css`; the container reported healthy.
Routes, role, safe selected context, viewport: Authenticated super-admin, `/admin/schedule?semester_id=9&faculty_id=1&groups[]=789` and `/admin/workload?faculty_id=1&semester_id=9`; Schedule desktop browser viewport was 914×976 after login and Workload was also checked at 390px wide.
Checks and exact results: Selecting `МК-3` changed the browser URL to include `groups[]=789`; a fresh navigation to that URL restored the checked group and grid. Computed Schedule heading was 24px/32px, committed context height 65px and first grid top 362px. Workload heading was 24px/32px, committed context height 138px and results top 376px. Schedule context inputs/buttons measured 40px. No console errors were reported. Current semester 9 has no workload rows, so populated table geometry was not claimed.
Browser/mutation/read-back evidence paths: `.playwright-mcp/page-2026-09-13T13-23-14-294Z.yml`, `.playwright-mcp/page-2026-09-13T13-25-39-090Z.yml`; no mutation or authoritative write read-back evidence yet.
Table inventory comparison: Schedule retains one time column plus the existing weekday columns. Workload table schema was untouched; the five-column narrow table remains pending populated-data verification.
Known remaining issue: B00 mutation anchor is still pending; B02 assignment/placement/edit operations and B03–B06 acceptance remain unfinished. The host curl probe returned 502 while the container healthcheck reported healthy, so liveness is based on browser 200 responses and container health rather than that probe.
Next concrete action: Use an older populated semester/faculty scope to verify Workload’s five-column scroll region, then complete the safe write/read-back journey before proceeding to B02.

Batch/slice: Focused UI/UX pass - Accounts, Calendar and Resources
Status: source and authenticated visual runtime checks completed for the focused layout pass; mutation and real dialog semantics remain pending
Files changed (attributable): focused admin tokens/components/resources/calendar/accounts styles, focused administrator ERB views, and the focused Stimulus picker/controller files.
Runtime source/asset verification method: Current Rails source was copied into the running schedule_web container, Propshaft assets were precompiled, and the service was restarted through Docker Compose. Served CSS fingerprint: application-5766d961.css; the container remained healthy.
Routes, role, context, viewport: Authenticated administrator session; /admin/accounts, /admin/posts, /admin/operations, and /admin/student_groups; desktop 1440x900 and narrow 390x844.
Checks and exact results: Focused pages use visible radio/list choices and no rendered select elements on the checked routes. At desktop, document width matched the viewport (1425/1425 with the browser content area) and the main workbench/header expanded across the available canvas; Accounts header width was 1153px. At 390px, all checked pages had document width equal to content width (375/375) with no page-level overflow, closed create/edit disclosures, and zero fresh console errors. Account edit role selection changed the retained hidden role from scheduler to super_admin with no controller errors. node --check, Rails loading, git diff --check, and the Impeccable detector passed. No mutation was sent.
Browser/mutation/read-back evidence paths: Browser session snapshots are in the Playwright session output for the authenticated checks; screenshot capture was attempted but did not complete, so no screenshot is claimed as evidence. No write/read-back evidence exists for this slice.
Table inventory comparison: Existing account, reservation, resource and group-semester table structures were preserved; no columns, order, headers or row meaning were changed. Dense content remains locally scrollable where the existing table requires it.
Known remaining issue: The account/resource editors use the existing disclosure-based Rails forms and still need conversion to a true accessible dialog/sheet with focus containment, inert background, Escape and dirty-close handling. Room reservations still renders the unavailable-data message in the current runtime, so reservation picker behavior is not verified. Raw numeric fallback fields in calendar settings/weekday transfers and full searchable catalog behavior remain pending. No CRUD mutation or authoritative reload/read-back has been claimed.
Next concrete action: Implement the shared real sheet semantics for Accounts/Resources, then trace and repair the reservation data dependency before performing authenticated failure, mutation and read-back checks.


Batch/slice: Buildings and Room Types content recovery plus Calendar scale
Status: source-complete; runtime redeployment and authenticated visual verification pending because Docker Desktop Linux engine is currently unavailable
Files changed (attributable): apps/schedule_web/app/views/admin/resources/buildings/index.html.erb, app/views/admin/resources/room_types/index.html.erb, app/assets/stylesheets/components/_admin_calendar.css, and the calendar page view class markers.
Source/runtime finding: Buildings and Room Types previously suppressed their entire table when the companion building-type or activity-type catalog failed. The page now keeps the primary rows visible, shows stored relationship names, and withholds only catalog-dependent create/edit controls until the companion list is available. Calendar controls now use larger 44px choices, 14px labels, a wider two-column context layout, and four period cards across desktop.
Checks: JavaScript syntax and git diff --check pass. Host HTTP and browser runtime could not be rechecked after the local Docker Linux engine stopped; no runtime success is claimed for this slice.
Remaining issue: Docker Desktop service cannot currently expose the dockerDesktopLinuxEngine named pipe, so the modified views/styles are not yet redeployed after the latest source edits. Restart the local engine, copy the focused files, precompile assets, and verify /admin/buildings, /admin/room_types and /admin/operations at desktop and narrow widths.


Runtime verification update: API gateway was found stopped and restarted through Docker Compose. After fixing the Hash-versus-object access in the live templates (building/activity catalog entries now use [:id] and [:name]) and restarting schedule_web, authenticated browser checks succeeded. /admin/buildings rendered 19 resource rows and /admin/room_types rendered 17 rows at desktop and narrow widths. Both routes reported zero fresh console errors and no document overflow. Calendar /admin/operations reported 44px navigation at 1440px and 390px with no overflow. Resources navigation now also measures 44px with 14px text. The pages expose one closed native dialog for create actions. No mutation was sent.


Calendar sheet runtime update: Migrated create actions for Semesters, Holidays, Weekday Transfers and Room Reservations to the shared native dialog sheet controller, preserving existing form fields and endpoints. Authenticated browser verification at 390px confirmed Semesters and Weekday Transfers render one closed dialog, zero visible select controls, 44px calendar navigation, no document overflow and zero fresh console errors. Opening the Weekday Transfer sheet produced a native dialog with a backdrop and initial focus on the close control. Docker Compose reports api_geteway and schedule_web healthy. No mutation was sent.


Resource editor geometry update: Converted the remaining resource row editors for posts, buildings, room types and rooms into shared native dialog sheets. Visible table values remain in their original columns; edit and delete actions now share one compact action cell, so row height is 61px in the checked narrow and desktop renders instead of expanding around inline forms. The buildings and room types tables continue to render stored relation labels even when companion catalogs are unavailable.

Files changed (attributable): `apps/schedule_web/app/views/admin/resources/posts/index.html.erb`, `buildings/index.html.erb`, `room_types/index.html.erb`, `rooms/index.html.erb`, and `app/assets/stylesheets/components/_admin_resources.css`.
Runtime source/asset verification: Files were copied into `schedule_web`, Propshaft was precompiled, and the service was restarted with Docker Compose. Current service state is healthy; current application asset fingerprint is `application-3da01bda.css`.
Routes, role, viewports: Authenticated administrator browser session; `/admin/buildings`, `/admin/room_types`, `/admin/rooms`, `/admin/posts` at 390px and `/admin/rooms` at 1440px. No mutation was sent.
Checks and exact results: Buildings rows measured 61px at 390px, 375px document width matched the client width, and the first edit sheet opened as a native dialog with `rgba(21, 19, 17, .34)` backdrop and focus on `������� ��������`. Room Types rendered 16 rows, zero visible selects, no overflow and zero fresh console errors. Posts rendered 24 row edit dialogs, retained name/short-name values and had zero visible selects, no overflow and zero fresh console errors. Rooms retained all four columns; first rows measured 61px at 1440px with document/client width 1425px and zero fresh console errors.
Table comparison: Resource table columns, order, headers and row meaning remain unchanged. Only the action cell composition changed from inline form fields to a shared editor sheet.
Remaining issue: CRUD success, validation/conflict retention, searchable relationship selection and authenticated read-back are still pending. Calendar at 390px currently uses 44px navigation controls and wraps to 148px of content-driven navigation height; this is documented as a narrow navigation exception caused by keeping all destinations visible.
Next concrete action: Continue Calendar and Accounts runtime acceptance, then run the required failure/read-back and responsive checks without altering Schedule or Workload.

Calendar control scale correction: The period context submit control was still receiving a legacy 36px/10px rule despite the page-level scale. Added a scoped override so the primary `�������� �������` action is 44px with 14px text, matching the Calendar touch target and the other focused controls.

Runtime verification: After copying `_admin_calendar.css`, precompiling Propshaft and restarting `schedule_web`, authenticated `/admin/operations` at 390px measured the context submit at 44px with 14px text. Document and client widths both measured 375px; no page overflow and zero fresh console errors were observed. The five Calendar navigation destinations remain visible and wrap to a 148px content-driven block at this width.

Remaining issue: Calendar and Accounts mutation/read-back and full accessibility/failure-state verification are still pending. The current pass has not changed Schedule or Workload.

Accounts runtime spot check: At authenticated 390px, `/admin/accounts` rendered without page overflow and without visible select controls. Opening `������� ������������` produced a native modal with the shared backdrop and initial focus on `������� ��������`; Escape closed it and returned focus to the create trigger. No fresh console errors were reported. This verifies sheet mechanics and responsive geometry only; account CRUD, validation and authorization remain pending.

Calendar entity fallback correction: Weekday Transfers now loads the existing student group catalog through the Rails gateway and presents visible group radio choices with `��� ������`; when the catalog is unavailable it explains that the transfer will apply to all groups instead of exposing a raw numeric ID field. Period Settings similarly presents an unavailable-catalog message instead of raw faculty or semester ID inputs.

Runtime verification: Ruby controller and ERB syntax passed. After copying the controller/views and restarting `schedule_web`, authenticated `/admin/weekday_transfers` at 390px rendered the group choices as radios, zero selects, one closed native create dialog, document/client width 375px and no overflow. Zero fresh console errors were observed.

Remaining issue: The visible group catalog is bounded inside the editor but still needs search for very large catalogs; CRUD read-back, invalid-date retention and full Calendar role/keyboard coverage remain pending.

Weekday Transfer catalog usability update: Added `choice_filter_controller.js` and a 40px local search field to the visible bounded group-choice list. The list remains radio-based, retains `��� ������`, and reports an explicit empty result state without introducing a dropdown or raw ID field.

Runtime verification: After correct Docker Compose deployment, authenticated `/admin/weekday_transfers` at 390px opened the native create sheet. The group search measured 40px; 101 visible options were filtered to 0 for a no-match query and the empty-state message became visible. The sheet retained zero selects, no document overflow and zero fresh console errors. Rails/ERB/Node syntax checks passed. Served assets included `controllers/choice_filter_controller-44c8b707.js` and `application-73804223.css`.

Remaining issue: Search currently filters the bounded catalog already loaded by the existing gateway; a server-backed full-catalog search is still outside the current API contract. CRUD/read-back and validation/conflict coverage remain pending.

Accounts sheet structure update: Wrapped create and edit content in the shared `admin-sheet__body` layout and applied a consistent 16px internal rhythm with 44px submit controls. Long account forms now scroll inside the sheet instead of bypassing the common editor geometry; table and account fields remain unchanged.

Runtime verification: After deployment, authenticated `/admin/accounts` at 390px opened the create sheet with a 664px scroll viewport and 949px content height, confirming internal scrolling. Initial focus remained on `������� ��������`; the page stayed at 375px document/client width with no overflow and zero fresh console errors. ERB syntax passed.

Remaining issue: Account mutation, validation/conflict retention, authorization and full search/read-back verification remain pending.

Desktop Calendar context composition: Committed period context now collapses into a readable summary showing faculty, semester and group, with an explicit Change context disclosure for the full radio selection form. This removes the always-expanded context wall while preserving all existing choices and URL parameters.

Runtime verification: After deployment, authenticated /admin/operations?faculty_id=1&semester_id=9&group_id=789 at 1440px showed the context summary at 56px and the four period cards beginning at y=352px. Opening the disclosure restored the full 535px selection form, with no document overflow and zero fresh console errors. The compact summary text rendered the selected faculty, semester and group correctly.

Remaining issue: Calendar CRUD success/read-back and conflict handling remain pending. Narrow behavior is deprioritized per the latest user direction; Schedule and Workload were not changed.

Desktop Accounts filter composition: On the PC layout, role and status choices now remain visible as horizontally scrollable choice strips rather than wrapping into a tall block. No option is hidden; the local strip preserves readable labels and keyboard reachability.

Runtime verification: At authenticated 1440px, the Accounts filter reduced from 281px to 114px and the six-column table moved from y=540px to y=374px. Document/client width remained 1425px with no overflow and zero fresh console errors. No dropdowns or table changes were introduced.

Desktop primary action scale: Standardized the focused Accounts, Resources and Calendar create actions to the 44px primary control role with 14px text. Existing table actions and schemas are unchanged.

Runtime verification: Authenticated 1440px checks measured ������� ������������, �������� ��������� and �������� ��������� ���� at 44px with 14px text. Document/client widths remained equal on Accounts, Posts and Holidays. The reservation route currently has no create action in its rendered unavailable-data state, so that action remains pending until the reservation data dependency is resolved.

Reservation runtime and desktop editor update: The previously unavailable reservation page was traced to `slices/admin/serializers/room_reservation_serializer.rb`, where `compact_blank` raised on the API runtime. The serializer now builds the teacher label with supported Ruby operations. The API syntax check passed, the API file was copied into the Compose container, and `api_geteway` was restarted. The authenticated reservation page now renders five rows and its existing five-column table.

Files changed (attributable): `apps/api_geteway/slices/admin/serializers/room_reservation_serializer.rb`, `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`, and `apps/schedule_web/app/assets/stylesheets/components/_admin_calendar.css`.

Runtime verification: After copying the Rails template/style into `schedule_web`, precompiling Propshaft and restarting through Docker Compose, authenticated `/admin/room_reservations` at 1440x900 rendered the table with five rows, no page overflow (1425/1425 content/client width) and zero fresh console errors. Each row measured 64px. The edit action opened a real native dialog sheet at x=841, width=560px, with the PATCH form inside the sheet, one-column field flow and a 44px Save control. The viewport screenshot is `admin-reservations-desktop-20260913.png` in the browser evidence output; the page snapshot is `.playwright-mcp/page-2026-09-13T18-37-20-853Z.yml`.

Table comparison: The five reservation columns and their order remain `Аудитория`, `Дата / слот`, `Преподаватель`, `Назначение`, `Действия`. Visible row values are separate from the action cell; edit/search/delete controls no longer expand the table row with the full form.

Focused desktop verification: At authenticated 1440px, `/admin/buildings` rendered 18 rows, `/admin/room_types` 16 rows, `/admin/accounts` 9 rows, and `/admin/operations` rendered the Calendar heading. Each checked page reported document width equal to client width and zero visible select elements. No fresh console errors were observed.

Remaining issue: Reservation CRUD success, validation/conflict retention and authoritative write read-back remain pending. Accounts and resource CRUD/read-back, and the broader Calendar mutation gates, also remain pending. The latest user direction makes desktop the implementation priority; Schedule and Workload were not changed in this slice.

Next concrete action: Continue the desktop UI/UX pass on the three requested workspaces, then perform the permitted existing mutation and read-back checks before marking any batch complete.
Shared dirty-editor behavior update: Replaced the browser two-choice confirmation in `admin_sheet_controller.js` with an in-sheet accessible alert dialog offering `Сохранить`, `Отменить изменения`, and `Продолжить редактирование`. Save submits the existing non-GET form, discard closes the sheet and clears the draft marker, and continue returns focus to the editor. Added scoped visual treatment in `_admin_components.css`.

Runtime verification: After copying the controller and stylesheet into `schedule_web`, precompiling Propshaft and restarting via Docker Compose, authenticated `/admin/accounts` at 1440px opened the create sheet, accepted a disposable draft email, and Escape displayed all three dirty actions. The prompt occupied the sheet without a nested native dialog. Discard closed the sheet, removed the prompt, and returned focus to `Создать пользователя`. The password field reported `autocomplete="new-password"` and no value. Zero fresh console errors were reported. Served assets included `controllers/admin_sheet_controller-9201fe44.js` and `application-7ac85af3.css`.

Remaining issue: Full mutation success, validation/conflict retention, search persistence while dirty, and authoritative read-back remain pending for the focused workspaces. This behavior was verified on Accounts; Calendar and Resources share the controller but still need equivalent dirty-form runtime checks.
Dirty-sheet cross-page verification: On authenticated `/admin/buildings` at 1440px, the first resource edit sheet accepted a disposable unsaved number change, Escape opened the shared three-action prompt, and `Отменить изменения` closed the sheet, returned focus to the row `Изменить` action, and left the authoritative row value unchanged. This confirms the shared dirty-close behavior also works for Resources. No business mutation was sent.
Calendar choice-label update: Weekday Transfer group choices were technically visible but all rendered as the same generic label. The view now uses the available speciality/group/year/course context to produce readable labels such as `МТ · 2022`, while retaining the radio identity and local search. Transfer table rows resolve selected group IDs through the same visible label map and show a neutral fallback instead of exposing a numeric ID.

Runtime verification: After copying the view into `schedule_web` and restarting Docker Compose, authenticated `/admin/weekday_transfers` at 1440px opened the create sheet with 101 group choices; the first choices were distinct (`Все группы`, `МТ · 2022`, `МТ · 2021`, `МВ · 2021`, `МО · 2021`). Zero generic `Учебная группа` labels remained, document/client width was 1440/1440, and no fresh console errors were reported. No business mutation was sent.

Remaining issue: The catalog still uses the existing bounded 100-item gateway result; server-backed pagination/search is outside the current contract and remains pending. Calendar CRUD read-back and failure/conflict verification remain pending.
Student Groups resource-shell update: Moved the permanent create form behind the shared `admin-sheet` action and moved each inline speciality/year editor into a native sheet. The three-column table remains table-first with visible speciality/year values and a compact action cell containing the semester link, edit action and delete action. Existing create/update/delete/semester routes are unchanged.

Runtime verification: After copying the view and `_admin_resources.css` into `schedule_web`, precompiling assets and restarting Docker Compose, authenticated `/admin/student_groups` at 1440px rendered 50 rows and 51 closed dialogs, with no visible select controls and document/client width 1425/1425. The first edit sheet measured 560px wide, used one form column, focused `Закрыть редактор`, and Escape returned focus to the row edit trigger. No fresh console errors were reported and no business mutation was sent.

Remaining issue: Student group CRUD success/read-back and companion group-semester editor verification remain pending. The desktop layout is the active priority per the latest user direction.
Group-semester editor update: The linked group-semester page now uses the shared sheet for parameter edits. Its five-column table keeps the identifier, semester, student count, parameters and actions visible, while the existing PATCH endpoint and Calendar link remain intact. Product labels were translated to Russian where the old `group-semester` wording was exposed.

Runtime verification: Authenticated `/admin/student_groups/1/semesters` at 1440px rendered eight rows and eight closed editor dialogs with zero visible select controls and document/client width 1425/1425. The first editor opened as a 560px native sheet with a one-column form, initial focus on `Закрыть редактор`, and zero fresh console errors. No business mutation was sent.

Remaining issue: Group-semester PATCH success/read-back and error retention remain pending.
Desktop route sweep: Authenticated Playwright navigation checked all 12 Resources routes (`posts`, `subjects`, `academic_titles`, `academic_degrees`, `activity_types`, `time_slots`, `week_types`, `building_types`, `buildings`, `rooms`, `room_types`, `student_groups`) plus Calendar `semesters`, `holidays`, `weekday_transfers`, and `room_reservations` at 1440px. Every route rendered a Russian heading and current content, had zero visible select elements, zero page-level horizontal overflow, and zero fresh console errors. Rendered row counts were 23, 50, 8, 39, 26, 7, 8, 10, 18, 37, 16, 50, 19, 2, 1, and 5 respectively. No business mutations were sent.

Remaining issue: These route checks establish desktop rendering and composition only. CRUD success, validation/conflict recovery, authorization boundaries, and authoritative read-back are still pending.
Shared sheet body normalization: Converted remaining Calendar and Resource create dialogs from the legacy disclosure body wrapper to `admin-sheet__body`, so create and edit sheets now share the same padding, internal scroll and form rhythm. This affected Buildings, Room Types, Rooms, Posts, Holidays, Semesters, Weekday Transfers and Room Reservations; endpoints and fields were unchanged.

Runtime verification: After explicit Docker Compose copies (the first PowerShell copy loop used incorrect root-relative paths and was corrected) and a schedule_web restart, authenticated desktop checks for Buildings, Holidays, Weekday Transfers and Room Reservations found zero legacy dialog body wrappers, shared sheet bodies on every dialog, no document overflow, and no fresh console errors. The `/admin/semesters` path was not a valid rendered target in this check; the established `/admin/operations/semesters` route remains the valid Calendar route.

Remaining issue: Full mutation and read-back gates remain pending. No responsive implementation work was added; desktop remains the active priority.
Corrected Calendar route verification: The valid semester route `/admin/operations/semesters` was rechecked after deployment. At 1440px it rendered `Учебные семестры`, 19 table rows, one shared sheet body, zero legacy dialog body wrappers, document/client width 1425/1425, and no fresh console errors. The earlier `/admin/semesters` probe was only a wrong route probe and is not treated as a runtime defect.

Current implementation status: Desktop visual composition and shared sheet mechanics are verified across the requested Accounts, Calendar and Resources workspaces. Business mutation/read-back, validation/conflict recovery and authorization role coverage remain open acceptance gates.
Final desktop visual evidence capture: Saved viewport screenshots for `/admin/accounts`, `/admin/operations/semesters`, and `/admin/buildings` as `admin-accounts-desktop-final-20260913.png`, `admin-calendar-semesters-desktop-final-20260913.png`, and `admin-resources-buildings-desktop-final-20260913.png` in the browser evidence output. These captures contain no passwords or one-time credentials.

Verification checks: `node --check app/javascript/controllers/admin_sheet_controller.js`, ERB compilation for Student Groups and group-semester templates, and scoped `git diff --check` passed. Compose reports `schedule_web` and `api_geteway` healthy.
Controlled resource mutation/read-back: Authenticated desktop `/admin/buildings` opened the first edit sheet, submitted its existing values unchanged through the real PATCH form, received `Здание обновлено.`, and closed the sheet. A fresh navigation to the same route retained the first row value and all 18 rows. The page still had zero visible selects and no fresh console errors. This was an idempotent write with no net data change.

Acceptance impact: The shared sheet now has one authoritative success/read-back verification for Resources. Other resource CRUD paths, validation/conflict retention and Calendar/Accounts mutations remain unverified.
## Focused continuation — reservation mutation read-back fix (2026-09-13)

- **Scope:** Calendar reservation editor; desktop administrator surface only. No Schedule/Workload source was changed for this slice.
- **Reproduced defect:** An unchanged edit of an existing reservation submitted valid fields, but the API returned 500 and Rails rendered a generic 422. API logs identified RoomReservationSerializer calling reservation.teacher on the bare record returned by RoomReservationRepo#update_with_associations.
- **Source change:** apps/api_geteway/slices/admin/repos/room_reservation_repo.rb now overrides the aggregate read relation with root.combine(:teacher). Mutation read-backs therefore hydrate the same teacher association already used by the filtered index relation.
- **Deployment/provenance:** Copied the attributable API repo file into the running api_geteway container and restarted that service with Docker Compose. No database reset or fixture cleanup. docker compose exec -T api_geteway ruby -c /app/slices/admin/repos/room_reservation_repo.rb returned Syntax OK.
- **Runtime route/role:** Authenticated super administrator, http://localhost:3000/admin/room_reservations, 1440px desktop browser.
- **Controlled write/read-back:** Opened the first visible reservation editor and submitted its retained values without changing them. Rails request POST /admin/room_reservations/5 with method override PATCH returned 303; API PATCH /admin/room_reservations/5 returned 200 and audit logging completed. Rails displayed Бронирование обновлено.; the refreshed list rendered normally.
- **Browser checks:** 0 console errors after the corrected mutation; reservation table remained visible with five rows. The earlier failing reservation 4 was preserved and no fallback or optimistic DOM success was introduced.
- **Remaining:** A full reservation create, conflict, invalid-date and forbidden-role journey remains pending. The focused desktop visual pass for Accounts, Calendar and Resources is complete at the inspected routes; broader role/concurrency coverage remains pending.
- **Next action:** Continue final evidence/status reconciliation for the three focused administrator sections without changing accepted Schedule/Workload composition.

## Focused continuation — desktop primary action refinement (2026-09-13)

- **Scope:** Accounts, Calendar and Resources desktop composition. Schedule and Workload were not changed.
- **Source change:** Scoped the three focused primary create actions to content width with 20px horizontal padding and preserved the 44px / 14px control role. This removes the full-canvas banner effect while retaining a clear single primary action.
- **Deployment/provenance:** Copied `_admin_accounts.css`, `_admin_calendar.css` and `_admin_resources.css` into the running `schedule_web` container, ran `rails assets:precompile`, and restarted `schedule_web` through Docker Compose. Served application CSS fingerprint: `application-e709f81f.css`.
- **Runtime routes/role/viewport:** Authenticated super administrator; `/admin/accounts`, `/admin/operations/semesters`, `/admin/buildings`; 1440px desktop.
- **Checks and exact results:** Accounts create action measured 203x44px at 14px; Calendar semester create measured 164x44px at 14px; Buildings create measured 164x44px at 14px. Accounts and Calendar headings remained 24px/32px. Buildings rendered one table with 18 data rows. All checked pages had document/client width 1425/1425 and zero fresh console errors.
- **Table comparison:** No table columns, order, headers, grouping or row meaning changed.
- **Remaining:** Full negative/conflict and role authorization journeys remain pending; this pass intentionally deprioritizes responsive work per the latest user direction.
- **Next action:** Continue focused desktop interaction verification for searchable selection, dirty drafts and safe mutation read-back across Calendar and Accounts.

## Focused continuation — searchable dirty draft retention (2026-09-13)

- **Scope:** Account create sheet interaction on desktop.
- **Runtime route/role/viewport:** Authenticated super administrator; `/admin/accounts`; 1440px.
- **Interaction check:** Opened `Создать пользователя`, entered a disposable email draft, searched teachers with `Pet`, selected the first result, then searched departments with `ПСи` while the sheet remained open. The result frames updated in place.
- **Exact result:** The native sheet stayed open; teacher hidden identity remained `1`; selected label became `Выбран преподаватель: Petrov Ivan Oleksandrovych`; the email draft remained `ui-search-draft@example.test`; the department result frame returned one result. No account submission was made.
- **Browser checks:** No fresh console errors. The sheet was closed without a business mutation.
- **Remaining:** Full account and Calendar invalid/conflict/role mutation coverage remains pending.

## Focused continuation — refined desktop evidence capture (2026-09-13)

- **Evidence:** Fresh full-page screenshots were captured after the scoped primary-action refinement: `admin-accounts-desktop-action-refined-20260913.png`, `admin-calendar-desktop-action-refined-20260913.png`, and `admin-resources-buildings-desktop-action-refined-20260913.png` in the Playwright evidence output.
- **Runtime check:** The final Resources check rendered the Russian `Здания` heading, an Add action at 164x44px, no page overflow (1440/1440), and zero console errors. Compose services remained healthy.
- **Table comparison:** Resource table inventory remains unchanged.

## Focused continuation — explicit search labels (2026-09-13)

- **Scope:** Accounts edit sheets and Calendar reservation search disclosures.
- **Source change:** Wrapped teacher and department edit search fields in explicit Russian labels and replaced placeholder-only wording with useful search guidance. Applied the same label treatment to reservation room and teacher search fields. GET parameters, Turbo frame targets and selection identity are unchanged.
- **Deployment/provenance:** Copied the two changed ERB templates into the running `schedule_web` container and restarted it through Docker Compose. Rails controller syntax check returned `Syntax OK`.
- **Runtime routes/role/viewport:** Authenticated super administrator; `/admin/accounts` and `/admin/room_reservations`; 1440px desktop.
- **Checks and exact results:** Account edit search inputs reported wrapped labels for teacher and department fields. Reservation search inputs reported wrapped labels `Поиск аудитории` and `Поиск преподавателя`; the reservation table rendered five rows. Both routes had no page overflow and zero fresh console errors.
- **Table comparison:** No table columns, order or row structure changed.
- **Remaining:** Full negative/conflict and role authorization journeys remain pending.

## Focused continuation — remove beige canvas (2026-09-13)

- **Scope:** Accounts, Calendar and Resources desktop workspaces only.
- **Source change:** Scoped the workspace and document canvas backgrounds to `var(--admin-paper)` in `_admin_resources.css` and `_admin_calendar.css`. The existing `--admin-panel` token and its accent/state uses remain intact; no public or accepted Schedule/Workload styling was changed.
- **Deployment/provenance:** Copied the changed styles into `schedule_web`, ran Propshaft asset precompilation, and restarted through Docker Compose. Served CSS fingerprint: `application-e9ea6b6a.css`.
- **Runtime routes/role/viewport:** Authenticated super administrator; `/admin/accounts`, `/admin/operations/semesters`, `/admin/buildings` and a Schedule regression check; desktop browser.
- **Checks and exact results:** Accounts, Calendar and Buildings reported page and body backgrounds `rgb(255, 255, 255)`, with no page overflow. Buildings rendered the Russian `Здания` heading and 18 rows with zero console errors. Schedule retained the original `rgb(247, 246, 243)` body canvas.
- **Evidence:** Fresh browser snapshots are in the Playwright evidence output for the three focused routes.
- **Remaining:** Full negative/conflict and role authorization journeys remain pending.

## Focused continuation — remove beige tone from focused surfaces (2026-09-13)

- **Scope:** Accounts, Calendar and Resources desktop workspaces only.
- **Source change:** On pages containing `.resources-page` or `.operations-page`, scoped `--admin-panel` to the cool neutral `#f3f5f6` and kept the workspace/document canvas on `var(--admin-paper)`. The global admin token remains unchanged.
- **Deployment/provenance:** Copied `_admin_resources.css` into `schedule_web`, precompiled Propshaft assets and restarted through Docker Compose. Served CSS fingerprint: `application-1665a1fe.css`.
- **Runtime checks:** Authenticated Accounts reported body/page backgrounds `rgb(255, 255, 255)` and focused panel token `#f3f5f6`; no console errors. Schedule regression check retained body background `rgb(247, 246, 243)` and panel token `#f7f6f3`.
- **Invariant:** No tables, routes, selectors, operations or public pages were changed.
- **Remaining:** Full negative/conflict and role authorization journeys remain pending.

## Focused continuation — sticky sheet actions (2026-09-13)

- **Scope:** Shared editor behavior for focused Accounts, Calendar and Resources sheets.
- **Source change:** Added a shared rule in `_admin_components.css` that keeps the existing non-GET form submit action sticky at the bottom of the scrolling sheet body. Account credential-generation actions are covered separately; search forms remain ordinary in-flow controls.
- **Deployment/provenance:** Copied the stylesheet into `schedule_web`, precompiled Propshaft assets and restarted via Docker Compose. Served CSS fingerprint: `application-6edb29ad.css`.
- **Runtime routes/role/viewport:** Authenticated super administrator; `/admin/accounts` and `/admin/room_types`; 1440px desktop.
- **Checks and exact results:** Room Type edit opened as a native dialog with a 44px sticky Save control and focus on the close button. Account create opened with a 720px scroll viewport and 803px content height; its 44px Save control computed as `position: sticky`. No fresh console errors.
- **Invariant:** Form endpoints, fields, tables and Schedule/Workload styling remain unchanged.
- **Remaining:** Full negative/conflict and role authorization journeys remain pending.

## Focused continuation — focused typography cleanup (2026-09-13)

- **Scope:** Accounts, Calendar and Resources desktop surfaces.
- **Source change:** Scoped legacy admin label rules so focused kickers, monitoring metadata, signed-in role metadata and the Calendar schedule link meet the prescribed minimum readable sizes. Calendar schedule action is now a 40px / 14px secondary action.
- **Deployment/provenance:** Copied `_admin_resources.css`, precompiled Propshaft and restarted `schedule_web` through Docker Compose. Served CSS fingerprint: `application-6f2cae43.css`.
- **Runtime routes/role/viewport:** Authenticated super administrator; `/admin/operations?faculty_id=1&semester_id=9&group_id=789` and `/admin/accounts`; desktop.
- **Checks and exact results:** Rendered leaf text below 11px count was zero on both routes. Calendar schedule action measured 235x40px at 14px. Calendar body remained white with 1440/1440 document/client width and zero fresh console errors; Accounts retained 1425/1425 width and zero fresh console errors.
- **Invariant:** Schedule was not changed; focused tables and field contracts are unchanged.
- **Remaining:** Full negative/conflict and role authorization journeys remain pending.

## 2026-09-13 — Focused desktop workspaces fill the available screen

- Status: completed for the focused desktop layout slice; no Schedule/Workload source changes.
- Finding addressed: Accounts, Calendar and Resources now explicitly stretch through the full Rails admin content column beside the fixed 224px sidebar. The page surfaces have no max-width or shrink-to-content behavior; tables retain their local scrolling behavior and the 24px internal gutter.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css` (scoped desktop full-workspace rule for Accounts, Calendar and Resources).
- Runtime provenance: deployed to the running `schedule_web` container with Docker Compose, assets precompiled as `application-6d14e6ec.css`, and the container restarted.
- Browser checks: authenticated Playwright session at 1440x900 visited `/admin/accounts`, `/admin/operations/semesters`, and `/admin/buildings`. Each focused page measured x=224, width=1201, right=1425, matching `.admin-main`; document scrollWidth/clientWidth both measured 1425. No visible `<select>` controls were present on these routes. Browser console was clear after the fresh checks.
- Visual evidence: `docs/design/admin-workbench-2026-09-13/evidence/accounts-fullscreen-1440.png`.
- Regression check: `/admin/schedule?faculty_id=1&semester_id=9` remained on the existing shell/content column; no Schedule source was edited.
- Remaining issue: the browser viewport still reserves the native vertical scrollbar width when the page is taller than the viewport; this is browser chrome, not a page width cap. The next focused UI pass should continue with visual polish inside this full-width canvas.
## 2026-09-13 — Accounts filter uses the full desktop canvas

- Status: completed for the Accounts desktop filter refinement.
- Finding addressed: the role filter no longer collapses into a narrow internal horizontal scroller. Role choices are now presented as one visible row across the full Accounts workspace; status choices and the search action occupy a clear second row.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Runtime provenance: copied the stylesheet into the running `schedule_web` container, precompiled Propshaft assets as `application-22515117.css`, and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900. `/admin/accounts` measured the filter at 1153px wide with role options 1119px wide, 40px high, `flex-wrap: nowrap`, and `overflow: visible`; document scrollWidth/clientWidth both measured 1425. The focused route had zero visible native selects and no console errors.
- Regression smoke check: `/admin/operations/semesters` and `/admin/buildings` still measured x=224, width=1201, right=1425, with no page overflow, no visible native selects and zero console errors.
- Visual evidence: `docs/design/admin-workbench-2026-09-13/evidence/accounts-fullscreen-current-1440.png`.
- Invariant: all six account table columns and their order remain unchanged; no Schedule/Workload source was edited.
- Remaining: complete negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Resources navigation aligned for the full desktop canvas

- Status: completed for the Resources navigation refinement.
- Finding addressed: the twelve reference destinations now use a deliberate six-column, two-row desktop grid. Labels and active state are aligned across the full workspace instead of forming an uneven trailing row.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css`.
- Runtime provenance: copied the stylesheet into the running `schedule_web` container, precompiled Propshaft assets as `application-d368bcd4.css`, and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/buildings`. Each navigation item measured 178x44px in six equal 177.5px tracks; all twelve labels remained visible, document scrollWidth/clientWidth both measured 1425, and the browser console had zero errors.
- Visual evidence: `docs/design/admin-workbench-2026-09-13/evidence/resources-fullscreen-current-1440.png`.
- Invariant: all existing navigation destinations and routes remain present; Buildings and Room Types table content and schemas are unchanged.
- Remaining: complete negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Calendar navigation aligned for the full desktop canvas

- Status: completed for the Calendar navigation refinement.
- Finding addressed: the five Calendar sections now use equal-width desktop tracks, making the navigation use the available workspace instead of clustering at the left.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_calendar.css`.
- Runtime provenance: copied the stylesheet into the running `schedule_web` container, precompiled Propshaft assets as `application-338b2aaf.css`, and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/operations/semesters`. Each Calendar destination measured 215x44px across five equal tracks; page measured x=224, width=1201, right=1425; document scrollWidth/clientWidth both measured 1425; console had zero errors.
- Visual evidence: `docs/design/admin-workbench-2026-09-13/evidence/calendar-fullscreen-current-1440.png`.
- Invariant: all five Calendar destinations, routes, table columns and calendar semantics remain unchanged.
- Remaining: complete negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Focused route sweep after desktop navigation refinements

- Status: completed for the current desktop visual sweep; deeper mutation and authorization gates remain pending.
- Runtime routes checked in the authenticated Playwright session at 1440x900: Resources `posts`, `subjects`, `academic_titles`, `academic_degrees`, `activity_types`, `time_slots`, `week_types`, `building_types`, `buildings`, `rooms`, `room_types`, `student_groups`; Calendar `operations/semesters`, `holidays`, `weekday_transfers`, and `room_reservations`.
- Exact results: every route rendered its Russian page heading; focused pages measured the full available desktop column (x=224, width=1201 where the vertical scrollbar was present, or width=1216 when absent); document width matched client width on each sample; no visible native `<select>` control was found; fresh browser console checks returned zero errors.
- Source check: focused templates contain no `<select>`, `select_tag`, `collection_select` or `options_for_select` usage in the audited route families.
- Content checks: Buildings and Room Types rendered their tables and edit dialogs; Reservations rendered its table and six editor dialogs; all existing navigation destinations remained reachable.
- Evidence: refreshed desktop captures are in `docs/design/admin-workbench-2026-09-13/evidence/` (`accounts-fullscreen-current-1440.png`, `calendar-fullscreen-current-1440.png`, `resources-fullscreen-current-1440.png`).
- Invariant: table schemas, route contracts and existing Schedule/Workload source remain unchanged.
- Remaining: focused write journeys beyond the previously verified reservation read-back, plus negative/conflict and role authorization coverage, remain pending.
## 2026-09-13 — Focused editor IDs and modal semantics cleaned up

- Status: completed for the focused editor accessibility refinement.
- Finding addressed: repeated hidden editor forms no longer reuse HTML IDs. Accounts, Reservations and Buildings now generate unique IDs for repeated search fields, hidden identity fields, scope fields, dates, time slots, purpose fields, status controls and building type/number fields.
- Attributable source: `apps/schedule_web/app/views/admin/accounts/index.html.erb`, `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`, and `apps/schedule_web/app/views/admin/resources/buildings/index.html.erb`.
- Runtime provenance: copied the three templates into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900. Accounts, Reservations and Buildings reported zero duplicate IDs; Reservations rendered five rows and Buildings rendered 18 rows with 19 dialogs. Each route had no horizontal overflow and zero console errors.
- Modal check: the create editor on each route opened as a native modal (`dialog.open=true`, `:modal=true`) with its `aria-labelledby` heading and a focused editor control.
- Invariant: request names, route contracts, table columns and record identity values were preserved; no Schedule/Workload source was edited.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Visible field labels completed in Calendar and Buildings sheets

- Status: completed for the focused form semantics refinement.
- Finding addressed: new and edit Reservation sheets now expose visible Russian labels for room search, teacher search, reservation date and purpose. Building create/edit sheets now label the building number field explicitly. Placeholder text remains supportive guidance only.
- Attributable source: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb` and `apps/schedule_web/app/views/admin/resources/buildings/index.html.erb`.
- Runtime provenance: copied both templates into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 opened both create sheets. Reservations reported visible labels `Поиск аудитории`, `Поиск преподавателя`, `Дата бронирования` and `Назначение`; Buildings reported `Номер здания`. Both opened as native modal dialogs, had zero duplicate IDs, no horizontal overflow and zero console errors.
- Invariant: request names, table schemas, routes and selection identities remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Room and Room Type editors made record-safe

- Status: completed for the explicit Resources room editor refinement.
- Finding addressed: repeated room and room-type sheets no longer reuse generated radio/input IDs. Create and edit forms now use unique IDs per record and catalog choice, and text fields have visible Russian labels for room number/name and room-type name.
- Attributable source: `apps/schedule_web/app/views/admin/resources/rooms/index.html.erb` and `apps/schedule_web/app/views/admin/resources/room_types/index.html.erb`.
- Runtime provenance: copied both templates into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900. Rooms rendered 37 rows and Room Types rendered 16 rows; both create sheets opened as native modal dialogs, reported zero duplicate IDs, no horizontal overflow and zero console errors.
- Invariant: table columns, routes, request parameter names and catalog identities remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Time Slot editor values normalized for native controls

- Status: completed for the generic Resources editor runtime cleanup.
- Finding addressed: Time Slot edit inputs previously received values such as `2026-`, which are invalid for native `input[type=time]` controls. The generic template now extracts the `HH:mm` portion for both the table display and edit fields.
- Attributable source: `apps/schedule_web/app/views/admin/resources/posts/index.html.erb`.
- Runtime provenance: copied the template into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/time_slots`. Existing edit values rendered as valid `08:30`, `10:00`, `10:10`, `11:35` examples; invalid time values count was zero, duplicate ID count was zero, page width matched client width at 1425, and the browser returned zero warnings and zero errors.
- Invariant: time-slot table meaning, stored parameter names, routes and row count (7) remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Student Group editor made record-safe

- Status: completed for the remaining high-volume Resources editor.
- Finding addressed: Student Group specialty radios and year fields now have unique record-scoped IDs. Create fields for admission year, student count and semester duration have explicit Russian labels and clearer guidance.
- Attributable source: `apps/schedule_web/app/views/admin/student_groups/index.html.erb`.
- Runtime provenance: copied the template into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/student_groups`. Fifty rows rendered; duplicate ID count was zero; the create sheet opened as a native modal; visible labels included `Год набора`, `Количество студентов` and `Длительность семестра`; document width matched client width at 1425 and the console had zero errors.
- Invariant: group table columns, semester links, routes, request names and specialty identities remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Group Semester editor labels and IDs completed

- Status: completed for the remaining group-semester editor surface.
- Finding addressed: repeated group-semester sheets no longer reuse hidden group, student-count or duration field IDs. The numeric fields now use visible Russian labels and record-scoped IDs.
- Attributable source: `apps/schedule_web/app/views/admin/student_groups/semesters.html.erb`.
- Runtime provenance: copied the template into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/student_groups/1/semesters`. Eight rows rendered; duplicate ID count was zero; all sixteen editor fields had explicit labels (`Количество студентов`, `Длительность семестра`); page width matched client width at 1425 and the console had zero errors.
- Invariant: the five-column group-semester table, group identity, semester links, routes and request names remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Week Type editor no longer leaves an orphan field label

- Status: completed for the generic Resources conditional-form cleanup.
- Finding addressed: Week Type sheets previously rendered a `Короткое название` label without an input because the conditional was applied only to the field helper. The generic template now conditionally renders the entire label/field pair.
- Attributable source: `apps/schedule_web/app/views/admin/resources/posts/index.html.erb`.
- Runtime provenance: copied the template into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on Week Types, Posts and Time Slots. Week Types reported zero orphan `Короткое название` labels, zero duplicate IDs and no overflow; all three routes had zero console errors.
- Invariant: Week Type name/code fields, generic catalog schemas, routes and request names remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Focused table actions use the compact control role

- Status: completed for the focused desktop action-density refinement.
- Finding addressed: row-level Edit/Delete and reservation/account row actions now use the prescribed compact 36px control role, while primary actions and sheet Save controls retain their larger 40–44px sizing.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css`.
- Runtime provenance: copied the stylesheet into the running `schedule_web` container, precompiled Propshaft assets as `application-a6a7e7f3.css`, and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on Buildings, Accounts and Reservations. First row actions measured 36px high at 13px/18px; each route remained width-safe at 1425/1425 and fresh console checks returned zero errors.
- Invariant: row action meaning, table columns, editor triggers and destructive-action separation remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Main Calendar workspace navigation expanded

- Status: completed for the main Calendar operations navigation slice.
- Finding addressed: `Периоды расписания` used the older left-clustered navigation while Calendar catalog pages used the full-width treatment. The operations route now presents all five Calendar destinations in equal desktop tracks.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_calendar.css`.
- Runtime provenance: copied the stylesheet into the running `schedule_web` container, precompiled Propshaft assets as `application-9f8dd603.css`, and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/operations?faculty_id=1&semester_id=9&group_id=789`. Five tabs measured 218x44px, spanning x=272 through x=1392 inside the 1216px workspace; page width matched the viewport and console errors were zero.
- Visual evidence: `docs/design/admin-workbench-2026-09-13/evidence/calendar-operations-current-1440.png`.
- Invariant: Calendar routes, period cards, context identity and table semantics remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.
## 2026-09-13 — Focused table regions are named and keyboard-reachable

- Status: completed for the focused table navigation semantics.
- Finding addressed: dense table containers now expose a named `region` landmark and `tabindex="0"`, allowing keyboard users to reach the local scrolling surface without changing table columns or converting rows to cards.
- Attributable source: focused table templates under `apps/schedule_web/app/views/admin/accounts`, `app/views/admin/resources`, `app/views/admin/room_reservations`, `app/views/admin/holidays`, `app/views/admin/semesters`, and `app/views/admin/student_groups`.
- Runtime provenance: copied the changed templates into the running `schedule_web` container and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on Accounts, Reservations, Buildings and Student Groups. Each table card reported `role=region`, a heading reference through `aria-labelledby`, and `tabindex=0`; programmatic focus landed on the region; document width remained equal to client width and fresh console checks returned zero errors.
- Invariant: table columns, grouping, row meaning and local horizontal scrolling behavior remain unchanged.
- Remaining: full negative/conflict and role authorization journeys remain pending.## 2026-09-13 — Full-width focused workspaces and served table focus treatment

- Status: completed for the requested desktop composition refinement on Accounts, Calendar and Resources.
- Finding addressed: the focused administrator pages now use the available desktop canvas with a white main surface, equal-width Calendar/Resources navigation tracks, and keyboard-reachable table regions. The new scoped table-region focus rule is scoped to the focused admin workspaces.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css`, `app/assets/stylesheets/components/_admin_calendar.css`, `app/assets/stylesheets/components/_admin_accounts.css`, and the focused table templates listed in the preceding handoff entry.
- Runtime provenance: the latest Rails assets were precompiled in the running `schedule_web` container as `application-4013baf1.css`, then the service was restarted through Docker Compose.
- Browser checks: authenticated Playwright session at 1440x900 on `/admin/accounts`, `/admin/room_reservations`, and `/admin/buildings`. Headings rendered in Russian; each route reported a 1201px main canvas within a 1440px viewport, white body background, no horizontal page overflow, and a focusable named table region; fresh console errors were zero. Programmatic focus reached the regions, while visual `:focus-visible` activation remains pending a real Tab sequence. Ruby controller syntax checks returned `Syntax OK` for Accounts and Room Reservations.
- Visual evidence: `docs/design/admin-workbench-2026-09-13/evidence/accounts-fullscreen-current-1440.png`, `calendar-fullscreen-current-1440.png`, `resources-fullscreen-current-1440.png`, and `calendar-operations-current-1440.png`.
- Invariant: Schedule source and composition were not changed by this slice; table schemas, columns, ordering, row meanings, routes and operation contracts remain unchanged.
- Remaining: mutation read-back, invalid/conflict handling, role coverage, and full browser acceptance across all prescribed viewports remain pending. Next action is a focused interaction pass for the three requested workspaces.## 2026-09-13 — Table-region focus ring uses an existing semantic token

- Status: completed for the focused table keyboard indication.
- Finding addressed: the first scoped focus rule referenced an undefined token and therefore computed to no visible outline. It now uses the existing `--velvet` semantic color with a 2px outline and 3px offset.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css`.
- Runtime provenance: copied the corrected stylesheet into `schedule_web`, precompiled Propshaft assets as `application-80cd91bd.css`, and restarted through Docker Compose.
- Browser checks: authenticated Playwright session at `/admin/accounts` on 1440x900 used `focus({ focusVisible: true })`; the named table region remained focused and computed `rgb(75, 38, 47) solid 2px` with a 3px offset. Fresh console errors were zero.
- Invariant: no table structure, columns, row meaning, navigation or Schedule styling was changed.
- Remaining: full mutation read-back, invalid/conflict handling and role coverage remain pending.## 2026-09-13 — Temporary account-password generation no longer returns 500

- Status: completed for the Accounts credential-generation regression.
- Finding addressed: UUID account records were incorrectly coerced with `Integer(id)` in the Rails Accounts gateway, and the controller used an unavailable `ActiveModel::Type::Boolean` constant while parsing the submitted generation flag. Together these caused the Generate temporary password action to fail before the API update operation.
- Attributable source: `apps/schedule_web/app/lib/gateways/admin/accounts_gateway.rb` and `app/controllers/admin/accounts_controller.rb`.
- Runtime provenance: copied the corrected Rails source into the running `schedule_web` container and restarted through Docker Compose. No API contract or database schema was changed.
- Browser checks: authenticated Playwright opened Accounts, opened an existing account editor, and submitted the real Russian `Сгенерировать временный пароль` action. The result page title was `Временный пароль`; an authenticated same-origin form submission returned HTTP 201 with `Cache-Control: no-store, max-age=0` and `Pragma: no-cache`. The response body and generated credential were not inspected or captured. Fresh browser errors were zero on the successful request path.
- Invariant: account UUID identity, PATCH `/auth/accounts/:id`, one-time credential behavior, password omission from drafts and API serializer, and role/scope authorization remain unchanged.
- Remaining: invalid/conflict and forbidden-role coverage for Accounts remains pending.## 2026-09-13 — Accounts validation failures reopen the same editor

- Status: completed for the Accounts safe-draft interaction slice.
- Finding addressed: a failed account create/update response preserved submitted values in the HTML but returned the workspace with every editor closed. The shared sheet controller now accepts an optional failed-editor ID and reopens that native dialog after the response is rendered.
- Attributable source: `apps/schedule_web/app/javascript/controllers/admin_sheet_controller.js` and `app/views/admin/accounts/index.html.erb`.
- Runtime provenance: copied the controller and template into `schedule_web` and restarted through Docker Compose; the previous UUID gateway and boolean parsing fixes remain deployed.
- Browser checks: authenticated Playwright opened the first account editor, submitted a deliberately invalid email through the real Save path, and received HTTP 422. The response rendered `data-admin-sheet-open-id-value` without escaped quotes; the same dialog reported `open=true` and `:modal=true`, retained `invalid-email`, and retained zero password values. The 422 network entry was the expected validation response; no 500 occurred. Ruby and JavaScript syntax checks passed.
- Invariant: passwords remain excluded from drafts, generation remains one-time/no-store, UUID identity and API contracts are unchanged, and table structure is untouched.
- Remaining: Accounts forbidden-role and conflict coverage, plus representative Resources/Calendar failure-retention journeys, remain pending.## 2026-09-13 — Reservation validation reopens the Calendar sheet

- Status: completed for the Calendar reservation safe-draft interaction slice.
- Finding addressed: reservation create/update already retained a safe draft on recoverable failure, but the native editor was closed after the 422 response. The view now passes the failed create/update editor ID to the shared sheet controller.
- Attributable source: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`.
- Runtime provenance: copied the template into `schedule_web` and restarted through Docker Compose.
- Browser checks: authenticated Playwright opened `Бронирования аудиторий`, submitted an intentionally incomplete reservation through the real `Забронировать` action, and received HTTP 422. The create sheet reopened with `open=true` and `:modal=true`; date and purpose drafts remained present as empty values, and no reservation was created. Fresh browser errors were zero for this path; Ruby syntax checks passed.
- Invariant: room/teacher person identity, existing reservation fields, table columns and reservation API contracts remain unchanged.
- Remaining: conflict/forbidden reservation coverage and representative Resources failure-retention remain pending.## 2026-09-13 — Generic Resources failures retain the active sheet draft

- Status: completed for the generic Resources create/edit failure-retention slice.
- Finding addressed: Posts, Subjects, Activity Types, Building Types, Time Slots and Week Types redirected after failed create/update requests, discarding the active sheet context. The controller now keeps submitted safe attributes, reloads the current catalog, returns HTTP 422, and passes the failed editor ID to the shared native sheet controller. The generic template uses the retained values for both create and edit fields.
- Attributable source: `apps/schedule_web/app/controllers/admin/resources/posts_controller.rb` and `app/views/admin/resources/posts/index.html.erb`.
- Runtime provenance: copied the controller and template into `schedule_web` and restarted through Docker Compose.
- Browser checks: authenticated Playwright rendered Posts at 1440x900 with 24 editors, a 1201px main canvas and no initial console errors. An intentionally empty create submission returned 422 and reopened `new-resource-editor` as a modal with the empty safe draft and Russian feedback. An intentionally empty edit submission returned 422 and reopened `edit-resource-posts-0` as a modal with the empty retained name and feedback. The two 422 network entries were expected validation responses; no record was created or changed. Ruby syntax passed.
- Invariant: resource schemas, routes, API operations, table columns and existing Russian labels remain unchanged.
- Remaining: dedicated Buildings/Rooms/Room Types failure retention and conflict/forbidden coverage remain pending.## 2026-09-13 — Dedicated Resources editors retain relationship drafts

- Status: completed for Buildings, Rooms and Room Types failure retention.
- Finding addressed: dedicated resource controllers redirected after failed create/update operations. They now retain submitted attributes, reload the catalog context, return HTTP 422 and reopen the corresponding native sheet. Radio relationships for building type, room building/type and room-type activity are restored from the safe draft.
- Attributable source: `apps/schedule_web/app/controllers/admin/resources/buildings_controller.rb`, `rooms_controller.rb`, `room_types_controller.rb`, and their three `index.html.erb` views.
- Runtime provenance: copied all six changed files into `schedule_web` and restarted through Docker Compose.
- Browser checks: authenticated Playwright rendered Buildings, Rooms and Room Types at 1440x900. All reported a 1201px main canvas, no horizontal overflow, zero visible native selects, and zero initial console errors. An intentionally incomplete Room Type create submission returned 422, reopened the native `new-resource-editor` with `open=true` and `:modal=true`, retained the empty name and no activity selection, and displayed Russian failure feedback. Ruby syntax checks passed for all four Resources controllers.
- Invariant: resource identities, relationship IDs, routes, table schemas and existing catalog operations remain unchanged; no record was created by the negative-path check.
- Remaining: dedicated Buildings/Rooms negative-path browser checks, conflict/forbidden coverage and successful CRUD read-back remain pending.

## 2026-09-13 — Calendar period validation retains the affected card draft

- Status: completed for the Calendar period validation slice; the broader Calendar batch remains in progress.
- Source: `apps/schedule_web/app/controllers/admin/period_settings/periods_controller.rb` now renders the current Calendar context on recoverable period failures instead of redirecting; `app/views/admin/period_settings/show/show.html.erb` uses the submitted dates for the affected card while preserving the persisted delete action.
- Runtime provenance: deployed to the `schedule_web` container with Docker Compose and restarted; the served page was `http://localhost:3000/admin/operations?faculty_id=1&semester_id=9&group_id=789`, title `Календарь периодов`, Russian document locale.
- Browser evidence: at the authenticated administrator route, submitted the first period card with `2026-12-31` as start and `2026-01-01` as end. The response was HTTP 422, retained both values, kept all four period cards rendered, kept the same URL/context, and displayed `Даты периода некорректны.`.
- Layout check: the served page measured 1216px for the main workspace at the desktop browser viewport and had no document-level horizontal overflow. Screenshot: `docs/design/admin-workbench-2026-09-13/evidence/calendar-periods-current.png`.
- Verification: Ruby syntax checks passed for both period controllers. Browser console contained only the expected failed-request entry for the deliberate 422 validation check; no 500 occurred after the renderer fix.
- Remaining issue: the full Calendar mutation/read-back matrix, including valid period persistence, reservations and weekday-transfer operations, remains to be completed and verified.
- Next action: continue with the remaining focused Calendar/Resources/Accounts visual and runtime gates, preserving the accepted Schedule composition.


## 2026-09-13 — Calendar period field labels brought to the readable admin scale

- Status: runtime-verified visual slice.
- Source: `apps/schedule_web/app/assets/stylesheets/components/_admin_calendar.css`; added a Calendar-scoped rule for period card labels at 12px/18px, leaving the accepted Schedule and public styles untouched.
- Runtime provenance: copied the stylesheet into `schedule_web`, ran Rails asset precompile, and restarted the container. Served application fingerprint: `application-15c29552.css`.
- Browser checks: authenticated `/admin/operations?faculty_id=1&semester_id=9&group_id=789` at 1440x900; computed period labels were 12px/18px, date inputs 14px and 44px high, Save buttons 44px high, and console errors were zero.
- Evidence: `docs/design/admin-workbench-2026-09-13/evidence/calendar-periods-readable-labels.png`.
- Table/layout invariant: no table structure changed; the four period editor units remain separate and the desktop document has no horizontal overflow.
- Remaining issue: the complete mutation/read-back and cross-page acceptance matrix for Calendar, Resources and Accounts is still pending.
- Next action: continue the focused visual/runtime audit on Resources and Accounts, then verify the remaining Calendar routes and editor states.

## 2026-09-19 — Excel import workspace

- Status: source-complete; runtime verification blocked by the pre-existing stopped API/PostgreSQL stack.
- Attributable source: `apps/schedule_web/app/controllers/admin/excel_imports_controller.rb`, `app/lib/gateways/admin/excel_imports_gateway.rb`, `app/javascript/controllers/excel_import_controller.js`, `app/views/admin/excel_imports/`, `app/assets/stylesheets/components/_admin_excel_imports.css`, scoped navigation/routes, and the API Excel-file serializer/upload service plus migration `20260919000000_add_original_filename_to_excel_files.rb`.
- Behaviour: a super administrator can open `Импорт Excel`, drag one `.xls` or `.xlsx` file into the visible workspace, retain the current semester context when present, see a paginated status history, refresh manually, receive five-second polling while uploads are pending, and delete a file after confirmation. Rails keeps the API token server-side; no file picker, dropdown, WebSocket, worker rewrite, or public-UI styling was introduced.
- API contract: Rails uses `GET /admin/files`, multipart `POST /admin/uploads/excel`, and `DELETE /admin/files/:id`. The new immutable `original_filename` column/projection keeps the source file name visible after the worker changes `title` to its detected structure name.
- Verification: Ruby syntax checks passed for the changed Rails controller/gateways/HTTP client and API service/serializer/migration; JavaScript syntax passed for the Stimulus controller. Runtime route, authenticated browser, upload/read-back, polling, deletion, asset, and migration checks remain unverified because `api_geteway` and `postgres` were already stopped and their existing logs show an incomplete database migration state. No storage reset or unrelated migration was attempted.
- Next action: restore the existing API/PostgreSQL environment, apply only the intended migration after confirming the outstanding migration set, rebuild the API and Rails assets, then perform the authenticated drag-upload → status polling → authoritative read-back → delete journey.

## 2026-09-19 — Excel import runtime recovery

- Status: service recovery completed; authenticated workflow verification remains pending.
- Runtime: rebuilt and restarted `api_geteway` and `schedule_web` with Docker Compose. Both containers report healthy, Rails `/up` returns successfully from inside the application container, and `GET /admin/files` now returns its expected unauthenticated `401` response rather than a server error.
- Database: applied only `20260919000000_add_original_filename_to_excel_files.rb` to the running PostgreSQL database. The `excel_files.original_filename` column is present and the migration is recorded, resolving the serializer/database schema mismatch that caused the 500 response.
- Remaining: verify the complete authenticated administrator journey: open the workspace, drag-upload an Excel file, observe status polling and authoritative read-back, then delete it.

## 2026-09-19 — Excel import 500 repair

- Status: fixed and deployed.
- Root cause: authenticated `GET /admin/excel_imports` raised `Dry::Container::KeyError` for `gateways.admin.excel_imports` before it could call the API. The gateway class existed, but its dependency-container registration was omitted.
- Fix: registered `Gateways::Admin::ExcelImportsGateway` in `apps/schedule_web/config/initializers/container.rb`, rebuilt the Rails image, and recreated `schedule_web`.
- Verification: Rails health check succeeds; the running container resolves and instantiates `ScheduleWeb::Container["gateways.admin.excel_imports"]` as `Gateways::Admin::ExcelImportsGateway`; no new Excel-import `KeyError` or 500 entries appear after the rebuild.

## 2026-09-19 — Excel import template route repair

- Status: fixed and deployed.
- Root cause: after the container registration was corrected, `app/views/admin/excel_imports/index.html.erb` still called `refresh_admin_excel_imports_path`. The named route generated by Rails is `admin_refresh_excel_imports_path`, so the signed-in page raised `NoMethodError` during rendering and returned 500.
- Fix: replaced the invalid helper, rebuilt the Rails image, and recreated `schedule_web`.
- Verification: Rails health check succeeds. The actual Excel-import template now renders inside the rebuilt Rails container with a successful file-list outcome and produces the expected `/admin/excel_imports/refresh` URL.

## 2026-09-19 — Excel import authenticated controller repair

- Status: fixed and deployed.
- Root cause: the authenticated `GET /admin/excel_imports` path received `Success<Array>` from `ExcelImportsGateway#semesters`, while `selected_semester_label` treated the value as a `Resilience::Outcome` and called `.data`. Live Rails logs captured `NoMethodError: undefined method 'data' for an instance of Array` at `excel_imports_controller.rb:63`.
- Fix: the controller now consumes the gateway's actual array contract with `Array(@semesters_result.value!)` before selecting the current semester.
- Verification: rebuilt and recreated `schedule_web`; Rails and API containers are healthy. Runtime checks inside the deployed Rails image cover the successful semester label, successful empty file list, upstream-failure state, template refresh URL and generated routes. The exact unauthenticated localhost route returns the expected login redirect, and post-rebuild logs contain no new Excel-import exception or 500.


## 2026-09-13 — Focused Resources and Accounts desktop pass rechecked

- Status: runtime-verified visual audit.
- Routes: `/admin/buildings`, `/admin/room_types`, `/admin/rooms`, `/admin/posts`, and `/admin/accounts`, authenticated as the existing administrator at 1440x900.
- Results: Buildings and Room Types render their content lists and shared navigation; each route uses the full 1201px main workspace beside the retained dark sidebar. Accounts renders the six-column table-first layout with the create action separated from row geometry.
- Interaction checks: zero visible native selects on all sampled focused routes; no initial alert state; no document overflow beyond the desktop shell. Accounts has no open row editor on initial load, and each edit action is represented as a separate dialog.
- Evidence: `docs/design/admin-workbench-2026-09-13/evidence/resources-buildings-current.png`, `docs/design/admin-workbench-2026-09-13/evidence/accounts-current.png`.
- Table invariant: resource and account table column meanings remain visible; no cards or hidden columns were introduced.
- Remaining issue: representative successful Resource/Calendar CRUD read-back and complete role/scope coverage remain pending.
- Next action: continue mutation-safe editor verification and address any concrete rendered defect found in the focused routes.
## 2026-09-20 — Staff date-resolved aggregate schedules and Schedule context

- Status: source-complete and runtime-verified for the faculty aggregate read and Rails rendering; department scope and full mutation/browser matrix remain pending.
- Functional slice: added staff-authorized date-resolved faculty and department occurrence endpoints in Hanami, reusing the occurrence-window transfer/cancellation semantics. Added the Rails gateway, operation, presenter, route, navigation item and Russian aggregate table with selected-date printing.
- UX slice: made the Schedule frame commit its selected context to browser history and constrained the planner inspector with its own viewport and sticky primary action so long editors remain operable.
- Runtime provenance: rebuilt `api_geteway` and `schedule_web` through Docker Compose; Rails `/up` returned 200, the aggregate route returned 200 for an authenticated faculty request and rendered two date-resolved occurrences, and unauthenticated access returned 302. Hanami routes, Rails routes and changed Ruby/JavaScript syntax checks passed.
- Attributable revisions: Rails `e3e3408`, `c915abc`; API `abb2dcd`, `27c31f9`.
- Runtime follow-up: direct authenticated API checks returned 200 for both faculty and department occurrence windows, 422 for an invalid ISO date, and 401 without a token. Rails rendered the department page with the selected department label and two lessons for the selected date.
- Remaining: verify department authorization/printing with a scoped account, moved/cancelled fixtures, copied URL Back/Forward behavior in a live browser, and continue B01/B04–B06 visual/runtime slices. Performance and availability measurements remain deferred by product decision.

## 2026-09-20 — Narrow-shell disclosure and heading consistency

- Status: source-complete and deployed.
- Finding addressed: secondary Grafana/Prometheus/Loki links consumed the narrow administrator shell, and Teachers/Schedule headings used larger page-specific scales than the shared workbench.
- Attributable source: `apps/schedule_web/app/views/admin/shared/_sidebar.html.erb`, `app/javascript/controllers/monitoring_disclosure_controller.js`, and `app/assets/stylesheets/components/_admin_workspace.css`.
- Behavior: monitoring links remain open on desktop and become an accessible collapsed disclosure at widths up to 760px; Schedule, aggregate Schedule and Teachers headings use the shared 24px/32px desktop role and 20px/28px narrow role.
- Runtime provenance: rebuilt and recreated `schedule_web`; `/up` returned 200, the served page contains the new Stimulus controller fingerprints, and the aggregate route still renders its date table.
- Remaining: browser-computed narrow measurements and the complete B01/B04–B06 acceptance matrix still require a functioning authenticated Playwright session.

## 2026-09-20 — Workload editor primary action reachability

- Status: source-complete and deployed.
- Finding addressed: long workload create/edit/assignment sheets required scrolling to reach their primary save action.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_workload.css`.
- Behavior: the existing server-backed primary action remains inside the editor form and now stays available at the bottom of the sheet while its body scrolls; no form fields, contracts or table columns changed.
- Runtime provenance: Rails image rebuilt and recreated; `/up` returned 200 and `rails zeitwerk:check` passed. Rails revision: `32e6a1a`.
- Remaining: browser bounding-box confirmation and complete workload failure/read-back coverage remain pending.

## 2026-09-20 — Lesson-transfer calendar rendering repair

- Status: fixed and runtime-verified.
- Finding: the dated lesson-transfer workspace called the missing `ru.date.formats.long` translation and returned HTTP 500 whenever two dates and a group were selected.
- Fix: replaced the unavailable localized formatter with an explicit Russian numeric date presentation while preserving the two timetable schemas, transfer controls and ISO values submitted to the API.
- Verification: authenticated `/admin/transfers?semester_id=1&faculty_id=1&group_semester_id=1&left_date=2026-09-21&right_date=2026-09-22` now returns HTTP 200 and renders both dated grids, lessons and transfer actions. Rails revision: `b968316`.
- Remaining: mutation/read-back, conflict handling and browser keyboard/drag acceptance remain pending.

The Russian locale now also defines the shared `date.formats.long` (`ДД.ММ.ГГГГ`) used by remaining date presenters, preventing the same missing-translation failure in future calendar/public render paths. Rails revision: `9287586`.

## 2026-09-20 — Weekday-transfer validation draft retention

- Status: source-complete and deployed; authenticated negative-path browser confirmation remains pending.
- Behavior: recoverable weekday-transfer failures now carry the safe submitted date, weekday, optional group and reason back through the redirect, reopen the transfer sheet, and restore the selected controls. No credentials or unrelated data are stored.
- Attributable source: `apps/schedule_web/app/controllers/admin/weekday_transfers_controller.rb` and `app/views/admin/weekday_transfers/index.html.erb`; Rails revision `2a78492`.
- Verification: ERB generation, diff checks and Docker rebuild passed; the Hanami contract independently returns `422` for an invalid date/weekday payload and creates no record.
- Remaining: authenticated Rails 422 flow, successful create/delete read-back and conflict coverage remain pending.

## 2026-09-20 — Aggregate schedule context filtering repair

- Status: source-complete and deployed; authenticated browser interaction remains pending with the unavailable Playwright transport.
- Finding: faculty search and its option list were mounted as separate `choice-filter` controller instances, so typing could not filter the list and could raise a missing-target error.
- Behavior: faculty and department aggregate-schedule catalogs now share one controller instance per search region, expose labelled Russian search fields, hide non-matching options, and show an empty-result message without changing the selected scope or table schema.
- Attributable source: `apps/schedule_web/app/views/admin/aggregate_schedules/show.html.erb`; Rails revision `072ad46`.
- Verification: ERB generation, `git diff --check`, Docker rebuild, Rails `zeitwerk:check`, and controller syntax check passed.
- Remaining: live keyboard filtering, selected-scope navigation and full aggregate mutation/read-back evidence remain pending.

## 2026-09-20 — Notice narrow-table semantics repair

- Status: source-complete and deployed; visual narrow/print browser comparison remains pending.
- Finding: the Notice report changed from a table to block/card-like rows below 680px, hiding the table header and violating the required column-preservation rule.
- Behavior: narrow Notice reports now remain real tables inside an explicitly horizontally scrollable region; all columns, order, headers and print rules remain unchanged.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_notice.css`; Rails revision `11130f7`.
- Verification: stylesheet diff check, Docker asset rebuild and Rails `zeitwerk:check` passed.
- Remaining: verify the narrow scroll affordance, keyboard reachability and desktop/narrow print output in a live browser.

## 2026-09-20 — Holiday editor draft retention and labels

- Status: source-complete and deployed; authenticated negative-path browser confirmation remains pending.
- Finding: a failed holiday create redirected away from the editor and discarded the submitted date/name; both controls also lacked visible labels.
- Behavior: recoverable holiday failures now re-render the Calendar page with the submitted date and name, reopen the editor, and show Russian field labels. Successful creation and delete routes remain unchanged.
- Attributable source: `apps/schedule_web/app/controllers/admin/holidays_controller.rb` and `app/views/admin/holidays/index.html.erb`; Rails revision `a1c634f`.
- Verification: Rails Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated 422 retention, successful holiday create/delete read-back and conflict evidence remain pending.

## 2026-09-20 — Semester editor draft retention

- Status: source-complete and deployed; authenticated negative-path browser confirmation remains pending.
- Finding: invalid or conflicting semester creation redirected away and discarded the submitted academic years and semester number.
- Behavior: failed semester creation now re-renders the Calendar page with safe submitted values, reopens the editor, and maps conflict/permission failures to Russian feedback. Successful creation still selects the new semester.
- Attributable source: `apps/schedule_web/app/controllers/admin/semesters_controller.rb` and `app/views/admin/semesters/index.html.erb`; Rails revision `f1be325`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated 422 retention and successful semester creation/read-back evidence remain pending.

## 2026-09-20 — Schedule edit draft retention

- Status: source-complete and deployed; authenticated conflict/validation browser confirmation remains pending.
- Finding: Schedule event update failures redirected with only a message, losing the submitted day, time, week, subgroup, status, room and assignment selections.
- Behavior: failed updates now retain a safe non-secret draft in the redirect flash and rehydrate the selected event editor, including checked teacher/room assignments and fallback room identity. The existing event ID and update operation remain unchanged.
- Attributable source: `apps/schedule_web/app/controllers/admin/schedules/update_controller.rb` and `app/views/admin/schedules/show/show.html.erb`; Rails revision `0195ff0`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated invalid/conflict response, original-record preservation and authoritative reload/read-back evidence remain pending.

## 2026-09-20 — Dated transfer draft retention

- Status: source-complete and deployed; authenticated conflict/validation browser confirmation remains pending.
- Finding: failed recurring-to-dated transfer requests redirected with only an alert and discarded the submitted dates, action, target slot, room and reason.
- Behavior: transfer failures now preserve a separate safe draft and reopen the dated-transfer disclosure, while keeping recurring edits and dated transfers on their existing distinct operations.
- Attributable source: `apps/schedule_web/app/controllers/admin/schedules/transfers_controller.rb` and `app/views/admin/schedules/show/show.html.erb`; Rails revision `05daa46`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated invalid/conflict response, cancellation/move read-back and original-record preservation evidence remain pending.

The same dated-transfer editor now offers readable room choices from the selected workload (with a current-room fallback) instead of exposing a raw room-ID input. Rails revision: `e1adf79`.

## 2026-09-20 — Schedule create draft retention

- Status: source-complete and deployed; authenticated occupied-slot/validation browser confirmation remains pending.
- Finding: failed Schedule event creation redirected with an alert and discarded the staged assignment, room, slot and period inputs.
- Behavior: failed creates now preserve a safe draft through the redirect and rehydrate the same selected-cell editor, including multi-teacher/multi-room selections and period-specific date values. The create operation and load identity remain unchanged.
- Attributable source: `apps/schedule_web/app/controllers/admin/schedules/events_controller.rb` and `app/views/admin/schedules/show/show.html.erb`; Rails revision `aedae5b`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated occupied-slot rejection, successful create/read-back and remaining-hours verification remain pending.

## 2026-09-20 — Schedule swap draft retention

- Status: source-complete and deployed; authenticated conflict/read-back browser confirmation remains pending.
- Finding: rejected dated swaps discarded the source date, target lesson, target date and reason.
- Behavior: failed swaps now preserve a separate draft and reopen the swap disclosure without merging it with recurring edits or dated transfers.
- Attributable source: `apps/schedule_web/app/controllers/admin/schedules/swaps_controller.rb` and `app/views/admin/schedules/show/show.html.erb`; Rails revision `6e81cff`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated occupied-target rejection, successful swap/read-back and original-event preservation evidence remain pending.

The Schedule and dated lesson-transfer selectors now use readable teacher, room and lesson labels without exposing raw database IDs in normal controls. Request values remain unchanged. Rails revision: `69069bb`.

## 2026-09-20 — Calendar dated-transfer draft recovery

- Status: source-complete and deployed; authenticated conflict/read-back browser confirmation remains pending.
- Finding: the two-date Calendar move/swap dialog was client-staged, so a rejected API mutation returned to the page without the submitted operation values.
- Behavior: move and swap failures now carry a separate safe draft through the redirect; the Stimulus dialog restores the correct operation, event identity, dates, target slot/lesson, room, and reason before reopening. Move and swap remain distinct server operations.
- Attributable source: `apps/schedule_web/app/controllers/admin/lesson_transfers_controller.rb`, `app/views/admin/lesson_transfers/show.html.erb`, and `app/javascript/controllers/lesson_transfer_drag_controller.js`; Rails revision `29ef4e4`.
- Verification: Ruby/ERB/JavaScript syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated rejected move/swap confirmation, successful read-back and original-event preservation evidence remain pending.

## 2026-09-20 — Student-group create draft retention

- Status: source-complete and deployed; authenticated validation/conflict browser confirmation remains pending.
- Finding: failed student-group creation discarded the selected speciality, admission year, student count, semester duration and automatic-provisioning choice.
- Behavior: failed creates now re-render the group catalog with safe submitted values and reopen the create sheet. Successful creation and provisioning contracts remain unchanged.
- Attributable source: `apps/schedule_web/app/controllers/admin/student_groups_controller.rb` and `app/views/admin/student_groups/index.html.erb`; Rails revision `c9d6ab0`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated rejected-create confirmation and successful group/read-back evidence remain pending.

## 2026-09-20 — Group-semester edit draft retention

- Status: source-complete and deployed; authenticated validation/conflict browser confirmation remains pending.
- Finding: failed updates to a group-semester's student count or duration redirected away and discarded the edited row values.
- Behavior: failed updates now re-render the selected group's semester list, preserve the submitted values for the affected row, and reopen that row editor. Successful updates retain their existing redirect and identity.
- Attributable source: `apps/schedule_web/app/controllers/admin/student_groups_controller.rb` and `app/views/admin/student_groups/semesters.html.erb`; Rails revision `5908d7e`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated rejected-update confirmation and successful group-semester read-back evidence remain pending.

## 2026-09-20 — Student-group edit draft retention

- Status: source-complete and deployed; authenticated validation/conflict browser confirmation remains pending.
- Finding: failed group edits discarded the selected speciality and admission year and returned to the unedited list.
- Behavior: failed edits now re-render the catalog with the affected row's safe draft values and reopen that row editor. Successful updates retain the existing operation and identity.
- Attributable source: `apps/schedule_web/app/controllers/admin/student_groups_controller.rb` and `app/views/admin/student_groups/index.html.erb`; Rails revision `40a05f8`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated rejected-edit confirmation and successful group update/read-back evidence remain pending.

## 2026-09-20 — Teacher search label cleanup

- Status: source-complete and deployed; authenticated browser visual confirmation remains pending.
- Finding: Teachers search results displayed a raw database ID beside every readable teacher label.
- Behavior: result labels now show the teacher name and role only; the existing link still carries the internal identifier server-side.
- Attributable source: `apps/schedule_web/app/views/admin/teachers/show/show.html.erb`; Rails revision `80e88d9`.
- Verification: ERB syntax check, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: complete Teachers mutation/read-back and responsive browser acceptance remain pending.

## 2026-09-20 — Teacher create draft retention

- Status: source-complete and deployed; authenticated validation/conflict browser confirmation remains pending.
- Finding: failed teacher creation redirected away and discarded names, post, academic degree/title, part-time status and department selections.
- Behavior: failed creates now retain a safe draft, reopen the teacher drawer, and restore all submitted controls. Passwords are not part of this operation or draft.
- Attributable source: `apps/schedule_web/app/controllers/admin/teachers/create_controller.rb`, `app/controllers/admin/teachers/mutation_controller.rb`, and `app/views/admin/teachers/show/_create.html.erb`; Rails revision `ba375f0`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated rejected-create confirmation and successful teacher/read-back evidence remain pending.

## 2026-09-20 — Teacher profile draft retention

- Status: source-complete and deployed; authenticated validation/conflict browser confirmation remains pending.
- Finding: failed teacher profile updates discarded submitted names, academic selections and part-time status, reverting the visible form to the persisted record.
- Behavior: failed updates now preserve a separate safe profile draft and rehydrate the selected teacher editor, including an intentionally blank middle name.
- Attributable source: `apps/schedule_web/app/controllers/admin/teachers/update_controller.rb`, `app/controllers/admin/teachers/mutation_controller.rb`, and `app/views/admin/teachers/show/_profile.html.erb`; Rails revision `139a5a3`.
- Verification: Ruby/ERB syntax checks, diff check, Docker rebuild and `rails zeitwerk:check` passed.
- Remaining: authenticated rejected-update confirmation and successful teacher profile/read-back evidence remain pending.

## 2026-09-20 — Preserve intentionally blank teacher profile drafts

- Status: source-complete and deployed; authenticated negative-path browser confirmation remains pending.
- Finding: the profile draft path claimed to preserve a cleared middle name, but the view used presence fallback and restored the persisted name instead.
- Behavior: submitted profile values now take precedence whenever the draft contains the field, including an intentionally blank middle name and empty optional selections.
- Attributable source: `apps/schedule_web/app/views/admin/teachers/show/_profile.html.erb`; Rails revision `a8566d6`.
- Verification: ERB generation and Ruby syntax checks passed.
- Remaining: authenticated rejected-update confirmation and successful teacher profile/read-back evidence remain pending.

## 2026-09-20 — Preserve blank Calendar and group drafts

- Status: source-complete and deployed; authenticated negative-path browser confirmation remains pending.
- Finding: invalid blank numeric/date submissions in semester and student-group editors could be replaced by fresh defaults or persisted row values on re-render.
- Behavior: when a draft contains a field, its submitted value now remains visible, including blank values; fresh editors still receive the existing defaults.
- Attributable source: semester and student-group ERB editors; Rails revision `320b089`.
- Verification: ERB generation, Ruby syntax and diff checks passed.
- Remaining: authenticated rejected-create/update confirmation and successful read-back evidence remain pending.

## 2026-09-20 — Remove reservation fallback identifiers

- Status: source-complete and deployed; authenticated reservation read/write confirmation remains pending.
- Finding: reservation room and teacher option fallbacks exposed raw database IDs when catalog labels were incomplete.
- Behavior: fallback labels now communicate catalog context without showing identifiers; internal room and teacher values remain unchanged for the API contracts.
- Attributable source: `apps/schedule_web/app/controllers/admin/room_reservations_controller.rb`; Rails revision `41f4a1c`.
- Verification: diff check and container Ruby syntax check passed.
- Remaining: authenticated reservation list/create/edit conflict and read-back evidence remain pending.

## 2026-09-20 — Remove room catalog fallback identifiers

- Status: source-complete and deployed; authenticated resource visual confirmation remains pending.
- Finding: room create/edit building choices exposed a raw building ID when the catalog had no display number.
- Behavior: incomplete building labels now use a catalog-context message while preserving the internal relationship value.
- Attributable source: `apps/schedule_web/app/views/admin/resources/rooms/index.html.erb`; Rails revision `ed012b0`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated resource CRUD/read-back and narrow browser evidence remain pending.

## 2026-09-20 — Remove period context fallback identifiers

- Status: source-complete and deployed; authenticated period configuration confirmation remains pending.
- Finding: period context labels exposed a raw group-semester ID when the catalog lacked a display name.
- Behavior: context and group selectors now use a catalog-context label while preserving the group-semester identifier internally.
- Attributable source: `apps/schedule_web/app/views/admin/period_settings/show/show.html.erb`; Rails revision `c4a84fa`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated period save/rejection/read-back and browser evidence remain pending.

## 2026-09-20 — Keep period actions inside their editor units

- Status: source-complete and deployed; authenticated period interaction remains pending.
- Finding: the four period save forms and their delete forms were sibling grid items, allowing a delete action to appear under a different period column.
- Behavior: each period now owns a compact unit containing its save editor and optional delete action; all period kinds, routes and payloads remain unchanged.
- Attributable source: period settings view and Calendar stylesheet; Rails revision `8f2a777`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated period save/delete/read-back and responsive browser evidence remain pending.

## 2026-09-20 — Expose reservation pagination

- Status: source-complete and deployed; authenticated reservation navigation remains pending.
- Finding: the reservation API request was paginated at 50 rows, but the Calendar view had no controls to reach later pages.
- Behavior: accessible previous/next links now preserve room and date filters while changing only the reservation page.
- Attributable source: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`; Rails revision `172d8b4`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated reservation list/create/edit conflict and read-back evidence remain pending.

## 2026-09-20 — Expose weekday-transfer pagination

- Status: source-complete and deployed; authenticated transfer navigation remains pending.
- Finding: weekday transfers were fetched in 50-row pages, but the five-column table had no controls for subsequent pages.
- Behavior: previous/next navigation now preserves the day-transfer mode while changing only the page.
- Attributable source: `apps/schedule_web/app/views/admin/weekday_transfers/index.html.erb`; Rails revision `bdd0249`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated transfer create/delete/read-back and conflict evidence remain pending.

## 2026-09-20 — Expose holiday pagination

- Status: source-complete and deployed; authenticated holiday navigation remains pending.
- Finding: the holiday endpoint was paginated at 50 rows, but the Calendar table exposed only the current page.
- Behavior: previous/next controls now preserve Calendar context and change only the holiday page.
- Attributable source: `apps/schedule_web/app/views/admin/holidays/index.html.erb`; Rails revision `be55a39`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated holiday create/delete/read-back and conflict evidence remain pending.

## 2026-09-20 — Preserve blank resource relationships

- Status: source-complete and deployed; authenticated resource validation confirmation remains pending.
- Finding: shared academic catalogs and dedicated room/building/type editors used truthy relationship fallbacks, so a failed blank selection could be replaced by the persisted relationship.
- Behavior: submitted relationship keys now take precedence, including blank values; persisted nested labels remain the fallback for normal read-only rows.
- Attributable source: shared academic catalog form and room/building/room-type editors; Rails revision `b605552`.
- Verification: diff check and container ERB compilation passed.
- Remaining: authenticated resource 422/conflict and successful CRUD read-back evidence remain pending.

## 2026-09-20 — Normalize shared context typography

- Status: source-complete and deployed; browser computed-style confirmation remains pending.
- Finding: shared Schedule/Calendar context labels and period controls still used 10px text, below the design-system minimum for context and primary controls.
- Behavior: those shared admin roles now use 12px text while preserving existing spacing, control heights, table schemas and page-specific layouts.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`; Rails revision `60b3626`.
- Verification: diff check passed.
- Remaining: computed-style checks at required viewports and complete browser acceptance remain pending.

## 2026-09-20 — Keep Accounts create action reachable

- Status: source-complete and deployed; browser bounding-box confirmation remains pending.
- Finding: the Accounts create form is nested inside role-selection controller markup, so the shared sheet-body sticky-action rule did not keep its primary action visible during long-form scrolling.
- Behavior: create and edit account form submissions now use the same reachable sticky action treatment within the Accounts sheet; fields and account contracts remain unchanged.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`; Rails revision `328c506`.
- Verification: diff check passed.
- Remaining: authenticated Accounts mutation/read-back and computed viewport evidence remain pending.

## 2026-09-20 — Keep Teachers create action reachable

- Status: source-complete and deployed; browser bounding-box confirmation remains pending.
- Finding: the Teachers create drawer placed its primary submit at the end of a long scrolling form without a persistent action treatment.
- Behavior: the teacher creation action now remains reachable while the drawer body scrolls; the existing fields, draft retention and create contract remain unchanged.
- Attributable source: `apps/schedule_web/app/assets/stylesheets/components/_admin_teachers.css`; Rails revision `b80d722`.
- Verification: diff check passed.
- Remaining: authenticated teacher mutation/read-back and computed viewport evidence remain pending.

## 2026-09-20 — Remove workload assignment identifier fallbacks

- Status: source-complete and deployed; authenticated workload search/read-back remains pending.
- Finding: workload assignment options exposed a raw teacher ID when a teacher label was unavailable, and an empty room label could be rendered for incomplete search data.
- Behavior: assignment choices now use readable catalog-context fallbacks while retaining membership and room identifiers in the submitted replacement set.
- Attributable source: workload presenter and assignment partial; Rails revision `966269c`.
- Verification: diff check, Ruby syntax and container ERB compilation passed.
- Remaining: authenticated multi-selection, failed-save retention and authoritative workload read-back remain pending.

## 2026-09-20 — Remove remaining administrator identifier labels

- Status: source-complete and deployed; authenticated visual confirmation remains pending.
- Finding: four presenter fallbacks still exposed raw teacher or department IDs when catalog labels were missing.
- Behavior: workload, Notice and Teachers presenters now use readable catalog-context labels for incomplete data; internal IDs remain available to operations and links.
- Attributable source: workload, Notice and Teachers presenters; Rails revision `bfb1cb4`.
- Verification: raw-ID fallback scan is clean; diff check and container Ruby syntax checks passed.
- Remaining: authenticated visual/read-back evidence remains pending.

## 2026-09-20 — Remove catalog identifier display fallbacks

- Status: source-complete and deployed; authenticated visual confirmation remains pending.
- Finding: aggregate catalogs, duplicate time-slot labels and Teachers reference options still displayed raw IDs in incomplete or duplicate-label cases.
- Behavior: these labels now use catalog-context or ordinal wording; internal IDs and ordering remain unchanged.
- Attributable source: aggregate and Teachers presenters; Rails revision `4d29b1e`.
- Verification: identifier-pattern scan is clean for visible fallback labels; diff check and container Ruby syntax checks passed.
- Remaining: authenticated visual/read-back evidence remains pending.

## 2026-09-20 — Remove raw identifiers from audit views

- Status: source-complete and deployed; authenticated audit visual confirmation remains pending.
- Finding: the audit list and inspector printed raw entity and actor IDs as the primary object and user labels.
- Behavior: audit views now show the localized entity type and a readable staff context label; the existing detail action and sanitized payload still provide the audit record.
- Attributable source: Overview presenter and audit/observability views; Rails revision `a1b1f53`.
- Verification: diff check and container Ruby syntax check passed.
- Remaining: authenticated audit navigation and payload read-back evidence remain pending.

## 2026-09-20 — Compact committed Schedule context

- Status: source-complete; authenticated computed-height and interaction evidence remains pending.
- Finding: after a valid semester/faculty/group selection, Schedule kept all three catalog selectors expanded as a tall context wall, pushing the timetable below the working-space budget.
- Behavior: the committed state now presents one readable semester/faculty/group summary and an explicit `Изменить контекст` disclosure. Existing selectors, search behavior, identifiers and URL parameters remain unchanged inside the disclosure.
- Files changed: `apps/schedule_web/app/lib/presenters/admin/schedule_workspace.rb`, `apps/schedule_web/app/views/admin/schedules/show/show.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `9672a27`; root worktree source remains limited to the handoff update.
- Runtime/source verification: template compiled through Rails' Erubi handler; presenter syntax and diff checks passed; rebuilt asset verification remains required after the next container build.
- Routes, role, context, viewport: `/admin/schedule`, staff administrator, selected semester/faculty/group; browser measurements at 1280×900 and 390×844 remain pending.
- Table inventory: unchanged; timetable headers, axes, cells and event semantics were not modified.
- Known remaining issue: browser connector is unavailable, so open/close, focus return and actual height reduction cannot yet be confirmed.
- Next action: rebuild `schedule_web`, verify asset loading and run the next B01 shared-control slice against Workload.

## 2026-09-20 — Normalize Schedule and Workload controls

- Status: source-complete; computed-style and keyboard/touch evidence remains pending.
- Finding: Schedule and Workload used competing 44–48px rules for ordinary context links and search controls, while the design contract calls for 40px default controls and 14px form text.
- Behavior: ordinary Schedule/Workload selectors and search controls now share a 40px/14px role; page-specific primary actions retain their larger touch target treatment.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `66eb35e`.
- Runtime/source verification: diff check passed; asset rebuild and Rails loading verification are pending in the current container cycle.
- Routes, role, context, viewport: `/admin/schedule` and `/admin/workload`, staff administrator, selected context; browser measurements at 1280×900, 768×1024 and 390×844 remain pending.
- Table inventory: unchanged; Schedule timetable and Workload five-column table retain their existing headers and row semantics.
- Known remaining issue: browser connector is unavailable, so actual computed sizes, focus treatment and narrow layout cannot yet be confirmed.
- Next action: rebuild the web container, run Rails/API checks, then continue with B02 workload assignment and placement verification.

## 2026-09-20 — Announce staged Schedule drag actions

- Status: source-complete; authenticated drag, keyboard and read-back evidence remains pending.
- Finding: typed Schedule drag sources selected a destination through the existing URL flow, but provided no live feedback about the selected load/event or staged destination.
- Behavior: the existing typed load/event drag path now announces source and destination state in a shared `aria-live` status region; click/tap links, destination URLs and save operations remain unchanged.
- Files changed: `apps/schedule_web/app/javascript/controllers/planner_drag_controller.js`, `apps/schedule_web/app/views/admin/schedules/show/show.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `9b2b846`.
- Runtime/source verification: Node syntax check, Rails Erubi template compilation and diff check passed; rebuilt asset verification remains pending.
- Routes, role, context, viewport: `/admin/schedule`, staff administrator, selected group; browser drag/keyboard checks at 1280×900 and 390×844 remain pending.
- Table inventory: unchanged; timetable axes, headers, cells and event links remain intact.
- Known remaining issue: browser connector is unavailable, so live announcements and destination validation cannot yet be observed.
- Next action: rebuild `schedule_web` with the staged-drag assets, then continue the B02 placement/edit source audit.

## 2026-09-20 — Add retry state for reservation reads

- Status: source-complete; authenticated dependency failure and read-back evidence remains pending.
- Finding: when reservations, rooms or time slots failed to load, Calendar showed only a static unavailable sentence and offered no recovery action.
- Behavior: the reservation workspace now distinguishes the unavailable state, preserves the current URL filters and exposes a Russian `Повторить` action inside the Calendar frame. Create/edit controls remain withheld until required read dependencies succeed.
- Files changed: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`.
- Source revision: Rails `a52d490`.
- Runtime/source verification: Rails Erubi template compilation and diff check passed.
- Routes, role, context, viewport: `/admin/room_reservations`, staff schedule writer, current room/date filters; browser retry and responsive evidence remain pending.
- Table inventory: unchanged; reservation columns, order and row semantics remain intact.
- Known remaining issue: the browser connector is unavailable, and the underlying authenticated reservation failure has not yet been reproduced live.
- Next action: rebuild `schedule_web`, then continue B04 context and dated-rule verification.

## 2026-09-20 — Fix period context field semantics

- Status: source-complete; authenticated keyboard and context-switch evidence remains pending.
- Finding: Periods wrapped fieldsets containing radio labels inside outer `<label>` elements, creating invalid nested label semantics and unreliable accessible grouping.
- Behavior: faculty and semester context controls now use explicit labelled field groups; radio inputs, context parameters and automatic submit behavior remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/period_settings/show/show.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_calendar.css`.
- Source revision: Rails `0a3ff81`.
- Runtime/source verification: Rails Erubi template compilation and diff check passed.
- Routes, role, context, viewport: `/admin/operations`, staff administrator, faculty/semester/group context; keyboard and responsive evidence remain pending.
- Table inventory: unchanged; period editor units and their four period kinds remain intact.
- Known remaining issue: browser connector is unavailable, so focus order and context disclosure behavior cannot yet be observed.
- Next action: rebuild `schedule_web`, verify Calendar assets, then continue B04 dated-rule state handling.

## 2026-09-20 — Add retry states for dated Calendar reads

- Status: source-complete; authenticated failure and read-back evidence remains pending.
- Finding: Holidays and weekday transfers rendered a static unavailable message without a recovery action.
- Behavior: both pages now expose a Russian `Повторить` action that preserves the current URL context, mode and page while keeping create/delete controls hidden until the read succeeds.
- Files changed: `apps/schedule_web/app/views/admin/holidays/index.html.erb`, `apps/schedule_web/app/views/admin/weekday_transfers/index.html.erb`.
- Source revision: Rails `5e742d0`.
- Runtime/source verification: Rails Erubi compilation for both templates and diff check passed.
- Routes, role, context, viewport: `/admin/holidays` and `/admin/transfers?mode=days`, staff administrator; browser retry and responsive evidence remain pending.
- Table inventory: unchanged; holiday three-column and weekday-transfer five-column structures remain intact.
- Known remaining issue: authenticated read failures and retry behavior cannot be observed until the browser connector is available.
- Next action: rebuild `schedule_web`, then move to B05 Accounts editor overlap and scope selection.

## 2026-09-20 — Add removable account scope chips

- Status: source-complete; authenticated account mutation/read-back and editor-overlap evidence remains pending.
- Finding: Accounts scope search could append a faculty or department scope, but neither existing nor newly added scopes had an explicit remove action.
- Behavior: every visible scope is now a removable labelled chip. Removal deletes only the matching hidden scope input; untouched scopes remain in the complete replacement collection sent by the existing account contract.
- Files changed: `apps/schedule_web/app/javascript/controllers/account_scope_picker_controller.js`, `apps/schedule_web/app/views/admin/accounts/index.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revision: Rails `d12db99`.
- Runtime/source verification: Node syntax check, Rails Erubi template compilation and diff check passed.
- Routes, role, context, viewport: `/admin/accounts`, staff account manager, existing account row and preserved filter context; browser chip, failure and read-back evidence remain pending.
- Table inventory: unchanged; all six account columns remain intact.
- Known remaining issue: browser connector is unavailable, so scope removal and editor positioning cannot yet be observed.
- Next action: rebuild `schedule_web`, then finish the B05 editor state review.

## 2026-09-20 — Align account editor sheet geometry

- Status: source-complete; authenticated overlap and focus-return evidence remains pending.
- Finding: the Accounts fixed dialog inherited the native `<dialog>` margin and content-box sizing, allowing the declared 520px sheet to render wider than its available track.
- Behavior: the edit sheet now uses border-box viewport sizing, zero native margin, no duplicate border and a bounded viewport height while retaining the shared modal controller.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revision: Rails `b535bf3`.
- Runtime/source verification: diff check passed; asset rebuild and computed geometry verification remain pending.
- Routes, role, context, viewport: `/admin/accounts`, staff account manager, existing account row; browser overlap checks at 1280×900 and 390×844 remain pending.
- Table inventory: unchanged; six account columns and action semantics remain intact.
- Known remaining issue: browser connector is unavailable, so actual sheet bounds and modal focus behavior cannot yet be observed.
- Next action: rebuild `schedule_web`, verify Accounts assets, then continue B05 failure/read-back review.

## 2026-09-20 — Preserve manual account logins

- Status: source-complete; authenticated create/edit failure and read-back evidence remains pending.
- Finding: typing a name regenerated and overwrote an existing or manually edited account email on every change.
- Behavior: login generation now acts as a suggestion. It updates an empty or previously generated value, while an existing/manual value is preserved until the administrator changes it deliberately.
- Files changed: `apps/schedule_web/app/javascript/controllers/account_login_controller.js`, `apps/schedule_web/app/views/admin/accounts/index.html.erb`.
- Source revision: Rails `7b79a8c`.
- Runtime/source verification: Node syntax check, Rails Erubi template compilation and diff check passed.
- Routes, role, context, viewport: `/admin/accounts`, staff account manager, create and edit sheets; browser manual-login and mutation evidence remain pending.
- Table inventory: unchanged; account columns and filters remain intact.
- Known remaining issue: browser connector is unavailable, so manual override behavior cannot yet be observed interactively.
- Next action: rebuild `schedule_web`, then continue B05 failure-state and one-time credential review.

## 2026-09-20 — Add Notice search retry action

- Status: source-complete; authenticated Notice failure and print evidence remains pending.
- Finding: a failed Notice teacher search showed only `Повторите запрос позже` and had no retry action.
- Behavior: the existing query and semester context now remain available through a Russian `Повторить` action inside the Notice frame; report columns and print controls are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/notice/show/show.html.erb`.
- Source revision: Rails `24dd440`.
- Runtime/source verification: Rails Erubi template compilation and diff check passed.
- Routes, role, context, viewport: `/admin/notice`, staff administrator, teacher query and semester context; browser retry and print evidence remain pending.
- Table inventory: unchanged; Notice retains its five report columns and print-only schema.
- Known remaining issue: browser connector is unavailable, so retry interaction and print layout cannot yet be observed.
- Next action: rebuild `schedule_web`, then complete B06 shared-state and responsive source review.

## 2026-09-20 — Collapse secondary monitoring navigation

- Status: source-complete; authenticated responsive navigation evidence remains pending.
- Finding: the shared sidebar rendered monitoring links expanded on every admin page, consuming vertical space despite being secondary navigation.
- Behavior: monitoring services now render as a collapsed native disclosure and remain available from the same sidebar location when opened.
- Files changed: `apps/schedule_web/app/views/admin/shared/_sidebar.html.erb`.
- Source revision: Rails `549954c`.
- Runtime/source verification: in-container Rails ERB compilation and diff check passed.
- Routes, role, context, viewport: all staff admin routes; sidebar at desktop and narrow widths; browser evidence remains pending.
- Table inventory: unchanged.
- Known remaining issue: browser connector is unavailable, so interactive disclosure and narrow-navigation behavior cannot yet be observed.
- Next action: continue B06 source review and perform browser acceptance when the connector is available.

## 2026-09-20 — Normalize disclosure focus states

- Status: source-complete; keyboard and responsive browser evidence remains pending.
- Finding: navigation group and monitoring disclosure summaries had no shared visible focus treatment.
- Behavior: keyboard focus now uses the admin almond outline with a consistent offset on both disclosure types.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `bf9f68b`.
- Runtime/source verification: in-container Rails Zeitwerk check passed; CSS diff is scoped to shared admin disclosure selectors.
- Routes, role, context, viewport: all staff admin routes; desktop and narrow sidebar navigation; browser evidence remains pending.
- Table inventory: unchanged.
- Known remaining issue: browser connector is unavailable, so keyboard focus visibility cannot yet be observed interactively.
- Next action: complete B06 source review and run the planned browser acceptance pass when the connector is available.

## 2026-09-20 — Add searchable Resource relationship selectors

- Status: source-complete; authenticated Resource CRUD and responsive evidence remains pending.
- Finding: room and building editors rendered relationship catalogs as unfiltered radio-card walls, and room rows could expose raw relationship IDs when nested labels were unavailable.
- Behavior: building types, buildings, room types and activity types now use bounded searchable choice lists with readable Russian labels and an explicit empty result state. Room table fallbacks use translated context text instead of database IDs; submitted relationship identifiers and existing contracts are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/resources/buildings/index.html.erb`, `apps/schedule_web/app/views/admin/resources/rooms/index.html.erb`, `apps/schedule_web/app/views/admin/resources/room_types/index.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css`.
- Source revision: Rails `e2606fa`.
- Runtime/source verification: ERB compilation for all three templates, Rails Zeitwerk check and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/buildings`, `/admin/rooms`, `/admin/room_types`, super administrator; create/edit relationship selection and narrow sheets require browser verification.
- Table inventory: unchanged; building, room and room-type columns remain in their existing order and row meaning.
- Known remaining issue: browser connector is unavailable, so search filtering, submit/read-back and CRUD failure retention cannot yet be observed interactively.
- Next action: continue B03 resource form and dependency-state review, then perform the complete CRUD acceptance path when browser access is available.

## 2026-09-20 — Add searchable student-group specialization selectors

- Status: source-complete; authenticated group CRUD and responsive evidence remains pending.
- Finding: student-group create/edit used an unfiltered specialization card wall even though the catalog can grow beyond a small stable enumeration.
- Behavior: both forms now provide a bounded searchable specialization list with readable labels and an explicit no-match state; the existing `speciality_id` request field and group table remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/student_groups/index.html.erb`.
- Source revision: Rails `727916b`.
- Runtime/source verification: Rails ERB compilation and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/student_groups`, super administrator, create/edit group sheets; browser selection, failure retention and read-back remain pending.
- Table inventory: unchanged; group specialization, admission year and action columns remain intact.
- Known remaining issue: browser connector is unavailable, so search and CRUD behavior cannot yet be observed interactively.
- Next action: continue B03 dependency and form-state review, then verify the full Resource CRUD journeys.

## 2026-09-20 — Add searchable Calendar context selectors

- Status: source-complete; authenticated period configuration and responsive evidence remains pending.
- Finding: Periods context rendered faculty and group-semester catalogs as unfiltered choice walls, making larger catalogs difficult to scan and inconsistent with the fixed selector rules.
- Behavior: faculty and group-semester context now expose bounded searchable lists with readable labels and explicit no-match states. Existing context parameters, automatic submit behavior and period semantics remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/period_settings/show/show.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_calendar.css`.
- Source revision: Rails `469688f`.
- Runtime/source verification: Rails ERB compilation and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/operations`, staff administrator, faculty/semester/group context; browser search, context retention and period read-back remain pending.
- Table inventory: unchanged; four period editor units and their field meanings remain intact.
- Known remaining issue: browser connector is unavailable, so selector behavior and context history cannot yet be observed interactively.
- Next action: continue B04 reservation dependency diagnosis and Calendar failure-state review.

## 2026-09-20 — Add searchable account faculty scope selector

- Status: source-complete; authenticated role/scope mutation and responsive evidence remains pending.
- Finding: super-admin account creation exposed faculty scope choices as an unfiltered radio-card wall, unlike the existing searched teacher and department selectors.
- Behavior: the faculty scope now has a bounded searchable list and explicit no-match state; hidden scope identity and role-driven submission behavior are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/accounts/index.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revision: Rails `1c45190`.
- Runtime/source verification: Rails ERB compilation and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/accounts`, super administrator, create sheet and faculty-admin role; browser selection, failure and read-back evidence remain pending.
- Table inventory: unchanged; all six account columns remain intact.
- Known remaining issue: browser connector is unavailable, so scope filtering and role-specific form behavior cannot yet be observed interactively.
- Next action: continue final B05 account state review and then complete B06 acceptance source checks.

## 2026-09-20 — Normalize Teachers header and search controls

- Status: source-complete; browser computed-style and responsive evidence remains pending.
- Finding: Teachers retained a 34–74px display heading and oversized search controls, unlike the shared admin header and Notice control roles.
- Behavior: the Teachers heading now uses a bounded 24–42px scale, and the search input/button use the shared 40px control height while preserving the dark search panel and existing workspace composition.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_teachers.css`.
- Source revision: Rails `28a5a52`.
- Runtime/source verification: Rails Zeitwerk check and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/teachers`, staff administrator, teacher search and selected workspace; computed-style and narrow/desktop browser evidence remain pending.
- Table inventory: unchanged; teacher availability grid and schedule preview semantics remain intact.
- Known remaining issue: browser connector is unavailable, so actual computed dimensions and responsive wrapping cannot yet be observed.
- Next action: complete B06 Notice/Observability source review and run browser acceptance when available.

## 2026-09-20 — Label Observability table scroll regions

- Status: source-complete; responsive and keyboard browser evidence remains pending.
- Finding: three Observability metric tables relied on card-level overflow without a labelled, keyboard-reachable scrolling region; only the audit table had a dedicated wrapper.
- Behavior: all four monitoring tables now use explicit labelled scroll regions, retain their existing columns, and expose scoped table headers. Card overflow no longer absorbs the scroll semantics.
- Files changed: `apps/schedule_web/app/views/admin/observability/show.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `435d550`.
- Runtime/source verification: Rails ERB compilation, Zeitwerk check and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/observability`, staff administrator, desktop and narrow widths; browser scrolling and focus evidence remain pending.
- Table inventory: unchanged; breaker, request, duration and audit schemas remain intact.
- Known remaining issue: browser connector is unavailable, so narrow overflow and keyboard reachability cannot yet be observed interactively.
- Next action: complete remaining B06 source checks and rerun the final source verification matrix.

## 2026-09-20 — Preserve initial department aggregate context

- Status: source-complete; authenticated aggregate navigation and read-back evidence remains pending.
- Finding: switching the staff aggregate workspace from Faculty to Department carried `scope_id=0`, so the first department-mode request returned a 404 even when the selected faculty had departments.
- Behavior: when department mode has no explicit department yet, the operation selects the first available department from the already loaded faculty catalog. Explicit department selections remain unchanged; API authorization still evaluates the selected department.
- Files changed: `apps/schedule_web/app/lib/operations/admin/load_aggregate_schedule.rb`.
- Source revision: Rails `7c8c77c`.
- Runtime/source verification: Ruby syntax, Rails Zeitwerk and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/aggregate_schedule`, staff administrator, faculty-to-department mode switch; browser URL/history and date-resolved read-back remain pending.
- Table inventory: unchanged; seven aggregate schedule columns remain intact.
- Known remaining issue: browser connector is unavailable, so the mode switch and selected-date transfer/cancellation rendering cannot yet be observed interactively.
- Next action: continue F01 source review for date/print semantics and authorization edge cases.

## 2026-09-20 — Remove raw group-semester identifiers from the table

- Status: source-complete; authenticated group-semester read-back remains pending.
- Finding: the group-semester table visibly rendered the database row ID and fell back to a raw `semester_id` when catalog context was incomplete.
- Behavior: the five-column table now shows a readable `Группа-семестр` label and semantic semester fallback text. Internal row IDs remain only in form/action targets and request values.
- Files changed: `apps/schedule_web/app/views/admin/student_groups/semesters.html.erb`.
- Source revision: Rails `45b36df`.
- Runtime/source verification: Rails ERB compilation and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/student_groups/:id/semesters`, super administrator, group-semester list and editor; browser read-back remains pending.
- Table inventory: unchanged at five columns; only the first column's visible wording was made semantic.
- Known remaining issue: browser connector is unavailable, so the readable labels and Calendar link context cannot yet be observed interactively.
- Next action: continue the final raw-identifier audit without changing table schemas.

## 2026-09-20 — Add Observability audit retry action

- Status: source-complete; authenticated failure and responsive evidence remains pending.
- Finding: an unavailable audit read showed a passive message without a recovery action.
- Behavior: the Observability audit section now exposes a Russian `Повторить` link using the current request URL, preserving route state and surrounding monitoring context.
- Files changed: `apps/schedule_web/app/views/admin/observability/show.html.erb`.
- Source revision: Rails `feb954a`.
- Runtime/source verification: Rails ERB compilation and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/observability`, super administrator, audit failure state; browser retry evidence remains pending.
- Table inventory: unchanged; audit columns and scroll region remain intact.
- Known remaining issue: browser connector is unavailable, so retry behavior cannot yet be observed interactively.
- Next action: continue final B06 failure-state and print source review.

## 2026-09-20 — Add searchable Workload group selectors

- Status: source-complete; authenticated multi-group creation/filter/read-back evidence remains pending.
- Finding: Workload faculty filtering and new-record creation rendered groups in bounded scroll walls without search, despite groups being a high-cardinality entity.
- Behavior: both group surfaces now provide a labelled searchable filter with an explicit no-match state. Existing multi-select checkboxes, retained selections, group IDs and create contract are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/workload/show/show.html.erb`, `apps/schedule_web/app/views/admin/workload/show/_create_record.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_workload.css`.
- Source revision: Rails `cb7c049`.
- Runtime/source verification: ERB compilation for both templates, Rails Zeitwerk check and `git diff --check` passed.
- Routes, role, context, viewport: `/admin/workload`, staff administrator, faculty filter and create sheet; browser search, draft retention and authoritative read-back remain pending.
- Table inventory: unchanged; Workload retains its existing five columns and dense table behavior.
- Known remaining issue: browser connector is unavailable, so multi-group filtering and create/read-back cannot yet be observed interactively.
- Next action: continue B02 assignment draft and placement source review.

## 2026-09-20 — Add searchable Schedule group and assignment selectors

- Status: source-complete; authenticated schedule group and inline assignment interaction evidence remains pending.
- Finding: the Schedule workspace rendered its group selector and inline lesson teacher/room collections without the searchable controls already used by Workload, despite these being high-cardinality entities.
- Behavior: Schedule now provides a labelled local group filter plus searchable teacher and room assignment lists in both create and edit inspectors. Existing checkbox names, IDs, retained selections, and event mutation routes are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/schedules/show/show.html.erb`, `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `fb059a2`.
- Runtime/source verification: Schedule ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/schedule`, staff administrator, selected faculty/group grid and create/edit inspectors; browser search and authoritative read-back remain pending.
- Table inventory: unchanged; the seven-day Schedule grid and its columns remain intact.
- Known remaining issue: browser connector is unavailable, so searchable Schedule interaction and the complete create/edit/read-back journey cannot yet be observed interactively.
- Next action: continue B02 placement and draft-retention source review.

## 2026-09-20 — Clarify Calendar reservation dependency failures

- Status: source-complete; authenticated reservation reads and conflict/read-back evidence remain pending.
- Finding: the Calendar reservation page collapsed failures from the reservation list, room catalog and time-slot catalog into one generic message, making the known unavailable-data state difficult to diagnose.
- Behavior: the page now identifies the failed required dependency or dependencies in Russian and keeps all reservation editors withheld until those reads succeed. Existing filters, retry URL and API contracts are unchanged.
- Files changed: `apps/schedule_web/app/controllers/admin/room_reservations_controller.rb`, `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`.
- Source revision: Rails `5104f44`.
- Runtime/source verification: controller Ruby syntax, reservation ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/room_reservations`, staff schedule writer, current room/date filters; browser dependency-failure and retry evidence remain pending.
- Table inventory: unchanged; reservation columns, ordering and row semantics remain intact.
- Known remaining issue: browser connector is unavailable, so the failing dependency cannot yet be confirmed against an authenticated live response.
- Next action: continue B04 period and dated-rule source verification, then return to the disposable core journey when browser access is restored.

## 2026-09-20 — Add searchable Calendar reservation room lists

- Status: source-complete; authenticated reservation search and read-back evidence remain pending.
- Finding: reservation filtering and create/edit forms rendered the loaded room catalog as long radio-card walls, despite rooms being high-cardinality and server search already being available.
- Behavior: filter, create and edit room lists now expose labelled local search with explicit no-match states. Selected room values, hidden identity fields, picker controllers and reservation request contracts are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`.
- Source revision: Rails `fc30fdf`.
- Runtime/source verification: reservation ERB compilation, controller syntax, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/room_reservations`, staff schedule writer, create/edit/filter room selectors; browser search and mutation/read-back remain pending.
- Table inventory: unchanged; reservation columns and row semantics remain intact.
- Known remaining issue: browser connector is still unavailable, so room filtering and the underlying reservation read failure cannot yet be observed interactively.
- Next action: continue B04 period and dated-rule source verification.

## 2026-09-20 — Expose weekday-transfer group catalog failures

- Status: source-complete; authenticated dated-rule creation and read-back evidence remain pending.
- Finding: the day-transfer controller converted a failed student-group catalog read into an empty list, making a dependency failure indistinguishable from a legitimate global-scope transfer.
- Behavior: session expiry now covers both transfer and group reads. The empty-state copy distinguishes an unavailable group catalog from a genuinely empty catalog and explicitly states the resulting global scope.
- Files changed: `apps/schedule_web/app/controllers/admin/lesson_transfers_controller.rb`, `apps/schedule_web/app/views/admin/weekday_transfers/index.html.erb`.
- Source revision: Rails `86f697d`.
- Runtime/source verification: controller syntax, weekday-transfer ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/transfers?mode=days`, super administrator, global or group-scoped dated transfer; browser failure-state and read-back evidence remain pending.
- Table inventory: unchanged; the five transfer columns and row semantics remain intact.
- Known remaining issue: browser connector is unavailable, so group-catalog failure and explicit global-scope behavior cannot yet be observed interactively.
- Next action: continue B04 period-editor source verification.

## 2026-09-20 — Show period catalog read failures

- Status: source-complete; authenticated period persistence and read-back evidence remain pending.
- Finding: a failed period read was converted into an empty period collection, leaving blank date editors and obscuring the unavailable state.
- Behavior: the period page now distinguishes a valid group with no configured periods from a failed period read and offers a retry action while preserving the selected context. Failed period form drafts continue to use the existing re-render path.
- Files changed: `apps/schedule_web/app/controllers/admin/period_settings/show_controller.rb`, `apps/schedule_web/app/controllers/admin/period_settings/periods_controller.rb`, `apps/schedule_web/app/views/admin/period_settings/show/show.html.erb`.
- Source revision: Rails `00fecb5`.
- Runtime/source verification: both controller syntax checks, period ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/operations`, staff administrator, selected faculty/semester/group; browser retry and period persistence evidence remain pending.
- Table inventory: unchanged; period editors are form units rather than tables.
- Known remaining issue: browser connector is unavailable, so the failure distinction and retry action cannot yet be observed interactively.
- Next action: continue B04 holiday and calendar-context source verification.

## 2026-09-20 — Add Notice context retry actions

- Status: source-complete; authenticated Notice failure and report read-back evidence remain pending.
- Finding: Notice displayed retryable search/report failures, but failed teacher and semester context reads had no recovery action.
- Behavior: failed teacher and semester context states now expose the same labelled retry action while preserving the current query and selected context. Report schema and print/export controls are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/notice/show/show.html.erb`.
- Source revision: Rails `6df5f20`.
- Runtime/source verification: Notice ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/notice`, staff administrator, teacher search and semester context; browser retry and report evidence remain pending.
- Table inventory: unchanged; Notice retains its five report columns and print semantics.
- Known remaining issue: browser connector is unavailable, so context retry behavior cannot yet be observed interactively.
- Next action: continue Overview and Observability source verification.

## 2026-09-20 — Add Teachers department-search retry

- Status: source-complete; authenticated department search and teacher read-back evidence remain pending.
- Finding: a failed department search in the Teachers workspace showed an error without a recovery action, while the surrounding catalog states already offered retry.
- Behavior: the department-search failure now includes a labelled retry link preserving the current teacher and search context. Department membership forms and identifiers remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/teachers/show/_departments.html.erb`.
- Source revision: Rails `6e4e325`.
- Runtime/source verification: department partial ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/teachers`, staff administrator, selected teacher and department query; browser retry and membership read-back remain pending.
- Table inventory: unchanged; Teachers availability and schedule structures remain intact.
- Known remaining issue: browser connector is unavailable, so department-search retry behavior cannot yet be observed interactively.
- Next action: finish Overview/Observability state review and run final source checks.

## 2026-09-20 — Clarify empty Observability metrics

- Status: source-complete; authenticated responsive and monitoring-state evidence remains pending.
- Finding: empty breaker, request and duration collections rendered blank table bodies, and the audit failure message was not exposed as a status region.
- Behavior: each metric table now has an explicit Russian empty row with the correct unchanged column span, and audit unavailability is announced through `role="status"`. Metric schemas, headings and scroll regions remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/observability/show.html.erb`.
- Source revision: Rails `64eda37`.
- Runtime/source verification: Observability ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/observability`, super administrator, empty and audit-failure states; browser accessibility and responsive evidence remain pending.
- Table inventory: unchanged; all three metric tables and the audit table retain their original columns and ordering.
- Known remaining issue: browser connector is unavailable, so empty-state announcement and narrow table behavior cannot yet be observed interactively.
- Next action: run final source-level checks across Rails and API, then retry the browser acceptance matrix.

## 2026-09-20 — Final source-level verification pass

- Status: source verification complete for the implemented slices; runtime mutation/read-back and responsive browser evidence remain pending.
- Checks: all 35 Rails administrator ERB templates compiled in the running `schedule_web` container; Rails `zeitwerk:check` passed; Hanami routes loaded successfully; aggregate faculty/department occurrence routes and administrator reservation routes are present; the aggregate occurrence repository passed Ruby syntax validation.
- Scope: no source changes in this verification pass; existing Rails, API and root untracked files were preserved.
- Known remaining issue: the authenticated Playwright transport still closes before a browser session can be used, so the B00 core journey, responsive matrix, authorization matrix and print/read-back acceptance cannot be claimed complete.
- Next action: rerun the same acceptance matrix when the browser transport is available; performance and availability measurement remain deferred by product decision.

## 2026-09-20 — Announce empty Overview audit state

- Status: source-complete; authenticated accessibility and responsive evidence remains pending.
- Finding: the empty audit journal state lacked a status role, unlike the unavailable state and adjacent monitoring surfaces.
- Behavior: the empty audit message is now announced with `role="status"`; audit filtering, pagination, table columns and inspector behavior are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/overview/show.html.erb`.
- Source revision: Rails `01270c8`.
- Runtime/source verification: Overview ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/overview`, staff administrator, empty audit journal; browser accessibility evidence remains pending.
- Table inventory: unchanged; the four-column audit table remains intact.
- Known remaining issue: browser transport is still closed, so live announcement behavior cannot yet be observed.
- Next action: retry browser acceptance when the connector recovers.

## 2026-09-20 — Verify serving container liveness

- Status: runtime liveness verified; authenticated browser acceptance remains pending.
- Evidence: from inside the running `schedule_web` container, `/` returned HTTP 200 and protected administrator routes `/admin/overview`, `/admin/aggregate_schedule`, and `/admin/room_reservations` returned HTTP 302 to authentication as expected.
- Scope: read-only requests only; no credentials, records or sessions were changed.
- Known remaining issue: this confirms route protection and serving health, not authenticated rendering, responsive behavior, mutation success or read-back.
- Next action: restore browser transport/authentication and execute the documented acceptance matrix.

## 2026-09-20 — Add Workload subject-search retry

- Status: source-complete; authenticated Workload creation and draft/read-back evidence remain pending.
- Finding: a failed subject search in the new workload editor displayed passive text without the recovery action used by other high-cardinality searches.
- Behavior: the subject-search failure now exposes a labelled retry link using the current request URL. Existing selected groups, search context and creation contract remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/workload/show/_create_record.html.erb`.
- Source revision: Rails `9216c11`.
- Runtime/source verification: workload creation ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/workload`, staff administrator, new workload editor and subject query; browser retry and creation/read-back evidence remain pending.
- Table inventory: unchanged; Workload retains its existing table columns and semantics.
- Known remaining issue: browser transport is unavailable, so the retry interaction cannot yet be observed.
- Next action: retry the browser acceptance matrix when the connector recovers.

## 2026-09-20 — Add Period Settings context retry links

- Status: source-complete; authenticated period-context and persistence evidence remain pending.
- Finding: failed faculty and semester catalog reads in Period Settings showed passive hints without recovery actions.
- Behavior: both context failures now expose labelled retry links that preserve the current URL and Turbo frame. Period selection, group identity and date editors are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/period_settings/show/show.html.erb`.
- Source revision: Rails `e12e565`.
- Runtime/source verification: Period Settings ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/operations`, staff administrator, faculty/semester/group context; browser retry and persistence evidence remain pending.
- Table inventory: unchanged; period editors retain their existing form structure.
- Known remaining issue: browser transport is unavailable, so context retry behavior cannot yet be observed.
- Next action: rerun browser acceptance when the connector recovers.

## 2026-09-20 — Announce Workload unavailable state

- Status: source-complete; authenticated Workload failure and read-back evidence remain pending.
- Finding: the Workload unavailable-load state had a retry action but lacked a status role for assistive technology.
- Behavior: the state now uses `role="status"`; retry URL, context retention and workload table semantics are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/workload/show/show.html.erb`.
- Source revision: Rails `2747dea`.
- Runtime/source verification: Workload ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/workload`, staff administrator, unavailable load state; browser announcement and retry evidence remain pending.
- Table inventory: unchanged; Workload retains its existing five-column table.
- Known remaining issue: browser transport is unavailable, so live status announcement cannot yet be observed.
- Next action: rerun browser acceptance when the connector recovers.

## 2026-09-20 — Add remaining administrator retry actions

- Status: source-complete; authenticated Accounts, academic-catalog and Workload assignment evidence remain pending.
- Finding: Accounts, Academic Catalogs and Workload room-search failures still showed passive unavailable text without recovery actions.
- Behavior: each state now exposes a labelled retry link using the current request URL. Account drafts, catalog editors, assignment selections and API identities remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/accounts/index.html.erb`, `apps/schedule_web/app/views/admin/resources/academic_catalogs/index.html.erb`, `apps/schedule_web/app/views/admin/workload/show/_assignment.html.erb`.
- Source revision: Rails `5a0b227`.
- Runtime/source verification: all three changed ERB templates compiled, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: Accounts, Academic Catalogs and Workload assignment routes, staff administrator; browser retry and mutation/read-back evidence remain pending.
- Table inventory: unchanged; account, catalog and Workload structures retain their existing schemas.
- Known remaining issue: browser transport is unavailable, so retry interactions cannot yet be observed.
- Next action: rerun browser acceptance when the connector recovers.

## 2026-09-20 — Add resource failure retry actions

- Status: source-complete; authenticated resource and Excel failure/read-back evidence remain pending.
- Finding: Buildings, Rooms, Room Types, Posts and Excel file-list failures displayed passive unavailable text without recovery actions.
- Behavior: each unavailable state now exposes a labelled retry link using the current request URL. Resource tables, editor contracts, upload state and file data remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/resources/buildings/index.html.erb`, `rooms/index.html.erb`, `room_types/index.html.erb`, `posts/index.html.erb`, `apps/schedule_web/app/views/admin/excel_imports/_files.html.erb`.
- Source revision: Rails `f777d0a`.
- Runtime/source verification: all five changed ERB templates compiled, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: resource catalog routes and `/admin/excel_imports`, staff administrator; browser retry and CRUD/upload read-back evidence remain pending.
- Table inventory: unchanged; all resource and import list structures remain intact.
- Known remaining issue: browser transport is unavailable, so retry behavior cannot yet be observed interactively.
- Next action: rerun browser acceptance when the connector recovers.

## 2026-09-20 — Add semester catalog retry action

- Status: source-complete; authenticated semester catalog and creation/read-back evidence remain pending.
- Finding: the Calendar semester page showed a passive unavailable message without recovery, unlike the other dated-rule pages.
- Behavior: the unavailable semester list now exposes a labelled retry action that preserves the current URL and Turbo frame. Semester columns and creation behavior are unchanged.
- Files changed: `apps/schedule_web/app/views/admin/semesters/index.html.erb`.
- Source revision: Rails `2474174`.
- Runtime/source verification: semester ERB compilation, Rails Zeitwerk check and `git diff --check` passed in the running `schedule_web` container.
- Routes, role, context, viewport: `/admin/semesters`, staff administrator, calendar context; browser retry and catalog read-back remain pending.
- Table inventory: unchanged; semester table headers, order and row meaning remain intact.
- Known remaining issue: browser connector is unavailable, so retry behavior cannot yet be observed interactively.
- Next action: continue B04 holiday and calendar-context source verification.

Batch/slice: B01 shared control contract and B02 failed placement draft retention
Status: source-complete; runtime/browser verification pending
Files changed (attributable): `apps/schedule_web/app/assets/stylesheets/components/_admin_tokens.css`, `_admin_components.css`, `_admin_workspace.css`, `_admin_workload.css`, `app/javascript/controllers/admin_context_history_controller.js`, `app/controllers/admin/schedules/events_controller.rb`
Source revision + dirty-scope identifier: Rails `e6560d0`; root pre-existing untracked files were preserved and not staged.
Runtime source/asset verification method: Rails controller syntax, ERB compilation, Zeitwerk loading, JavaScript syntax and `git diff --check` passed. The running browser connector remains unavailable, so computed-style and authenticated mutation evidence are pending.
Routes, role, safe selected context, viewport: Existing staff-only Schedule and Workload routes; runtime role, selected data and viewport remain unverified.
Checks and exact results: Admin ordinary controls now use the prescribed 40px baseline, 14px body text, compact 36px row controls and 44px primary actions; Schedule headings use 24/32 desktop and 20/28 narrow roles; Workload context/editor spacing is reduced after the legacy page rules while its five-column table remains unchanged. Schedule frame history stores the requested same-origin URL before frame navigation and uses the response URL on completion. Failed event creation now redirects with `selected_load` retained so the safe draft remains visible in the same placement inspector.
Browser/mutation/read-back evidence paths: None available; no write was sent.
Table inventory comparison: Schedule time plus weekday columns and Workload `Кафедра`, `Дисциплина и группа`, `Вид занятия`, `Часы`, `Назначение` remain unchanged.
Known remaining issue: The browser connector is still unavailable; full B00/B02 journey, computed control sizes, asset fingerprints and failure read-back remain unverified.
Next concrete action: Continue source inspection and implementation of the next plan delta, then retry authenticated runtime verification when the browser session is available.

Runtime follow-up: Rails image `milk_schedule-schedule_web:latest` was rebuilt successfully and `schedule_web` recreated. Host/container SHA-256 for `_admin_workload.css` matched (`6af84ebf1346bfe41d4d3665b3283a4e13c84730f59111e3a09feab925f1c4f7`). Propshaft served the new `components/_admin_tokens-a2f58e62.css` (`--admin-control: 40px`) and `components/_admin_workload-9c2c278d.css` (B01 authority block). `/up` returned the healthy response; unauthenticated `/admin/schedule`, `/admin/workload`, and `/admin/aggregate_schedule` each returned the expected 302 to `/?auth=1`. Authenticated browser and mutation evidence remain pending.

Runtime follow-up: Playwright MCP recovered for read-only checks. The current browser session had no staff authentication and `/admin/aggregate_schedule` redirected to `/?auth=1`; no credentials were entered. Public routes `/group` and `/group/1` rendered with zero console errors. Inside the Compose network, unauthenticated requests to both aggregate Hanami routes returned HTTP 401 (`{"error":"unauthorized"}`), confirming API-side staff protection. Hanami route loading and syntax checks passed for both occurrence actions and the aggregate repository; Rails Zeitwerk remained green.

Batch/slice: Aggregate schedule shared admin primitive alignment
Status: source-complete; unauthenticated runtime verified, authenticated read-back pending
Files changed (attributable): `apps/schedule_web/app/views/admin/aggregate_schedules/show.html.erb`, `app/assets/stylesheets/components/_admin_workspace.css`
Source revision + dirty-scope identifier: Rails `7ad2b51`; root pre-existing untracked files preserved.
Runtime source/asset verification method: Aggregate ERB compilation and Rails Zeitwerk passed. The Rails image rebuilt successfully, Propshaft served `_admin_workspace-333e6d1b.css`, `/up` returned 200, and unauthenticated `/admin/aggregate_schedule` returned the expected 302 to `/?auth=1`.
Routes, role, safe selected context, viewport: Existing staff-only aggregate route; selected date/faculty/department and viewport remain unauthenticated/unverified.
Checks and exact results: The aggregate page now uses the shared `admin-page__header`, `admin-primary`, and `admin-secondary` primitives. Date/search inputs use the 40px default control height; the seven-column dated report and print behavior remain unchanged.
Browser/mutation/read-back evidence paths: Current Playwright session has no staff authentication; no mutation was sent. Public browser checks had zero console errors.
Table inventory comparison: Aggregate dated report remains seven columns in the same order: time, group, subject, activity, teacher, room, change.
Known remaining issue: Authenticated aggregate selection, transfer/cancellation read-back and print evidence remain pending.
Next concrete action: Continue the plan's remaining source/runtime acceptance work with an authenticated disposable-data session.

Browser follow-up after rebuild: Playwright loaded the public home at `http://localhost:3000/` with HTTP 200, zero console errors/warnings, and all 38 observed document/static requests returned 200, including the current application bundles and `_admin_workspace-333e6d1b.css`. The tab has no authenticated staff session, so protected administrator rendering and mutations remain unclaimed.

Batch/slice: B06 Teachers workspace shared shell alignment
Status: source-complete; runtime asset/liveness verified, authenticated visual evidence pending
Files changed (attributable): `apps/schedule_web/app/assets/stylesheets/components/_admin_teachers.css`
Source revision + dirty-scope identifier: Rails `560316d`; root pre-existing untracked files preserved.
Runtime source/asset verification method: Rails Zeitwerk, Teachers ERB compilation, JavaScript syntax and `git diff --check` passed. The Rails image rebuilt and `schedule_web` was recreated; `/up` returned 200 and Propshaft served `_admin_teachers-121ac18f.css`.
Routes, role, safe selected context, viewport: Existing `/admin/teachers` staff workspace; authenticated role, teacher selection and viewport remain pending.
Checks and exact results: The custom Teachers header now uses the shared 82px desktop shell, 24/32 heading (20/28 narrow), 14px action text, 12px labels and 40px ordinary controls. Constraint and six-day schedule tables were not altered.
Browser/mutation/read-back evidence paths: No authenticated session was available; no mutation was sent.
Table inventory comparison: Teacher availability grid and day schedule preview retain their existing axes, rows and columns.
Known remaining issue: Authenticated computed-style, keyboard and narrow viewport evidence remains pending.
Next concrete action: Continue B06 Notice/adjacent-page consistency and retry the authenticated browser journey.

Batch/slice: B06 Notice workspace shared shell alignment
Status: source-complete; runtime asset/liveness verified, authenticated visual and print evidence pending
Files changed (attributable): `apps/schedule_web/app/assets/stylesheets/components/_admin_notice.css`
Source revision + dirty-scope identifier: Rails `af6aacf`; root pre-existing untracked files preserved.
Runtime source/asset verification method: Notice ERB compilation, Rails Zeitwerk and `git diff --check` passed. The Rails image rebuilt and `schedule_web` was recreated; `/up` returned 200 and Propshaft served `_admin_notice-403fe669.css`.
Routes, role, safe selected context, viewport: Existing `/admin/notice` staff workspace; authenticated teacher/semester context, desktop/narrow rendering and print remain pending.
Checks and exact results: Notice context/report headers, labels, links and actions now use the shared 40px/14px control rhythm while the five-column notice report and print-specific table rules remain unchanged.
Browser/mutation/read-back evidence paths: No authenticated session was available; no export mutation was sent.
Table inventory comparison: Notice retains its existing `Число`, `Часы`, `Поток, группа`, `Вид занятий`, `Аудитория` columns and print semantics.
Known remaining issue: Authenticated responsive and print evidence remains pending.
Next concrete action: Continue final adjacent-page consistency and retry the authenticated browser journey.

Batch/slice: B06 adjacent-page control targets
Status: source-complete; runtime asset/liveness verified, authenticated visual evidence pending
Files changed (attributable): `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`
Source revision + dirty-scope identifier: Rails `3938377`; root pre-existing untracked files preserved.
Runtime source/asset verification method: Rails Zeitwerk, Accounts and period-settings ERB compilation and `git diff --check` passed. The Rails image rebuilt and `schedule_web` was recreated; `/up` returned 200 and Propshaft served `_admin_workspace-1f9d99b9.css`.
Routes, role, safe selected context, viewport: Existing Accounts, Calendar period and Observability admin routes; authenticated context and viewport remain pending.
Checks and exact results: Scoped final rules raise Accounts filters, Calendar period controls, account search controls and monitoring service links to the shared 40px target; labels use 12px/16px. Existing table structures and monitoring data semantics were unchanged.
Browser/mutation/read-back evidence paths: No authenticated session was available; no mutation was sent.
Table inventory comparison: No table columns, order, grouping or report semantics changed.
Known remaining issue: Authenticated responsive and focus evidence remains pending.
Next concrete action: Retry staff browser access and complete the remaining B00/B02 mutation/read-back gate.

Batch/slice: B01/V02 Workload committed-context disclosure
Status: source-complete; runtime asset/liveness verified, authenticated interaction evidence pending
Files changed (attributable): `apps/schedule_web/app/views/admin/workload/show/show.html.erb`, `app/assets/stylesheets/components/_admin_workload.css`
Source revision + dirty-scope identifier: Rails `e648166`; root pre-existing untracked files preserved.
Runtime source/asset verification method: Workload ERB compilation, Rails Zeitwerk and `git diff --check` passed. The Rails image rebuilt and `schedule_web` was recreated; `/up` returned 200 and Propshaft served `_admin_workload-f540cb0d.css`.
Routes, role, safe selected context, viewport: Existing `/admin/workload` staff workspace; authenticated context and viewport remain pending.
Checks and exact results: Once semester/faculty/department or teacher context is valid, the page presents one readable Russian summary band and an explicit `Изменить контекст` disclosure. Existing searchable semester, faculty, department, teacher and group controls remain inside the disclosure; workload table columns and request parameters are unchanged.
Browser/mutation/read-back evidence paths: No authenticated session was available; no mutation was sent.
Table inventory comparison: Workload keeps `Кафедра`, `Дисциплина и группа`, `Вид занятия`, `Часы`, `Назначение` in the same order.
Known remaining issue: Browser computed-height, disclosure keyboard behavior and full workload-to-schedule read-back remain pending.
Next concrete action: Retry staff browser access and verify context disclosure plus the complete B02 journey.

## 2026-09-20 — Unify Calendar workspace navigation

- Status: source-complete; authenticated Calendar navigation and CRUD read-back evidence remain pending.
- Finding: the five Calendar workspaces duplicated their destination navigation, allowing active-state and transfer-route behavior to drift between pages.
- Behavior: a scoped `admin/calendar_navigation` partial now owns the five Calendar destinations, shared calendar context links, Turbo frame targeting and active-page semantics. Periods, semesters, reservations, holidays and weekday transfers pass their active key; the weekday-transfer destination consistently opens day-transfer mode.
- Files changed: `apps/schedule_web/app/views/admin/_calendar_navigation.html.erb`, `holidays/index.html.erb`, `period_settings/show/show.html.erb`, `room_reservations/index.html.erb`, `semesters/index.html.erb`, `weekday_transfers/index.html.erb`.
- Source revision: Rails `8a374ef`.
- Runtime/source verification: Rails image rebuilt, Propshaft precompiled, schedule_web recreated, Rails Zeitwerk check passed, and all six changed ERB templates compiled in the rebuilt container. The container reported healthy status; host `/up` was temporarily answered by the local proxy with HTTP 502 despite the healthy container.
- Routes, role, safe selected context, viewport: existing staff-only Calendar routes and session calendar context; authenticated navigation and responsive evidence remain pending.
- Table inventory: unchanged; period, semester, reservation, holiday and transfer table structures remain intact.
- Known remaining issue: current Playwright session has no staff authentication, and the local host proxy did not return `/up` during this rebuild check.
- Next concrete action: retry authenticated Calendar navigation and the B04 create/delete/read-back journey when the staff browser session is available.

## 2026-09-20 — Preserve selected semester in period editors

- Status: source-complete; authenticated invalid-period and read-back evidence remain pending.
- Finding: the period page and failed-save renderer always resolved the remembered/default semester, even when a valid `semester_id` was present in the URL or submitted form. A failed editor could therefore reload groups from a different semester while retaining the submitted dates.
- Behavior: both controllers now prefer the submitted semester when it exists in the loaded catalog, then fall back to the existing remembered-semester resolver only when the request is absent or invalid. Group-semester identity and safe period drafts remain tied to the selected context.
- Files changed: `apps/schedule_web/app/controllers/admin/period_settings/show_controller.rb`, `periods_controller.rb`.
- Source revision: Rails `d5eff57`.
- Runtime/source verification: Rails image rebuilt, both changed controllers returned `Syntax OK`, Rails Zeitwerk check passed, and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only period routes; authenticated invalid-range preservation and responsive evidence remain pending.
- Table inventory: unchanged; period editor units and calendar tables retain their existing structure.
- Known remaining issue: current browser session has no staff authentication, so invalid submission and authoritative API read-back cannot yet be observed interactively.
- Next concrete action: continue B04 reservation and dated-transfer contract inspection, then retry authenticated period acceptance.

## 2026-09-20 — Preserve reservation drafts during search

- Status: source-complete; authenticated reservation search, conflict and read-back evidence remain pending.
- Finding: the create reservation sheet used separate GET forms for room and teacher searches. Those requests carried the search text but omitted the current room, teacher, date, time-slot and purpose fields, so a Turbo response could silently reset selections already made in the editor.
- Behavior: a scoped `reservation-draft` Stimulus controller captures the editor values into the search request. The controller restores a permitted draft on the server before rendering the reservation frame, while the existing room/teacher IDs and API contract remain unchanged.
- Files changed: `apps/schedule_web/app/javascript/controllers/reservation_draft_controller.js`, `app/controllers/admin/room_reservations_controller.rb`, `app/views/admin/room_reservations/index.html.erb`.
- Source revision: Rails `ecb1a20`.
- Runtime/source verification: JavaScript syntax, controller syntax, reservation ERB compilation, Rails Zeitwerk check and `git diff --check` passed. Rails image rebuilt and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only reservation create/edit routes; authenticated search interaction and responsive evidence remain pending.
- Table inventory: unchanged; reservation columns, row meaning and pagination remain intact.
- Known remaining issue: current browser session has no staff authentication, so the search-preservation behavior and conflict read-back cannot yet be observed interactively.
- Next concrete action: inspect weekday-transfer creation and deletion context, then retry the authenticated reservation journey.

## 2026-09-20 — Normalize global weekday transfer scope

- Status: source-complete; authenticated global/group transfer create-delete and occurrence read-back evidence remain pending.
- Finding: the explicit `Все группы` option submitted an empty `student_group_id`, and the Rails controller passed that blank value to the API integer contract. Global transfers could therefore be rejected as invalid instead of using the supported nullable scope.
- Behavior: weekday-transfer attributes now compact blank values before the gateway call. The global option reaches the API as an omitted/nil group scope, while selected groups retain their integer identity.
- Files changed: `apps/schedule_web/app/controllers/admin/weekday_transfers_controller.rb`.
- Source revision: Rails `ab1e5ea`.
- Runtime/source verification: Rails image rebuilt, controller syntax returned `Syntax OK`, Rails Zeitwerk check passed, and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only weekday-transfer create/delete route; authenticated scope and occurrence evidence remain pending.
- Table inventory: unchanged; transfer columns and pagination remain intact.
- Known remaining issue: current browser session has no staff authentication, so API validation and schedule read-back cannot yet be observed interactively.
- Next concrete action: continue the B04 occurrence/read-back contract audit, then retry authenticated Calendar acceptance.

## 2026-09-20 — Respect group-scoped transfers on holidays

- Status: source-complete; authenticated occurrence read-back remains pending.
- Finding: occurrence expansion skipped a holiday only when there were no transfers at all. A group-scoped transfer on a holiday therefore allowed unaffected groups to match their ordinary weekday schedule.
- Behavior: holiday filtering now runs per template. A global weekday transfer permits all groups; a group-scoped transfer permits only its matching group; unaffected groups remain suppressed for the holiday. Existing weekday precedence and dated event-transfer handling are unchanged.
- Files changed: `apps/api_geteway/lib/api_geteway/queries/schedule_occurrences.rb`.
- API source revision: `0d91ab3`.
- Runtime/source verification: API syntax returned `Syntax OK`, the Hanami image rebuilt, the API container was recreated and became healthy, and `git diff --check` passed.
- Routes, role, safe selected context, viewport: existing staff/public occurrence consumers; authenticated or seeded occurrence comparisons remain pending.
- Table inventory: unchanged; no UI table or report structure changed.
- Known remaining issue: the current browser session has no staff authentication and no disposable seeded holiday/group-transfer read-back has been executed.
- Next concrete action: continue API occurrence contract inspection for cancellation/move precedence, then run authenticated schedule acceptance when the session is available.

## 2026-09-20 — Add Student Groups catalog retry

- Status: source-complete; authenticated catalog failure and CRUD read-back evidence remain pending.
- Finding: Student Groups was the remaining high-cardinality resource page whose dependency failure state only displayed passive text and offered no recovery action.
- Behavior: the failure state now exposes a labelled retry link targeting the existing `resources-workspace` Turbo frame and preserving the current URL. Group selectors, pagination and CRUD contracts remain unchanged.
- Files changed: `apps/schedule_web/app/views/admin/student_groups/index.html.erb`.
- Source revision: Rails `6e52ff8`.
- Runtime/source verification: Rails image rebuilt, the changed ERB compiled in the container, Rails Zeitwerk check passed, and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only Student Groups catalog; authenticated retry and read-back evidence remain pending.
- Table inventory: unchanged; group columns, row meaning and pagination remain intact.
- Known remaining issue: current browser session has no staff authentication, so the retry state cannot yet be observed interactively.
- Next concrete action: continue the resource/catalog failure-state sweep, then retry authenticated B03/B05 acceptance.

## 2026-09-20 — Add group-semester catalog retry

- Status: source-complete; authenticated group-semester failure and edit/read-back evidence remain pending.
- Finding: the Student Group Semesters detail page still rendered a passive dependency failure without a recovery action.
- Behavior: the failure state now exposes a labelled retry link targeting the existing `resources-workspace` Turbo frame and preserving the current group URL.
- Files changed: `apps/schedule_web/app/views/admin/student_groups/semesters.html.erb`.
- Source revision: Rails `3e686e0`.
- Runtime/source verification: Rails image rebuilt, the changed ERB compiled in the container, Rails Zeitwerk check passed, and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only group-semester route; authenticated retry and edit/read-back evidence remain pending.
- Table inventory: unchanged; group-semester columns, row meaning and editor behavior remain intact.
- Known remaining issue: current browser session has no staff authentication, so the retry state cannot yet be observed interactively.
- Next concrete action: continue the remaining adjacent-page failure-state sweep, then retry authenticated B03/B05 acceptance.

## 2026-09-20 — Collapse Schedule inspector at intermediate widths

- Status: source-complete; authenticated computed-layout and placement journey evidence remain pending.
- Finding: the Schedule planner kept its optional 300px inspector in a three-column layout through 1280px viewports. With the dark admin sidebar present, this left the timetable with an unnecessarily narrow working region even though the legacy collapse breakpoint was 1180px.
- Behavior: at 1181–1360px the planner keeps the source-load rail and timetable columns, then moves the optional inspector below the grid. The existing two-column and mobile tiers remain unchanged; the inspector is still scrollable/sticky at wider desktop widths.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_workspace.css`.
- Source revision: Rails `83c88f9`.
- Runtime/source verification: Rails image rebuilt with Propshaft precompile, the served asset was fingerprinted as `_admin_workspace-fafa21d8.css`, Rails Zeitwerk check passed, and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only Schedule route; authenticated 1280px/1360px computed-layout and mutation evidence remain pending.
- Table inventory: unchanged; Schedule time and weekday columns remain in the same table and retain local horizontal scrolling.
- Known remaining issue: current browser session has no staff authentication, so the intermediate-width layout cannot yet be inspected interactively.
- Next concrete action: continue the responsive B01/B02 source pass and retry the authenticated Schedule placement journey.

## 2026-09-20 — Retain staged Workload rooms during search

- Status: source-complete; authenticated assignment search, save and read-back evidence remain pending.
- Finding: the Workload assignment sheet replaced its room fieldset through a Turbo frame, but the room search request omitted rooms already checked in the draft. A search could therefore silently remove a staged room before the collection-replacing assignment PUT.
- Behavior: a scoped `assignment-search-context` controller carries checked `room_ids[]` into `selected_room_ids[]`. The Workload presenter restores those IDs as retained room choices after the search, and the final form submits the complete retained collection. Existing teacher selections, room authorization and API contracts remain unchanged.
- Files changed: `apps/schedule_web/app/javascript/controllers/assignment_search_context_controller.js`, `app/controllers/admin/workload/show_controller.rb`, `app/lib/presenters/admin/workload_workspace.rb`, `app/views/admin/workload/show/_assignment.html.erb`.
- Source revision: Rails `8f014e8`.
- Runtime/source verification: JavaScript syntax, controller syntax, presenter syntax, assignment ERB compilation and Rails Zeitwerk check passed. The Rails image rebuilt with Propshaft precompile and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only Workload assignment route; authenticated search/save/read-back and responsive evidence remain pending.
- Table inventory: unchanged; Workload retains its five-column report table and assignment semantics.
- Known remaining issue: current browser session has no staff authentication, so staged-room preservation cannot yet be observed interactively.
- Next concrete action: continue the B02 assignment draft audit for teacher/room collection retention, then retry authenticated workload-to-schedule acceptance.

Follow-up: Rails `81f703c` removes previously injected `selected_room_ids[]` fields before each repeated room search, preventing duplicate query values while preserving the same retained collection behavior. JavaScript syntax and `git diff --check` passed.

## 2026-09-20 — Preserve Workload editor drafts during subject search

- Status: source-complete; authenticated editor search, validation and read-back evidence remain pending.
- Finding: the Workload edit sheet’s subject search navigated the whole workspace without carrying unsaved activity type, split strategy or hour values. Searching could therefore discard a dirty editor before the user submitted the PATCH.
- Behavior: a scoped `workload-editor-draft` controller serializes the current subject, activity, split and hour fields into the search request. The controller and presenter restore those values after the result reload, while the update operation and subject identity contract remain unchanged.
- Files changed: `apps/schedule_web/app/javascript/controllers/workload_editor_draft_controller.js`, `app/controllers/admin/workload/show_controller.rb`, `app/lib/presenters/admin/workload_workspace.rb`, `app/views/admin/workload/show/_edit_record.html.erb`.
- Source revision: Rails `8712498`.
- Runtime/source verification: JavaScript syntax, controller syntax, presenter syntax, edit-template ERB compilation and Rails Zeitwerk check passed. The Rails image rebuilt with Propshaft precompile and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only Workload edit route; authenticated draft/search/PATCH/read-back and responsive evidence remain pending.
- Table inventory: unchanged; Workload retains its five-column report table and row semantics.
- Known remaining issue: current browser session has no staff authentication, so dirty-editor preservation cannot yet be observed interactively.
- Next concrete action: inspect Workload creation search for the same draft-loss pattern, then retry the authenticated B02 journey.

## 2026-09-20 — Preserve Workload creation drafts during search

- Status: source-complete; authenticated creation search, POST validation and read-back evidence remain pending.
- Finding: the Workload creation sheet’s subject search navigated the full workspace while selected groups, activity type, split mode and hour values remained only in the form DOM. Searching could discard a dirty creation draft.
- Behavior: the existing `workload-editor-draft` bridge now carries creation fields and checked groups through `editor_draft[]` parameters. The presenter restores those values, including an explicit empty-group selection, before the create form is rendered again. The create operation and group identity contract remain unchanged.
- Files changed: `apps/schedule_web/app/javascript/controllers/workload_editor_draft_controller.js`, `app/controllers/admin/workload/show_controller.rb`, `app/lib/presenters/admin/workload_workspace.rb`, `app/views/admin/workload/show/_create_record.html.erb`.
- Source revision: Rails `ae9cc47`.
- Runtime/source verification: JavaScript syntax, controller syntax, presenter syntax, create/edit ERB compilation and Rails Zeitwerk check passed. The Rails image rebuilt with Propshaft precompile and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only Workload creation route; authenticated draft/search/POST/read-back and responsive evidence remain pending.
- Table inventory: unchanged; Workload retains its five-column report table and row semantics.
- Known remaining issue: current browser session has no staff authentication, so creation draft preservation cannot yet be observed interactively.
- Next concrete action: retry authenticated B02 creation and edit journeys when a staff browser session is available.

## 2026-09-20 — Align Rooms resource table tracks

- Status: source-complete; authenticated Rooms rendering and CRUD evidence remain pending.
- Finding: Rooms renders four report columns, but inherited the generic three-track resource grid. The final action cell therefore created an implicit track and could misalign headers, values and actions.
- Behavior: the Rooms resource table now declares four explicit tracks with a bounded local minimum width: building, room type, room identity and actions. Existing column order, row meaning and horizontal access remain unchanged.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_resources.css`.
- Source revision: Rails `4fd7465`.
- Runtime/source verification: Rails image rebuilt with Propshaft precompile, Rails Zeitwerk check passed, and the recreated `schedule_web` container was healthy after startup.
- Routes, role, safe selected context, viewport: existing staff-only Rooms catalog; authenticated computed-track and CRUD evidence remain pending.
- Table inventory: unchanged; Rooms retains its four columns in the existing order.
- Known remaining issue: current browser session has no staff authentication, so rendered track alignment cannot yet be observed interactively.
- Next concrete action: continue the remaining Resources track audit, then retry authenticated B03 acceptance.

## 2026-09-20 — Keep Account search actions in normal flow

- Status: source-complete; authenticated Account sheet geometry and update evidence remain pending.
- Finding: the Account editor sticky-submit selector matched every nested form, including GET teacher and department search forms. Search buttons could therefore become competing sticky actions inside the modal body.
- Behavior: only non-GET mutation forms retain the sticky primary action. Search controls remain in normal document flow while the save and password-generation actions stay reachable in long editors.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revision: Rails `f7ac612`.
- Runtime/source verification: Rails image rebuilt with Propshaft precompile, Rails Zeitwerk check passed, and the recreated `schedule_web` container became healthy.
- Routes, role, safe selected context, viewport: existing staff-only Accounts routes; authenticated modal geometry, keyboard and update evidence remain pending.
- Table inventory: unchanged; Accounts retains its six-column report.
- Known remaining issue: current browser session has no staff authentication, so computed modal behavior cannot yet be observed interactively.
- Next concrete action: continue B05 keyboard/focus source verification, then retry authenticated Account acceptance.

## 2026-09-21 — Authenticated core journey and schedule inspector fixes

- Status: authenticated browser acceptance resumed with the supplied staff account; the core read/edit path now renders successfully.
- Evidence: `/admin/workload` loaded semester 1 and the Construction faculty with three workload rows. `/admin/schedule` opened group СИ-1 with existing lessons and the load rail; a direct event URL rendered the inspector with teacher, room, edit, transfer and swap controls. Browser console errors were zero after the fix. `/admin/aggregate_schedule?faculty_id=1&semester_id=1` resolved the faculty context and displayed two dated occurrences for 21.09.2026.
- Fixes: moved `event_entry` initialization outside the nested form block and corrected the swap target `select_tag` call, removing two 500 paths when opening an event inspector. Aggregate schedule now uses the requested `faculty_id` when the displayed URL omits `scope_id`, preventing an UNKNOWN/ID-0 context on fresh navigation.
- Files changed: `apps/schedule_web/app/views/admin/schedules/show/show.html.erb`, `apps/schedule_web/app/lib/operations/admin/load_aggregate_schedule.rb`.
- Source revisions: Rails `bb15593`, `3b3809b`, `3c68eae`.
- Runtime verification: Rails image rebuilt with Propshaft precompile, `schedule_web` recreated healthy, API and PostgreSQL healthy, and authenticated Playwright read-back completed on 127.0.0.1. No credentials were recorded in evidence or documentation.
- Remaining acceptance: no destructive mutation was performed against fixture data. A disposable workload create/assignment and lesson transfer/edit should be exercised next, followed by responsive computed-layout checks for Schedule, Workload, Resources and Accounts.

## 2026-09-21 — Disposable workload-to-schedule journey and responsive shell pass

- Status: B00/B02 functional anchor completed against disposable records and cleaned up after read-back.
- Journey evidence: created temporary workload requirement `5` for group СИ-1, assigned Кожедуб Сергей Сергеевич, selected it in Schedule, placed event `9` on Monday slot 4, edited the same event to Tuesday slot 5 with status “Изменено”, reloaded the direct event URL, and confirmed the same event ID, teacher, day, time and status. The remaining load changed from 2/2 to 0, then returned after the event and requirement were deleted. The created requirement and event are absent after cleanup.
- Responsive evidence: at 390×844 Schedule and Workload keep document width at 390px; Workload retains its 850px five-column table inside the labelled local scroller. Accounts keeps 390px document width, 20px heading, 44px primary controls and no page overflow. At 1280×900 Accounts keeps the role options in a local horizontal rail and document width at 1280px instead of expanding to 1419px.
- Fixes: the final shared admin skin now applies the 20px narrow heading role after domain styles, and the desktop Accounts role/status option rail is bounded to its own scroller.
- Files changed: `apps/schedule_web/app/assets/stylesheets/components/_admin_studio.css`, `apps/schedule_web/app/assets/stylesheets/components/_admin_accounts.css`.
- Source revisions: Rails `924e6a2`, `68a4176`.
- Runtime verification: Rails image rebuilt with Propshaft precompile, `schedule_web` recreated healthy, Rails Zeitwerk check passed, and authenticated Playwright console errors remained at zero on the verified pages. No fixture records remain from the journey.
- Remaining acceptance: complete the calendar/resource/account failure-state and print matrix, then rerun the core journey after those batches. Performance and availability optimization remain deferred by instruction.

## 2026-09-21 — Calendar and resource browser acceptance

- Status: B03/B04 read and disposable transfer acceptance advanced.
- Evidence: authenticated `/admin/rooms` and `/admin/subjects` render their list-first resource workspaces with explicit navigation and action controls. `/admin/operations`, `/admin/operations/semesters`, `/admin/holidays`, `/admin/room_reservations` and `/admin/transfers?mode=days` all load through the shared Calendar shell. Reservations now expose searchable room/teacher controls and an empty result state instead of the historical unavailable-data page.
- Transfer journey: created a temporary global weekday transfer for 2026-10-01, verified the five-column row (`Дата`, `Следует дню`, `Группа`, `Причина`, `Действия`), then deleted it through the explicit confirmation path. The list returned to “Переносы не добавлены.” and no browser errors occurred.
- Remaining acceptance: resource CRUD failure/read-back, period validation persistence, reservation mutation/conflict handling, account failure states and Notice/print verification remain pending. Performance and availability optimization remain deferred by instruction.

## 2026-09-21 — Subject resource create/delete read-back

- Status: authenticated subject resource mutation path verified with a disposable record.
- Evidence: `/admin/subjects` opened the Russian editor with full and short-name fields. A temporary `Codex Acceptance Subject 20260921` / `CAS-0921` subject was created and the success state reported “Дисциплина создано.”; it was then removed through the authenticated DELETE route and confirmed absent from PostgreSQL. Browser console errors remained at zero.
- Scope: this validates the existing list-first editor and mutation contract without changing fixture subjects. No new test files were added.
- Remaining acceptance: resource update and failure-state read-back, period validation persistence, reservation mutation/conflict handling, account failure states and Notice/print verification remain pending. Performance and availability optimization remain deferred by instruction.

## 2026-09-21 — Reservation read and mutation hardening

- Status: B04 reservation list/create/edit/delete path runtime-verified after targeted fixes.
- Findings fixed: the new reservation teacher picker lacked its live status target and raised a Stimulus error; failed reservation submissions targeted an inner Turbo frame and produced a missing-frame error instead of preserving the editor; fresh reservation navigation reopened the editor because an empty draft hash was treated as a failed draft; Hanami serialization used Rails-only `compact_blank`; and cancelled reservations remained in the active admin list.
- Behavior: teacher selection now announces the chosen person without console errors, mutation forms render full-page failure feedback with preserved draft data, clean navigation leaves the sheet closed, reservation reads serialize correctly, and soft-cancelled rows disappear from the active list while remaining stored as cancelled history.
- Files changed: `apps/schedule_web/app/views/admin/room_reservations/index.html.erb`, `app/controllers/admin/room_reservations_controller.rb`, `app/javascript/controllers/admin_sheet_controller.js`, `apps/api_geteway/slices/admin/serializers/room_reservation_serializer.rb`, `apps/api_geteway/slices/admin/repos/room_reservation_repo.rb`.
- Source revisions: Rails `7f05b07`, `6cfb405`; API `005c2b2`.
- Runtime evidence: created reservation `2026-10-15` in room 173 for Кожедуб Сергей Сергеевич, edited its purpose, deleted it, and confirmed the active list returned to the empty state. Browser console errors were zero after the fixes; the API and Rails containers rebuilt healthy.
- Conflict evidence: a disposable reservation on 2026-10-16/slot 1 was created, a duplicate attempt returned the Russian conflict message while preserving the editor draft and leaving one active row, and the anchor was then soft-cancelled. The API create response now hydrates associations before serialization, so successful writes no longer appear as generic failures after persistence.
- Additional source revision: API `a9bc2a0`.
- Period evidence: `/admin/operations?faculty_id=1&semester_id=1&group_id=1` rejected an inverted disposable lecture-week range while preserving both submitted dates, accepted and read back a temporary 2028-01-01…2028-01-07 period, then deleted it through the explicit confirmation path. The existing semester period remained unchanged; console errors were zero.

## 2026-09-21 — Account edit contract alignment

- Status: authenticated account edit read-back verified.
- Finding: the Accounts editor submitted empty optional `password` and `teacher_id` values. Hanami’s update contract correctly rejects blank optional values, so saving an unchanged global administrator returned 422 even though the UI supplied no changes.
- Behavior: Rails now removes blank optional fields at the request boundary and only renders the existing teacher identity field when a teacher is actually linked. The member PATCH route remains unchanged and role/scope authorization stays server-side.
- Source revision: Rails `249e07f`.
- Runtime evidence: saved the existing super-administrator record without changing its identity or credentials; API returned 200, the editor closed, the account remained readable, and browser console errors were zero.
- Remaining acceptance: invalid account draft feedback, generated one-time credential flow and scoped-role coverage remain pending. Password values were not captured.

- Follow-up: the Accounts index now renders shared success/error feedback. Repeating the unchanged edit after this fix displayed “Учётная запись обновлена.”, closed the editor, and produced zero browser errors. Source revision: Rails `1bd0c38`.

## 2026-09-21 — Narration-led schedule presentation

- Artifact: [administrator_schedule_creation_workflow.pptx](../../presentations/administrator_schedule_creation_workflow.pptx), with source note in [README.md](../../presentations/README.md).
- Contents: seven full-slide screenshots covering context selection, manual workload creation and assignment, lesson placement/editing, weekday transfers, and the Excel import entry point. Slides intentionally contain no instructional copy so the presenter can narrate the process.
- Verification: the PPTX ZIP passed integrity testing and contains seven slide XML parts. No credentials, tokens or session data were included.

## 2026-09-21 — Notice populated report and responsive print surface

- Status: B06 Notice screen acceptance advanced; no print dialog was invoked.
- Evidence: authenticated `/admin/notice?q=Кожедуб` selected Кожедуб Сергей Сергеевич, loaded the current semester report with 73 rows and exposed the print action. At 390px the document remained 390px wide while the 760px report table stayed inside its labelled horizontal scroller; at 1280px the document and table fit the viewport. The loaded Notice CSS contains the dedicated print rules for hiding the sidebar/screen controls, repeating table headers and avoiding row breaks.
- Print-media evidence: Playwright emulated `print` on the populated report; the sidebar and screen-only controls computed to `display:none`, the shell/main became block flow, table overflow became visible, the table header computed as `table-header-group`, and rows retained `break-inside: avoid`. No passwords or credential output were captured.
- Remaining acceptance: generated one-time credential and scoped-role failure coverage, plus a saved PDF artifact if the runtime export worker is exercised.

- Asset follow-up: CSP now allows the already-declared Google Fonts hosts in `connect-src`; after rebuilding Rails, the populated Notice route reported zero browser console errors. Source revision: Rails `c68f988`.

## 2026-09-21 — One-time credential and export gating acceptance

- Credential evidence: created a disposable teacher account through the Accounts editor with a searched teacher identity and no supplied password. The response opened the dedicated “Временный пароль” page, rendered exactly one password output of nonzero length, and showed the one-time-copy guidance. The generated value was never read, logged or documented. The disposable account was removed from the local database afterward and the filtered Accounts list returned “Учётные записи не найдены.”
- Export evidence: the Notice report correctly kept “Скачать PDF” disabled when the selected lecture-week report contained no rows. A temporary lecture-week period was created and removed after the check; the existing semester period remained unchanged. No export job was queued without report data.
- Remaining acceptance: scoped-role denial coverage requires a separate scoped administrator account; no such account was available without introducing another fixture. Performance/availability optimization remains deferred.

- Scope audit follow-up: the authenticated creation editor currently exposes only one faculty catalog entry (`Строительный факультет`, id 1), and the database has no second faculty fixture suitable for a cross-scope denial check. The Hanami policy source was inspected directly: non-super-admin account management requires matching teacher membership or faculty/kafedra scope, and scope creation is constrained to the actor’s allowed faculty. Runtime denial remains intentionally unclaimed rather than simulated with an invented catalog record.
- Remaining acceptance: explicit conflict rejection and failed reservation draft read-back, period validation persistence, account failure states and Notice/print verification remain pending. Performance and availability optimization remain deferred by instruction.

## 2026-09-21 — 320px narrow-shell verification

- Status: the plan's narrowest responsive threshold was checked after the shared shell pass.
- Evidence: at 320×844, Schedule/Workload, Accounts and Notice each kept both document and body width at 320px with no page-level horizontal overflow. Workload's required 850px table remains inside its labelled local scroller; Accounts keeps its resource table bounded to its own region. Notice retains the compact parameter state at this width and does not expand the document.
- Fix: the Schedule top bar now stacks its title and live-status badge below 380px so the status text cannot force a 357px page on a 320px viewport. Source revision: Rails `a2e5622`.
- Runtime verification: Rails image rebuilt with Propshaft precompile, `schedule_web` recreated healthy, and authenticated Playwright checks completed on all three routes. No new test files were added.

## 2026-09-21 — Searchable Subjects resource catalog

- Batch/slice: B03 resource browser, high-cardinality catalog search.
- Status: runtime-verified.
- Change: the Subjects workspace now uses the existing authorized `/admin/search/disciplines` endpoint for queries of three or more characters. The search keeps readable subject names and short names, hides pagination while filtered, preserves a Russian empty result state, and falls back to the paginated catalog for shorter input. A bounded search toolbar was added without changing table columns or row meaning.
- Files changed: `apps/schedule_web/app/controllers/admin/resources/posts_controller.rb`, `app/lib/gateways/admin/teachers_workspace_gateway.rb`, `app/views/admin/resources/posts/index.html.erb`, `app/assets/stylesheets/components/_admin_resources.css`.
- Source revision: Rails `6312f69`.
- Runtime verification: `/admin/subjects?q=Авто` returned two matching rows; an unmatched query returned “По запросу «zzzzzzzz» ничего не найдено.”; a two-character query retained the paginated catalog and displayed the minimum-length hint. At 320px document and body width remained 320px. Rails syntax checks and `bundle exec rails zeitwerk:check` passed; no browser errors were observed.
- Table inventory: unchanged three columns (`Название`, `Короткое название`, `Действия`) and existing row actions.
- Next concrete action: continue B03 CRUD failure/read-back coverage for Rooms and the remaining resource families before broadening calendar work.

## 2026-09-21 — Room CRUD deletion contract

- Batch/slice: B03 Resources, room CRUD failure/read-back.
- Finding: deleting a room returned HTTP 500 because `slices/admin/contracts/rooms/destroy_contract.rb` contained the same Dry Validation contract definition twice. Hanami raised `DuplicateSchemaError` before the action could authorize or delete the record.
- Fix: removed the duplicate definition and rebuilt the API image. Source revision: API `b52aa51`.
- Runtime verification: created disposable room `992 / Codex Room 20260921`, edited it to `Codex Room Updated 20260921`, then deleted it through the authenticated Rooms UI. The UI reported “Аудитория удалена.”, the row disappeared, and the API completed `DELETE /admin/rooms/2` with HTTP 204. No browser errors were observed; the disposable record is absent after cleanup.
- Table inventory: Rooms retains the existing four meanings (`Здание`, `Тип`, `Номер / название`, `Действия`).
- Next concrete action: exercise a rejected room create/update with preserved draft values, then continue the remaining resource families.

- Failure evidence follow-up: submitted a room create with the required catalog selections deliberately cleared while retaining `draft-993` and `Draft Room Failure`. The API rejection returned the Russian message “Не удалось создать аудиторию.”, reopened the create sheet, preserved both safe values, and created no row. This confirms the resource editor's failure retention path for Rooms.

## 2026-09-21 — Resource editor Russian copy

- Batch/slice: B03 shared resource editor copy and feedback.
- Status: runtime-verified.
- Finding: the generic resource template assembled grammatically invalid messages and actions such as “Добавить дисциплина” and “Дисциплина создано.”
- Fix: resource configurations now provide explicit Russian create labels and created/updated/deleted messages for every generic catalog family. Routes, contracts, table columns and failure behavior remain unchanged.
- Source revision: Rails `b38270a` (with search toolbar styles in `6312f69`).
- Runtime verification: Subjects rendered “Добавить дисциплину”; a disposable subject create reported “Дисциплина создана.”, search read it back, and deletion reported “Дисциплина удалена.” before the row disappeared. Browser errors were zero and the disposable record was cleaned up.
- Next concrete action: continue calendar/resource family coverage and then rerun the full core journey after the shared UI changes.

## 2026-09-21 — Calendar navigation context preservation

- Batch/slice: B04 shared Calendar navigation.
- Finding: the weekday-transfer destination and the separate lesson-transfer mode links dropped the current calendar context. Switching modes therefore returned to an unscoped transfer page even when the originating page had a selected faculty, semester, group or date pair.
- Fix: the shared calendar navigation now includes remembered context for Transfers; weekday-transfer forms and redirects retain context; lesson-transfer mode links preserve semester, faculty, group-semester and both dates; the lesson-transfer page now consumes the shared navigation partial.
- Source revision: Rails `62524f2`.
- Runtime verification: `/admin/transfers?mode=days&faculty_id=1&semester_id=1&group_id=1` rendered all five navigation links with the same context and included the context hidden fields in the create form. Lesson-transfer links preserved `semester_id=1`, `faculty_id=1`, `group_semester_id=1`, and both dates. Both desktop and document widths remained 1280px with no browser errors.
- Table inventory: weekday transfers retains its five columns; lesson-transfer grids and existing axes remain unchanged.
- Next concrete action: verify Calendar mutation failure retention after this context pass, then rerun the core workload-to-schedule journey.

## 2026-09-21 — Core journey rerun after Calendar changes

- Batch/slice: B00/B02 regression gate after shared Calendar and resource changes.
- Status: runtime-verified.
- Journey: created disposable workload requirement `6` for group СИ-1 and subject `авто`, assigned Кожедуб Сергей Сергеевич, placed event `12` on Monday slot 4, edited the same event to Tuesday slot 5 with status “Изменено”, opened its direct event URL, and read back the same event ID, teacher, placement and status. The event and requirement were then deleted through their explicit UI confirmations.
- Evidence: workload creation reported “Записи нагрузки созданы.”; assignment reported “Назначение нагрузки сохранено.”; placement reported “Занятие создано.”; edit reported “Занятие изменено.”; direct reload retained day `2`, slot `5`, status `modified` and teacher ID `1`; cleanup reported “Нагрузка и связанные занятия удалены.” and no temporary row remained.
- Responsive check: the direct event read-back remained within a 320px document width with no page overflow. Browser errors were zero.
- Next concrete action: complete the remaining Calendar mutation failure/read-back matrix and then audit the final adjacent-page regression set.

## 2026-09-21 — Weekday transfer failure draft retention

- Batch/slice: B04 Calendar mutation failure handling.
- Finding: an invalid weekday-transfer submission displayed the error alert but closed the editor and discarded the entered date and reason. The custom `weekday_transfer_draft` key had been passed as an unrecognized top-level redirect option instead of Rails flash data.
- Fix: the controller now passes the complete notice/alert/draft hash through `flash:` while retaining the current calendar context.
- Source revision: Rails `691495f`.
- Runtime verification: submitted an invalid transfer with date `2026-12-12` and reason `Draft transfer failure`, with no weekday selected. The page retained the context URL, showed “Не удалось изменить перенос дня.”, reopened the editor, preserved both values, and created no transfer. Syntax and Zeitwerk checks passed; browser errors were zero.
- Next concrete action: finish the remaining adjacent-page and final responsive/print matrix.

## 2026-09-21 — Room reservation mutation/read-back acceptance

- Batch/slice: B04 Calendar reservation editor.
- Status: runtime-verified.
- Runtime source: rebuilt Rails image serving the current Rails source; authenticated staff-only administrator at 1280×900.
- Journey: searched and selected the readable room `173 · Лаборатория кафедры ПСИЭТО` and teacher `Кожедуб Сергей Сергеевич`, created a disposable reservation for `2026-12-20`/slot `1`, edited the same row to `2026-12-21`/slot `2` and changed its purpose, reloaded the scoped URL, then deleted the disposable record through the explicit confirmation.
- Evidence: create showed “Бронирование создано.”; the edit row and direct reload showed the updated date, slot, teacher, room and purpose; deletion removed the row and restored “Бронирований по выбранному фильтру нет.”. No reservation row remained after cleanup.
- Table inventory: unchanged five meanings (`Аудитория`, `Дата / слот`, `Преподаватель`, `Назначение`, `Действия`). Browser console errors: zero.
- Known remaining issue: reservation conflict and rejected-editor draft retention still need a deliberate failure run; no new reservation code was required in this acceptance slice.
- Next concrete action: exercise Accounts invalid-input draft retention and successful edit/read-back.

## 2026-09-21 — Accounts editor action and safe draft retention

- Batch/slice: B05 Accounts editor failure/read-back.
- Finding: the shared resource hover rule made the Accounts edit trigger `opacity: 0` and `pointer-events: none` until row hover. The native sheet was therefore intercepted by its table row in the authenticated desktop flow. A rejected create also discarded the safe full-name input used for login generation.
- Fix: Accounts edit triggers are now always visible and actionable; the editor remains a fixed native sheet. Create and edit failures retain safe full-name inputs alongside email, while password fields remain empty.
- Source revision: Rails `4612984`.
- Runtime verification: a rejected teacher-account create preserved `Codex Draft Account` and its email, reopened the editor and cleared the password. A disposable teacher account was then created with a searched teacher identity, edited to disabled, reloaded and read back with the same email, teacher and status. A rejected edit preserved `Codex Edit Draft` and the attempted email while clearing the password. The disposable account was removed from the local database after verification.
- Table inventory: unchanged six meanings (`Email`, `Роль`, `Статус`, `Преподаватель`, `Область`, `Действия`). At 1280px document/body width remained 1280px; browser console errors were zero.
- Known remaining issue: scoped-role denial still lacks a second scoped administrator fixture; generated credential evidence remains deliberately unlogged.
- Next concrete action: complete final responsive/print and adjacent-page matrix, then rerun the core workload-to-schedule journey after this Accounts CSS/controller change.

## 2026-09-21 — Reservation conflict draft retention

- Batch/slice: B04 Calendar mutation failure handling.
- Runtime verification: created a disposable reservation for room `173`, `2026-12-22`, slot `3`, then submitted a second reservation for the same room/date/slot with purpose `Codex conflict draft`. The API rejected it as a conflict; the editor reopened with room ID, teacher ID, date, selected slot and purpose intact, while the original row remained unchanged.
- Cleanup: closed the failed editor, deleted the original disposable reservation through the confirmation flow, and verified the empty-state message returned. Browser console errors were zero.
- Known interaction note: while the failed editor is intentionally open, its modal backdrop correctly blocks background row actions until the editor is closed.
- Next concrete action: finish the final responsive/print matrix and rerun the core journey after the Accounts changes.

## 2026-09-21 — Final adjacent narrow-shell rerun after Accounts changes

- Routes: `/admin/accounts`, `/admin/teachers`, `/admin/notice?q=Кожедуб`, `/admin/overview`, `/admin/observability`.
- Viewport: authenticated Playwright at 320×844; every route measured document and body width exactly 320px. The Observability table columns remained inside their labelled local scrolling regions.
- Browser console: zero errors across the matrix.
- Source checks: Rails `zeitwerk:check`, changed-controller syntax check and `git diff --check` passed after rebuilding the Rails image with current Propshaft assets.
- Remaining acceptance: a final full workload-to-schedule mutation rerun after the Accounts-only change and the separately documented scoped-role fixture limitation.

## 2026-09-21 — Core journey rerun and readable Schedule subjects

- Batch/slice: B02 regression gate plus Schedule presenter correction.
- Finding: a disposable subject whose database `short_name` was the numeric value `5342` appeared in the Schedule load panel as `5342`, although the Workload page correctly showed the human-readable name `авто`.
- Fix: Schedule load entries, recommendation labels and event labels now prefer the subject name and fall back to the short name only when the name is absent.
- Source revision: Rails `272d23e`.
- Runtime journey: created workload requirement `7` for group СИ-1/subject `авто`, assigned Кожедуб Сергей Сергеевич, selected it for Monday slot 5, created event `13`, edited the same event to Tuesday slot 4 with status `modified`, reloaded the direct event URL and read back day `2`, slot `4`, status `modified` and teacher ID `1`. The Schedule load panel showed `авто` throughout. The event and workload were then deleted through their explicit confirmations.
- Evidence: creation, assignment, placement, edit and deletion each returned their Russian success feedback; no temporary workload/event remained. At 320px document/body width remained 320px and browser console errors were zero.
- Table inventory: unchanged Schedule grid axes and Workload table columns.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture.

## 2026-09-21 — Remaining resource-family render matrix

- Routes checked at authenticated 1280×900: `/admin/buildings`, `/admin/room_types`, `/admin/time_slots`, and `/admin/student_groups`.
- Evidence: each route rendered its existing table and action set, with no dependency error state, no document/body overflow and zero browser console errors. Student-group creation exposes readable specialty choices and no raw database ID field.
- Table inventory: Buildings (`Тип здания`, `Номер`, `Действия`), Room types (`Вид занятия`, `Название`, `Действия`), Time slots (`Время`, `Номер`, `Действия`) and Student groups (`Специальность`, `Год набора`, `Действия`) remain unchanged.
- Known remaining issue: full CRUD failure/read-back coverage for these additional families is still pending; scoped-role denial still requires a separate administrator fixture.

## 2026-09-21 — Resource row-action reachability and Buildings CRUD

- Batch/slice: B03 shared resource actions and Buildings CRUD.
- Finding: the generic hover rule left resource edit/delete controls with `pointer-events: none`; direct pointer activation was intercepted by the row action wrapper until a hover state happened to be established.
- Fix: resource row edit/delete controls are now always visible and actionable for pointer, keyboard and touch input. Hover remains available for row feedback rather than being the only hit path.
- Source revision: Rails `9d2a012`.
- Runtime verification: Buildings rejected create with missing building type preserved number `994`, reopened the editor and showed “Не удалось создать здание.” with no new row. A disposable building `992` was created, edited to `993`, reloaded/read back, then deleted through confirmation. The duplicate cleanup row was removed; no disposable building remains. Browser console errors were zero.
- Table inventory: Buildings retains `Тип здания`, `Номер`, `Действия`.
- Known remaining issue: full CRUD failure/read-back coverage for the remaining resource families and scoped-role denial remain pending.

## 2026-09-21 — Calendar period validation and read-back

- Batch/slice: B04 period settings.
- Runtime verification: submitted an invalid lecture-week range (`2027-02-01` through `2027-01-01`) for group-semester `1`. The page retained both submitted dates, preserved the selected context URL and showed “Даты периода некорректны.”; no period was created.
- Mutation/read-back: saved a disposable lecture-week period (`2027-01-11` through `2027-01-15`), read the same dates back from the rendered editor after redirect, then deleted it through the explicit confirmation. Success feedback was shown for save and delete, and the persisted period was gone afterward.
- Browser console errors: zero. Table structures and four-period editor composition were unchanged.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture.

## 2026-09-21 — Adjacent-page 320px containment

- Batch/slice: B06 adjacent-page responsive verification.
- Finding: at 320px the Teachers action row forced a 329px document because the create link and live-status badge stayed on one line. The Observability grid cards also inherited the minimum width of their long audit table, expanding the document to 541px despite the table's existing local scroller.
- Fix: the Teachers action row wraps below 540px while keeping both controls visible, and Observability cards now permit grid shrinkage so each labelled table region owns its horizontal scrolling.
- Source revision: Rails `4d70826`.
- Runtime verification: authenticated `/admin/teachers` and `/admin/observability` both measured 320px document/body width at 320px and 1280px at desktop width. Observability table regions retained their full column sets with local scroll widths of 326–594px. Browser console errors were zero.
- Table inventory: no columns, order, headings, grouping, row meaning or report semantics changed.

## 2026-09-21 — Room-type CRUD and database-length validation

- Batch/slice: B03 Resources, room-type editor failure/read-back.
- Runtime verification: the authenticated room-type workspace preserved a rejected create draft with the entered name when the activity type was missing. A disposable room type was then created for `Лекция`, edited, reloaded and read back with the updated name, and deleted through the confirmation flow; the catalog returned to its original row set.
- Finding: the database column limits room-type names to 25 characters, while the API contract previously accepted longer values and surfaced a PostgreSQL 500 on update. This made a normal editor mistake look like an infrastructure failure.
- Fix: API create/update contracts now enforce `max_size?: 25`; both Rails editor inputs expose the same `maxlength` constraint. The existing controller keeps the safe draft and Russian failure message when a request bypasses the browser limit.
- Source revisions: API `04a7ff8`; Rails `9554135`.
- Failure read-back: a deliberately bypassed overlong update returned the normal “Не удалось сохранить тип аудитории.” alert, reopened the editor with the long draft intact, and left the original `лекционная` row unchanged. Browser console errors were zero.
- Table inventory: unchanged two data meanings (`Вид занятия`, `Название`) plus `Действия`.
- Remaining B03 work: complete CRUD failure/read-back coverage for time slots and student groups; scoped-role denial still requires a separate administrator fixture.

## 2026-09-21 — Time-slot CRUD and chronological validation

- Batch/slice: B03 Resources, time-slot editor failure/read-back.
- Finding: the existing time-slot contract accepted an end time before its start time, so the catalog could contain an impossible slot (`19:00–18:00`).
- Fix: API create/update contracts now reject an end time that is not strictly after the start time. Rails already retained the submitted form values and translated the failure; no table or editor structure changed.
- Source revision: API `df555f4`.
- Runtime verification: a rejected disposable create (`98`, `19:00`, `18:00`) reopened the editor with all three values intact and showed “Не удалось создать временной слот.”; no row was created. A valid disposable slot was created (`98`, `18:00–18:45`), edited to `97`, `18:05–18:50`, reloaded and read back, then deleted through confirmation. The catalog returned to its original five rows.
- Table inventory: unchanged three meanings (`Время`, `Номер`, `Действия`). Browser console errors were zero.
- Remaining B03 work: complete CRUD failure/read-back coverage for student groups and their group-semester editor; scoped-role denial still requires a separate administrator fixture.

## 2026-09-21 — Student-group and group-semester CRUD validation

- Batch/slice: B03 Resources, student-group and group-semester identity preservation.
- Runtime verification: created a disposable `СИ` group for `2025-09-01` with auto-semester provisioning disabled, updated it to `2024-09-01`, reloaded and read back the same group row, then deleted it. The original `2026-09-01` group remained unchanged.
- Failure evidence: a create request with no speciality preserved the safe year (`2023-09-01`), student count (`7`), semester duration (`14`) and checkbox state while showing the Russian failure message; no group row was created.
- Finding/fix: negative student counts and non-positive semester durations were accepted by the API contracts even though the editors expressed non-negative/positive bounds. Student-group and group-semester contracts now enforce those bounds. The group-semester failure view also now renders its alert/notice feedback, and the success copy is fully Russian.
- Source revisions: API `70a68a8`; Rails `ecb8c3c`.
- Group-semester runtime: submitting `students_now=-1` for an existing disposable editor path returned 422, showed “Не удалось обновить параметры семестра группы. Проверьте значения.”, reopened the same group-semester editor with `-1` and `18` intact, and left the authoritative row at `1` and `18` after reload. Browser console errors were zero.
- Table inventory: student groups retains `Специальность`, `Год набора`, `Действия`; group-semesters retains `Группа-семестр`, `Семестр`, `Студентов`, `Параметры`, `Действия`.
- B03 status: all listed resource families have now had at least one runtime render/readback pass; focused CRUD matrix evidence exists for Buildings, Rooms, Room types, Time slots and Student groups. Scoped-role denial still requires a separate administrator fixture.

## 2026-09-21 — Final core journey rerun after Accounts and resource changes

- Batch/slice: B00/B02 regression gate after the latest Rails/API revisions.
- Runtime journey: created disposable workload requirement `8` for group СИ-1 and readable subject `авто`, assigned Кожедуб Сергей Сергеевич, selected it in Schedule, placed event `14` on Monday slot 5, edited the same event to Tuesday slot 4 with status `modified`, reloaded the event and read back the same event ID, teacher, placement and status, then deleted the event and requirement through their explicit UI confirmations.
- Evidence: Russian success feedback appeared for workload creation, assignment, placement, edit and cleanup. Schedule showed `авто` rather than the numeric short name. Reloaded event controls reported day `2`, slot `4`, status `modified` and teacher membership `1`; the grid cell carried `slot_day=2` and `slot_time=4`. The disposable requirement/event no longer appeared after cleanup.
- Responsive/runtime check: the reloaded Schedule surface measured 1280px document/body width at desktop; browser console errors were zero. The existing 320px core check remains recorded in the earlier regression entries.
- Source/runtime: current Rails image was rebuilt with Propshaft assets and current API image was rebuilt before this rerun. No new tests or table changes were introduced.
- Remaining acceptance: scoped-role denial still lacks a second scoped administrator fixture; a saved PDF artifact for Notice export is optional and was not generated. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Notice responsive and print acceptance

- Batch/slice: B06 final Notice verification.
- Runtime route: authenticated `/admin/notice?q=Кожедуб&teacher_id=1&semester_id=1&period=semester` with 73 report rows.
- Responsive evidence: at 390×844 the document and body remained exactly 390px wide; the report table retained its 760px schema inside the labelled `.notice-table-wrap` scroller (`overflow-x: auto`, 360px viewport). No columns were hidden or reordered. Browser console errors were zero.
- Print-media evidence: with Playwright print emulation, the admin sidebar and all `.notice-screen-only` controls computed to `display: none`; the table wrapper became visible overflow, the header computed as `table-header-group`, and sampled rows retained `break-inside: avoid`.
- Export note: the PDF control correctly remained disabled for the unconfigured lecture-week period; an authenticated semester report is printable but the export contract intentionally supports only lecture-week/exam-session periods. No PDF artifact was generated.
- Remaining acceptance: scoped-role denial still lacks a second scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Generated account credential flow

- Batch/slice: B05 one-time credential behavior.
- Runtime verification: created a disposable teacher account with a searched teacher identity and an empty password. The authenticated response rendered the dedicated `Временный пароль` page with an `output[aria-label="Временный пароль"]`; only the presence and length of the one-time output were checked, and the credential value was never read, logged or recorded. The page URL contained no password or credential query data.
- Cleanup: removed the disposable account by its exact email from the local database and confirmed the account search returned no row. No fixture account was changed.
- Remaining acceptance: scoped-role denial still lacks a second scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Account editor keyboard focus check

- Batch/slice: B06 adjacent interaction acceptance.
- Runtime evidence: on authenticated `/admin/accounts`, opening the create sheet moved focus to `Закрыть редактор`; pressing Escape closed the native dialog and restored focus to `Создать пользователя`. This confirms a keyboard cancellation path without changing the table or editor contract.
- Browser console errors: zero.
- Remaining acceptance: scoped-role denial still lacks a second scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Faculty and department date-resolved aggregate schedules

- Batch/slice: specification compliance F01, staff-only aggregate timetable.
- Runtime evidence: authenticated `/admin/aggregate_schedule` loaded the current faculty catalog and displayed the selected date with readable rows. The faculty scope and the department scope both returned the same occurrence window semantics, including group, subject, activity, teacher and room columns. Switching from `2026-09-21` to `2026-09-22` updated the weekday, date and rows without losing scope context.
- API path: `/admin/faculties/:faculty_id/schedule/occurrences` and `/admin/kafedras/:kafedra_id/schedule/occurrences` validate positive identifiers and ISO dates, enforce staff scope authorization, and build on the shared occurrence engine so transfers, cancellations and holidays use the same date resolution as group/teacher schedules.
- Print evidence: the selected-date button invoked the existing print controller; the report table remains the print surface while the admin shell is excluded by the shared print rules.
- Finding/fix: the seeded catalog included a zero-ID faculty row that rendered as `UNKNOWN` and could trigger an invalid `/0` request. Rails now filters non-positive catalog IDs and chooses the first positive ID when establishing default context (Rails `ccd89a2`).
- Browser console errors: zero during faculty, department and date-switch checks. No table axes or report semantics changed.

## 2026-09-21 — Workload assignment editor keyboard entry

- Batch/slice: B02 editor accessibility and safe navigation.
- Finding: the assignment side sheet was visually fixed and scrollable, but rendered as a plain `section` without dialog semantics and left focus on `BODY` after navigation.
- Fix: workload create, edit and assignment partials now expose `role="dialog"`, `aria-modal="true"` and an explicit labelled heading. The shared Stimulus controller focuses the close action on entry, traps Tab within the sheet, maps `Escape` to the existing safe close URL, and confirms before discarding a changed form (Rails `d1d5899`, `45ba066`, `b08a71a`).
- Runtime evidence: authenticated assignment editor for requirement `2` measured 500×900 at desktop, reported the dialog semantics, focused `Закрыть назначение`, wrapped forward Tab from `Сохранить назначение` back to the close action, and a dirty Escape attempt opened the Russian discard confirmation; cancelling it kept the same URL and editor draft. Browser console errors were zero.
- Table inventory and assignment identity remain unchanged.

## 2026-09-21 — Schedule URL and reservation state rerun

- Schedule context: selecting the available `СИ-1` group from `/admin/schedule?faculty_id=1&semester_id=9` committed `/admin/schedule?semester_id=1&faculty_id=1&groups[]=1`. A fresh navigation to that exact URL restored the committed context, period tabs, load panel and timetable grid; the old V03 stale-address behavior did not reproduce.
- Reservation state: authenticated `/admin/room_reservations` now rendered its searchable room filter (`173 · Лаборатория кафедры ПСИЭТО`) and the explicit empty state `Бронирований по выбранному фильтру нет.` with no dependency alert. This is an empty catalog state, not an unavailable-data fallback.
- Browser console errors: zero during both checks. Existing table and route semantics were preserved.

## 2026-09-21 — Dated lesson transfer through aggregate schedule

- Batch/slice: B04 dated occurrence transfer and F01 aggregate read-back.
- Finding: the existing Schedule transfer form returned a 500 because its controller called `gateway` without defining the existing ScheduleWorkspace gateway. After that dependency was fixed, blank optional room/time fields still reached Hanami as empty strings and caused a 422.
- Fix: the Rails transfer controller now resolves `gateways.admin.schedule_workspace` and removes blank optional transfer attributes before the API call (Rails `25fe8ba`).
- Runtime evidence: moved disposable event `7` from `24.09.2026` to `27.09.2026` through the Schedule UI. The UI showed `Изменение занятия сохранено.`. The faculty aggregate showed zero lessons on the original date and one row on the destination date with `Перенесено на эту дату`. The exact disposable transfer row was then removed and verified absent.
- Browser console errors: zero after the fix. No recurring event, table schema or transfer API contract was changed.

## 2026-09-21 — Dated cancellation through aggregate schedule

- Runtime evidence: cancelled disposable event `11` for `25.09.2026` through the same Schedule editor with no destination date. The API accepted the normalized optional fields, the faculty/department occurrence window retained the row with state `cancelled`, and the aggregate report displayed `Отменено`.
- Cleanup: removed the exact disposable cancellation row and verified `event_transfers` returned to zero rows. Browser console errors were zero.

## 2026-09-21 — Resource action-specific failure feedback

- Batch/slice: B03 shared resource editor feedback.
- Finding: generic resource delete failures were reported with the update verb (“Не удалось изменить …”), which obscured the operation that failed.
- Fix: resource redirects now pass the operation kind and produce Russian create/update/delete failure verbs while preserving existing conflict, forbidden and session-expiry handling.
- Source revision: Rails `ce5b020`.
- Runtime checks: Rails syntax and Zeitwerk checks passed; Propshaft assets were rebuilt and `schedule_web` restarted healthy. Browser console errors remained zero in the authenticated session.
- Table inventory: unchanged across all resource families.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Room and weekday-transfer workspace repair

- Batch/slice: B04 Calendar context and Turbo failure boundary.
- Finding: room reservations used a mismatched outer Turbo frame and duplicated room/date controls; the weekday-transfer editor exposed an unscoped raw group search instead of the faculty and semester context used by the scheduling workspace.
- Fix: room reservations now use the `calendar-workspace` frame, opt full-page search/filter requests out of Turbo replacement, load the selected room's date-resolved occupancy, and keep one room context date for the create editor. Weekday transfers now select semester, faculty and group before opening the editor, preserve readable course context, and submit the selected group identity without the duplicate search block.
- Source revision: Rails `af00fc9`.
- Runtime evidence: authenticated room `173 · Лаборатория кафедры ПСИЭТО` rendered occupancy for `21.09.2026` with two schedule rows; the create sheet contained one teacher search and one hidden reservation date. Authenticated weekday transfers rendered semester, faculty and group selectors with populated options and no raw group-search field. Both pages had no `Content missing` text, no browser console errors, and no horizontal overflow at 390px.
- Checks: Rails container syntax checks passed for both changed controllers; `rails zeitwerk:check` passed; Propshaft assets rebuilt and `schedule_web` restarted healthy.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Final authenticated administrator regression sweep

- Batch/slice: B06 final route-level regression after the calendar workspace repair.
- Runtime evidence: authenticated staff loaded Schedule, Workload, Rooms, Subjects, period settings, Semesters, Holidays, Room reservations, weekday transfers, Accounts, Teachers, Notice and the event journal at 1280×900. Every route returned its expected Russian page title, one main landmark, no visible `Content missing` response, no alert state and no document-level horizontal overflow.
- Targeted Calendar evidence: the room-reservation route loaded the selected-room occupancy surface; weekday transfers loaded its semester/faculty/group context. The browser console contained zero errors or warnings across the sweep.
- Source revisions: Rails `af00fc9`; workspace handoff `5a0643e`.
- Known remaining issue: staff-only acceptance is complete for the available environment. A scoped-role denial requires a separate scoped administrator fixture; performance and availability optimization remain deferred by instruction.

## 2026-09-21 — Weekday-transfer context controls and Turbo boundary

- Batch/slice: B04 transfer context interaction repair.
- Finding: the transfer context still used three dropdowns. The group selector carried a group-semester identity while the dated-rule API contract requires the base student-group identity. The reported applied-context URL was also a Turbo-frame failure risk when entered from an older cached page state.
- Fix: replaced the three selects with keyboard-operable radio-card choices. Faculty and group choice lists expose search once their catalogs exceed the bounded visible list. The context form is a deliberate top-level navigation (`data-turbo="false"`, `_top`), and calendar navigation now retains `group_semester_id`. The selected group-semester identity is translated once to its base student-group ID at the Rails boundary before the dated-rule create form submits it.
- Source revision: Rails `16ec036`.
- Runtime evidence: authenticated `http://localhost:3000/admin/transfers?mode=days&semester_id=1&faculty_id=1&group_semester_id=1&commit=Применить` rendered the selected semester, faculty, group-semester and base-group identities, zero select elements and no `Content missing` text. Clicking `Применить контекст` performed the same top-level request without a Turbo error. At 390px the document remained 390px wide with no horizontal overflow; browser console errors were zero.

## 2026-09-21 — Aggregate schedule narrow table containment

- Batch/slice: B06 aggregate schedule responsive verification.
- Finding: the faculty/department aggregate report's 980px table correctly had a labelled horizontal scroller, but intrinsic sizing from the report/context flex items expanded the entire 320px document to 1012px.
- Fix: aggregate schedule page, context, report and table wrapper now opt into shrink-to-container sizing while preserving the existing table schema and horizontal scroll region (Rails `c61b41b`).
- Runtime evidence: authenticated `/admin/aggregate_schedule?scope=faculty&faculty_id=1&date=2026-09-21` at 320×844 reports body/document/page width 320px; the labelled table region is 288px wide with 980px scroll content. No columns were hidden or reordered. Browser console errors: zero.
- Checks: Rails `zeitwerk:check` passed; Propshaft assets rebuilt and `schedule_web` restarted healthy.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Notice narrow overflow containment

- Batch/slice: B06 responsive administrator verification.
- Finding: at 320px, the Notice report header's print/export action group stayed on one flex row and expanded the document to 379px, while the report table's intended horizontal scroller was already correctly bounded.
- Fix: notice rail/grid children now allow shrink-to-container sizing; narrow report/context headers stack their controls and the action group wraps inside the page. The report table remains a 760px schema inside `.notice-table-wrap` and no columns are hidden or reordered (Rails `fb04cad`).
- Runtime evidence: authenticated `/admin/notice?teacher_id=1&semester_id=1&period=semester` at 320×844 now reports body/document width 320px with zero page overflow; the semester rail remains the labelled horizontal scroller and the report actions remain reachable. Browser console errors: zero.
- Checks: Rails `zeitwerk:check` passed; Propshaft assets rebuilt and `schedule_web` restarted healthy.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Public notice download endpoint

- Batch/slice: B06 Notice export download boundary.
- Finding: signed PDF links returned the internal Docker hostname `minio:9000`, so an authenticated browser could render the completed export page but could not download the file.
- Fix: configured the API's public notice URL storage with `NOTICE_EXPORT_PUBLIC_ENDPOINT=http://localhost:9000`; private upload storage remains on the internal MinIO endpoint. The compose configuration remains valid and the API was recreated with the new environment.
- Runtime evidence: the completed export page now emits a `localhost:9000` download link, and the authenticated browser downloaded the generated PDF successfully. Browser console errors: zero.
- Checks: `docker compose config --quiet` passed; the API container reports the public endpoint; all services remain up.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Holiday create, duplicate failure and cleanup

- Batch/slice: B04 Calendar holiday mutation matrix.
- Runtime verification: created disposable holiday `2026-12-24` with the Russian title `Проверка праздничного дня`; the list showed the persisted date and title.
- Failure evidence: submitted the same date again with title `Дубликат`; the page retained both submitted values, reopened the editor and showed `Проверьте дату и название нерабочего дня.` while leaving the original row unchanged.
- Cleanup: deleted the disposable holiday through the explicit confirmation; the list returned to `Нерабочие дни не добавлены.`.
- Browser console errors: zero. Table inventory remains three meanings (`Дата`, `Название`, `Действия`).
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Shared administrator control dimensions

- Batch/slice: B01 shared primitives, computed-style acceptance.
- Finding: Schedule search fields and cell actions inherited local padding on top of `min-height`, producing visible 48.5px and 47px controls despite the 40px/44px design roles.
- Fix: shared administrator inputs, selects, buttons and submit controls now use border-box sizing and an explicit token height; textareas retain content-driven height. Existing role-specific minimums still govern primary and compact actions.
- Source revision: Rails `a71666c` (following `71bb340`).
- Runtime evidence: authenticated Schedule at desktop reports visible controls at 40px or the intended 44px role; Workload at 390px retains 390px document/body width and its visible controls at 40px/44px. Browser console errors: zero.
- Table inventory: Schedule and Workload axes/columns unchanged.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Intermediate schedule inspector containment

- Batch/slice: B02 schedule placement editor UX.
- Finding: at the 1181–1360px breakpoint the inspector moved below the timetable and its long form had no local height limit, forcing the confirmation action below the page content.
- Fix: the intermediate inspector now remains sticky, bounded to the viewport and internally scrollable; the existing submit action remains sticky within the form. The timetable grid and table structure are unchanged.
- Source revision: Rails `8c6b4a3`.
- Runtime evidence: authenticated 1280×900 selected-load editor reports an 868px inspector with `overflow-y: auto`; after the page reaches the inspector, the submit action is visible at viewport y 788–832. Document/body width remains 1280px and browser errors remain zero.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Narrow Schedule inspector regression check

- Batch/slice: B02 responsive regression after intermediate inspector containment.
- Runtime evidence: authenticated selected-load Schedule at 390×844 keeps document/body width at exactly 390px; the inspector remains bounded to the viewport (`max-height: 812px`, local vertical scrolling) and its submit action remains inside the scrollable editor. Browser console errors: zero.
- Table inventory: Schedule time axis and six weekday columns remain unchanged.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Atomic lesson swap acceptance

- Batch/slice: B02c/B04 dated lesson swap operation.
- Runtime verification: selected the existing `Автомобили` occurrences on `21.09.2026` slot 3 and `22.09.2026` slot 1 in the authenticated Calendar transfer workspace, opened the explicit swap confirmation and submitted it with an empty optional reason.
- Evidence: the UI returned `Занятия обменены местами.` and the API created exactly two reciprocal moved occurrence records. The records were removed by their exact disposable event/date predicates, returning `event_transfers` to zero; the underlying recurring schedule events were unchanged.
- Fix: Rails now removes blank optional swap reasons before calling the API, matching the dated-move normalization (Rails `273e986`).
- Table inventory: both transfer grids retain their existing `Время` and `Занятие` columns. Browser console errors were zero.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Compact administrator navigation labels

- Batch/slice: B06 responsive navigation accessibility.
- Finding: at narrow widths non-active sidebar links collapse to icon-only controls, but their labels were not explicit attributes for hover discovery or assistive technology.
- Fix: shared sidebar links and unavailable navigation items now expose their Russian label through `title` and `aria-label`; active-route styling and desktop composition remain unchanged.
- Source revision: Rails `e66a153`.
- Runtime evidence: authenticated Workload at 390px reports 390px document/body width; every compact navigation item exposes matching `title` and `aria-label`, and `Нагрузка` retains `aria-current="page"`. Browser console errors: zero.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Searchable reservation teacher selectors

- Batch/slice: B04 reservation editor control matrix.
- Finding: room reservation create/edit sheets provided bounded room search, but teacher choices were an unfiltered long list despite teachers being a high-cardinality entity.
- Fix: both teacher fieldsets now use the shared `choice-filter` controller with a labelled search input and explicit no-match state. Hidden teacher person IDs and the reservation write contract remain unchanged.
- Source revision: Rails `0733312`.
- Runtime evidence: authenticated reservation create sheet renders the teacher search field (`Фамилия или имя`) alongside the room search; at 390px document/body width remains exactly 390px and browser console errors are zero.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Calendar transfer catalog filtering

- Batch/slice: B04 Calendar transfer context.
- Finding: the lesson-transfer context rendered the seeded zero-ID faculty row as `Unknown`, allowing an invalid catalog option to appear beside the valid faculty.
- Fix: semester, faculty, group-semester, time-slot and room catalogs used by the transfer workspace now retain only positive identifiers, while preserving the existing request identity and table structures (Rails `dc7e9b5`).
- Runtime evidence: authenticated transfer context now renders only `Строительный факультет` with faculty value `1`; no `Unknown` option or `/0` context is present. At 390px document/body width remains exactly 390px and browser console errors are zero.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Reservation conflict draft retention

- Batch/slice: B04 Calendar reservation failure matrix.
- Runtime verification: authenticated staff created a disposable reservation for room `173 · Лаборатория кафедры ПСИЭТО`, teacher `Кожедуб Сергей Сергеевич`, `2026-12-30`, slot `1`, then submitted a second reservation for the same room/date/slot.
- Failure evidence: the API conflict was rendered as `Комната уже занята на эту дату и время. Проверьте черновик и выберите другой слот.`; the create editor reopened and retained room ID `1`, teacher ID `1`, date `2026-12-30`, slot `1` and purpose `Temporary conflict duplicate`.
- Cleanup: the original disposable reservation was removed through the UI confirmation and its authoritative row is now `cancelled`; no fixture reservation was changed.
- Browser console errors: zero. Reservation table columns remain `Аудитория`, `Дата / слот`, `Преподаватель`, `Назначение`, `Действия`.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Localized audit entity filter

- Batch/slice: B06 adjacent administrator UX, event journal.
- Finding: the journal exposed backend entity identifiers such as `Student group semester periods` and `Study load requirements`; its filter was an unbounded raw identifier text field.
- Fix: added Russian labels for emitted audit resources and replaced the free-text filter with a bounded native select that submits the existing API identifiers. Unknown future resources now use the neutral Russian label `Объект системы` instead of leaking an identifier.
- Source revision: Rails `ef3045f`.
- Runtime evidence: authenticated `/admin/overview` renders the select with `Все объекты`, localized options and localized rows for period and workload events. Existing journal columns and pagination remain unchanged; browser console errors: zero.
- Checks: container Zeitwerk passed; Propshaft assets rebuilt and `schedule_web` restarted healthy.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Localized audit field summaries

- Batch/slice: B06 adjacent administrator UX, event journal inspector.
- Finding: the audit inspector summarized changes with raw snake-case backend keys, which made the Russian staff UI difficult to scan.
- Fix: common audit fields now render Russian labels; the existing expandable sanitized payload preserves the detailed technical representation for inspection.
- Source revision: Rails `f25a33f`.
- Runtime evidence: authenticated event `119` now reports `Связанные аудитории`, `Связанные занятия`, `Связанные назначения`, `Связанные назначения преподавателей` and `Требование нагрузки`; browser console errors: zero. Journal table and inspector structure are unchanged.
- Checks: Propshaft assets rebuilt, `schedule_web` restarted healthy, and container Zeitwerk remains passing.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Excel import authenticated workflow

- Batch/slice: Excel import runtime acceptance carried forward from the migration handoff.
- Runtime verification: authenticated super administrator opened `/admin/excel_imports?semester_id=1`; the page retained `2026/2027 · 1-й семестр`, rendered the drop zone, status refresh control and six-column file history table.
- Mutation/read-back: dropped a disposable `.xlsx` workbook into the drop zone, received `Файл отправлен на обработку.`, and observed the authoritative file row with the original filename, semester context and `Ошибка обработки` status from the deliberately minimal workbook. This confirms upload, asynchronous status read-back and original filename persistence without changing fixture files.
- Cleanup: deleted the disposable upload through its explicit confirmation; the file row was removed from the history.
- Browser console errors: zero. Table columns remain `Файл`, `Структура`, `Семестр`, `Обновлён`, `Статус`, `Действия`.
- Checks: Rails container Zeitwerk passed; all services remained healthy. The existing processed fixture file was not modified.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Notice period context preservation

- Batch/slice: B06 Notice report navigation and export context.
- Finding: opening `/admin/notice?period=lecture_week`, searching for a teacher and selecting the result dropped the period parameter, silently switching the report back to the semester-wide range.
- Fix: notice search, teacher-result and semester links now retain the selected period while changing their own context value (Rails `22d7ebc`).
- Runtime evidence: authenticated lecture-week flow for `Кожедуб Сергей Сергеевич` preserved `period=lecture_week`, rendered the `Лекционная неделя` report label and kept the period navigation selected. The current fixture has zero lecture-week rows, so PDF remains correctly disabled by the existing empty-report guard.
- Browser console errors: zero. Notice table columns remain `Число`, `Часы`, `Поток, группа`, `Вид занятий`, `Аудитория`; print/export contracts were unchanged.
- Known remaining issue: a populated lecture-week/exam-session fixture is still needed for successful PDF worker read-back; scoped-role denial requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Department notice batch PDF read-back

- Batch/slice: B06 Notice export worker and department batch print.
- Finding: the batch job was queued and completed, but its Rails status page returned HTTP 500 because `export_return_path` called `.compact` on the URL string returned by a route helper.
- Fix: removed the invalid string `.compact` calls from both individual and department export return paths (Rails `e137984`).
- Runtime evidence: authenticated department workload (`Строительный факультет · ПСиЭТ`, semester 1) queued `lecture_week` batch export for the department. The API worker completed the job, produced the merged PDF and one teacher PDF, and the status page now renders `Готово`, `Файлы сформированы`, `Скачать общий PDF` and `Отдельные извещения (1)`.
- Browser console errors: zero. The status page returns HTTP 200 and its return link preserves the department/semester context. No schedule or workload records were modified.
- Checks: Rails image rebuilt and restarted; container Zeitwerk passed. Generated signed URLs were not copied into documentation or logs.
- Known remaining issue: individual populated notice export and scoped-role denial still need separate acceptance coverage. Performance/availability optimization remains deferred by instruction.

## 2026-09-21 — Individual notice PDF worker read-back

- Batch/slice: B06 Notice individual export completion.
- Runtime verification: authenticated teacher `Кожедуб Сергей Сергеевич`, semester 1 and `lecture_week` export contract was queued through the Rails endpoint, processed by the notice worker and read back from the authoritative status endpoint.
- Evidence: the worker completed job `66ec5cba-1d0c-41d0-a8b6-b413efc1eadf`, persisted one teacher PDF, and the Rails status page returned HTTP 200 with `Готово`, `Файлы сформированы`, a signed `Скачать общий PDF` link and `Отдельные извещения (1)`.
- Return-path evidence: the status page links back to the same teacher, semester and `lecture_week` context. The report fixture currently has no lecture-week rows, so the export was exercised through the authorized worker contract rather than the disabled empty-report button.
- Browser console errors: zero. No schedule, workload or teacher records were changed.
- Known remaining issue: scoped-role denial still requires a separate scoped administrator fixture. Performance/availability optimization remains deferred by instruction.

## 2026-09-23 — Two-date lesson transfer and positional week parity

- Batch/slice: B00 journey read-back, B01 Schedule/Workload control polish, B04 dated lesson transfers.
- Status: runtime-verified for the administrator journey, two-date batch save/read-back, repeated move, moved-in swap, single and two-item conflict retention, and desktop/mobile layout. Cross-group teacher/room conflict and scoped-role denial remain unverified.
- Attributable files: Rails transfer controller, gateway, Stimulus controller, transfer view/grid, Schedule view/event partial, scoped calendar/workspace/studio/workload CSS; API batch action/contract, dated occurrence read action, event transfer/schedule event repositories, scope resolver, routes. Pre-existing dirty Rails files were preserved and are not wholly attributable to this slice. Root design README was updated separately.
- Source revisions at verification: Rails `16ec036` plus working tree; API `70a68a8` plus working tree. Both Docker images were rebuilt from the current source and restarted healthy; Propshaft emitted new digested assets. The authenticated browser loaded the new card geometry and text.
- Browser journey: semester 1, faculty 1, group semester 1; disposable workload and teacher assignment led to a placed Schedule event, an edited parity value, reload and read-back. Transfer selection moved two dated occurrences in one save. A subsequent batch move returned them, then an individual move and same-day exchange of moved-in occurrences succeeded with authoritative dated read-back. An occupied slot rejected a move, preserved both lessons, and reopened the editor with the attempted date/slot/reason. Batch preview disabled Save for a visibly occupied target; a deliberately submitted conflicting two-item batch was rejected atomically, kept all original placements, and restored both selections and the disabled preview.
- Table inventory: Schedule retains time/day axes; dated transfer grids retain `Время`, `Занятие`; Workload retains `Кафедра`, `Дисциплина и группа`, `Вид занятия`, `Часы`, `Назначение`. At 390px the transfer tables scroll inside labelled regions and the document has no horizontal overflow. Equal upper/lower Schedule parity track heights were measured in-browser. Browser console errors: zero.
- Checks: changed Ruby syntax, Rails Zeitwerk, and transfer Stimulus `node --check` passed. Evidence and open gates are linked from [the design package](../admin-ux-2026-09-23/README.md).
- Next concrete action: verify cross-group teacher/room conflict and scoped authorization with suitable fixtures; then finish the remaining workbench acceptance matrix without changing table schemas.

## 2026-09-23 — Transfer tab navigation regression

- Finding: from `/admin/transfers?mode=days`, clicking `Переносы занятий` rendered Turbo's `Content missing` because the day-transfer view lived in `calendar-workspace` and the lesson-transfer response did not contain that frame.
- Fix: both transfer-mode links explicitly target `_top` in both views. The Calendar destination navigation already used `_top` and was left intact.
- Runtime evidence: authenticated browser reproduced the error before the change, then completed days → lessons → days after rebuilding Rails. Both destination titles and URLs changed correctly and no browser console error remained.
- Additional interaction evidence: dragging a moved-in lesson from slot 2 to empty slot 3 on the same displayed date opened the dated editor, saved, and read back slot 3. Dragging it back restored slot 2, confirming that an already moved occurrence can change slots within its displayed date.

## 2026-09-23 — Transfer context and batch draft alignment

- Finding: changing a date input left the previously loaded tables on screen until `Показать расписание`, but the batch preview would use the unsaved date. This could stage a move to a date whose timetable the administrator had not seen. Submitting the context form also discarded a selected batch without an explicit decision.
- Fix: batch preview requires the two date inputs to match the dates used for the displayed tables. A changed date/group form asks before discarding a selected transfer or pending exchange; cancelling keeps the selection and entered dates, accepting reloads the new tables. Client-side catalog searches now have accessible Russian labels and no form name, so date changes no longer append empty search parameters to the shareable URL.
- Runtime evidence: with one selected lesson, editing date 2 blocked preview and showed an instruction to load the schedule. Rejecting the context-change prompt kept the URL and selection; accepting it updated both table headings and cleared the selection. An unchanged context still opened the normal batch preview, and submitting the visible dates produced a URL containing only semantic context fields.
- Checks: rebuilt Rails/Propshaft, Stimulus `node --check`, and browser console inspection; no new browser errors.

## 2026-09-23 — Schedule lesson editor sheet

- Finding: selecting a timetable lesson placed its editor below the full-height grid at desktop width, forcing a long scroll away from the selected cell.
- Fix: the existing edit and creation content now opens in a right-side modal sheet, full-width on narrow screens. The timetable keeps its two working columns. The sheet asks before discarding changed input; the selected lesson's week detail uses the same Russian labels as the timetable.
- Runtime evidence: clicking event 19 opened the sheet at the right edge of a 1280px viewport; the timetable remained 574px high. At 390px, both the edit sheet and the empty-slot creation sheet filled the viewport without document horizontal overflow. With a selected workload, the creation sheet exposed its `Создать занятие` form, and Escape closed it back to the same workload context. Rejecting the close prompt kept the unsaved choice; accepting it restored the saved lesson. The edit form submitted and a fresh authenticated load read back the saved even-week value.
- Turbo navigation note: `turbo:before-cache` fired after the frame rendered but before the history update; closing the live dialog in that hook hid it after a normal timetable click. The hook was removed, and click-to-open was retested. Browser console errors: zero.
- Checks: rebuilt Rails/Propshaft, `node --check` for the new controller, and `git diff --check`; no new test files.

## 2026-09-23 — Reservation context and CRUD read-back

- Finding: reservation data now loads in the running app, superseding the older unavailable-data observation. Opening the create sheet without a room led to a dead end; searching for a teacher inside a selected-room sheet dropped `room_id` and `occupancy_date`. Successful mutations also returned to an unfiltered list.
- Fix: the create action requires a selected room and gives a visible instruction when none is selected. Teacher search carries the selected room and occupancy date while retaining the draft. Create/edit redirects use the submitted room/date; delete carries the displayed context. Failed writes use the draft room to reconstruct the editor and occupancy context.
- Runtime evidence: selected room 173 and date 2026-09-23; teacher search for Кожедуб preserved the room, date and open sheet. A disposable reservation was created, read back, edited, read back again, then deleted. A duplicate for its occupied slot returned a Russian conflict message, reopened the sheet with room/teacher/date/slot/purpose intact, and left exactly one original row. The final delete returned to the same room/date with zero rows.
- Checks: Rails image rebuilt and restarted; container Ruby syntax and Zeitwerk passed. No new tests or test files. Broader scoped-role and cross-group transfer conflict gates remain open.

## 2026-09-23 — Transfer teacher identity and batch regression

- Finding: transfer destination checks compared `teacher_on_kafedra_id` membership IDs. The schedule occurrence projection also carries the stable teacher person `id`; a teacher assigned through two departments can have different membership IDs and still be one person.
- Fix: transfer plans and occupied occurrences now compare teacher person IDs. This applies to single moves, swaps and batch pair checks without changing assignment write IDs.
- Runtime evidence: rebuilt the API image and used the authenticated two-date workspace for 2026-09-23/24. Selected events 7 and 16 together; preview mapped each to the other date at its original slot (2 and 5). Saved once, reloaded and read both on the target date; selected both again, saved the reverse batch, and reloaded to confirm both original placements. No lasting schedule change remains.
- Limit: the current database has one base student group and no teacher with multiple department memberships. The browser run proves batch regression behavior but cannot prove cross-group teacher conflict rejection; that gate needs a suitable fixture. API Ruby syntax passed and the running API was healthy.

## 2026-09-23 — Accounts filtered return context

- Finding: account create/edit success returned to the unfiltered list, and the one-time credential return link also lost the list context. Search, role, status and page are now carried as view parameters through mutation forms and validated before building the return URL.
- Runtime evidence: the authenticated filtered list at `q=admin&role=super_admin&status=active` reopened its edit sheet, saved the existing administrator record without field changes, showed `Учётная запись обновлена.`, and stayed at the same filtered URL with one account row. A failed create without the required teacher reopened the sheet with safe name/email fields intact and an empty password field. The search term used in this pass returned no teacher; a later pass below verified selection using an existing teacher.
- Checks: rebuilt and restarted Rails from the current source; container Ruby syntax, Zeitwerk and `git diff --check` passed. Browser console errors: zero. The one-time credential link was inspected in source but not exercised, to avoid generating a new password for the active administrator.

## 2026-09-23 — Resource CRUD and list context

- B03 runtime journey: created a disposable Building Type, reloaded to read it back, edited its short name, reloaded again, then deleted it with confirmation. A final fresh load showed no disposable row. The three report columns remained `Название`, `Короткое название`, `Действия`.
- Finding and fix: the shared Resource controller redirected every successful mutation to the first unfiltered page. Create/edit/delete forms now carry their current page and, for Subjects, search query; the return path validates and retains those view parameters. No resource write payload or API contract changed.
- Runtime verification after rebuilding Rails: an unchanged Subject edit from a searched list returned to the same query with a success notice and its row visible. Another unchanged edit from page 2 returned to page 2 with the same first row. The browser was reauthenticated after the container restart; no credentials were written to evidence. Browser console errors: zero.
- Checks: container Ruby syntax, Zeitwerk and `git diff --check` passed. Failure-draft behavior for this resource family and scoped-role denial still require suitable validation/role fixtures; the current fixture did not provide them.

## 2026-09-23 — Resource validation feedback

- B03 failure journey: bypassed the browser-only `required` guard to submit an empty short name against the server contract. Create rejected without adding a row and kept the entered full name in the reopened sheet. A disposable Building Type then exercised the same failed edit: the list retained its original short name while the sheet retained the attempted blank value. The disposable row was deleted and a fresh load showed it absent.
- Fix: for an API invalid-request response with a missing required resource field, the shared controller now supplies one explicit Russian field message inside the reopened editor. Other failures retain the existing generic feedback. The message uses the existing admin danger token and is announced once through `role=alert`.
- Runtime verification after rebuilding Rails: an invalid Building Type create showed exactly one `Укажите короткое название.` alert inside the open sheet, kept the safe name draft, and created no row. Container Ruby syntax, Zeitwerk and `git diff --check` passed; browser console errors: zero. Other validation shapes and scoped-role denial remain open.

## 2026-09-24 — Calendar period date recovery

- B04 finding: a reversed Lecture Week range kept both submitted dates, but its generic error appeared above all four period cards. The rejected form now shows one specific Russian date-order error inside its own card, marks the end-date input invalid, and links it to the message. All eight period date inputs now have unique IDs.
- Runtime verification after rebuilding Rails: group-semester 1, semester 1; submitting 2026-10-10 through 2026-10-01 kept both values in the Lecture Week card, showed one alert, and left the existing Academic Semester start at 2026-09-01. A fresh reload showed the Lecture Week still absent. A disposable valid Lecture Week (2026-10-05 through 2026-10-11) saved, survived a fresh reload, then was deleted; a final reload showed the original empty Lecture Week and unchanged Academic Semester. Browser console errors: zero.
- The browser session had expired because the local Postgres and MinIO containers stopped overnight; the existing services were restarted without touching storage. API, Rails, database, MinIO and workers are running again. Container Ruby syntax, Zeitwerk and `git diff --check` passed. Scoped-role failure and the other period kinds remain open.

## 2026-09-24 — Holiday conflict and CRUD read-back

- B04 finding: duplicate holiday dates reached the API as a database uniqueness error, but ROM raised `ROM::SQL::UniqueConstraintError`; the action rescued only the Sequel exception. The API returned generic 422 and Rails told the administrator to check the date and name. The action now handles the observed ROM error as HTTP 409. The existing gateway maps 409 to conflict, so the sheet shows the specific Russian duplicate-date message beside the date field, retains both inputs, and marks the date invalid.
- Runtime evidence: submitting 2026-09-08 again returned API 409, kept the original 2026-09-08 row, and showed one `Такая дата уже отмечена как нерабочая.` alert in the open sheet. A disposable 2026-09-09 holiday returned API 201, survived a fresh list load, then was deleted with API 204; a final load showed only the original row. Calendar faculty, semester and group-semester context stayed in the URL after create and delete.
- Checks: rebuilt API and Rails; both changed Ruby files passed syntax, Rails Zeitwerk and both repository diff checks passed; browser console errors: zero. Holiday edit is not an available route, so it was not simulated through delete/create. Other dated-rule and scoped-role acceptance remains open.

## 2026-09-24 — Day-transfer scope and conflict read-back

- B04 finding: a duplicate group-scoped day transfer was rejected but showed a generic failure above the page. As with Holidays, ROM raises `ROM::SQL::UniqueConstraintError`, which the Sequel-only action did not catch. The action now returns HTTP 409 for that constraint; the reopened sheet shows one `Для этой даты уже задан перенос.` alert, retains date/weekday/reason, and marks the date input invalid.
- Group scope runtime: created a disposable transfer for group-semester 1 on 2026-09-26 following Friday; a fresh load showed the base-group label and reason. A duplicate submission returned API 409 and left one original row. The original was deleted with API 204, and a fresh load showed it absent.
- Global scope runtime: choosing `Все группы` produced a blank `student_group_id` write field and explicit all-groups hint. A disposable 2026-09-27 transfer following Monday returned API 201; a fresh load showed `Все группы`. It was deleted with API 204; the final transfer list was empty. The five table columns stayed `Дата`, `Следует дню`, `Группа`, `Причина`, `Действия`.
- Checks: rebuilt API and Rails; both changed Ruby files passed syntax, Rails Zeitwerk and both repository diff checks passed; browser console errors: zero. The context GET form still emits an extra `commit` query parameter when applying `Все группы`; this is URL noise, not an identity or persistence error. Scoped-role coverage remains open.

## 2026-09-24 — Account role draft and searched selection

- B05 finding: the existing teacher catalog returned `Кожедуб Сергей Сергеевич`, and selection persisted through another search with name/email draft intact. Switching the new-account role away from Teacher cleared the hidden teacher ID but left the selected-teacher label visible; switching back therefore showed a false selection. Department and faculty choices had similar draft-loss or irrelevant-field submission risks.
- Fix: the role controller keeps teacher, department and faculty choices in the unsaved draft, disables write fields for inactive roles, and shows only the active role's selected-entity summary. The existing search and API write contracts are unchanged.
- Runtime evidence after rebuilding Rails: selected the teacher through search and a department through search, then switched among Teacher, Department Administrator and Faculty Administrator. Browser `FormData` contained only the active role's teacher or scope field; inactive selections remained available after switching back. The faculty radio stayed checked while disabled and submitted again when Faculty Administrator was restored. Name/email draft remained intact. Closing the dirty sheet presented Save, Discard and Continue; the disposable draft was discarded and no account row was added.
- Checks: `node --check` and repository diff check passed before rebuild; final browser verification had no mutation. Full account creation/read-back and scoped administrator authorization remain open.

## 2026-09-28 — Existing-account teacher picker

- B05 regression: the edit sheet omitted its teacher ID target when an account had no linked teacher. Choosing a teacher from search then raised a Stimulus action error. The sheet also showed teacher and department search controls for unrelated roles.
- Fix: always render the edit teacher ID input, disable it unless the draft role is Teacher, and show the teacher and department search sections only for their corresponding roles. The role controller reads the account's existing role for managers who cannot change roles. Existing API update and scope contracts are unchanged.
- Runtime verification after rebuilding Rails: the super-admin edit sheet initially hid both searches and excluded teacher ID from `FormData`. Switching the unsaved draft to Teacher exposed its search; choosing the existing catalog match filled the ID and selected-person hint without a console error. Switching back to Super Administrator hid the search again, retained the draft choice, and excluded teacher ID from `FormData`. No account update was submitted. Browser console errors: zero; `node --check`, asset precompile, and repository diff check passed. Scope editing across role changes still needs separate contract-aware work and read-back.

## 2026-09-28 — Account edit scope draft across roles

- B05 finding: the edit sheet displayed an empty scope fieldset for global roles and kept prior faculty/department inputs active when the draft role changed. The API replaces the whole scope collection and rejects scopes of the wrong kind. The edit form also had no way to pick a faculty, while a blank teacher ID was dropped by Rails rather than clearing a link during a non-teacher role change.
- Fix: the edit sheet shows scope controls only for Faculty or Department Administrator, adds a bounded searchable faculty choice, and submits only scope IDs for the active role. A blank scope entry explicitly clears the collection when switching to a global or Teacher role; a separate blank teacher input clears the prior link when leaving Teacher. Role switches retain inactive selections in the unsaved browser draft. Rails now passes explicit null teacher IDs on update; create behavior is unchanged.
- Runtime evidence after rebuilding Rails: with the sole super-admin account in an unsaved edit draft, selected the available faculty, then searched and selected department `ПСиЭТ`. Switching between these roles retained both chips but `FormData` included only the active scope kind plus the blank clearing entry. Switching to Teacher and selecting the existing catalog person submitted a teacher ID and no filled scope; switching back to Super Administrator submitted blank teacher and scope values while hiding both role-specific sections. Discarded the draft; a fresh load still showed one unchanged super-admin row. Then submitted an unchanged super-admin edit through the server: the success notice appeared, and a fresh read showed one active super-admin with global scope and no teacher. Browser console errors: zero. Ruby syntax, Rails Zeitwerk, JS syntax, asset precompile and diff checks passed. Scoped-role mutation and authorization still need their own read-back.

## 2026-09-28 — Overview journal at narrow widths

- B06 confirmed runtime defect: at 390px the Overview audit table hid its `Инициатор` header and every cell in that column. The audit entry therefore lost its actor in the list, despite the table's four-column source schema.
- Fix: removed the narrow-width column-hiding rule, kept all four headers/cells, set a 600px minimum table width, and labelled the existing horizontal scroll container as a keyboard-focusable journal region with a visible focus outline. The journal and inspector structure is unchanged.
- Runtime verification after rebuilding Rails: at 390px all four columns have table-cell display; the journal region measures 356px wide with 600px scroll content, receives focus and responds to ArrowRight while the document itself has no horizontal overflow. Opening an event still puts its inspector above the table, and every column remains available. At 1280px the table fits without horizontal scrolling. Browser console errors: zero; asset precompile and repository diff check passed. Full B06 keyboard/print/public-surface matrix remains open.
- Adjacent Notice check at 390px: the authenticated semester report has 143 rows and retains all five headers inside its 760px local scroller without document overflow. Under print-media emulation, the sidebar and on-screen controls are hidden, the table header is a repeating header group, and sample rows avoid breaks. A later headless Chromium PDF check found a printed skip link overlapping the first-page table and a sixth A4 page containing only two rows; see the print correction below.

## 2026-09-28 — Notice multipage print correction

- B06 real PDF finding: the 143-row semester report printed to six A4 pages. The keyboard skip link appeared over the first-page table and at page breaks. Two rows were stranded on page six. Later B06 screen selectors overrode the earlier print padding and header spacing.
- Fix: the Notice-only final print rules hide the skip link, remove the screen page padding and header minimum height, and tighten table cell padding by one pixel vertically while retaining 10pt table text, all five columns and repeating table headers.
- Runtime verification: used the authenticated Firefox browser's in-memory session to launch local headless Chromium and print the current 143-row report. The resulting PDF has five A4 pages with 29, 31, 31, 31 and 21 rows. Text extraction found all 143 rows and all five headers on every page, with no skip-link text. Rendered pages 1, 3 and 5 were visually inspected: no column clipping, overlap, blank edge page or broken row. The temporary PDF and renders stayed under `/tmp`; no session data was written to evidence or the repository. Asset precompile and diff check passed.

## 2026-09-28 — Teachers workspace and compact mobile navigation

- B06 finding: the Teachers search workspace still used prominent sequential `01–06` numerals and a tall ink search block; at 390px the block was 351px tall. The shared sidebar intended an icon strip on mobile, but grouped links stretched the flex row into a 276px navigation area.
- Fix: removed decorative section numerals, reduced the search heading and panel spacing, and kept the search input and action in one touch sized row on narrow screens. Added a separate mobile navigation strip with labelled links; the grouped desktop navigation remains intact and is hidden at phone widths. This avoids relying on nested `<details>` flattening in a flex container.
- Runtime verification after Rails rebuild: at 390px the sidebar is 218px high, the mobile nav is 60px, and the teacher search panel is 244px (down from 351px). At 320px the page remains 320px wide with no document overflow; the nav scrolls locally and teacher search controls stay side-by-side. Tabbing through the mobile strip reaches each labelled link with visible focus and scrolls the focused link into view. At 1280px the existing grouped sidebar remains visible and the mobile strip is hidden; the search panel is 150px. The selected teacher still shows the seven-column, five-row availability table in its local scroller on mobile and without extra scrolling at desktop. Browser console errors: zero. Asset precompile and diff check passed. Full teacher edit/constraint mutation acceptance remains open.

## 2026-09-28 — Teacher availability toggle read-back

- B06 behavior check: traced the Teachers cell button through the Rails toggle operation, the API list/create/delete contracts, and the presenter’s per-cell state. The operation creates a blocked constraint when no exact row exists and deletes that row when toggled again.
- Runtime verification: on the selected teacher/semester/week context, chose a neutral Monday 10:10 cell (pressed `false`, no cell state, six existing marks). Clicking it returned the Russian “restriction added” notice and showed blocked state; a fresh page load kept the cell blocked and mark count at seven. Clicking again returned “restriction removed”; another fresh load showed the cell neutral and count six, matching the original read. Availability table still has seven headers and five time rows; page width stays within the 320px viewport and browser console errors: zero. No test files were added. Profile edit, inherited-cell navigation, conflict and forbidden-role paths remain open.

## 2026-09-28 — Shared navigation and public surface regression check

- Batch/slice: B06 shared mobile navigation regression after Teachers shell change.
- Runtime evidence on the current running Rails revision: navigated from Workload into `/admin/schedule?semester_id=1&faculty_id=1&groups[]=1` through the rendered shell. The committed context showed semester 1, faculty 1 and group СИ-1; the existing seven workload requirements appeared in both the Workload list and Schedule assignment panel. Opened the existing `Физика` editor from the timetable and confirmed its recurring fields and dated-transfer/swap actions remained available. At 320px the schedule document stayed 320px wide and the labelled timetable scroller contained its 780px table. No schedule record was changed.
- Public surface check: after client data loaded, `/`, `/teacher`, `/group`, and `/room` rendered their public navigation/content at 320px with no document horizontal overflow. These sampled states do not cover every public detail route or zoom/accessibility case.
- Browser console errors: zero. Source/asset build and the full create-to-reload journey remain covered by the September 23 evidence above; this focused regression check covers navigation, context handoff and editor access after the shared mobile-nav change.
- Known remaining issue: full B06 keyboard/print/public surface matrix, teacher profile edit, constraint conflict and forbidden-role paths remain open.
- Next concrete action at that checkpoint: verify a safe teacher profile edit/read-back or a supported inherited-cell navigation path, then complete scoped-role acceptance when a scoped administrator fixture is available. The inherited-cell route is verified in the following entry.

## 2026-09-28 — Teacher context links commit URL

- Batch/slice: B06 teacher week and semester navigation.
- Finding: in the selected even-week view, following an inherited blocked cell changed the table to `Каждую неделю` inside the outer `teachers-workspace` Turbo frame, but left `week_type_id=4` in the browser address. Reload then returned to the even-week view. The semester and week context links used the same frame behavior.
- Fix: the semester links, week-type links and inherited-cell links in `app/views/admin/teachers/show/show.html.erb` now target `_top`, so each context change commits its route to browser history.
- Runtime verification: rebuilt and restarted the current Rails image. From semester 1/even week, the inherited Monday 08:30 cell moved to `week_type_id=6`; a fresh load retained `Каждую неделю`. Switching back to even week updated to `week_type_id=4`, and reload retained `Чётная неделя`. Selecting semester 2 updated to `semester_id=2`; reload retained semester 2, even week, teacher and query. Returned the browser to its original semester 1/even-week route. No teacher profile or constraint data was changed.
- Browser console errors: zero. Rails image asset precompile succeeded; current ERB rendered and the links exposed `data-turbo-frame="_top"`.
- Known remaining issue: teacher profile save/failure read-back, constraint conflict handling and scoped-role authorization remain open.
- Next concrete action: verify a safe teacher profile edit on a disposable fixture; if none exists, continue read-only B06 viewport/keyboard checks and leave write acceptance explicitly pending.

## 2026-09-28 — Teachers reduced-motion and keyboard check

- Batch/slice: B06 responsive/accessibility sampling.
- Runtime evidence: at 640px (half the 1280px desktop width as a 200%-zoom-equivalent reflow check), the document remained 640px wide. The availability table retained all seven columns inside its local scroller (606px viewport, 900px table). Under `prefers-reduced-motion: reduce`, the preference was active and no page overflow appeared. Starting from the loaded teacher workspace, Tab focused the skip link with a visible 2px outline. After correcting the table scroller markup below, at 390px it exposed role `region`, the Russian name `Таблица ограничений по дням и времени`, and `tabindex=0`; focusing it showed a 2px outline. Tabbing into Wednesday automatically scrolled the 900px table inside its 356px viewport while the document remained 390px wide.
- Scope: read-only. The available teacher is a named seeded record, not a disposable edit fixture, so profile values were inspected for labels but no update was submitted.
- Browser console errors: zero. One Firefox warning during container rebuild reported a stylesheet preload not used; the current `application-a51e40bd.css` stylesheet is enabled and exposes its rules. No tests or test files were added.
- Known remaining issue: profile save/failure retention, availability conflict and forbidden-role paths, true browser zoom, and the rest of the B06 public/keyboard matrix remain unverified.
- Next concrete action: locate or create an explicitly disposable teacher fixture through the supported CRUD contract before testing profile mutation; otherwise continue read-only B06 matrix work.

## 2026-09-28 — Observability tables scroll by keyboard

- Batch/slice: B06 narrow-table keyboard access.
- Finding: at 390px the performance table was 436px wide inside a 352px scroll viewport, and the audit table was 598px wide. Both regions had names and `tabindex=0`, but focusing the performance region and pressing ArrowRight left `scrollLeft` at zero; that table has no focusable descendants to provide another keyboard path.
- Fix: added a small table-scroll Stimulus controller for ArrowLeft/ArrowRight and Home/End when the labelled region itself has focus, plus a Russian ARIA description/key shortcut list and a 2px visible focus outline. Cell links and other descendants retain their normal key behavior. The existing table schemas are unchanged.
- Runtime verification: at 390px ArrowRight moved the performance table from 0 to its 36px end, and Home returned it to 0. On the audit table ArrowRight reached its 246px end; Tab then focused the first `Открыть` link inside the scroller. The document stayed 390px wide throughout. All four ordered table headers remain unchanged. At 640px the four tables fit their 602px local regions; at 1280px they fit their existing 471px/994px panels, and the document matched the viewport at both widths.
- Checks: `node --check` for the controller, Rails image asset precompile, current page render and repository diff checks passed. Browser JavaScript errors: zero. Firefox again emitted a transient stylesheet-preload warning after container rebuild; the current application stylesheet is enabled and exposes its rules.
- Known remaining issue: the wider profile edit/failure, constraint conflict and forbidden-role acceptance remains open; this slice verified table keyboard access only.
- Next concrete action: continue the B06 acceptance matrix with any remaining named route/state gaps, keeping profile mutation pending until a disposable teacher fixture and safe cleanup path are available.

## 2026-09-28 — Public detail routes after shared styles

- Batch/slice: B06 public-route responsive smoke check.
- Runtime evidence from the current Rails build: at 390px, the teacher, group and room indexes and their detail pages rendered without document overflow. The group journey opened faculty 1, course 1, group `СИ-1`, selected the ordinary schedule type, then opened `Выбрать расписание` at `/schedule?date=2026-09-01&group=1`. The schedule page loaded at 390px without horizontal document overflow. At 1280px, the schedule, teacher and room detail routes also rendered with their expected titles and no overflow.
- Scope: read-only navigation; no profile or schedule mutations. Public table and route semantics were unchanged.
- Known remaining issue: these route checks do not complete the full B06 viewport/keyboard matrix, nor teacher profile save/failure, constraint conflict, or scoped-role authorization acceptance.

## 2026-09-28 — Observability narrow and wide viewport matrix

- Batch/slice: B06 follow-up for the monitoring workspace.
- Runtime evidence: with the authenticated session, Observability rendered at 320, 390, 768, 1280 and 1440 CSS pixels. At every width the document and body stayed equal to the viewport; each of the four named table regions retained its own horizontal scrolling where its ordered table required more width. The four accessible names resolve through their heading IDs, and each region exposes the Russian keyboard instructions.
- At 320px, focused the audit table region and pressed ArrowRight eight times; its scroll position reached the 316px end while document width remained 320px. The current page has no JavaScript errors. One earlier account-picker console error remains in the browser's historical log, outside the current page load; it is excluded from this slice's result and should be checked if that account flow is reopened.
- Scope: no data mutation. Browser zoom itself was not available through this Playwright session; viewport reflow sampling does not substitute for true 200% zoom acceptance.
- Remaining B06 work includes actual browser-zoom and print checks plus the pending teacher profile save/failure, constraint conflict, forbidden-role and scoped-authorization paths.

## 2026-09-28 — Lesson transfers route and multi-selection staging

- Rechecked the reported “Content missing” path in the authenticated browser: opened `/admin/lesson_transfers`, followed the `Переносы занятий` tab to `/admin/transfers`, selected semester 1, `Строительный факультет` and group `СИ · 1 курс`, then loaded the two-date schedule. The Rails page rendered both date tables and current occurrences; the inspected 2026-09-28 source table was empty and 2026-09-29 showed its current and already-transferred lessons.
- Selected two lessons on 2026-09-29 and opened the batch editor. Its staged preview placed them on 2026-09-28 in their original periods (periods 1 and 2). The operation remained staged until explicit confirmation; I closed it and cleared the selection without saving, so no transfer data changed.
- At 390px both schedules stacked within the 356px content area; their 420px tables remained in local scroll regions and document width stayed 390px. Returned the browser to the lesson-transfer page at 1280px with group and dates selected for review.
- This reproduced a valid empty-context state before a group is chosen, not the reported Turbo “Content missing” response. The direct tab transition and loaded grouped schedule both work in the current runtime. This verification does not certify the multi-transfer write/read-back or every drag/drop target; no new transfer was created.
- UX refinement: the context submit now says `Показать группы` before the semester/faculty group list is loaded, and a status line explains the next step (or reports an empty group catalog). When groups are available but none is selected, the hint asks for a group selection. With a selected group, the button remains `Показать расписание`.
- Runtime verification after the standard Rails image rebuild: direct `/admin/lesson_transfers` shows the correct first-step label and instruction; semester 1/faculty 1 shows the group-selection hint; the selected-group route renders both date tables at 1280px, with no page overflow or console errors. Build asset precompile and repository diff checks passed. The staged multi-transfer preview was opened and dismissed before this markup refinement; no data writes were made.

## 2026-09-28 — Two-date transfer drag staging recheck

- With semester 1, faculty 1, group СИ-1 and the two current dates loaded, dragging `Автомобили` from 2026-09-29 to the empty first period on 2026-09-28 opened the transfer editor prefilled with target date 2026-09-28 and period 1.
- Dragging `5342` from period 4 to period 5 on its own source date also opened the editor with original date 2026-09-29, target date 2026-09-29 and period 5. This confirms a destination on the source date is stageable.
- Both editors were closed without confirming. A fresh page load showed the same occurrences, zero selected checkboxes and no open dialogs. No transfer mutation was issued. Cross-date and same-date write/read-back remain separate from this staging check.

## 2026-09-28 — Schedule parity cards constrained to their cells

- B01 acceptance recheck: even-only and odd-only lessons render in equal-height upper and lower halves, and common-week lessons span the full cell width. Long lesson titles exposed a width defect: a common-week card for `Учебная практика «Автоматизация учета»` rendered at 130px inside a 115px cell, overlapping its neighbor.
- Fix: constrained Schedule event cards to their grid area with `min-width: 0`, `max-width: 100%`, border-box sizing and wrapping for long words. Week labels, ordered axes, row grouping and event semantics are unchanged.
- Runtime verification after the normal Rails image rebuild: at 1280px no common event card exceeded the cell content width, and the even/odd tracks remained equal height. At 390px the 780px timetable remained inside its labelled 360px scroller, document width stayed 390px, there were no overflowing event cards, and every even/odd pair had equal widths with the odd track below the even track. Browser console JavaScript errors: zero. Propshaft asset precompile and both repository diff checks passed.
- The shared timetable still needs the wider B01/functional acceptance gates already listed above; this focused fix is not a claim that all schedule interactions were reverified.

## 2026-09-28 — Account teacher picker historical error recheck

- Rechecked `/admin/accounts` on the current Rails image using the unsaved create sheet: searched `Кожедуб`, selected the catalog match, and confirmed the selected-teacher summary appeared with no alert or current-page JavaScript error. Closed the sheet without creating an account; the existing account table remained unchanged.
- The earlier `account-teacher#choose` console entry was historical and did not reproduce in this current flow. The separate teacher profile edit/failure and scoped-authorization acceptance remains open; this is a picker-only check.

## 2026-09-28 — Resources navigation grouped by domain

- Finding: the Resources workspace exposed 15 links at the same visual level across three rows, using 148px of navigation height and 287px for the full heading/context block. The flat list obscured subject areas and consumed space before the catalog table.
- Fix: grouped the existing routes into four domains — Учебная структура, Сотрудники, Обучение and Помещения — and show only the active domain's existing catalog links in a secondary row. The links and catalog table structures remain unchanged. The navigation block now uses 84px and the full header/context block 223px at desktop.
- Browser verification on the rebuilt Rails image: clicking Учебная структура from `/admin/rooms` navigated to `/admin/faculties` and updated the title/content; clicking Учебные группы then navigated to `/admin/student_groups` and updated all three consistently. This also verified the links target the top-level page rather than leaving stale URL state in the resources Turbo frame.
- At 390px, the domain navigation is 108px tall and the active catalog links 74px tall; both wrap into two columns, and document width remains 390px. Browser console errors: zero. No catalog data was changed. Rails asset build and root/Rails `git diff --check` passed.

## 2026-09-28 — Notice print controls hidden in print output

- B06 finding: the Notice report's `.notice-screen-only` actions retained the `Печать` and PDF controls under print media. The screen-only empty-state message shared that class and could also appear in printed output.
- Fix: added a page-scoped print rule hiding `.notice-screen-only`; report title, five-column table schema, and print-specific row/header rules are unchanged.
- Runtime verification after `docker compose up -d --build schedule_web`: loaded teacher Кожедуб Сергей Сергеевич, semester 1, 2026/2027; emulated print at 1280px. Sidebar and all three screen-only regions computed to `display:none`, including report actions; document/table widths were 1280px; the five headers remained in original order; all 143 report rows remained present; `thead` computed to `table-header-group` and body rows to `break-inside:avoid`. Print-render screenshot: `.playwright-mcp/page-2026-09-28T17-02-36-290Z.png`.
- Browser JavaScript errors: zero. Firefox reported its transient application stylesheet preload warning after rebuild. Rails asset precompile and root/Rails `git diff --check` passed. This print-media render does not verify physical multipage pagination, blank edge pages or printed page count. True browser zoom is also still unverified; Ctrl+Equal in the connected browser session did not change its device scale or CSS viewport.

## 2026-09-28 — Notice context selection commits URL and reload state

- Finding: choosing a teacher from search rendered the report inside `notice-workspace` but left the browser at `/admin/notice`; reload discarded the selected report context. Semester and period links used the same frame target.
- Fix: the teacher result, semester and period links in `app/views/admin/notice/show/show.html.erb` now target `_top`, committing each durable selection to the route and browser history. Search submission and recoverable retry links remain frame-scoped.
- Runtime verification on the rebuilt Rails image: searched Кожедуб, selected Кожедуб Сергей Сергеевич, changed to semester 2 (2026/2027), then selected `Лекционная неделя`; each click updated the browser URL. Reload retained teacher, semester and period. Returned the browser to the teacher's semester 1 report for review (143 rows). The rendered context links all exposed `data-turbo-frame="_top"`.
- Shared-control regression recheck on current Workload: at 320, 390, 768 and 1280px, document/body widths equalled the viewport. The existing five columns stayed in the 850px labelled table scroller at 320/390/768; at 1280 the table fit its 982px panel. At 320, focusing the table region and pressing ArrowRight moved horizontal scroll from 0 to 43px. At 390, visible primary buttons/inputs measured 40–44px high and the heading remained within the page. Ordered table headers remain `КАФЕДРА`, `ДИСЦИПЛИНА И ГРУППА`, `ВИД ЗАНЯТИЯ`, `ЧАСЫ`, `НАЗНАЧЕНИЕ`.
- Notice print emulation at a 390px viewport retained all five columns and 143 rows, with the table/header inside the viewport, screen-only actions hidden, repeated-header display and row break avoidance. At 1280px, the print table spans the page width. Physical pagination was already verified in the preceding `Notice multipage print correction` entry: five A4 pages, all 143 rows, repeated headers, and visual inspection found no clipping, overlap, blank edge page or broken row.
- Browser JavaScript errors: zero. Rails asset precompile and root/Rails `git diff --check` passed. Actual 200% browser zoom remains unverified; the connected session did not respond to Ctrl+Equal as browser zoom.

## 2026-09-28 — Accounts create-sheet keyboard and dirty-draft check

- B05 read-only acceptance: at 390×844, the create-user sheet opened as a native modal dialog, measured 374px wide with no document overflow, and received initial focus on `Закрыть редактор`. Escape closed the blank sheet and returned focus to `Создать пользователя`.
- Entered only disposable placeholder name/email values. Attempting to close opened the `Есть несохранённые изменения` alertdialog. `Продолжить редактирование` retained both values; closing again and choosing `Отменить изменения` closed the dialog, cleared the draft, and restored focus to the opener. The in-frame account list still contains only the seeded administrator; no account request was submitted.
- Verification: authenticated `/admin/accounts`, 390px viewport, browser JavaScript errors zero. This does not verify account creation/read-back, failed create retention, credential generation, or scoped-role authorization.

## 2026-09-28 — Accounts filters preserve URL and visible state

- Finding: the email/role/status GET filters updated the `accounts-workspace` frame without advancing the URL/history. Reset changed the route but Turbo's permanent search input retained the old query, leaving visible input state inconsistent with the unfiltered results.
- Fix: the list filter form, reset link and pagination links use Turbo `advance`; the query input is permanent only while a query is present, and the existing `entity-search#rememberFocus` action restores focus after submission. No account mutation or table-schema change.
- Runtime verification on the rebuilt Rails image: searched for the seeded admin email, selected `Главный администратор` and `Активна`, and submitted. URL became `/admin/accounts?q=admin%40milk-schedule.local&role=super_admin&status=active`; the query, selected role/status and matching row remained correct after direct reload. Earlier in the same check, Reset returned to `/admin/accounts` and cleared the query; browser Back restored the query state. Current-page console errors: zero. An older historical `account-teacher#choose` error did not reproduce in its later picker recheck recorded above.
- Scope: one seeded account means pagination links were not traversed, and this does not cover account create/edit/authorization workflows.

## 2026-09-28 — Calendar context removes repeated headings

- Batch/slice: B04 context selector clarity. On `/admin/operations`, each loaded selector showed its name twice: once as a visual wrapper label and again as the fieldset legend. Removed only the redundant wrapper label; retained the fieldset legends and show a wrapper label only when that catalog is unavailable, so the fallback state remains identified.
- Files changed: `app/views/admin/period_settings/show/show.html.erb` (targeted ERB lines only). No table, route, context or mutation contract changed.
- Runtime/source: rebuilt and restarted `schedule_web` with `docker compose up -d --build schedule_web` from source HEAD `16ec036`; authenticated browser reloaded the rendered page. Before screenshot: `.playwright-mcp/page-2026-09-28T17-30-56-905Z.png`; after: `.playwright-mcp/page-2026-09-28T17-33-58-679Z.png`.
- Verification: at 1280px each loaded selector now has one legend, document width is 1280px, and the context form is 524px tall (the prior wrapper labels are gone). At 390px document width remains 390px; all 2 faculty and 8 semester choices remain present in their bounded selection areas, with accessible group names intact. Browser console errors: zero. No catalog selection or period mutation was submitted.
- Remaining B04 and B06 acceptance is unchanged, including scoped-role checks and true browser zoom.

## 2026-09-28 — Weekday transfer context omits submit text from URL

- Batch/slice: B04 weekday-transfer context. Reproduced the known URL noise on `/admin/transfers?mode=days&semester_id=1&faculty_id=1`: applying the visible context appended `commit=Применить контекст` even though the button text is not context state.
- Fix: set `name: nil` on that GET form's submit button. The form still requires explicit submit and carries the selected semester, faculty and group scope.
- Runtime verification: after rebuilding `schedule_web`, reloaded the same route with semester 1, the available faculty, and `Все группы` selected. Applying the context navigated to `/admin/transfers?mode=days&semester_id=1&faculty_id=1&group_semester_id=` with no `commit` parameter. The transfer mode and selection remained in the resulting context. This was a read-only GET; no calendar record was created or removed. Source HEAD: `16ec036`; browser console errors: zero.
- Files changed: `app/views/admin/weekday_transfers/index.html.erb` (one submit helper option). `git diff --check` passed in Rails and workspace repositories. Remaining B04 acceptance includes scoped-role coverage and broader state/viewport checks.

## 2026-09-28 — Mobile admin navigation reveals the active workspace

- Batch/slice: B06 shared-shell navigation. At 320px, the active Calendar item began at x=386 while the mobile navigation viewport ended at x=320 (`scrollLeft=0`), so the current workspace was invisible on entry.
- Fix: added a small Stimulus controller to the mobile navigation. On connect and viewport resize it scrolls the existing active link into view within the nav only; it does not change DOM order, focus, route state or desktop navigation.
- Files changed: `app/views/admin/shared/_sidebar.html.erb` (controller mount) and new `app/javascript/controllers/admin_mobile_nav_controller.js`.
- Runtime/source: rebuilt and restarted `schedule_web` with `docker compose up -d --build schedule_web` from source HEAD `16ec036`; authenticated browser loaded Calendar, changed viewport from desktop, then navigated Schedule → Workload. Evidence screenshot: `.playwright-mcp/page-2026-09-28T17-44-07-753Z.png`.
- Verification: after load/resize, active Calendar is fully inside the nav at 680, 390 and 320px; document width equals the viewport at each width. At 1280px the mobile nav remains hidden and the desktop sidebar's active route is Schedule. At 320px, clicking Schedule then Workload updated the active visible item and retained `faculty_id=1&semester_id=1`; Workload rendered all seven current rows and the unchanged five ordered headers inside its 290px labelled scroller (850px table), with no document overflow. Browser console errors: zero. No workload or schedule mutation was submitted. `node --check` and both repository diff checks passed.
- Scope: this verifies the shared-shell navigation segment and table access; it does not rerun the full workload-create/assignment/place/edit/read-back mutation journey. Do that on a confirmed disposable local fixture as required by the acceptance plan.

## 2026-09-28 — SoL-Pi project setup and transfer-route recheck

- SoL-Pi is installed project-locally from `.pi/git/github.com/NVlabs/SoL-Pi` at `1559b5cb12c72da4a485bc50fe326586b216fb19`; Pi is `0.85.1`, Node is `22.22.1`. Removed the duplicate user-wide package registration so the project registration is the only active scope. Project trust is already persisted.
- Updated only `.pi/sol-pi.json`: all four mechanisms are enabled, using the default reducer provider/model route and `cacheWriteReadRatio: 12.5`. The effective-config preflight passed. Pi opened its offline TUI without an extension-load error; no authenticated provider is configured for Pi in this environment, so no model request or task run was performed.
- SoL-Pi source validation: `npm run check` passed (typecheck, 19 files / 158 tests, package dry run); `node scripts/check-pi-compat.mjs` passed; `npx vitest run tests/all-mechanisms.test.ts` passed (4 tests). `npm audit --audit-level=high` could not reach the npm audit endpoint because the configured proxy returned HTTP 407; dependency audit status remains unknown.
- Authenticated browser recheck: opening `/admin/lesson_transfers` and following `Переносы занятий` navigated to `/admin/transfers` without Turbo `Content missing`. With semester 1, faculty 1 and group-semester 1 selected, both dated schedule tables rendered (five period rows each); the body contained no `Content missing` text and browser console errors were zero. No transfer was saved.
- Safety check: group-semester 2 had zero curriculum streams, requirements and schedule events. Its baseline is empty, but no supported Rails action was found to remove a newly created parent stream after deleting its requirement. The workload → assignment → placement → edit → reload mutation journey remains pending until a fixture with a complete supported cleanup path is available.

## 2026-09-28 — Two-date transfer selection by keyboard

- On the authenticated, loaded transfer page for semester 1 / faculty 1 / group-semester 1, focused the selection checkboxes for two dated lessons and selected each with Space. The batch editor showed `2026-09-29 → 2026-09-28` at periods 1 and 2, preserving each original time slot as requested.
- Closed the staged preview and cleared both selections. Browser inspection confirmed zero checked lessons, a closed batch dialog, and no transfer mutation request. This verifies the keyboard selection and staged destination path; it does not claim a keyboard-only save or mutation read-back.
- Browser snapshot of the staged preview: `.playwright-mcp/page-2026-09-28T18-01-20-433Z.yml`.
- The API does expose authorized `DELETE /admin/student_group_semesters/:id/load`, which removes all streams and dependent records, but the Rails application has no proxy route for this operation. Keep the fixture-based workload journey pending until cleanup can use an existing authorized flow; do not introduce a destructive UI action solely for test cleanup.

## 2026-09-28 — Reduced-motion transfer workspace check

- Emulated `prefers-reduced-motion: reduce` on the loaded two-date transfer page. The preference matched; the sampled admin buttons and transfer table cells computed to zero transition and animation duration, and document plus table-region scrolling computed to `auto`.
- Browser screenshot: `.playwright-mcp/page-2026-09-28T18-05-08-159Z.png`.
- No data changed. This covers the transfer workspace only; true 200% browser zoom and the broader remaining B06 route/state matrix are still open.

## 2026-09-28 — Transfer editor keyboard cancel and focus return

- Focused the dated `Автомобили` event button and pressed Enter. The single-transfer native dialog opened with its close button focused and the transfer editor labelled by its heading.
- Pressed Escape. The dialog closed, focus returned to the same event button, no selection remained, and no transfer request was sent. Snapshot while the dialog was open: `.playwright-mcp/page-2026-09-28T18-06-59-895Z.yml`.
- This verifies keyboard open/cancel and focus return for the single-transfer editor; save/failure retention remains covered only by the prior write/read-back evidence and broader role/conflict cases remain open.

## 2026-09-28 — Two-date batch preview by keyboard

- Selected two lessons using Space, focused `Перенести выбранные`, and opened the batch editor using Enter. The dialog focused its close control and listed both mappings to the other date at original periods 1 and 2.
- Pressed Escape; focus returned to `Перенести выбранные`. Tab focused `Снять выбор`, and Enter cleared the selection. Final browser state had zero checked lessons, zero open dialogs and zero transfer mutation requests. Snapshot of the keyboard-opened preview: `.playwright-mcp/page-2026-09-28T18-08-21-245Z.yml`.
- This verifies the keyboard selection → preview → cancel → clear journey; batch save and its read-back remain separate acceptance gates.

## 2026-09-28 — Mobile transfer selection tap target

- B06 finding: at a 390px viewport, each `Выбрать для переноса` label measured 32px high. This was a small tap target for selecting lessons into a batch.
- Fix: added a page-scoped 44px minimum height for those labels only under the existing 680px mobile breakpoint. The event cards, date controls, desktop density, and both timetable schemas remain unchanged.
- Runtime verification: rebuilt `schedule_web`; the authenticated 390px page loaded the current fingerprinted stylesheet, all three selection labels measured 44px, and document width remained 390px. Clicking the first label selected its lesson; `Снять выбор` cleared it. At 1280px the labels remain 32px, the document remains 1280px, zero lessons remain selected, and the four ordered table headers are still `Время`, `Занятие` on both dates. Browser JavaScript errors: zero. Firefox emitted one stylesheet-preload warning after rebuild, while the active stylesheet loaded and computed the new 44px rule correctly.
- Screenshot: `.playwright-mcp/page-2026-09-28T18-10-54-165Z.png`. Full admin/API repository `git diff --check` passed. No schedule mutation occurred.

## 2026-09-28 — Accounts table keyboard scrolling

- B06 finding: the 320px Accounts page kept its six-column table inside a labelled, focusable local region, but ArrowRight did not scroll its 654px overflow. The region was already named by `accounts-heading`; no extra label was needed.
- Fix: connected the existing `table-scroll` controller and its ArrowLeft/ArrowRight/Home/End instructions to that region. No columns, order or row meaning changed.
- Runtime verification after rebuilding `schedule_web` from Rails source HEAD `16ec036`: at 320px, ArrowRight moved 229px, End reached 654px and Home returned to 0; Tab focused the row's `Изменить` action. The document remained 320px wide. At 1280px all six columns fit in the 982px region and the document remained 1280px. Authenticated account listing only; no account was edited. Snapshot: `.playwright-mcp/page-2026-09-28T18-13-57-562Z.yml`.
- Broader account acceptance remains open for filter round-trip, edit draft failures, role-specific forbidden scopes and 200% browser zoom.

## 2026-09-28 — Accounts filter and create-sheet keyboard path

- Submitted the visible email query `admin` through the Accounts filter. The GET URL and search field retained the query after page reload; the result contained one matching account row. `Сбросить` returned to `/admin/accounts` with the query cleared. No account fields were changed.
- Focused `Создать пользователя`, opened its side-sheet dialog with Enter, then cancelled with Escape. Focus returned to the trigger button; the form was never submitted.
- This verifies the filter URL round-trip and create-sheet keyboard cancel only. Edit validation/failure retention and role-scope authorization remain open. No credentials, password values, or account identifiers were recorded here.

## 2026-09-28 — Accounts empty-search state

- Submitted a no-match email query. The page retained it in the URL and search field across reload, showed the Russian no-results state, omitted the table, and kept the `Сбросить` action available. Reset returned to the unfiltered table.
- At 1280px the document remained viewport-width throughout. This was a read-only check; no account data changed.

## 2026-09-28 — Accounts duplicate-email feedback and failed-sheet focus

- Reproduced the safe duplicate-email rejection in the create sheet. The API operation checks for an existing email before account creation and also has a database uniqueness guard, so this request could not add or change an account. Before the fix, Rails reduced the API's `email_taken` result to the generic `Проверьте email, роль и область доступа.` message.
- Added an additive `code: "email_taken"` to that API 422 response, mapped only that code to the Rails `:email_taken` outcome, and added the Russian message `Аккаунт с таким email уже существует.` Other 422 responses retain the existing generic mapping.
- Reused the matching `data-admin-sheet-id-param` trigger when the server reopens a failed editor. After the error, the sheet stayed open with its safe email/role draft, password stayed empty, the original account row count remained one, and Escape returned focus to `Создать пользователя`.
- Runtime source: Rails HEAD `16ec036`, API HEAD `70a68a8`; rebuilt both images through `docker compose up -d --build schedule_web`. Rails Zeitwerk and changed Ruby/JS syntax checks passed. Browser JavaScript errors: zero; root/Rails/API `git diff --check` passed. No tests were added, no credentials/passwords were recorded, and no account data changed. Message screenshot: `.playwright-mcp/element-2026-09-28T18-25-34-456Z.png`.

## 2026-09-28 — Teacher create drawer keeps its action reachable

- B06 finding: opening `Создать преподавателя` made a fixed-height panel whose header, department search and tall form content exceeded the viewport. The explanatory department-scope note fell below the initial view and after the submit button; on short/mobile windows the user had to scroll the whole drawer and could lose the primary action.
- Fix: made the drawer a viewport-height grid with fixed header/search rows and one independently scrollable form row. The submit action sticks to the form viewport bottom. Moved the short department-scope explanation to the top of the form so its purpose is visible before data entry. No create request, route contract or table changed.
- Runtime verification on rebuilt `schedule_web`: at 1280×900, 390×844 and 320×720, the panel fit the viewport and the primary action remained visible; at 320px document width stayed 320px and the drawer had no horizontal overflow. The scope note was visible immediately on each checked viewport. Scrolling the form to its bottom kept the submit control in the same visible position. Closed and reopened the create panel through its visible controls; the route and panel state matched. No form was submitted or record created.
- Evidence: `.playwright-mcp/teacher-create-drawer-mobile-after.png`; browser console errors: zero. `docker compose up -d --build schedule_web` rebuilt the fingerprinted CSS and Rails image. No tests were added. Teacher profile-save, validation-retention and scoped-role acceptance remain open.

## 2026-09-28 — Teacher semester context is compact on mobile

- B06 finding: on the selected-teacher view at 390px, the eight semester links stacked as one column. The context section measured 843px high, pushing the profile and availability areas far below the search.
- Fix: added a scoped class to only the semester-options wrapper and changed it to a two-column grid at phone widths. All semester links remain visible, retain their existing labels/routes/selected state, and have at least 44px hit height. Desktop, week-period choices and table structures are unchanged.
- Runtime verification after rebuilding `schedule_web`: at 390×844, the context section measures 727px (116px shorter), displays all eight semester links in four rows, and keeps the document at 390px wide. At 320×720 the links remain two columns (114px wide, 54px high), the page remains 320px wide, and all eight choices remain present. Opened the `2 семестр · 2029/2030` link, verified the URL and selected state, then restored the original `2 семестр · 2026/2027` route. This was read-only; no profile/constraint data changed.
- Evidence: `.playwright-mcp/teacher-context-semester-grid-mobile.png`. Browser console errors: zero. Root/Rails/API `git diff --check` passed. No tests were added. Teacher profile-save, validation-retention, conflict and scoped-role acceptance remain open.

## 2026-09-28 — Schedule parity and constrained-viewport runtime recheck

- Reopened the running Schedule for semester 1, faculty 1, group СИ-1 after the current Rails rebuild. Read-only inspection confirmed the seven existing headers in order (`Время`, Monday–Saturday), all 30 schedule cells, even-only lessons in the upper parity track, odd-only lessons in the lower track, and common-week cards spanning the cell content width. In each alternating cell, both tracks remained equal height; sampled common cards fit within their cells.
- At a 640×450 CSS viewport, document width stayed 640px while the labelled, focusable timetable region remained 610px wide with 780px scroll content. All seven columns and 30 cells remained in the DOM and accessible; ArrowRight moved only the table region from 0 to 43px scroll. This width/height is a reflow proxy for a reduced CSS viewport, not a true browser-zoom verification.
- Browser console errors: zero. No schedule mutation occurred. Screenshot evidence: `.playwright-mcp/schedule-grid-640x450.png`. True 200% browser zoom remains unverified.

## 2026-09-28 — Public schedule journey and narrow-surface regression check

- B06 public-surface regression after the scoped admin CSS work: at 390px, `/`, `/teacher`, `/group`, `/room`, and the valid group schedule rendered with document/body width equal to the viewport. Followed Group → faculty → course → СИ-1 → ordinary schedule; the application reached `/schedule?date=2026-09-01&group=1`. No data was changed.
- Repeated the width check at 320px for Home, Teacher, Group, Room, and the valid group schedule. All five pages stayed within 320px. The schedule showed its date/mode, subgroup and week controls, six weekday selectors and empty-state content without horizontal document overflow. A direct `/schedule` request without a group/date remains a contextless 404; it is not used as evidence for the valid flow.
- Browser console errors on the final rendered route: zero. Screenshot: `.playwright-mcp/public-schedule-320-audit.png`. The desktop public-route comparison and the full keyboard/print/zoom matrix are still open.

## 2026-09-28 — Teachers availability shows scheduled-slot context

- Finding: the availability grid could show a restriction or neutral state with no indication that a recurring lesson already occupies the same day/time/parity. The separate schedule preview below made that conflict hard to spot while editing.
- Change: the presenter now matches schedule rows by day, time-slot and selected week parity. Matching cells show the compact Russian marker `Занятие уже стоит`, also included in the accessible label. Existing toggle behavior, API contract and table structure are unchanged.
- Runtime verification: Rails image rebuilt and recreated. Authenticated teacher page rendered the new ERB and fingerprinted CSS; the selected weekly view showed 10 markers for 10 recurring lessons across the 30 availability cells. Switching to even and odd views showed 9 and 7 parity-matching markers. At 390px the document stayed 390px wide and the 900px table remained inside its 358px labelled scroll region. The marker uses 8px text; screenshot: `.playwright-mcp/teacher-availability-table.png`.
- Checks: presenter Ruby syntax, locale YAML, Rails Zeitwerk, image asset precompile and `git diff --check` passed. Browser JavaScript errors: zero; Firefox reported the existing transient stylesheet-preload warning. No records were changed and no tests were added.
- Limit: the marker is informational; it does not reject availability changes over an existing recurring lesson. Cross-session conflict and scoped-role paths remain unverified.
- Next action: a Rails rollback path is now available; verify transfer write/read-back only with an explicitly disposable occurrence and remove that exact transfer afterward.

## 2026-09-28 — Undo dated lesson transfers from the two-date view

- Finding: moved-in occurrences showed their source date but had no way to revert the dated override from the transfer workspace, although Hanami already exposed an authorized, transactional `DELETE /admin/event_transfers/:id` operation.
- Change: added a Rails DELETE route, a one-attempt gateway call to the existing API, and a confirmed `Вернуть` action on moved-in lesson cards only. The form retains semester, faculty, group and both displayed dates. API authorization and its occupancy check remain authoritative; a conflict leaves the transfer in place and receives a Russian recovery message.
- Runtime verification: the Rails image rebuilt and recreated; route listing maps `admin_lesson_transfer_revert` to the controller; Ruby syntax, Zeitwerk and diff checks passed. The authenticated two-date view rendered two moved-in cards with source-specific undo labels. At 390px both 356px local schedule regions remained inside a 390px document. Clicking or pressing Enter on an undo button opened the Russian confirmation; declining it retained the card and URL context. Network inspection showed no DELETE or transfer-create request. Browser JavaScript errors: zero; one existing stylesheet-preload warning. Screenshot: `.playwright-mcp/lesson-transfer-revert-action.png`.
- Scope at this checkpoint: this verified the undo affordance and cancel path only. A later entry records the reversible create/read-back/undo/read-back journey and fixes the API conflict discovered during it. Batch write/read-back remains open. No tests were added.
- Next action: verify batch transfer save/read-back/undo where two safe occurrences are available; do not reuse or overwrite an existing moved occurrence.

## 2026-09-28 — Transfer undo conflict and single-move round-trip

- Finding: the first live undo request returned 409 and preserved the transfer. In `EventTransferRepo#revert`, the transaction removed the overlay, resolved the source occurrence, then included that same restored event/date in its own destination-conflict check.
- Fix: pass only the event/date being restored through the conflict helper's existing `ignored` argument. Other occurrences still participate in group, teacher, room and reservation conflict checks; the delete remains transactionally rolled back if a real conflict exists.
- Runtime verification: rebuilt the API; the changed API repository and destroy action passed Ruby syntax checks and the API container returned healthy. The changed Rails controller and gateway had also passed syntax checks during the UI route verification. Through the authenticated Rails view, dragged the unmoved lesson from 2026-09-29 period 4 to empty period 4 on 2026-09-28 and confirmed it. The success notice and moved-in card appeared; after a fresh load the same dated override and source label remained. The new `Вернуть` action initially exposed the 409, then succeeded after the API fix. The success notice confirmed the revert; after another fresh load the lesson was back on 2026-09-29 period 4 with no moved-in copy on 2026-09-28. The two pre-existing moved-in cards remained, and no recurring schedule event was created, edited or deleted.
- Side effects: the normal transfer and revert audit/outbox change events were emitted by the API. The dated override was removed and the resolved schedule returned to its pre-check state. No tests were added. API/Rails/root `git diff --check` passed.
- The direct `/admin/lesson_transfers` route also rendered the expected first-step context chooser after the Rails rebuild; browser errors: zero.
- Next action at this checkpoint: verify the multi-item batch operation; see the following entry.

## 2026-09-28 — Two-item batch transfer round-trip

- Runtime setup: selected 2026-10-02 and 2026-10-03 for the same group. The October 3 table had two untransferred lessons at periods 2 and 5; both corresponding October 2 cells were empty.
- Behavior verified: selected both lessons by checkbox, opened the batch sheet and confirmed the preview mapped each lesson to the opposite date while retaining its period. No conflict was shown and Save was enabled. One batch submission returned `Выбранные занятия перенесены.`; after a fresh load both cards appeared on October 2 in their original periods with October 3 as the source. Selection was cleared.
- Cleanup/read-back: used the new per-card confirmed undo action on each of those two transfers. The first undo left only the second moved card; the second restored the other. After another fresh load, both lessons appeared on October 3 in their original periods with no moved-in copy on October 2, no undo actions and no checked lessons.
- Narrow view: at 390px the page remained 390px wide and both labelled schedule regions measured 356px around their 420px tables; no undo actions remained after cleanup. Browser JavaScript errors: zero.
- Batch-sheet narrow check: restaged the same two lessons without saving, opened the batch sheet at 390×844 and confirmed both opposite-date/period rows fit, no conflict was shown, the sheet stayed within the viewport and Save remained visible. Closed the sheet and cleared both selections; no request was sent.
- Scope: this verifies the two-item batch create → fresh read-back → individual undo → fresh read-back path. The recurring schedule events were not created, edited or deleted. Expected schedule-change audit/outbox events remain as operational history; the temporary transfer overlays are gone. No tests were added.
- Remaining transfer acceptance: occupied-source conflict behavior during undo and scoped-role authorization. Current route is super-admin-only and no scoped-admin fixture is available.

## 2026-09-28 — Occupied transfer destination preserves the editor draft

- Runtime verification: staged the restored October 3 period 2 lesson toward an empty October 2 cell, then selected October 2 period 1, which visibly contained another lesson. Confirming the move returned the Russian occupied-cell alert and reopened the editor with source date October 3, target date October 2 and period 1 still selected.
- After closing the rejected draft and freshly loading both dates, the lesson remained on October 3 period 2, the existing October 2 period 1 lesson remained, and no moved-in card or undo action existed. The browser document stayed 1280px wide; no JavaScript errors or tests were added.
- This verifies destination conflict rejection and safe single-transfer draft recovery, not the separate revert-while-source-is-occupied conflict path.

## 2026-09-28 — Workload creation guidance uses administrator language

- Current runtime inspection showed the creation sheet exposed API and transaction terminology in its helper text. Replaced it with a Russian explanation that each selected group receives a separate workload record and that successful records remain saved if another group fails.
- Runtime verification: rebuilt and recreated only `schedule_web`; the authenticated workload sheet rendered the updated copy. Closing the sheet sent no mutation. Browser JavaScript errors: zero; `git diff --check` passed.
- Safe journey setup remains pending. The current workload creation operation creates a curriculum stream for each selected group; deleting a requirement cascades its assignments and schedule events, while the Rails UI has no matching stream cleanup operation. No workload data was created or removed to avoid leaving an orphan stream or risking existing lessons. B02 workload-to-placement journey remains open.

## 2026-09-28 — Prevent schedule placement from exceeding assigned hours

- Finding: manual schedule creation accepted a common-week lesson even when only one hour remained in a workload requirement whose lesson duration was two hours. The rendered balance could consequently become negative. The same budget rule must apply to edits and recommendation-based placement, while an already-over-budget requirement must still allow a change that does not worsen its balance.
- Change: Hanami now calculates the projected remaining hours under the placement lock for manual create, update and recommendation-created sibling events. A write that would make the balance negative (or worsen an existing deficit) returns the typed hours error before persistence. Rails maps that response to Russian recovery feedback and keeps the edit/create draft. The schedule presenter omits unaffordable common-week choices and defaults a fresh editor to a suitable parity option when possible. Frame submissions suppress the duplicate outer flash so the editor shows one alert.
- Runtime verification: rebuilt the API and Rails containers. In the authenticated schedule, the Object workload had 4/5 hours and one hour remaining. A forced attempt to choose the omitted common-week option returned exactly one `Недостаточно часов в нагрузке для выбранного типа недели.` alert; the selected requirement, Saturday, period 3, week option and teacher selection remained in the editor, and the balance stayed 4/5. Choosing the affordable even-week option created a lesson and brought the balance to exactly 5/5. Opening that exact lesson and attempting to edit it to common week returned the same alert, preserved the event and proposed edit draft, and did not change the balance. The exact temporary event (ID 22) was then removed through its confirmed schedule inspector action; after the refreshed read-back it no longer appeared and the original 4/5 balance was restored.
- Checks: all four changed API Ruby files passed `ruby -c`; the changed Rails presenter, gateway and controllers passed Ruby syntax; Rails `zeitwerk:check` passed; root/Rails/API `git diff --check` passed. Browser JavaScript errors: zero. No tests were added.
- Limit: the live check covered manual create and edit budget enforcement. Recommendation-path enforcement was source-reviewed and syntax-checked but not exercised with a disposable recommendation fixture. No schedule records remain from the runtime check.
- Next action: continue the workbench acceptance journey from B02 and verify recommendation placement when a safe disposable workload fixture and cleanup path are available.

## 2026-09-28 — Default split workloads to a valid subgroup

- Finding: a manually selected workload with `SEPARATE` split strategy rendered `Вся группа` as the default subgroup. Hanami correctly returned 422 because a separate workload only accepts subgroup 1 or 2, but Rails showed a generic create failure.
- Change: the Schedule presenter omits the whole-group choice for separate workloads and resolves a valid draft/default subgroup; a fresh placement defaults to subgroup 1. The gateway recognizes the subgroup-strategy response and Rails displays a specific Russian correction message if it occurs again.
- Runtime verification: after rebuilding/recreating Rails, selected the existing disposable-safe workload with one hour remaining and an empty Tuesday period 3 slot. The first render exposed a nil-initialization bug in the new presenter branch and returned 500; initialized the empty option set explicitly, rebuilt, and reloaded successfully. The editor then rendered only Подгруппа 1 and Подгруппа 2 with subgroup 1 selected and the affordable even-week option selected. Creation succeeded; the event appeared as even week, subgroup 1, and the workload balance became 3/3. After a fresh load, edited that same event ID from even to odd week; the success notice appeared, the ID stayed unchanged, the card read back as odd week/subgroup 1, and the balance stayed 3/3. Deleted only that temporary event using the confirmed inspector action. The post-delete page read-back showed no temporary card and restored the original 2/3 balance.
- Checks: changed Rails Ruby syntax, `rails zeitwerk:check`, and `git diff --check` passed. No tests were added.
- Limit: the separate-workload placement → recurring edit → fresh read-back path is verified. Multi-item recommendation placement and workload creation with cleanup remain pending; this is not the full B02 journey.
- Next action: continue the remaining B02 assignment/recommendation acceptance, then return to B03 in plan order.

## 2026-09-28 — Keep selected assignments visible while searching

- Finding: filtering the teacher or room list to a no-match query hid already-selected checkboxes. Although the selections remained checked in the form, their absence from view could make them appear removed.
- Change: selected options remain visible while filtering; the Russian live status reports both matching and selected counts and updates on checkbox changes.
- Runtime verification: rebuilt Rails assets, opened the authenticated assignment editor for requirement 10, searched for no-match teacher and room terms, and confirmed each status showed `Совпадений: 0 · выбрано: 1` while the selected option remained visible and checked. Cleared both filters, closed without saving, reopened after a fresh navigation and confirmed the original teacher and room were still selected. Browser console errors: zero. JavaScript syntax and `git diff --check` passed; no data was changed.
- B02 status clarification: this focused assignment-search check supplements, but does not replace, the disposable end-to-end journey recorded on 2026-09-21. Multi-item recommendation and remaining failure/conflict paths are still open; no fixture was created for this read-only check.

## 2026-09-28 — Current-runtime Schedule and two-date transfer staging

- Batch/slice: B02b workload-to-slot staging and B04 dated-transfer editor; focused non-mutating acceptance.
- Runtime verification: on the authenticated current Rails build, dragged the existing one-hour workload item into an empty Tuesday period-3 cell. The Schedule editor retained that load, destination, teacher, room, parity and subgroup. Closed without saving, reopened the same editor through the cell’s click/tap link, confirmed the same destination and assignment inputs, and closed without saving. No workload or event data changed.
- Transfer verification: the authenticated two-date workspace rendered both selected dates and their schedule tables. Dragging the existing October 2 first-period occurrence into the empty October 3 first-period cell opened the explicit transfer confirmation with the correct source date, destination date and period; closed without saving. At 390×844, the document/body remained 390px wide and both labelled, keyboard-scrollable schedule regions measured 356px with 420px table content. Browser console errors: zero.
- Limit: this confirms editor staging and responsive containment, not the save/read-back mutation (already evidenced separately in the two-date transfer package). Cross-group conflicts and scoped-role denial remain open. No new tests were added.

## 2026-09-28 — Compact mobile Resources navigation

- Batch/slice: B03 shared reference-area navigation, mobile layout.
- Finding: at 390px the four area links and the active area’s destinations wrapped into several tall rows. A first horizontal-strip revision clipped category labels in the viewport without an obvious scrollbar; it was replaced before acceptance with a two-column, fully labelled area grid and compact wrapping destination tabs.
- Change: under the existing 680px breakpoint only, all four reference areas remain visible in a 2×2 grid, while the active area’s links wrap as readable single-line tabs. Desktop rules and resource rows are untouched.
- Runtime verification: rebuilt/recreated `schedule_web`. On `/admin/posts`, checked 390px and 320px: document/body width matched the viewport, all area and destination links fit without horizontal clipping, and the current section remained marked active. At 320px, opened `Помещения` and verified the page changed to `Типы зданий` with both the area and destination marked active. At 1280px, the four-column desktop area navigation and existing resource row/header structure remained intact. Browser console errors: zero.
- Existing editor behavior: at 390px, opened `Добавить должность` and confirmed its labelled create form appeared in the separate bottom sheet; closed it without submitting. No resource records changed.
- Evidence: `.playwright-mcp/resources-posts-mobile-320-after.png`.
- Limit: this is a navigation/layout slice; Resources create/edit/delete and server-failure read-back remain open as recorded for B03. No data changed and no tests were added.

## 2026-09-29 — Scheduling prototype and published timetable analyzer

- New design and isolated data: `docs/architecture/scheduler-design-draft-2026-09-28.md` describes private generation runs, administrator conflict review, static analysis and final publication. `scheduler-synthetic-scenario-2026-09-29.json` is an isolated scenario and was not inserted into the shared database.
- Executable prototype: `apps/scheduler/` contains a pinned OR-Tools CP-SAT baseline, a conservative Russian preference compiler and a static analyzer. The sample produced four placements with no hard findings; an approved consecutive-lesson preference put two laboratory lessons in adjacent slots. The compiler flagged text that contradicted a profile constraint and deferred room-software matching.
- Live application: Hanami `GET /admin/schedule/analysis` analyzes recurring schedule rows across the semester, reports teacher/group/room clashes and explicit teacher unavailability, and returns coverage flags. The Rails Schedule workspace displays the report and marks affected lesson cards. It is read-only.
- Runtime evidence: rebuilt `api_geteway` and `schedule_web`, signed in through the current application, selected semester 1 (2026/2027), Construction Faculty and its available group, then ran the analyzer. The page reported three teacher-unavailability findings among eleven recurring events; all three corresponding lesson cards received an error marker. The browser reported no console errors. Screenshot: `docs/architecture/evidence/schedule-analysis-2026-09-29.png`.
- Limits: the local solver still consumes its standalone JSON snapshot; no private run storage, live workload adapter or publish operation is connected. The live analyzer does not yet cover dated exceptions, reservations or room capacity, and the UI states those limits. No schedule records were changed and no new tests or test files were added.

## 2026-09-29 — Isolated solver service container

- Change: added `apps/scheduler/server.py`, a small HTTP adapter over the pinned CLI solver, analyzer and preference compiler. The Python image pins both the Python base-image digest and OR-Tools version. Docker Compose gives the service no host-published port or database credentials, attaches it to an internal network shared with Hanami, and caps it at one CPU and 2 GiB.
- Boundaries: requests use schema version 1, are limited to 8 MiB, omit snapshots from logs, and only one CP-SAT request can run at once. The service has no durable state; Hanami still needs to own run authorization, input snapshots, progress and proposals before live generation.
- Verification: `docker compose config` accepts the scheduler service; the image built successfully. The API container reached `/health` over the internal network. A synthetic snapshot sent to `/v1/solve` returned `optimal` with four placements and two findings. The container was stopped after verification. `python3 -m py_compile apps/scheduler/*.py` passed. No live schedule rows changed; no tests or test files were added.
- Remaining: create durable Hanami-owned generation runs, implement a project-faithful snapshot builder (including workload hours, streams, parity, periods, transfers and reservations), relay runs to this service with recoverable progress, then build the private diff/review and atomic publication path. Do not add a public Generate action until those paths are complete.

## 2026-09-29 — Durable private generation, teacher wishes and bulk publication

- Change: Hanami now builds faculty/university snapshots from live workload and scheduling records, stores private generation runs, and uses a bounded worker to call the local CP-SAT service. Rails provides the Schedule sandbox, run progress/status and proposal review. Teacher wish submission uses a conservative Russian-to-typed-JSON compiler; profile availability remains a hard constraint, while only administrator-approved supported wishes guide scoring.
- Publication: administrators select lesson rows for a batch. Each request checks selected proposal keys, run revision and source digest, runs final analysis, then creates lessons through existing placement validation and Outbox writes. Unselected rows stay private; successful publication advances the run revision and rebases its snapshot/digest. The run becomes `published` only after the final proposal row is consumed. Existing lessons are never replaced.
- Editing: each row has a private editor for weekday, period and its assigned room choices. Saving checks source freshness and revision, then reruns the analyzer. Rows with errors remain red and cannot be published; admins can adjust the edited row and recheck it. Week parity, subgroup and dated edits are out of scope until their workload semantics are specified.
- Verification: a live faculty snapshot generated five placements and appeared in the sandbox while the ordinary schedule stayed unchanged. Browser editing moved one row from Wednesday period 2 to Monday period 5, reanalysis returned no findings, and a second browser edit restored the original day/period. A conflicting Tuesday period 1 edit showed three findings, rendered the row in conflict state without an approval checkbox, and was resolved by restoring its original time. The run remains at revision 9 with all five proposals, original placement, zero findings, and the schedule at 11 events. API rollback checks also covered successive two-batch publication and publishing all five rows.
- Checks: API and Rails images rebuilt; Rails `zeitwerk:check`, changed-file Ruby syntax, API publication/edit operation result shapes, JavaScript syntax and Rails asset precompile passed. The editor and selectable-room controls rendered in the authenticated browser with no console errors. No tests or test files were added. The host lacks the repository-pinned Ruby versions/gems, so checks ran in the project containers.
- Remaining at this checkpoint: week parity/subgroup editing, live CP-SAT incumbent reporting, and the broader admin acceptance backlog. No generated placement from the verified run is published.

## 2026-09-29 — Sandbox week-parity editing

- Change: added the generated lesson unit's ordinal to solver output so the editor can resolve its exact remaining-hours unit. The run endpoint now supplies allowed week-parity choices per proposal row. The Rails editor sends the selected parity through the existing API contract; Hanami checks it against that unit's allowed parity set, preserves run revision/source checks, and reruns the full analyzer before updating the private proposal.
- Safety: a full-week lesson exposes only `both`; an alternating half-week lesson exposes `even`/`odd`. Tampered values outside the lesson unit's hours model are rejected. The sandbox remains isolated from ordinary schedule events.
- Runtime verification: in the authenticated browser, changed proposal `generated-10-1` from odd to even. Reanalysis marked both colliding rows as conflicts and removed their publication checkboxes. Restored odd; the run read back with “Нечётная”, the analyzer reported no conflicts, and the proposal remained private. The run advanced from revision 9 to 11; no publication request was made. The full page had no browser console errors.
- Additional checks: rebuilt the scheduler, API and Rails images; synthetic `/v1/solve` returned four placements with positive `lesson_unit_ordinal` values; Hanami route loading, changed Ruby syntax and Rails eager loading passed. No tests or test files were added.
- Remaining: subgroup/stream edits, more detailed live CP-SAT progress, and broader admin acceptance work. Parity changes are limited to each unit's generated remaining-hours model.

## 2026-09-29 — Durable CP-SAT search progress

- Change: the solver emits coalesced incumbent metrics. An internal callback endpoint checks that the run is still solving under its current lease and persists numeric progress plus the monotonic event sequence. The Schedule page shows feasible-solution count, placed units, search branches/conflicts, elapsed time, objective and bound while the run is active and after it finishes.
- Security: each solve receives a per-run random callback capability; only its SHA-256 digest is persisted, and it is cleared on completion or retry. The API exposes no database access to the scheduler. An invalid/inactive capability returned 404.
- Runtime verification: rebuilt worker/API/Rails images, applied the additive digest-column migration, then restarted API and worker so Hanami reloaded database relations. A fresh private faculty run read back `event_sequence: 7`, status `proposed`, seven feasible solutions, 944 branches, eight CP-SAT conflicts and objective/bound 6.0. The authenticated Schedule page displayed the same metrics, five private proposal rows and the unchanged-published-schedule notice. No publication was made; browser errors: zero.
- Remaining: expose presolve/search activity before the first feasible incumbent; current live numeric updates are emitted on incumbent callbacks, with the initial phase checkpoint visible before then. No tests or test files were added.

## 2026-09-29 — CP-SAT presolve progress

- Change: the isolated solver now reports the CP-SAT `Starting presolve` and `Starting search` lifecycle markers through the existing progress callback. Hanami accepts the additional `presolving` phase, and the Schedule sandbox labels it in Russian as constraint analysis/model simplification. Progress heartbeats continue to advance elapsed time while a phase is running.
- Privacy: the callback converts only two fixed solver log prefixes into phase names. CP-SAT's detailed log is disabled on stdout; no model, solver log lines, or identifiers are sent to the admin UI.
- Verification: the isolated synthetic scenario returned `optimal` with four placements and the phase sequence `preparing → presolving → searching → validating → complete`. Repeating the smoke check after disabling stdout logging produced only the result summary. Scheduler, API and Rails images were rebuilt; Python compilation, changed Ruby syntax, Rails eager loading, JavaScript syntax, scoped whitespace checks and authenticated browser asset/console checks passed. No published lesson was changed and no tests or test files were added.
- Limit: the synthetic run finishes too quickly to observe an intermediate `presolving` update in the browser. The authenticated page loads the rebuilt progress controller and has no console errors, but a deliberately long live run is still needed to verify the transient phase label and heartbeat end to end.

## 2026-09-29 — Room reservations in manual placement

- Finding: the snapshot solver and published-schedule analyzer already account for dated room reservations, but manual placement recommendations, create and edit only checked existing schedule events. Those paths could offer or save a room/date that the generator would reject.
- Change: `Rooms` now produces a bounded set of room/weekday/slot/week-type tuples from active reservations within the selected group-semester ranges. It applies special-period replacement through the shared week-parity helper and fetches only the fields needed. Recommendation search consumes this set without a per-candidate query; API create, edit and recommendation acceptance recheck the reservation alongside occupied-room checks.
- Verification: a database transaction inserted one temporary active reservation and rolled back. The matching recurring parity was blocked, the opposite parity remained available, and the exact reserved date was blocked. The live placement recommender loaded the updated context and returned 60 candidates for the remaining-hours scenario. API stayed healthy; no reservation or lesson persisted; no tests or test files were added.
- Limit: recurring reservation checks require a configured semester date range for the affected group-semester, matching the snapshot builder's current coverage boundary.

## 2026-09-29 — University-scope generation browser smoke

- Verification: from the authenticated Schedule workspace, started `Составить для университета`. The run returned as `Готово к проверке`, showed the whole-university scope and five private proposal rows, and the page stated that the published timetable was unchanged. The ordinary grid still rendered eleven published lesson cards; browser console errors: zero.
- No proposal was selected or published. This small local dataset solved too quickly to show the transient presolve phase in the browser; the synthetic solver phase check remains the evidence for that transition.

## 2026-09-29 — Reservation snapshot parity in special periods

- Finding: room reservations in the solver snapshot were encoded as ordinary even/odd weeks for every date, while manual placement already applies special-period replacement. That could report false reservation collisions during lecture, credit or exam periods.
- Change: snapshot reservation rows now resolve each selected group-semester's special period for the reserved date and encode its week type with the shared `WeekParity` rules. Dates outside special periods retain ordinary parity. Invalid/missing special-period date bounds are ignored safely.
- Verification: rebuilt and recreated the Hanami API and generation worker; both containers returned healthy. The authenticated browser completed another whole-university private generation against the rebuilt API with five proposal rows and eight feasible variants. The run remains unpublished; the public grid remains unchanged. Ruby syntax and scoped whitespace checks passed; no tests or test files were added.

## 2026-09-29 — Preserve proposal lesson-unit identity after partial publication

- Finding: publishing selected rows rebuilds remaining workload units, which may renumber their ordinals. Remaining private proposal rows previously retained the old ordinals, so later week-parity edits could validate against the wrong unit.
- Change: within the publication transaction, remaining rows are rebound to unused units in the fresh snapshot with the same linked requirements, subgroup and supported week type before the run snapshot and proposal are advanced. If the fresh snapshot cannot represent every remaining row, the existing transaction aborts before any event or run update commits. Proposal keys remain stable for the administrator's selection state.
- Verification: API and generation worker rebuilt and returned healthy; Hanami loaded the changed operation. A live, in-memory operation check rebased two shared-stream rows from stale ordinals 7/8 to current ordinals 1/2 while preserving subgroups and even/odd choices. Ruby syntax and scoped whitespace checks passed. No published lesson was changed and no tests or test files were added.

## 2026-09-29 — Search progress stress check and conflict locations

- Solver verification: ran an isolated 144-requirement scenario (288 lesson units) through the pinned scheduler with an eight-second search limit. It returned `feasible` with 288 placements and nine progress updates: preparation, presolve, search updates, validation and completion. The scenario ran only in memory in the scheduler container; no database or timetable rows were touched.
- Analyzer UI: current authenticated Schedule runtime reported four profile-unavailability errors and marked the three visible recurring cells red. The issue list previously omitted weekday/time for recurring rows, leaving same-subject links hard to distinguish. It now includes the Russian weekday and the lesson's `HH:MM`; dated occurrences keep their date and show the time. The rebuilt Rails page rendered all four findings and three red cells with no browser console errors.
- Limit: the live database solve still completes too quickly to observe its transient progress labels in the browser. The larger isolated solve confirms repeated engine callbacks; durable progress storage and the browser poller are in place, but a long-running authenticated end-to-end run remains unobserved. No tests or test files were added.

## 2026-09-29 — Date-aware navigation for moved conflict occurrences

- Finding: analyzer findings for a transferred occurrence pointed to the recurring event editor. The user could land on the template instead of the date-specific move responsible for the conflict.
- Change: dated analyzer lesson context now includes occurrence state and original date. For super-administrators, findings about moved-in occurrences link to the existing two-date transfer workspace with the original and destination dates and affected group selected. Recurring findings keep their Schedule-cell editor link; other roles retain the prior route rather than receiving a link to the super-admin-only transfer page.
- Runtime verification: rebuilt Hanami and Rails. The current analyzer rendered four findings and three red recurring cells. Following a moved-occurrence finding opened `/admin/transfers` with the source date 2026-09-29 and destination date 2026-09-28, showing the affected transferred `Автомобили` lesson on the destination date. Browser console errors: zero. The page was only inspected; no transfer was saved.

## 2026-09-29 — Clarify generation scope before queueing

- Change: the Schedule workspace now says that existing lessons stay fixed, the private draft proposes placements for remaining workload only, and the published timetable changes only after selected rows are published.
- Verification: rebuilt Rails and checked the authenticated Schedule page. The full Russian scope notice rendered and the browser reported no console errors; no generation or schedule mutation was started.

## 2026-09-29 — Empty incremental draft state

- Finding: a generation run can validly finish with zero remaining lesson units when all workload is already scheduled, but the proposal panel offered no explanation for the empty result.
- Change: an empty, unpublished proposal now says there are no new placements to publish and that existing lessons were left unchanged. Runs with published batches keep their existing published-count message.
- Verification: rebuilt Rails and rendered an existing five-row private university proposal to confirm the proposal panel still behaves normally and compiles without errors. The zero-row copy is a direct state branch; no currently scoped fixture has zero remaining workload. No lessons were published or changed; no tests or test files were added.

## 2026-09-29 — Keep a newly generated sandbox visible

- Batch/slice: B02 schedule generation start, proposal review, and conflict correction.
- Finding: starting a generation run submitted from the nested `schedule-workspace` Turbo frame created and completed the run, but the browser returned to the prior context URL and hid the run panel. Opening the returned `generation_run_id` directly showed the valid proposal, so this was a navigation/handoff defect rather than a solver failure.
- Change: the generation form now targets the top-level page. The redirect retains the run ID and the completed proposal remains visible after the progress poll reloads.
- Runtime verification: rebuilt `schedule_web` (Compose also rebuilt its API dependency). Authenticated on the live 2026/2027 semester and started a faculty-scoped private run. It reached `proposed`, showed solver progress (8 feasible incumbents; 1,712 branches; 25 conflicts), and rendered five placements. Staged one correction for existing event 19 to Wednesday period 4; the run then rendered six placements and the finding list dropped the resolved teacher-availability issue. The published event remained Monday period 1 after the staging operation. Static analysis marked the published conflict cells with `is-conflict`; computed outline was `3px solid rgb(180, 57, 47)` and error findings had the same red border. Proposal selection remained disabled while unresolved errors remained. No publication request was sent and no published timetable row was changed.
- Evidence: browser snapshots `.playwright-mcp/page-2026-09-29T10-31-50-854Z.yml` (completed private run), `.playwright-mcp/page-2026-09-29T10-34-21-948Z.yml` (static analyzer plus private run), and `.playwright-mcp/page-2026-09-29T10-35-55-578Z.yml` / `.playwright-mcp/page-2026-09-29T10-36-07-619Z.yml` (queued then completed university-scoped run). Browser console showed zero errors. API and Rails containers healthy after rebuild.
- Source/runtime identity: `schedule_web` HEAD `16ec036972ba6b05e7fa1a72135d3f80eb1d94c2`, dirty scope limited for this slice to `app/views/admin/schedules/show/show.html.erb`; workspace and `/app/app/views/admin/schedules/show/show.html.erb` SHA-256 both `9b74216b4e5551b99f1ee91eeedc6278ba73576d3553cc24206aa856455f3657`. Root documentation HEAD: `0397d44576cc6694f667ee04a84529128ce6c979`. Existing proposal and weekly timetable tables retain their prior ordered headers and five-by-six schedule grid; no table schema changed.
- Scope verification: also started a university-scoped private run, observed it move from queued to proposed, and confirmed the run panel says “весь университет” with five placements. The observed synthetic workspace is limited to the currently selected СИ-1 group, so this proves the university-scope request/worker/UI path but does not establish multi-faculty load at scale.
- Limit: publishing was not exercised. Two private test runs remain proposed for review; the faculty run includes the staged correction. No published schedule mutation occurred. No tests or test files were added.

## 2026-09-29 — Reject stale edits across schedule tabs

- Batch/slice: B02 sandbox concurrency and dirty-draft recovery.
- Runtime verification: opened the same university-scoped proposed run in two authenticated browser tabs at revision 1. Tab A staged the generated lesson for Thursday period 4; the page read back revision 2 and retained that placement. Tab B submitted its stale revision 1 draft for Friday period 5. The API rejected it with `Черновик изменился или устарел. Обновите страницу и проверьте данные снова.`; after redirect, the latest run remained at revision 2 and Tab B's Friday/period-5 input was still present. The published Physics lesson remained in its original Monday period-1 cell.
- Isolation/evidence: changes were confined to the private proposal in the university run, and no publication form was submitted. Browser snapshot `.playwright-mcp/page-2026-09-29T10-44-25-838Z.yml` captures the stale-edit conflict. The active-tab network record showed the proposal edit request returning 303; no publish action was invoked. Browser console errors: zero.
- Table/runtime scope: the proposal and weekly timetable structures and ordered headers were unchanged. The live synthetic workspace is still limited to group СИ-1, so this does not verify cross-faculty concurrency or scale.
- Limit: this used two tabs for the same requester, not two distinct administrator identities. Owner isolation was source-reviewed in the API authorization path; cross-account denial was not exercised against a second live account. No tests or test files were added.

## 2026-09-29 — Verify non-owner draft access denial

- Batch/slice: B02 private-run authorization.
- Runtime verification: loaded the running Hanami authorization service and checked the existing university-scoped proposal using in-memory `faculty_admin`, `kafedra_admin` and `scheduler` accounts with non-owner UUIDs. The real authorization resolver denied both `read` and `update` for each role. This exercises the shared API boundary used by run status/progress and edit/publication actions without creating accounts or changing the run.
- Evidence: command output was exactly `faculty_admin/read:denied`, `faculty_admin/update:denied`, `kafedra_admin/read:denied`, `kafedra_admin/update:denied`, `scheduler/read:denied`, and `scheduler/update:denied`; the probe queried run `b5a73573-9414-4910-abad-2710da80d5dc`. No HTTP publication route was called and no schedule row changed. No tests or test files were added.
- Limit: super-administrator oversight remains intentionally permitted by the existing top-level authorization rule. This check used the real app-loaded authorizer/resolver but did not make a request through Rails with a second logged-in browser identity.

## Open product-fit finding — Whole-scope timetable entry

- Current runtime/source evidence: Aggregate Schedule shows all occurrences for one selected date at faculty or department scope, but offers no generation action. The Schedule workspace now exposes the faculty/university sandbox as soon as a semester is selected. Faculty generation is enabled when a faculty is selected; university generation works without choosing a faculty or focus group. A focus group remains required only to show the existing group-specific weekly calendar and lesson editor.
- Browser verification (2026-09-29): started run `3ada86db-6c0f-47f5-b9d6-b680e26e9d3f` from `/admin/schedule?semester_id=1`, with no faculty or group selected. It reached `proposed`; the page showed “весь университет”, five proposal rows, the existing nine ordered proposal columns, and the message that the published timetable was unchanged. The initial six errors were findings on existing recurring/date-specific timetable entries, not on the five generated rows. The run remains private and unpublished.
- Change: `ScheduleWorkspace#generation_ready?` now distinguishes semester-level generation readiness from `selection_ready?` for the group-specific weekly grid. The analyzer link is shown only for a selected faculty, with explanatory Russian copy at university scope. Existing timetable tables, axes and proposal columns were preserved.
- Verification: rebuilt `schedule_web` and its API dependency; Rails syntax and Zeitwerk checks passed, both services were healthy, and authenticated browser console errors were zero. No tests or test files were added. Run remains private and unpublished.
- Product decision (user, 2026-09-29): recurring university/faculty schedules use one existing weekly table per student group, not a combined cross-group matrix. Every in-course group-semester attached to the selected semester is represented, including groups with no scheduled lesson.
- Verification status: the 2026-09-29 live seed has one student group and one selectable faculty. Disposable no-event group fixtures were used to verify additional groups in both faculty and university views, including a second faculty; the second faculty appeared in the university scope, was absent from faculty 1, and appeared alone in faculty 2. All fixtures were removed and read back absent; details are recorded below.

## 2026-09-29 — Exclude past date exceptions from forward generation conflicts

- Finding: the Schedule sandbox includes past moved occurrences in its date-expanded snapshot, even though those occurrences cannot be edited through the forward proposal flow. A September 28 occurrence therefore kept a September 29 proposal blocked after its actionable conflicts had been corrected.
- Change: `BuildGenerationSnapshot#build_date_occurrences` now limits date-expanded exceptions to dates on or after the API host's current date, matching the existing forward-only handling for moved and weekday-transfer blockers. Recurring lesson templates remain checked against profile availability for the whole selected schedule; the separate published-schedule analyzer is unchanged.
- Runtime verification: rebuilt API and generation-worker images; API healthy, worker running, Ruby syntax and Hanami route loading passed. Started fresh university run `b3d143fa-8f5e-4e81-87b5-bb2f18224203` from the semester-only Schedule page. It proposed five generated placements and surfaced the actionable recurring and current-date findings. Staged three recurring lesson corrections plus one current-date room correction in that private sandbox. Findings fell to zero; all nine proposal rows (five generated placements and four staged corrections) became selectable. Selected one generated row in the browser and verified the publish control enabled; no publish request was submitted.
- Isolation/read-back: the run remains `proposed`, revision 5, with nine proposal rows, zero findings and no `published_at`. Direct read-back confirmed published schedule events 5, 8, 11 and 19 remain at their original day/slot/room values and event transfers 5 and 6 retain their original dates/room/slot. No published schedule mutation occurred. Browser console errors: zero.
- Local wish-compiler smoke: “Хочу 2 пары подряд по лабораторной, потому что печка включена” compiled to a proposed soft `consecutive_lessons` rule scoped to the single matching lab requirement. A requested Monday period 1 preference conflicting with the teacher profile returned `PROFILE_TEXT_CONTRADICTION` and no rule. A request for installed Compass 3D software in a room returned `UNSUPPORTED_ROOM_CAPABILITY` for administrator review and no active rule.
- Multi-faculty solver smoke: the database has two faculty rows, but the second is only the “Unknown” placeholder and there is one real student group. To exercise cross-faculty resource constraints without adding persistent fixture rows, ran a two-group in-memory scenario through the pinned scheduler. It scheduled both groups with a shared teacher and room at distinct periods, honored a hard Tuesday-period-1 profile block, and produced no findings. Deliberately colliding the two placements produced both `TEACHER_CLASH` and `ROOM_CLASH` in static analysis.
- API snapshot-builder smoke: inside a database transaction, inserted a temporary second faculty, department, speciality, group-semester, one workload, shared teacher assignment and room reference. The real faculty-scoped snapshot contained only the temporary group; the university snapshot contained both the original and temporary groups. Both snapshots were sent to the isolated `/v1/solve` service, and both solver runs placed the temporary faculty workload with no analyzer finding attached to that row. Baseline university findings remained limited to the original seed's teacher-availability and missing-room issues. The transaction rolled back; read-back found zero synthetic faculty/speciality rows, and the existing published lesson/transfer rows remain unchanged. No durable generation run was created.
- Scope: both faculty and university database snapshot/solver paths are verified transactionally. A persistent multi-faculty browser journey, role matrix across both faculties and scale/load remain unverified. No tests or test files were added.

## 2026-09-29 — Room capacity lookup and rollback-only publication path

- Finding: a rollback-only end-to-end publication probe found that CP-SAT emitted a valid faculty placement, but `CreateScheduleEventForStream` rejected it while checking room capacity. The live ROM relation returns room rows as hashes, while `Rooms#capacities_for` assumed entity methods (`room.id`, `room.capacity`), raising `NoMethodError` before the write.
- Change: `capacities_for` now reads either entity accessors or symbol/string hash keys. Existing unknown capacity remains `nil`, so solver and write validation keep the same conservative unknown-capacity behavior.
- Runtime verification: rebuilt API and generation worker; API healthy. The live room relation returned `{1 => nil}` through the changed lookup. In a transaction, created temporary faculty/workload data, built a faculty snapshot, solved it, created a proposed run and called the real `PublishScheduleGeneration` operation. The operation created one schedule event and advanced the run to `published` inside the transaction. An explicit outer rollback then removed all fixture, run and event writes. Synthetic faculty/speciality read-back returned zero; the existing private university run stayed `proposed` and published lesson rows remain unchanged.
- Boundaries: the operation was invoked directly inside the Hanami app container, so this verifies business-operation validation and transactional writes, not HTTP publication authorization or the browser confirmation action. No tests or test files were added.

## 2026-09-29 — Reject partial publish while selected rows leave conflicts

- Browser/API verification: in the authenticated Schedule page, selected one generated row from private university run `b3d143fa-8f5e-4e81-87b5-bb2f18224203`, leaving the three recurring corrections and one dated correction unselected, then submitted the real publish form. The Rails-to-API request was rejected with the Russian conflict/stale-draft message; the page retained all nine private proposal rows and no browser console errors occurred.
- Read-back: the run remained `proposed` at revision 5 with its nine-row proposal, zero stored findings and no `published_at`. The publish operation reanalyzed only the selected subset against the still-published timetable and rejected it before writing because unresolved baseline conflicts remained. Published events 5, 8, 11 and 19 remained at their original day/slot/room values. No schedule write or publication occurred; browser checkbox selection cleared after redirect.
- Scope: this verifies the authenticated HTTP rejection path and final conflict gate. The successful write path was verified separately inside an explicit database rollback in the preceding section. No tests or test files were added.

## 2026-09-29 — Trace teacher-wish submission and administrator review boundary

- Browser check: the authenticated administrator opened the semester's teacher-wishes panel; it correctly reported that no wishes had been submitted. No wish was created or changed.
- Contract trace: teachers submit ordinary text through their own Teacher Workspace form. Rails sends it to `/admin/me/schedule_wishes`; the API `CompileTeacherWish` invokes the pinned local scheduler compiler and persists typed proposals/findings for administrator review. Only approved preferences are included in generation snapshots. The admin Schedule page is the review surface, not a second teacher-submission form.
- Verification boundary: the teacher portal submission path was confirmed from the current Rails view/controller/gateway and API operation source. A browser submission still needs an authenticated teacher account; the current browser session is the super-administrator. The existing compiler example smoke and profile-conflict precedence checks are recorded in the September 29 generation section above. No test wish or published schedule change was made.

## 2026-09-29 — Add university scope to date-resolved Aggregate Schedule

- Change: Aggregate Schedule now offers University, Faculty and Department scopes. The new `/admin/schedule/occurrences` API path uses the existing occurrence engine, active group-semester windows and the unchanged aggregate table columns. Both the University tab and API read are limited to super-administrator and scheduler roles; existing faculty/department endpoints and the semester-grid contract remain unchanged.
- Runtime verification: rebuilt/restarted API and Rails, confirmed Hanami route loading, Ruby syntax and Rails Zeitwerk checks. In the authenticated browser the university report for 2026-09-29 rendered two rows in the existing seven-column table with no alert or console errors. Switching to Faculty and Department scopes rendered the same two rows. A request without authentication returned 401.
- Initial live request found a missing repository helper; the helper was added and the rebuilt endpoint then rendered successfully. No timetable or private generation data was changed. The seed still has only one real group, so this does not verify multi-faculty rendering or load.

## 2026-09-29 — Verify teacher wish submission, review, and solver inclusion

- Browser journey: created a disposable teacher account for the existing lab instructor, signed in through an isolated browser origin, and submitted ordinary Russian text from Teacher Workspace. The local compiler proposed one soft `consecutive_lessons` rule for the matching laboratory requirement. The teacher page showed the submitted text and typed proposal; no password value was captured or documented.
- Findings and fixes: the administrator wishes endpoint failed because the ROM teachers relation returns hashes while its presenter assumed entity accessors; it now reads either form. The review UI then exposed revision `0` being rejected by Rails' positive-integer parser; the controller now accepts nonnegative revisions. Building a generation snapshot with approved wishes exposed a Rails-only `deep_stringify_keys` call in Hanami; it now uses a local recursive JSON-key normalizer.
- Verification: the authenticated admin list returned the wish; after the revision fix, an actual browser approval returned API `PATCH 200` and showed `Одобрено`. A real faculty `BuildGenerationSnapshot` then contained two approved `consecutive_lessons` preferences, demonstrating that approved text reaches solver input. Rails syntax/Zeitwerk and API Ruby syntax passed; no test files were added.
- Cleanup and boundaries: both synthetic wishes and the disposable teacher account were removed; database read-back returned zero matching accounts and wishes, and the teacher browser session was signed out. No published schedule or generation run was changed. The seed still has one real group, so this verifies the wish path for one teacher, not multi-faculty scale.

## 2026-09-29 — Pin local solver dependencies and preserve teacher identity in analysis

- Finding: the Python image and OR-Tools were pinned, but its transitive packages floated during rebuilds. A live synthetic solve also exposed an analyzer identity mismatch: generated rows carry teacher display names, while profile rules and approved wishes are keyed by teacher identity. This falsely reported a fulfilled consecutive wish as unmet and failed to flag generated rows edited into a hard-unavailable period.
- Change: `apps/scheduler/requirements.txt` now pins the complete dependency set observed in the healthy local solver image. The analyzer resolves generated proposal teacher identities from linked workload requirements (or explicit internal `teacher_ids`) rather than display labels.
- Runtime verification: rebuilt/recreated the internal scheduler. `pip check`, Python AST parsing, `/health` (HTTP 200) and a solve through `/v1/solve` passed. The isolated scenario returned `optimal` with four placements and zero error-severity findings; its two laboratory lessons were adjacent and no false unmet-wish finding was reported. Sending those placements through `/v1/analyze` after moving both into Monday periods 1–2 produced two `TEACHER_UNAVAILABLE` findings.
- Boundaries: the six other scenario findings are review-only wish/compiler notices. The check used isolated synthetic JSON; it did not modify any schedule rows or private generation run, and no tests or test files were added.

## 2026-09-29 — Add semester-wide recurring schedule inspection

- Change: Aggregate Schedule now has a read-only recurring weekly-grid view for University, Faculty, and Department scopes. It groups the existing API schedule rows by student group, uses the configured period and week-parity catalogs, and marks recurring analyzer errors on the affected cells and lessons. Date-resolved transfers and special periods remain in the separate existing date view; its seven ordered columns are unchanged.
- Verification: the running Docker Rails and Hanami services are healthy; Rails syntax and Zeitwerk checks passed. The authenticated browser journey previously rendered University, Faculty, and Department week views, found three red-highlighted recurring unavailability conflicts, and showed the unchanged date view with its original seven columns. At a 390px viewport, only the explicitly labelled timetable region scrolled horizontally; the page itself did not overflow. Search filtered group sections correctly.
- Scope and limits: the live seed contains only one group, so multi-group or university-scale rendering has not been established. Browser MCP was unavailable during the final repeat attempt (`NS_ERROR_CONNECTION_REFUSED`); no schedule rows, generated drafts, or wish records were mutated in this slice. No tests or test files were added.

## 2026-09-29 — Use the canonical group name in recurring grids

- Finding: the weekly grid rebuilt a group title from specialty and course even though the existing grid API already returns its canonical `group_display_name`. As a result, conflict details and the timetable heading used different formats for the same group.
- Change: the aggregate presenter now prefers the API's canonical group display name, retaining the previous derived label as a fallback for older or partial responses.
- Verification: rebuilt the Rails image; Ruby syntax, Zeitwerk loading and `/up` passed, and all Compose application services remained healthy. The browser backend still refused connections, so the updated heading could not be visually rechecked. No data was changed and no tests or test files were added.

## 2026-09-29 — Discard terminal generation snapshots

- Finding: private solver snapshots include teacher availability, workload assignments and wish-related context. Published, infeasible and terminally failed runs kept those snapshots after the run could no longer be published.
- Change: snapshot JSON is now replaced with `{}` after a run is fully published or reaches infeasible/terminal-failure status. Queued work, retryable failures and proposals with unpublished rows retain the snapshot they need. Findings, proposal rows, status, source digest and audit metadata remain available.
- Verification: rebuilt and restarted Hanami API and generation worker; generation routes loaded, the API became healthy, and the worker remained running. Inline isolated repo smoke checks confirmed terminal infeasible/failure and fully published paths scrub, while retries, active proposals and partially published proposals retain their source snapshot. No database rows were used or modified by the smoke checks; no tests or test files were added.

## 2026-09-29 — Reduce idle generation-worker database and log load

- Finding: every three-second idle poll selected the full generation-run row, including its potentially large immutable snapshot and proposal, although the relay only needs each candidate ID. The worker's ORM SQL logger also emitted one full query per poll.
- Change: pending-run scans now select only `id`; the worker loads the full run after its lease claim. SQL INFO logging is set to WARN only in the generation-worker process, leaving the API's logging unchanged. Scheduler-unavailable and invalid-response retries now emit a structured warning with run ID and exception class; warning/error logs remain enabled.
- Verification: rebuilt/restarted API and worker, confirmed API health and worker process state, and observed the live queue poll query selecting only `schedule_generation_runs.id`. After setting worker-only WARN logging, the idle worker emitted no SQL poll lines across a 20-second observation while remaining running. Compose configuration and changed Ruby syntax passed; no generation was queued and no database row changed. No tests or test files were added.

## 2026-09-29 — Scope department conflict summaries to displayed events

- Finding: department weekly grids reuse a faculty-wide analyzer report. The presenter counted every recurring faculty conflict, including findings unrelated to the selected department, while only rendering that department's lessons.
- Change: department summaries and red-cell markers now include findings only when at least one affected event belongs to the displayed recurring grid. Cross-department clashes touching the selected department remain visible, including the other lesson in their detail context. Faculty and university scopes keep their full-scope counts.
- Verification: rebuilt Rails and ran an inline synthetic presenter smoke with one selected-department conflict, one unrelated department conflict, one cross-department clash and one dated finding. Department mode showed two applicable recurring findings and marked its event red; faculty mode showed all three recurring findings; dated findings stayed excluded. No database rows changed. Browser MCP remains unavailable (`NS_ERROR_CONNECTION_REFUSED`), so this slice was not visually rechecked. No tests or test files were added.
- Runtime follow-up: reloaded the authenticated department view at the application's configured port. The live heading matched the canonical group label (`СИ 1 курс`), the page rendered one group and three red events, and the document had no horizontal overflow. Console errors: zero; one non-blocking CSS preload warning. The seed still has only one real group, so live cross-department filtering remains unverified; the synthetic presenter smoke covers that condition.

## 2026-09-29 — Restore selected proposal batch after publish rejection

- Change: generation publication now maps API conflict codes to actionable Russian messages. The selected proposal keys are held in per-tab `sessionStorage`, scoped to generation run ID and revision, and restored after recoverable redirects/reloads. A new draft revision invalidates the stored selection.
- Verification: rebuilt and recreated the Rails container from the current worktree. In the authenticated browser, selecting one private proposal row survived a full reload; the row, count and enabled publish action were restored. Clearing the test selection returned the form to zero selected and disabled publish. The private run remained proposed, and no publish request was submitted. Browser console errors: zero. Rails Ruby syntax, JavaScript syntax and `/up` returned successfully.
- Files: Rails generation controller/gateway, Schedule generation proposal form and `proposal_selection_controller.js`. No tests or test files were added.

## 2026-09-29 — Measure solver scaling under shared resources

- Evidence: an ephemeral solver-only benchmark in the pinned single-CPU scheduler container is recorded in `docs/architecture/scheduler-design-draft-2026-09-28.md`. Independent synthetic copies reached optimality quickly but are not representative. With shared teachers and only three rooms, 25 and 50 units remained feasible-but-unproven after 15 seconds; the 50-unit run had objective 46 and bound 0. With 15 shared rooms, the same 50 units proved objective 0 optimal in 5.697 seconds. The difference exposes a weak current objective bound under resource scarcity; it does not establish semester-scale performance.
- No schedule rows, wishes or generation runs changed during the benchmark. No code or test files were added for it.
- Next decision: choose the relative importance of approved teacher wishes, fewer gaps, compact days, preferred times and workload fairness before changing solver scoring. The current objective is intentionally left unchanged pending that product decision.
- Progress follow-up: on the same synthetic shared-resource cases, the solver reported its first full incumbent after 0.14 seconds for 25 units/3 rooms and 0.32 seconds for 50 units/3 rooms. It continued improving over the 15-second solve window and emitted 27 and 19 incumbent reports respectively; neither scarce-room case proved optimality. For 50 units/15 rooms, the first incumbent arrived at 1.93 seconds and optimality was proved at 2.57 seconds. This confirms early progress and a complete draft under these controlled inputs, while leaving real semester latency unverified.

## 2026-09-29 — Flag contradictory active wishes before approval

- Finding: each teacher wish was compiled independently. A new “prefer Monday period 1” rule could therefore be proposed and approved even when the same teacher already had an active “unavailable Monday period 1” wish; both could enter the solver objective.
- Change: `CompileTeacherWish` now reads the teacher's existing wishes for the same semester. Overlapping available/unavailable rules are withheld from the incoming wish and produce a Russian `CONTRADICTORY_TEACHER_WISH` review finding referencing the involved wishes. Existing approved preferences are preserved; opposite even/odd rules do not conflict. The incoming item stays non-approvable until the teacher clarifies it. Compiler version advanced to `russian-templates-v14`.
- Change: the super-administrator can withdraw an existing wish approval with the existing revision-checked rejection action. The teacher can then submit a clarified wish for recompilation against the remaining active wishes.
- Verification: Ruby syntax passed. An inline smoke verified that a conflict is withheld and reports both sources, a rejected wish is ignored, and opposite parity remains compatible. A read-only compile of a wish contradicting the selected teacher's seeded profile returned `PROFILE_TEXT_CONTRADICTION` with zero proposals. Routes loaded, and the authenticated Schedule wish-review page rendered with zero browser console errors.
- Concurrency follow-up: approval repeats contradiction detection inside a PostgreSQL advisory-locked transaction. The earlier teacher-keyed review lock has since been replaced by the shared preference-context lock described in the 2026-09-29 stale-compilation entry below, so workload/profile writes and approvals serialize on the same key. A production repository smoke selected only the active approved conflict and ignored the rejected wish. Two Hanami threads on separate transaction connections confirmed that the review lock serializes critical sections. Contradiction returns a distinct 409 that Rails translates to Russian guidance.
- Rollback-only integration: using the live Hanami compiler, repository and database inside a transaction forced to roll back, created and approved a temporary wish, verified the incoming contradictory rule was held for review, withdrew the approved wish, and recompiled the clarified request successfully. The harness checked that all temporary wish rows were absent after rollback. The Rails/API/scheduler health checks passed, and the authenticated review route had zero console errors; the running data still has no approved wish for a real-browser withdrawal click. No persistent wish, generation run or timetable row changed; no tests or test files were added.

## 2026-09-29 — Index fixed occupancy before solver candidate generation

- Finding: candidate pruning scanned every profile rule, room reservation and published lesson for every candidate placement. This repeated work grew with both snapshot size and candidate count before CP-SAT started.
- Change: `apps/scheduler/solver.py` now builds a hash index for fixed teacher, group/subgroup and room occupancy once per input snapshot, preserving parity and overlap behavior.
- Verification: compared old and indexed decisions over 648 deliberately varied candidate combinations; every result matched. In an isolated container microbenchmark, 500 lookups against 6,000 unrelated fixed lessons took 2.825 seconds with the old scan and 0.001 seconds with the index (about 3,300× for this hot path only). Rebuilt the pinned scheduler; `/health` is healthy and the checked-in synthetic faculty snapshot solved optimally with four placements. The live generation queue was empty before restart, and no generation run or published schedule row changed. `python3 -m py_compile apps/scheduler/solver.py` passed. No tests or test files were added.
- Limit: this microbenchmark isolates blocker lookup and does not predict total solve latency or establish semester-scale capacity.

## 2026-09-29 — Index soft objective rules during candidate generation

- Finding: each schedulable candidate also rescanned every profile-availability rule and approved soft wish to calculate its unchanged objective contribution.
- Change: `apps/scheduler/solver.py` now indexes the existing `-12` available and `+120` unavailable weights by teacher, weekday, period and week parity; no scoring priorities or weights changed.
- Verification: indexed scores matched the former calculation across 2,160 candidate/team combinations and 1,500 mixed rules. In an isolated benchmark, 12,000 candidate lookups took 2.489 seconds by scan and 0.010 seconds indexed (about 257× for the objective lookup). Rebuilt the pinned scheduler and repeated the checked-in synthetic HTTP solve: optimal, four placements, five analyzer findings, 0.03 seconds. The generation queue was empty before restart. Python compilation and `git diff --check` passed. No live generation run, published lesson or test file changed.
- Limit: the lookup benchmark isolates objective-rule matching and does not establish total solve throughput or semester-scale capacity.

## 2026-09-29 — Aggregate teacher-scoped consecutive preferences

- Finding: every teacher-scoped two-consecutive-lessons wish created CP-SAT pair variables for every ordered pair of eligible lesson units at every adjacent day/period/parity position. Teacher `AtMostOne` resource constraints already guarantee that at most one matching lesson occupies each such cell.
- Change: teacher-scoped wishes now aggregate lesson occupancy per cell and create pair variables only between adjacent aggregate cells. Requirement-only wishes keep the existing unit-pair logic because they do not imply one shared teacher resource.
- Verification: for a six-unit synthetic case, model size fell from 1,390 to 620 variables; consecutive-pair variables fell from 840 to 28 while 42 aggregate occupancy variables were added. Correctly loaded baseline and optimized implementations both solved optimally with objective −39 and eight placements (0.554s vs 0.021s on the pinned single-CPU container). CP-SAT selected different cell arrangements among tied optima, so the check establishes matching optimal score and feasibility, not identical cells. Rebuilt the worker; the existing HTTP synthetic scenario still returned optimal with four placements and `/health` succeeded. Python compilation and `git diff --check` passed. No live run or timetable row was changed, and no tests were added.
- Limit: the paired solver run and model-size comparison use one synthetic input; they do not predict semester-scale solve times.

## 2026-09-29 — Index candidate pairs in the static analyzer

- Finding: `analyzer.py` compared every lesson pair before filtering by weekday/period and shared teacher/group/room. Large snapshots therefore paid a quadratic scan cost even when almost all events used different resources.
- Change: conflict analysis now indexes lessons by weekday/period and resource identity, then runs the existing parity, date, subgroup, event-batch and staged-transfer checks only on pairs sharing a potential conflict resource.
- Verification: output exactly matched the previous analyzer for the checked-in synthetic proposal and empty proposal, plus 25 randomized snapshots with 72 recurring, dated and proposed events each. In an intentionally sparse-resource scenario with 2,500 lessons all at the same weekday/period, analysis took 10.035 seconds before indexing and 0.018 seconds after; both returned zero findings. `python3 -m py_compile` and `git diff --check` passed. No tests or live rows changed.
- Limit: the benchmark isolates sparse pair-search overhead and does not measure dense-conflict throughput or total generation latency.

## 2026-09-29 — Stop stale solver work during model construction

- Finding: the solver checked the generation lease-loss event immediately before CP-SAT search, but a worker whose lease expired during snapshot indexing or candidate/model construction could keep using CPU until model construction completed.
- Change: the generator now checks cancellation while counting/indexing fixed occupancy, expanding candidates, adding resource and occupancy constraints, and building consecutive-preference constraints. It also checks after optimization and analysis so a stale worker does not return a proposal. The existing CP-SAT search monitor is retained.
- Verification: a deterministic cancellation signal fired during occupancy indexing and during candidate construction; both calls returned `unknown / GENERATION_LEASE_LOST` with no placements. The uncancelled synthetic input still solved optimally with four placements. Python syntax and diff checks passed. No live generation run or schedule row was changed; no tests were added.
- Limit: this cooperatively stops Python model-building work; it does not alter lease timing, worker retries or server-side run ownership.

## 2026-09-29 — Keep double-negative avoidance wishes in review

- Finding: the deterministic Russian parser saw the word “избегать” as unavailability even in a phrase such as “не хочу избегать занятий в понедельник на первой паре,” which reverses the intent. It could therefore add an unwanted soft penalty to the solver objective.
- Change: negated avoidance language now produces an `AMBIGUOUS_PREFERENCE` review finding and no typed rule. The Hanami compiler version advanced to `russian-templates-v15`, so persisted wish compilations identify the changed parser semantics.
- Verification: the exact double-negative example produced review only. Clear “не могу” and “хочу избегать” examples still compile as `unavailable_slot`; “хочу вести” still compiles as `available_slot`. Python compiler syntax passed. No live wish, generation run or schedule data changed; no tests were added.
- Limit: this is a targeted conservative rule for a specific Russian negation pattern, not a general semantic parser.

## 2026-09-29 — Accept sparse solver progress callbacks

- Finding: the local worker reports best-bound checkpoints with a sparse payload (`total`, `bound_updates`, `objective_bound`, elapsed time), while the API endpoint required incumbent-only metrics such as `placed`, `solutions`, `branches` and `conflicts`. The endpoint rejected those checkpoints, and the worker treated the response as a lost lease.
- Change: `apps/api_geteway/slices/admin/actions/schedule/generation_runs_progress.rb` now accepts any known integer/float progress fields while requiring `total`; it validates each supplied value and checks `placed <= total` whenever an incumbent count is present. Unknown fields and invalid values remain rejected.
- Verification: Ruby syntax passed. Inline Hanami action checks accepted both sparse bound and full incumbent shapes and rejected an unknown key. Rebuilt/restarted the API. From the authenticated Schedule workspace, queued a university-wide private run `e09d0921-757a-409c-8a55-f03113a7a978`; all five progress POSTs returned 204, including the 117-byte sparse bound update. The run reached `proposed`, persisted solver metrics (8 solutions, 1,712 branches, 25 conflicts, objective/bound 6.0), and contained five private proposal rows. The browser showed the proposal and disabled publication because analyzer errors remain; no publish request was made. Browser console errors: zero. No tests or test files were added.
- Limit: this confirms the progress contract and one seeded university-wide run; it does not establish solve capacity for a production-sized university schedule.

## 2026-09-29 — Verify conflict correction inside a university draft

- Finding: the latest university-wide proposal reported three teacher-profile unavailability conflicts on existing recurring events and two room-eligibility findings. The Schedule workspace exposed each recurring conflict as a direct link into a private edit form.
- Verification: in private run `e09d0921-757a-409c-8a55-f03113a7a978`, moved existing events 5, 19 and 11 to profile-available cells using the draft editor. The run advanced to revision 4, retained the three `update_existing` proposal rows, and the analyzer cleared all three teacher-unavailability findings. The source `schedule_events` rows remained at their original weekday/slot/room values. The conflict list retained only two `ROOM_NOT_ASSIGNED` findings; the UI showed them with the red error treatment and kept publication disabled.
- Boundary: the generated Physics proposal row had no eligible room options beyond “Без аудитории,” so I did not alter workload room assignments to clear the remaining findings. I did not publish. The private run remains proposed at revision 5 after a dated-editor submission; its proposal has eight rows and two room findings. No tests or test files were added.

## 2026-09-29 — Clarify ineligible-room analyzer findings

- Finding: `ROOM_NOT_ASSIGNED` is emitted when a lesson already names a room, but that room is not in the linked workload's eligible-room set. The prior Russian message could be read as “no room was assigned.”
- Change: the local analyzer now says “Эта аудитория не закреплена за данной нагрузкой.”
- Change: the Rails proposal finding title now reads “Аудитория не закреплена за нагрузкой,” so the red finding heading and analyzer explanation describe the same eligibility problem.
- Verification: an inline live HTTP request to the rebuilt scheduler's `/v1/analyze` with a valid room outside the workload's eligible list returned `ROOM_NOT_ASSIGNED` with the new explanation; `/health` returned 200, Python compilation passed, and the scheduler plus generation worker were rebuilt and healthy. A fresh authenticated university-wide private run `197d998f-f60d-42e1-8609-11a424cd08bd` displayed both the corrected heading and explanation; publication remained disabled by unresolved errors. Rails was rebuilt, Zeitwerk loaded successfully, browser console errors remained zero, and no schedule or workload data changed. No tests or test files were added.

## 2026-09-29 — Verify faculty-wide generation from the administrator workspace

- Verification: from the authenticated Schedule workspace, selected faculty 1 and started “Составить для факультета.” The persisted run `1082baca-8e74-4cdd-a634-40765823f6fd` has `scope_type=faculty`, `faculty_id=1`, semester 1 and status `proposed`; it contains five proposal rows and persisted progress (5 placed, 8 solutions, 1,712 branches, 25 conflicts). All six progress callbacks returned HTTP 204. The university-wide run path was separately verified in the previous entry and stores `scope_type=university`. Neither run was published; generation changed no timetable rows. The seeded database has one faculty, so a previous rollback-only two-faculty fixture remains the evidence that university scope includes another faculty while a faculty scope excludes it. No tests or test files were added.

## 2026-09-29 — Revalidate the local Jev decision

- User requirement: the scheduling and wish-compilation path should remain usable locally if a hosted model becomes unavailable or is blocked.
- Evidence: TypeSafe's current [quick start](https://docs.typesafe.ai/introduction/quickstart) shows `POST https://api.typesafe.ai/v1/systemone` with a bearer API key; its [API reference](https://api.typesafe.ai/docs) describes the hosted service. The reviewed public docs do not show a Jev checkpoint or local inference runtime. This documents the public integration path, not proof that no private/on-premises offering exists.
- Decision: retain the local deterministic Russian-to-typed-JSON compiler and local CP-SAT solver; do not send teacher wishes or timetable snapshots to Jev. A local model remains optional shadow-only work behind the same validated rule schema. No runtime code or schedule data changed.
- Source limitation: reopening the shared-chat URL in the current browser failed with `NS_ERROR_PROXY_CONNECTION_REFUSED`; this entry records only the current official docs and the existing design decision, not new evidence from the shared transcript.

## 2026-09-29 — Report individually unplaceable lesson units precisely

- Finding: when any lesson unit had no legal placement candidates, CP-SAT returned an infeasible assumption core that could include unrelated units that did have candidates. The admin message then implied those lessons could not be placed together, obscuring the actual blocker.
- Change: the local solver records units with zero legal candidates and reports them as `NO_FEASIBLE_PLACEMENTS`, with a targeted Russian message. CP-SAT assumption cores remain in use for conflicts that arise only from interactions among otherwise placeable units. The schedule analysis view now labels both findings distinctly.
- Verification: rebuilt the local scheduler image and ran an isolated two-unit runtime scenario: one teacher unavailable in every slot and one unrelated feasible unit. The result was `infeasible`, listed only the blocked unit, and did not name the feasible unit. Python compilation and root/nested `git diff --check` passed. No generation or published schedule rows were changed; no tests or test files were added.
- Decision (resolved in the follow-up below): use best-effort partial private drafts with omitted lesson units marked as blocking errors. The later placement form makes those units editable in the same sandbox; the original all-or-nothing behavior is superseded.

## 2026-09-29 — Keep feasible placements in partially satisfiable drafts

- Finding: the solver treated every required lesson as mandatory, so one impossible unit discarded all otherwise valid placements. The all-or-nothing behavior also prevented administrators from seeing which part of a large faculty schedule remained useful.
- Change: each lesson unit is now optional in CP-SAT, with an objective weight bounded so maximizing the number of placed units always takes priority over approved soft preferences and period costs. Each omitted unit becomes a red `UNPLACED_REQUIRED_LESSON` error with its group, subject and ordinal. Such errors block the entire publication checklist. Proposal edits preserve these run-level errors when ordinary static analysis is recomputed, preventing an edit from accidentally unlocking publication. The schedule page states that the administrator must correct source constraints and generate a new draft; it shows a distinct empty-draft message when no unit can be placed.
- Verification: after rebuilding the scheduler, an isolated case with one fully unavailable teacher and one feasible lesson returned the feasible placement, one precise missing-unit finding, and progress of 1/2; a fully placeable case remained optimal with no missing-unit finding. The scheduler, API and Rails images rebuilt. Ruby syntax, Python compilation, solver import, existing admin schedule-page rendering, and focused diff checks passed. No publication or source schedule mutation was performed. No tests or test files were added.
- Current workflow boundary: missing units are not editable as virtual proposal rows yet. A run containing any omitted unit stays unpublishable; after resolving source constraints, the administrator generates a fresh draft. Ordinary conflicts on placed rows can still be edited and reanalyzed in the current private run.

## 2026-09-29 — Let administrators place missing units in the private draft

- Change: each `UNPLACED_REQUIRED_LESSON` finding now includes a form for choosing a weekday, period, supported week parity and eligible room. A new revision- and source-checked API operation adds the lesson as a private proposal row, reruns full analysis and removes only that unit's missing finding. Other missing-unit findings remain blocking; conflicts from the chosen cell use the existing proposal editor.
- Safety: the finding must still exist in the current run, the lesson unit and parity must match the current snapshot, room selection is constrained by the combined solver workload, and persistence uses the current run revision inside the placement lock. “No room” is offered and accepted only when the workload has no eligible rooms. Publication retains its existing error gate and final validation.
- Verification: rebuilt API and Rails images and used an authenticated browser against disposable clones of the seeded private generation run. An eligible-room lesson rejected a tampered “no room” value without changing the run, then accepted a valid placement. A roomless lesson with no eligible rooms accepted “no room”. A two-omission clone retained its other missing finding and kept publication disabled after one lesson was placed. All clones were deleted. No source schedule rows were changed or published; no tests or test files were added.

## 2026-09-29 — Normalize Russian ё/е in teacher-wish parsing

- Finding: the same time preference compiled for “четвертой паре” but fell into generic manual review for “четвёртой паре”. Subject matching had the same spelling sensitivity.
- Change: the deterministic compiler now folds `ё` to `е` for wish parsing and subject-token matching while keeping the original teacher text unchanged in storage.
- Verification: both fourth-period spellings compile to the same Friday `available_slot`; “Учет геодезии” resolves to the workload named “Учёт геодезии” for a consecutive-pair wish. All ten cases in the seeded Russian corpus retained their expected typed proposals and review finding codes through the rebuilt scheduler HTTP endpoint. No database or timetable data changed; no tests or test files were added.

## 2026-09-29 — Remeasure solver after max-placement objective

- Evidence: on a fresh deterministic fixture (six weekdays × four periods, 20 cyclically reused teachers, unique groups, uniform rooms, no published lessons/preferences), the solver placed/proved all 25 units with three rooms in 0.17s and all 50 in 0.39s. With 15 rooms it placed/proved 50 in 4.82s. At 100 units and three rooms it proved the 72-cell capacity maximum (72 placed, 28 omitted) in 1.36s. At 100/15 it placed/proved all units in 11.64s; first incumbent 6.61s. Full fixture methodology and branch/objective data are recorded in the scheduler design note.
- Interpretation: on this fixture, many interchangeable rooms increase symmetry and solve time; tighter three-room capacity made the 100-unit maximum easier to prove. Earlier 2026-09-29 benchmarks used a different exact candidate shape and are not directly comparable. This remains a single-container solver smoke, not a semester/API load test or a production SLO.
- No schedule, wish or generation-run rows changed; no tests or test files were added.

## 2026-09-29 — Recompile teacher wishes before approval

- Finding: administrators could approve persisted typed proposals without checking whether the compiler version, teacher profile restrictions, or workload context had changed since submission.
- Change: each approval request recompiles the original teacher text against current context before entering the per-teacher review transaction. If proposals, findings, or compiler version differ, the API stores the refreshed result as `review`, increments the revision, and returns a conflict. The admin receives a message to inspect the refreshed interpretation and submit a separate approval. Rejection remains available without recompilation. Compilation stays outside the database transaction so the scheduler HTTP call does not hold a review lock or database connection.
- Verification: an authenticated browser approval attempt against an isolated synthetic old-version wish returned the refresh notice; authoritative read-back showed `review`, revision 1, current compiler version, and a parser finding. The temporary wish was deleted and the table returned to zero rows. API and Rails images were rebuilt; Ruby syntax and runtime checks passed. No published schedule rows changed; no tests or test files were added.
- Concurrency follow-up: approvals now compile outside the database transaction, then take a short shared advisory lock and fingerprint the current compiler context before refreshing or approving. Statement-level database triggers take the same lock before writes to teacher constraints, workload assignments and labels, group-semester links, subjects, activity types, periods and week types. A context change between compilation and the approval transaction returns a retryable conflict; it cannot be approved from the stale compile. Statement-level locking acquires the advisory lock before row changes and avoids per-row lock ordering inversions on batch writes.
- Verification follow-up: the ten context-table triggers are installed as `FOR EACH STATEMENT`; an authenticated stale-wish approval still refreshed to review/revision 1 after the image rebuild. A live transaction-lock probe showed a context-table update remain pending while the approval lock was held, then complete and roll back after release. The temporary wish was deleted and the table returned to zero rows. No timetable or workload row changed.
- Boundary: future profile/workload edits are detected and invalidated when a generation snapshot includes that teacher, as described in the following entry; wishes outside the selected generation scope are checked when they next enter scope or an administrator attempts approval. Profile unavailability remains a hard solver constraint throughout.

## 2026-09-29 — Revalidate approved wishes when building a generation snapshot

- Finding: the approval-time fingerprint protected the approval transaction, but an approved wish could remain active after a later profile or workload change. A subsequent generation snapshot would otherwise send its old rule to the solver.
- Change: teacher wishes now persist the canonical compiler-context fingerprint. Generation snapshot construction runs under the shared context lock; for each in-scope approved wish it recomputes the fingerprint. A mismatch demotes the wish to `review`, clears its approval metadata, increments its revision, adds `STALE_APPROVED_CONTEXT`, and excludes its proposals from `approved_preferences`. The review page exposes the approval action so the administrator can trigger recompilation; changed output requires a second explicit approval.
- Verification: an authenticated faculty generation used a temporary stale approved wish for an in-scope teacher. Read-back showed `review`, revision 1, a stale-context finding, and zero approved preferences in the private run snapshot. The admin page displayed the finding and re-review action. The run was still unpublished; both temporary rows were deleted, and the wish table returned to zero. No published schedule or workload rows changed; no tests or test files were added.
- Migration verification: created an empty local `database_test` required by the configured Hanami database environment; `hanami db migrate --env=development` then completed for both development and test. The clean test schema contains all ten statement-level context-lock triggers and the wish fingerprint column. The generated development `structure.sql` dump now matches the repository snapshot exactly.
- Review UI follow-up: stale wishes now use the action label “Перепроверить пожелание” so administrators can distinguish recompilation from approval. An authenticated browser click displayed the refresh notice, updated the wish to review/revision 3 with the current fingerprint, and removed the approval action when the fresh compile returned no proposal plus a profile contradiction. The temporary row was deleted; no approval occurred.
- Boundary: only wishes for teachers in the selected generation scope are revalidated by that run. Other scopes do not consume those preferences; they are checked when an approval is attempted or a later run includes that teacher.

## 2026-09-29 — Apply administrator-selected solver priorities

- Decision: after maximizing the number of placed required lessons, optimize approved teacher wishes first, then compact teaching days and fewer gaps; period number is only a final tie-breaker.
- Change: the local CP-SAT objective now encodes those priorities lexicographically with conservative bounds. Group-day occupancy contributes active-day and interior-gap costs, while groups with one fixed lesson unit skip the constant compactness terms. This keeps the objective aligned with the selected order and avoids unnecessary symmetry variables in sparse group schedules.
- Verification: the supplied synthetic Russian scenario reached an optimal 4-placement draft with the expected five review/analyzer findings. Focused solver-only scenarios confirmed an approved Tuesday wish wins over keeping a group's schedule on Monday, and two lessons for one group use the same day in adjacent periods when no wish overrides that choice. A shared-resource fixture with 50 units, 15 rooms and one CPU placed all 50 and proved optimal in 6.01 seconds (108,126 branches, 8 progress reports). The scheduler image was rebuilt and health returned 200. Python compilation and `git diff --check` passed.
- No generation run or published schedule was created or changed; no tests or test files were added. Fairness weights and target semester size remain undefined. By product decision there is no hard solve-time objective or wall-clock deadline; progress remains visible while a run continues.

## 2026-09-29 — Remeasure priority solver at 100 lesson units

- Evidence: on the updated one-CPU CP-SAT model, 100 units with three shared rooms proved the 72-room-cell capacity maximum in 1.32 seconds; the first full incumbent arrived at 1.32 seconds, and 28 required units remained visibly unplaced. With 15 shared rooms, all 100 units were placed and optimality was proved in 11.38 seconds; the first incumbent arrived at 7.15 seconds. These shapes match the earlier synthetic scale smoke and include the approved-wish, compact-day/gap and period tie-break priority structure.
- Interpretation: the added goals preserve the same room-capacity bound and similar elapsed time on this fixture. This still does not establish API throughput, expected real semester capacity, or a solve-time SLO.
- No generation run or published schedule was created or changed; no tests or test files were added.

## 2026-09-29 — Verify current solver through administrator generation

- Verification: from the authenticated Schedule workspace, queued a fresh university-wide private run through the administrator button. The browser received durable progress updates while all five lesson units were placed and CP-SAT continued optimizing. The run reached `proposed` after 202 seconds with five private proposal rows and five analysis findings (three teacher-availability, two room-eligibility); all five affected lesson rows carried the red `is-error` state with a computed 4px `rgb(180, 57, 47)` left stripe, and the publication section explained that selection stays unavailable until errors are fixed. Its `published_at` remained empty and the page explicitly stated that the published timetable was unchanged. No publish action was submitted; browser console errors: zero.
- The run generated 131 progress events and reported eight feasible solver solutions. The final solver report recorded 7,201,287 branches, 3,857,177 conflicts, and matching best objective/bound 51. The run is intentionally retained as an administrator-reviewable private draft. Scheduler source SHA-256 matched the rebuilt container image; scheduler health returned 200.
- This demonstrates end-to-end privacy, durable live progress and terminal proposal behavior with the selected objective, while exposing that exact optimization can take several minutes even for this five-unit seeded snapshot. Solve duration is open-ended by product decision; this observation is not a general latency guarantee, and no numeric latency SLO is defined. No published schedule rows were changed; no tests or test files were added.
- Conflict-resolution follow-up: staged three recurring event moves to non-conflicting periods that avoid the teacher's hard first-period restrictions, then removed the invalid room from the dated occurrence because its workload has no eligible-room assignments. Reanalysis removed all five findings, including both findings for the same transferred dated occurrence. The private proposal now has nine publishable rows at revision 7; no rows were selected and the publish action was not submitted. Authoritative read-back shows `published_at` null, zero run findings, and original `schedule_events` rows 5, 8, 11 and 19 unchanged; transfer row 5 still has room 1 and its original date/time overlay in the live table. This demonstrates sandbox repair and whole-proposal reanalysis without changing the published schedule. No tests or test files were added.
- Selection follow-up: checked one eligible generated row in the browser and observed the publish action enable; unchecking it returned the selection count to zero and disabled the action. No publish request was sent, the run revision stayed unchanged, and the clean private proposal remains available for review.

## 2026-09-29 — Clarify solver objective in live progress

- Finding: the progress panel showed a solver objective and bound without explaining that the score is minimized, making an improving search hard for administrators to interpret.
- Change: the Russian progress copy now labels the value as a target objective, says lower is better, and identifies the second value as the lower bound.
- Verification: rebuilt and restarted the Rails service; `/up` returned successfully. The authenticated page rendered “Целевая оценка (меньше — лучше)” and “нижняя граница” against the retained university proposal, with all nine rows and zero findings preserved. The publish button stayed disabled with zero selected rows; the run remained `proposed` at revision 7 with no `published_at`. Browser console errors: zero. No tests or test files were added.

## 2026-09-29 — Make the analysis heading valid without a faculty selection

- Finding: the semester-only Schedule workspace offered university generation without a faculty selection, but titled the analysis section “Анализ расписания факультета”.
- Change: the section heading is now scope-neutral: “Анализ расписания”.
- Verification: rebuilt/recreated `schedule_web` and opened `/admin/schedule?semester_id=1` in the authenticated browser. The neutral heading and enabled university-generation action rendered; faculty generation remained disabled without a faculty selection. Browser console errors: zero. No generation or schedule mutation was submitted; no tests or test files were added.

## 2026-09-29 — Cancel an active private schedule generation

- Product decisions: the user deferred workload fairness. The solver objective remains maximum required placements, approved wishes, compact days/gaps and an early-period tie-break. Text-based “cannot teach” preferences remain soft; hard profile unavailability stays authoritative.
- Finding: the worker already stopped CP-SAT when its lease was lost, and the run schema allowed `cancelled`, but administrators had no action to stop an active run.
- Change: added an owner-authorized cancellation endpoint and Schedule control. A single conditional update moves only queued/processing runs to `cancelled`, clears the private snapshot and callback digest, increments revision/event sequence and retains progress for review. The next protected worker progress callback is rejected, which signals the existing cooperative CP-SAT stop path. Published lessons are not touched.
- Preference alignment: the deterministic compiler now accepts text-based unavailability as a soft rule when it opposes soft profile availability. A text request for availability that conflicts with hard profile unavailability remains flagged for review and withheld. The compiler version is `russian-templates-v16`, so existing approvals are recompiled through the established stale-version review path.
- Verification: rebuilt API, Rails, scheduler and generation worker. Hanami/Rails route loading and Rails Zeitwerk passed; changed Ruby syntax and Python compilation passed. Two authenticated university runs displayed live progress and the stop control, then transitioned to `cancelled`. Read-back for both showed the snapshot cleared, proposal null, no publication timestamp, and the schedule event count unchanged at 11. A follow-up solve request reached the scheduler after cancellation and returned the expected invalid-snapshot response rather than `SOLVER_BUSY`, confirming its one-solve slot was released. The browser showed the stopped-state message, “Этап: составление остановлено”, and zero JavaScript errors. During the second run, the updated live progress controller rendered “Целевая оценка (меньше — лучше)” and “Нижняя граница” consistently with the static page. Direct compiler scenarios confirmed the soft-unavailability rule and hard-profile precedence. No tests or test files were added.

## 2026-09-29 — Keep sensitive bind values out of application logs

- Finding: ORM SQL logging interpolated bind values, including the generation worker's hashed progress capability. This query content does not belong in routine application logs.
- Change: the Hanami application logger now defaults to WARN. Structured request metadata and administrator audit events continue through their existing separate sinks; worker and API warnings/errors remain available.
- Verification: rebuilt API and generation worker. A deliberately invalid callback against a cancelled run returned 404; API container logs contained no `progress_token_digest` SQL, while the dedicated access log recorded only the request method/path/status. Hanami route loading and changed-file syntax passed. The probe did not update a run or published schedule. No tests or test files were added.

## 2026-09-29 — Serialize scheduler snapshots with source writes

- Finding: publication rechecked the source digest while holding the schedule placement lock, but the snapshot builder read its inputs in separate queries while locking only teacher-preference context. Concurrent edits to rooms, calendar overlays, transfers, or other inputs could therefore race the digest check.
- Change: snapshot construction now holds the placement lock for the full read and then acquires the teacher-preference lock. Wish review uses the same placement-then-preference lock order. Statement triggers serialize writes to all 26 snapshot input tables with those locks, including source tables for lesson and room data, calendar overlays, wishes, and speciality labels.
- Verification: applied both migrations and rebuilt/restarted the API; all services remained healthy. Live database inspection found all 26 distinct triggers and confirmed the lock order. A no-op holiday update blocked while the placement lock was held and resumed immediately after release. The authenticated Schedule page successfully queued a university run; the verification run was stopped through the UI, read back as `cancelled`, and displayed the message that the published schedule was unchanged. Browser console errors: zero. No tests or test files were added.

## 2026-09-29 — Start generation from the reviewed aggregate timetable

- Finding: the administrator could inspect a university/faculty weekly aggregate, but the table offered no direct route to create its corresponding private draft.
- Change: the weekly aggregate report now links to generation with its selected semester and, for faculty scope, its faculty ID. The action is omitted for dated and department views, which do not define a supported generation scope. The per-group timetable table and its columns are unchanged.
- Verification: rebuilt/recreated `schedule_web` and used the authenticated browser. University view linked to `/admin/schedule?semester_id=1`; faculty view linked to `/admin/schedule?faculty_id=1&semester_id=1`, and opening it retained both selections. The existing group timetable still rendered with its labelled horizontal scroll region. At 390px the document width remained 390px while the table scrolled inside its wrapper; dated view rendered no compose action. Browser console errors: zero. No generation or timetable mutation was submitted; no tests or test files were added.

## 2026-09-29 — Validate whole and partial publication against the live draft

- Finding: the real publication operation rejected generated proposal rows because JSON supplied `subgroup` as an integer while the publisher passed it to Ruby's base-aware `Integer(value, 10)` parser, which only accepts strings. The same conversion was present for dated edits.
- Change: both recurring and dated publication paths now normalize the value with `to_s` before decimal parsing. No contract or persisted schema changed.
- Verification: `ruby -c` passed for the publisher, and `git diff --check` passed for that file. In the live Hanami operation, a rollback-only whole-publication attempt accepted all nine rows (five created, four updates/corrections), left zero proposal rows, and reported `published` inside the transaction. A separate rollback-only partial batch containing the four staged conflict corrections plus one generated row succeeded, read back the expected schedule placement, retained four proposal rows and zero findings, and advanced the run to revision 8 inside the transaction. Selecting the generated row alone correctly returned conflicts because the four required corrections were omitted. After each attempt, the outer rollback restored the draft to revision 7 with nine proposal rows and zero findings, and restored schedule event, transfer and outbox counts exactly to 11, 4 and 83. No publication was committed.
- Authenticated browser verification: the clean draft page showed nine enabled proposal checkboxes, the selected-publication submit button disabled at zero selection, and the error/reanalysis guidance. No publish request was submitted; browser console errors: zero. No tests or test files were added.

## 2026-09-29 — Include empty groups in recurring scope grids

- Finding: the aggregate weekly view derived its group sections only from schedule-event rows. A student group in the selected semester with no placed lesson disappeared, so faculty/university views did not represent the full selected-semester roster.
- Change: added the read-only API route `/admin/schedule/group_roster`, with semester, faculty and department filters, and a single database query over in-course group-semester memberships. University scope is restricted to super-admin/scheduler accounts; scoped filters pass through the authenticated-admin read policy. The Rails view unions this roster with event-backed groups and renders the existing labelled grid for each, with empty groups showing zero lessons. A roster-fetch failure blocks the table display so a partial scope is not presented as complete. The university read uses one roster query, not one request per faculty.
- Verification: rebuilt API and Rails. The route appeared in Hanami's route table, Hanami setup loaded, Rails Zeitwerk passed, and Rails `/up` returned successfully. In the authenticated browser, a temporary no-event group in faculty 1 appeared in both faculty and university views with the existing five time rows and all six weekday columns and showed `0 занятий`. A second temporary faculty and group appeared in the university scope, stayed out of faculty 1, and appeared alone in faculty 2. Department scope still rendered its existing event-backed group. Browser console errors: zero. All temporary memberships, groups, speciality and faculty were deleted and read back absent; the university page returned to the original group. The database returned to one student group and one selectable faculty, and `schedule_events` remained at 11. No published timetable rows were changed. No tests or test files were added.

## 2026-09-29 — Measure full-scope grid rendering with 1,000 empty groups

- Finding: the requested one-table-per-group view has no pagination because administrators need the whole selected scope. Its browser cost had not been measured beyond the one-group seed.
- Verification: added 1,000 temporary in-course group-semester memberships with no schedule events, then loaded the university view. It rendered all 1,001 groups, each with five period rows and six weekday cells; 1,000 showed `0 занятий`. Browser `PerformanceNavigationTiming` reported response start at 215 ms, DOM interactive at 397 ms, and load at 914 ms. The page contained 62,361 DOM elements and 3,756,745 decoded HTML bytes (30,552 encoded); document/body width stayed at 1,280 px. This is a single-browser local smoke, not a concurrent-load or production database benchmark. The temporary 1,000 groups were deleted; read-back found zero in their ID range, the database returned to one group/one membership, and `schedule_events` remained at 11. No published timetable rows changed; no tests or test files were added.

## 2026-09-29 — Serve brand fonts locally in every layout

- Finding: an unavailable/blocked Google Fonts stylesheet delayed `DOMContentLoaded` to 25,970 ms on the public root page, despite a 185 ms response start and 255 ms DOM interactive time. The admin page had the same external dependency. The browser reported OpaqueResponseBlocking for the remote stylesheet.
- Change: bundled the existing Manrope and Unbounded variable font faces as Cyrillic/Latin WOFF2 subsets from their upstream SIL Open Font License releases, preserving both licenses under `app/assets/fonts/` ([Manrope](https://github.com/googlefonts/manrope), [Unbounded](https://github.com/googlefonts/unbounded)). The admin, teacher and public layouts now load the same local `brand_fonts.css`; the external font links and CSP allowances were removed. Unbounded retains the public layout's 800 weight.
- Verification: Propshaft precompiled and fingerprinted all four WOFF2 assets. The authenticated university page and public root both loaded all declared faces with zero external font requests; their measured load events were 368 ms and 193 ms respectively. Computed stacks remain Manrope and Unbounded, public/admin page layouts loaded without alerts, and the browser recorded zero new console errors. No tests or test files were added.

## 2026-09-29 — Verify soft wishes cannot override hard profile availability

- Verification: ran the checked-in synthetic scenario through the pinned scheduler container's current `compile_wishes` and `generate` functions. The compiler produced typed soft proposals for supported wishes and review findings for profile contradictions, ambiguous multi-subject requests, unsupported consecutive avoidance, and unverified room software; the heater explanation produced no room or equipment constraint.
- Solver boundary: constrained a single lesson to Monday period 1 while an approved soft wish asked to avoid that slot. The solver still placed the required lesson and emitted `TEACHER_SOFT_PREFERENCE_NOT_MET` as a review finding. After marking that same slot hard-unavailable in the teacher profile, the solver produced no placement and reported `UNPLACED_REQUIRED_LESSON` as an error.
- Scope: both solver inputs were modified in memory from the synthetic fixture and executed inside the running pinned scheduler container. No generation run, teacher wish, schedule event, or published timetable row was created or changed. No tests or test files were added.

## 2026-09-29 — Enforce generation-run privacy across super-admin accounts

- Finding: the API's super-admin authorization shortcut ran before the existing requester check, so a different super-admin who knew a run UUID could read, edit, cancel, or publish another administrator's private generation run.
- Change: `schedule_generation_runs` read/update requests now verify `requested_by_account_id` before any super-admin shortcut. The owning super-admin retains access; other administrators, including other super-admins, are denied. The run's creation scope rules are unchanged.
- Verification: rebuilt and restarted the API image. A focused in-container authorization probe against the current authorizer allowed the owner super-admin to read and update its run and denied a different super-admin for both actions. Ruby syntax and scoped whitespace checks passed. The API, scheduler, worker and Rails services are running. No run or timetable row was read or changed by the probe; no tests or test files were added.

## 2026-09-29 — Confirm generation has no configured wall-clock deadline

- Requirement: the user permits generation to run as long as necessary, provided its progress remains visible.
- Verification: the live `schedule_generation_worker` reports `SCHEDULER_SOLVE_SECONDS` unset. In that path `GenerateScheduleRun` omits `X-Solve-Seconds` and sets the Net::HTTP read timeout to `nil`; an in-container Ruby check confirmed the effective timeout value remains `nil`. The scheduler CLI and HTTP handler also default to no deadline when no limit is supplied. The solver container is bounded to one CPU and 2 GiB memory, which constrains resource consumption but imposes no wall-clock cutoff. The worker refreshes its DB lease independently while waiting, and the progress reporter continues posting run-scoped events.
- Scope: read-only runtime/config inspection; no generation run or timetable data was created or changed. No tests or test files were added.

## 2026-09-29 — Requeue transient scheduler-capacity responses

- Finding: the scheduler correctly returns `429 SOLVER_BUSY` while another CP-SAT solve owns its single slot, but the API treated every non-200 response as an I/O failure. After five claimed attempts this could turn sustained capacity contention into a terminal failed run.
- Change: the API now recognizes only the scheduler's explicit `SOLVER_BUSY` response and requeues that run with capped exponential backoff and jitter. A separate contention counter is preserved across worker claims; it clears the stale lease/progress capability, advances the event sequence so polling sees the queued state, and does not consume the bounded solver-failure attempt counter. Other errors retain the existing bounded retry behavior.
- Verification: syntax and scoped whitespace checks passed. A two-cycle rollback-only integration smoke used the actual API operation/repository against the live database while stubbing the scheduler response to `429 {"error":"SOLVER_BUSY"}`. Retries 5 and 6 used the expected longer/capped delays, advanced the separate contention counter, retained the normal attempt count, and left no terminal error; the outer transaction restored all schedule-generation status counts exactly. A separate in-memory concurrency smoke sent two simultaneous requests to the live scheduler: the first 250-unit synthetic solve held the single CP-SAT slot and the second received exactly HTTP 429 `SOLVER_BUSY`; the first ended `unknown` at its explicit eight-second smoke limit with no database interaction. With no active or queued runs, the rebuilt API and worker were restarted and became healthy. No test files or durable schedule/run rows were changed.

## 2026-09-30 — Seed dense CP-SAT searches with deterministic feasible hints

- Finding: on a deterministic 50-group/20-teacher/15-room synthetic snapshot with four periods and three eligible rooms per unit, a 10-second solve found only 160 of 500 placements and 35 of 1,000. The checked-in small scenario did not expose this search-start problem.
- Change: the solver now tries five deterministic greedy passes over candidate placements and adds partial assignment hints for the best conflict-free draft. Candidate legality, hard constraints, the lexicographic objective and final analysis are unchanged; CP-SAT may reject or improve the hint.
- Verification: on the same 10-second diagnostic shape, the rebuilt HTTP service returned 100/100, 357/500 and 360/1,000 placements. The 1,000-unit result reaches the synthetic 360 room-cell upper bound (15 rooms × six days × four periods); all runs still reported `feasible`, not proven `optimal`. An in-process progress-callback run observed first incumbents of 97/100 at 1.44s, 357/500 at 7.52s and 360/1,000 at 11.05s including model construction. The checked-in scenario remained deterministic across repeated solves, optimal with four placements and zero analyzer errors. Focused one-cell smokes confirmed whole-group/subgroup overlap is blocked while even- and odd-week lessons for the same group may share a displayed cell. Scheduler health returned 200 and container source SHA-256 matched the worktree.
- Limits and isolation: each scale sample used an explicit 10-second diagnostic cap; this is not the normal generation path or a production capacity benchmark. No generation run, teacher wish, timetable event or published lesson changed. No test files were added.

## 2026-09-30 — Keep consecutive wishes soft under the placement-first objective

- Finding: the consecutive-wish solver encoded `sum(actual adjacent pairs) <= pair_count`. Because this was a hard model constraint, an approved soft wish could force required lessons to remain unplaced when the only legal schedule had more adjacent pairs than requested.
- Change: replace the hard cap with an integer reward variable bounded by `pair_count` and by the number of actual adjacent pairs. The objective rewards up to that count while leaving additional pairs legal. Required placement remains lexicographically higher priority than all wish rewards.
- Verification: a live HTTP solve with one teacher, three required lessons, exactly three profile-available periods and one approved soft pair wish returned `optimal` with all three lessons placed in periods 1–3. The final analyzer returned zero errors. The checked-in synthetic scenario stayed deterministic and optimal with four placements and zero analyzer errors; its review findings remained visible. Scheduler health returned 200, and the rebuilt container's `solver.py` SHA-256 matches the worktree.
- Profile precedence: with Monday period 1 as the only profile-available cell, an approved text wish to avoid that time still placed the required lesson and returned `TEACHER_SOFT_PREFERENCE_NOT_MET` as a review finding. Making the same cell profile-unavailable blocked placement and returned `UNPLACED_REQUIRED_LESSON` as an error.
- Isolation: all requests were in-memory solver/analyzer HTTP calls. No generation run, wish row, published event or timetable data changed. No tests or test files were added.

## 2026-09-30 — Recheck the referenced shared Jev discussion

- Evidence: reopening the supplied share URL through the public-web reader returned the page title but no transcript body; the authenticated browser tool failed with `NS_ERROR_PROXY_CONNECTION_REFUSED`; exact-ID web search returned no result.
- Documentation correction: the architecture draft now attributes confirmed requirements to the user's answers in this thread, not to content that could not be read. The clarified requirements remain actionable: local deterministic prose-to-JSON compilation, hard profile unavailability, private scope-isolated generation, visible progress, conflict review and explicit publication.
- Boundary: the user has been asked in chat to supply any additional decisions from the transcript that are not already captured here. Work continues against the confirmed requirements; no source code or schedule data changed in this check.

## 2026-09-30 — Verify cross-group teacher and room transfer conflicts

- Verification: exercised the real `EventTransferRepo#move_batch` operation under `ScheduleEventRepo#with_placement_lock` using disposable event/roster rows inside an outer rollback-only database transaction. A recurring source lesson moved onto another group's same-time recurring lesson was rejected with `:slot_taken` for a shared teacher; an isolated room-only collision was also rejected with `:slot_taken`.
- Fixture correction: the teacher collision probe explicitly inserted both `event_teachers` links, so the occurrence projection resolved the same teacher person on each group. No fixture rows or transfer records survived either transaction. The pre-existing timetable was not changed.
- Scoped authorization: invoked the production `Authorizer#authorize!` for `event_transfers:create` against a real schedule event owned by kafedra 1, using in-memory `CurrentAccount` principals. A kafedra admin scoped to kafedra 1 was allowed; an otherwise identical principal scoped to kafedra 999999 was denied. No account or scope row was inserted, and no transfer was submitted.
- HTTP authorization: sent a request to the running `/admin/event_transfers/batch` route with a short-lived, locally signed synthetic kafedra-admin token scoped to kafedra 999999 and targeting an event owned by kafedra 1. The API returned HTTP 403 `forbidden`. Its deliberately out-of-semester source date would also have been rejected before persistence if authorization had unexpectedly allowed it. No account or scope row was inserted.
- Read-back: student-group, schedule-event and transfer counts remained 1, 11 and 4 after the HTTP request. Cross-group teacher/room conflict and scoped-role denial are verified at the repository, authorizer and HTTP layers. No tests or test files were added.

## 2026-09-30 — Recheck live publication selection gates

- Clean draft: opened the authenticated Schedule page for an owner-visible university run with nine proposal rows and zero findings. With no row selected, `Опубликовать выбранные занятия` was disabled. Selecting one proposal enabled it; deselecting restored the zero-selection state.
- Conflicted draft: opened an owner-visible faculty run with unresolved findings. The page displayed the correction instruction, disallowed publication selection, and kept the publish button disabled.
- Isolation/read-back: neither publish form was submitted. Both runs remained `proposed`, their revisions were unchanged, and `published_at` remained null. Group, event and transfer counts remained 1, 11 and 4. Browser snapshots: `.playwright-mcp/page-2026-09-29T21-30-07-244Z.yml` (one clean row selected) and `.playwright-mcp/page-2026-09-29T21-30-22-594Z.yml` (unresolved findings block selection). No tests or test files were added.

## 2026-09-30 — Recheck positional week-parity tracks

- Runtime geometry: the live Schedule grid rendered four cells with alternating-week lessons. At 1280px each even/odd track pair measured equal heights (148–151px) with the odd track below the even track. At 390px the pairs remained equal; the 780px timetable stayed inside its labelled 360px scroll region and document/body width remained 390px.
- Uneven-content probe: temporarily appended four cloned cards to one parity half in the browser DOM, measured equal 725px tracks, then removed the clones. No request or schedule mutation was made.
- Source identity: the Rails container's `_admin_workspace.css` and Schedule ERB SHA-256 values matched the worktree. Browser console errors: zero. No code change was needed; broader shared Schedule interaction acceptance remains tracked above. No tests or test files were added.

## 2026-09-30 — Compact Schedule entry point and confirm active-group grid behavior

- Change: moved schedule analysis and generation entry points from the tall default analysis block into the Schedule header and a disclosure menu. The detailed analysis stays expanded when requested or when a run/review result is present. Closed disclosure content no longer contributes to page width; the open menu stays within a 390px viewport. The committed context summary and navigation tabs were tightened without changing timetable axes, columns or cells.
- Verification: on the authenticated Schedule page at 1280×900, the first timetable row begins at y=359px (the design target is at or above 400px); the committed context summary is 58px high and common controls are 40px. The read-only analyzer link opened the review section and showed all four current errors. At 390px, document and body widths both equal 390px; the 780px table remains in its explicitly labelled 360px horizontal scroller. The open generation panel measured 358px and stayed within x=18–376px. No generation or publication form was submitted.
- Workload: the current authenticated page retained its 24px/32px Unbounded heading, 40px search/actions, table structure and labelled table scroller; the table begins at y=440px. Browser console reported zero errors or warnings.
- Active groups: confirmed the user's choice to render a blank grid for every active group in scope. The existing API roster query selects all in-course group-semester memberships for the selected semester (with optional faculty/department scope), and the presenter unions that roster with scheduled groups before rendering. The current faculty runtime had one active group and rendered its full 30-cell weekly grid. The existing 2026-09-29 university smoke with 1,000 temporary unscheduled active groups rendered all 1,001 grids, including 1,000 groups labelled `0 занятий`; its fixtures were removed and read back as zero. No schedule data changed in this verification.
- No tests or test files were added.

## 2026-09-30 — Enforce room field limits before persistence

- Finding: the Rooms form accepted a room name longer than the database's `varchar(30)` limit. Hanami surfaced the database exception as HTTP 500, while Rails showed a generic failure. The corresponding room-number column is limited to 20 characters.
- Change: API create/update contracts now enforce 30-character names and 20-character numbers. Create and edit inputs expose matching `maxlength` values. Rails retains the submitted room draft and gives a Russian validation message with those limits; forbidden, conflict and service-failure outcomes have distinct safe messages.
- Contract path: Rooms form → `Admin::Resources::RoomsController` → `TeachersWorkspaceGateway` → API `POST/PATCH /admin/rooms` → `Rooms::Create/Update` contracts → inherited resourceful repository write. No table columns or relationship identities changed.
- Runtime CRUD: created disposable room ID 14 in building 1/type `лекционная`, read it back in the refreshed list, updated its name under the same ID, then deleted that exact unreferenced room. The delete notice appeared and a fresh Rooms response listed only the original room; the temporary marker was absent.
- Runtime failure: attempted overlength room-name create and edit submissions plus an overlength room-number create, all with valid building/type selections. Each reopened the relevant editor, retained all submitted field values, and did not create/change a row. The create error explicitly displayed both limits. No API database exception was emitted by these validation rejections.
- Sheet behavior: at 390×844 the create sheet measured x=8..382 and y=69..836, within the viewport, with no horizontal page overflow. At desktop width, Escape closed it and returned focus to “Добавить аудиторию.” Browser console errors/warnings: zero.
- Checks: Rails and API changed files passed Ruby syntax checks in their running container images; Rails `zeitwerk:check` passed; both repository-scoped `git diff --check` commands passed. No tests or test files were added.
- Remaining: this verifies only Rooms; the other Resources CRUD families and broader B03 acceptance remain open.

## 2026-09-30 — Bound subject names to their database columns

- Finding: the Subjects create/update contracts accepted names longer than the database's 50-character columns, leaving PostgreSQL to reject oversized values during persistence. The shared form did not expose either limit, and an invalid response had no field-level explanation.
- Change: API Subjects create/update contracts enforce 50-character maximums for full and short names. The shared ERB form emits `maxlength=50` only for Subjects, preserving other resource-field contracts. Rails maps oversized submitted values to specific Russian full-name/short-name feedback and reopens the editor with the draft.
- Contract path: Subjects form → `Admin::Resources::PostsController` → `TeachersWorkspaceGateway` → API `POST/PATCH /admin/subjects` → Subjects contracts/actions → `SubjectRepo`. Existing query `q` continues through create, edit and delete forms.
- Runtime failure: with search context `q=TMP-CODEX-0930`, an overlength create (66-character name) showed the field-specific error, kept name/short-name/search values, and created no row. An overlength short-name update (51 characters) similarly retained the editor draft and left the original row unchanged.
- Runtime CRUD/read-back: created disposable subject ID 5609; the active search returned its full and short names. Updated the short name and read it back under the same ID with the search query retained. Deleted that exact unreferenced subject; the refreshed search showed zero rows and the empty-result state, with `Дисциплина удалена.` feedback. No schedule or workload data referenced the disposable subject.
- Table and viewport: the existing three labels (`Название`, `Короткое название`, `Действия`) remain in the same order. At 390px the page width remained 390px and no editor remained open after cleanup. Browser console error count: zero.
- Checks: changed API contracts passed Ruby syntax inside the API image; changed Rails controller passed Ruby syntax and `zeitwerk:check`; scoped `git diff --check` passed. No tests or test files were added.
- Remaining: this representative Subjects path does not complete the other shared resource families or the full B03 acceptance matrix.

## 2026-09-30 — Enforce Activity Type field lengths

- Finding: Activity Type name and short-name columns are limited to 30 and 10 characters, but their create/update contracts had no matching bounds. The shared editor also let administrators exceed those limits.
- Change: API create/update contracts validate both limits. The shared resource form emits the matching `maxlength` values only on Activity Types and Subjects. Rails now identifies an overlength Activity Type field in Russian and retains the submitted editor draft.
- Contract path: shared catalog form → `Admin::Resources::PostsController` → `TeachersWorkspaceGateway` → API `POST/PATCH /admin/activity_types` → Activity Types contracts/actions → `ActivityTypeRepo`.
- Runtime failure: submitted a 39-character activity name; the editor reopened with its draft and reported the 30-character limit. No row was created. Created a valid activity type without a short name, confirming that field remains optional.
- Runtime update/read-back: submitted a 12-character short name; the editor retained it and displayed the 10-character limit while leaving the list row unchanged. Corrected the value to `TMPA`; the refreshed list showed the update under the same record ID (6).
- Cleanup/table: deleted only the newly created, unreferenced type. The success notice appeared and a fresh list showed the original six rows, with no temporary marker. Existing three column meanings/order remain unchanged. Browser page width was 1280px with no dialog left open.
- Checks: changed API contracts passed Ruby syntax inside the API image; changed Rails controller passed Ruby syntax and `zeitwerk:check`; scoped `git diff --check` passed. No tests or test files were added.
- Remaining: other Resources families and the broader B03 acceptance matrix remain open.

## 2026-09-30 — Enforce Building Type field lengths

- Finding: Building Type name and short-name columns are limited to 30 characters, but create/update contracts did not enforce the database bounds and the shared editor had no field-level feedback.
- Change: API create/update contracts enforce 30-character limits for both fields. The shared editor emits `maxlength=30` for Building Types, Subjects and Activity Types; Rails maps oversized Building Type values to specific Russian full-name/short-name errors while retaining the submitted editor draft.
- Contract path: shared catalog form → `Admin::Resources::PostsController` → `TeachersWorkspaceGateway` → API `POST/PATCH /admin/building_types` → Building Types contracts/actions → repository.
- Runtime failure: an overlength create retained the entered values in the reopened sheet, showed the 30-character name error and created no row. An overlength edit retained its draft and displayed the short-name-specific limit while the list row stayed unchanged.
- Runtime CRUD/read-back: created disposable Building Type ID 4, corrected the short name and read the update back under the same ID. Deleted only that record; a fresh list showed the original two rows and no temporary marker.
- Table and viewport: the existing three columns (`Название`, `Короткое название`, `Действия`) remain unchanged; no editor remained open after cleanup.
- Checks: changed API contracts passed Ruby syntax inside the API image; changed Rails controller passed Ruby syntax and `zeitwerk:check`; scoped `git diff --check` passed. No tests or test files were added.
- Remaining: other Resources families and the broader B03 acceptance matrix remain open.

## 2026-09-30 — Enforce Week Type field lengths

- Finding: Week Type `name` and `code` columns are limited to 20 and 50 characters, but create/update API contracts accepted longer values and the shared editor exposed no matching bounds.
- Change: API create/update contracts validate both database limits. The shared resource form emits `maxlength=20` for Week Type names and `maxlength=50` for codes. Rails returns field-specific Russian errors and preserves the failed create/edit draft.
- Contract path: shared catalog form → `Admin::Resources::PostsController` → `TeachersWorkspaceGateway` → API `POST/PATCH /admin/week_types` → Week Types contracts/actions → repository.
- Runtime failure: bypassed browser maxlength and submitted a 21-character name and 51-character code separately. Both were rejected with the matching field error; the create sheet retained all submitted fields and no row appeared. An overlength code edit retained its draft and left the list value unchanged.
- Runtime CRUD/read-back: created disposable Week Type ID 7, edited both fields, and reloaded to read back the changed name/code under the same ID. Deleted only that row; a fresh list showed the original six Week Types and no temporary marker.
- Table and viewport: the existing three columns (`Название`, `Код`, `Действия`) remain unchanged. At 1280px the document had no horizontal overflow and no editor remained open after cleanup.
- Checks: changed API contracts passed Ruby syntax inside the API image; changed Rails controller passed Ruby syntax and `zeitwerk:check`; scoped `git diff --check` passed. No tests or test files were added.
- Remaining: Posts, Academic Titles/Degrees and the broader B03 acceptance matrix remain open.

## 2026-09-30 — Enforce remaining name-catalog field lengths

- Finding: Posts columns allow 255-character names and 10-character short names; Academic Title and Degree name/short-name columns allow 50 characters. Their create/update contracts accepted longer strings and the shared editor did not consistently expose schema limits.
- Change: API create/update contracts now enforce those column bounds. Shared catalog fields emit matching `maxlength` values, and Rails returns resource/field-specific Russian errors while preserving rejected form drafts.
- Contract paths: shared catalog form → `Admin::Resources::PostsController` → `TeachersWorkspaceGateway` → the respective admin POST/PATCH routes, contracts/actions and repositories for Posts, Academic Titles and Academic Degrees.
- Runtime failure and CRUD/read-back: Posts rejected an 11-character short name, then a disposable record was created, edited and reloaded under the same ID. Academic Titles rejected a 51-character name, and Academic Degrees rejected a 51-character short name; each retained the submitted draft. A valid record was created, edited in place and read back after reload for each catalog.
- Cleanup: deleted only the exact disposable Posts, Academic Title and Academic Degree records. Fresh reads showed no temporary markers and retained the original catalog rows; no editor remained open.
- Table and checks: existing table column meanings/order were preserved. API contracts passed Ruby syntax; Rails controller passed Ruby syntax and `zeitwerk:check`; scoped `git diff --check` passed. Browser console errors and recent API `[ERROR]` log entries were zero. No tests or test files were added.
- Remaining: student-group acceptance, scoped-role denial and the broader B03 acceptance matrix remain open.

## 2026-09-30 — Preserve student-group numeric drafts and allow zero students

- Finding: the create controller converted every non-positive or malformed `students_now` value to `1`, and malformed semester duration to `18`, before API validation. That discarded the submitted value on failure. The browser form also required at least one student even though the API create contract allows `students_now >= 0`.
- Change: blank numeric inputs still use defaults, valid integers (including zero students) pass unchanged, and malformed values pass to API validation so the failed editor can retain them. The student-count input now uses `min=0`; create failure copy also names the numeric parameters.
- Contract path: student-group editor → `Admin::StudentGroupsController#create` → `TeachersWorkspaceGateway#create_student_group` → API `POST /admin/student_groups` → Student Groups create contract/action/repository.
- Runtime failure: bypassed the browser minimum and submitted `students_now=-1`. API validation rejected it before creating a group. The reopened sheet retained speciality, admission year, `-1`, semester duration and auto-provision selection.
- Runtime create/edit/read-back/cleanup: submitted a valid zero-student group with semester provisioning disabled, edited its admission year under the same record ID, reloaded to read it back, then deleted only that disposable group. The fresh list returned to its original single group; no schedule or group-semester records were created for the fixture.
- Table and viewport: existing three column meanings/order remain unchanged; at 1280px the page had no horizontal overflow. No editor remained open after cleanup.
- Checks: changed Rails controller passed Ruby syntax and `zeitwerk:check`; scoped `git diff --check` and browser console checks passed. No tests or test files were added.
- Remaining: the broader student-group acceptance matrix (including failed edit and blocked dependency feedback), scoped-role denial and cross-resource acceptance remain open.

## 2026-09-30 — Block destructive student-group deletion when dependencies exist

- Finding: both `student_group_semesters.group_id` and `weekday_transfers.student_group_id` used `ON DELETE CASCADE`. Deleting a group with memberships could therefore silently erase semester-scoped workload and schedule descendants; the UI's warning that dependencies block deletion did not match the database.
- Change: the API checks for group-semester memberships and group weekday transfers before deletion and returns HTTP 409 with a dependency error. Both foreign keys now use `ON DELETE RESTRICT` as a race-safe backstop; the API maps a concurrent FK rejection to the same 409. Rails translates that conflict into a specific dependency message rather than create-oriented generic copy.
- Runtime blocked-delete journey: created disposable group ID 1028 with semester provisioning enabled, which produced eight empty group-semester memberships. The confirmed delete returned to the list with “Группу нельзя удалить: к ней привязаны семестры, нагрузка или переносы.” and left the group row present. The precheck returned true for the existing group that has dependencies.
- Cleanup: there is no group-semester delete UI/API operation. Queried the exact fixture and confirmed it had zero curriculum streams and zero weekday transfers, removed only its eight empty group-semester links, then deleted group 1028 through the API. Fresh database counts for the group, memberships, streams and transfers were all zero; the original group remained the only row in the list.
- Race-safety verification: a database transaction inserted a temporary group and membership, attempted to delete the parent, observed PostgreSQL's FK violation, and rolled the transaction back. Both development and test schemas migrated; `structure.sql` records `RESTRICT` for both references.
- Table and checks: existing three group columns remain unchanged. API action/repository and migration passed Ruby syntax; Rails controller passed Ruby syntax and `zeitwerk:check`; Hanami app setup, scoped diff checks and browser console checks passed. No tests or test files were added.
- Remaining: failed student-group edit coverage, scoped-role denial and the broader cross-resource B03 matrix remain open.

## 2026-09-30 — Retain failed group-date and group-semester drafts without masking stored rows

- Finding: an invalid `year_of_admission` edit was retained in the Rails draft hash but rendered into an HTML date input, whose browser value became blank. Both student-group and group-semester tables also substituted rejected drafts into their data rows, making unsaved values look authoritative.
- Change: malformed admission-date drafts now render as visible text inputs with an ISO-date pattern and specific Russian validation feedback; valid dates keep the native date picker. Student-group and group-semester table cells now show only values from the latest API read while editor fields retain submitted drafts.
- Runtime failed-edit/read-back: group 1030 submitted `not-a-date`; the editor reopened with that exact text and a field-specific date message, while its table row continued to show stored date `2040-09-01`. Corrected the same record to `2041-09-01`, read it back after reload, then deleted only group 1030. The group list returned to its original single row.
- Runtime group-semester failure: submitted `students_now=-1` for group-semester ID 1 after bypassing the browser minimum. API validation returned 422; the editor retained `-1` and duration `18`, while the table continued to show stored values `1` and `18`. Reload discarded the rejected draft; no group-semester data changed.
- Table and viewport: student-group and group-semester column schemas remain unchanged. At 1280px the document had no horizontal overflow; no editor remained open after verification.
- Checks: changed Rails controller passed Ruby syntax and `zeitwerk:check`; the rebuilt runtime rendered and exercised both failure paths; scoped `git diff --check` and browser console checks passed. No tests or test files were added.
- Remaining: scoped-role denial and the broader cross-resource B03 matrix remain open.

## 2026-09-30 — Complete failed-edit recovery for remaining name catalogs

- Finding: Posts and Academic Titles/Degrees had server-side column limits and failed-create evidence, but their failed-update recovery paths had not been exercised in the browser.
- Runtime Posts edit: created disposable Post ID 3, bypassed `maxlength` and submitted a 256-character Cyrillic name. Rails returned the 255-character field message, reopened the same editor with all 256 characters, and kept the table at the stored `TMP должность` / `TMPCHK`. Corrected both fields on the same record, reloaded to read back `TMP должность edit` / `TMPEDT`, then deleted only ID 3.
- Runtime Academic Title edit: created disposable ID 3, submitted a 51-character Cyrillic short name, confirmed the specific 50-character error and retained draft while the table kept its original values. Corrected the same record, reloaded it, and deleted only ID 3.
- Runtime Academic Degree edit: created disposable ID 3, submitted a 51-character Cyrillic full name, confirmed the specific 50-character error and retained draft while the table kept its original values. Corrected the same record, reloaded it, and deleted only ID 3.
- Cleanup/table: fresh reads for all three catalogs showed their original rows and no temporary markers. Table columns and ordering did not change; no editor remained open.
- Checks: live create/edit/failure/reload/delete paths ran on the rebuilt Rails/API images; browser console errors were zero. No tests or test files were added.
- Remaining: scoped-role denial and any remaining cross-resource dependency/failure paths in the B03 acceptance matrix remain open.

## 2026-09-30 — Verify faculty-admin scope denial

- Runtime: created a disposable faculty-admin account scoped to the only configured faculty, signed in through an isolated browser tab, and requested `/admin/student_groups` directly.
- Result: the app redirected to the administrator schedule and displayed `Раздел доступен только главному администратору.`; no student-group table was exposed. The super-admin tab remained signed in.
- Cleanup/read-back: removed only the disposable account and its scope row after confirming the account UUID and role; a database read-back showed `super_admin | 1` and no other account role.
- Remaining: this verifies the protected Student Groups route. Other protected resource routes and broader cross-resource acceptance remain open.

## 2026-09-30 — Verify failed Subjects edit recovery

- Runtime: created disposable Subject records, searched by their marker, then retained one exact fixture (ID 5612) for the failure path. The Subjects view caps its unfiltered list at 50 rows, so newer rows are not guaranteed to appear in that list even when the query is retained.
- Failure: removed the browser `maxlength` guard only in the disposable editor and submitted a 51-character full name. The server rejected it with `Полное название дисциплины должно содержать не более 50 символов.`, kept all 51 submitted characters in the reopened editor, and the authoritative row remained valid at 50 characters.
- Recovery: corrected that same record under ID 5612 to the original marker values. Database read-back confirmed the corrected name/short-name pair. The API-backed list search did not expose this newest row during the session, so read-back used the authoritative database rather than treating the empty search result as proof of absence.
- Cleanup: confirmed zero `curriculum_streams` references for the exact disposable Subject IDs, deleted them through the Rails resource route, and verified zero matching Subject rows and zero references in the database.
- Checks: browser console errors remained zero; no tests or test files were added.
- Remaining: complete the other resource-family dependency/failure paths required for B03.

## 2026-09-30 — Prevent deletion of Rooms with dependent data

- Finding: Rooms can be referenced by assignments, schedule events, event-room links, event transfers, reservations, availability rows, and map rows. Several foreign keys use `ON DELETE CASCADE`, so relying on a later restrictive-FK error can still delete unrelated scheduling data.
- Change: `RoomRepo#delete_with_dependency_check` locks the room row, checks every room-reference table inside the same transaction, and only deletes when all are empty. The Rooms DELETE action returns 409 with dependency counts when blocked and retains a 409 fallback for any concurrent/unexpected foreign-key rejection. The existing Rails gateway maps 409 to its localized dependency message.
- Runtime: attempted deletion of existing room ID 1, which had 3 assignment references, 2 dated-transfer references, 6 reservations, and 4 schedule events. The administrator saw `Аудитория используется и не может быть изменена таким образом.`, and the row remained in the list.
- Authoritative read-back: all seven dependency counts for room ID 1 were identical before and after the request; the room row remained present. This proves no schedule, assignment, transfer, reservation, availability, or map dependency was removed by the attempted deletion.
- Checks: API image rebuilt and healthy; both changed Ruby files passed syntax checks inside the running image; browser console errors were zero. No tests or test files were added.
- Remaining: continue cross-resource B03 acceptance for other dependent entities and remaining failure paths.

## 2026-09-30 — Prevent deletion of Room Types with dependent rooms

- Finding: the Room Type foreign key from Rooms is `ON DELETE CASCADE`; deleting a type with Rooms would silently delete the rooms and their schedule relationships.
- Change: `RoomTypeRepo#delete_with_dependency_check` locks the type row, checks for Rooms in the same transaction, and deletes only when none remain. The API returns 409 with the blocking count otherwise; the existing Rails route translates the conflict into a localized message. A foreign-key conflict remains a 409 fallback.
- Runtime: attempted to delete existing Room Type ID 1, which has one Room. The administrator saw `Тип аудитории используется и не может быть изменён таким образом.`, and the type remained listed.
- Authoritative read-back: Room Type ID 1 and its one associated Room both remained present after the rejected request.
- Checks: API image rebuilt and healthy; both changed Ruby files passed syntax checks; browser console errors were zero. No tests or test files were added.
- Remaining: audit and protect other resource families whose foreign keys cascade into business data.

## 2026-09-30 — Prevent deletion of Building Types with dependent buildings

- Finding: Buildings reference Building Types with `ON DELETE CASCADE`, and each Building may own Rooms. Deleting a used Building Type can therefore erase physical-space and schedule data through multiple cascade levels.
- Change: `BuildingTypeRepo#delete_with_dependency_check` locks the type row, counts Buildings inside the same transaction, and deletes only when no Buildings reference it. The API reports 409 with the dependent count; Rails now gives a type-specific Russian message. A foreign-key conflict remains a 409 fallback.
- Runtime: attempted deletion of existing Building Type ID 1 with one Building. The administrator saw `Тип здания нельзя удалить, пока к нему привязаны здания.`, and the type remained listed.
- Authoritative read-back: the Building Type and its Building both remained present after the rejected request.
- Checks: API and Rails images rebuilt; changed Ruby files passed syntax checks; Rails `zeitwerk:check`, Hanami route loading, and browser console checks passed. No tests or test files were added.
- Remaining: audit and protect other resource families whose foreign keys cascade into business data.

## 2026-09-30 — Protect activity and teacher catalogs from cascade deletion

- Finding: deleting an Activity Type cascades to activity-period rules, Room Types and teaching-load requirements. Deleting a Post, Academic Title or Academic Degree cascades to Teachers through their corresponding catalog foreign keys.
- Change: each repository now locks the catalog row, counts all direct business dependencies in one transaction, and deletes only when there are none. The API returns a 409 with dependency counts when blocked and catches concurrent/unexpected foreign-key conflicts as 409. The shared Rails catalog controller shows resource-specific Russian messages for these delete conflicts.
- Runtime: attempted deletion of Activity Type ID 1 (1 period rule, 1 Room Type, 5 teaching-load requirements), Post ID 1 (2 Teachers), Academic Title ID 1 (2 Teachers), and Academic Degree ID 1 (2 Teachers). Each UI request was refused with a specific message and each record stayed listed.
- Authoritative read-back: all 13 dependent rows remained present after the four rejected requests.
- Checks: API and Rails images rebuilt; changed Ruby files passed syntax checks; Rails `zeitwerk:check`, Hanami route loading, and browser console checks passed. No tests or test files were added.
- Remaining: continue protecting other cascade roots and finish the broader B03 acceptance matrix.

## 2026-09-30 — Prevent deletion of Buildings with dependent rooms or map rows

- Finding: Rooms reference Buildings with `ON DELETE CASCADE`; map-building references use `ON DELETE SET NULL`. Deleting a used building could remove Rooms and their scheduling data or silently detach map data.
- Change: `BuildingRepo#delete_with_dependency_check` locks the Building, checks both Rooms and map-building rows in the same transaction, and deletes only when both sets are empty. The API reports 409 with dependency counts for blocked deletes and uses a 409 fallback for concurrent/unexpected FK conflicts. The existing Rails controller maps conflict to its localized in-use message.
- Runtime: attempted deletion of Building ID 1 with one Room. The administrator saw `Здание используется и не может быть изменено таким образом.`, and the Building remained listed.
- Authoritative read-back: Building ID 1 and its Room remained present after the rejected request.
- Checks: API image rebuilt; changed Ruby files passed syntax checks; Hanami route loading and browser console checks passed. No tests or test files were added.
- Remaining: continue protecting other cascade roots and finish the broader B03 acceptance matrix.

## 2026-09-30 — Prevent deletion of Week Types and Time Slots used by scheduling data

- Finding: deleting a Week Type cascades to schedule events and teacher constraints. Deleting a Time Slot cascades to schedule events, room reservations and teacher constraints; dated transfers also reference Time Slots.
- Change: both repositories now lock their parent row and count every direct schedule/reference dependency inside one transaction. They delete only when the dependency set is empty, return 409 with counts when blocked, and map concurrent/unexpected foreign-key violations to 409. The shared Rails catalog controller now explains the specific Week Type and Time Slot dependencies in Russian.
- Runtime: attempted deletion of Week Type ID 6 (`Общая`) with seven events and six teacher constraints; attempted deletion of Time Slot ID 1 with three events, three reservations and six teacher constraints. Both requests were refused with specific messages, and both rows remained listed.
- Authoritative read-back: the same counts remained after the rejected requests: Week Type 6 retained seven events and six teacher constraints; Time Slot 1 retained three events, three reservations, six teacher constraints and one dated-transfer reference.
- Checks: API and Rails images rebuilt; changed Ruby files passed syntax checks; Hanami route loading, Rails `zeitwerk:check`, and browser console checks passed. No tests or test files were added.
- Remaining: continue protecting other cascade roots and finish the broader B03 acceptance matrix.

## 2026-09-30 — Protect Faculty, Department and Specialty dependencies

- Finding: deleting a Faculty cascades to account scopes, Departments and Specialties, and schedule-generation runs have a restrictive FK; deleting a Department cascades to account scopes, curriculum streams and teacher memberships; deleting a Specialty cascades to student groups.
- Change: each repository locks its parent row, checks its complete direct dependency set in the same transaction, and deletes only when empty. The API returns 409 with dependency counts for blockers and catches foreign-key races as 409. The Academic Catalogs controller now uses specific Russian dependency messages.
- Runtime: attempted deletion of Faculty ID 1 (one Department, one Specialty and 31 schedule-generation runs), Department ID 1 (11 curriculum streams and one teacher membership), and Specialty ID 1 (one student group). Each request was refused and each record stayed listed.
- API wiring correction: the Specialty destroy action referenced a missing `contracts.specialities.destroy_contract`, although the existing contract was named `delete_contract`. Corrected the action to use that contract; the next request returned the intended 409 and localized dependency message instead of a generic API failure.
- Authoritative read-back: Faculty, Department, Specialty, their dependent rows, and the current account-scope counts were unchanged after the rejected requests. API logs showed no new errors after the wiring correction.
- Checks: API and Rails images rebuilt; changed Ruby files passed syntax checks; Rails `zeitwerk:check`, Hanami route loading and browser console checks passed. No tests or test files were added.
- Remaining: continue protecting other cascade roots and finish the broader B03 acceptance matrix.

## 2026-09-30 — Guard Semester, Group Semester and Curriculum Stream cascade paths

- Finding: deleting a Semester cascades to Group Semesters and teacher constraints, while nulling Excel-file context; it can also conflict with schedule-generation runs and teacher wishes. Deleting a Group Semester cascades to Curriculum Streams and period records. Deleting a Curriculum Stream cascades to workload requirements, then teaching assignments and schedule events.
- Change: the three API repositories now lock their parent row and check every direct dependency in the same transaction. They delete only when empty, return 409 with dependency counts when blocked, and map FK races to 409. The intentional bulk “clear all streams for this Group Semester” operation is unchanged; this guard protects the direct per-stream DELETE endpoint.
- Runtime evidence: in the running Hanami application, `delete_with_dependency_check` returned `blocked` for Semester ID 1 (1 Excel file, 50 generation runs, 1 Group Semester, 6 teacher constraints), Group Semester ID 1 (11 Curriculum Streams, 1 period), and Curriculum Stream ID 2 (1 workload requirement). The paths are API-only; the Rails administrator currently exposes no matching delete controls.
- Read-back: these checks are non-mutating; authoritative DB counts remained unchanged for the referenced rows after execution.
- Checks: API image rebuilt; all six changed Ruby files passed syntax checks; Hanami loaded the API routes. No tests or test files were added.
- Remaining: continue auditing other cascade roots and complete the broader B03 acceptance matrix.

## 2026-09-30 — Keep workload-delete cascade preview consistent

- Finding: deleting a Workload Requirement intentionally cascades to teaching assignments, room references, scheduled events and event-teacher rows. The existing UI explicitly asks for confirmation, but the API collected its cascade snapshot before opening the delete transaction. A concurrent child insert could therefore be absent from the reported snapshot even though the database removed that row.
- Change: `StudyLoadRequirementRepo#delete_with_snapshot` now locks the requirement row with `FOR UPDATE`, hydrates the snapshot, reads all cascading child IDs and deletes the requirement in one transaction. PostgreSQL's parent-row lock serializes FK-backed child creation against this cascade, making the returned preview/audit snapshot agree with the deleted graph.
- Checks: changed API file passed `ruby -c` and `git diff --check`; the running API container passed the same syntax check and loaded Hanami routes. No test files were added.
- Remaining: continue auditing other cascade roots and complete the broader B03 acceptance matrix.

## 2026-09-30 — Block Subject deletion while curriculum streams use it

- Finding: direct Subject deletion cascaded to Curriculum Streams, then workload requirements, assignments and scheduled lessons. The shared Rails confirmation also described every resource as a teacher reference, which was misleading for Subjects.
- Change: `SubjectRepo#delete_with_dependency_check` locks the Subject, counts linked Curriculum Streams and deletes only when none exist. The API returns 409 with the dependency count when blocked and catches an FK race as a conflict. Rails now explains the Curriculum Stream dependency and uses a Subject-specific confirmation.
- Runtime: attempted to delete Subject ID 5342 (`авто`) after its five Curriculum Streams were confirmed in PostgreSQL. The administrator saw `Дисциплину нельзя удалить, пока она включена в учебные потоки.`, and the Subject stayed in the list.
- Read-back: Subject ID 5342 and all five Curriculum Streams remained present after the rejected request.
- Checks: API and Rails images rebuilt; changed Ruby files passed syntax checks in their containers; Hanami route loading succeeded; `git diff --check` passed; no new tests or test files were added.
- Remaining: continue auditing other cascade roots and complete the broader B03 acceptance matrix.

## 2026-09-30 — Protect Teacher records and their scheduling graph

- Finding: deleting a Teacher cascades to department memberships, which can then remove teaching assignments and scheduled event-teacher rows; it also cascades to time constraints and room reservations. Schedule wishes and notice-export files restrict deletion, while linked accounts would be silently detached.
- Change: `TeacherRepo#delete_with_dependency_check` locks the Teacher and counts memberships, time constraints, reservations, schedule wishes, notice exports and linked accounts in one transaction. It deletes only when all are absent. The API returns 409 with per-type counts when blocked and catches FK races as 409.
- Runtime: the repository operation for Teacher ID 1 returned `blocked` with one membership, six time constraints, six room reservations and four notice-export files.
- Read-back: Teacher ID 1 and the same dependent-row counts remained in PostgreSQL after the non-mutating check.
- Checks: API image rebuilt; changed Ruby files passed syntax checks in the running container; Hanami route loading and `git diff --check` passed. No tests or test files were added. Rails currently exposes no Teacher deletion control.
- Remaining: continue auditing other cascade roots and complete the broader B03 acceptance matrix.

## 2026-09-30 — Guard Room Availability Type deletion

- Finding: the API's direct Aviability Type DELETE cascades to every Room Availability row using that type. Rails currently has no Aviability Type management view.
- Change: `AviabilityTypeRepo#delete_with_dependency_check` locks the type, counts Room Availability references in the transaction, and deletes only when unused. The API returns 409 with dependency counts for blocked deletes and a conflict fallback for FK races.
- Runtime: repository check for a nonexistent ID returned `missing` without mutation. Current database read-back shows 13 availability types and no Room Availability rows, so there is no populated record against which to exercise the blocked branch safely.
- Checks: API image rebuilt; changed Ruby files passed syntax checks; Hanami route loading, Rails `zeitwerk:check`, and `git diff --check` passed. No tests or test files were added.
- Remaining: continue auditing the remaining cascade roots and complete the broader B03 acceptance matrix.

## 2026-09-30 — Preserve uploads when deleting an account

- Finding: `DELETE /auth/accounts/:id` cascades to account scopes as expected, but also cascades to Excel and media file metadata owned by that account. Media objects live in external storage, so dropping their rows through account deletion can orphan objects and destroy file history.
- Change: `AccountRepo#delete_with_upload_guard` locks the account, counts its Excel and media uploads in one transaction, and deletes only when both counts are zero. The API returns 409 with dependency counts when blocked, 404 for missing IDs, and 409 for an FK race. Account scopes continue to cascade with the explicitly deleted account.
- Runtime: the repository operation found an account owning one Excel upload and returned `blocked`. Read-back before and after remained `[1 Excel file, 0 media files]` for that owner.
- Checks: API image rebuilt; changed Ruby files passed syntax checks; Hanami routes loaded. The Rails administrator currently has no account-delete UI, so verification was performed through the API repository path without deleting the account.
- Remaining: finish the cascade-root inventory, then continue remaining B03 acceptance work.

## 2026-09-30 — Make bulk group-load deletion snapshots atomic

- Finding: `DELETE /admin/student_group_semesters/:id/load` read curriculum streams and their nested workload graph before opening the deletion transaction. Concurrent stream, requirement, assignment, room-reference or event inserts could therefore be absent from the response snapshot while still being removed by the cascade.
- Change: `CurriculumStreamRepo#delete_for_group_semester` now locks the Group Semester, all its streams, their requirements and assignments, plus existing room references and schedule events before taking the snapshot and deleting the streams in the same transaction. Existing bulk-delete behavior and authorization are unchanged.
- Runtime: exercised Group Semester ID 1's 11-stream deletion inside an outer rollback transaction. The returned snapshot contained 11 streams; stream, requirement, assignment, room-reference and event counts were `[11, 7, 7, 3, 11]` both before and after rollback.
- Checks: API image rebuilt; changed Ruby file passed syntax check; Hanami routes loaded. No tests or test files were added.
- Remaining: finish the cascade-root inventory, then continue remaining B03 acceptance work.

## 2026-09-30 — Verify the Subjects CRUD and safe validation journey

- Runtime: using the authenticated administrator UI, confirmed a unique disposable Subject name was absent, created it, edited its name, and reloaded the page. Hanami read-back matched the edited full and short names. A 51-character Playwright fill was capped by the input's `maxlength`; PostgreSQL confirmed the stored value was 50 characters.
- Failure retention: attempting to create with the required full name blank left the create editor open and retained its short-name draft. Attempting to edit with the required name blank left the edit editor open and retained that draft; PostgreSQL still held the original edited Subject value. Both unsaved drafts were explicitly discarded.
- Cleanup: deleted the disposable Subject through its confirmation. Authoritative read-back found zero Subject rows with its unique short name and zero linked Curriculum Streams.
- Checks: browser console errors were zero; API and Rails services remained healthy. No tests or test files were added.
- Remaining: repeat the CRUD/read-back and failure-retention journey for other required resource families, then complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Activity Type CRUD and correct catalog delete copy

- Runtime: created a unique unused Activity Type through the admin sheet, edited its name, and reloaded the list. Hanami read-back matched the edited name and code. Before deletion, its period-rule, Room Type and workload-requirement counts were all zero; after the confirmed delete, the record was absent.
- UX correction: the shared catalog confirmation claimed all records might be assigned to teachers. Activity Types are referenced by period rules, Room Types and workload requirements, so the fallback copy now accurately says that linked data can block deletion. The tailored Subject confirmation remains unchanged.
- Checks: Rails image rebuilt; Rails `zeitwerk:check` passed; API remained healthy; browser console errors were zero. No test records remain and no tests or test files were added.
- Remaining: repeat CRUD/read-back and failure-retention journeys for other required resource families, then complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Rooms CRUD, relationship selection and failure retention

- Runtime: in the authenticated admin, searched and selected the existing Building and Room Type from their bounded radio lists, created a disposable Room with capacity 12, edited its name and capacity to 14, then reloaded the page. Hanami read-back matched the number, name, capacity, building ID and room-type ID.
- Failure retention: submitting the create sheet without selecting its required Building and Room Type left the sheet open with number, name and capacity draft values intact. Editing capacity to zero was blocked by native validation; the edit stayed staged and the persisted capacity remained 14. The invalid draft was explicitly discarded.
- Cleanup: all seven Room dependency counts (assignment references, event-room links, dated-transfer references, map rows, availability rows, reservations and schedule events) were zero before the confirmed delete. Read-back confirmed the disposable Room was removed.
- Checks: Rails `zeitwerk:check` passed; Hanami routes loaded; browser console errors were zero; API and Rails services remained healthy. No table schema changed and no tests or test files were added.
- Remaining: repeat CRUD/read-back and failure-retention journeys for other required resource families, then complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Building Type CRUD and safe cleanup

- Runtime: the authenticated administrator created a unique disposable Building Type, edited its full name, and reloaded the catalog. Hanami read-back matched the edited full name and short code.
- Failure retention: submitting create and edit sheets with the required full name blank kept each editor open and retained the short code. The invalid edit left the persisted name unchanged; both drafts were explicitly discarded.
- Cleanup: verified the Building Type had no Buildings, deleted it through the confirmation, and read back that the record no longer existed.
- Checks: Rails `zeitwerk:check` passed; Hanami routes loaded; browser console errors were zero; services remained healthy. No tests or test files were added.
- Remaining: continue the CRUD/read-back and failure-retention journeys for other required resource families and complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Buildings CRUD and relationship selection

- Runtime: the authenticated administrator opened the searchable Building Type list, submitted a draft without selecting its required type, then selected `корпус` and created Building 30926. Hanami read-back confirmed the foreign key and number. Edited the number to 30927 and confirmed it persisted after reloading the list.
- Cleanup: checked that the disposable Building had zero Rooms and zero map-building rows, deleted it through the UI confirmation, and confirmed its ID was absent in Hanami read-back.
- Checks: browser console errors were zero; services remained healthy. No tests or test files were added.
- Remaining: continue the CRUD/read-back and failure-retention journeys for other required resource families and complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Room Type CRUD and relationship selection

- Runtime: in the authenticated administrator, opened the searchable Activity Type list, submitted a named draft without selecting its required Activity Type, and confirmed the editor retained the name. Selected `Лекция`, created a disposable Room Type, edited its name, and reloaded the list. Hanami read-back matched its Activity Type ID and edited name.
- Failure retention: cleared the required name in the edit sheet and submitted; the editor stayed open with the blank draft while the persisted name remained unchanged. Explicitly discarded the draft.
- Cleanup: checked the Room dependency count was zero, deleted the disposable Room Type through its confirmation, and confirmed its ID was absent from Hanami read-back.
- Checks: browser console errors were zero; services remained healthy. No tests or test files were added.
- Remaining: continue CRUD/read-back and failure-retention journeys for other required resource families and complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Student Group CRUD without semester provisioning

- Runtime: created a disposable Group for the existing searchable Specialty, explicitly unchecked automatic semester provisioning, and confirmed Hanami stored the Group while creating zero Group Semesters. Edited its admission date and reloaded the list; read-back matched the edited value.
- Failure retention: submitting an empty admission date kept the editor open with its draft while the database retained the original date. The valid edit was then saved through the UI.
- Cleanup: confirmed zero Group Semesters before deletion, deleted the empty disposable Group through its confirmation, and verified both Group and Group Semester read-backs returned zero rows for the test ID.
- Checks: browser console errors were zero; services remained healthy. No tests or test files were added.
- Remaining: continue CRUD/read-back and failure-retention journeys for other required resource families and complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Time Slot CRUD and invalid-time retention

- Runtime: the list retained the existing two-column schema (displayed time and period number), while the editor exposed all three fields. Created unused period 6, edited it, and reloaded the list; Hanami read-back matched `18:05–18:45`.
- Failure retention: an invalid create with end before start kept period number and both times in the open editor. An invalid edit was rejected with localized feedback and retained the attempted start time; Hanami confirmed the stored slot remained `18:05–18:45`. Explicitly discarded the invalid draft.
- Cleanup: confirmed all four time-slot link families (events, teacher constraints, room reservations and event transfers) had zero references to the disposable ID, then deleted it through the UI. Hanami read-back found no row with that ID.
- Checks: browser console errors were zero; services remained healthy. No tests or test files were added.
- Remaining: continue CRUD/read-back and failure-retention journeys for other required resource families and complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify Week Type CRUD and failure retention

- Runtime: the authenticated administrator submitted a code-only draft and the editor retained its code when the required name was missing. Created a disposable Week Type, corrected the name to stay within the input's maximum length, edited it and reloaded the catalog. Hanami read-back matched the edited name and code.
- Failure retention: clearing the required name in the edit sheet kept it open with the code intact; Hanami confirmed the saved name and code were unchanged. Explicitly discarded the draft.
- Cleanup: checked both discovered Week Type references (schedule events and teacher time constraints) were zero, deleted the disposable type through the UI confirmation, and confirmed its ID was absent in Hanami read-back.
- Checks: browser console errors were zero. No tests or test files were added.
- Remaining: continue CRUD/read-back and failure-retention journeys for other required resource families and complete the wider B03 acceptance matrix.

## 2026-09-30 — Verify period failure retention and Calendar-to-Schedule scope

- Runtime: selected Faculty 1, Semester 1 and Group 1 in Calendar Periods. Submitting a lecture-week range with end before start returned the Russian field error and retained both entered dates in the correct period editor. Hanami read-back for Group Semester 1 remained unchanged with only its original semester period; no lecture-week row was created.
- Context: the failure response and subsequent same-context reload retained the selected Faculty/Semester/Group. The linked Schedule opened Semester 1, Faculty 1 and Group 1 with the existing lesson rows intact.
- Narrow table: at 390px, document width equalled viewport width (390px); the explicitly labelled timetable region was 360px wide with 780px scroll width, keeping horizontal scrolling within the table region. Browser console reported zero errors.
- Draft cleanup: reloaded the same scoped Calendar URL to explicitly discard the invalid lecture-week draft; stored dates remained unchanged. Table schemas were not changed; no tests or test files were added.
- Remaining: continue the outstanding B04 Calendar and B05/B06 acceptance gates, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Verify Holiday create, validation and cleanup

- Runtime: on the scoped Calendar Holidays page, submitting a named draft without its required date kept the dialog open and retained the name. Created a disposable holiday for the previously unused date 2099-12-31 and confirmed it appeared after reloading the same scoped page.
- Cleanup: deleted the exact disposable row through its confirmation. Hanami read-back found zero rows for both its ID and date; the existing holiday row remained.
- Checks: browser console errors were zero. Holiday table columns were unchanged; no tests or test files were added.
- Remaining: continue the outstanding B04 Calendar and B05/B06 acceptance gates, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Verify weekday-transfer scope and staged form

- Runtime: opened weekday transfers with Semester 1 and Group Semester 1. The group-specific scope radio was selected; “All groups” remained unselected. Source tracing confirmed this page expects `group_semester_id` for context and resolves it to the Student Group ID for the transfer write.
- Form: the add editor exposed the date, following weekday and reason fields, with the selected group carried into the staged mutation. Closed without saving; no transfer data changed. The existing five-column transfer table remained empty.
- Remaining: verify successful weekday-transfer CRUD and the remaining B04/B05/B06 acceptance gates, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Verify weekday-transfer create, read-back and cleanup

- Runtime: confirmed 2026-10-19 had no weekday transfers, then created a Group 1 transfer through the scoped Semester 1 UI with weekday Tuesday and a unique QA reason. The page displayed the expected date, weekday, group and reason.
- Persistence and cleanup: Hanami read-back matched the transfer fields. Deleted that exact row through the UI confirmation; the page returned to its empty state and database read-back confirmed zero matching rows.
- Checks: browser console errors were zero; no tests or test files were added.
- Remaining: verify dated lesson-transfer acceptance and the remaining B04/B05/B06 gates, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Verify dated lesson transfer, conflict preview and undo

- Runtime: opened the two-date transfer workspace for Group Semester 1 on 2026-10-12 and 2026-10-19. Selecting event 8 and previewing its batch transfer to the same period on the second date exposed the occupied-cell conflict (“Проектная” already exists there); the staged batch was closed without saving, and Hanami confirmed no transfer row was created.
- Create/read-back: moved that dated occurrence from 2026-10-12, period 2 to the verified free period 4 on 2026-10-19 through the single-transfer editor. The UI displayed “Перенесено с 2026-10-12”; Hanami read-back matched event ID 8, source date, target date, target period and the unique QA reason.
- Undo: used the moved occurrence's “Вернуть” action and confirmed it. The original dated occurrence reappeared, the target card disappeared, and Hanami confirmed the temporary transfer row was absent. The recurring schedule event remained unchanged at weekday 1, period 2.
- Checks: browser console errors were zero; no tests or test files were added.
- Remaining: complete the outstanding B04 acceptance matrix and B05/B06 gates, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Verify current narrow Accounts and Teachers tables

- Accounts: at 320px, the existing six-column table remained inside its labelled, focusable region (286px viewport, 940px content width). One ArrowRight moved the region to `scrollLeft=229`; the document remained 320px wide.
- Teachers: searched and explicitly selected a teacher, then inspected the existing seven-column availability matrix without changing constraints. At 390px and 320px, the labelled matrix region contained the 900px table (356px and 286px wide respectively), document width matched the viewport, and ArrowRight advanced the region by 43px at 390px.
- Checks: browser console errors were zero; Accounts and Teachers data were not mutated. No tests or test files were added.
- Remaining: finish B04/B05/B06 gates, including Notice print and scoped-role coverage where fixtures permit, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Label and keyboard-enable the Notice report table

- Finding: at 390px the 760px Notice report table stayed inside a local overflow wrapper, but that wrapper had no accessible name and could not receive keyboard focus.
- Change: added the Russian labelled region and `tabindex="0"` to the Notice table wrapper, plus a scoped `:focus-visible` outline. Existing five table columns, their order, and print rules are unchanged.
- Runtime: rebuilt `schedule_web` and reloaded a 143-row teacher report. At 390px the named region measured 360px with 760px content; at 320px it measured 290px with the same content width. ArrowRight scrolled it 43px at both widths while the document stayed within the viewport, and the focus-visible outline was present.
- Print stylesheet: print-media emulation hid the sidebar and screen-only controls, removed the minimum table width, kept all five headers and 143 rows, set the header to `table-header-group`, rows to `break-inside: avoid`, and overflow to visible. This confirms print CSS but does not verify actual PDF pagination or blank trailing pages.
- Checks: Rails rebuilt and remained healthy; `git diff --check` passed for the edited Notice files. Browser errors were zero; one existing application CSS preload warning appeared. No tests or test files were added.
- Remaining: verify actual multipage PDF output, finish B04/B05/B06 gates including scoped-role coverage where fixtures permit, then rerun the full workload-to-schedule journey after shared behavior changes.

## 2026-09-30 — Recheck Notice PDF and scoped-role prerequisites

- Notice: Semester 1 has 143 rows for the selected teacher, but its only configured group-semester period is `semester`; there are no `lecture_week` or `exam_session` period rows. Both PDF-capable report views therefore show “Период не настроен” and disable “Скачать PDF”. No export job was queued and no calendar period was changed.
- Export lifecycle: PDF jobs are durable and write files to object storage; the app exposes no user-facing job/file deletion flow. Actual multipage output remains pending a populated export-period fixture and cleanup plan.
- Accounts: authoritative role/status aggregate contains one active `super_admin` and no scoped administrator accounts. Scoped-role authorization coverage therefore remains pending a suitable fixture; no account was created or changed.
- Remaining: verify real Notice PDF pagination when a removable fixture is available, complete scoped-role coverage when a suitable account fixture exists, then finish B04/B05/B06 and rerun the full workload-to-schedule journey.

## 2026-09-30 — Recheck Notice report at narrow width

- Runtime: the Semester 1 Notice report retained all 143 rows and all five columns at a 640px viewport; the document remained 640px wide and the 760px table stayed inside its 610px labelled keyboard-scroll region.
- Zoom: browser key input did not change browser zoom (`innerWidth` stayed 1280px and `devicePixelRatio` stayed 1). The 640px viewport check is not a substitute for the required 200% browser-zoom check; that acceptance remains open.
- Remaining: verify true 200% zoom and real multipage PDF output, finish scoped-role coverage when a suitable fixture exists, then complete B04/B05/B06 and rerun the full workload-to-schedule journey.

## 2026-09-30 — Visually inspect production Notice PDF pagination

- Runtime: rendered a 143-row synthetic Notice report through the production `PdfRenderer`; Ghostscript reported five A4 pages. A 65-dpi contact sheet of the generated PDF showed the original five-column header repeated on pages 2–5, rows continuing on every page, and the final report rows on page 5 without a blank trailing page.
- Runtime source: the running API container's renderer SHA-256 matched the worktree (`e942a89727c8b419bf2c963a62930e8d05aed8c3ac8e85a28f5bf6fa006d7e83`).
- Isolation: the report content was synthetic. The PDF and page images were created under `/tmp`, visually inspected, then removed from both host and API container. No export job, object-storage file, or schedule/calendar data changed.
- Scope: renderer pagination and repeated-header behavior are runtime-verified. The authenticated download/queue path remains unverified because the live semester has no configured PDF-export period and the app has no user-facing export deletion flow.
- Remaining: exercise the UI export path with a removable configured-period fixture, verify true 200% browser zoom, finish scoped-role coverage when a suitable fixture exists, then complete B04/B05/B06 and rerun the full workload-to-schedule journey.

## 2026-09-30 — Exercise the production Notice PDF renderer in memory

- Runtime: called the production `PdfRenderer` directly with an in-memory, synthetic report containing 143 rows (matching the live report row count and field shape). Ghostscript parsed the generated PDF and reported five pages; the PDF contained 2,351,197 bytes.
- Isolation: the renderer and verification used temporary files only; no Notice export job, object-storage artifact or calendar-period mutation was created. Temporary files were removed when the command completed.
- Scope: this verifies the PDF renderer can paginate a large report, but not the authenticated queue/download flow, repeated header presence in the resulting PDF, or absence of a blank trailing page. The live semester still has no configured lecture-week or exam-session period.
- Remaining: verify the UI export flow and final PDF page contents with a suitable removable report fixture, verify true 200% zoom, finish scoped-role coverage when a suitable fixture exists, then complete B04/B05/B06 and rerun the full workload-to-schedule journey.

## 2026-09-30 — Verify representative Russian teacher wishes in the running compiler

- Runtime identity: the scheduler container's `preference_compiler.py` SHA-256 matched the worktree (`ad33a8a4663830a110c93003a9aca1fec99732f770c0b422402895ccc9f24f5f`).
- Inputs and compiled output: “Хочу 2 пары подряд, потому что печка включена” produced a proposed soft `consecutive_lessons` rule scoped to the unique lab requirement; “Не могу в понедельник 1–2 пары” produced a proposed soft Monday `unavailable_slot` for periods 1 and 2; a room-software request produced no rule and an `UNSUPPORTED_ROOM_CAPABILITY` review finding.
- Ambiguity: the heater/consecutive-pairs wish with two plausible lab requirements produced only `AMBIGUOUS_PREFERENCE` for administrator review; the compiler did not guess a subject. These were direct in-memory calls inside the running scheduler container; no wish, generation run or timetable data changed, and no tests were added.
- Remaining: broaden natural-language coverage only through explicit user examples and preserve the review boundary; finish B04/B05/B06 acceptance and the final workload-to-schedule journey.

## 2026-09-30 — Read the shared Jev discussion and align the architecture record

- The supplied share page's server-rendered HTML contained the conversation payload even though the browser and public-web reader did not expose its transcript. The conversation's core recommendation is a hybrid: hard feasibility and arithmetic stay deterministic; a constraint solver builds valid schedules; an optional typed-decision model may rank bounded feasible alternatives; final validation and publication remain authoritative.
- The architecture draft now records that recommendation and maps it to the implementation: one-time natural-language preference compilation into a narrow, grounded, reviewed IR; local CP-SAT scheduling over immutable snapshots; isolated proposals with visible progress; conflict analysis; and explicit transactional publication. It also distinguishes the wish parser from an optional Jev-style candidate-ranking adapter.
- Local Jev is not represented as an available dependency: the existing technical review records no documented downloadable Jev runtime, and the tested small local Russian model failed the frozen preference corpus. The deterministic compiler and CP-SAT remain the dependable path; any model-guidance experiment must stay optional, shadowable, and unable to relax constraints.
- The user's scope-view answer is verified in the runtime: every active group receives a blank grid even with no lessons. The previous large synthetic roster check rendered 1,001 group grids, including 1,000 empty groups; all fixture rows were removed and read back as zero.
- No timetable or account data changed. No tests or test files were added.

## 2026-09-30 — Verify room reservation lifecycle and occupancy overlay

- Finding: the reservation workbench's date occupancy panel called the room schedule endpoint, which returns lesson rows but omits active room reservations. This made an already booked room appear free. The date panel now uses the authenticated occupancy endpoint, which merges date-resolved lessons and active reservations; the separate weekly lesson schedule gateway keeps its existing contract.
- Runtime: room 173 was inspected on disposable date 2099-12-30. Creating a reservation made it appear in both the reservation table and the occupancy timeline with matching slot, teacher and purpose. After a second reservation occupied another slot, moving the first into that slot was rejected; its saved row remained unchanged and the edit draft stayed available. Moving it back to a free slot and changing its purpose succeeded and was confirmed after reload.
- Failure preservation: a duplicate room/date/slot create was rejected while retaining date, slot, purpose and the readable selected teacher. The failure form no longer adds a redundant generic teacher option when the chosen teacher is already in search results.
- Cleanup: all disposable reservations were deleted through the UI. The occupancy panel returned to “Записей: 0” and its explicit empty state. No lesson or calendar data changed.
- Checks: Rails gateway and controller syntax checks passed in the running container; `git diff --check` passed for the three edited Rails files; the web and API services remained healthy. No tests or test files were added.
- Remaining: this closes the reservation occupancy and failure-preservation slice, not all of B04. Continue the remaining B04/B05/B06 acceptance gates and rerun the full workload-to-schedule journey after shared scheduling behavior changes.

## 2026-09-30 — Verify all group period upserts and invalid-date retention

- Runtime scope: selected the existing group-semester context `СИ-1` (`group_id=1`, semester 1). Submitted reversed lecture-week dates; the editor rejected them, retained both exact dates, marked the end field invalid, and displayed the inline Russian range error. No API write occurred for that invalid range.
- Upserts: the existing semester period was submitted unchanged and returned success. Temporary lecture-week (2026-10-05–2026-10-11), credit-week (2026-11-02–2026-11-08), and exam-session (2026-12-14–2026-12-27) periods were each saved through their own upsert form. The lecture-week appeared in the selected group’s schedule period navigation with the same dates, proving group-semester-scoped read-back.
- Cleanup/read-back: deleted each temporary special period through its own UI delete control. The group schedule then displayed only the original semester period (2026-09-01–2027-01-06); no special periods or timetable changes remained.
- Checks: browser console errors were zero. No tests or test files were added.
- Remaining: proceed through the remaining B05/B06 acceptance gates and rerun the full workload-to-schedule journey after shared scheduling behavior changes.

## 2026-09-30 — Verify Accounts editor and safe create failure

- Runtime data: the Accounts workspace contains only the active super-admin. The existing six-column report is preserved. Its row editor opens as a real modal sheet; at 320px it fits the viewport at 304px wide, and at desktop it remains a centered 560px sheet. The create flow also opens in the shared sheet.
- Selectors and draft behavior: changing the unsaved role to faculty administrator reveals a searchable faculty selector; selecting a result adds a readable faculty chip. Teacher search returns a named result and the form confirms the selected teacher without exposing IDs. Filling FIO suggests a login; a manually edited login remains unchanged when FIO changes. All of these checks were dismissed without saving.
- Failure retention: submitted a syntactically valid, disposable faculty-admin create draft with no required scope. The API rejected it with the localized validation message; the editor retained the FIO and email, stayed open, and showed no generated credential. Searching for that email returned no account, confirming no record was created. The sole active super-admin remained unchanged.
- Scope boundary: did not create a persistent account or alter the only working super-admin. The source contract requires a scope for faculty-admin creation, but successful creates, edits to existing scoped accounts, and their authoritative read-back remain unverified because there is no removable non-admin account fixture or account-delete UI. No account-source changes were needed for this slice.
- Checks: browser console reported zero errors or warnings. No tests or test files were added.
- Remaining: verify successful role-specific create/edit and scoped-account read-back with a removable non-admin fixture, continue B06 acceptance, then rerun the full workload-to-schedule journey after shared scheduling behavior changes.

## 2026-09-30 — Check current browser support for true zoom acceptance

- The authenticated Playwright page is currently running with a 390×844 emulated viewport. Sending the browser zoom shortcut did not change the viewport or device pixel ratio, so this session cannot demonstrate true 200% browser zoom. The existing narrow-width checks remain useful but are not treated as a substitute for zoom acceptance.
- No application data or source code changed. True 200% zoom remains open for a browser session that exposes browser-level zoom controls.

## 2026-09-30 — Exercise faculty schedule generation and weekly scopes

- Generation scope: from the administrator Schedule page in semester 1, the “Составить для факультета” action created a private faculty run for the Building Faculty. The page explicitly said that published lessons change only after selected lessons are published. The API/scheduler received the existing semester workload and returned one feasible incumbent with 3 of 5 remaining lesson units placed.
- Live progress and cancellation: the run remained in its separate draft view for 281 seconds. The elapsed-time status continued updating, while the incumbent, branch/conflict counts and objective bound remained unchanged after the initial search updates. Stopped the diagnostic run through the UI. Its terminal state was “stopped”; the interface confirmed the published schedule did not change. No proposal was published.
- Authoritative read-back: after the run stopped, reloaded the Schedule analyzer. It still showed the same 11 published lesson event IDs as the pre-run baseline, and the analyzer still reported 4 teacher-unavailable findings. This confirms the private run and cancellation did not mutate the timetable.
- Analyzer evidence: the findings linked to the affected schedule lessons and a dated transfer, including repeat-week and dated-occurrence context. The aggregate weekly view reported one active group in both faculty and university scope and rendered its full weekly grid. Current fixtures contain no second empty active group, so the requested blank-grid behavior for an unscheduled active group remains unproven.
- Local solver fixture: ran the committed synthetic scenario directly through the running scheduler's pinned OR-Tools 9.15.6755 engine with a 15-second diagnostic ceiling. It completed `optimal`, placing all 4 units in 0.03 seconds (2,806 branches, 575 conflicts; objective and bound both -37,906). Progress advanced through preparing, presolving, searching, validating and complete. The expected contradiction, ambiguity and unsupported-room/preference cases remained review findings. This verifies the solver path only; it does not verify API persistence, UI proposal review or publication.
- Remaining: verify a terminal generated proposal and its cell-level analysis/publication path on a suitable run; investigate why this faculty fixture plateaued at 3/5 for over four minutes and whether progress should expose solver activity beyond elapsed time; verify blank active-group rendering with a suitable fixture. No source code changed and no tests or test files were added.

## 2026-09-30 — Show time since the last solver update

- Finding: the faculty solver run kept reporting its last incumbent and search counters while only elapsed time advanced. The operator could not tell whether new solver information had arrived recently.
- Change: the scheduler progress reporter now sends `solver_idle_seconds`, measured with a monotonic clock from the last solver callback. The existing internal progress action validates the finite metric and persists it through the same sequenced progress path. The administrator controller displays “Последнее обновление решателя: N сек. назад.”; it does not fabricate or increment branch/solution counters.
- Runtime: copied the four changed source files to the scheduler, API and Rails containers, restarted those services, and ran `rails assets:precompile` so Propshaft served a new fingerprinted Stimulus asset. Hashes of all four source files matched the running containers. The progress endpoint returned `solver_idle_seconds`; the active browser view displayed it at 8.0 seconds and then 20.1 seconds as the same search continued without a solver callback. A local HTTP mock around the actual ProgressReporter verified a 2.0-second heartbeat and reset to 0.0 after a new callback.
- Cleanup/read-back: stopped the private diagnostic run through the UI after 30.2 seconds. A fresh Schedule analysis still read back the same 11 published lesson IDs and the same 4 teacher-unavailable findings; no proposal was published. Browser console errors and warnings were zero; services were healthy.
- Checks: `python3 -m py_compile`, `node --check`, API Ruby syntax, and focused `git diff --check` passed. No tests or test files were added.
- Remaining: complete a terminal UI proposal review and cell-level publication journey; investigate the real faculty fixture’s long 3/5 search; verify an unscheduled active group when such a fixture exists.

## 2026-09-30 — Verify a bounded faculty proposal in the review UI

- Exact-snapshot diagnostic: captured the private run snapshot without printing it, then ran that snapshot directly through the same pinned scheduler. The 15-second bounded solve placed all 5 of 5 required units and returned a feasible incumbent (6 solutions, 834,622 branches, 328,590 conflicts; objective 51, bound -19,450). It did not prove optimality. This differed from earlier unbounded UI searches that plateaued with 3/5; investigate search variability and objective formulation before treating generation quality as acceptable.
- Follow-up replay on the persisted review snapshot: repeated the bounded run directly in the scheduler container; it again returned 5/5 at 14.96 seconds (6 solutions, 428,633 branches, 149,933 conflicts; objective 51, bound -19,450). An unbounded replay reported a 3/5 incumbent within 0.02 seconds and improved its bound to -19,450 by 0.24 seconds, then produced no better incumbent during a 30-second observation. A separate unbounded replay also had no incumbent callback for 120 seconds. Both processes were stopped locally; the API run was unaffected. Search is active, but useful incumbent quality depends sharply on the bounded/unbounded search path.
- Hint diagnostic: the deterministic greedy initializer supplied `assigned=1` hints for all five units on this snapshot, even though the first CP-SAT incumbent in the unbounded run placed three. This narrows the issue to CP-SAT hint/model search behavior, rather than greedy construction or snapshot loading. No persistent solver configuration was changed. A feasibility-only monkeypatch was stopped after 30 seconds without a conclusion, so it does not establish that feasibility itself is slow.
- Audit correction: the first complete-hint diagnostic patched `solver.CpSolver`, while `generate` constructs `cp_model.CpSolver`; its settings were not applied. A second wrapper received `assigned_units` and therefore never completed the candidate-placement hints. Neither run tested complete placement hints, and their earlier conclusions about that strategy were invalid.
- Corrected complete-placement experiment: fixed hints for every selected and unselected candidate prove the greedy 5/5 placement feasible in 0.009 seconds with zero branches (objective 53); this is a feasibility check, not a global optimum. With complete placement hints left unfixed and a genuine 5-second limit, CP-SAT returned the same full assignment immediately, then improved to objective 51 by five seconds when hint repair was enabled. Without hint repair, the complete hinted solve remained at objective 53 after 15 seconds. The ordinary bounded solve also reached 5/5/objective 51, so the paired complete-hint and repair change improves the first incumbent without sacrificing this fixture's measured secondary objective.
- UI/API journey: repeated the faculty flow with a temporary 15-second limit on the actual `schedule_generation_worker` (not the API container). Run `9cab7c98-99ad-4a69-9788-8b3fddef917c` reached “Готово к проверке”; its private proposal contained five placements. The page showed three `TEACHER_UNAVAILABLE` findings linked to existing lesson records 19, 5 and 11. Every proposed-row checkbox and “Опубликовать выбранные занятия” were disabled until all draft errors are fixed. No proposal was published and published timetable data was not changed.
- A preceding diagnostic attempt put the temporary limit on the API container by mistake. Because that component does not execute the solver and its live internal progress action lacked the new metric contract after container recreation, that run failed with a lease/progress error. The API source was recopied and restarted before the successful worker-limited run; the failed run also did not publish data.
- Restored the normal Compose configuration afterward and verified `SCHEDULER_SOLVE_SECONDS` is unset in both `schedule_generation_worker` and `api_geteway`; scheduler, API, and web are healthy. The 15-second cap was diagnostic only and is not a product setting. Removed the task-specific host and container snapshot/override files from `/tmp`.
- Remaining: resolve the three teacher-availability conflicts through normal edits and then re-run analysis before attempting publication; investigate why the unbounded faculty search stalls at 3/5 while the same snapshot yields 5/5 under a bounded run. Do not publish the current error-bearing proposal.

## 2026-09-30 — Verify Calendar narrow tables and keyboard access

- Responsive evidence: at 390px and 320px, the document and main workspace stayed within the viewport on all five Calendar pages. Period settings had no wide table. Semester and Holiday tables retained their full 3-column layouts inside named, focusable regions; at 320px the region widths were 286px while table content measured 1,120px. Reservations and weekday transfers were checked with populated 5-column rows at 320px; their regions measured 286px while table content measured 1,120px and 860px respectively. No table columns were hidden or reordered.
- Keyboard path: all four list regions now reuse the existing `table-scroll` controller and expose Russian shortcut instructions plus `aria-keyshortcuts`. At 390px/320px, ArrowRight advanced by 285px/229px, End reached each table’s horizontal end, and Home returned to 0. This was verified with populated Semester/Holiday tables at both widths and populated Reservation/weekday-transfer tables at 320px.
- Semantics: the accessible tree exposes 3 column headers for Semester and Holiday; populated Reservation and weekday-transfer tables expose 5 column headers and 5 cells per data row, with the delete action represented as the action cell.
- Cleanup/checks: disposable reservations and weekday transfers were removed through the UI; read-back confirmed 0 active room occupancy and an empty transfer list. Browser errors were zero. Rails source hashes matched the running container, both services were healthy, `git diff --check` passed for the edited views and this handoff, and no tests or test files were added.
- Remaining: continue the remaining B05/B06 acceptance gates and rerun the full workload-to-schedule journey after shared scheduling behavior changes.

## 2026-09-30 — Verify holiday and weekday-transfer scope

- Holiday: created a uniquely labelled nonworking date on 2099-12-30, read it back in the existing three-column list, then deleted only that row through its confirmation. The prior 2026-09-08 holiday remained untouched; the disposable label was absent after cleanup.
- Weekday transfer, group scope: explicitly selected catalog group semester `СИ · 2026 · 1 курс`; the URL carried `group_semester_id=1`, the editor stated that the group was selected in context, and read-back displayed that group for the disposable 2099-12-30 Monday transfer. Deleted the exact row through its confirmation.
- Weekday transfer, global scope: explicitly selected “Все группы”; the context URL had an empty group-semester value and the editor stated it would apply to all groups. Read-back showed “Все группы” for the disposable Wednesday transfer on the same date. Deleted the exact row through its confirmation.
- Cleanup/checks: weekday-transfer list returned to its empty state; no holiday QA row remained; browser console errors were zero. No tests or test files were added.
- Remaining: proceed through the remaining B05/B06 acceptance gates and rerun the full workload-to-schedule journey after shared scheduling behavior changes.

## 2026-09-30 — Resolve generated-run conflicts inside the private draft

- Starting point: faculty run `9cab7c98-99ad-4a69-9788-8b3fddef917c` reached the proposal page with five generated rows and three `TEACHER_UNAVAILABLE` findings on existing events 19, 5 and 11. The profile blocks period 1 on every weekday.
- Draft-only edits: moved Physics/event 19 to Thursday period 3, Cars/event 5 to Thursday period 4, and Object/event 11 to Friday period 3. Each save returned the Russian “saved to draft” feedback and reanalyzed the full sandbox; the findings reduced 3 → 2 → 1 → 0. All three source events remain unchanged in `schedule_events` at their original weekday/period/room/week values.
- Review gate: the private proposal now has eight rows (five generated plus three staged existing-event edits), zero findings, and all row checkboxes enabled. Selecting one generated Physics row enabled the publish button; clearing the selection disabled it again. No publish request was submitted.
- Authoritative read-back: run status `proposed`, revision 4, eight proposal rows, empty findings, and `published_at = NULL`. Events 5, 11 and 19 retain their original database coordinates. The existing analyzer remains unaffected; no published timetable mutation occurred.
- Remaining: the successful bounded solver proposal is still not optimal and current unbounded search behavior remains unexplained. Continue solver investigation and preserve the terminal-only review boundary until the pending early-checkpoint policy is answered.

## 2026-09-30 — Verify the empty active-group weekly grid in the browser

- Fixture: created disposable student group 1032 through the administrator UI with automatic semester provisioning disabled. Because the group catalog has no one-semester add control, inserted one group-semester membership (1041) for semester 1; it had no workload, schedule events or period rows.
- University weekly view: the selected 2026/2027 semester reported two groups. `СИ 2 курс` showed `0 занятий` and a complete five-period by six-weekday table with all 30 lesson cells blank. The original `СИ 1 курс` grid remained present with its 11 scheduled events. This confirms empty active groups are included alongside event-backed groups in the running Rails/API path.
- Cleanup: removed only membership 1041, then deleted group 1032 through the administrator UI. Reloaded the aggregate view; it returned to one group. Database read-back found zero rows for the disposable group/membership and one remaining semester membership. Browser console errors/warnings: zero; services healthy. No published schedule rows changed and no tests or test files were added.

## 2026-09-30 — Seed all CP-SAT placement choices from the greedy schedule

- Corrected the prior diagnostics: one patched the wrong `CpSolver` reference; another treated `assigned_units` booleans as placement variables. Neither measured complete candidate-placement hints. The earlier claim that complete hints had no benefit was invalid.
- On the retained exact faculty snapshot, adding hints for every unselected candidate as zero and retaining each greedy selected choice as one gave CP-SAT a complete feasible 5/5 incumbent in 0.009 seconds with zero branches (objective 53). With the hints unfixed and hint repair disabled, the run remained at 53 after 15 seconds. With CP-SAT `repair_hint` enabled, the incumbent was still 5/5 immediately and improved to objective 51 by five seconds.
- Change: `_add_greedy_hints` now supplies complete placement-variable hints, and `generate` enables hint repair. The exact snapshot was sent through the restarted scheduler's `/v1/solve` HTTP endpoint with a five-second diagnostic cap; the live service returned 5/5 placements, objective 51, feasible status and bound -19,450. Host and container solver-source hashes matched. The cap was request-only; normal generation remains unbounded.
- The existing private proposal remains at eight rows, zero findings, revision 4, and `published_at = NULL`; no schedule publication or database change occurred. No tests or test files were added. `py_compile` and focused `git diff --check` passed.
- Open product decision: whether the first complete proposal should be reviewable while CP-SAT continues optimizing. Until answered, proposals still become reviewable only at terminal solver completion.

## 2026-09-30 — Verify complete-placement hints through the administrator worker

- Started faculty generation from the authenticated Schedule workspace, creating private run `24189c83-d650-4289-988f-7d621ae1d603`. No solve-time limit was configured on the worker.
- The DB-backed worker called the updated scheduler, and durable progress reported 5/5 required units placed after about six seconds. The live administrator page displayed the same count and solver metrics. At 233 seconds the run remained `processing/solving`, with one feasible incumbent, 1,656 branches, 5 bound updates, objective 263 and bound -19,450; the idle-since-callback indicator had advanced to 232.6 seconds. The dedicated scheduler was using one CPU core. The browser showed the active stop control and had zero console errors.
- This validates the queued UI → API → worker → solver progress path with the new placement hints. The run remains private and cancellable while optimizing; no proposal has been finalized and nothing was published. This live snapshot differs from the earlier retained snapshot's objective values, so compare placement completeness/progress, not the objective numbers across those snapshots.
- Remaining: the terminal-only proposal gate means this full incumbent is not yet editable or reviewable. The administrator's preference on exposing a first complete checkpoint during continued optimization is pending; do not change checkpoint/publication semantics before that decision. Continue observing this run or stop it explicitly from its visible control if the long search is no longer wanted.

## 2026-09-30 — Complete the live optimal proposal review without publishing

- The queued faculty run `24189c83-d650-4289-988f-7d621ae1d603` reached terminal `proposed` after 309.08 seconds of unbounded search. CP-SAT proved the five required units optimal: 10,276,633 branches, 5,640,892 conflicts, eight incumbent reports, objective 51 and bound 51. The Schedule page showed “Готово к проверке” and all five generated placements.
- The analyzer correctly flagged three existing recurring events against the teacher profile. Staged fixes only inside this private run: Physics/event 19 → Thursday period 3 (even week); Cars/event 5 → Thursday period 4 (both weeks); Object/event 11 → Friday period 3 (both weeks). Reanalysis reached zero findings. The proposal now has eight rows (five generated plus three staged edits), revision 4, status `proposed`, and `published_at = NULL`.
- Review gate: with zero findings, all eight row checkboxes were enabled. Selecting one generated lesson enabled “Опубликовать выбранные занятия”; clearing the selection disabled it again. No publish request was submitted. Authoritative read-back confirms source events 5, 11 and 19 retain their original Tuesday/Friday/Monday period-1 cells. No published timetable rows changed.
- Preference-compiler boundary: updated Hanami to reject malformed scheduler responses and any rule outside schema-v1 soft/proposed slot or consecutive types, source wish, submitting teacher, supported day/week/period, or assigned workload. Findings must be the known review-only codes and refer to the current wish. An inline smoke called the live scheduler compiler for both a weekday-slot wish and the oven/consecutive wish; both validated. Unknown rule types and another teacher's rule were rejected. No wish/database row was created.
- Verification: API source hash matched the running container; the API restarted healthy; the active scheduler progress feed recovered and completed normally. `ruby -c`, Hanami boot, scheduler `py_compile`, and focused whitespace checks passed. RuboCop is not installed in the project bundle, so it was not run; no dependencies, tests, or test files were added. Browser console errors: zero.
- No publication was made. The pending design decision about reviewing a first complete checkpoint during optimization remains separate; this run reached terminal before review. Existing blanket-schedule and cell-level publish behavior is verified through the ready-to-publish gate, not through a publication mutation.

## 2026-09-30 — Ground text period wishes against the real time-slot catalog

- Finding: the deterministic parser can read period numbers through pair 9, while the live semester currently has only five time slots. Before this change, a wish for pair 9 could be approved as `p9`; snapshot building later filtered that rule out because it had no matching slot ID, making the approved wish an ineffective no-op.
- Change: `BuildTeacherPreferenceContext` now supplies canonical `available_slots` and includes that domain in its fingerprint. The Python compiler sends any numbered slot missing from the catalog to `UNSUPPORTED_PREFERENCE` review. Hanami v17 validation accepts slot rules only when every `pN` belongs to that current catalog. The version bump causes pending wishes to be recompiled under the updated catalog contract.
- Runtime checks: the frozen synthetic scenario still compiles to five proposals and five review findings. A catalog-missing pair-9 wish yields zero proposals and one `UNSUPPORTED_PREFERENCE`. The real Hanami `CompileTeacherWish` component, with live DB context and scheduler HTTP, accepts pair 1 and routes pair 9 to review.
- Safety/read-back: the live DB has five time slots and zero teacher-wish rows; the read-only compilation created no wish row. No approved preferences were invalidated by the fingerprint change. Scheduler and API source hashes match the worktree; both services restarted healthy. Ruby syntax, Python `py_compile`, and Hanami boot passed. No tests/test files, dependencies, or database rows were added.

## 2026-09-30 — Recheck aggregate weekly grid keyboard scrolling at 320px

- Runtime: the university weekly view rendered one in-scope group at a 320px viewport. The document stayed 320px wide; the labelled, focusable group-grid region measured 258px wide and contained the unchanged 1,080px timetable table.
- Keyboard: after focusing and clicking the table region, ArrowRight moved its horizontal scroll position from 0 to 43px while the document remained within the viewport. The browser reported zero console errors.
- Scope: this verifies the narrow aggregate table's local overflow and keyboard path; it does not replace true 200% browser-zoom acceptance. No schedule data changed.

## 2026-09-30 — Reassess local Jev availability

- Discovery: the public `amithgc/local-jev` repository now provides a third-party MIT-licensed, Jev-compatible `/v1/systemone` server. A shallow clone at `64a0b31ff343dca32142496cf9edca5a0174a18d` confirmed the license and API package source. Its README identifies it as a research project and reports 80.5% on general JevBench for Qwen3.5-4B; this is not evidence of Russian scheduling accuracy. The repo has no checked-in dependency lock, and its `torch`/`transformers` ranges are broad. The README lists 9.32 GB disk and about 8.5 GB memory for its default model; this workstation reported 7.8 GB available RAM and a 4 GiB GPU at inspection, so the default model is not a safe assumption.
- Fit: Jev's typed choice/score/yes-no response is not the product's constraint JSON. Keep the grounded deterministic compiler, Hanami schema validation and CP-SAT as the only active path. A Jev-compatible model may be evaluated later in an isolated shadow adapter over bounded options after pinning both source and model revisions and measuring the Russian wish corpus; it must not approve rules or relax hard constraints.
- No runtime was installed, no model weights were downloaded, and no product or schedule data changed. The architecture draft's local-model section now records this finding and corrects the earlier statement that no local-compatible implementation was available.


## 2026-09-30 — Start isolated pinned local Jev evaluation

- The earlier source-only inspection is followed by an isolated evaluation under `/tmp/milk-schedule-local-jev-eval`, still at source commit `64a0b31ff343dca32142496cf9edca5a0174a18d`. A temporary uv 0.12.21 environment uses CPython 3.12.14 and a generated dependency lock with SHA-256 `ee4355df47817940ee2281ac23a133bf86c0cf7bce4698773b398d191ab98212`. Dependency installation is still running; no successful runtime import or inference is claimed yet.
- The Hugging Face metadata confirmed Qwen/Qwen2.5-1.5B-Instruct revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`. Its configuration and tokenizer files downloaded into an isolated temporary directory; `model.safetensors` is still downloading to a `.partial` file and is not usable yet.
- Evaluate two independent bounded questions for each of the ten frozen Russian wishes: intent and review disposition. Expected outcomes must remain independent of model predictions. This is a small smoke comparison, not evidence that arbitrary Russian text is understood reliably or that a local model can generate authoritative constraint JSON.
- No application dependencies, approval state, schedule rows or UI design changed. Keep both existing process handles until authoritative completion or failure; download latency alone does not justify restarting them.


## 2026-09-30 — Preserve conditional teacher wishes

- Reproduced: “Хочу в среду на второй паре, кроме экзаменационной недели” and a wish conditional on having no morning lessons previously became unconditional soft slot rules.
- The compiler now withholds explicit `если`, `кроме`, `за исключением`, `при условии` and `только когда` clauses as `UNSUPPORTED_PREFERENCE` review findings. A reason such as the original “потому что печка включена” remains supported. Hanami compiler version is v18.
- Inline verification preserved the frozen five-proposal/five-review baseline and withheld three conditional slot/consecutive wishes. Ruby syntax passed. Updated sources were copied to the running API and scheduler and restarted; direct execution in the scheduler confirmed review-only behavior. A follow-up live HTTP request and the real Hanami `scheduling.compile_teacher_wish` component both returned review-only output; Hanami reported v18 with the current database context. Compilation was read-only. No test files or database rows were added.


## 2026-09-30 — Align generation-worker compiler source

- Runtime source comparison found the generation worker still contained compiler v16, while the API and worktree had v18. The worker and API share an image but have independent container filesystems.
- A read-only database check found zero queued or processing generation runs before restart. Copied the current compiler source into the worker and restarted it. Hanami loading reports v18; the source SHA-256 now matches the API and worktree (`85f65b0b449b45683ef00e965b900150cf94f4a461e78afdf5ff15321f583adb`). No schedule or wish data changed.


## 2026-09-30 — Align worker slot catalog context

- Compared all 22 scheduling operations, generation relay and run-repository source files across the worktree, API and worker. The API matched all files; the worker still had an older teacher-preference context builder without the current slot-catalog contract.
- Confirmed zero queued/processing runs, copied that builder and restarted the worker. All 22 source hashes now match in both containers.
- A positive Wednesday period-1 probe correctly hit existing profile unavailability, so the catalog acceptance probe used a supported negative wish instead. The real worker Hanami compiler v18 proposed existing period 1 and withheld absent period 9 as `UNSUPPORTED_PREFERENCE`. These component calls were read-only; no teacher wishes or schedule records were saved.


## 2026-09-30 — Recover isolated local-model runtime installation

- The initial locked install completed downloads but failed while copying Torch onto `/tmp`, a 7.4 GB tmpfs, with `Disk quota exceeded`. This was an authoritative installation failure, not an observation timeout.
- Moved only the experiment’s partial virtual environment to `/home/xjensu/.cache/milk-schedule-local-jev-venv` and linked the original temporary path to it. A normal sync initially considered the partial Torch metadata installed; an actual import exposed missing module contents. Reinstalled the same locked Torch package from the completed cache.
- Verified imports of Torch (`2.14.0+cu130`), Transformers (`5.17.0`) and `local_jev.engine.Engine`; CUDA availability is true. Application dependencies and containers were untouched.
- Model weights remain incomplete. Upstream pinned metadata specifies 3,087,467,144 bytes and SHA-256 `dd924a11b4c220f385b51ffa522daea7c9f3d850e31b162bb5661df483c6d3ee`; verify this checksum before accepting any inference evidence. The waiting evaluation process has not run inference yet.


## 2026-09-30 — Complete pinned local Jev GPU smoke comparison

- Download completed; checkpoint size and SHA-256 matched upstream pinned metadata. The isolated Qwen2.5-1.5B runtime executed locally on the RTX 3050 with network access disabled for model loading.
- Ten frozen Russian wishes, two independent bounded questions: intent 5/10, disposition 5/10, joint outcomes 3/10. All dispositions were `propose`; all five review cases were missed. No input truncation. Total measured inference was 9.854 seconds including first load; subsequent nine cases took 2.668 seconds.
- Input-format sensitivity: wish-only intent classification improved to 7/10; rotating answer order yielded 8/20 answers. This configuration is unsuitable for active parsing or review decisions. These are small synthetic checks, not a general model benchmark.
- Saved inputs, distributions, revisions, checksum and sensitivity results in `docs/architecture/evidence/local-jev-qwen2.5-1.5b-2026-09-30.json`. The deterministic compiler, administrator approval and CP-SAT remain the active path. No model dependency, test file, wish or timetable mutation was added to the application.


## 2026-09-30 — Verify teacher-wish request stack with rollback

- Executed the booted Hanami Rack application, including routing, bearer decoding, authorization, contracts, compiler HTTP and repositories, using short-lived synthetic signed role claims linked to existing fixture identities. This does not verify teacher browser sign-in. No credentials or token values were emitted.
- Teacher POST submission returned 201/submitted. Teacher PATCH approval returned 403. Super-administrator PATCH approval returned 200, with authoritative repository read-back approved at revision 1. Repeating revision 0 returned 409.
- All requests ran inside one rollback-only database transaction. After rollback the wish count matched the starting count; no wish or schedule data remained from the check. No test files were created.


## 2026-09-30 — Stop late progress updates after view disconnect

- Found a pending progress fetch could finish after Stimulus disconnect and then redirect/reload the new page or write obsolete feedback. Disconnect previously cleared only the next polling timer.
- The controller now aborts its active request and clears its identity on disconnect. It checks request identity and connection state after both fetch and JSON parsing; aborted or replaced requests neither display failure feedback nor schedule retries.
- Inline checks cover disconnect during fetch and JSON parsing. The rebuilt Rails asset `/assets/controllers/schedule_generation_progress_controller-5c18a2a0.js` was imported in the real browser: both late-response paths were ignored, a normal update rendered and advanced sequence, and the intact eight-row private draft remained present. The temporary fetch override was restored, and the verification polling timer was cleared. No tests/test files, schedule data or design changes were added. Services are healthy.
- The user’s CRDT requirement is still an open architecture decision: the current private-draft model uses server-authoritative progress and revision checks rather than CRDT merging. Asked whether shared draft editing/merging is required; no answer received yet. This is not evidence that the CRDT requirement is complete.


## 2026-09-30 — Verify conditional and contradictory wish review requests

- In the booted Hanami Rack request stack, a conditional wish submitted as review-only and approval returned 422. A supported negative wish was approved; an opposing positive wish became `CONTRADICTORY_TEACHER_WISH` review-only and its approval returned 422.
- Withdrawing the first approval returned 200. Reviewing the opposing wish next returned 409/recompiled with a fresh proposal; approval at its new revision returned 200. Authoritative read-back showed approved/revision 2.
- Used synthetic signed role claims over existing fixture identities within one rollback-only database transaction. Final wish count matched the starting count. This verifies API request behavior, not teacher browser sign-in. No test files or lasting schedule/wish mutations were created.


## 2026-09-30 — Reject obsolete progress versions

- The controller previously trusted `changed` and could accept a duplicate or older sequence. It now requires a safe integer sequence strictly greater than the current cursor before changing displayed progress or processing terminal state. Invalid versions stay on the retry path.
- Inline checks covered older, duplicate, null, malformed, fractional and unsafe-integer versions, plus a newer valid update. Rebuilt only Rails with `--no-deps`; imported the served module in the browser and verified older/duplicate updates were ignored while the newer update rendered.
- The browser session now requires normal sign-in. Earlier isolated-context copies did not provide a durable independent login. No temporary teacher account was created. This verification used the public page’s served module and controlled responses; it does not claim a newly authenticated live generation journey.
- This is monotonic progress delivery, not a CRDT implementation for timetable edits. Shared-draft merging remains an unresolved scope decision. No test files, passwords in output or timetable mutations were introduced.

## 2026-09-30 — User withdraws CRDT requirement; verify visible generation

- Latest user direction explicitly drops CRDT: the administrator needs to see schedule creation progress after pressing the button. This supersedes the unresolved CRDT scope notes above. Updated the architecture document accordingly; private drafts, durable progress and optimistic revision checks remain the implementation.
- Signed in normally with the existing administrator account. In the running browser, opened the university scope and clicked «Составить для университета». New private run `3c0e9bd2-b1ca-4eea-b6ac-55e50bdb33f2` immediately displayed «В очереди» and preparation feedback, then automatically switched to «Составление» with 5/5 units placed.
- Observed automatic elapsed-time updates at 8, 22, 66, 108, 144, 192, 228 and 271 seconds. At 271 seconds the displayed bound update count advanced from 5 to 6 and the lower bound changed from -19450 to -18443. Reload at 156 seconds preserved the same run and resumed polling. The stop control remained available.
- Authoritative read-back while active showed processing, event_sequence 46 and published_at nil. The run was still searching at the final observation; this check does not claim natural completion. No publication was performed. Earlier completed-run evidence remains separate from this fresh live-progress journey.
- No design changes, new tests/test files or account insertion. Normal authentication credentials and session data were not emitted.

## 2026-09-30 — Completed live generation browser journey

- The university generation run `3c0e9bd2-b1ca-4eea-b6ac-55e50bdb33f2` reached `proposed` with event sequence 184, revision 1 and `published_at` nil (authoritative API repository read-back).
- After normal sign-in, the administrator workspace loaded the same run and showed «Готово к проверке», five private generated lessons, eight feasible candidates, a final objective and bound of 51, and three red teacher-unavailability findings. The UI disables publication selection until the draft errors are repaired. This completes the earlier live-progress journey's terminal-state verification; no publication occurred.
- Local Jev remains an optional experiment, not the active wish compiler. The previously recorded ten-case evaluation showed inadequate review classification, so the deterministic Russian parser and administrator review remain active. The local-model feature is not claimed complete.

## 2026-09-30 — Repair the completed university draft and select one row

- In the real administrator browser, opened each of the three red teacher-unavailability findings in run `3c0e9bd2-b1ca-4eea-b6ac-55e50bdb33f2`. Staged event 19 at Thursday period 3/even, event 5 at Thursday period 4/both, and event 11 at Friday period 3/both. Each editor saved into the private run; the third repair cleared all findings.
- Authoritative run read-back: `proposed`, revision 4, eight proposal rows, zero findings, `published_at` nil. The UI enabled all eight individual row checkboxes. Selecting only `generated-10-1` enabled «Опубликовать выбранные занятия», and the selection survived a full page reload.
- This verifies the individual selection UI and draft repair flow. The publication button was deliberately not submitted, so it does not prove the publication transaction in this check. Other earlier rollback-only publication evidence remains separate.

## 2026-09-30 — Correct generic consecutive-period wish scope

- Created a demo teacher account through the existing account UI linked to the existing sample teacher identity. Signed into the teacher cabinet, submitted «Хочу две пары подряд, потому что печка включена.» and confirmed that the cabinet showed a parsed proposal.
- This exposed a parser error: the rationale word «печка» was being treated as a lab subject and the wish was incorrectly scoped to a specific Mathematics/Lab workload. The compiler now scopes a consecutive-pair wish to a requirement only when a subject is actually named; otherwise it emits a teacher-wide soft preference. The solver and analyzer already support teacher-wide scope. Ruby response validation now accepts that exact scope, and the compiler version is `russian-templates-v19` so existing wishes are recognized as stale.
- Rebuilt and restarted the API and scheduler. Submitted the same wish again through the teacher UI. Authoritative DB read-back showed v19, a `consecutive_lessons` proposal with scope `{teacher: 1}`, `pair_count: 1`, and no findings. The incorrect v18 sample was rejected through the administrator UI; the corrected wish remains submitted for review. No wish was approved and no timetable was changed.
- The application was accessed at `127.0.0.1` because `localhost` went through the configured HTTP proxy and returned 502; direct local access succeeded. Ruby syntax and Python compilation checks passed. No test files were added.

## 2026-09-30 — Approved teacher-wide wish reaches the solver

- Approved the corrected sample wish in the super-administrator workspace. Repository read-back showed status approved, revision 1, compiler version `russian-templates-v19`, and a teacher-only consecutive-pair preference with `pair_count: 1`.
- Started a faculty run from the administrator button. Its persisted snapshot contained the approved teacher-wide rule. The live progress panel showed queued then solving, five of five lessons placed, candidate/branch/conflict metrics, elapsed time and lower-bound changes while searching. It completed naturally after 392 seconds.
- Final run read-back was `proposed`, revision 1, unpublished. Its five Wednesday placements include adjacent periods 2–3 in both alternating weeks and periods 3–4 with a both-weeks placement; thus a consecutive pair exists in each week under the approved teacher-wide rule. The proposal analyzer reported `TEACHER_UNAVAILABLE` findings on existing published events; the page marks them red and blocks publication until resolved. No publication occurred.
- This verifies the approved natural-language wish passed through the snapshot into a completed solve and produced a preference-satisfying schedule. The schedule remains a private draft pending those unrelated hard conflicts.

## 2026-09-30 — Resolve conflicts on the wish-aware generated draft

- In faculty run `91dfb6c7-8916-405d-9b82-fe1848361878`, staged three recurring-event corrections: source 19 → Thursday period 3/even, source 5 → Thursday period 4/both, source 11 → Friday period 3/both. The browser form retained the run revision, and repository read-back confirmed all three edits at revision 5.
- Final authoritative state: run `proposed`, five generated placements plus three existing-event changes, zero analyzer findings, and `published_at` nil. The snapshot retains the approved teacher-wide consecutive-pair rule. The UI showed eight enabled individual rows; checking one row enabled publication. No publish request was submitted.
- This closes the sample teacher wish → review → approval → solver snapshot → live progress → preference-satisfying proposal → administrator conflict repair and row selection path. The demo teacher account and two submitted sample wish records remain in the local database; the inaccurate wish is rejected, the corrected wish is approved. They are local sample data and no credentials are recorded here.

## 2026-09-30 — Read-only analyzer on the published timetable

- Opened the published Schedule workspace for faculty 1, semester 1, group 1 with analysis enabled. It reported four profile-unavailability findings: three recurring lessons and one dated occurrence; coverage stated 11 recurring lessons and three exception dates checked.
- The issue list rendered four `.is-error` entries; the weekly grid visibly labelled its three affected lesson cards «Ошибка». The dated issue is listed separately from the recurring grid. This verified the analyzer against live published data without changing it.

## 2026-09-30 — Profile contradictions remain review-only

- The sample teacher profile marks Monday period 1 unavailable and period 2 allowed. Submitting «Не могу в понедельник 1–2 пару» produced a soft `unavailable_slot` wish for both periods, leaving the hard profile rule authoritative for period 1.
- Submitting the opposing «Хочу занятия в понедельник 1–2 пару» produced `PROFILE_TEXT_CONTRADICTION`, status `review`, no proposals and compiler v19. Teacher cabinet copy says the profile restriction was preserved. The super-administrator list shows the finding and no approve action; only rejection is offered.
- This verifies the policy against current profile constraints through teacher submission, persisted compiler output and administrator controls. No schedule write occurred.

## 2026-09-30 — Preserve soft wishes against positive profile availability

- Reviewed the agreed rule: text wishes stay soft while hard profile unavailability remains authoritative. The approved-preference loader incorrectly treated a profile `available_slot` as a reason to discard a teacher's soft `unavailable_slot` wish.
- Narrowed the loader's override to an affirmative text wish that conflicts with a hard profile `unavailable_slot`. Inline calls to the real snapshot operation verified that a soft avoid wish is retained when the profile says available, while an affirmative available wish is still blocked by profile unavailability. Ruby syntax passed; no tests/files or profile/schedule data were changed.
- Rebuilt and restarted the API so the running service contains this code. This verifies snapshot preference filtering logic directly; the live demo profile currently has unavailable slots but no explicit positive availability rows.

## 2026-09-30 — Ground named subjects and reject no-workload wishes

- The teacher-wide consecutive rule introduced for generic wishes needed a fail-closed boundary: a named subject the teacher does not teach must not broaden into a teacher-wide preference, and a teacher without semester workload must not receive a no-op rule.
- The parser now keeps heater/oven rationale generic, scopes a uniquely matched subject to that requirement, routes an unmatched subject reference to review, routes multiple matches to ambiguity review, and routes zero-load wishes to unsupported review. The Hanami response validator independently rejects teacher-wide consecutive output unless the teacher has semester workload. Compiler version is `russian-templates-v20`.
- Inline checks passed against the compiled scheduler and live Hanami compiler: generic multi-requirement wish → teacher scope; “по математике” → matching requirement key; unknown “по астрофизике” → review finding; no workload → review finding; and boundary validation rejects generic scope with zero load. Both API and scheduler were rebuilt and healthy. Ruby/Python syntax checks passed; no test files were added.
- Updated the scheduler architecture notes so scope and grounding rules match the implementation.

## 2026-09-30 — Cancel an active generation and resume its terminal state

- Started a faculty generation from the authenticated Schedule workspace and submitted «Остановить составление» while it was active. Captured only safe request fields: the stop form submitted semester 1; Rails returned 303 to the same faculty, semester and run ID.
- The browser rendered «Остановлено» and the message that the published timetable was unchanged. A full reload at the returned URL loaded the same terminal run again. Authoritative repository read-back showed status `cancelled`, event sequence 2, semester 1 and `published_at` nil.
- This verifies cancellation from the UI, scope-preserving redirect, durable terminal status and no publication.

## 2026-09-30 — Show live generation progress and invalidate old compiler approvals

- Rebuilt the API and Rails images and opened the running administrator Schedule workspace. Starting faculty generation showed the solver's improving-solution count, search branches/conflicts, elapsed time, current objective and bound; the values updated in place while the run remained active. Stopping it produced the terminal stopped state and explicitly retained the published timetable.
- During snapshot construction, approved wishes now become review-only if either their teacher/load context fingerprint or stored compiler version is stale. The compare-and-set invalidation checks the approved status plus expected fingerprint and compiler version, preserving concurrent re-approvals. The admin finding explains that the parser version can require a fresh review, and the existing “Перепроверить пожелание” path recompiles it for administrator review.
- The live run downgraded an old approved wish from compiler v19. The admin page showed the stale reason and recheck action; rechecking compiled the saved text with v20 and displayed the resulting soft Monday avoidance rule for explicit re-approval. The wish was left pending review. No timetable was published.

## 2026-09-30 — Make snapshot preparation part of the visible generation run

- Moved snapshot construction out of the synchronous create request. The API now persists a private queued run immediately; the worker claims it, reports a preparing phase while building the immutable input, stores the snapshot and digest with an owner/status compare-and-set, then switches to solving. The worker lease is heartbeated through both preparation and solving, and a cancelled or replaced run cannot store a late snapshot.
- Preparation failures are terminal and the admin gets Russian explanations for common missing workload, time-slot, date-range and teacher-assignment conditions. The snapshot remains private to the run; publication semantics are unchanged.
- A live run exposed an incorrect positional call to the new keyword-only snapshot storage method. Added a safe exception location to worker error logs, corrected the call, and rebuilt the API and worker. The next faculty run completed on its first attempt in 392.6 seconds: 5/5 lesson units placed, 8 incumbents, objective 51 proved optimal, and the browser moved to the private proposal with one visible hard finding. Authoritative read-back showed status `proposed`, one attempt and no `published_at`; the primary timetable was not modified.

## 2026-09-30 — Resolve published conflicts in the private proposal

- The completed run initially contained three `TEACHER_UNAVAILABLE` errors for existing recurring lessons in period 1, plus two review-only unsupported wish findings. The profile blocks period 1 across all weekdays, so an initial staged Wednesday-period-1 edit correctly remained an error. Moving the same lesson to Tuesday period 3 removed that finding; a first Monday-period-3 move for another lesson correctly exposed simultaneous teacher/group/room clashes with a fixed published event, and changing it to Saturday period 3 cleared those clashes. Moving the last period-1 lesson to Thursday period 3 removed the final hard error.
- The proposal now has eight rows, zero error-severity findings and two review-only findings. The browser enabled publication after one row was selected, then selection was cleared; no publish request was submitted. After a full page reload, the private edits remained, all eight rows were present and the publish button was disabled with zero rows selected.
- Authoritative DB read-back showed run revision 6, status `proposed`, `published_at` nil, and source event IDs 5, 11 and 19 still at their original weekday/time-slot pairs. Only the run's private proposal changed.

## 2026-09-30 — Preserve freshness after teacher-wish approvals

- A one-row publish attempt on the older private draft was rejected by the source-digest guard before any write. Rebuilding the current snapshot showed only `teacher_wishes` and derived `approved_preferences` had changed since that run was generated; the published lesson rows remained unchanged. The current workspace reports the run as stale, and DB read-back still shows the same proposal revision and no publication timestamp.
- The previous Rails message incorrectly said only the published timetable had changed. It now tells the administrator that schedule source data, constraints or teacher wishes changed, and asks for a new draft based on current inputs. This preserves source freshness while accurately describing why the old proposal cannot be published.

## 2026-09-30 — Verify current wishes through completed faculty generation

- Started a new faculty run from the signed-in administrator Schedule page after the two teacher wishes were approved. The progress panel updated automatically during the 336-second solve: it reached 13 feasible solutions, 10,952,377 branches, 8,898,412 conflicts, and a proved objective/bound of -41,109. Later objective-bound updates appeared in the browser while the solve was active.
- The run completed as `proposed` at revision 1, event sequence 203, with five proposal rows and `published_at` nil. Its stored immutable input contained the three current wishes (two approved) and the two approved typed rules: one `unavailable_slot` and one `consecutive_lessons`.
- The administrator page automatically reloaded into «Готово к проверке». Static analysis surfaced a review-level notice for a wish that does not identify an existing lesson; three separate hard teacher-unavailability errors kept row selection and publication disabled. Browser console reported no errors. No publication or live schedule mutation occurred.

## 2026-09-30 — Resolve hard conflicts and retain review-only wish findings

- In run `00a4d8b5-eb98-4c90-8afb-0aead4188552`, used the administrator's private edit forms to stage source event 19 → Tuesday period 3/even, event 5 → Thursday period 4/both, and event 11 → Friday period 3/both. After each save, the browser returned to the same proposal and re-ran static analysis; the three `TEACHER_UNAVAILABLE` errors cleared.
- The remaining findings are review-level `TEACHER_SOFT_PREFERENCE_NOT_MET` and `UNSUPPORTED_PREFERENCE` items. They remain visible but do not block publication selection. The administrator could select one generated lesson; the selected count changed to 1 and the publish button enabled. Cleared the selection again and confirmed count 0/button disabled; did not submit publication.
- API repository read-back: status `proposed`, revision 4, eight proposal rows, no error-severity findings, `published_at` nil. Source schedule events 19, 5 and 11 remain scheduled at their original weekday/period/week/room values. Browser console has zero errors or warnings. The proposal is still private and unpublished.
- Reloaded the Schedule page after the staged edits: all three placements and review findings persisted, selection returned as 0, and the publish button stayed disabled until an explicit row selection. This reload read the same owner-scoped run and did not change its revision.
- Exercised the publisher operation in an outer rollback-only database transaction with its inline Redis publisher replaced by a no-op. A selection containing only `generated-10-1` was rejected at final analysis because its source schedule still contains the three moved lessons; no write was reached. Selecting those three staged edits together with that generated row returned success: would create 1 event, update 3, advance to revision 5 and retain 4 proposal rows. The forced rollback restored schedule-event count, Outbox count and run state (`proposed`, revision 4, eight rows, `published_at` nil); all four inline Redis publishes were suppressed. This verifies the operation's success path without a committed timetable change, but not the HTTP/controller commit path.
- Exercised the same rejected single-row selection through the authenticated Rails form. The controller mapped the API conflict to a Russian alert, redirected to the same run, and `sessionStorage` restored the selected row at the unchanged revision. Added the three staged edits to the selection; the count reached four and the publish button stayed enabled. Cleared all rows again without submitting the compatible selection; the live run remains unpublished.

## 2026-09-30 — Reconfirm visible generation after the Generate action

- Started a new faculty generation from the authenticated Schedule workspace. Within roughly one second, the page showed the queued run, the active solver phase, five of five required units placed, feasible-solution count, branch/conflict counters, elapsed time, objective-bound updates, last solver-update age, and a visible stop action. After ten seconds, polling updated the same page in place: solution count and search counters changed while the run stayed private and active.
- Stopped the diagnostic run from the visible action. The page showed «Составление остановлено» and said the published timetable was unchanged. Authoritative read-back for run `1c798736-2e23-4aab-ae42-906d9ff9b777`: `cancelled`, event sequence 24, phase `cancelled`, progress retained at 5/5, and `published_at` nil. Schedule-event count remained 11 and Outbox count remained 85. Browser console errors: zero.
- This reconfirms the requested live process visibility without CRDT: sequenced HTTP polling and durable run progress are sufficient for the current single-admin workflow. No source schedule row or publication changed. No code or tests were added.

## 2026-09-30 — Verify committed row publication in an isolated database

- Restored a local PostgreSQL dump into a task-specific database clone and invoked the real `PublishScheduleGeneration` operation against the current, fresh eight-row private proposal. The operation committed all selected rows: five generated lessons and three existing-event edits. It returned `published`, revision 5, eight published rows, and zero remaining proposal rows.
- Read-back from the isolated database confirmed `published_at` set, run status `published`, proposal empty, 16 schedule events, and 93 Outbox rows. The shared database remained unchanged at 11 schedule events and 85 Outbox rows. Inline Redis notifications were replaced with a no-op for this one-off process; transactional Outbox writes remained enabled in the clone.
- Dropped the temporary database and removed its dump after read-back. This verifies the operation's committed transaction and Outbox path in isolation. The successful HTTP/controller response is still unverified; the live UI conflict-rejection and selection-retention paths are verified separately. No test files or application code were added.

## 2026-09-30 — Verify incremental cell publication and remaining draft

- Repeated the isolated-database operation with a four-row selection: the three staged existing-event edits plus `generated-10-1`. The real publisher committed that batch and returned `proposed`, revision 5, four published rows and four remaining rows. The remaining four generated placements stayed in the same private run.
- Read back the intermediate clone state before continuing: all four rows remained, the status was still `proposed`, and the snapshot digest matched a newly rebuilt source snapshot. Published only those four remaining rows in a second operation call; the run then became `published` at revision 6 with eight total rows published and none remaining.
- Final clone read-back: 16 schedule events, 93 Outbox rows, and a publication timestamp. The shared database remained at 11 schedule events and 85 Outbox rows. The clone and dump were removed. This verifies committed partial publication, rebasing, and final publication at the operation layer; no live timetable was published and no test files were added.

## 2026-09-30 — Check Rails publication success contract

- Ran the real Rails `ScheduleWorkspaceGateway#publish_generation` with a synthetic HTTP 200 response matching the API's committed partial-publication payload. The gateway parsed `published`, four accepted rows and four remaining rows, and sent the expected POST path, revision and accepted-key body. The Rails controller's success branch maps this response to the publication notice and redirects back to the same run.
- At this point, the successful authenticated browser/controller request remained unverified because the existing browser session had expired. The isolated operation commit and synthetic gateway response contract were independently verified; no live timetable mutation was made.

## 2026-09-30 — Verify authenticated API route and Rails success redirect in isolation

- Restored a fresh DB clone and sent two requests through `Rack::MockRequest` to the real Hanami route `POST /admin/schedule/generation_runs/:id/publish`, with short-lived synthetic super-administrator JWT claims for the cloned run owner. The first HTTP 200 published four compatible rows and retained a four-row proposal at revision 5; the second HTTP 200 published the remainder at revision 6. This exercised bearer authentication, route/action mapping, publication operation, and JSON response serialization without human credentials.
- Authoritative clone read-back showed `published`, revision 6, zero proposal rows, `published_at` set, 16 schedule events and 93 Outbox rows. The shared database remained at 11 schedule events and 85 Outbox rows. The isolated Redis container, clone database and dump were removed afterward.
- Separately invoked the real Rails controller's `publish` success method with a synthetic gateway result and a request/response context. It returned HTTP 303, displayed the expected Russian notice for one creation and three updates, and redirected to the same run. This checks controller success mapping but bypasses Rails authentication/routing callbacks; a fully authenticated browser submit remains unverified because the available browser session had expired. No application code or tests were added.

## 2026-09-30 — Align the synthetic wish corpus with compiler v20

- Current-container replay showed the deterministic compiler returns six supported proposals and four review findings for the ten-wish scenario. Wish `w4` is an unnamed two-consecutive-lessons request for a teacher with multiple requirements; current compiler policy correctly scopes it to that teacher, not to an inferred subject and not to review. The previously stored `expected_review` metadata and two prose descriptions were stale.
- Updated the synthetic scenario's `w4` expectation and aligned the scheduler README and architecture description with compiler v20: unnamed consecutive wishes are teacher-wide, unique explicit subjects are grounded to one requirement, and heater/oven reasons are never interpreted as subject names. The saved local-Jev evaluation remains an immutable historical record under the old `w4` disposition; the architecture note now gives its current-label rescore (4/10 rather than 3/10), with all four current review cases still incorrectly marked `propose` by that model.
- Verification on the running scheduler image: source hashes matched the worktree; compile produced 6 proposals/4 review findings and teacher scope for `w4`; CP-SAT returned all four units optimally; final analyzer had zero hard errors. No database rows, application code, or tests changed.

## 2026-09-30 — Repair run details and verify private progress access

- An isolated HTTP check of a proposed generation run found that the owner-scoped details endpoint raised `NoMethodError` on Rails' `.presence` helper, which is not loaded by Hanami. Replaced that call with a plain Ruby empty-string check in `GenerationRunsShow`.
- Rebuilt and restarted the running API image. Against the live service, synthetic signed claims for the recorded run owner returned HTTP 200 for both details and progress; a different synthetic `super_admin` received HTTP 403 for details, progress and a publish attempt. The check emitted only actor labels and response codes.
- Repeated the same access check against an isolated clone before rebuilding. Dropped that database clone, removed the temporary Redis container and dump, and confirmed the shared published schedule still contains 11 events and the recorded run remains proposed. No publication or other schedule write occurred.
- `ruby -c` passed. After the denied publish attempt, authoritative read-back still showed the private run proposed at revision 4 with eight rows and the published schedule at 11 events. The browser session had expired, so no new authenticated UI journey is claimed; earlier live browser verification of progress, draft repair and row selection remains the UI evidence.

## 2026-09-30 — Verify the complete Rails publication flow on an isolated clone

- Restored the live database into a task-specific PostgreSQL clone and started temporary Rails, Hanami and Redis services against that clone. Signed in through the normal administrator form and opened the existing eight-row private proposal.
- Selected the staged edits together with one generated placement and submitted the real Rails publication form. Rails showed the notice for one created lesson and three updated existing lessons; the run remained `proposed` at revision 5 with four rows still private. Selected and published the remaining four rows through the same form; Rails showed four created lessons.
- Clone read-back after both batches: run `published` at revision 6, proposal empty, publication timestamp set, 16 schedule events and 93 Outbox rows. This verifies the browser form, authenticated Rails controller, gateway, real Hanami route and transactional publisher together.
- Signed out of the temporary UI and removed its Rails/API/Redis containers, database clone and dump. Shared database read-back remains 11 schedule events and 85 Outbox rows; the shared run remains proposed at revision 4 with eight rows. No live timetable was published and no test files were added.

## 2026-09-30 — Recheck the clarified wish and solver path on the running worker

- Replayed the checked-in synthetic scenario through the running scheduler HTTP endpoints `/v1/compile-preferences`, `/v1/analyze` and `/v1/solve`, without creating a generation run. Compilation returned six proposals and four review findings; the generic oven/heating consecutive wish remained teacher-wide, and room software stayed review-only. Analysis reported the scenario's expected hard conflicts. CP-SAT returned four placements with `optimal` status and zero hard findings in its generated solution.
- A direct compiler boundary check confirmed a positive Monday-period-1 wish that conflicts with the hard profile returns `PROFILE_TEXT_CONTRADICTION` for administrator review and no proposal. The negative Monday-period-1–2 wish remains a soft rule; it does not modify profile constraints.
- SHA-256 hashes for compiler, solver and analyzer matched the running container to the worktree. Shared database counts remained 11 schedule events and 85 Outbox rows. No database mutation or test file was added.

## 2026-09-30 — Recognize common explicit negative wish forms

- Current-worker probing showed that “Предпочитаю не проводить занятия в понедельник…” was needlessly sent to review, while the equivalent “Не могу вести занятия…” was already supported. Added a narrow set of explicit negative teaching verbs and “нежелательно” forms; these still require a recognized weekday and slot before producing soft unavailability.
- Advanced the wish compiler version to `russian-templates-v21`, so an approval can never outlive a changed parser. Two v20 wishes are currently approved; they remain untouched now and will be returned for administrator re-review on the next snapshot build. No schedule or wish records were changed during this implementation.
- Source-mounted scheduler checks passed for four negative phrasings, including “предпочитаю не проводить” and “первая пара нежелательна.” A positive wish conflicting with a hard profile unavailability still produced `PROFILE_TEXT_CONTRADICTION` and no proposal. Python byte-compilation and Ruby syntax checks passed; no test files were added.
- Rebuilt API, generation worker and scheduler. The running API reports compiler v21, and an HTTP request to the rebuilt scheduler produced the new soft unavailability rule while leaving the profile-conflicting positive wish in review. The two v20 approvals and shared schedule counts remained unchanged after deployment; re-review occurs only during a later snapshot build.
- Verified that later transition in a disposable database clone by calling the real `BuildGenerationSnapshot`: both v20 approvals became review-only and zero wishes entered `approved_preferences`. Removed the clone, dump and isolated Redis. The shared database still has both v20 approvals, 11 published events and 85 Outbox rows; its private run remains proposed at revision 4.

## 2026-09-30 — Route double-negated wishes to administrator review

- Adversarial probing found that v21 interpreted “не нежелательна”, “не могу не вести” and similar double negatives as a negative scheduling preference. Added a conservative ambiguity guard for double-negative adjectives and explicit teaching-action constructions; it returns `AMBIGUOUS_PREFERENCE` with no proposal.
- Advanced the compiler to `russian-templates-v22` and documented the boundary. Inline checks pass for four clear negative forms and four double-negative cases. A compiler-version change leaves existing v20 wishes stale for the next snapshot; no wish or schedule row was changed during the check.
- Rebuilt API, generation worker and scheduler. The live scheduler HTTP endpoint returned four soft unavailable rules and four `AMBIGUOUS_PREFERENCE` findings for the same eight cases; the API reports compiler v22. Shared service state remains unchanged.

## 2026-09-30 — Cover additional double-negative verb forms

- Further probes showed v22 missed double negatives whose second verb was “провести”, “прочитать”, or “посещать”; each had been miscompiled as soft unavailability. Generalized the ambiguity guard to modal phrases followed by Russian infinitives, including reflexive infinitives. These phrases now return review findings instead of solver proposals.
- Advanced to `russian-templates-v23`. Source-mounted checks preserve three clear negative forms and route five double-negative variants to `AMBIGUOUS_PREFERENCE`. Ruby and Python syntax checks passed; no wish or timetable data was changed.
- Rebuilt API, generation worker and scheduler. The running API reports v23; the live scheduler HTTP endpoint returned three soft unavailability proposals and five ambiguity findings. Shared wish states, 11 schedule events and 85 Outbox rows remain unchanged.

## 2026-09-30 — Verify admin-visible progress from a fresh university run

- On the live Rails administrator page, clicked «Составить для университета». The POST returned immediately to a private run (`818ab79b-d866-4e16-a91e-29d5813c6245`) in `queued`; the published timetable remained separate.
- The same page automatically advanced to `solving` and showed 5/5 lesson units placed, one feasible solution, 1,656 search branches, objective 263, bound -19,450, elapsed time, and time since the solver's last callback. Subsequent browser snapshots showed elapsed/idle time advancing without a page reload. Scheduler container CPU was about 100%, confirming the solver remained active while progress was visible.
- Cancelled this verification run from the admin control. The page reloaded the durable `cancelled` state and displayed «Опубликованное расписание не изменилось»; scheduler CPU returned to idle. Reloading the run URL with semester 1 preserved the terminal state. No publication occurred and no source/test files changed in this verification.
- Ruby 3.4.2 runtime check confirmed `Net::HTTP#read_timeout = nil` disables the default 60-second read timeout. With `SCHEDULER_SOLVE_SECONDS` unset, a long solve therefore remains observable until completion or administrator cancellation; no CRDT is involved.

## 2026-09-30 — Recheck faculty and university weekly-scope views

- On the authenticated current Rails runtime, opened the aggregate weekly timetable for faculty 1 / semester 1, then switched to university scope. Both rendered one table per active group with the requested weekday/time axes, a group search, conflict markers and a link to start scope-appropriate generation. The current data has one active group in this semester, so this browser visit does not demonstrate a rendered empty-group table.
- Traced the blank-grid path: Hanami's `StudyingGroups#for_semester` selects in-course `student_group_semesters` independently of timetable rows; Rails' aggregate presenter seeds groups from that roster before adding recurring events. A roster group without events therefore receives an empty weekly grid in source behavior. No database or schedule mutation occurred.

## 2026-09-30 — Keep cancellation on the active generation URL

- A live cancel/reload check exposed a nested-Turbo navigation race: the cancel POST returned the correct semester-1/run redirect, but the browser could replace the address with a stale semester-4 context and drop the run ID. The run stayed cancelled; this was a navigation defect, not a solver or publication error.
- Set the cancel form's Turbo target to `_top`, matching the generation form's top-level navigation. Rebuilt the Rails image and repeated the university Generate → Cancel flow from a clean tab. The cancelled run (`eabb3494-1803-4713-b512-ce13eff7f46f`) remained at `/admin/schedule?generation_run_id=…&semester_id=1`; after a full reload it still showed the same cancelled run and the message that the published timetable was unchanged.
- Scheduler CPU returned to idle after cancellation. Browser console errors: zero. ERB asset precompilation and `git diff --check` passed. No publication, new test file or timetable mutation occurred.

## 2026-09-30 — Keep calendar-specific teacher wishes in review

- Inline compiler probes found unsafe broadening in v23: “первый понедельник месяца” and “раз в две недели” became weekly rules, while “только после второй пары” was interpreted as one exact available slot. None of these scopes exists in the typed IR.
- Added a conservative review boundary for ordinal weekdays tied to month/semester/week, multiweek cadence, and relative lesson-period phrases; advanced the API compiler version to `russian-templates-v24`. Ordinary weekly soft wishes remain unchanged. Because a compiler-version change invalidates prior approvals at snapshot time, I checked the shared database first: it currently has no approved wish rows, so no active approval was silently affected.
- The frozen ten-wish synthetic scenario still returns six proposals and four findings. Source-mounted probes route all three risky examples to `UNSUPPORTED_PREFERENCE`, retain “Не могу в понедельник 1–2 пару” as a soft two-slot rule, retain “Предпочитаю не проводить…” as soft unavailability, and keep a wish opposing hard profile unavailability in `PROFILE_TEXT_CONTRADICTION` review.
- Rebuilt API, generation worker and scheduler. Runtime Hanami reports compiler v24; the live scheduler HTTP endpoint returns review findings for the unsupported scopes and valid soft proposals for ordinary weekly rules. Shared database read-back remains 11 schedule events, 85 Outbox rows, and zero approved wishes. Python byte-compilation and Ruby syntax pass; no tests/files or schedule/wish rows were added.

## 2026-09-30 — Keep calendar-specific teacher wishes in review

- Compiler v23 incorrectly broadened “first Monday of the month” and “every other week” into weekly rules, and treated “only after the second period” as one exact available slot. Those scopes are not representable in the current typed rule schema.
- Added a fail-closed review boundary for ordinal weekdays tied to calendar periods, multiweek cadence, and relative lesson-period windows; advanced the API compiler version to `russian-templates-v24` so existing approvals become stale on the next snapshot build. Ordinary weekly wishes keep their existing soft-rule behavior.
- Replayed the frozen ten-wish scenario: six proposals and four review findings. Focused source probes route all three unsupported temporal examples to `UNSUPPORTED_PREFERENCE`, while “Не могу в понедельник 1–2 пару” remains one soft two-slot rule. Positive wishes conflicting with hard profile unavailability remain review-only.
- Python byte-compilation, Ruby syntax validation, and targeted `git diff --check` passed. No test files, wish rows, or timetable rows were added or changed. The running API and scheduler had previously been rebuilt for v24; their runtime health was reconfirmed during this continuation. Shared schedule state remains 11 events and 85 Outbox rows.

## 2026-09-30 — Keep relative period boundaries in review

- Adversarial follow-up found “В понедельник могу вести занятия не раньше третьей пары” became a soft preference for only period three. Added “не раньше/позже/ранее/позднее N-й пары” to the relative-window review guard and advanced the compiler version to `russian-templates-v25`, invalidating prior approvals on the next snapshot under the existing stale-version policy.
- Inline probes route four boundary variants to `UNSUPPORTED_PREFERENCE`; an ordinary Monday period 1–2 avoidance remains a soft `unavailable_slot`. The frozen scenario still compiles to six proposals and four findings. Python byte-compilation and Ruby syntax checks pass.
- Rebuilt the local scheduler and API/worker images. A live request to the rebuilt scheduler returned the relative-boundary review finding and the ordinary weekly soft proposal; the API image's compiler source hash matches the v25 worktree file. API, scheduler and web containers are healthy. No wish or published schedule data changed; no tests were added.

## 2026-09-30 — Verify v25 invalidates older approved compiler output

- The shared semester currently has no approved wish; its review records are v19/v20. Used the established rollback-only database transaction to temporarily simulate a context-current v24 approval for a teacher with active semester workload, then invoked the real `BuildGenerationSnapshot` under v25.
- The snapshot operation moved the simulated approval to `review`, added the stale-approval finding, and excluded its typed rule from `approved_preferences`. After forced rollback, read-back matched the selected record's exact prior status, compiler version and context fingerprint. No shared wish or schedule change persisted.
- This verifies that the relative-boundary parser change cannot leave previously approved v24 output active in the solver. No tests or test files were added.

## 2026-09-30 — Verify teacher-wish priority over compactness

- Ran a solver-only counterexample against the rebuilt CP-SAT container. Two lessons share one group: one teacher can teach either Monday period 1 or Tuesday period 2, the second lesson is fixed to Monday period 2, and an approved soft wish avoids Monday period 1. The preference-aware optimum places the first lesson Tuesday despite opening a second group day; with the wish removed, the optimum packs both lessons onto Monday.
- Both runs placed all required lessons with no unmet-wish finding in the preference-aware case. The runtime `solver.py` hash matches the worktree. This verifies the requested ordering: required placement first, approved teacher wishes next, then compact days/gaps and earlier-period tie-breaks. No application/database state changed and no test files were added.

## 2026-09-30 — Catch punctuated relative-period wishes

- New adversarial phrases showed that “не раньше, чем на третьей паре”, “не ранее чем на третьей паре”, “не раньше начала третьей пары”, and matching “не позже/не позднее” forms were still being compiled as an exact period wish. Expanded the relative-window guard across punctuation and short explanatory wording; advanced the parser version to `russian-templates-v26`.
- Six relative-boundary variants now return `UNSUPPORTED_PREFERENCE`; a normal Monday period 1–2 soft avoidance still compiles. The frozen scenario remains six proposals/four findings. Python compilation, Ruby syntax, and `git diff --check` pass.
- Rebuilt API, generation worker, and scheduler. The live scheduler endpoint passed the same boundary probes; Hanami runtime reports v26. API and scheduler source hashes match the worktree, and the services are healthy. No wish or timetable rows changed; no tests were added.

## 2026-09-30 — Re-run Generate → live progress → Cancel on the current runtime

- Against the rebuilt v26 API/scheduler, opened the authenticated Schedule page and started a university run. The browser navigated to its private run URL immediately; the panel showed the solver phase, 5/5 placed units, search metrics, objective/bound and a stop action. After a five-second wait, the same page showed newer elapsed/solver-idle values without a reload.
- Cancelled through the administrator control. Browser read-back showed the durable `cancelled` state and that the published timetable was unchanged. Hanami read-back showed `published_at` nil and 11 schedule events. Browser console had zero errors/warnings; API, scheduler, worker and web containers were healthy.
- No timetable row was published or modified, and no tests were added.

## 2026-09-30 — Keep longer consecutive-lesson requests out of the two-unit rule

- Adversarial compiler probing found that “three lessons/classes in a row”, “four lessons”, “several lessons”, and ordinal/range counts were being broadened into the supported two-unit consecutive preference when the text used nouns other than “пары”.
- Expanded the count boundary across pair, lesson, and class nouns. Counts other than two, ordinal counts, ranges and vague quantities now return `UNSUPPORTED_PREFERENCE`; explicit two-pair/two-lesson wishes remain soft proposals. The frozen scenario remains six proposals/four findings. Python compilation, Ruby syntax, and `git diff --check` pass.
- Rebuilt API, worker and scheduler. The live endpoint passed all ten count variants; Hanami reports compiler v27, runtime source hashes match the worktree, and API/scheduler/web are healthy. No wish or timetable records changed; no tests were added.

## 2026-09-30 — Reject non-lesson and qualified consecutive quantities

- Follow-up probing found “three lectures in a row”, “two days/weeks in a row”, and “more than two pairs” could still be broadened into the two-lesson wish. Reworked count handling so only an exact two with a recognized pair/lesson/class noun is supported; longer, ranged, ordinal, vague, qualified, or non-lesson quantities stay in review. Advanced the compiler version to `russian-templates-v28`.
- Fourteen focused variants passed: the unsupported forms return `UNSUPPORTED_PREFERENCE`, while explicit two-pair/two-lesson wishes and the heater rationale remain teacher-scoped soft proposals. The frozen ten-wish scenario remains six proposals/four findings. Python compilation, Ruby syntax, and `git diff --check` pass.
- Rebuilt API, worker and scheduler. The live endpoint passed the same variants; Hanami reports v28 and both compiler source hashes match the running images. API, scheduler and web services are healthy. No wish or timetable rows changed; no tests were added.

## 2026-09-30 — Verify v28 review-only wishes through Hanami snapshot construction

- Exercised the real `CompileTeacherWish` operation and `TeacherScheduleWishRepo#create_submission` inside a rollback-only transaction, using “Хочу три лекции подряд.” Hanami accepted the scheduler response, stored the temporary row as `review` with compiler v28 and the expected `UNSUPPORTED_PREFERENCE` finding.
- Called the real `BuildGenerationSnapshot` with that row present. The snapshot included the wish as review-only and emitted no approved solver preference for it. Forced rollback restored the database, and repository read-back confirmed the probe row no longer existed.
- This verifies the new count boundary through compiler HTTP integration, API response validation, persistence status, and solver-snapshot filtering without leaving a wish record behind. No tests or timetable rows were changed.

## 2026-09-30 — Explain live solver activity during long searches

- The admin progress panel already receives two-second heartbeat updates, but when CP-SAT had a complete feasible arrangement and was optimizing it without a new incumbent, the phase label still said it was searching for placements. The panel now distinguishes improving a complete schedule from searching for placements, and explicitly reports when the search is still running but no new solver event has arrived recently.
- Rebuilt the Rails image and verified the active university run in the browser: it reported a complete 5/5 arrangement, one feasible solution, search metrics and the revised optimization/last-event message while heartbeat elapsed time advanced without a reload. Stopped the run through the admin control; the page confirmed the published timetable was unchanged. Browser console errors: zero. JavaScript syntax validation passed; no test files were added.

## 2026-09-30 — Enforce owner-only access for generation drafts

- A source audit found that generation creation stored `requested_by_account_id`, but detail/progress reads and several draft mutations selected by run UUID alone. Bound detail and progress reads, cancellation, proposal edits, and publication to the requesting account; write operations now repeat the owner condition in their SQL updates and row-lock lookup.
- Rebuilt Hanami API and the generation worker. A rollback-only runtime probe verified an owner can read the run while a different account cannot read its detail/progress or cancel it; a proposed draft could not be locked, edited, or advanced to publication by another account. All temporary rows rolled back. Browser read-back through the current owner still returned their cancelled run; the published timetable remained unchanged. Ruby syntax checks passed; no tests were added.

## 2026-09-30 — Verify red timetable findings and private conflict repair

- On the authenticated Schedule page, «Проверить расписание» reported four seeded errors; following a finding opened the corresponding lesson and rendered its cell with the conflict class and red background. No published event was edited in this inspection.
- Created an owner-bound university draft through the real `GenerateScheduleRun` operation with a three-second, process-local solver limit for this verification only; the app's normal no-limit setting was not changed. The draft reached `proposed` with five generated placements and five findings (three unavailable-time conflicts in existing events and two teacher-wish review findings).
- Staged an edit of event 19 inside the draft. The analyzer flagged a trial destination at Thursday period 5 with teacher/group overlap findings; changing it to Wednesday period 5 removed that lesson's unavailable-time finding. The final draft shows six proposal rows, four remaining findings, and keeps row publication disabled until all errors are resolved. Database read-back confirmed published event 19 remains Monday period 1 and the run has no `published_at`. The owner can open the review through `generation_run_id=e6e039a6-37e8-41fc-b831-7c4095f01e28`; this unpublished sample run is retained for administrator inspection. The generation worker was restarted and is healthy.

## 2026-09-30 — Resolve published conflicts inside the retained private run

- Reopened the owner-bound university run `e6e039a6-37e8-41fc-b831-7c4095f01e28` and used the finding links to stage corrections for recurring events 5 (Automobiles) and 11 (Object-oriented programming). Moved the first to Tuesday period 3 and the second to Friday period 3. The analyzer removed both hard teacher-unavailability findings; two review-only teacher-wish findings remain.
- Browser read-back shows eight proposal rows, zero error-severity findings, enabled per-row selection and a disabled publish button until a row is selected. Toggling one row enabled the button; clearing the selection disabled it again. No publication request was submitted. The run remains `proposed` at revision 5 with `published_at` nil. Database read-back confirms the source events retain their original weekday/period values and the shared timetable still contains 11 events.
- No proposal row was selected or published. API, scheduler, worker and web containers are running; browser console errors/warnings: zero. No tests or test files were added.

## 2026-09-30 — Route alternative period wishes to review

- A live parser probe found that “Monday, period 1 or 2” could be compiled as a soft preference for both slots; “period 1 or 2” could also be reduced to only period 1. Those interpretations are not equivalent to a selected alternative and could skew the solver objective.
- The v29 compiler now sends alternative periods joined by “or/either” or slash notation to `AMBIGUOUS_PREFERENCE`, alongside alternative weekdays. Conjunctions, explicit ranges, a single period, teacher unavailability, and the heater/two-consecutive example retain their supported outputs. Nine focused cases passed against the live `/v1/compile-preferences` endpoint.
- Before advancing the version, database read-back found zero approved teacher wishes. Rebuilt the scheduler and Hanami API images and restarted the generation worker. Hanami reports `russian-templates-v29`; the running scheduler compiler SHA-256 matches the worktree. API, scheduler, worker and web containers are healthy. Python compilation, Ruby syntax and `git diff --check` passed. No wish or published schedule data changed; no tests were added.

## 2026-09-30 — Keep non-integer consecutive counts review-only

- Adversarial probes found the compiler treated “3-х пар подряд” and “две с половиной пары подряд” as the supported two-lesson preference. The count parser now recognizes inflected numeric forms and fractional language; only an exact count of two is proposed. Other inflected counts, fractions, decimals, ranges and larger integer counts produce `UNSUPPORTED_PREFERENCE`; “2-х занятий”, “две пары из-за печки” and ordinary exact-two lesson wording remain supported.
- Advanced the compiler to `russian-templates-v30` after a current database read found zero approved wishes. The rebuilt live `/v1/compile-preferences` endpoint passed twelve count cases. Hanami reports v30, and the running scheduler compiler hash matches the worktree. Python compilation, Ruby syntax and documentation `git diff --check` passed; API, scheduler, worker and web containers are healthy.
- Authoritative database read-back still shows the retained run `proposed` at revision 5, eight private proposal rows, two review-only findings, zero error findings, `published_at` nil and 11 published schedule events. No wish or timetable data changed; no tests were added.
- Exercised the real Hanami `CompileTeacherWish`, wish repository and `BuildGenerationSnapshot` in a rollback-only transaction using “В понедельник предпочитаю первую или вторую пару.” The stored v30 result had no proposed rule and one ambiguity finding; the snapshot retained it as a review wish and emitted no approved solver preference. The temporary row was absent after rollback and the wish-table count was restored.

## 2026-09-30 — Keep non-lesson counts out of consecutive-lesson wishes

- A live v30 probe found “two days/weeks/periods of lessons in a row” could be read as the supported consecutive-lesson preference because the parser found a lesson noun later in the sentence. The compiler now detects counts attached to non-lesson units (days, weeks, days-of-week, semesters, years, courses, shifts, hours, periods and occurrences) and routes them to `UNSUPPORTED_PREFERENCE`.
- The rebuilt live endpoint passed ten cases: nine non-lesson/larger/fractional quantities went to review; exact “2-х занятий” and the heater/two-pair request remained proposals. Hanami v31 compilation, wish persistence and snapshot filtering passed in a rollback-only transaction; the temporary review row was removed.
- No approved wishes existed before the v31 bump. The retained generation run remains private and unpublished; no shared teacher-wish or published-schedule rows changed. API, scheduler, worker and web containers are healthy. Python compilation, Ruby syntax and documentation `git diff --check` passed; no tests were added.
- Follow-up implementation: the administrator Teachers workspace now has a semester-scoped workload tab showing assigned lessons, groups, activities, assigned/actual/remaining hours and current rooms. Room actions open the existing requirement-scoped assignment editor, which preserves current teacher and room selections. The administrator wish-review link carries the selected teacher and semester; the API's admin wish-list response includes `teacher_id`, and review redirects preserve the teacher filter. Wish authorship is resolved: teachers submit in their cabinet and administrators review. Runtime verification below passed; no schedule or room assignment was mutated during the UI walkthrough.

## 2026-09-30 — Add teacher workload and wishes tab

- Added the semester-scoped “Нагрузка и пожелания” tab to the administrator Teachers workspace. The selected teacher’s requirements show subject, student group, activity, assigned hours, completed hours, remaining hours and room. Empty and unavailable states are explicit. A room action opens the established searchable assignment editor at the requirement’s department; that entry path does not require a redundant faculty selection.
- Confirmed wish authorship with the user: teachers submit wishes through their own cabinet; administrators review them. The tab links to the existing semester review page filtered to the selected teacher. Added `teacher_id` to the administrator-only wish-list response so filtering does not depend on teacher names; approval/rejection forms preserve the filter.
- Browser walkthrough against rebuilt web/API images showed seven load rows for the selected sample teacher/semester, four wish cards all belonging to that teacher, and no browser errors. The room editor preselected the existing teacher and room. No write form was submitted. Rails eager-load and changed Ruby syntax checks passed; API action syntax and scoped `git diff --check` passed. No tests or test files were added.

## 2026-10-01 — Let administrators author workload-scoped wishes

- Added “Добавить пожелание” to assigned workload rows. The side sheet identifies the load record, requires an explicit choice among its assigned teachers, and keeps the natural-language draft on recoverable failure. The saved wish records the submitting admin account separately from the affected teacher and stores a foreign-key link to the workload requirement.
- The API checks both administrator ownership scope and that the selected teacher is still assigned to the requirement in the selected semester. The deterministic compiler now anchors consecutive-lesson and weekday/period rules to that requirement. Solver costs and static analysis honor the same scope; wishes still remain proposed soft rules until a super-administrator approves them. The review list identifies administrator-authored wishes.
- Browser verification opened the editor from a real assigned row and confirmed the form context; a first pass caught a missing optional Stimulus target, which was fixed. The rebuilt page then opened with zero browser console errors. The existing wish-review page loaded with author labels and zero errors. A live API compilation and a rollback-only repository submission probe passed; wish-row count remained unchanged. No wish or schedule data was written, and no tests were added.

### 2026-10-12 — Excel release verification

Published Docker release `2026-10-12-1` with the existing 120-second single-attempt Excel upload deadline and standalone scanner Shellwords dependency. Local multipart upload reached API 201, MinIO, outbox/Redis, and worker schema validation; diagnostic files were removed without importing curriculum data. Production authenticated reproduction returned the generic error after 5.34 seconds but a later history read showed the upload had committed; its diagnostic file was deleted through the UI endpoint. Exact production exception is unconfirmed without server logs. Update instructions are in `deploy/EXCEL_UPLOAD_RELEASE_2026-10-12.md`, including per-image overrides and discovery preflight. Playwright navigation was blocked by proxy connection refusal; verification used direct authenticated HTTP, so no visual acceptance is claimed.

## 2026-10-16 — production socket exhaustion repair

Rails commit e729d8a closes each outbound HTTP pool as well as its response, including errors and cancellation; readiness API calls have a two-second deadline. Production static-file serving is explicit. API commit 9aba520 starts Puma directly. Source is published on codex/production-stability-2026-10-16 in the owning repositories; Docker images use tag 2026-10-16-1. Deployment details and limitations are in deploy/DEPLOYMENT_GUIDE.md and deploy/image-releases/2026-10-16-1.json.

The same-process socket diagnostic reproduced growth from 9 to 209 descriptors on 100 old-client calls (including diagnostic server sockets). The fixed client stayed at 9; 20 HTTP-500 calls and 10 cancellations also returned to 9. The rebuilt real Falcon worker stayed at 9 descriptors across 100 readiness probes. Both Rails replicas and direct Puma returned readiness 200. API stop made Rails unready, and API restart restored readiness without Rails restart. Seven compiled CSS/JS assets returned 200; Playwright MCP loaded the public selection page. No visual redesign or full administrator journey is claimed.

The ClamAV CDN returned 403/cooldown during local verification; successful live signature updates remain blocked by upstream network access. Freshness checks reject stale databases, and the updater retries hourly instead of rapid restarts. No remote server deployment or multi-day soak is claimed. Local project containers are stopped again after checks.

## 2026-10-17 — simplified single-host runtime

A dedicated deployment agent removed Consul/ACL/three registrars and replaced the Python edge supervisor with native Docker DNS refresh. The optional operations console no longer causes idle DNS retries. Default Rails count is one; business workers and all data volumes remain. New deployment instructions and exact evidence are in deploy/DEPLOYMENT_GUIDE.md and deploy/image-releases/2026-10-17-1.json.

Rails 1646796 checks API readiness even with discovery disabled. API ddf921c gates required scans on signature freshness and returns 503 before accepting an Excel upload while unavailable. Excel deefab6 selects its installed psycopg2 driver in direct mode. Five images are published under 2026-10-17-1; scheduler retains its previous tag.

Local verification: cached startup 17.01s, 250 readiness probes at 9 descriptors afterward, 180-second idle check range 9–11 ending at 9, API IP replacement without Rails restart/Nginx reload, admin login and persisted faculty read-back, Excel worker healthy, public Playwright load without console errors, stale-signature upload 503 with no new record, direct db version command. No remote server deployment, multi-day soak, full business import/export or successful live CDN refresh is claimed. Local containers are returned to stopped state after verification.

Follow-up: worker PID 9 remained at 9 descriptors at 38,889 seconds of monotonic process age. This is a later snapshot, not continuous monitoring of the entire interval.


## 2026-10-19 — independent outage UI and bounded host recovery

Implemented static Russian Nginx outage HTML/CSS/JS with the existing ink/velvet/almond identity, browser/JSON gateway distinction, safe GET retry and no automatic replay of ambiguous writes. Edge starts without healthy backends; API business errors remain structured. Infrastructure now supplies a project-scoped systemd recovery timer with dependency gating, grace, cooldown and restart budgets. Four API worker polling loops emit completed-batch heartbeats; Docker healthchecks and the controller can identify stalled loops without a new sidecar.

Isolated checks passed: absent backends, failed POST handling, mixed healthy/failing Rails addresses, DNS recovery, real unhealthy restart, budget/dependency/manual-stop/project isolation, four empty-queue heartbeats and 1000 writes with stable descriptors. A fresh database stack passed migration, seed and all 12 non-antivirus service healthchecks. Playwright/Chromium at 1440×1000 and 390×844 verified content, responsive geometry, status transition, keyboard focus and safe retry. Browser plugin unavailable; diagnostics/screenshots retained under /tmp only. Generated host units pass systemd-analyze verify; no timer installed on the shared workstation. ClamAV CDN and whole-host redundancy remain outside the result. See deploy/DEPLOYMENT_GUIDE.md for rollout and rollback. Only infrastructure/API repositories are publication targets; milk_proto is unrelated and must not receive further workspace pushes.


## 2026-10-19 — consolidate the deployment runbook

All current installation, upgrade, Consul migration, recovery, antivirus, diagnostics and rollback procedures now live in deploy/DEPLOYMENT_GUIDE.md. Removed five overlapping/obsolete guide files; README and server packaging reference the single guide. Preserved the mixed published image versions, data-preserving update rules, first-install-only seed, timer acceptance and verification limits. Documentation links, shell syntax and archive contents checked; no runtime rebuild/redeployment required.
