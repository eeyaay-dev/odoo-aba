from odoo.tests.common import TransactionCase


class AbaSalesCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Users = cls.env["res.users"].with_context(no_reset_password=True)
        g_salesman = cls.env.ref("sales_team.group_sale_salesman")
        cls.salesman = Users.create({
            "name": "Commerciale Test", "login": "aba_salesman_test",
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, g_salesman.id])],
        })
        cls.andrea = Users.create({
            "name": "Andrea Test", "login": "aba_andrea_test",
            "group_ids": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("sales_team.group_sale_manager").id,  # as the real Andrea: Sales administrator
                cls.env.ref("aba_sales.group_catalog_manager").id,
                cls.env.ref("aba_sales.group_discount_approver").id,
            ])],
        })
        cls.partner = cls.env["res.partner"].create({"name": "Cliente Test"})
        # product created by the catalog manager (the rule applies to everybody else)
        cls.product = cls.env["product.product"].with_user(cls.andrea).create({
            "name": "ABA Test Service", "type": "service", "list_price": 1000.0,
        })

    def _order(self, price_unit=1000.0, discount=0.0, user=None):
        user = user or self.salesman
        order = self.env["sale.order"].with_user(user).create({
            "partner_id": self.partner.id,
            "order_line": [(0, 0, {
                "product_id": self.product.id, "product_uom_qty": 1,
                "price_unit": price_unit, "discount": discount,
            })],
        })
        return order
