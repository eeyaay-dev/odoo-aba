from odoo.exceptions import AccessError
from odoo.tests import tagged

from .common import AbaSalesCommon


@tagged("post_install", "-at_install")
class TestCatalogPermissions(AbaSalesCommon):

    def test_salesman_can_read_but_not_change_products(self):
        product = self.product.with_user(self.salesman)
        self.assertEqual(product.name, "ABA Test Service")
        with self.assertRaises(AccessError):
            product.write({"list_price": 1.0})
        with self.assertRaises(AccessError):
            self.env["product.template"].with_user(self.salesman).create({"name": "Nope", "type": "service"})
        with self.assertRaises(AccessError):
            product.product_tmpl_id.unlink()

    def test_salesman_cannot_change_categories_or_attributes(self):
        with self.assertRaises(AccessError):
            self.env["product.category"].with_user(self.salesman).create({"name": "Nope"})
        with self.assertRaises(AccessError):
            self.env["product.attribute"].with_user(self.salesman).create({"name": "Nope"})

    def test_catalog_manager_can_change_products(self):
        product = self.product.with_user(self.andrea)
        product.write({"list_price": 1200.0})
        self.assertEqual(product.list_price, 1200.0)
        categ = self.env["product.category"].with_user(self.andrea).create({"name": "Nuova categoria"})
        self.assertTrue(categ)

    def test_salesman_can_still_sell(self):
        """Creating and confirming a quotation must keep working for a salesperson."""
        order = self._order()
        order.action_confirm()
        self.assertEqual(order.state, "sale")
