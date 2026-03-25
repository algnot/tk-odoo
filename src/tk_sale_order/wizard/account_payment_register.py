from odoo import models, _


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _post_payments(self, to_process, edit_mode=False):
        """Keep created payments in Draft when clicking Pay."""
        return

    def _reconcile_payments(self, to_process, edit_mode=False):
        """Skip reconciliation until payments are posted."""
        return

    def action_create_payments(self):
        """Create draft payments and always redirect to them.

        Odoo's base implementation may return True in some edge cases (e.g. sibling
        companies) to avoid redirects. For this customization, we always open the
        created payment(s) so the user can review/post them manually.
        """
        if self.is_register_payment_on_draft:
            self.payment_difference_handling = "open"

        payments = self._create_payments()
        # Keep a reference to the invoices/bills being paid so the receipt can show details
        # even before posting/reconciliation.
        moves = self.line_ids.move_id
        payments.tk_receipt_invoice_ids = moves

        action = {
            "name": _("Payments"),
            "type": "ir.actions.act_window",
            "res_model": "account.payment",
            "context": {"create": False},
        }
        if len(payments) == 1:
            action.update({"view_mode": "form", "res_id": payments.id})
        else:
            action.update({"view_mode": "list,form", "domain": [("id", "in", payments.ids)]})
        return action

