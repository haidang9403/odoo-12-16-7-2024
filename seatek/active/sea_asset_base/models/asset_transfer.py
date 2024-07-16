from odoo import models, fields,api


class AssetTransfer(models.Model):
    _name = "asset.transfer"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Asset Transfer'
    _order = 'acceptance_date desc'

    name = fields.Char('Code',default='')
    active = fields.Boolean(string='active',default=True)
    owner_company_id=fields.Many2one('res.company', 'Owner Company',default =lambda self:self.env.user.company_id.id)
    source_company_id = fields.Many2one('res.company', 'Company',default =lambda self:self.env.user.company_id.id)
    source_location_id = fields.Many2one('sea.office', 'Source Location')
    source_department_temporary = fields.Many2one('hr.department.temporary', string='Department #', domain="[('company_id','=',source_company_id)]")
    dest_location_id = fields.Many2one('sea.office', 'Destination Location',required=False)
    dest_company_id=fields.Many2one('res.company',string='Dest Company',required=False,default =lambda self:self.env.user.company_id.id)
    dest_department = fields.Many2one('hr.department', string='Default Department.')
    dest_department_temporary = fields.Many2one('hr.department.temporary', string='Department #', domain="[('company_id','=',dest_company_id)]")
    dest_asset_user_default_temporary = fields.Many2one('hr.employee.temporary', string='To Default User #', domain="[('department_id','in',"
                                                                                                                    "[dest_department])]")

    @api.onchange('dest_location_id')
    def onchange_dest_location_id(self):
        if self.dest_location_id:
            for line in self.asset_transfer_line_ids:
                line.dest_location_id=self.dest_location_id.id
    @api.onchange('dest_company_id')
    def onchange_dest_company_id(self):
        domain={}

        if self.dest_company_id:
            self.dest_department_temporary=False
            for line in self.asset_transfer_line_ids:
                line.dest_company=self.dest_company_id.id
                line.dest_department_temporary = False
                line.dest_asset_user_temporary = False
            domain = {'dest_asset_user_default_temporary': [('company_id', '=', self.dest_company_id.id)
                                                            ]}
            return {'domain': domain}
        return domain

    @api.model
    @api.onchange('dest_department_temporary')
    def onchange_dest_department_temporary(self):
        domain = {}
        if self.dest_department_temporary:
            for line in self.asset_transfer_line_ids:
                line.dest_department_temporary = self.dest_department_temporary.id
                line.dest_asset_user_temporary = False
            domain = {'dest_asset_user_default_temporary': [('department_id', '=', self.dest_department_temporary.department_id.id)
                                                                        ]}
            if self.dest_department_temporary.department_id:
                self.dest_department = self.dest_department_temporary.department_id.id
            return {'domain': domain}
        return domain

    @api.onchange('dest_asset_user_default_temporary')
    def onchange_dest_asset_user_default_temporary(self):
        if self.dest_asset_user_default_temporary:
            for line in self.asset_transfer_line_ids:
                line.dest_asset_user_temporary = self.dest_asset_user_default_temporary.id

    source_asset_user_default_temporary=fields.Many2one('hr.employee.temporary',string='From Default User #', domain="[('department_id','=',dest_department)]")
    acceptance_date = fields.Datetime('Acceptance Date',required=False,default=lambda self: fields.Datetime.now())
    validate_date = fields.Datetime('Acceptance Date')
    acceptance_number = fields.Char('Acceptance Number')

    handover_party = fields.Char('Handover Party')
    receiver_handover_party = fields.Char('Receiver Party')
    from_user=fields.Char(string='From User')
    to_user=fields.Char(string='To User')
    asset_transfer_line_ids = fields.One2many('asset.transfer.line', 'asset_transfer_id', string='Transfer Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('transfer', 'Transfer'),
        ('done', 'Done'),
        ('validated', 'Validated'),
        ('cancel', 'Cancel')], string='Status', default='draft', index=True)
    handover_party = fields.Char(string='Handover Party')
    receiver_handover_party = fields.Char(string='Receiver Party')
    shipping_party=fields.Char(string='Shipping Party')
    transfer_type = fields.Selection([('asset_recovery', 'Asset Recovery'), ('asset_transfer', 'Asset Transfer')],required=True,default='asset_transfer')

    @api.onchange('transfer_type')
    def _onchange_transfer_type(self):
        if self.transfer_type=='asset_recovery':
            if self.dest_company_id.id!=self.owner_company_id.id:
                self.dest_company_id = self.owner_company_id.id
                self.dest_department_temporary = False
                self.dest_asset_user_default_temporary = False
                for line in self.asset_transfer_line_ids:
                    line.dest_company = self.owner_company_id.id
                    line.dest_department_temporary = self.dest_department_temporary.id
                    line.dest_asset_user_temporary = self.dest_asset_user_default_temporary.id



    def set_state_done(self):
        self.write({'state':'done'})
    def set_state_transfer(self):
        self.write({'state':'transfer'})
    def set_state_validated(self):
        self.write({'state': 'validated'})
        for asset_transfer_line in self.asset_transfer_line_ids:
            asset_transfer_line.validate_date=fields.Datetime.now()
            asset=self.env['account.asset.asset'].sudo().search([('id','=',asset_transfer_line.asset_id.id)])
            if asset:
                if asset_transfer_line.transfer_type == 'asset_transfer':
                    if asset.latest_asset_transfer_date:
                        '''if asset already transfer'''
                        '''check date transfer for update asset'''
                        if self.acceptance_date>=asset.latest_asset_transfer_date:
                            asset.write({'latest_asset_transfer_date': self.acceptance_date})
                            asset.write({'latest_inventory_status': asset_transfer_line.asset_status_transfer})
                            asset.write({'sea_office_id': self.dest_location_id.id})
                            asset.write({'asset_user_temporary': asset_transfer_line.dest_asset_user_temporary.id})
                            asset.write({'management_dept': asset_transfer_line.dest_department.id})
                            asset.write({'company_using': asset_transfer_line.dest_company.id})
                            asset.write({'transfer_type': 'asset_transfer'})
                            asset.write({'handover_party': self.handover_party})
                            asset.write({'receiver_handover_party': self.receiver_handover_party})

                    else:

                        '''if asset not transfer yet'''
                        asset.write({'latest_asset_transfer_date': self.acceptance_date})
                        asset.write({'latest_inventory_status': asset_transfer_line.asset_status_transfer})
                        asset.write({'sea_office_id': self.dest_location_id.id})
                        asset.write({'asset_user_temporary': asset_transfer_line.dest_asset_user_temporary.id})
                        asset.write({'management_dept': asset_transfer_line.dest_department.id})
                        asset.write({'company_using': asset_transfer_line.dest_company.id})
                        asset.write({'transfer_type': 'asset_transfer'})
                        asset.write({'handover_party': self.handover_party})
                        asset.write({'receiver_handover_party': self.receiver_handover_party})
                else:
                    if asset.asset_receive_date:
                        '''if asset already transfer'''
                        '''check recovery date for update asset'''
                        if self.acceptance_date>=asset.asset_receive_date:
                            asset.write({'latest_inventory_status': asset_transfer_line.asset_status_transfer})
                            asset.write({'sea_office_id': self.dest_location_id.id})
                            asset.write({'asset_user_temporary': asset_transfer_line.dest_asset_user_temporary.id})
                            asset.write({'management_dept': asset_transfer_line.dest_department.id})
                            asset.write({'company_using': asset_transfer_line.dest_company.id})
                            asset.write({'asset_receive_date': fields.Datetime.now()})
                            asset.write({'transfer_type': 'asset_recovery'})
                            asset.write({'handover_party': self.handover_party})
                            asset.write({'receiver_handover_party': self.receiver_handover_party})

                    else:
                        asset.write({'latest_inventory_status': asset_transfer_line.asset_status_transfer})
                        asset.write({'sea_office_id': self.dest_location_id.id})
                        asset.write({'asset_user_temporary': asset_transfer_line.dest_asset_user_temporary.id})
                        asset.write({'management_dept': asset_transfer_line.dest_department.id})
                        asset.write({'company_using': asset_transfer_line.dest_company.id})
                        asset.write({'asset_receive_date': fields.Datetime.now()})
                        asset.write({'transfer_type': 'asset_recovery'})
                        asset.write({'handover_party': self.handover_party})
                        asset.write({'receiver_handover_party': self.receiver_handover_party})

    def export_xls(self):
        data = {
            'name':self.name,
            'company_id': self.source_company_id.ids,
        }
        return self.env.ref('sea_asset_base.action_export_asset_transfer').report_action(self, data=data)

    @api.model
    def create_asset_transfer_line(self,records):
        for record in records:
            res=self.env['asset.transfer.line'].sudo().create({'asset_transfer_id':self.id,'asset_id':record.id,'dest_company':self.env.user.company_id.id,
                                                               'source_location_id':record.sea_office_id.id,
                                                               'source_asset_user_temporary':record.asset_user_temporary.id,
                                                               'transfer_type':'asset_transfer'})

    @api.multi
    def write(self, vals):
        validated=False
        if 'state' in vals:
            if vals.get('state')=='validated':
                vals.update({'validate_date':fields.Datetime.now()})
                validated = True
        res =super(AssetTransfer, self).write(vals)
        # if validated:
        #     for asset_transfer_line in self.asset_transfer_line_ids:
        #         if asset_transfer_line.asset_id:
        #             if asset_transfer_line.transfer_type=='asset_transfer':
        #                 asset_transfer_line.asset_id.write({'latest_asset_transfer_date':fields.Datetime.now()})
        #             else:
        #                 asset_transfer_line.asset_id.write({'asset_receive_date': fields.Datetime.now()})
        return res
class AssetTransferLine(models.Model):
    _name = 'asset.transfer.line'
    _description = 'Asset Transfer Line'

    asset_transfer_id = fields.Many2one('asset.transfer', string='Asset Transfer')
    asset_id = fields.Many2one('account.asset.asset', 'Asset Name', domain=lambda self: [('company_id','=',self.env.user.company_id.id),
                                                                                         ('company_using', '=', self.asset_transfer_id.source_company_id.id),
                                                                                         ('state','=','open'),
                                                                                         ('management_dept','=',
                                                                                          self.asset_transfer_id.source_department_temporary.department_id.id)])

    @api.depends('asset_transfer_id')
    def compute_company_id_compute(self):
        for rec in self:
            if rec.asset_transfer_id:
                rec.compute_company_id_compute=rec.asset_transfer_id.dest_company_id.id
    company_id_compute=fields.Many2one('res.company',string='Company',compute='compute_company_id_compute')



    @api.onchange('asset_transfer_id','asset_id')
    def _onchange_asset_transfer(self):
        asset_ids = []
        for line in self.asset_transfer_id.asset_transfer_line_ids:
            asset_ids.append(line.asset_id.id)
        if self.asset_transfer_id.source_department_temporary:
            domain = {'asset_id': ['|',('company_id','=',self.env.user.company_id.id),
                                   ('company_using', '=', self.asset_transfer_id.source_company_id.id),
                                     ('state','=','open'),
                                     ('management_dept','=',self.asset_transfer_id.source_department_temporary.department_id.id),

                                   ('id','not in',asset_ids)]}
        else:
            domain = {'asset_id': ['|',('company_id', '=', self.env.user.company_id.id),
                                   ('company_using', '=', self.asset_transfer_id.source_company_id.id),
                                   ('state', '=', 'open'),('id','not in',asset_ids)]}
        return {'domain': domain}
    @api.onchange('asset_id')
    @api.model
    def onchange_asset_id(self):
        if self.asset_id.company_id.id==self.dest_company.id:
            self.transfer_type='asset_recovery'
        else:
            self.transfer_type = 'asset_transfer'
        self.quantity_demanding=self.asset_id.quantity
        self.quantity_done=self.asset_id.quantity
        self.asset_management_dept_staff_temporary=self.asset_id.asset_management_dept_staff_temporary
        if self.asset_id.asset_user_temporary:
            self.source_asset_user_temporary=self.asset_id.asset_user_temporary.id
        if self.asset_transfer_id.dest_company_id:
            self.dest_company=self.asset_transfer_id.dest_company_id.id
        if self.asset_transfer_id.dest_location_id:
            self.dest_location_id = self.asset_transfer_id.dest_location_id.id
        if self.asset_transfer_id.dest_asset_user_default_temporary:
            if self.asset_transfer_id.dest_asset_user_default_temporary.department_id:
                self.dest_department=self.asset_transfer_id.dest_asset_user_default_temporary.department_id.id
        self.dest_department_temporary=self.asset_transfer_id.dest_department_temporary.id
        self.dest_asset_user_temporary = self.asset_transfer_id.dest_asset_user_default_temporary.id

        if self.asset_id.latest_inventory_status:
            self.asset_status_transfer=self.asset_id.latest_inventory_status
        if self.asset_id.sea_office_id:
            self.source_location_id=self.asset_id.sea_office_id.id
        self.transfer_type=self.asset_transfer_id.transfer_type

    @api.onchange('dest_company')
    @api.model
    def _onchange_dest_company(self):
        self.dest_department_temporary=self.asset_transfer_id.dest_department_temporary.id
        self.dest_asset_user_temporary=self.asset_transfer_id.dest_asset_user_default_temporary.id


    asset_code = fields.Char('Asset code', related='asset_id.code')
    validate_date = fields.Datetime('Acceptance Date')
    quantity_demanding = fields.Float('Quantity Demand')
    quantity_done = fields.Float('Quantity Done')
    uom_id = fields.Many2one('uom.uom', 'Unit', related='asset_id.asset_uom')
    alt_unit = fields.Char('Alt Unit', related='asset_id.alt_unit')
    asset_status_transfer = fields.Selection([
        ('good', 'Good'),
        ('damaged_waiting_for_repair', 'damaged waiting for repair'),
        ('damaged_waiting_for_liquidation', 'damaged waiting for liquidation'),
        ('self_destruct', 'Self destruct')],
        'Asset Status Transfer',required=False)
    acceptance_number=fields.Char('Acceptance Number',related='asset_transfer_id.acceptance_number')
    @api.model
    def create(self,vals):
        asset=self.env['account.asset.asset'].sudo().search([('id','=',vals.get('asset_id'))])
        asset_transfer_id=self.env['asset.transfer'].sudo().search([('id','=',vals.get('asset_transfer_id'))])
        '''Tam thoi de quantity = voi quantity assset'''
        if asset:
            vals.update({'quantity_demanding':asset.quantity})
            vals.update({'quantity_done':asset.quantity})
            vals.update({'source_location_id':asset.sea_office_id.id})
            vals.update({'dest_location_id':asset_transfer_id.dest_location_id.id})
            vals.update({'dest_company': asset_transfer_id.dest_company_id.id})
            vals.update({'asset_management_dept_staff_temporary':asset.asset_management_dept_staff_temporary.id})
            vals.update({'source_asset_user_temporary':asset.asset_user_temporary.id})

        if 'asset_management_dept_staff_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('asset_management_dept_staff_temporary'))])
            if temporary:
                vals.update({'asset_management_dept_staff':temporary.employee_id.id})
        if 'source_asset_user_temporary' in vals:
            employee_temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('source_asset_user_temporary'))])
            if employee_temp:
                vals.update({'source_asset_user': employee_temp.employee_id.id})
        if 'dest_asset_user_temporary' in vals:
            employee_temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('dest_asset_user_temporary'))])
            if employee_temp:
                vals.update({'dest_asset_user':employee_temp.employee_id.id})
        return super(AssetTransferLine, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'asset_management_dept_staff_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('asset_management_dept_staff_temporary'))])
            if temporary:
                vals.update({'asset_management_dept_staff':temporary.employee_id.id})
        if 'source_asset_user_temporary' in vals:
            employee_temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('source_asset_user_temporary'))])
            if employee_temp:
                vals.update({'source_asset_user': employee_temp.employee_id.id})
        if 'dest_asset_user_temporary' in vals:
            employee_temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('dest_asset_user_temporary'))])
            if employee_temp:
                vals.update({'dest_asset_user':employee_temp.employee_id.id})
        if self.asset_transfer_id.dest_company_id:
            vals.update({'dest_company':self.asset_transfer_id.dest_company_id.id})
        if self.asset_transfer_id.dest_location_id:
            vals.update({'dest_location_id': self.asset_transfer_id.dest_location_id.id})
        asset = self.env['account.asset.asset'].sudo().search([('id', '=', vals.get('asset_id'))])
        '''Tam thoi de quantity = voi quantity assset'''
        if asset:
            vals.update({'source_location_id': asset.sea_office_id.id})
            vals.update({'asset_management_dept_staff_temporary': asset.asset_management_dept_staff_temporary.id})
        return super(AssetTransferLine, self).write(vals)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('transfer', 'Transfer'),
        ('done', 'Done'),
        ('validated', 'Validated'),
        ('cancel', 'Cancel')], string='Status', default='draft', index=True,related='asset_transfer_id.state',store=True)
    source_location_id = fields.Many2one('sea.office', 'Source Location')
    source_asset_user_temporary = fields.Many2one('hr.employee.temporary', 'From User #', required=False)
    source_asset_user = fields.Many2one('hr.employee.multi.company', 'Asset Employee.')
    dest_company=fields.Many2one('res.company',string='Company')
    dest_department = fields.Many2one('hr.department', string='Department.')
    dest_department_temporary = fields.Many2one('hr.department.temporary', string='Department #',domain="[('company_id','=',dest_company)]")
    @api.onchange('dest_department_temporary')
    def onchange_dest_department_temporary(self):
        if self.dest_department_temporary.department_id:
            self.dest_department=self.dest_department_temporary.department_id.id
            domain = {'dest_asset_user_temporary': [('department_id', '=', self.dest_department_temporary.department_id.id)
                                  ]}
            return {'domain': domain}
    dest_asset_user_temporary = fields.Many2one('hr.employee.temporary', 'To User #', required=False)
    dest_asset_user = fields.Many2one('hr.employee.multi.company', 'Destination Employee.')
    dest_location_id = fields.Many2one('sea.office', 'Destination Location',required=False)
    asset_uom = fields.Many2one('uom.uom', 'Unit of Measure',related='asset_id.asset_uom')
    asset_management_dept_staff_temporary = fields.Many2one('hr.employee.temporary', string='Asset Management Dept Staff #')
    asset_management_dept_staff = fields.Many2one('hr.employee.multi.company', string='Asset Management Dept Staff',domain="[('department_id','=',235)]")
    note= fields.Char(string='Note')
    transfer_type=fields.Selection([('asset_recovery','Asset Recovery'),('asset_transfer','Asset Transfer')],related='asset_transfer_id.transfer_type')