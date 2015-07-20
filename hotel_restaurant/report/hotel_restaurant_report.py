# -*- encoding: utf-8 -*-


import time
from . import report_sxw
import datetime
from openerp import pooler

class hotel_restaurant_report(report_sxw.rml_parse):
    def __init__(self, name):
        super(hotel_restaurant_report, self).__init__(name)
        self.localcontext.update( {
            'time': time,
            'get_res_data':self.get_res_data,
        })
        self.context=context
       
    def get_res_data(self,date_start,date_end):
        tids = self.env['hotel.restaurant.reservation'].search([('start_date', '>=', date_start),('end_date', '<=', date_end)])
        res = self.env['hotel.restaurant.reservation'].browse(tids)
        return res

report_sxw.report_sxw('report.hotel.kot', 'hotel.restaurant.order', 'addons/hotel_restaurant/report/kot.rml',parser=hotel_restaurant_report)        
report_sxw.report_sxw('report.hotel.bill', 'hotel.restaurant.order', 'addons/hotel_restaurant/report/bill.rml',parser=hotel_restaurant_report)
report_sxw.report_sxw('report.hotel.table.res', 'hotel.restaurant.reservation', 'addons/hotel_restaurant/report/res_table.rml',parser=hotel_restaurant_report)

     