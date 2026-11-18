# Phase 0 · Task 2 — Buy licenses and odoo.com account (Odoo.sh version)

**Owner of execution:** EEY AAY consultant (support role) — purchase executed by **Vergara** on behalf of **ABA Web Agency SRL** (contract holder / license owner).
**Related answers:** C-23 *"Acquisto licenze: Vergara"*, TEC-02 *"Non l'abbiamo ancora comprato, sarà proprietaria aba web agency srl."*
**Depends on:** Task 1 — hosting decided: **Odoo.sh** (custom code required).

---

## 1. Goal

At the end of this task:

1. An **odoo.com account** legally owned by **ABA Web Agency SRL** (Italian P.IVA), with Vergara as purchasing/billing user.
2. A paid **Odoo Enterprise subscription — Custom plan, with Odoo.sh hosting included** — for the agreed number of internal users.
3. An **Odoo.sh project** linked to the GitHub repo `eeyaay-dev/odoo-aba`, hosted in **Saint-Ghislain (EU)**, on the agreed Odoo version, with a **production** branch and one **staging** branch.
4. The production database set to **Italy / Italian / Italian fiscal localization** (`l10n_it`).
5. EEY AAY consultants added as **Odoo.sh collaborators** (Admin) and as **database administrators**.

Until this is done, every other Phase-0/1 task is blocked.

---

## 2. Prerequisites

Collect from ABA before purchasing (see §5):

| Item | Needed for |
|---|---|
| Legal name, address, P.IVA / Codice Fiscale, SDI code / PEC | odoo.com account + Italian e-invoicing |
| Vergara's **company** email (ABA domain, not personal) | odoo.com account owner |
| Number of internal users at go-live and in 12 months (plan: 19) | License count |
| Odoo.sh sizing: workers, storage, staging branches (start: 1 worker, default storage, 1 staging) | Hosting price |
| Billing cycle (annual = discount) and start date | Billing |
| Odoo version: **19.0 or 20.0** | Project creation (version chosen at creation) |

Access needed by EEY AAY:
- A nominal email per consultant (no shared login).
- A **GitHub account** per consultant (Odoo.sh login = GitHub).
- Admin rights on the GitHub repo `eeyaay-dev/odoo-aba` for whoever creates the Odoo.sh project.

---

## 3. Steps

### Step 1 — Create the odoo.com account in ABA's name (Vergara)
1. Sign up at https://www.odoo.com/web/signup with Vergara's ABA-domain email.
2. *My Account ▸ Account Info*: Company **ABA Web Agency SRL**, legal address, Country **Italy**, **P.IVA**, language Italiano.
3. Enable 2FA; store recovery codes in ABA's password manager (shared with the EEY AAY lead).

> ⚠️ The account must be created by ABA/Vergara, not by EEY AAY — otherwise ownership transfer needs an Odoo support ticket.

### Step 2 — Plan & hosting (already decided)
- **Plan: Custom** — mandatory for Odoo.sh (Standard plan is Odoo Online only). Includes Studio, external API, multi-company.
- **Hosting: Odoo.sh**, billed **on top of** the per-user licences (workers + storage + staging environments). Get the live quote for Italy at https://www.odoo.sh/pricing before Vergara pays.

> ⚠️ **Do NOT start on an Odoo Online trial (odoo.com/trial).** Online trials run on SaaS versions (e.g. 19.x) that **cannot be imported into Odoo.sh**. Any configuration made there would be lost. Work starts directly on Odoo.sh.

### Step 3 — Purchase the subscription (Vergara)
1. Buy via https://www.odoo.com/pricing (choose **Custom** plan and **Odoo.sh** hosting) or through the EEY AAY partner channel (see §5).
2. Select number of users, apps, billing period, Odoo.sh options (workers / storage / staging).
3. Pay with ABA's company means; invoice issued to ABA Web Agency SRL with P.IVA.
4. Send the **subscription code** to the EEY AAY lead via the secure channel (Task 6) — needed to create the Odoo.sh project.

### Step 4 — Create the Odoo.sh project (EEY AAY lead)
1. Go to https://www.odoo.sh/project/new, sign in with GitHub, authorize the Odoo.sh app (incl. access to the `eeyaay-dev` organization).
2. Repository: select existing **`eeyaay-dev/odoo-aba`**.
3. Odoo version: **19.0 or 20.0** as agreed (check what the picker offers).
4. Subscription code: paste ABA's code.
5. Hosting location: **Saint-Ghislain (Europe)** — ⚠️ cannot be changed later.
6. Project name: e.g. `aba-web-agency` → URL `aba-web-agency.odoo.com`.
7. After creation: the `main` branch becomes **Production**; create a `staging` branch and drag it to **Staging**.

### Step 5 — Set Italian localization on the production database
1. Open the production database (Odoo.sh ▸ Production ▸ Connect).
2. *Settings ▸ General Settings*: language **Italiano** (install via *Languages* if needed).
3. *Settings ▸ Companies ▸ My Company*: **ABA Web Agency SRL**, address, Country **Italy**, phone, email, website, logo, **P.IVA**, **Codice Fiscale**.
4. Install **Accounting/Invoicing** and check *Settings ▸ Accounting ▸ Fiscal Localization* = **Italy** (`l10n_it` chart of accounts and taxes).

> ⚠️ Set the fiscal localization **before any accounting entry** exists — it cannot be changed afterwards.

### Step 6 — Add EEY AAY access
**Odoo.sh project:** *Settings ▸ Collaborators* → add each consultant's GitHub username, role **Admin** (lead) / **Developer** (others). Testers from ABA can be added later as **Tester**.

**Database users:** *Settings ▸ Users & Companies ▸ Users ▸ New*
- Internal User, nominal EEY AAY email, *Administration: Settings*.
- Save ▸ *Send Invitation Email*.

> ⚠️ Each internal user consumes a licence. Agree whether EEY AAY users are in the paid count and archived at go-live.

**odoo.com portal:** Vergara adds the EEY AAY lead as a contact of ABA Web Agency SRL (subscription visibility, support tickets); fallback = support ticket.

### Step 7 — Record credentials & baseline
Store in the project vault: odoo.com owner (Vergara), Odoo.sh project URL, production DB URL, subscription code, plan, user count, Odoo.sh sizing, expiry date, Odoo version, region.
Flag IAP credit needs (SMS, Partner Autocomplete, document digitization, WhatsApp, AI) to ABA now.

---

## 4. Verification

- [ ] https://www.odoo.com/my/subscriptions (as Vergara) shows the subscription **In Progress**, Custom plan, correct users, **Odoo.sh included**.
- [ ] Subscription invoice issued to ABA Web Agency SRL with P.IVA (PDF archived).
- [ ] Odoo.sh project exists, linked to `eeyaay-dev/odoo-aba`, region **Saint-Ghislain**, correct version; Production build is green.
- [ ] A `staging` branch exists in the Staging stage and builds green.
- [ ] Production DB: no trial/expiry banner; *Settings ▸ Odoo Subscription* shows valid expiration.
- [ ] Company = ABA Web Agency SRL, Country Italy, P.IVA filled, fiscal localization Italy.
- [ ] EEY AAY consultants: Odoo.sh collaborators **and** confirmed internal users with Settings rights.
- [ ] Studio icon visible (Custom plan entitlement).

---

## 5. Open points with ABA (confirm in writing before Vergara pays)

1. Internal users at go-live and within 12 months (plan says 19).
2. **Odoo.sh sizing & budget**: licences (Custom plan) + hosting (workers, storage, staging). Share the live quote.
3. **Odoo version: 19.0 or 20.0** (recommend latest available on Odoo.sh if our required modules exist for it).
4. Purchase channel: direct on odoo.com, or via EEY AAY as Odoo partner.
5. Billing: monthly/annual; start date (Odoo.sh trial projects revert to development after 30 days — buy before real configuration starts).
6. Legal data: full name, address, P.IVA / CF, SDI / PEC.
7. Account ownership: ABA email owning odoo.com account; who holds 2FA recovery codes.
8. **GitHub repo ownership**: the code lives in `eeyaay-dev/odoo-aba`. Decide whether it stays with EEY AAY or is transferred to an ABA GitHub organization (affects who controls the Odoo.sh project if the partnership ends).
9. EEY AAY users: included in licence count? Archived at go-live?
10. IAP services (SMS, WhatsApp, autocomplete, digitization, AI): budget prepaid credits.
