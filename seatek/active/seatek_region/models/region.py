from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Region(models.Model):
    _name = 'region'
    _description = "Vietnam's Region"

    name = fields.Char(string="Name", required=True)
    state_region_ids = fields.One2many('state.region', 'region_id', string='Region')
    country_state_region_ids = fields.One2many('res.country.state', 'region_id', string='Region')

    @api.model
    def _create(self, data_list):
        c = super(Region, self)._create(data_list)
        for data in data_list:
            if data.get('stored') is not None:
                if data['stored'].get('state_region_ids') is not None:
                    list_region = data['stored'].get('state_region_ids')
                    for region in list_region:
                        if region[2]:
                            id_state = region[2]['country_state_id']
                            if data.get('record') is not None:
                                record_id = data['record'].id
                                search_country_state = self.env['res.country.state'].sudo().browse(id_state)
                                search_country_state.sudo().write({'region_id': record_id})
        return c

    @api.model
    def _write(self, vals):
        # xoa cac region khoi thanh pho
        if vals.get('state_region_ids') is not None:
            list_region = vals.get('state_region_ids')
            for region in list_region:
                if isinstance(region[1], str) == False and region[2]:
                    search_state_region = self.env['state.region'].sudo().browse(region[1])
                    search_state_region.country_state_id.sudo().write({'region_id': None})
        w = super(Region, self)._write(vals)

        # ghi cac region vao thanh pho moi
        if vals.get('state_region_ids') is not None:
            list_region = vals.get('state_region_ids')
            for region in list_region:
                if region[2]:
                    id_state = region[2]['country_state_id']
                    record_id = self.id
                    search_country_state = self.env['res.country.state'].sudo().browse(id_state)
                    search_country_state.sudo().write({'region_id': record_id})
        return w

    @api.multi
    def unlink(self):
        for r in self:
            for i in r.state_region_ids:
                # xoa region_id trong res.country.state
                i.country_state_id.sudo().write({'region_id': None})

        return super(Region, self).unlink()

    @api.onchange('state_region_ids')
    def _onchange_state_region_ids(self):
        country_ids = []
        for i in self.state_region_ids:
            if i.country_state_id.id in country_ids:
                raise ValidationError(_('%s has been added above') % i.country_state_id.name)
            else:
                country_ids.append(i.country_state_id.id)


class State(models.Model):
    _name = 'state.region'
    _description = "State of region"

    region_id = fields.Many2one('region', string='State of Region', ondelete='cascade')
    country_state_id = fields.Many2one('res.country.state', string="State")

    @api.multi
    def unlink(self):
        self.country_state_id.sudo().write({'region_id': None})
        return super(State, self).unlink()


class CountryState(models.Model):
    _inherit = 'res.country.state'

    region_id = fields.Many2one('region', string='Region', ondelete='cascade')


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    region_name = fields.Char(related='state_id.region_id.name', string="Region", store=True)
    district_id=fields.Many2one('res.district',string='District', domain="[('city_id','=',state_id)]")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    region_name = fields.Char(related='partner_id.region_name', string='Region', store=True)


class SaleReport(models.Model):
    _inherit = 'sale.report'

    region_name = fields.Char(string='Region', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['region_name'] = ", s.region_name as region_name"
        groupby += ', s.region_name'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
