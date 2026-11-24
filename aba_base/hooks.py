import logging

from lxml import etree

from odoo.tools import file_open

_logger = logging.getLogger(__name__)

MODULE = "aba_base"

# Discuss channels created by this module, matched by name on existing databases.
CHANNELS = {
    "channel_commerciale": "commerciale",
    "channel_progetti": "progetti",
    "channel_direzione": "direzione",
    "channel_amministrazione": "amministrazione",
}

# Members added by hand to "amministrazione" (only full-access users can join it).
AMMINISTRAZIONE_MEMBERS = ["partner_andrea_basile", "partner_francesco_vergara"]


def _link(env, name, record):
    """Give an existing record this module's external ID (noupdate) if it hasn't one yet."""
    if not record:
        return
    record.ensure_one()
    imd = env["ir.model.data"]
    if imd.search_count([("module", "=", MODULE), ("name", "=", name)]):
        return
    imd.create({
        "module": MODULE,
        "name": name,
        "model": record._name,
        "res_id": record.id,
        "noupdate": True,
    })
    _logger.info("aba_base: linked existing %s(%s) to %s.%s", record._name, record.id, MODULE, name)


def _users_in_data_file():
    """Yield (user xml id, partner xml id, login) for each user in data/res_users_data.xml."""
    with file_open(f"{MODULE}/data/res_users_data.xml", "rb") as fh:
        root = etree.parse(fh).getroot()
    for rec in root.iter("record"):
        if rec.get("model") != "res.users":
            continue
        login = rec.findtext("field[@name='login']")
        partner_xmlid = rec.find("field[@name='partner_id']").get("ref")
        yield rec.get("id"), partner_xmlid, login


def pre_init_hook(env):
    """Link records that already exist to this module's external IDs.

    The setup was first done by hand in production, so those records have no
    external ID. Without this, installing the module would create a second copy
    of every user, partner, channel… With the link, Odoo updates the existing
    record instead. On a fresh database nothing matches and the data files
    create everything as usual. Safe to run more than once.
    """
    users = env["res.users"].with_context(active_test=False)
    for user_xmlid, partner_xmlid, login in _users_in_data_file():
        user = users.search([("login", "=", login)], limit=1)
        _link(env, user_xmlid, user)
        _link(env, partner_xmlid, user.partner_id)

    channels = env["discuss.channel"]
    for xmlid, name in CHANNELS.items():
        _link(env, xmlid, channels.search([("name", "=", name), ("channel_type", "=", "channel")], limit=1))

    _link(env, "alias_domain_abawebagency",
          env["mail.alias.domain"].search([("name", "=", "abawebagency.com")], limit=1))
    _link(env, "appointment_call_conoscitiva",
          env["appointment.type"].with_context(active_test=False).search(
              [("name", "=", "Call Conoscitiva – ABA Web Agency")], limit=1))
    _link(env, "filter_cronologia_modifiche",
          env["ir.filters"].with_context(active_test=False).search(
              [("name", "=", "Cronologia modifiche"), ("model_id", "=", "mail.message")], limit=1))


def post_init_hook(env):
    """Things that can't be plain XML data.

    1. Italian translations loaded for every installed module (the language itself
       is activated first thing in data/res_lang_data.xml).
    2. Andrea and Francesco in the "amministrazione" channel, skipping anyone who is
       already a member (a duplicate member would make the install fail).
    3. Italian chart of accounts, when the company doesn't have it yet. On a fresh
       database with demo data the generic chart already has entries and Odoo
       refuses to switch: we log it and move on instead of failing the install.
    """
    env["res.lang"]._activate_lang("it_IT")
    env["ir.module.module"].search([("state", "=", "installed")])._update_translations(["it_IT"])

    channel = env.ref(f"{MODULE}.channel_amministrazione", raise_if_not_found=False)
    if channel:
        wanted = env["res.partner"].browse([env.ref(f"{MODULE}.{xmlid}").id for xmlid in AMMINISTRAZIONE_MEMBERS])
        for partner in wanted - channel.channel_member_ids.partner_id:
            env["discuss.channel.member"].create({"channel_id": channel.id, "partner_id": partner.id})

    company = env.ref("base.main_company")
    if company.chart_template != "it":
        try:
            with env.cr.savepoint():
                env["account.chart.template"].try_loading("it", company, install_demo=False)
        except Exception as exc:  # noqa: BLE001 - never block the install on this
            _logger.warning("aba_base: Italian chart of accounts not loaded on %s: %s", company.name, exc)
