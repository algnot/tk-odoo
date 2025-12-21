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
                "<li>การจัดส่งสินค้า/บริการจะดำเนินการภายหลังจากการยืนยันคำสั่งซื้อ</li>"
                "<li>การตกลงราคานอกเหนือจากวันที่ใบเสนอราคานี้มีผล<b>ให้ถือว่าเป็นโมฆะ</b> จำเป็นต้องออกใบเสนอราคาฉบับใหม่</li>"
                "</ul>"
            )
        return super(SaleOrder, self).create(vals)
