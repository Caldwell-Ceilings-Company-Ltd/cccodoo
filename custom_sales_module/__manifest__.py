{
    'name': 'Custom Sales Module',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom modifications for sales and product modules',
    'depends': ['sale', 'product'],
    'data': [
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
