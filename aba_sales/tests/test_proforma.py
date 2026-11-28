from odoo.tests import tagged

from .common import AbaSalesCommon


@tagged("post_install", "-at_install")
class TestProforma(AbaSalesCommon):

    def test_number_is_assigned_once(self):
        order = self._order()
        first = order._aba_get_proforma_number()
        self.assertRegex(first, r"^PF/\d{4}/\d{4}$")
        self.assertEqual(order._aba_get_proforma_number(), first)
        self.assertEqual(order.aba_proforma_number, first)

    def test_numbers_are_sequential_and_unique(self):
        n1 = self._order()._aba_get_proforma_number()
        n2 = self._order()._aba_get_proforma_number()
        self.assertNotEqual(n1, n2)
        self.assertEqual(int(n2.rsplit("/", 1)[1]), int(n1.rsplit("/", 1)[1]) + 1)

    def test_sending_a_proforma_assigns_the_number(self):
        order = self._order()
        self.assertFalse(order.aba_proforma_number)
        order.with_context(proforma=True).action_quotation_send()
        self.assertTrue(order.aba_proforma_number)

    def test_a_normal_quotation_gets_no_proforma_number(self):
        order = self._order()
        order.action_quotation_send()
        self.assertFalse(order.aba_proforma_number)

    def test_report_shows_number_and_wording(self):
        order = self._order()
        html, _ = self.env["ir.actions.report"]._render_qweb_html("sale.report_saleorder_pro_forma", order.ids)
        text = html.decode() if isinstance(html, bytes) else html
        self.assertIn(order.aba_proforma_number, text)
        self.assertIn("Documento non valido ai fini fiscali", text)

    def test_quotation_report_is_unchanged(self):
        order = self._order()
        html, _ = self.env["ir.actions.report"]._render_qweb_html("sale.report_saleorder", order.ids)
        text = html.decode() if isinstance(html, bytes) else html
        self.assertNotIn("Documento non valido ai fini fiscali", text)
        self.assertFalse(order.aba_proforma_number)
