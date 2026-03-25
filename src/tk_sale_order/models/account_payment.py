from odoo import models, fields


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

