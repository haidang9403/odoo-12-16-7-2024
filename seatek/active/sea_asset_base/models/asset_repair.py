from odoo import models, fields,api


class AssetRepair(models.Model):
    _name = "asset.repair"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Asset Repair'

    name=fields.Char(string='Name',default='Phiếu sửa chữa')
    company_id=fields.Many2one('res.company',string='Company', default=lambda self:self.env.user.company_id.id)
    repair_date=fields.Datetime(string='Date')
    employee_temporary=fields.Many2one('hr.employee.temporary',string='Employee #',domain="[('company_id','=',company_id)]")
    employee_id=fields.Many2one('hr.employee.multi.company',string='Employee')
    asset_repair_lines=fields.One2many('asset.repair.lines','asset_repair_id',string='Asset repair lines')
    state=fields.Selection([('draft','Draft'),('process','Process'),('done','Done')],default='draft')

    active=fields.Boolean(string='Active',default=True)
    def set_to_done(self):
        values={'state':'done'}
        for line in self.asset_repair_lines:
            if line.repair_date_start and line.asset_id:
                if line.asset_id.repair_date:
                    if  line.repair_date_start>line.asset_id.repair_date:
                        line.asset_id.write({'repair_date':line.repair_date_start})
                else:
                    line.asset_id.write({'repair_date': line.repair_date_start})



        self.write({'state':'done'})
    def set_to_process(self):
        self.write({'state':'process'})
        # for asset_repair_line in self.asset_repair_lines:
        #     asset=self.env['account.asset.asset'].sudo().search([('id','=',asset_repair_line.asset_id.id)])
        #     if asset:
        #         if asset_repair_line.repair_date_end:
        #             asset.write({'repair_date', '=', asset_repair_line.repair_date_end})

    def set_back_to_draft(self):
        self.write({'state':'draft'})
    def export_xls(self):
        data = {
            'name':self.name,
            'company_id': self.company_id.ids,
        }
        return self.env.ref('sea_asset_base.action_export_asset_repair').report_action(self, data=data)

    @api.multi
    def write(self, vals):
        if 'employee_temporary' in vals:
            temporary = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('employee_temporary'))])
            if temporary:
                vals.update({'employee_id': temporary.employee_id.id})
        return super(AssetRepair, self).write(vals)
    @api.model
    def create(self, vals):
        if 'employee_temporary' in vals:
            temporary = self.env['hr.employee.temporary'].sudo().search([('id', '=', vals.get('employee_temporary'))])
            if temporary:
                vals.update({'employee_id': temporary.employee_id.id})
        return super(AssetRepair, self).create(vals)
class AssetRepairLines(models.Model):
    _name = "asset.repair.lines"
    _description = 'Asset Repair'

    asset_repair_id=fields.Many2one('asset.repair')
    asset_id=fields.Many2one('account.asset.asset',string='Asset',domain="[('company_id','=',company_id)]")
    company_id=fields.Many2one('res.company',string='Company',related='asset_repair_id.company_id')
    asset_code=fields.Char(string='Code',related='asset_id.code')
    repair_date_start=fields.Datetime(string='Start date')
    repair_date_end=fields.Datetime(string='End date')
    repair_party=fields.Char(string='Repair party')
    accident_place=fields.Char(string='Accident place')
    description=fields.Text(string='Description')
    uom_id = fields.Many2one('uom.uom', 'Unit', related='asset_id.asset_uom')
    alt_unit = fields.Char('Alt Unit',related='asset_id.alt_unit')
    active=fields.Boolean(string='Active',default=True)
    state = fields.Selection([('draft', 'Draft'), ('process', 'Process'), ('done', 'Done')], default='draft',related='asset_repair_id.state')
    @api.onchange('asset_id')
    def onchange_asset_id(self):
        if self.asset_id:
            self.quantity=self.asset_id.quantity

    @api.onchange('quantity')
    def onchange_quantity(self):
        if self.asset_id:
            if self.quantity> self.asset_id.quantity:
                self.quantity=self.asset_id.quantity

    quantity =  fields.Float(string="Quantity",default=lambda self: self.asset_id.quantity)
