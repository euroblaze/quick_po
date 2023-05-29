# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import io
import base64
from odoo.exceptions import UserError
from odoo.tools import pycompat


class PurchaseOrder(models.Model):
	_inherit = "purchase.order"

	def generate_export_report(self, po_ids):
		"""
		Generate report in CSV file with all the PO selected
		:param po_ids: Selected Purchase Orders
		:return:
		"""
		products = list(set(po_ids.mapped('order_line').filtered(lambda order: not order.article_no or not order.product_id.seller_ids).mapped('product_id.display_name')))
		if products:
			products = '\n'.join(product for product in products)
			raise UserError(_("Following products do not have this supplier set up with an article number.\n%s ", (products)))
		output = io.BytesIO()
		writer = pycompat.csv_writer(output, quoting=1)
		writer.writerow([u"Vendor Article Number", u"Quantity"])
		for line in po_ids.order_line:
			writer.writerow([line.article_no, line.product_uom_qty])
		report_data = base64.b64encode(output.getvalue())
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
			"url": "/web/content?model=po.report&download=true&field=quick_po_report&filename=exported_po_{}.csv&id={}".format(report_id.id, report_id.id),
		}


class PurchaseOrderLine(models.Model):
	_inherit = "purchase.order.line"

	article_no = fields.Char('Article No.', translate=True, compute="_compute_article")

	@api.depends('product_qty', 'product_uom', 'product_id', 'order_id.partner_id')
	def _compute_article(self):
		for line in self:
			article_no = ''
			if line.product_id and line.product_id.seller_ids and line.order_id.partner_id:
				seller_id = line.product_id.seller_ids.filtered(lambda supplier: supplier.product_id.id == line.product_id.id and supplier.name.id == line.order_id.partner_id.id)
				if not seller_id:
					seller_id = line.product_id.seller_ids.filtered(lambda supplier: supplier.product_tmpl_id.id == line.product_id.product_tmpl_id.id and supplier.name.id == line.order_id.partner_id.id)
				if seller_id:
					article_no = seller_id and seller_id.sorted('sequence')[0].article_no
			line.article_no = article_no
