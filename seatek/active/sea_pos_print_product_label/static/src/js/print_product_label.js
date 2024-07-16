odoo.define('sea_pos_print_product_label.print_product_label', function (require) {
    "use strict";
    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('pos.rpc');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var chrome = require('point_of_sale.chrome');
    var field_utils = require('web.field_utils');

    var print_product_label = screens.ScreenWidget.extend({
        template: 'print_product_label',
        show: function () {
            this._super();
            this.render_receipt();
            this.handle_auto_print();
            this.auto_print_network(); // TODO: supported module pos_retail_network_printer
        },
        handle_auto_print: function () {
            if (this.should_auto_print()) {
                this.print();
            } else {
                this.lock_screen(false);
            }
        },
        auto_print_network: function () {
            if (this.pos.epson_printer_default && this.pos.report_xml) {
                this.pos.print_network(this.pos.report_xml, this.pos.epson_printer_default['ip']);
            }
        },
        should_auto_print: function () {
            return this.pos.config.iface_print_auto;
        },
        lock_screen: function (locked) {
            this._locked = locked;
            if (locked) {
                this.$('.back').removeClass('highlight');
            } else {
                this.$('.back').addClass('highlight');
            }
        },
        print_web: function () {
            window.print();
        },
        print_xml: function () {
            var self = this;
            this.pos.proxy.print_receipt(this.pos.report_xml);
            if (!this.pos.report_xml) {
                setTimeout(function () {
                    self.print_web();
                }, 500)
            }
        },
        print: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {
                this.lock_screen(true);
                setTimeout(function () {
                    self.lock_screen(false);
                }, 1000);
                this.print_web();
            } else {
                this.print_xml();
                this.lock_screen(false);
            }
            this.auto_print_network()
        },
        click_back: function () {
            this.pos.gui.show_screen('products')
        },
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.back').click(function () {
                if (!self._locked) {
                    self.click_back();
                }
                self.pos.trigger('back:order');
            });
            this.$('.button.print').click(function () {
                self.print();
            });
        },
        render_receipt: function () {
            var last_order = this.pos.db.get_pos_orders().reverse()[0];
            var last_order_line = []
            for (const value of Object.keys(this.pos.db.lines_by_order_id)){
                if (value == last_order.id) {
                    last_order_line = this.pos.db.lines_by_order_id[String(value)]
                }
            }
            var label_html =''
            var count_item = last_order_line.length;
            if (count_item == 1) {
                for (const line of last_order_line) {
                    var get_product_line = this.pos.db.get_product_by_id(line.product_id[0])
                    if (get_product_line.print_product_label && Number.isInteger(line.qty)) {
                        var set_num = 0
                        var count_product = line.qty
                        for (var i = 0; i < line.qty; i++) {
                            set_num += 1
                            label_html +=
                            "<div style='width: 100%; height: 110px; position: relative; font-size: 9px; text-align:left; background-color: white; font-family: arial'>"+
                            '<div style="font-size: 11px; position: relative; top: 5px">' + String(last_order.pos_reference)+' ['+set_num +'/'+line.qty+']'+'</div>'+
                            '<div style="text-align: left; width: 180px; margin-top: 7px; font-family: monospace; font-weight: 700; font-size: 12px; line-height: initial;">'+String(line.product_id[1].split('] ')[1])+'</div>'+
                            '<div style="text-align: left; width: 180px; margin-left: 8px; margin-top: 3px; font-size: 10px;">'+String(line.note)+'</div>' +
                            '<div style="position: absolute; top: 79px">'+String(line.write_date)+'</div>' +
                            '<div style="position: absolute; top: 57px; left: 127px"><img src="'+String(window.location.origin)+'/web/image?model=pos.config&id='+String(this.pos.config.id)+'&field=logo_label" alt="label" height="40"'+'/></div>' +
                            '<div style="width: 179px; font-size: 7.7px; position: absolute; top: 97px; font-weight: 500">DannyGreen Lovers - For your fast healthy meals!</div>'+
                            "</div>"
                        }
                    }
                }
            }
            else {
                for (const line of last_order_line) {
                    var get_product_line = this.pos.db.get_product_by_id(line.product_id[0])
                    if (get_product_line.print_product_label && Number.isInteger(line.qty)) {
                        if (line.qty > 1) {
                            var set_num = 0
                            var count_product = line.qty
                            for (var i = 0; i < line.qty; i++) {
                                set_num += 1
                                label_html +=
                                "<div style='width: 100%; height: 110px; position: relative; font-size: 9px; text-align:left; background-color: white; font-family: arial'>"+
                                '<div style="font-size: 11px; position: relative; top: 5px">' + String(last_order.pos_reference)+'</div>'+
                                '<div style="text-align: left; width: 179px; margin-top: 7px; font-family: monospace; font-weight: 700; font-size: 12px; line-height: initial;">'+String(line.product_id[1].split('] ')[1])+' ['+set_num +'/'+count_product+']'+'</div>'+
                                '<div style="text-align: left; width: 179px; margin-left: 8px; margin-top: 3px; font-size: 10px;">'+String(line.note)+'</div>' +
                                '<div style="position: absolute; top: 79px">'+String(line.write_date)+'</div>'+
                                '<div style="position: absolute; top: 57px; left: 127px"><img src="'+String(window.location.origin)+'/web/image?model=pos.config&id='+String(this.pos.config.id)+'&field=logo_label" alt="label" height="40"'+'/></div>' +
                                '<div style="width: 179px; font-size: 7.7px; position: absolute; top: 97px; font-weight: 500">DannyGreen Lovers - For your fast healthy meals!</div>'+
                                "</div>"
                                /*"<div style='width: 100%; height: 110px; position: relative; font-size: 9px; text-align:left; background-color: white; font-family: arial'>"+
                                '<div style="font-size: 10px;">' + String(last_order.pos_reference)+' ( '+set_num +'/'+count_item+' )'+'</div>'+
                                '<div style="text-align: left; width: 180px; margin-top: 7px; font-family: monospace; font-weight: 700; font-size: 12px; line-height: initial;">'+String(line.product_id[1].split('] ')[1])+ ' | ' + String(new Intl.NumberFormat().format(line.price_unit)) +' đ'+'</div>'+
                                '<div style="text-align: left; width: 180px; font-size: 11px; line-height: initial;">'+String(line.product_id[1].split('] ')[1])+'</div>'+
                                '<div style="text-align: left; width: 180px; margin-left: 5px">'+String(line.note)+'</div>' +
                                '<div style="position: absolute; top: 58px">'+String(line.write_date)+'</div>' +
                                '<div style="font-style: italic; position: absolute; top: 74px">DannyGreen Lovers - Healthy Fast Meal</div>'+
                                "</div>"*/
                            }
                        }
                        else {
                            label_html +=
                            "<div style='width: 100%; height: 110px; position: relative; font-size: 9px; text-align:left; background-color: white; font-family: arial'>"+
                            '<div style="font-size: 11px; position: relative; top: 5px">' + String(last_order.pos_reference)+'</div>'+
                            '<div style="text-align: left; width: 180px; margin-top: 7px; font-family: monospace; font-weight: 700; font-size: 12px; line-height: initial;">'+String(line.product_id[1].split('] ')[1])+' [1/1]'+'</div>'+
                            '<div style="text-align: left; width: 180px; margin-left: 8px; margin-top: 3px; font-size: 10px;">'+String(line.note)+'</div>' +
                            '<div style="position: absolute; top: 79px">'+String(line.write_date)+'</div>'+
                            '<div style="position: absolute; top: 57px; left: 127px"><img src="'+String(window.location.origin)+'/web/image?model=pos.config&id='+String(this.pos.config.id)+'&field=logo_label" alt="label" height="40"'+'/></div>' +
                            '<div style="width: 179px; font-size: 7.7px; position: absolute; top: 97px; font-weight: 500">DannyGreen Lovers - For your fast healthy meals!</div>'+
                            "</div>"
                        }
                    }
                }
            }
            this.$('.pos-receipt-container').html(label_html);
        }
    });

    gui.define_screen({name: 'print_product_label', widget: print_product_label});
});