# -*- encoding: utf-8 -*-

from openerp import fields,api,models
import time
from mx import DateTime
from openerp import netsvc
import datetime
from openerp import pooler
from openerp.tools import config


class product_category(models.Model):
    _inherit = "product.category"
    
    ismenutype = fields.Boolean(string='Is Menu Type')


class product_product(models.Model):
    _inherit = "product.product"

    ismenucard = fields.Boolean(string='Is Room')


class hotel_menucard_type(models.Model):
    _name = 'hotel.menucard.type'
    _description = 'Amenities Type'

    menu_id = fields.Many2one('product.category', 
                              'category', 
                              required=True, 
                              ondelete='cascade',
                              delegate=True)

    _defaults = {
        'ismenutype': lambda * a: 1,

    }

class hotel_menucard(models.Model):
    _name = 'hotel.menucard'
    _description = 'Hotel Menucard'

    product_id = fields.Many2one('product.product', 
                                 string='Product_id',
                                 delegate=True)

    _defaults = {
        'ismenucard': lambda * a: 1,
        }


class hotel_restaurant_tables(models.Model):
    _name = "hotel.restaurant.tables"
    _description = "Includes Hotel Restaurant Table"
    
    name = fields.Char('Table number', 
                       size=64, 
                       required=True)
    capacity = fields.Integer('Capacity')


class hotel_restaurant_reservation(models.Model):

    @api.multi
    def create_order(self):
         k = []
         for i in self.browse(self.ids):
             table_ids = [x.id for x in i.tableno]
             kot_data = self.env['hotel.reservation.order'].create(
                                            {'reservationno':i.reservation_id,
                                            'date1':i.start_date,
                                            'table_no':[(6, 0, table_ids)],
                                            })

         return True

    @api.multi
    def onchange_partner_id(self, part):
         if not part:
             return {'value':{'partner_address_id': False}}
         addr = self.env['res.partner'].address_get([part], ['default'])
         pricelist = self.env['res.partner'].browse(part).property_product_pricelist_purchase.id
         return {'value':{'partner_address_id': addr['default']}}


    @api.multi
    def action_set_to_draft(self):
        self.write(self.ids, {'state': 'draft'})
        wf_service = netsvc.LocalService('workflow')
        for id in self.ids:
            wf_service.trg_create(self._name, self.id)
        return True


    @api.multi
    def table_reserved(self):
        for reservation in self.browse(self.ids):

            self._cr.execute("select count(*) from hotel_restaurant_reservation as hrr " \
                       "inner join reservation_table as rt on rt.reservation_table_id = hrr.id " \
                       "where (start_date,end_date)overlaps( timestamp %s , timestamp %s ) " \
                       "and hrr.id<> %s " \
                       "and rt.name in (select rt.name from hotel_restaurant_reservation as hrr " \
                       "inner join reservation_table as rt on rt.reservation_table_id = hrr.id " \
                       "where hrr.id= %s) " \
                        , (reservation.start_date, reservation.end_date, reservation.id, reservation.id))

            res = self._cr.fetchone()

            roomcount = res and res[0] or 0.0
            if roomcount:
                raise osv.except_osv('Warning', 'You tried to confirm reservation with table those already reserved in this reservation period')
            else:
                self.write({'state':'confirm'})
            return True

    @api.multi
    def table_cancel(self):
        self.write({'state':'cancel'})
        return True

    @api.multi
    def table_done(self):
        self.write({'state':'done'})
        return True
    

    _name = "hotel.restaurant.reservation"
    _description = "Includes Hotel Restaurant Reservation"
    
    reservation_id = fields.Char('Reservation No', 
                                 size=64, 
                                 required=True)
    room_no = fields.Many2one('hotel.room', 
                              'Room No', 
                              size=64)
    start_date = fields.Datetime('Start Date', 
                                 required=True)
    end_date = fields.Datetime('End Date', 
                               required=True)
    cname = fields.Many2one('res.partner', 
                            'Customer Name', 
                            size=64, 
                            required=True)
    partner_address_id = fields.Many2one('res.partner.address', 
                                         'Address')
    tableno = fields.Many2many('hotel.restaurant.tables', 
                               'reservation_table', 
                               'reservation_table_id', 
                               'name', 
                               'Table number')
    state =  fields.Selection([('draft', 'Draft'), 
                               ('confirm', 'Confirmed'), 
                               ('done', 'Done'), 
                               ('cancel', 'Cancelled')], 
                              'state', 
                              select=True, 
                              required=True, 
                              readonly=True)

    
    _sql_constraints = [
                        ('check_dates', 'CHECK (start_date<=end_date)', 'Start Date Should be less than the End Date!'),
                       ]
    
    _defaults = {
        'state': lambda * a: 'draft',
        'reservation_id':lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'hotel.restaurant.reservation'),
    }
    


class hotel_restaurant_kitchen_order_tickets(models.Model):
    _name = "hotel.restaurant.kitchen.order.tickets"
    _description = "Includes Hotel Restaurant Order"
    
    orderno = fields.Char('Order Number', size=64, readonly=True)
    resno = fields.Char('Reservation Number', size=64)
    kot_date = fields.Datetime('Date')
    room_no = fields.Char('Room No', size=64, readonly=True)
    w_name = fields.Char('Waiter Name', size=64, readonly=True)
    tableno = fields.Many2many('hotel.restaurant.tables', 'temp_table3', 'table_no', 'name', 'Table number', size=64)
    kot_list = fields.One2many('hotel.restaurant.order.list', 'kot_order_list', 'Order List')


class hotel_restaurant_order(models.Model):

    @api.multi
    def _sub_total(self):
        res = {}
        for sale in self.browse(self.ids):
            res[sale.id] = 0.00
            for line in sale.order_list:
                res[sale.id] += line.price_subtotal
        return res


    @api.multi
    def _total(self):
       res = {}
       for line in self.browse(self.ids):
           res[line.id] = line.amount_subtotal + (line.amount_subtotal * line.tax) / 100
       return res

    @api.multi
    def generate_kot(self, part):
        
        for order in self.browse(self.ids):
            table_ids = [x.id for x in order.table_no]
            kot_data = self.env['hotel.restaurant.kitchen.order.tickets'].create({
                                                    'orderno':order.order_no,
                                                    'kot_date':order.o_date,
                                                    'room_no':order.room_no.name,
                                                    'w_name':order.waiter_name.name,
                                                    'tableno':[(6, 0, table_ids)],
                                                    })

            for order_line in order.order_list:

                o_line = {
                         'kot_order_list':kot_data,
                         'name':order_line.name.id,
                         'item_qty':order_line.item_qty,
                             }
                self.env['hotel.restaurant.order.list'].create(o_line)

        return True


    _name = "hotel.restaurant.order"
    _description = "Includes Hotel Restaurant Order"
    
    order_no = fields.Char('Order Number', 
                           size=64, 
                           required=True)
    o_date = fields.Datetime('Date', 
                             required=True)
    room_no = fields.Many2one('hotel.room', 
                              'Room No', 
                              size=64)
    waiter_name = fields.Many2one('res.partner', 
                                  'Waiter Name', 
                                  size=64, 
                                  required=True)
    table_no = fields.Many2many('hotel.restaurant.tables', 
                                'temp_table2', 
                                'table_no', 
                                'name', 
                                'Table number', 
                                size=64)
    order_list = fields.One2many('hotel.restaurant.order.list', 
                                 'o_list', 
                                 'Order List')
    tax = fields.Float('Tax (%) ', 
                       size=64)
    amount_subtotal = fields.Float(compute="_sub_total", 
                                      method=True, 
                                      string='Subtotal')
    amount_total = fields.Float(compute="_total", 
                                   method=True, 
                                   string='Total')
    
    _defaults = {
     'order_no': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'hotel.restaurant.order'),

     }



class hotel_reservation_order(models.Model):
    
    @api.multi
    def _sub_total(self):
        res = {}
        for sale in self.browse(self.ids):
            res[sale.id] = 0.00
            for line in sale.order_list:
                res[sale.id] += line.price_subtotal
        return res

    @api.multi
    def _total(self):
       res = {}
       for line in self.browse(self.ids):
           res[line.id] = line.amount_subtotal + (line.amount_subtotal * line.tax) / 100
       return res

    @api.multi
    def reservation_generate_kot(self, part):

        for order in self.browse(self.ids):
            table_ids = [x.id for x in order.table_no]
            kot_data = self.env['hotel.restaurant.kitchen.order.tickets'].create({
                                                'orderno':order.order_number,
                                                'resno':order.reservationno,
                                                'kot_date':order.date1,
                                                'w_name':order.waitername.name,
                                                'tableno':[(6, 0, table_ids)],
                                                })

            for order_line in order.order_list:

                o_line = {
                         'kot_order_list':kot_data,
                         'name':order_line.name.id,
                         'item_qty':order_line.item_qty,
                             }
                self.env['hotel.restaurant.order.list'].create(o_line)

        return True

    _name = "hotel.reservation.order"
    _description = "Reservation Order"
    
    order_number = fields.Char('Order No', 
                               size=64)
    reservationno = fields.Char('Reservation No', 
                                size=64)
    date1 = fields.Datetime('Date', 
                            required=True)
    waitername = fields.Many2one('res.partner', 
                                 'Waiter Name', 
                                 size=64)
    table_no = fields.Many2many('hotel.restaurant.tables', 
                                'temp_table4', 
                                'table_no', 
                                'name', 
                                'Table number', 
                                size=64)
    order_list = fields.One2many('hotel.restaurant.order.list', 
                                 'o_l', 
                                 'Order List')
    tax = fields.Float('Tax (%) ', 
                       size=64)
    amount_subtotal = fields.Float(compute="_sub_total", 
                                      method=True, 
                                      string='Subtotal')
    amount_total = fields.Float(compute="_total", 
                                   method=True, 
                                   string='Total')
    
    _defaults = {
        'order_number':lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'hotel.reservation.order'),
        }



class hotel_restaurant_order_list(models.Model):

    @api.multi
    def _sub_total(self):
        res = {}
        for line in self.browse(self.ids):
           res[line.id] = line.item_rate * int(line.item_qty)
        return res

    @api.multi
    def on_change_item_name(self, name):
      if not name:
         return {'value':{}}
      temp = self.env['hotel.menucard'].browse(name)
      return {'value':{'item_rate':temp.list_price}}


    _name = "hotel.restaurant.order.list"
    _description = "Includes Hotel Restaurant Order"
    
    o_list = fields.Many2one('hotel.restaurant.order')
    o_l = fields.Many2one('hotel.reservation.order')
    kot_order_list = fields.Many2one('hotel.restaurant.kitchen.order.tickets')
    name = fields.Many2one('hotel.menucard', 'Item Name', required=True)
    item_qty = fields.Char('Qty', size=64, required=True)
    item_rate = fields.Float('Rate', size=64),
    price_subtotal = fields.Float(compute="_sub_total", method=True, string='Subtotal')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
