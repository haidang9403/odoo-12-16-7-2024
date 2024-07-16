odoo.define('sea_pos_auto_issue_invoice.screen_payment', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    console.log(screens)
    console.log(models)
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    var _super_order = models.Order.prototype;

    models.load_models([{
        model:  'res.country.state',
        fields: [ 'code', 'name', 'country_id',],
        domain: function(self) {return [['country_id', '=', 241]]},
        loaded: function(self, state_ids){
            if(state_ids.length){
                self.state_ids = state_ids
                self.state_by_id = {}
                _.each(state_ids, function(state){
                    self.state_by_id[state.id] = state;
                });
            }
        },
    }], {'after': 'res.country'});


    screens.PaymentScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            var order = self.pos.get_order();
            var client = self.pos.get_client();
            if (order.is_get_invoice) {
                self.$('.get_invoice').addClass('highlight');
            } else {
                self.$('.get_invoice').removeClass('highlight');
            }
            this.$('.get_invoice').click(function () {
                self.renderElement();
                self.customer_get_invoice();
            });
        },
        customer_get_invoice: function () {
            var self = this;
            var order = self.pos.get_order();

            var _get_partners_invoice_address = {}
            var get_customer_current = self.pos.get_client()
            if (get_customer_current.is_company == true && get_customer_current.vat != false) {
                _get_partners_invoice_address = self.pos.db.get_partners_sorted().filter(x => x.vat == get_customer_current.vat)
            }
            else {
                _get_partners_invoice_address = self.pos.db.get_partners_sorted().filter(x => x.is_company == true && x.vat != false).slice(0, 3);
            }

            const data_temp_id = {}
            for (const value of Object.values(self.pos.db.partner_by_id)){
                if (value.is_company == true && value.vat != false) {
                    const adc = String(value.id);
                    Object.assign(data_temp_id, data_temp_id[adc] = value);
                }
            }


            if (order.is_get_invoice) {
                order['is_get_invoice'] = false;
                order['invoice_address_id'] = ""
                order['invoice_address_name'] = ""
                self.renderElement();
                self.get_invoice_remove_highlight();

            } else {
                var quickly_search_client = self.pos.config.quickly_search_client;
                if (quickly_search_client) {
                    self.gui.show_screen('products');
                    self.pos.gui.show_popup('popup_selection_extend', {
                        title: 'Select Customer Invoice Address',
                        fields: ['name', 'email', 'phone', 'mobile'],
                        /*sub_datas: self.pos.db.get_partners_sorted(5),*/
                        sub_datas: _get_partners_invoice_address,
                        sub_search_string: self.pos.db.partner_search_string,
                        /*sub_record_by_id: self.pos.db.partner_by_id,*/
                        sub_record_by_id: data_temp_id,
                        /*sub_template: 'clients_list',*/
                        sub_template: 'select_invoice_address',
                        /*sub_button: '<div class="btn btn-success pull-right go_clients_screen">Go Clients Screen</div>',
                        sub_button_action: function () {
                            self.pos.gui.show_screen('clientlist')
                        },*/

                        sub_button: '<div class="btn btn-success pull-right">NEW INVOICE ADDRESS</div>',
                        sub_button_action: function () {
                            self.pos.gui.show_popup('popup_create_customer')
                        },
                        body: 'Please select one client',
                        confirm: function (client_id) {
                            var client = self.pos.db.get_partner_by_id(client_id);
                            if (client) {
                                if (! client.vat){
                                    return this.pos.gui.show_popup('dialog', {
                                        title: 'Warning',
                                        body: 'Please Enter Tax code for Customer.'
                                    }),
                                    self.gui.show_screen('payment');
                                }
                                else {
                                    order['is_get_invoice'] = true;
                                    order['invoice_address_id'] = client.id
                                    order['invoice_address_name'] = client.name
                                    self.renderElement();
                                    self.get_invoice_add_highlight();
                                }
                            }
                            self.gui.show_screen('payment');
                        },
                        cancel: function(){
                            self.get_invoice_remove_highlight()
                            self.gui.show_screen('payment');
                        },
                    })
                }
            }
        },
        get_invoice_add_highlight: function () {
            var self = this;
            self.$('.get_invoice').addClass('highlight');
        },
        get_invoice_remove_highlight: function () {
            var self = this;
            self.$('.get_invoice').removeClass('highlight');
        },

    });

    models.Order = models.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this,arguments);
            this.is_get_invoice = this.is_get_invoice;
            this.save_to_db();
        },

        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.is_get_invoice = this.is_get_invoice;
            json.invoice_address = this.invoice_address_id;
            return json;
        },
    });
});