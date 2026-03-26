from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tk_receipt_invoice_ids = fields.Many2many(
        comodel_name="account.move",
        relation="tk_sale_order_payment_receipt_invoice_rel",
        column1="payment_id",
        column2="move_id",
        string="Receipt Invoices",
        help="Invoices intended to be referenced on the receipt before posting/reconciliation.",
        copy=False,
    )

    is_withholding_registation = fields.Boolean(
        string="Withholding Tax",
        default=False,
    )
    withholding_percent = fields.Float(
        string="Withholding (%)",
        default=3.0,
        digits=(16, 4),
    )
    withholding_amount = fields.Monetary(
        string="Withholding Amount",
        currency_field="currency_id",
        compute="_compute_withholding",
        store=True,
    )
    net_amount = fields.Monetary(
        string="Net Amount",
        currency_field="currency_id",
        compute="_compute_withholding",
        store=True,
    )

    @api.depends("amount", "is_withholding_registation", "withholding_percent", "currency_id")
    def _compute_withholding(self):
        for pay in self:
            if pay.is_withholding_registation and pay.withholding_percent:
                wht = pay.amount * (pay.withholding_percent / 100.0)
            else:
                wht = 0.0
            pay.withholding_amount = wht
            pay.net_amount = pay.amount - wht

    @api.constrains("withholding_percent")
    def _check_withholding_percent(self):
        for pay in self:
            if pay.withholding_percent < 0 or pay.withholding_percent > 100:
                raise ValidationError("Withholding (%) must be between 0 and 100.")

    def action_post_payment(self):
        self.ensure_one()
        # Post the payment entry.
        self.action_post()

        # Try to reconcile against the intended invoice(s) so the invoice becomes Paid.
        moves = self.tk_receipt_invoice_ids
        if moves:
            domain = [
                ("parent_state", "=", "posted"),
                ("account_type", "in", self._get_valid_payment_account_types()),
                ("reconciled", "=", False),
            ]
            payment_lines = self.move_id.line_ids.filtered_domain(domain)
            lines = moves.line_ids.filtered_domain(domain)

            for account in (payment_lines + lines).account_id:
                (payment_lines + lines).filtered_domain([
                    ("account_id", "=", account.id),
                    ("reconciled", "=", False),
                    ("parent_state", "=", "posted"),
                ]).reconcile()

            moves.matched_payment_ids += self

        return True

    def action_preview_receipt(self):
        self.ensure_one()
        report = self.env.ref("account.action_report_payment_receipt")
        url = f"/report/pdf/{report.report_name}/{self.id}?download=false"
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }

