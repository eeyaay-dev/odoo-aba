from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged

from .common import AbaSalesCommon


@tagged("post_install", "-at_install")
class TestDiscountApproval(AbaSalesCommon):

    def test_discount_within_limit_confirms(self):
        order = self._order(discount=10.0)
        self.assertAlmostEqual(order.aba_max_discount_pct, 10.0)
        self.assertFalse(order.aba_discount_blocked)
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_discount_over_limit_blocks_confirmation(self):
        order = self._order(discount=11.0)
        self.assertTrue(order.aba_discount_blocked)
        with self.assertRaises(UserError):
            order.action_confirm()
        self.assertNotEqual(order.state, "sale")

    def test_typed_unit_price_counts_as_discount(self):
        order = self._order(price_unit=880.0)  # 12% below the 1000 list price
        self.assertAlmostEqual(order.aba_max_discount_pct, 12.0)
        self.assertTrue(order.aba_discount_blocked)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_unit_price_above_list_is_not_a_discount(self):
        order = self._order(price_unit=1500.0)
        self.assertEqual(order.aba_max_discount_pct, 0.0)
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_onchange_warning(self):
        order = self._order(discount=15.0)
        result = order.order_line._onchange_aba_discount_warning()
        self.assertTrue(result and result["warning"])
        order.order_line.discount = 5.0
        self.assertFalse(order.order_line._onchange_aba_discount_warning())

    def test_request_and_approval_unlocks_confirmation(self):
        order = self._order(discount=20.0)
        self.assertTrue(order.aba_discount_blocked)
        request = self.env["aba.discount.request"].with_user(self.salesman).create({
            "order_id": order.id, "reason": "Cliente storico",
        })
        request.action_submit()
        self.assertEqual(request.state, "pending")
        self.assertEqual(order.aba_pending_request_id, request)
        with self.assertRaises(UserError):
            order.action_confirm()  # still blocked while pending
        request.with_user(self.andrea).action_approve()
        self.assertEqual(request.state, "approved")
        self.assertEqual(request.decided_by, self.andrea)
        self.assertAlmostEqual(order.aba_approved_discount_pct, 20.0)
        self.assertFalse(order.aba_discount_blocked)
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_rejection_keeps_it_blocked(self):
        order = self._order(discount=20.0)
        request = self.env["aba.discount.request"].with_user(self.salesman).create({
            "order_id": order.id, "reason": "Prova",
        })
        request.action_submit()
        request.with_user(self.andrea).action_reject()
        self.assertEqual(request.state, "rejected")
        self.assertTrue(order.aba_discount_blocked)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_salesman_cannot_approve(self):
        order = self._order(discount=20.0)
        request = self.env["aba.discount.request"].with_user(self.salesman).create({
            "order_id": order.id, "reason": "Prova",
        })
        request.action_submit()
        with self.assertRaises(AccessError):
            request.with_user(self.salesman).action_approve()
        with self.assertRaises(AccessError):
            request.with_user(self.salesman).action_reject()
        self.assertEqual(request.state, "pending")

    def test_higher_discount_after_approval_needs_new_request(self):
        order = self._order(discount=20.0)
        request = self.env["aba.discount.request"].with_user(self.salesman).create({
            "order_id": order.id, "reason": "Prova",
        })
        request.action_submit()
        request.with_user(self.andrea).action_approve()
        self.assertFalse(order.aba_discount_blocked)
        order.order_line.discount = 30.0
        self.assertTrue(order.aba_discount_blocked)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_audit_trail_on_order(self):
        order = self._order(discount=20.0)
        request = self.env["aba.discount.request"].with_user(self.salesman).create({
            "order_id": order.id, "reason": "Prova",
        })
        request.action_submit()
        request.with_user(self.andrea).action_approve()
        bodies = " ".join(order.message_ids.mapped("body"))
        self.assertIn("AUTORIZZATO", bodies)
        self.assertIn(request.name, bodies)

    def test_approver_gets_an_activity(self):
        order = self._order(discount=20.0)
        request = self.env["aba.discount.request"].with_user(self.salesman).create({
            "order_id": order.id, "reason": "Prova",
        })
        request.action_submit()
        self.assertIn(self.andrea, request.sudo().activity_ids.mapped("user_id"))

    def test_demo_data_installation_is_never_blocked(self):
        """Odoo's demo data confirms orders with huge discounts; that must keep working."""
        order = self._order(discount=96.25)
        self.assertTrue(order.aba_discount_blocked)
        order.with_context(install_demo=True).action_confirm()
        self.assertEqual(order.state, "sale")
