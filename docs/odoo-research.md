# Odoo research brief — ABA project

_Researched 2026-11-17. Hosting target: **Odoo.sh** (Enterprise, Custom plan) with custom modules._
_Items marked ⚠️ come from secondary sources or could not be confirmed on odoo.com — verify before quoting to the client._

---

## 1. TL;DR

- **Odoo** = modular open-core ERP. Python + PostgreSQL backend, own ORM, XML views, OWL (JS) frontend. Every feature is an "app"/module.
- **Current version: Odoo 20.0** (released at Odoo Experience, Sept 2026). Odoo 19.0 = Sept 2025. Supported: 18, 19, 20 (3 majors, ~3 years each).
- **Odoo.sh** = Odoo's PaaS: GitHub-driven, branches mapped to Production / Staging / Development, CI builds, daily backups, shell/SSH. **No root, no apt packages, no Postgres extensions.**
- Odoo.sh **requires the Enterprise Custom plan** (per-user licence) **+ separate hosting fees** (workers, storage, staging envs).
- **Big rule:** configuration → Studio (sparingly) → custom module. Every line of custom code is our cost at every yearly upgrade; Odoo's upgrade service migrates *standard* data only.
- ⚠️ **Decide 19.0 vs 20.0 first.** 20 is current but reportedly not all tooling caught up (Odoo.sh version picker, OCA ports, upgrade service). Odoo 20 also changes security files (`ir.access.csv`), OWL 3, etc. — code written for 19 needs porting.

---

## 2. What Odoo is

**Architecture**
- Backend: Python (Odoo 20 ⚠️ requires Python 3.12+, PostgreSQL 16+), PostgreSQL only.
- Modules (addons) with a `__manifest__.py` declaring deps, data, assets.
- ORM models, XML views (form/list/kanban/search/pivot/graph/calendar; Enterprise adds gantt/map/cohort/grid), QWeb PDF reports.
- Frontend: OWL (Odoo 20 ships Owl 3).
- APIs: **JSON-2** (`/json/2/<model>/<method>`, bearer API key) is the new standard; XML-RPC/JSON-RPC are deprecated (removed in Odoo 22, fall 2028).

**App catalog**

| Area | Apps |
|---|---|
| Finance | Accounting, Invoicing, Expenses, Spreadsheet (BI), Documents, Sign, ESG |
| Sales | CRM, Sales, POS (shop/restaurant), Subscriptions, Rental, marketplace connectors (Amazon…) |
| Websites | Website builder, eCommerce, Blog, Forum, Live chat, eLearning |
| Supply chain | Inventory, Barcode, Manufacturing (MRP), PLM, Purchase, Maintenance, Quality |
| HR | Employees, Recruitment, Time Off, Attendances, Appraisals, Referrals, Fleet, Payroll |
| Marketing | Email/SMS marketing, Social, Marketing Automation, Events, Surveys |
| Services | Project, Timesheets, Helpdesk, Planning, Appointments (**Field Service folded into Planning in v20**) |
| Productivity | Discuss, Approvals, To-Do, Calendar, VoIP, Knowledge, IoT, AI agents |
| Customization | Studio |

---

## 3. Versions & lifecycle

- One major per year (X.0, Sept/Oct). Odoo **Online** also gets SaaS releases X.1–X.4 — **these never run on Odoo.sh**; Odoo.sh = major versions only.
- Support: last 3 majors (~3 years each). On Odoo.sh: +2 years grace to upgrade, 25% surcharge after 3.5 years, phase-out at 6 years.
- 17.0 support ended Oct 2026; 18.0 ends Oct 2027.

**Odoo 20 highlights (relevant for scoping)**
- AI: agents can create/update records, MCP support — **all AI uses paid IAP credits**.
- Accounting: parent accounts replace account groups; bank-consistency rule; payment status renamed ("In Process"→"Paid", "Paid"→"Reconciled").
- Inventory: valuation without Inventory app, bulk lot/serial generation, demand-based min/max suggestions, stock at past date.
- MRP: continuous production, split MOs, work-order Gantt/Kanban.
- Sales: dashboard, product-less description lines, single-use discount codes.
- Project: budget & margin reports; Field Service → Planning (technician map, routing).
- Framework: **`ir.access` replaces ACL csv + record rules**, tracking values computed on the fly, offline mode.

---

## 4. Community vs Enterprise

- **Community** — LGPLv3, free, self-hosted only.
- **Enterprise** — Community + private `odoo/enterprise` addons, proprietary OEEL licence; required for Odoo.sh.

**Enterprise-only (main ones):** Studio, mobile apps, full Accounting (reports, reconciliation, assets, budgets, consolidation, follow-ups), bank sync ⚠️, OCR bill digitization, most localization/e-invoicing, Documents, Sign, Spreadsheet dashboards, Payroll, Appraisals, Subscriptions, Rental, marketplace connectors, VoIP, Barcode, MRP work-center planning/shop floor, PLM, Quality, Maintenance, Helpdesk, Planning, Appointments, Approvals, timesheet grid, Marketing Automation, Social, Knowledge, IoT, AI features, **free version upgrades via upgrade.odoo.com**.

---

## 5. Pricing (varies by country — always quote from the client's country page)

| Plan | Notes | Indicative price |
|---|---|---|
| One App Free | 1 app, Online only | Free |
| Standard | All apps, **Online only**, no Studio / multi-company / external API / custom code | ~US$24.90/user/mo (yearly) |
| **Custom** | + Studio, multi-company, external API, agentic AI; Online, **Odoo.sh** or on-prem | ~US$49 (Americas); EU €35.90 (from Sept 2026) ⚠️ |
| Light user (new, v20 / agreement v13) | Limited seat | ~US$8.90 / €7.90 ⚠️ |

- **Odoo.sh hosting extra** (⚠️ third-party figures, check live calculator): ~$72/worker/mo, ~$0.25/GB/mo, ~$18/staging env/mo, ~20% off yearly. Shared: 1–16 workers, ≤512 GB, 0–20 staging; beyond that = Dedicated.
- Portal users (customers/vendors) are free.
- ⚠️ New agreement v13 (Sept 2026): employees without a user account may be billed as Light Users — matters if client has many kiosk/attendance-only staff.

---

## 6. What Odoo is NOT good at (set expectations early)

- **Upgrade cost of customization** — every year changes ORM/views/OWL/data models. Heavy customization = expensive upgrades (we own migration of custom code).
- **Complex manufacturing** — weak at finite-capacity APS scheduling, process/batch/formula/catch-weight, deep CTO/ETO configurators, regulated industries (GMP, aerospace).
- **Multi-company / intercompany** — works but a classic failure point (record rules, intercompany SO/PO, reconciliation, shared products/pricelists, consolidation). Design up front, test with real data.
- **Scale/performance** — fine for millions of records, but stored-compute cascades, huge `stock.move`/`account.move.line`, mass imports and long crons need care. On Odoo.sh crons are best-effort (≥5 min interval, time-limited) → batch + idempotent jobs.
- **Reporting** — pivot/graph/spreadsheet fine for operations; no data warehouse; advanced financial/cross-model analytics usually need external BI. Non-trivial PDF reports = dev work.
- **Localization** — quality varies a lot per country; **payroll exists only for some countries**. Check the client's `l10n_*` + payroll early.
- **Not out of the box:** advanced WMS (wave/slotting/voice picking), EDI (X12/EDIFACT), complex CPQ/pricing engines, advanced revenue recognition, commission plans beyond basics, full field-level audit trail, fine-grained field security, approvals on arbitrary documents without Studio/code.
- **AI** — paid credits since v20.
- **Third-party apps** (apps.odoo.com) vary wildly in quality — vet each for a maintained port to our version.

---

## 7. Deployment options

| | Odoo Online | **Odoo.sh (us)** | On-premise |
|---|---|---|---|
| Custom Python modules | ❌ | ✅ via GitHub | ✅ |
| Third-party / OCA apps | ❌ | ✅ (submodules) | ✅ |
| Studio | ✅ (Custom plan) | ✅ | ✅ (EE) |
| Versions | Major + SaaS x.1–x.4 | Major only | Major only |
| Server access | None | Shell/SSH, logs, psql — **no root/apt** | Full |
| Ops | Fully managed | CI, backups, monitoring, mail, DNS managed | All on us |

---

## 8. Odoo.sh in practice

### 8.1 Branch stages
- **Production** (one) — push = code update + restart. **Modules are only upgraded (`-u`) if their manifest `version` increased.** Failed update auto-reverts. No tests, no demo data.
- **Staging** — each build = **fresh neutralized copy of production** (crons off, mail caught, IAP off, payments/shipping in test mode). No tests. DB deleted after 1 month. **Config done on staging is NOT carried to production on merge.**
- **Development** — fresh DB with demo data, **runs tests**; red build on failure. DB lives ~3 days.
- Flow: `feature/*` (dev) → merge to `staging` → merge to `main` (prod). Dev → prod direct is allowed but discouraged.
- Env vars `ODOO_STAGE`, `ODOO_VERSION` let code detect environment (e.g. disable integrations outside prod).

### 8.2 Repo layout (GitHub only — no GitLab)
```
odoo-aba/
├── requirements.txt            # Python deps (pip); no system packages
├── aba_base/                   # custom modules at repo root (auto-detected via __manifest__.py)
├── aba_sale/
├── .oca-web/  (submodule, dot-folder = ignored)  + symlinks to chosen modules
└── third_party/<repo>/ (submodule, auto-detected)
```
- Submodules: use **SSH URLs**; private ones need a deploy key (Odoo.sh Settings → Submodules → add public key to repo Deploy keys).
- Dev builds default to "Install only my modules" → **submodule modules not installed**; use "install a list of modules" if tests need them.
- Not allowed: apt packages, Postgres extensions (PostGIS…), daemons, port 25 (use 465/587). Odoo can add an OS package on support request.

### 8.3 Features
- Web shell + SSH (key from your GitHub profile), online editor, `odoo-bin shell`, `psql` (⚠️ acts on real DB — wrap SQL in `BEGIN`/`ROLLBACK`).
- Logs (`odoo.log`, `update.log`, `install.log`, `pip.log`), mail catcher, monitoring, profiler (flame graph).
- **Backups**: daily on prod — 7 daily / 4 weekly / 3 monthly, 3 locations. Manual backups kept 3 days (max 5/day). Auto backup on merges that bump versions — **not on plain code pushes** → take a manual one before risky pushes. Downloadable dumps.
- Custom domain via CNAME (no apex → redirect to `www`), auto Let's Encrypt. Add SPF/DKIM for mail.
- Hosting region chosen at creation — **cannot change later**.
- Roles: Admin / Tester / Developer.

### 8.4 Gotchas
- Forgot to bump `version` → prod gets new Python but no `-u` → missing columns / stale views.
- **New modules aren't auto-installed** on staging/prod: Apps → Update Apps List → install (or add as a dependency of an installed module + bump its version).
- Long builds (up to ~1h) if many modules installed; slow/flaky tests = red builds.
- Staging crons/mail are off by design; trigger crons manually.

### 8.5 Major upgrades
1. Port custom modules on a dev branch switched to the target version (`odoo-bin upgrade_code --from 19.0` helps).
2. Odoo.sh **Upgrade** tab on staging → prod backup goes to upgrade.odoo.com → upgraded DB restored; check `upgrade.log`.
3. Run on production (downtime, auto-revert on failure).

### 8.6 Local dev mirroring Odoo.sh
- Same major + recent revision of `odoo/odoo` + `odoo/enterprise`; PostgreSQL 16.
- Addons path order: our repo → enterprise → odoo/addons.
- Docker: official `odoo` image is Community only → mount enterprise addons + our repo as volumes, `postgres:16`.
- Enterprise source: partners → GitHub access via partner dashboard; customers → odoo.com/page/download.
- Prod data locally: download dump, then `odoo-bin neutralize -d <db>`.

---

## 9. Custom development cheat-sheet

### 9.1 Module anatomy
```
aba_xxx/
├── __init__.py  __manifest__.py
├── models/  views/  security/  data/  report/  wizard/  controllers/
├── static/src/{js,xml,scss}  static/description/icon.png
├── migrations/<version>/{pre,post,end}-*.py
├── i18n/  tests/
```
- Manifest `version`: `20.0.x.y.z` (or `19.0.…`). **Bump on any model/view/data/security change.**
- `license`: `OPL-1`/`OEEL-1` when depending on Enterprise.
- `data` order: groups → access csv → views → menus.
- Naming: module prefix `aba_`; models singular dotted (`aba.delivery.slot`); `_id` / `_ids` suffixes; `_compute_x`, `_check_x`, `action_x`.

### 9.2 ORM essentials
- `Model` (table) / `TransientModel` (wizards) / `AbstractModel` (mixins).
- Inheritance: `_inherit='sale.order'` (extend in place — our default), new `_name`+`_inherit` (prototype), `_inherits` (delegation).
- Prefer **computed fields with `@api.depends` (+ `store=True`, `readonly=False`)** over `@api.onchange` (onchange doesn't run on import/RPC/create).
- `@api.model_create_multi` for `create`. Use `env.cr` / `env.uid` / `env.context` (not `_cr`…). `display_name` instead of `name_get`.
- Constraints: `@api.constrains` + `models.Constraint(...)` / `models.UniqueIndex(...)` (replaces `_sql_constraints` since 18.1).
- Domain API: `Domain('state','=','sale') & Domain(...)`.
- Raw SQL: `odoo.tools.SQL` with params — never string-format.

### 9.3 Views
- `<list>` (not `<tree>` since 18), no `attrs` since 17 → `invisible="state != 'draft'"`.
- Inherit with `inherit_id` + anchored xpaths (`field[@name=…]`), never replace core views.
- Frontend: extend via `registry` + `patch()`; templates `aba_module.ComponentName`; `t-out` not `t-esc`.
- PDF: `ir.actions.report` + QWeb template on `web.external_layout`.

### 9.4 Security
- **Odoo 20:** single `security/ir.access.csv`:
  ```csv
  id,name,model_id,group_id/id,operation,domain
  access_slot_user,slot user,aba.delivery.slot,base.group_user,r,
  access_slot_manager,slot manager,aba.delivery.slot,sales_team.group_sale_manager,crud,
  ```
  Empty `group_id` = global restriction (intersected).
- **Odoo ≤19:** `ir.model.access.csv` + `ir.rule` records.
- Multi-company: `company_id` field, `_check_company_auto = True`, `check_company=True` on relations, company rule.
- Public methods (no `_` prefix) are callable over RPC — be careful.

### 9.5 Integrations
- New integrations → **JSON-2 API** with a dedicated integration user + API key.
- Webhooks in: `@http.route(..., auth='public'|'bearer', csrf=False)` + verify HMAC; or automation rules with "incoming webhook" trigger.
- Long/async jobs: OCA `queue_job`; crons must batch and be idempotent.

### 9.6 Customization ladder
1. **Configuration** — free at upgrade time; always try first.
2. **Studio** — quick UI tweaks; stored in DB, no git/review, fragile xpaths, hard to promote staging→prod. **House rule: avoid on production except labels/reports; port to code.**
3. **Custom module** — business logic, integrations, security, reports, widgets.

### 9.7 Upgrade-safe rules
- Always call `super()`; override the smallest hook (`_prepare_*`, `_get_*`), never copy core methods.
- One module per concern, thin `depends`, no monkey-patching, never edit core/OCA in place.
- Tests: `TransactionCase`, `HttpCase` + tours, `Form`; tag `@tagged('post_install','-at_install')`; keep fast (Odoo.sh runs them on every dev build).
- Lint: `pylint-odoo` + OCA `oca-addons-repo-template` pre-commit (⚠️ check 20.0 readiness).

### 9.8 OCA modules with Enterprise
- Useful repos: `server-tools` (auditlog), `server-ux` (tier validation), `web`, `reporting-engine` (report_xlsx), `mis-builder`, `queue`, `rest-framework`, `sale-workflow`, `purchase-workflow`, `stock-logistics-*`, `account-*`, `server-env`, `l10n-<country>`.
- Caveats: overlap with Enterprise features (don't install `web_responsive`, OCA helpdesk/DMS/financial reports alongside EE equivalents); OCA CI tests Community only; **20.0 ports lag months**; pin submodules to commits; Odoo's upgrade service doesn't cover them.

---

## 10. Open decisions / to verify

1. **Odoo 19.0 vs 20.0** — check Odoo.sh version picker + whether needed OCA/third-party modules exist for 20.
2. Client country → localization, e-invoicing, payroll availability, pricing zone, Odoo.sh hosting region (irreversible).
3. Odoo.sh sizing: workers, storage, # of staging branches; get a live quote.
4. Number of internal users vs portal vs Light users (v13 agreement impact).
5. Enterprise source access for our devs (partner dashboard).
6. Any integration needing system libraries / Postgres extensions → not possible on Odoo.sh.
7. Map the client questionnaire (must-haves / won't-haves) → standard / config / Studio / custom / not a fit. _(pending — questionnaire not yet in repo)_

## Sources
- https://www.odoo.com/odoo-20-release-notes · https://www.odoo.com/odoo-19-release-notes · https://www.odoo.com/page/release-notes
- https://www.odoo.com/page/editions · https://www.odoo.com/pricing · https://www.odoo.sh/pricing · https://www.odoo.sh/faq
- Odoo.sh docs: https://www.odoo.com/documentation/19.0/administration/odoo_sh.html (source: github.com/odoo/documentation `content/administration/odoo_sh/`)
- Dev docs: https://www.odoo.com/documentation/20.0/developer/reference/backend/orm/changelog.html · …/backend/security.html · …/contributing/development/coding_guidelines.html · …/developer/reference/external_api.html
- Upgrade scripts: https://www.odoo.com/documentation/19.0/developer/reference/upgrades/upgrade_scripts.html
- Secondary: oec.sh, cybrosys.com, iventureteam.com, octurasolutions.com, gloriumtech.com, ksolves.com
- OCA: https://github.com/OCA/oca-addons-repo-template · https://pypi.org/project/pylint-odoo
