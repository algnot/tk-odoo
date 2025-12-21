from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    note = fields.Html(string='Terms and Conditions')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = (
                "<ul>"
                "<li>สามารถชำระเงินได้ผ่านธนาคาร กสิกรไทย เลขที่บัญชี <strong>143-1-34439-0</strong> ชื่อบัญชี <strong>ธนวัฒน์ ตลับทอง</strong></li>"
                "<li>การชำระเงินนอกเหนือวันที่ใบเสนอราคานี้มีผล <b>ให้ถือว่าข้อเสนอในใบเสนอราคานี้เป็นอันสิ้นสุดและจำเป็นต้องออกใบเสนอราคาฉบับใหม่</b></li>"
                "</ul>"
            )
        return super(SaleOrder, self).create(vals)
