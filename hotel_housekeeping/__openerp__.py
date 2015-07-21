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
    "demo_xml" : ["hotel_housekeeping_data.xml",
    ],
    "update_xml" : [
                    #"data/hotel_housekeeping_data.xml",
                    "views/hotel_housekeeping_view.xml",
                    "data/hotel_housekeeping_workflow.xml",
                    "report/hotel_housekeeping_report.xml",
                    "wizard/hotel_housekeeping_wizard.xml",
                    "security/ir.model.access.csv"
    ],
    "active": False,
    'installable': True
}