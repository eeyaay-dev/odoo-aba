# odoo-aba

Odoo 19 Enterprise implementation for **ABA Web Agency SRL**, hosted on **Odoo.sh** (Europe).

## Layout

- Custom Odoo modules go at the repository root (one folder per module, prefixed `aba_`). Odoo.sh detects them through their `__manifest__.py`.
- Python dependencies go in `requirements.txt` at the root.
- Project documentation lives in [`docs/`](docs/).

## Branches

| Branch | Odoo.sh stage |
|---|---|
| `main` | Production |
| `staging` | Staging |
| `feature/*` | Development |

Bump the module `version` in `__manifest__.py` on every change to models, views, data or security, otherwise production won't update the module.
