# aba_base — ABA Web Agency base setup

Code version of everything configured by hand in the ABA database during Phase 0/1
(read from production through the API on 24/11/2026).

| File | What it sets | Task |
|---|---|---|
| `data/res_lang_data.xml` | Activates Italian first (users and contacts below use `it_IT`) | P1·4 |
| `data/res_company_data.xml` | Company identity, Italian e-invoicing fields, logo, document layout + footer, Italian as default contact language | P1·4, P1·5 |
| `data/mail_data.xml` | Alias domain `abawebagency.com` (bounce / catchall / notifications), catchall domain, from filter | P0·4 |
| `data/settings_data.xml` | 2FA for employees, sign-up on invitation, Google sign-in, Google Calendar client ID | P1·2, P1·3, P1·7 |
| `data/res_users_data.xml` | 21 users + their access level + employee | P1·1 |
| `data/crm_team_data.xml` | Sales team: leader Rocco, members Rocco/Fedele/Luca, alias `leads@` | P1·6 |
| `data/discuss_channel_data.xml` | `generale`, `commerciale`, `progetti`, `direzione`, `amministrazione` | P1·8 |
| `data/appointment_data.xml` | Booking page *Call Conoscitiva – ABA Web Agency* | P1·7 |
| `data/ir_filters_data.xml` | Admin favourite *Cronologia modifiche* | P1·10 |
| `hooks.py` | Before install: link existing records (no duplicates). After install: Italian translations, `amministrazione` members, Italian chart of accounts on a fresh database | P1·4, P1·8 |

## Not in the module (on purpose)

- **Secrets**: Google client secret, passwords, API keys → platform Credentials tab, set by hand.
- **`web.base.url`**: Odoo.sh sets it per build; production uses `https://erp.abawebagency.com` (frozen).
- **Odoo.sh custom domain, DNS, Google Workspace groups**: outside Odoo.
- **WhatsApp account**: connected with Meta's *Connect* button, not configurable as data.
- The `admin` user (it already exists in every database).

## Installing

- **Fresh database (development branch):** installs everything. Demo data stays; the Italian
  chart is only loaded if the database has no accounting entries yet (logged otherwise).
- **Production / staging:** the setup already exists there without external IDs. The
  `pre_init_hook` links it before the data files load (users by login, their partners,
  channels by name, alias domain, booking page, filter), so installing **updates** the
  existing records instead of duplicating them. The linked records are rewritten with the
  values in these files — they match production as of 24/11/2026 (checked against a
  read-only comparison), except `amministrazione`, which gains Andrea and Francesco.
  Test on **staging** first (Apps ▸ install `aba_base`), then production.

All data files are `noupdate="1"`: after installation, changes made in the UI are kept on
module upgrades.
