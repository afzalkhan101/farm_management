
{
    'name': "farm_management",
    'summary': "Manage Layer Farm Operations ",
    'description': """ Layer Farm Management Module for Poultry Farms """,
    'author': "Betopia",
    'category': 'Farm Management',
    'version': "18.0",
    'depends': ['base', 'stock', 'sale', 'purchase','mail'],

    'data': [

        'security/ir.model.access.csv',
        'views/flock_views.xml',
        'views/mortality_details_views.xml',
        'views/productiondetails.xml',
        'views/farm_temperature_views.xml',
        'views/medicine_views.xml'

    ],
    
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
