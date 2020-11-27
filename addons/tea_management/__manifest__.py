# -*- coding: utf-8 -*-
{
    'name': "Tea Management",

    'summary': """
        Manage your tea estate wit AI powered""",

    'description': """
        Software is based on odoo and this module is designed by Sizil Enterprise, This module can manage all yor estate activities digitally.
    """,

    'author': "Sizil Enterprise",
    'website': "http://www.sizil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dryer_mouth_data.xml',
        'views/packing_data.xml',
        'views/price_table.xml',
        'views/price_incentive.xml',
        'views/serial_and_lot.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable':True,
    'application':True,
    'auto_install':False
}
