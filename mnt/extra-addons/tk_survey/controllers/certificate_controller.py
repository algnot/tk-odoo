from odoo import http
from odoo.http import request


class SurveyCertificateController(http.Controller):

    @http.route('/survey/certificate/<string:token>', type='http', auth='public', website=True)
    def preview_certificate(self, token):
        user_input = request.env['survey.user_input'].sudo().search(
            [('access_token', '=', token)],
            limit=1
        )

        if not user_input or user_input.state != 'done':
            return request.not_found()

        report_ref = 'tk_survey.action_report_survey_certificate'

        pdf, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
            report_ref,
            res_ids=user_input.ids
        )

        return request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'inline; filename="certificate.pdf"'),
            ]
        )
