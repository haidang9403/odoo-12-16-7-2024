odoo.define("multi_company_employee.hr_employee_form", function (require) {
    "use strict";

    var ListRenderer = require("web.ListRenderer");
    ListRenderer.include({
        _renderRow: function (record) {
            let row = this._super(record);
            var self = this;
            if (record.model == "hr.employee.multi.company" && this.getParent().displayName!=undefined ) {
                row.addClass('o_list_no_open');
                // add click event
                row.bind({
                    click: function (ev) {
                        if((typeof(ev.target.type)=="undefined" && ev.target.tagName!="LABEL") ){
                            if(ev.target.type!="checkbox"){
                                ev.preventDefault();
                                ev.stopPropagation();
                                self.do_action({
                                    type: "ir.actions.act_window",
                                    res_model: "hr.employee",
                                    res_id: record.data.name.res_id,
                                    views: [[false, "form"]],
                                    target: "target",
                                    context: record.context || {},
                                });
                            }
                        }
                    }
                });
            }
            return row
        },
    });
});