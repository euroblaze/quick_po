# -*- coding: utf-8 -*-
from odoo import fields, models, api


class POReport(models.TransientModel):
	_name = "po.report"
	_description = "po.report"

	quick_po_report = fields.Binary('PO Report', translate=True)
