import logging

_logger = logging.getLogger(__name__)

# ABA decision: product management and discount approval belong to Andrea Basile only.
OWNER_LOGIN = "andrea.basile@abawebagency.com"


def post_init_hook(env):
    """Give Andrea Basile the two ABA groups, when that user exists (not on a fresh database)."""
    user = env["res.users"].with_context(active_test=False).search([("login", "=", OWNER_LOGIN)], limit=1)
    if not user:
        _logger.warning("aba_sales: user %s not found, assign the two ABA groups by hand", OWNER_LOGIN)
        return
    groups = env.ref("aba_sales.group_catalog_manager") | env.ref("aba_sales.group_discount_approver")
    user.write({"group_ids": [(4, g.id) for g in groups]})
    _logger.info("aba_sales: %s added to %s", OWNER_LOGIN, ", ".join(groups.mapped("name")))
