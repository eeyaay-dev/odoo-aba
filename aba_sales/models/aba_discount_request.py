from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

APPROVER_GROUP = "aba_sales.group_discount_approver"


class AbaDiscountRequest(models.Model):
    _name = "aba.discount.request"
    _description = "ABA – Richiesta di autorizzazione sconto"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(string="Riferimento", default=lambda self: _("Nuova"), readonly=True, copy=False)
    order_id = fields.Many2one("sale.order", string="Ordine / contratto", required=True, ondelete="cascade", index=True)
    partner_id = fields.Many2one(related="order_id.partner_id", store=True, string="Cliente")
    requested_by = fields.Many2one(
        "res.users", string="Richiesto da", default=lambda self: self.env.user, readonly=True, tracking=True
    )
    max_discount_pct = fields.Float(string="Sconto richiesto (%)", digits=(16, 2), tracking=True)
    reason = fields.Text(string="Motivazione", required=True)
    line_summary = fields.Text(string="Righe con sconto", compute="_compute_line_summary")
    state = fields.Selection(
        [("draft", "Bozza"), ("pending", "In attesa"), ("approved", "Approvata"), ("rejected", "Rifiutata")],
        default="draft", required=True, tracking=True, copy=False,
    )
    decided_by = fields.Many2one("res.users", string="Deciso da", readonly=True, copy=False, tracking=True)
    decided_on = fields.Datetime(string="Data decisione", readonly=True, copy=False)
    decision_note = fields.Text(string="Nota della decisione")

    @api.depends("order_id.order_line.price_unit", "order_id.order_line.discount")
    def _compute_line_summary(self):
        for req in self:
            lines = []
            for line in req.order_id.order_line:
                pct = line._aba_get_discount_pct()
                if pct > 0:
                    lines.append(f"{line.product_id.display_name or line.name}: {pct:.2f}%")
            req.line_summary = "\n".join(lines)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == _("Nuova"):
                vals["name"] = self.env["ir.sequence"].next_by_code("aba.discount.request") or _("Nuova")
        return super().create(vals_list)

    def action_submit(self):
        for req in self:
            if req.state != "draft":
                raise UserError(_("Solo una richiesta in bozza può essere inviata."))
            if req.order_id.aba_pending_request_id:
                raise UserError(_("Esiste già una richiesta in attesa per questo ordine."))
            req.max_discount_pct = req.order_id.aba_max_discount_pct
            req.state = "pending"
            req.order_id.message_post(
                body=_("Richiesta di autorizzazione sconto %(ref)s inviata: %(pct).2f%%.\nMotivo: %(reason)s",
                       ref=req.name, pct=req.max_discount_pct, reason=req.reason)
            )
            req._notify_approvers()
        return True

    def _notify_approvers(self):
        group = self.env.ref(APPROVER_GROUP)
        approvers = self.env["res.users"].sudo().search([("group_ids", "in", group.id)])
        for req in self:
            for user in approvers:
                req.sudo().activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=user.id,
                    summary=_("Autorizza sconto %(pct).2f%% – %(order)s", pct=req.max_discount_pct, order=req.order_id.name),
                )

    def _check_can_decide(self):
        if not self.env.user.has_group(APPROVER_GROUP):
            raise AccessError(_("Solo l'approvatore degli sconti (Andrea Basile) può approvare o rifiutare."))
        if any(req.state != "pending" for req in self):
            raise UserError(_("Si possono decidere solo richieste in attesa."))

    def _finish(self, state):
        self.sudo().activity_ids.action_feedback(feedback=_("Richiesta decisa."))
        for req in self:
            req.write({"state": state, "decided_by": self.env.user.id, "decided_on": fields.Datetime.now()})

    def action_approve(self):
        self._check_can_decide()
        self._finish("approved")
        for req in self:
            order = req.order_id.sudo()
            order.aba_approved_discount_pct = max(order.aba_approved_discount_pct, req.max_discount_pct)
            order.message_post(
                body=_("Sconto %(pct).2f%% AUTORIZZATO da %(user)s (%(ref)s).",
                       pct=req.max_discount_pct, user=self.env.user.name, ref=req.name)
            )
        return True

    def action_reject(self):
        self._check_can_decide()
        self._finish("rejected")
        for req in self:
            req.order_id.sudo().message_post(
                body=_("Sconto %(pct).2f%% RIFIUTATO da %(user)s (%(ref)s). %(note)s",
                       pct=req.max_discount_pct, user=self.env.user.name, ref=req.name,
                       note=req.decision_note or "")
            )
        return True
