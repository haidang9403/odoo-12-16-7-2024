odoo.define("sea_pos_print_product_label.model", function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var session = require('web.session');
    var rpc = require('web.rpc');

    var field_utils = require('web.field_utils');

    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({

        initialize: function (session, attributes) {
            var self = this;
            this.get_model('product.product').fields.push('print_product_label');
            _super_PosModel.initialize.apply(this, arguments);
        }
    });
})