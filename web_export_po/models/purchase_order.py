# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.tools.misc import xlwt
import io
import base64
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
	_inherit = "purchase.order"

	def generate_export_report(self, po_ids):
		"""
		Generate report in excel file with all the PO selected
		:param po_ids: Selected Purchase Orders
		:return:
		"""
		products = list(set(po_ids.mapped('order_line').filtered(lambda x: not x.article_no or not x.product_id.seller_ids).mapped('product_id.display_name')))
		if products:
			products = '\n'.join(product for product in products)
			raise UserError(_("Following products do not have this supplier set up with an article number.\n%s ", (products)))

		file_data = io.BytesIO()
		workbook = xlwt.Workbook('report.csv')
		worksheet = workbook.add_sheet('Purchase Orders')
		header_style = xlwt.easyxf('font:height 200,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center,vert center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')
		worksheet.write(0, 0, u' Vendor Article Number', header_style)
		worksheet.col(0).width = int(20 * 500)
		worksheet.write(0, 1, u'Quantity', header_style)
		worksheet.col(1).width = int(20 * 200)
		row = 1
		for line in po_ids.order_line:
			worksheet.write(row, 0, line.article_no)
			worksheet.write(row, 1, line.product_uom_qty)
			row += 1
		workbook.save(file_data)
		file_data.seek(0)
		report_data = base64.b64encode(file_data.read())
		return report_data

	def action_export_orders(self):
		"""
		Let you export the orders
		:return: Downloaded report
		"""
		po_ids = self.env['purchase.order'].search([('id', 'in', self._context.get('active_ids', []))])
		if po_ids and len(po_ids) > 10:
			raise UserError(_('Warning: Limit Exceeded\nPerform operation on 10 or fewer POs at a time to prevent performance issues.'))
		report_data = self.generate_export_report(po_ids)
		report_id = self.env['po.report'].create({'quick_po_report': report_data})
		return {
			"type": "ir.actions.act_url",
			"target": "self",
			"url": "/web/content?model=po.report&download=true&field=quick_po_report&filename=exported_po_{}.xls&id={}".format(report_id.id, report_id.id),
		}


class PurchaseOrderLine(models.Model):
	_inherit = "purchase.order.line"

	article_no = fields.Char('Article No.', translate=True, compute="_compute_article")

	@api.depends('product_qty', 'product_uom', 'product_id', 'order_id.partner_id')
	def _compute_article(self):
		for obj in self:
			article_no = ''
			if obj.product_id and obj.product_id.seller_ids and obj.order_id.partner_id:
				seller_id = obj.product_id.seller_ids.filtered(lambda x: x.product_id.id == obj.product_id.id and x.name.id == obj.order_id.partner_id.id)
				if not seller_id:
					seller_id = obj.product_id.seller_ids.filtered(lambda x: x.product_tmpl_id.id == obj.product_id.product_tmpl_id.id and x.name.id == obj.order_id.partner_id.id)

				if seller_id:
					article_no = seller_id and seller_id.sorted('sequence')[0].article_no
			obj.article_no = article_no
