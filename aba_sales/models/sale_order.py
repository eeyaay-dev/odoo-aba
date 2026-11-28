from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .sale_order_line import EPS

PARAM = "aba_sales.max_discount_pct"


class SaleOrder(models.Model):
    _inherit = "sale.order"

    aba_max_discount_pct = fields.Float(
        string="Sconto massimo su listino (%)", compute="_compute_aba_discount", digits=(16, 2)
    )
    aba_approved_discount_pct = fields.Float(
        string="Sconto autorizzato (%)", copy=False, readonly=True, digits=(16, 2),
        help="Highest discount approved for this order. A higher discount needs a new approval.",
    )
    aba_discount_blocked = fields.Boolean(
        string="Sconto da autorizzare", compute="_compute_aba_discount",
        help="The discount exceeds the limit and is not covered by an approved request.",
    )
    aba_proforma_number = fields.Char(
        string="Numero proforma", copy=False, readonly=True,
        help="ABA's own pro-forma number (PF/year/0001). Assigned the first time a pro-forma is issued.",
    )
    aba_request_ids = fields.One2many("aba.discount.request", "order_id", string="Richieste di sconto")
    aba_pending_request_id = fields.Many2one(
        "aba.discount.request", compute="_compute_aba_discount", string="Richiesta in attesa"
    )

    @api.model
    def _aba_get_max_discount_pct(self):
        value = self.env["ir.config_parameter"].sudo().get_param(PARAM, "10")
        try:
            return float(value)
        except ValueError:
            return 10.0

    @api.depends(
        "order_line.price_unit", "order_line.discount", "order_line.product_id",
        "aba_approved_discount_pct", "aba_request_ids.state",
    )
    def _compute_aba_discount(self):
        threshold = self._aba_get_max_discount_pct()
        for order in self:
            pcts = [line._aba_get_discount_pct() for line in order.order_line]
            top = max(pcts, default=0.0)
            order.aba_max_discount_pct = top
            order.aba_discount_blocked = top > threshold + EPS and top > order.aba_approved_discount_pct + EPS
            order.aba_pending_request_id = order.aba_request_ids.filtered(lambda r: r.state == "pending")[:1]

    def _compute_amounts(self):
        """ABA rule: first invoice in full; above 20,000 EUR (VAT excluded) only a 30% deposit.

        Applied when the totals are computed. It is not done in `_compute_prepayment_percent`
        because that field is precomputed and cannot depend on the (not precomputed) totals.
        The company default (100%) is kept up to the threshold. Both numbers are system
        parameters: aba_sales.deposit_threshold and aba_sales.deposit_percent_above.
        """
        super()._compute_amounts()
        threshold, percent = self._aba_get_deposit_rule()
        for order in self:
            if order.state not in ("draft", "sent"):
                continue
            if order.amount_untaxed > threshold:
                order.prepayment_percent = percent
            else:
                order.prepayment_percent = order.company_id.prepayment_percent

    @api.model
    def _aba_get_deposit_rule(self):
        params = self.env["ir.config_parameter"].sudo()
        try:
            threshold = float(params.get_param("aba_sales.deposit_threshold", "20000"))
            percent = float(params.get_param("aba_sales.deposit_percent_above", "30")) / 100.0
        except ValueError:
            threshold, percent = 20000.0, 0.30
        return threshold, percent

    def _aba_get_proforma_number(self):
        """Return the ABA pro-forma number, assigning it on first use.

        The standard pro-forma only shows the quotation reference (S00042). ABA wants its own
        numbering. It is assigned once, so re-sending the same pro-forma keeps the same number.
        """
        self.ensure_one()
        if not self.aba_proforma_number:
            number = self.env["ir.sequence"].sudo().next_by_code("aba.proforma")
            self.sudo().aba_proforma_number = number
        return self.aba_proforma_number

    def action_quotation_send(self):
        if self.env.context.get("proforma"):
            for order in self:
                order._aba_get_proforma_number()
        return super().action_quotation_send()

    def action_aba_request_discount(self):
        """Open the request form (the salesperson writes the reason and sends it)."""
        self.ensure_one()
        if not self.aba_discount_blocked:
            raise UserError(_("Nessuna autorizzazione necessaria: lo sconto è entro il limite o già autorizzato."))
        if self.aba_pending_request_id:
            raise UserError(_("Esiste già una richiesta in attesa di approvazione."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "aba.discount.request",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_order_id": self.id,
                "default_max_discount_pct": self.aba_max_discount_pct,
            },
        }

    def action_confirm(self):
        # Odoo's own demo data confirms orders with big discounts: never block while installing data.
        if self.env.context.get("install_demo") or self.env.context.get("install_mode"):
            return super().action_confirm()
        blocked = self.filtered("aba_discount_blocked")
        if blocked:
            threshold = self._aba_get_max_discount_pct()
            raise UserError(
                _(
                    "Impossibile finalizzare il contratto: lo sconto su listino (%(pct).2f%%) supera il limite "
                    "del %(max).0f%% e non è stato autorizzato.\n"
                    "Invia una richiesta di autorizzazione: solo Andrea Basile può approvarla.",
                    pct=max(blocked.mapped("aba_max_discount_pct")),
                    max=threshold,
                )
            )
        return super().action_confirm()
