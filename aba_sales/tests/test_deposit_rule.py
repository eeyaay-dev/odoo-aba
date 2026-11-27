from odoo.tests import tagged

from .common import AbaSalesCommon


@tagged("post_install", "-at_install")
class TestDepositRule(AbaSalesCommon):

    def _order_for(self, amount):
        return self._order(price_unit=amount)

    def test_up_to_threshold_full_prepayment(self):
        self.assertAlmostEqual(self._order_for(15000.0).prepayment_percent, 1.0)

    def test_exactly_threshold_is_full_prepayment(self):
        self.assertAlmostEqual(self._order_for(20000.0).prepayment_percent, 1.0)

    def test_above_threshold_30_percent_deposit(self):
        self.assertAlmostEqual(self._order_for(20000.01).prepayment_percent, 0.30)
        self.assertAlmostEqual(self._order_for(50000.0).prepayment_percent, 0.30)

    def test_rule_follows_the_amount(self):
        order = self._order_for(25000.0)
        self.assertAlmostEqual(order.prepayment_percent, 0.30)
        order.order_line.price_unit = 10000.0
        self.assertAlmostEqual(order.prepayment_percent, 1.0)

    def test_threshold_is_a_parameter(self):
        self.env["ir.config_parameter"].sudo().set_param("aba_sales.deposit_threshold", "5000")
        self.assertAlmostEqual(self._order_for(6000.0).prepayment_percent, 0.30)
