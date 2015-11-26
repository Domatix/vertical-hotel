# -*- encoding: utf-8 -*-

{
    "name" : "Hotel Housekeeping Management",
    "version" : "1.0",
    "author" : ["Domatix",
                "Serpent Consulting Services Pvt. Ltd.",
                "OpenERP SA" ],
    "category" : "Generic Modules/Hotel Housekeeping",
    "depends" : ["hotel"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    "security/ir.model.access.csv",
                    "views/hotel_housekeeping_view.xml",
                    "data/hotel_housekeeping_workflow.xml",
                    #"wizard/hotel_housekeeping_wizard.xml"
    ],
    "active": False,
    'installable': True
}