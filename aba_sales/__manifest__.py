{
    "name": "ABA Web Agency – Sales rules",
    "version": "19.0.1.2.0",
    "summary": "Catalog managed only by Andrea, 10% discount cap with approval request and audit trail",
    "description": """
Sales rules requested by ABA Web Agency (Phase 3):

* Only members of "ABA / Gestore catalogo" (Andrea Basile) can create, edit or delete
  products, product categories and attributes. Everybody else is read-only.
* A salesperson can discount a line up to 10% from the product list price (the
  discount field or a directly typed lower unit price). Above that, the quotation
  cannot be confirmed (also through online signature or payment).
* The salesperson sends a discount authorization request from the order.
  Only members of "ABA / Approvatore sconti" can approve or reject it. Every
  request and decision is logged (chatter + activity) on the request and the order.

The threshold is the system parameter aba_sales.max_discount_pct (default 10).
""",
    "author": "EEY AAY",
    "category": "Sales",
    "license": "LGPL-3",
    "depends": ["sale_management"],
    "data": [
        "security/aba_sales_security.xml",
        "security/ir.model.access.csv",
        "data/aba_sales_data.xml",
        "views/aba_discount_request_views.xml",
        "views/sale_order_views.xml",
        "views/report_proforma.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
