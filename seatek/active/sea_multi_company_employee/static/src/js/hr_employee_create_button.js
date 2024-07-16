odoo.define('multi_company_employee.create_employee_button', function (require) {
"use strict";
var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');
var CreateButton = ListController.extend({
   buttons_template: 'multi_company_employee.buttons',
   events: _.extend({}, ListController.prototype.events, {
       'click .open_wizard_actions': '_OpenWizard',
   }),
   init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);
        console.log('open create employee',this)
    },
   _OpenWizard: function () {
   console.log('open employee')
       var self = this;
        this.do_action({
           type: 'ir.actions.act_window',
           res_model: 'hr.employee',
           name :'Create Employee',
           view_mode: 'form',
           view_type: 'form',
           views: [[false, 'form']],
           target: 'new',
           res_id: false,
       });
   },renderButtons: function () {
            this._super.apply(this, arguments); // Possibly sets this.$buttons
            if (this.$buttons) {
                var self = this;
                this.$buttons.on('click', '.open_wizard_action', function () {
                    self.do_action({
                        type: 'ir.actions.act_window',
                           res_model: 'hr.employee',
                           name :'Create Employee',
                           view_mode: 'form',
                           view_type: 'form',
                           views: [[false, 'form']],
                           target: "target",
                           res_id: false,
                    });
                });
            }
        }

});
var CreateEmployeeButton = ListView.extend({
   config: _.extend({}, ListView.prototype.config, {
       Controller: CreateButton,
   }),
});
viewRegistry.add('create_employee_button', CreateEmployeeButton);
});