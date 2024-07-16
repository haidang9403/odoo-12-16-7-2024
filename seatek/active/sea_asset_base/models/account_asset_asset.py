# -*- coding: utf-8 -*-
from odoo import models, fields,api


class AccountAssetAsset(models.Model):
    _inherit = "account.asset.asset"

    @api.multi
    def name_get(self):
        result = []
        for asset in self:
            asset_code=''
            asset_name=''
            if asset.code:
                asset_code='['+asset.code+']'
            if asset.name:
                if len(asset.name)>80:
                    asset_name=asset.name[:80]+'...'
                else:
                    asset_name = asset.name
            name = asset_code + ' ' + asset_name
            result.append((asset.id, name))
        return result

    code = fields.Char(string='Asset Code', size=32, readonly=True, states={'draft': [('readonly', False)]})
    old_code=fields.Char(string='Old Asset Code', size=32)
    state = fields.Selection([('draft', 'Draft'), ('open', 'Running'),('pending','Pending'),('liquidation','Liquidation'),('close', 'Close')], 'Status',
                             required=True, copy=False, default='draft')
    company_id = fields.Many2one('res.company', string='Company Owner', required=True, readonly=True, states={'draft': [('readonly', False)]},
                                 default=lambda self: self.env['res.company']._company_default_get('account.asset.asset'))
    category_id = fields.Many2one('account.asset.category', string='Category', required=True, change_default=True, readonly=True,
                                  states={'draft': [('readonly', False)]},domain="[('company_id','=',company_id)]")
    value = fields.Float(string='Gross Value', required=False, readonly=True, digits=0, states={'draft': [('readonly', False)]}, oldname='purchase_value')
    acceptance_date = fields.Datetime('Acceptance Date')
    acceptance_number = fields.Char('Acceptance Number')
    description = fields.Char('Description')
    quantity = fields.Float('Quantity', required=True, default=1)
    asset_uom = fields.Many2one('uom.uom', 'Unit of Measure')
    alt_unit = fields.Char('Alt Unit')
    management_dept = fields.Many2one('hr.department', 'Usage Management Dept',domain="[('company_id','=',company_using)]")
    asset_user_temporary = fields.Many2one('hr.employee.temporary', 'Asset User #')
    asset_user = fields.Many2one('hr.employee.multi.company', 'Asset User')
    handover_party = fields.Char('Handover Party')
    receiver_handover_party = fields.Char('Receiver Party')
    related_handover_party = fields.Char('Related Party')

    asset_management_dept_staff_temporary = fields.Many2one('hr.employee.temporary', 'Asset Management Dept Staff #')
    asset_management_dept_staff = fields.Many2one('hr.employee.multi.company', 'Asset Management Dept Staff',domain="[('department_id','=',235)]")
    procurement_staff_temporary = fields.Many2one('hr.employee.temporary', 'Procurement Staff #')
    procurement_staff = fields.Many2one('hr.employee.multi.company', 'Procurement Staff')
    asset_status_start = fields.Selection([
        ('good', 'Good'),
        ('damaged_waiting_for_repair', 'Damaged waiting for repair'),
        ('damaged_waiting_for_liquidation', 'Damaged waiting for liquidation'),
        ('self_destruct', 'Self destruct')],
        'Asset Status Start',required=True, default='good')
    latest_inventory_status = fields.Selection([
        ('good', 'Good'),
        ('damaged_waiting_for_repair', 'Damaged waiting for repair'),
        ('damaged_waiting_for_liquidation', 'Damaged waiting for liquidation'),
        ('self_destruct', 'Self destruct')],
        'Latest Inventory Status')

    repair_date = fields.Datetime('Repair Date')
    latest_asset_transfer_date = fields.Datetime('Latest Asset Transfer Date')
    asset_receive_date = fields.Datetime('Asset Receive Date')
    liquidation_date = fields.Datetime('Liquidation Date')
    '''tkk.'''
    asset_type = fields.Many2one('account.asset.type',string='Asset Type')

    note = fields.Text('Note')
    ''''''
    barcode = fields.Char('Barcode')
    dept_owner = fields.Many2one('hr.department', 'Department Owner',domain="[('company_id','=',company_id)]")
    sea_office_id = fields.Many2one('sea.office', 'Location')
    asset_transfer_line=fields.One2many('asset.transfer.line','asset_id',string="Asset Transfers",domain=lambda self:[('id','in',
                                                                                                                      self.env['asset.transfer.line'].sudo(

                                                                                                                      ).search([('asset_transfer_id.active','=',
                                                                                                                                 True),('asset_id','=',self.id),
                                                                                                                                ('state','=','validated')]).ids)])
    asset_adjustment_lines=fields.One2many('account.asset.adjustment','asset_id',string='Asset Adjustment')
    asset_repair_lines=fields.One2many('asset.repair.lines','asset_id',string='Asset Adjustment',domain=lambda self:[('id','in',
                                                                                                                      self.env['asset.repair.lines'].sudo(

                                                                                                                      ).search([('asset_id','=',self.id),
                                                                                                                                ('state','=','done')]).ids)])
    asset_inventory_lines = fields.One2many('asset.inventory.line', 'asset_id', string='Asset Inventory', domain=lambda self: [('id', 'in',
                                                                                                                                self.env[
                                                                                                                                    'asset.inventory.line'].sudo(

                                                                                                                                ).search(
                                                                                                                                    [(
                                                                                                                                        'asset_inventory_id.active','=',True),
                                                                                                                                     ('state','=',
                                                                                                                                        'validated'),
                                                                                                                                     ('asset_id',
                                                                                                                                                 '=',
                                                                                                                                       self.id)]).ids)])
    vendor_name = fields.Char(string='Vendor Name')
    document_ref=fields.Char(string='Document Ref')
    company_using=fields.Many2one('res.company',string='Company Using')
    @api.depends('company_id')
    def compute_is_seagroup(self):
        self.is_seagroup = False
        if self.env.user.company_id.id==1:
            self.is_seagroup=True
        for rec in self:
            rec.current_company_for_filter='none'
            if rec.company_using:
                if rec.company_using.id==self.env.user.company_id.id :
                    rec.current_company_for_filter='using'
            if rec.company_id:
                if rec.company_id.id==self.env.user.company_id.id :
                    if rec.current_company_for_filter == 'using':
                        rec.current_company_for_filter='all'
                    else:
                        rec.current_company_for_filter = 'owner'

    is_seagroup=fields.Boolean(string='Company',compute='compute_is_seagroup')

    @api.multi
    def write(self,vals):
        if 'asset_user_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('asset_user_temporary'))])
            if temporary:
                vals.update({'asset_user':temporary.employee_id.id})
        if 'asset_management_dept_staff_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('asset_management_dept_staff_temporary'))])
            if temporary:
                vals.update({'asset_management_dept_staff':temporary.employee_id.id})
        if 'procurement_staff_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('procurement_staff_temporary'))])
            if temporary:
                vals.update({'procurement_staff':temporary.employee_id.id})
        return super(AccountAssetAsset, self).write(vals)

    @api.model
    def create(self, vals):
        if 'asset_user_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('asset_user_temporary'))])
            if temporary:
                vals.update({'asset_user':temporary.employee_id.id})
        if 'asset_management_dept_staff_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('asset_management_dept_staff_temporary'))])
            if temporary:
                vals.update({'asset_management_dept_staff':temporary.employee_id.id})
        if 'procurement_staff_temporary' in vals:
            temporary=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('procurement_staff_temporary'))])
            if temporary:
                vals.update({'procurement_staff':temporary.employee_id.id})
        vals.update({'company_using':self.env.user.company_id.id})
        if 'dept_owner' in vals:
            vals.update({'management_dept':vals.get('dept_owner')})
        return super(AccountAssetAsset, self).create(vals)

    def asset_adjustment(self):
        self.ensure_one()
        return {
            'name': 'Phiếu Điều Chỉnh',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.asset.adjustment',
            'view_id': self.env.ref('sea_asset_base.account_asset_adjustment_form').id,
            'type': 'ir.actions.act_window',
            'res_id':False,
            'context': {
                'default_asset_id': self.id,
                'asset_id': self.id,
            },
            'target': 'new',
        }
    def set_pending(self):
        self.write({'state':'pending'})
    def set_liquidation(self):
        self.write({'state':'liquidation'})
    asset_images=fields.One2many('account.asset.image','account_asset_id',string="Asset Images")
    kanban_view = fields.Many2many('account.asset.image', compute='_compute_kanban_view')

    @api.depends('asset_images')
    def _compute_kanban_view(self):
        self.kanban_view = self.asset_images

class AssetAdjustment(models.Model):

    _name = 'account.asset.adjustment'
    _description = 'Asset Adjustment'

    name= fields.Char(string='Name',default='')
    adjustment_code=fields.Char(string='Code')
    increase_quantity=fields.Float(string='Increase Quantity',default=1,require=True)
    date_adjustment=fields.Datetime(string='Adjustment Date',default=lambda self: fields.Datetime.now())
    description=fields.Text(string='Description')
    asset_id=fields.Many2one('account.asset.asset')
    active = fields.Boolean(string='active',default=True)
    vendor = fields.Many2one('res.partner',string='Vendor', domain="[('supplier','=',True),('parent_id','=',False)]")
    vendor_name =fields.Char(string='Vendor Name')

    document_ref=fields.Char(string='Document Ref')
    @api.multi
    def save_method(self):
        # Your save logic here
        self.close()

    @api.model
    def create(self, vals):

        if 'asset_id' in self:
            increase_quantity=float(vals.get('increase_quantity'))
            asset=self.env['account.asset.asset'].sudo().search([('id','=',vals.get('asset_id'))])
            if asset:
                increase_quantity+=asset.quantity
                asset.write({'quantity':increase_quantity})

        return super(AssetAdjustment,self).create(vals)
class AccountAssetAssetAttachment(models.Model):
    _name = "account.asset.image"
    _description = "Account Asset Images"

    account_asset_id=fields.Many2one('account.asset.asset')
    asset_temporary_id=fields.Many2one('asset.inventory.asset.temporary')
    asset_image = fields.Binary(string='Image',attachement=True,preview=True)
    asset_filename = fields.Char(string='Images Note')
    active=fields.Boolean(default=True)
    @api.multi
    def unlink(self):
        return super(AccountAssetAssetAttachment, self).unlink()

    @api.multi
    def write(self):
        return super(AccountAssetAssetAttachment, self).write()