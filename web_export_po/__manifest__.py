# -*- coding: utf-8 -*-
{
	'name': 'Export Purchase orders',
	'category': 'Purchase',
	'summary': 'To export multiple purchase order',
	'description': """
       To export multiple purchase order
    """,
	'version': '15.0.1.0.0',
	'author': 'Simplify-ERP™',
	'website': 'https://simplify-erp.de',
	'license': 'OPL-1',
	'depends': [
		'purchase',
		'purchase_stock',
	],
	'data': [
		'security/ir.model.access.csv',
		'views/purchase_order_views.xml',
		'views/product_supplierinfo_views.xml',
	],
	'installable': True,
	'application': False,
}
