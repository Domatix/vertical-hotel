# -*- encoding: utf-8 -*-

from openerp import fields,models,api,netsvc
import time

class product_category(models.Model):
    _inherit = "product.category"
    
    isactivitytype = fields.Boolean(string='Is Activity Type',
                                    default=lambda *a: True)
    

class hotel_housekeeping_activity_type(models.Model):
    _name = 'hotel.housekeeping.activity.type'
    _description = 'Activity Type'
    
    activity_id = fields.Many2one('product.category',
                                  string='category',
                                  required=True,
                                  ondelete='cascade',
                                  delegate=True)
    

class product_product(models.Model):
    _inherit = "product.product"
    
    isact = fields.Boolean(string='Is Activity')


class hotel_activity(models.Model):
    _name = 'hotel.activity'
    _description = 'Housekeeping Activity'

    h_id = fields.Many2one('product.product',
                           string='Product',
                           delegate=True)


class hotel_housekeeping(models.Model):
    _name = "hotel.housekeeping"
    _description = "Reservation"
    
    current_date = fields.Date(string="Today's Date",
                               required=True,
                               default=lambda *a: time.strftime('%Y-%m-%d'))
    clean_type = fields.Selection([('daily','Daily'),
                                   ('checkin','Check-in'),
                                   ('checkout','Check-out')],
                                  string='Clean Type',
                                  required=True)
    room_no = fields.Many2one('hotel.room',
                              string='Room No',
                              required=True)
    activity_lines = fields.One2many('hotel.housekeeping.activities',
                                     'a_list',
                                     string='Activities')
    inspector = fields.Many2one('res.users',
                                string='Inspector')
    inspect_date_time = fields.Datetime(string='Inspect Date Time')
    quality = fields.Selection([('bad','Bad'),
                                ('good','Good'),
                                ('ok','Ok')],
                               string='Quality')
    state =  fields.Selection([('dirty','Dirty'),
                               ('clean','Clean'),
                               ('inspect','Inspect'),
                               ('done','Done'),
                               ('cancel', 'Cancelled')],
                               string='state', 
                               select=True, 
                               required=True, 
                               readonly=True,
                               default= lambda *a: 'dirty')

    
    @api.multi
    def action_set_to_dirty(self):
        self.write({'state': 'dirty'})
        wf_service = netsvc.LocalService('workflow')
        for id in self.ids:
            wf_service.trg_create(self._uid, self._name, self.id, self._cr)
        return True
    
    
    @api.multi
    def room_cancel(self):
        self.write({'state':'cancel'})
        return True
    
    
    @api.multi
    def room_done(self):
        self.write({'state':'done'})
        return True
    
    
    @api.multi
    def room_inspect(self):
        self.write({'state':'inspect'})
        return True
    
    
    @api.multi
    def room_clean(self):
        self.write({'state':'clean'})
        return True
     

class hotel_housekeeping_activities(models.Model):
    _name = "hotel.housekeeping.activities"
    _description = "Housekeeping Activities"
    
    a_list = fields.Many2one('hotel.housekeeping',
                             string='Reservation')
    activity_name = fields.Many2one('hotel.activity',
                                    string='Housekeeping Activity')
    housekeeper = fields.Many2one('res.users',
                                  string='Housekeeper',
                                  required=True)
    clean_start_time = fields.Datetime(string='Clean Start Time',
                                       required=True)
    clean_end_time = fields.Datetime(string='Clean End Time',
                                     required=True)
    dirty = fields.Boolean(string='Dirty')
    clean = fields.Boolean(string='Clean')
    room_id = fields.Many2one('hotel.room',
                              string='Room No')


