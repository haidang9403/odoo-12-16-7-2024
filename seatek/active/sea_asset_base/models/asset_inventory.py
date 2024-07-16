from odoo import models, fields,api
from odoo import http, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import json
from odoo.http import request, Response
class DonViDuocKiemKe(models.Model):
    _name = 'asset.inventoried.department'
    _description = 'Inventoried Department'

    employee_id_temp = fields.Many2one('hr.employee.temporary', string='Employee',domain="[('department_id','=',department)]")

    @api.onchange('employee_id_temp')
    @api.model
    def onchange_asset_id(self):
        if self.employee_id_temp.employee_id:
            employee=self.env['hr.employee.multi.company'].sudo().search([('id','=',self.employee_id_temp.employee_id.id)])
            if employee:
                self.job_id=employee.sudo().job_id.id

    employee_id = fields.Many2one('hr.employee.multi.company', string='Employee.')
    company_id = fields.Many2one('res.company', string='Company',related='asset_inventory_id.company_id')
    department = fields.Many2one('hr.department', string='Department',domain="[('company_id','=',company_id)]")
    job_id =fields.Many2one('hr.job',related='employee_id.job_id')
    asset_inventory_id =fields.Many2one('asset.inventory')
    active = fields.Boolean(string='Active',default=True)
    @api.multi
    def write(self, vals):
        if 'employee_id_temp' in vals:
            temp=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('employee_id_temp'))])
            if temp:
                vals.update({'employee_id':temp.employee_id.id})
        return super(DonViDuocKiemKe, self).write(vals)
    @api.model
    def create(self, vals):
        if 'employee_id_temp' in vals:
            temp=self.env['hr.employee.temporary'].sudo().search([('id','=',vals.get('employee_id_temp'))])
            if temp:
                vals.update({'employee_id':temp.employee_id.id})
        return super(DonViDuocKiemKe, self).create(vals)
class InventoryCommitteePosition(models.Model):
    _name = 'asset.committee.position'
    _description = 'Inventory Committee Position'

    name=fields.Char(string='Name')
    active = fields.Boolean(string='Active',default=True)


class InventoryCommittee(models.Model):
    _name='asset.inventory.committee'
    _description = 'Asset Inventory Committee'

    name=fields.Char(string='Name',default='Committee')
    employee_id_temp=fields.Many2one('hr.employee.temporary',string='Employee',domain="[('department_id','=',235)]")
    employee_id=fields.Many2one('hr.employee.multi.company',string='Employee.')
    company_id=fields.Many2one('res.company',string='Company',related='employee_id_temp.company_id')
    position=fields.Many2one('asset.committee.position')
    asset_inventory_id =fields.Many2one('asset.inventory')
    active = fields.Boolean(string='Active',default=True)

    @api.multi
    def write(self, vals):
        if 'employee_id_temp' in vals:
            temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('employee_id_temp'))])
            if temp:
                vals.update({'employee_id': temp.employee_id.id})
        return super(InventoryCommittee, self).write(vals)

    @api.model
    def create(self, vals):
        if 'employee_id_temp' in vals:
            temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('employee_id_temp'))])
            if temp:
                vals.update({'employee_id': temp.employee_id.id})
        return super(InventoryCommittee, self).create(vals)
class AssetInventoryLines(models.Model):
    _name = 'asset.inventory.line'
    _description = 'Asset Inventory Line'
    _order = 'write_date desc'

    asset_id=fields.Many2one('account.asset.asset',string='Asset',domain=lambda self: [('company_using','=',self.env.user.company_id.id),('state','=',
                                                                                                                                            'open')]
                             )

    @api.onchange('asset_id')
    @api.model
    def onchange_asset_id(self):
        if self.asset_id.asset_user_temporary:
            self.asset_user_temporary = self.asset_id.asset_user_temporary.id
        if self.asset_id.asset_uom:
            self.asset_uom = self.asset_id.asset_uom.id
        self.quantity_so_sach = self.asset_id.quantity
        self.quantity_chenh_lech = self.asset_id.quantity -self.quantity_thuc_te
        self.latest_inventory_status = self.asset_id.latest_inventory_status

    @api.onchange('quantity_thuc_te')
    def onchange_quantity_thuc_te(self):
        if self.quantity_thuc_te<0:
            self.quantity_thuc_te = 0
        self.quantity_chenh_lech=self.quantity_so_sach-self.quantity_thuc_te

    asset_code = fields.Char(string='Reference', size=32,related='asset_id.code')
    asset_uom = fields.Many2one('uom.uom', 'Unit of Measure',related='asset_id.asset_uom')

    quantity_so_sach=fields.Float('Số Lượng Sổ Sách')
    quantity_thuc_te=fields.Float('Số Lượng Thực Tế')
    quantity_chenh_lech=fields.Float('Số Lượng Chênh Lệch')
    status=fields.Selection([('dang_su_dung','Đang Sử Dụng'),('hu_hong','Hư Hỏng')],default='dang_su_dung', string="Status")
    da_dan_tem=fields.Boolean(string='Đã dán tem',default=True)

    asset_user_temporary=fields.Many2one('hr.employee.temporary',string ='Asset User')
    asset_user=fields.Many2one('hr.employee.multi.company',string ='Asset User.')
    asset_inventory_id = fields.Many2one('asset.inventory')
    note=fields.Char(string='Ghi chú')

    de_xuat_xu_ly=fields.Text(string='Đề xuất xử lý')
    giai_trinh=fields.Text(string='Giải trình của đơn vị')
    active=fields.Boolean(string='Active',default=True)
    latest_inventory_status = fields.Selection([
        ('good', 'Good'),
        ('damaged_waiting_for_repair', 'Damaged waiting for repair'),
        ('damaged_waiting_for_liquidation', 'Damaged waiting for liquidation'),
        ('self_destruct', 'Self destruct')],
        'Latest Inventory Status', default='good')
    validated_date=fields.Datetime(string='Validated Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('process', 'Process'),
        ('validated', 'Validated'),
        ('cancel', 'Cancel')], string='Status', default='draft', index=True)
    @api.multi
    def write(self, vals):
        if 'asset_user_temporary' in vals:
            temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('asset_user_temporary'))])
            if temp:
                vals.update({'asset_user': temp.employee_id.id})

        if 'state' in vals:
            if vals.get('state')!='validated':
                vals.update({'quantity_so_sach':self.asset_id.quantity})
        else:
            vals.update({'quantity_so_sach': self.asset_id.quantity})
        if 'quantity_thuc_te' in vals:
            quantity_chenh_lech=float(self.quantity_so_sach)-float(vals.get('quantity_thuc_te'))
            vals.update({'quantity_chenh_lech':quantity_chenh_lech})
        return super(AssetInventoryLines, self).write(vals)

    @api.model
    def create(self, vals):
        if 'asset_user_temporary' in vals:
            temp = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('asset_user_temporary'))])
            if temp:
                vals.update({'asset_user': temp.employee_id.id})

        asset = self.env['account.asset.asset'].sudo().search([('id', '=', vals.get('asset_id'))])
        vals.update({'quantity_so_sach': asset.quantity})
        quantity_so_sach=0
        if 'quantity_so_sach' in vals:
            quantity_so_sach=vals.get('quantity_so_sach')
        quantity_thuc_te=0
        if 'quantity_thuc_te' in vals:
            quantity_thuc_te=vals.get('quantity_thuc_te')
        vals.update({'quantity_chenh_lech': quantity_so_sach-quantity_thuc_te})
        return super(AssetInventoryLines, self).create(vals)


class AssetInventory(models.Model):
    _name='asset.inventory'
    _description = 'Inventory Of Asset'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']



    name=fields.Char(string='Name')
    code=fields.Char(string='Code')
    company_id=fields.Many2one('res.company',string='Company',default=lambda self:self.env.user.company_id.id)
    department=fields.Many2many('hr.department','asset_inventory_department_rel','asset_inventory_id','department_id',string='Department',domain="[('company_id',"
                                                                                                                                            "'=',company_id)]")
    sea_office_id = fields.Many2many('sea.office','asset_inventory_sea_office_rel','asset_inventory_id','sea_office_id',string= 'Location')
    start_time=fields.Datetime(string='Start time')
    end_time=fields.Datetime(string='End time')
    asset_inventory_lines=fields.One2many('asset.inventory.line','asset_inventory_id',string='Asset List')
    member_of_inventory=fields.One2many('asset.inventory.committee','asset_inventory_id',string='Inventory Committee')
    inventoried_department=fields.One2many('asset.inventoried.department','asset_inventory_id',string ='Employee')
    active=fields.Boolean(string='Active',default=True)
    note=fields.Text(string="Note")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('process', 'Process'),
        ('validated', 'Validated'),
        ('cancel', 'Cancel')], string='Status', default='draft', index=True)

    draft_state=fields.Boolean(string='Draft',default=False)
    process_state=fields.Boolean(string='Running',default=True)
    pending_state=fields.Boolean(string='Pending',default=False)
    liquidation_state=fields.Boolean(string='Liquidation',default=False)
    asset_temporary=fields.One2many('asset.inventory.asset.temporary','asset_inventory_id',string='Asset Temporary')
    def set_state_process(self):
        self.write({'state': 'process'})
    def set_state_draft(self):
        self.write({'state': 'draft'})
    def set_state_validated(self):
        self.write({'state': 'validated'})
        for line in self.asset_inventory_lines:
            line.write({'validated_date': fields.Datetime.now(), 'state': 'validated'})
            asset=self.env['account.asset.asset'].sudo().search([('id','=',line.asset_id.id)])
            if asset:
                if line.quantity_thuc_te:
                    asset.write({'quantity':line.quantity_thuc_te})
                if line.asset_user_temporary:
                    asset.write({'asset_user_temporary': line.asset_user_temporary.id})
                asset.write({'latest_inventory_status': line.latest_inventory_status})


    def toggle_active(self):
        self.write({'active':False})
    def export_xls(self):
        data = {
            'name':self.name,
            'company_id': self.company_id.ids,
        }
        return self.env.ref('sea_asset_base.action_export_asset_inventory_pkk').report_action(self, data=data)

    @api.model
    def create(self,vals):
        return super(AssetInventory, self).create(vals)
    @api.multi
    def start_asset_inventory(self):
        domain=[]
        if self.department:
            domain.append("|")
            domain.append(('dept_owner','=',self.department.ids))
            domain.append(('management_dept','=',self.department.ids))
        else:
            domain.append("|")
            domain.append(('company_id', '=', self.env.user.company_id.id))
            domain.append(('company_using', '=', self.env.user.company_id.id))
        if self.sea_office_id:
            domain.append(('sea_office_id', '=', self.sea_office_id.ids))
        count_state=-1
        if self.draft_state:
            count_state+=1
        if self.process_state:
            count_state+=1
        if self.pending_state:
            count_state+=1
        if self.liquidation_state:
            count_state += 1
        for i  in range(count_state):
            domain.append(('|'))
        if self.draft_state:
            domain.append(('state', '=', 'draft'))
        if self.process_state:
            domain.append(('state', '=', 'open'))
        if self.pending_state:
            domain.append(('state', '=', 'pending'))
        if self.liquidation_state:
            domain.append(('state', '=', 'liquidation'))
        assets=self.env['account.asset.asset'].sudo().search(domain)
        values=[]
        self.asset_inventory_lines.unlink()
        for asset in assets:
            value=self.asset_inventory_lines.new({'asset_id':asset.id,'quantity_so_sach':asset.quantity,'asset_user_temporary':asset.asset_user_temporary.id})
            values.append(value.id)
        if len(values)>0:
            self.asset_inventory_lines=values[0]
            self.asset_inventory_lines=values
        else:
            self.asset_inventory_lines=None

    @api.multi
    def write(self, vals):

        try:
            return super(AssetInventory,self).write(vals)
        except Exception as e:
            return False

class AssetInventoryAssetTemporary(models.Model):
    _name = 'asset.inventory.asset.temporary'
    _description = 'Asset Not In List'

    name=fields.Char(string='Name')
    code=fields.Char(string='Code')
    description=fields.Char(string='Description')
    asset_images = fields.One2many('account.asset.image', 'asset_temporary_id', string="Asset Images")
    asset_inventory_id=fields.Many2one('asset.inventory')



