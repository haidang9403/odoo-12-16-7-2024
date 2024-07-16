odoo.define('sea_pos_print_product_label.buttons', function (require) {
    var screens = require('point_of_sale.screens');

    // Thaipham - 29/06/2024
    var button_print_product_label = screens.ActionButtonWidget.extend({
        template: 'button_print_product_label',
        button_click: function () {
            this.pos.gui.show_screen('print_product_label');
        },
    });
    screens.define_action_button({
        'name': 'button_print_product_label',
        'widget': button_print_product_label,
        'condition': function () {
            return this.pos.config.print_product_label;
        },
    });
})