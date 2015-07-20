# -*- encoding: utf-8 -*-


from openerp import fields,api,models
#from openerp import models
import time
from mx import DateTime
from datetime import datetime
from openerp import pooler
from openerp.tools import config
from openerp import netsvc

class wizard_hotel_restaurant(models.Model):
    _name = 'wizard.hotel.restaurant'
    
    date_start = fields.Datetime('Start Date',
                                 required=True)
    date_end = fields.Datetime('End Date',
                               required=True)        
    
    @api.multi
    def print_report(self):
        datas = {
             'ids': self.ids,
             'model': 'hotel.restaurant.reservation',
             'form': self.read(self.ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hotel.table.res',
            'datas': datas,
        }

