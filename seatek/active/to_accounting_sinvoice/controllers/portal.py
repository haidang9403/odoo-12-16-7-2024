import base64

from odoo import http
from odoo.http import request, content_disposition
from odoo.addons.account.controllers import portal
from odoo.exceptions import AccessError, MissingError


class PortalAccount(portal.PortalAccount):

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        """
        Override to add support for downloading S-Invoice in zipped XML
        """
        try:
            invoice_sudo = self._document_check_access('account.invoice', invoice_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        if report_type == 'xml':
            return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)
        else:
            return super(PortalAccount, self).portal_my_invoice_detail(invoice_id, access_token, report_type, download, **kw)

    def _show_report(self, model, report_type, report_ref, download=False):
        """
        Override to add support for downloading S-Invoice in zipped XML
        """
        if model._name == 'account.invoice' and model.sinvoice_state != 'not_issued' and report_type == 'xml':
            try:
                model._ensure_sinvoice_representation_files(retries=3)
            except MissingError as e:
                return str(e)

            filecontent = base64.b64decode(model.sinvoice_representation_zip)
            reporthttpheaders = [
                ('Content-Type', 'application/zip'),
                ('Content-Length', len(filecontent)),
            ]
            if download:
                reporthttpheaders.append(('Content-Disposition', content_disposition(model.sinvoice_representation_filename_zip)))
            return request.make_response(filecontent, headers=reporthttpheaders)
        else:
            return super(PortalAccount, self)._show_report(model, report_type, report_ref, download)

