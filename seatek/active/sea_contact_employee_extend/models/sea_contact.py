# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.osv.expression import get_unaccent_wrapper


class SeaContactEmployee(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [('model_sea_business_code_uniq', 'unique(sea_business_code)',
                         'Contact with this sea_business_code is  already exist!!')]
    company_type = fields.Selection(
        selection_add=[('employee', 'Employee'), ('internal', 'Internal')])
    is_employee = fields.Boolean(string='Is a Employee', default=False,
                                 help="Check if the contact is a Employee, "
                                      "otherwise it is a person and company and Internal")
    is_internal = fields.Boolean(string='Is a Internal', default=False,
                                 help="Check if the contact is a Internal, "
                                      "otherwise it is a person and company and employee")
    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select the employee for contact')

    is_owner = fields.Boolean(string='Is owner', default=False)

    # type = fields.Selection(
    #     selection_add=[('vat', 'VAT address'), ])

    partner_vat_ids = fields.Many2many('res.partner', 'children_partner_vat_rel', 'parent_id', 'child_id',
                                       help="VAT address for current Contact.", string='VAT Address')
    partner_invoice_ids = fields.Many2many('res.partner', 'children_partner_inv_rel', 'parent_id', 'child_id',
                                           help="Invoice address for current Contact.", string='Invoice Address')

    @api.constrains('employee_id')
    def onchange_sea_company_ids(self):
        for rec in self:
            if rec.employee_id:
                check = rec.env['res.partner'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id), ('id', '!=', rec.id)])
                if check:
                    raise UserError(_("Nhân viên này thuộc về người liên hệ " + check.name))
                elif rec.is_employee:
                    rec.update({'sea_business_code': rec.employee_id.s_identification_id})

    @api.model
    def create_contact_action(self):
        # print("create_contact_action")
        '''create_contact_action'''
        self.env.cr.execute(
            "SELECT DISTINCT a.id,a.name, a.s_identification_id "
            "FROM public.hr_employee as a , hr_employee_multi_company as b "
            "WHERE b.employee_current_status!='resigned' and a.id=b.name "
            "and  a.active='true' and b.active='true' order by id asc")
        list_employee = self.env.cr.dictfetchall()
        # print("list_employee:", len(list_employee))
        for employee in list_employee:
            self.create_for_employee(self.env['hr.employee'].sudo().search([('id', '=', employee.get('id'))], limit=1),
                                     False)
            # employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
            #     [('employee_current_status', '!=', 'resigned'), ('primary_company', '=', 'true'),
            #      ('name', '=', employee.get('id'))],
            #     limit=1)
            # account_id = False
            # property_product_pricelist = False
            # if employee_multi_id:
            #     account_id = self.env['account.account'].search(
            #         [('company_id', '=', employee_multi_id.company_id.id), ('code', '=', '141')])
            #     property_product_pricelist = self.env['product.pricelist'].search(
            #         [('company_id', '=', employee_multi_id.company_id.id), ('is_default', '=', True)])
            # check = self.env['res.partner'].sudo().search([('employee_id', '=', employee.get('id'))])
            # if not check:
            #     val = [{'company_id': 1, 'company_ids': [[6, False, [1]]],
            #             'name': employee.get('name'), 'display_name': employee.get('name'),
            #             'sea_business_code': employee.get('s_identification_id'),
            #             'property_product_pricelist': property_product_pricelist.id if property_product_pricelist else False,
            #             'is_employee': True, 'company_type': 'employee',
            #             'employee_id': employee.get('id'), 'customer': False, 'supplier': True,
            #             'email': employee.get('sea_personal_email'),
            #             'phone': employee.get('main_phone_number'),
            #             'mobile': employee.get('main_phone_number'),
            #             'property_account_payable_id': account_id.id if account_id else False}]
            #     self.env['res.partner'].create(val)
            #     print("create done ", "::: ", employee.get('name'), employee.get('s_identification_id'),
            #           employee_multi_id.name.name, " -- ", employee_multi_id.company_id.name, " -- ",
            #           account_id.name if account_id else "NONE", " ++ ",
            #           property_product_pricelist.name if property_product_pricelist else "NONE")

    @api.depends('is_employee', 'is_internal', 'is_company')
    def _compute_company_type(self):
        for partner in self:
            partner.company_type = 'company' if partner.is_company \
                else 'employee' if partner.is_employee \
                else 'internal' if partner.is_internal else 'person'

    def _write_company_type(self):
        for partner in self:
            is_internal = False
            is_employee = False
            is_company = False
            if partner.company_type == 'company':
                is_company = True
            elif partner.company_type == 'employee':
                is_employee = True
            elif partner.company_type == 'internal':
                is_internal = True
            partner.is_employee = is_employee
            partner.is_company = is_company
            partner.is_internal = is_internal
            if partner.employee_id and not is_employee:
                partner.write({'employee_id': False})

    @api.onchange('company_type')
    def onchange_company_type(self):
        for partner in self:
            is_employee = False
            is_company = False
            is_internal = False
            if partner.company_type == 'company':
                is_company = True
            elif partner.company_type == 'employee':
                is_employee = True
            elif partner.company_type == 'internal':
                is_internal = True
            partner.update({'is_company': is_company})
            partner.update({'is_internal': is_internal})
            partner.update({'is_employee': is_employee})

    # @api.model
    # def create(self, values):
    #     print("value: ", values)
    #     res = super(SeaContactEmployee, self).create(values)
    #     return res

    @api.multi
    def create_for_employee(self, employee, company):
        # print("create_contact")
        rec = False
        employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
            [('employee_current_status', '!=', 'resigned'), ('primary_company', '=', 'true'),
             ('name', '=', employee.id)],
            limit=1)
        property_product_pricelist = False
        if employee_multi_id:
            property_product_pricelist = self.env['product.pricelist'].sudo().search(
                [('company_id', '=', employee_multi_id.company_id.id), ('is_default', '=', True)])
        elif company:
            property_product_pricelist = self.env['product.pricelist'].sudo().search(
                [('company_id', '=', company.id), ('is_default', '=', True)])
        check = self.env['res.partner'].sudo().search([('employee_id', '=', employee.id)])
        if not check:
            val = [{'company_ids': [(6, False, employee.sea_company_ids.ids)],
                    'name': employee.name,
                    'display_name': employee.name,
                    'sea_business_code': employee.s_identification_id,
                    'property_product_pricelist': property_product_pricelist.id
                    if property_product_pricelist else False,
                    'is_employee': True, 'company_type': 'employee',
                    'employee_id': employee.id, 'customer': False, 'supplier': True,
                    'email': employee.sea_personal_email,
                    'phone': employee.main_phone_number,
                    'mobile': employee.main_phone_number,
                    # 'property_account_payable_id': account_id.id if account_id else False
                    }]
            # print("value: ", val, " -- ", property_product_pricelist, " -- ",
            #       employee_multi_id.company_id.name)
            # print("acount_list: ", account_list)

            rec = self.env['res.partner'].sudo().create(val)
            for company_id in self.env['res.company'].sudo().search([]):
                if self.env['account.account'].sudo().search(
                        [('company_id', '=', company_id.id), ('code', '=', '141')]):
                    rec.with_context(force_company=company_id.id).write(
                        {'property_account_payable_id': self.env['account.account'].sudo().search(
                            [('company_id', '=', company_id.id), ('code', '=', '141')]).id})
            # print("create done ", "::: ", employee.name, employee.s_identification_id,
            #       employee_multi_id.name.name, " -- ", employee_multi_id.company_id.name, " -- ",
            #       account_id.name if account_id else "NONE", " ++ ",
            #       property_product_pricelist.name if property_product_pricelist else "NONE")
        return rec

    '''TKK 04/01/2024'''
    contact_code = fields.Char(string='Contact Code', index=True)

    @api.constrains('company_type', 'vat', 'phone', 'sea_business_code')
    def set_default_contact_code(self):
        for rec in self:
            rec.check_uniq_contact()
            contact_code = {
                'employee': rec.sea_business_code,
                'company': rec.vat,
            }.get(rec.company_type, rec.phone)

            if rec.contact_code != contact_code:
                rec.contact_code = contact_code

    @api.multi
    @api.constrains('parent_id')
    def check_uniq_contact(self):
        for rec in self:
            if not rec.parent_id:
                domain, error = [('id', '!=', rec.id), ('company_id', '=', rec.company_id.id),
                                 ('parent_id', '=', False)], None

                if rec.company_type == 'employee' and rec.sea_business_code:
                    domain.append(('sea_business_code', '=', rec.sea_business_code))
                    error = f"Business Code: {rec.sea_business_code}"
                elif rec.company_type == 'company' and rec.vat:
                    domain.append(('vat', '=', rec.vat))
                    error = f"VAT: {rec.vat}"
                elif rec.phone:
                    domain.append(('phone', '=', rec.phone))
                    error = f"Phone: {rec.phone}"
                if error and self.env['res.partner'].sudo().search_count(domain):
                    raise UserError(_(f"{error} đã tồn tại"))

    @api.constrains('sea_business_code')
    def constrains_sea_business_code(self):
        for rec in self:
            if rec.sea_business_code:
                if self.env['res.partner'].search(
                        [('sea_business_code', '=', rec.sea_business_code), ('id', '!=', self.id)]):
                    raise UserError(_("Business Code already exist!"))

    @api.multi
    # @api.constrains('contact_code', 'ref', 'name')
    def name_get(self):
        # result = []
        # for partner in self:
        #     name = partner._get_name()
        #     if partner.contact_code:
        #         name = name + ' | ' + partner.contact_code
        #     if partner.ref:
        #         name = name + ' | ' + partner.ref
        #     result.append((partner.id, name))
        result = super(SeaContactEmployee, self).name_get()
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=10):
        print('Name unaccent 123 TKK')
        print("args: ", args)

        if args is None:
            args = []

        print("name TKK: ", name)
        print("operator TKK: ", operator)

        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            print('ABC123 TKK')
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            query = """SELECT id
                         FROM res_partner
                      {where} ({contact_code} {operator} {percent}
                           OR {display_name} {operator} {percent}
                           OR {reference} {operator} {percent}
                           OR {name_unaccent} {operator} {percent})
                           -- don't panic, trust postgres bitmap
                     ORDER BY {display_name} {operator} {percent} desc,
                              {display_name}
                    """.format(where=where_str,
                               operator=operator,
                               contact_code=unaccent('contact_code'),
                               display_name=unaccent('display_name'),
                               reference=unaccent('ref'),
                               name_unaccent=unaccent('name_unaccent'),
                               percent=unaccent('%s'))

            where_clause_params += [search_name] * 5
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            partner_ids = map(lambda x: x[0], self.env.cr.fetchall())

            if partner_ids:
                return self.browse(partner_ids).tgl_name_get()
            else:
                return []

        print("TKK self.search(args, limit=limit).tgl_name_get(): ", self.search(args, limit=limit).tgl_name_get())
        return self.search(args, limit=limit).tgl_name_get()

    @api.multi
    def tgl_name_get(self):
        res = []
        for partner in self:
            if partner.name:  # trường hợp field name có giá trị
                name = partner.name
            else:  # trường hợp field name không có giá trị
                name = partner.name_unaccent
            if partner.contact_code:
                name += ' | ' + partner.contact_code
            if partner.ref:
                name += ' | ' + partner.ref
            res.append((partner.id, name))
        return res
