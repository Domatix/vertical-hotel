# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
from openerp import fields
from openerp import pooler
from openerp import models
from openerp.tools import config
from openerp import api
from openerp import netsvc

import time
from mx import DateTime
import datetime
#from openerp import wizard


class hotel_reservation_wizard(models.TransientModel):
    
    _name = 'hotel.reservation.wizard'
    
    date_start = fields.Datetime('Start Date',
                                 required=True)
    
    date_end = fields.Datetime('End Date',
                               required=True)       
    
    @api.multi
    def report_reservation_detail(self):    
        datas = {
             'ids': self.ids,
             'model': 'hotel.reservation',
             'form': self.read()[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'reservation.detail',
            'datas': datas,
        }        
    
    def report_checkin_detail(self,cr,uid,ids,context=None):    
        datas = {
             'ids': ids,
             'model': 'hotel.reservation',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'checkin.detail',
            'datas': datas,
        }
        
    def report_checkout_detail(self,cr,uid,ids,context=None):    
        datas = {
             'ids': ids,
             'model': 'hotel.reservation',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'checkout.detail',
            'datas': datas,
        }
        
    def report_maxroom_detail(self,cr,uid,ids,context=None):    
        datas = {
             'ids': ids,
             'model': 'hotel.reservation',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'maxroom.detail',
            'datas': datas,
        }

class make_folio_wizard(models.TransientModel):
    
    _name = 'wizard.make.folio'
    
    grouped = fields.Boolean('Group the Folios',
                             default = False)
    
    def makeFolios(self, cr, uid, data, context):
        order_obj = self.pool.get('hotel.reservation')
        newinv = []
        for o in order_obj.browse(cr, uid, context['active_ids'], context):
            for i in o.folio_id:
               newinv.append(i.id)
        return {
            'domain': "[('id','in', ["+','.join(map(str,newinv))+"])]",
            'name': 'Folios',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hotel.folio',
            'view_id': False,
            'type': 'ir.actions.act_window'
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: