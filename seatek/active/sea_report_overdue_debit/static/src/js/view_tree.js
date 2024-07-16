
odoo.define('sea_report_overdue_debit.view_tree', function (require) {
// The goal of this file is to contain JS hacks related to allowing
// section and note on sale order and invoice.

// [UPDATED] now also allows configuring products on sale order.

"use strict";
var viewRegistry = require('web.view_registry');
var rpc = require('web.rpc');
//widget view tree
var ListRenderer = require('web.ListRenderer');
var ListView = require('web.ListView');
var ListController = require('web.ListController');
var SaleOrderApprovedListRenderer = ListRenderer.extend({
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        var self=this;
    },
    _renderHeader: function () {
        var $header = this._super.apply(this, arguments); // Tạo một th mới
        $header.find('tr:nth-child(1) th:first').remove();
        // Xóa hai <th> đầu tiên ở dòng 2
        $header.find('tr:nth-child(2) th:lt(2)').remove();
        // Thêm th vào cuối cùng trong ttr
        var $newHeader = $('<th>');
        $header.find('tr:nth-child(2)').append($newHeader);

        return $header;
    },
//    _renderFooter: function () {
//        var $footer = this._super.apply(this, arguments);
//
//        // Tạo một td mới
//        var $newFooterCell = $('<td>');
//
//        // Thêm td vào cuối cùng trong tr của tfoot
//        $footer.find('tr').append($newFooterCell);
//
//        return $footer;
//    },
    _renderRow: function (record, index) {
        var $row = this._super.apply(this, arguments); // Lấy kết quả render row gốc

        // Xóa td đầu tiên trong dòng
        $row.find('td:first').remove();
        return $row;
    },

});
var SaleOrderApprovedListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: ListController,
        Renderer: SaleOrderApprovedListRenderer,
    }),
});
viewRegistry.add('sale_order_approved_view', SaleOrderApprovedListView);

//========================================================= ---  =====================================//
var HideCheckboxListRenderer = ListRenderer.extend({
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        var self=this;
    },
    _renderHeader: function () {
        var $header = this._super.apply(this, arguments); // Tạo một th mới
        // Xóa thẻ th đầu tiên trên cả hai dòng <tr>
        $header.find('tr').each(function() {
            $(this).find('th:first').remove();
        });
        return $header;
    },
    _renderRow: function (record, index) {
        var $row = this._super.apply(this, arguments); // Lấy kết quả render row gốc
        // Xóa td đầu tiên trong dòng
        $row.find('td:first').remove();
        return $row;
    },
    _renderBodyCell: function (record, node, index, options) {
        var $cell = this._super.apply(this, arguments);
        if ($cell.hasClass('o_data_cell o_list_number o_monetary_cell o_readonly_modifier')) {
            $cell.addClass('text_right');
        }
        return $cell;
    },

});
var HideCheckbox = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: ListController,
        Renderer: HideCheckboxListRenderer,
    }),
});
viewRegistry.add('hide_checkbox', HideCheckbox);

//========================================================= ---  =====================================//
//widget view form
var FormRenderer = require('web.FormRenderer');
var FormController = require('web.FormController');
var FormView = require('web.FormView');
var MarkAsTodoFormRenderer = FormRenderer.extend({
    _render: function () {
        console.log("renderer");
        var res = this._super.apply(this, arguments);
        // Truy cập đến đối tượng FormController
        var self = this;
        var controller = this.getParent();
        if (controller) {
            if (this.state.data.mark_as_todo){
                controller.$buttons.find('.o_form_button_edit').hide();
            }else{
                controller.$buttons.find('.o_form_button_edit').show();
            }
        }
        return res;
    },
})
var MarkAsTodoFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: FormController,
        Renderer: MarkAsTodoFormRenderer,
    }),
});

viewRegistry.add('mark_as_todo', MarkAsTodoFormView);


//========================================================= ---  =====================================//

});
