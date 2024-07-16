# -*- coding: utf-8 -*-

from . import models

# def post_init_hook(cr, registry):
#     """set the contact_code default. """
#     cr.execute("UPDATE res_partner "
#                "SET contact_code = "
#                "CASE "
#                "WHEN is_employee THEN sea_business_code"
#                "WHEN is_company THEN vat "
#                "ELSE phone END;")
#     print("update data res_partner")
