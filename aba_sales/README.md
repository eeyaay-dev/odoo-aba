# aba_sales — ABA Web Agency sales rules

Implements the Phase 3 sales requirements from ABA (message of 2026-11-26):

| Requirement | How it is done |
|---|---|
| Only Andrea Basile creates, edits and validates products | Group **ABA / Gestore catalogo**. Global record rules block create / write / delete on products, variants, categories, attributes and product documents for everybody else. Reading stays open. |
| Contract attached to each product, replaceable | Standard Odoo: upload the PDF in the product's **Documents** tab (shown in the quotation). Only the catalog manager can upload or replace it. The salesperson edits only price, discount and duration, never the PDF. |
| 6 or 12 months for the main products | Product attribute *Durata contratto* (6 mesi / 12 mesi), see the import files. |
| Salesperson discount up to 10% of the list price | Measured against the product list price, so a lower unit price typed by hand counts too. A warning appears when it is entered. |
| Above 10%: error and block | `action_confirm` raises an error, so confirming, online signature and online payment are all blocked. |
| Authorization request sent from the system | Button **Richiedi autorizzazione sconto** on the order, then **Invia richiesta** on the request. |
| Only Andrea approves or rejects | Group **ABA / Approvatore sconti** (buttons and Python check). Approving unlocks the order up to the approved percentage. A higher discount needs a new request. |
| Everything traced | Chatter on the request and on the order, one activity for each approver, and the *Richieste di sconto* menu under Sales ▸ Orders. |

## Settings

- `aba_sales.max_discount_pct` (system parameter, default 10): the limit, in percent.
- Andrea Basile (`andrea.basile@abawebagency.com`) gets both groups when the module is installed
  (`post_init_hook`). On a database where that user does not exist, assign the groups by hand
  (Settings ▸ Users).

## Install order on an existing database (staging / production)

1. **Import the catalog first** (products, categories, duration attribute). The catalog rules
   block every user who is not in the *Gestore catalogo* group, so the import has to be done
   before installing this module, or by a user already in the group.
2. Install `aba_sales`.
3. Check with a salesperson account: they can read products but not edit them, and a 15%
   discount cannot be confirmed without Andrea's approval.

To let someone else (for example the EEY AAY consultants) change the catalog, add them to
*ABA / Gestore catalogo* temporarily.

## Tests

```
odoo -d test -i aba_sales --test-tags /aba_sales --stop-after-init
```
