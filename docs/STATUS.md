# ABA Odoo project — status

_Last updated: 2026-11-19_

## Setup (done)

| Item | Value |
|---|---|
| Client | ABA Web Agency SRL, Taranto (Italy) |
| Edition / plan | Odoo 19 Enterprise, Custom plan, 22 users, yearly |
| Hosting | Odoo.sh, region Europe |
| Odoo.sh project | `eeyaay-dev-odoo-aba` |
| GitHub repo | `eeyaay-dev/odoo-aba` (private) |
| Production | `main` → https://eeyaay-dev-odoo-aba.odoo.com |
| Staging | `staging` branch |
| Development | create `feature/*` branches from `staging` when custom code starts |
| Target URL | https://erp.abawebagency.com (not live yet) |

Subscription code: in the project Credentials tab (not in git).

## In the production database

- Company: ABA WEB AGENCY SRL, Taranto, Italy, EUR, Europe/Rome, VAT and Codice Fiscale filled.
- Invoicing installed (Italian localization).
- Subscription registered (expiry banner gone).
- Logo uploaded (white version → need a dark/colour one for documents).

## Phase 0 tasks

| # | Task | Status |
|---|---|---|
| 1 | Odoo Online vs Odoo.sh | Done — Odoo.sh |
| 2 | Licenses & account | Done |
| 3 | ERP domain | Waiting — DNS email sent (CNAME `erp` → `eeyaay-dev-odoo-aba.odoo.com`) |
| 4 | Outbound email & DNS | Waiting — same DNS email (SPF `include:_spf.odoo.com`, DKIM CNAME `odoo._domainkey` → `odoo._domainkey.odoo.com`, DMARC `p=none`). Decision: Odoo's own mail servers (scenario A) |
| 5 | Project Manager details | Waiting — email sent to Francesco Vergara |
| 6 | Secure channel for credentials | Waiting — asked to send accesses in private WhatsApp DM |
| 7 | Audit sessions calendar | To do — Mondays 15:00–18:00 in Taranto, ~30 Nov → 21 Dec |

## After DNS is live

1. Odoo.sh → `main` → Settings → Custom domains → add `erp.abawebagency.com`.
2. Odoo → System Parameters: `web.base.url` = `https://erp.abawebagency.com`, add `web.base.url.freeze` = `True`.
3. Odoo → Settings → Alias Domain → `abawebagency.com`.
4. Google Workspace: `catchall@` and `bounce@` groups forwarding to Odoo.
5. Test with mail-tester.com.

Do the domain **before** inviting users and setting up Google SSO.

## Waiting on ABA (Francesco Vergara)

- List of the 22 users (each with their **own** email — shared emails refused because of 2FA)
- DNS records added by their domain manager
- Logo in dark/colour version
- REA number, share capital, sole/multiple shareholders (e-invoicing tab)
- Tax System confirmation (RF01 – Ordinario assumed)
- Address: "Piazza" vs "Piazzale" Dante 2 — order said Piazza
- PM details (task 5), accesses (task 6), audit dates/attendees (task 7)

## Notes

- Plan says "19 users" in Phase 1 task 1 → real count is **22**.
- Phase 1 guides in the admin panel were written for Odoo 19 (matches our version).
- Old IB2B/odoo-aba repo and old `ib2b-odoo-aba` Odoo.sh project can be deleted.
