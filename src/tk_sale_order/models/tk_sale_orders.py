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
                "<li>กรุณาชำระเงินมัดจำ 50% ของมูลค่างานทั้งหมดก่อนเริ่มดำเนินการ</li>"
                "<li>ระยะเวลาดำเนินงานทั้งหมดประมาณ 90 วัน โดยจะเริ่มนับหลังจากได้รับการยืนยันคำสั่งซื้อและชำระเงินมัดจำ</li>"
                "</ul>"
            )
        return super(SaleOrder, self).create(vals)
