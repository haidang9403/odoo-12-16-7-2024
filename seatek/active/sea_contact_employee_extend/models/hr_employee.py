from odoo import api, models


class HREmployee(models.Model):
    _inherit = "hr.employee"

    @api.multi
    def default_data_contact_for_employee(self, dng_fc=False):
        for rec in self:
            print("dng_fc: ", dng_fc)
            property_product_pricelist = self.env['product.pricelist'].sudo().search(
                [('company_id', '=', 30 if dng_fc else self.env.user.company_id.id), ('is_default', '=', True)])
            partner = {'name': rec.name,
                       'display_name': rec.name,
                       'property_product_pricelist': property_product_pricelist.id
                       if property_product_pricelist else False,
                       'email': rec.sea_personal_email,
                       'phone': rec.main_phone_number,
                       'mobile': rec.main_phone_number,
                       '''property_product_pricelist=SeaFamily'''
                       'company_ids': [
                           (6, False, [30] if dng_fc else rec.sea_company_ids.ids)],
                       'company_type': 'person' if dng_fc else 'employee',
                       'customer': dng_fc,
                       'sea_business_code': False if dng_fc else rec.s_identification_id,
                       'employee_id': False if dng_fc else rec.id,
                       'is_employee': not dng_fc,
                       'supplier': not dng_fc,
                       'lang': 'vi_VN',
                       'tz': 'Asia/Ho_Chi_Minh'
                       }
            if dng_fc:
                partner['custom_type_id'] = 1
                partner['group_ids'] = [(6, False, [1])]

            return partner

    @api.model
    def create(self, vals):
        if 'sea_company_ids' in vals:
            if self.env.user.company_id.id not in vals['sea_company_ids'][0][2]:
                vals['sea_company_ids'][0][2].append(self.env.user.company_id.id)
        else:
            vals.update({'sea_company_ids': [[6, False, [self.env.user.company_id.id]]]})

        if not vals.get('user_id'):
            user = self.env['res.users'].sudo().create(
                {'name': vals.get('name'), 'login': vals.get('s_identification_id'),
                 'password': vals.get('s_identification_id'),
                 'company_ids': vals.get('sea_company_ids'),
                 'company_id': self.env.user.company_id.id,
                 'notification_type': 'inbox',
                 'employee_id': False})
            vals['user_id'] = user.id
            # values ={}
            # values.update(vals)
            # values.update({'user_id': user.id, 'password': str(password)})
            # self.send_mail(values)
        else:
            user = self.env['res.users'].sudo().search([('id', '=', vals['user_id'])])
        rec = super(HREmployee, self).create(vals)
        check = True
        if user:
            if user.partner_id and not self.env['res.partner'].sudo().search([('employee_id', '=', rec.id)]):
                user.partner_id.write(rec.default_data_contact_for_employee())
                check = False
        if check:
            partner = self.env['res.partner'].create([rec.default_data_contact_for_employee()])
            user.partner_id = partner.id if partner else False

        for company_id in user.partner_id.company_ids.ids:
            acc = self.env['account.account'].sudo().search(
                [('company_id', '=', company_id), ('code', '=', '141')], limit=1)
            if acc and user.partner_id:
                user.partner_id.with_context(force_company=company_id).write(
                    {'property_account_payable_id': acc.id})

        '''một số hardcode tạo mới contact cho DNG retail 2, 29'''
        # if self.env.user.company_id.id in [30]:
        self.env['res.partner'].sudo().create([rec.default_data_contact_for_employee(True)])
        return rec

    #
    # def send_mail(self, vals):
    #     body = '<center><table style="width: 500px; background-color: bisque; font-size: 16pt;" border="0">'  \
    #                     '<tr> <td colspan="2">User account: <b>' + vals['name'] + '</b> has been created </td>'  \
    #                     '</tr> <tr> <td colspan="2">Login Information: </td></tr>'  \
    #                     '<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>' \
    #                             '<u>Username:</u> <b>' + vals['s_identification_id'] +'</b> <br />' \
    #                             '<u>Password:</u> <b>' + vals['password'] + '</b>'  \
    #                         '</td></tr><tr><td colspan="2"> ' \
    #                             '<a href="https://docs.google.com/document/d/1YvMdrRLcgURfUJaXRyi9GcIkB2N3BUQHF6sCw6ou9V4/edit?usp=share_link">Click here </a>' \
    #                             ' to see instructions for changing password</td></tr></table></center>'
    #     mail_to = 'user@seacorp.vn'
    #     mail_from = '"seaerp" <info@seacorp.vn>'
    #     template_obj = self.env['mail.mail']
    #     template_data = {
    #         'subject': 'Welcome to Seaerp',
    #         'body_html': body,
    #         'email_from': mail_from,
    #         'email_to': mail_to
    #     }
    #     template_id = template_obj.create(template_data)
    #     template_obj.send(template_id)
    #     print('Mail ID 1: ', template_id)
    #
    #     if vals['sea_personal_email']:
    #         template_data.update({'email_to': vals['sea_personal_email']})
    #         template_id = template_obj.create(template_data)
    #         template_obj.send(template_id)
    #         print('Mail ID 2: ', template_id)
    #     # if vals['send_to_mails']:
    #     #     for id_user in vals['send_to_mails'][0][2]:
    #     #         print('user id: ', id_user)
    #     #         login_user = self.env['res.users'].sudo().search([('id', '=', id_user)])['login']
    #     #         employee_mail = self.env['hr.employee'].sudo().search([('s_identification_id', '=', login_user)])['sea_personal_email']
    #     #         if employee_mail:
    #     #             template_data.update({'email_to': employee_mail})
    #     #             template_id = template_obj.create(template_data)
    #     #             template_obj.send(template_id)
    #
    #     return

    @api.multi
    def write(self, value):
        res = super(HREmployee, self).write(value)
        for rec in self:
            contacts = rec.env['res.partner'].sudo().search(
                [('employee_id', '=', rec.id)])
            for contact in contacts:
                if not set(rec.sea_company_ids.ids).issubset(contact.company_ids.ids):
                    contact.company_ids.ids.extend(
                        [item for item in rec.sea_company_ids.ids if item not in contact.company_ids.ids])
        return res
