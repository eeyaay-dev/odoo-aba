import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Things that can't be plain XML data.

    1. Italian translations loaded for every installed module (the language itself
       is activated first thing in data/res_lang_data.xml).
    2. Italian chart of accounts, when the company doesn't have it yet. On a fresh
       database with demo data the generic chart already has entries and Odoo
       refuses to switch: we log it and move on instead of failing the install.
    """
    env["res.lang"]._activate_lang("it_IT")
    env["ir.module.module"].search([("state", "=", "installed")])._update_translations(["it_IT"])

    company = env.ref("base.main_company")
    if company.chart_template != "it":
        try:
            with env.cr.savepoint():
                env["account.chart.template"].try_loading("it", company, install_demo=False)
        except Exception as exc:  # noqa: BLE001 - never block the install on this
            _logger.warning("aba_base: Italian chart of accounts not loaded on %s: %s", company.name, exc)
