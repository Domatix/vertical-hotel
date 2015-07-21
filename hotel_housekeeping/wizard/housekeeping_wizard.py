# -*- encoding: utf-8 -*-

from openerp import models,fields,api

class hotel_housekeeping_wizard(models.Model):
    _name = 'hotel.housekeeping.wizard'
    
    date_start = fields.Date('Start Date',required=True)
    date_end = fields.Date('End Date',required=True)
    room_no = fields.Many2one('hotel.room', 'Room No.', required=True)

    @api.multi
    def print_report(self):
        datas = {
             'ids': self.ids,
             'model': 'hotel.housekeeping',
             'form': self.read(self.ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'activity.detail',
            'datas': datas,
        }        

