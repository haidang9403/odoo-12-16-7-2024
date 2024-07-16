import datetime
from datetime import timedelta
from odoo import models, fields, api
from PIL import Image
try:
    import qrcode
    import io
except ImportError:
    qrcode = None
import base64
class AssetQRCode(models.TransientModel):
    _name = "asset.qrcode"

    start_date = fields.Datetime(string='Date', default=fields.Datetime.now())
    qrcode = fields.Binary('QRCode',attachment=True)
    assets_for_print=[]
    def export_xlsx(self):
        datas = {}
        domain=[('id','in',self.assets_for_print)]

        assets=self.env['account.asset.asset'].sudo().search(domain)
        temp_assets=[]

        for asset in assets:
            temp_asset={}
            data={}
            # name=''
            # code=''
            # company_id=''
            # if asset.code:
            #     code="\n"+"Code: "+ asset.code
            # if asset.name:
            #     name="Tài sản: "+ str(asset.name)
            # if asset.company_id:
            #     company_id="\n"+"Cty: "+asset.company_id.sudo().short_name
            # qr_code =name+company_id+code
            if asset.code:
                qr_code=asset.code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=40,
                    border=0,
                )
                qr.add_data(qr_code)
                qr.make(fit=True)
                image = qr.make_image(fill_color="white", back_color="black")
                with io.BytesIO() as stream:
                    image.save(stream, format="PNG")
                    qr_code_data = base64.b64encode(stream.getvalue())

                temp_asset.update({'qr_code':qr_code_data})
                name='Tên: '
                if asset.name:
                    name+=asset.name
                description='Mô tả: '
                if asset.description:
                    description+=asset.description
                company='Công ty: '
                if asset.company_id:
                    company+=asset.company_id.sudo().short_name
                code='Mã TS: '
                if asset.code:
                    code+=asset.code
                dept_owner='Phòng Ban: '
                if asset.dept_owner:
                    dept_owner+=asset.dept_owner.sudo().name
                temp_asset.update({'name':name})
                temp_asset.update({'description':description})
                temp_asset.update({'company':company})
                temp_asset.update({'code':code})
                temp_asset.update({'dept_owner':dept_owner})
                temp_asset.update({'asset':asset})
                temp_assets.append(temp_asset)
        if assets:
            datas.update({'asset':temp_assets})
            datas.update({'start_date':self.start_date.strftime("%d/%m/%Y")})
        return self.env.ref('sea_asset_base.action_print_qrcode').report_action(self, data=datas)


    @api.model
    def get_asset(self,records):
        for record in records:
            self.assets_for_print.append(record.id)
        self.export_xlsx()

    @api.model
    def get_datas(self, records):
        self.assets_for_print=[]
        for record in records:
            self.assets_for_print.append(record.id)
        datas = {}
        domain = [('id', 'in', self.assets_for_print)]
        assets = self.env['account.asset.asset'].sudo().search(domain)
        temp_assets = []
        for asset in assets:
            temp_asset = {}
            data = {}
            # name=''
            # code=''
            # company_id=''
            # if asset.code:
            #     code="\n"+"Code: "+ asset.code
            # if asset.name:
            #     name="Tài sản: "+ str(asset.name)
            # if asset.company_id:
            #     company_id="\n"+"Cty: "+asset.company_id.sudo().short_name
            # qr_code =name+company_id+code
            if asset.code:
                qr_code = asset.code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=40,
                    border=0,
                )
                qr.add_data(qr_code)
                qr.make(fit=True)
                image = qr.make_image(fill_color="white", back_color="black")
                with io.BytesIO() as stream:
                    image.save(stream, format="PNG")
                    qr_code_data = base64.b64encode(stream.getvalue())

                temp_asset.update({'qr_code': qr_code_data})
                name = ''
                if asset.name:
                    if len(asset.name) > 60:
                        name = asset.name[:60] + '...'
                    else:
                        name = asset.name
                sea_office='---'
                if asset.sea_office_id:
                    sea_office = asset.sea_office_id.name
                description = ''
                # if asset.description:
                #     description += asset.description
                company = ''
                if asset.company_id:
                    company += asset.company_id.sudo().short_name
                code = ''
                if asset.code:
                    code += asset.code
                dept_owner = ''
                if asset.dept_owner:
                    dept_owner += asset.dept_owner.sudo().name
                temp_asset.update({'name': name})
                temp_asset.update({'sea_office': sea_office})
                temp_asset.update({'description': description})
                temp_asset.update({'company': company})
                temp_asset.update({'code': code})
                temp_asset.update({'dept_owner': dept_owner})
                temp_asset.update({'asset': asset})
                temp_assets.append(temp_asset)
        if assets:
            datas.update({'asset': temp_assets})
            datas.update({'start_date': self.start_date.strftime("%d/%m/%Y")})
        return datas
class ListAssetQRCode(models.TransientModel):
    _name = "list.asset.qrcode"

    name=fields.Char(string="Name")
    asset_code=fields.Char(string="Code")
    sea_office_id=fields.Char(string="Location")
    asset_id=fields.Many2one('account.asset.asset')
    asset_qrcode=fields.Many2one('asset.qrcode')

    @api.onchange('asset_id')
    def asset_id_onchange(self):
        if self.asset_id:
            self.name=self.asset_id.sudo().name
            self.asset_code=self.asset_id.sudo().code
            self.sea_office_id=self.asset_id.sudo().sea_office_id.sudo().name

    @api.model
    def create(self, vals_list):
        return super(ListAssetQRCode,self).create(vals_list)