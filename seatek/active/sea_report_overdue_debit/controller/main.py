from odoo import http
from odoo.http import request


class Attendance(http.Controller):

    @http.route('/load/check_mark_as_todo', type="json", website=True, auth='user')
    def load_calendar(self, id):
        return request.env['res.partner'].sudo().search(
            [('id', '=', id)], limit=1).mark_as_todo
