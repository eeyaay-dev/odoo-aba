from odoo import _, api, fields, models

EPS = 0.005  # tolerance for rounding (percent points)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    aba_discount_pct = fields.Float(
        string="Sconto su listino (%)",
        compute="_compute_aba_discount_pct",
        digits=(16, 2),
        help="Real discount against the product list price: it also counts a lower unit price typed by hand.",
    )

    @api.depends("product_id", "price_unit", "discount", "currency_id", "order_id.date_order")
    def _compute_aba_discount_pct(self):
        for line in self:
            line.aba_discount_pct = line._aba_get_discount_pct()

    def _aba_get_discount_pct(self):
        """Effective discount (in %) of this line against the product list price."""
        self.ensure_one()
        product = self.product_id
        if self.display_type or not product:
            return 0.0
        list_price = product.lst_price
        company = self.company_id or self.env.company
        if product.currency_id and self.currency_id and product.currency_id != self.currency_id:
            date = self.order_id.date_order or fields.Date.context_today(self)
            list_price = product.currency_id._convert(list_price, self.currency_id, company, date)
        if list_price <= 0:
            return 0.0
        net_unit = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        return round(max(0.0, (1 - net_unit / list_price) * 100.0), 2)

    @api.onchange("price_unit", "discount", "product_id")
    def _onchange_aba_discount_warning(self):
        threshold = self.env["sale.order"]._aba_get_max_discount_pct()
        for line in self:
            pct = line._aba_get_discount_pct()
            if pct > threshold + EPS:
                return {
                    "warning": {
                        "title": _("Sconto oltre il limite"),
                        "message": _(
                            "Lo sconto su listino è del %(pct).2f%%, oltre il massimo consentito del %(max).0f%%.\n"
                            "Il contratto non potrà essere finalizzato senza l'autorizzazione di Andrea Basile: "
                            "usa «Richiedi autorizzazione sconto» sull'ordine.",
                            pct=pct,
                            max=threshold,
                        ),
                    }
                }
        return None
