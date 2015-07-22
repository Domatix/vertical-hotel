# -*- encoding: utf-8 -*-

from openerp import api,models
import time

class activity_report(models.Model):
    
    '''def __init__(self, name):
        super(activity_report, self).__init__(name)
        
        self.localcontext.update( {
            'time': time,
            'get_activity_detail': self.get_activity_detail,
            'get_room_no': self.get_room_no,
            
        })'''
                
    
    @api.model
    def get_activity_detail(self,date_start,date_end,room_no):
        self._cr.execute("select hh.current_date,ppt.name as Activity,pt.name as Room,rs.login,hha.clean_start_time,hha.clean_end_time,(hha.clean_end_time-hha.clean_start_time) as duration  from hotel_housekeeping as hh " \
                        "inner join hotel_housekeeping_activities as hha on hha.a_list=hh.id " \
                        "inner join hotel_activity as ha on ha.id=hha.activity_name " \
                        "inner join hotel_room as hor on hor.product_id=hh.room_no " \
                        "inner join product_product as pp on pp.product_tmpl_id=hh.room_no " \
                        "inner join product_template as pt on pt.id=pp.product_tmpl_id " \
                        "inner join product_product as ppr on ppr.product_tmpl_id=ha.h_id " \
                        "inner join product_template as ppt on ppt.id=ppr.product_tmpl_id " \
                        "inner join res_users as rs on rs.id=hha.housekeeper " \
                        "where hh.current_date >= %s and hh.current_date <= %s  and hor.id= cast(%s as integer) " \
                        ,(date_start,date_end,str(room_no))
                        )
                     
        res=self._cr.dictfetchall()
        print res
        return res
   
    
    @api.model
    def get_room_no(self, room_no):
        return self.env['hotel.room'].browse(self._cr, self._uid, room_no).name
    
 