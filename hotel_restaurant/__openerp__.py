# -*- encoding: utf-8 -*-

{
    "name" : "Hotel Restaurant Management",
    "version" : "1.0",
    "author" : ["Domatix",
                "Serpent Consulting Services Pvt. Ltd.",
                "OpenERP SA" ],
    "category" : "Generic Modules/Hotel Restaurant",
    "depends" : ["base","hotel"],
    "init_xml" : [],
    "demo_xml" : ["hotel_restaurant_data.xml",
    ],
    "update_xml" : [
                    #"data/hotel_restaurant_data.xml",
                    "data/hotel_restaurant_workflow.xml",
                    "views/hotel_restaurant_view.xml",
                    "report/hotel_restaurant_report.xml",
                    "wizard/hotel_restaurant_wizard.xml",
                    "views/hotel_restaurant_sequence.xml",
                    "security/ir.model.access.csv"
                    
    ],
    "active": False,
    'installable': True
}