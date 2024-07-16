import base64

from odoo import models, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        # OVERRIDE: replace the PDF version generated by Odoo's standard invoice report with the converted version of S-Invoice
        if self.model == 'account.invoice' and res_ids and len(res_ids) == 1:
            invoice = self.env['account.invoice'].browse(res_ids)
            if not invoice.journal_id.send_mail_sinvoice_disabled and invoice.type in ('out_invoice', 'out_refund') and invoice.sinvoice_state != 'not_issued':
                if invoice.journal_id.sinvoice_send_mail_option == 'converted':
                    invoice._ensure_sinvoice_converted_file()
                    pdf_content = base64.b64decode(invoice.sinvoice_converted_file)
                else:
                    invoice._ensure_sinvoice_representation_files()
                    pdf_content = base64.b64decode(invoice.sinvoice_representation_pdf)
        return super(IrActionsReport, self)._post_pdf(save_in_attachment, pdf_content, res_ids)

