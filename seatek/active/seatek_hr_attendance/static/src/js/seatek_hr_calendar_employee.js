
odoo.define('seatek_hr_appraisal.seatek_hr_calendar_employee', function (require) {
// The goal of this file is to contain JS hacks related to allowing
// section and note on sale order and invoice.

// [UPDATED] now also allows configuring products on sale order.

"use strict";
var pyUtils = require('web.py_utils');
var core = require('web.core');
var ajax = require('web.ajax');
var _t = core._t;
var rpc = require('web.rpc');
var FieldOne2Many = require('web.relational_fields').FieldOne2Many;

var fieldRegistry = require('web.field_registry');
var ListRenderer = require('web.ListRenderer');
var session = require('web.session');
var dom = require('web.dom');

var config = require('web.config');
var Sidebar = require('web.Sidebar');
var AbstractController = require('web.AbstractController');
var ListView = require('web.ListView');
var CalendarView = require('web.CalendarView');
var viewRegistry = require('web.view_registry');
var ControlPanel = require('web.ControlPanel');
var qweb = core.qweb;


var FIELD_CLASSES = {
    float: 'o_list_number',
    integer: 'o_list_number',
    monetary: 'o_list_number',
    text: 'o_list_text',
};
//widget one2many
var AttendanceRenderer = ListRenderer.extend({
    events: _.extend({}, ListRenderer.prototype.events, {
        'click tbody td.o_data_cell': '_onCellClick',
        'keydown .o_field_x2many_list_row_add a': '_onKeyDownAddRecord',
        'click tbody tr': '_onRowClicked',
        'click .o_field_x2many_list_row_add a': '_onAddRecord',
    }),
    init: function (parent, state, params) {
        var self = this;
        this._super.apply(this, arguments);
        FilterControllerMixin._bindFilter.call(self);
    },

    start: function () {
        // Gọi hàm start của lớp cha
        this._super.apply(this, arguments);
        // Thêm các button vào DOM ở đây


    },


    _onCellClick(event){
        if(this.state.model === "sea.hr.attendance.month") {
            var $td = $(event.currentTarget);
            var $tr = $td.parent();
            var rowIndex = this.$('.o_data_row').index($tr);
            var fieldIndex = Math.max($tr.find('.o_data_cell').not('.o_list_button').index($td), 0)-1;
//             console.log(rowIndex, fieldIndex)

            var self = this;
            var id = this.state.res_ids[rowIndex + this.state.offset]
//            console.log(this, id)
            this._rpc({
                model: 'sea.hr.attendance.month',
                method: 'search_read',
                domain: [['id','=',id]],
                fields: ['id', 's_identification_id', 'employee_multi_id', 'attendance_id', 'year','month', 'day_1', 'day_2', 'day_3', 'day_4', 'day_5', 'day_6', 'day_7', 'day_8', 'day_9', 'day_10', 'day_11', 'day_12', 'day_13', 'day_14', 'day_15', 'day_16', 'day_17', 'day_18', 'day_19', 'day_20', 'day_21', 'day_22', 'day_23', 'day_24', 'day_25', 'day_26', 'day_27', 'day_28', 'day_29', 'day_30', 'day_31'],
            }).then(function (result) {
                // console.log(result)
                event.preventDefault();
                event.stopPropagation(); // Ngăn chặn sự kiện click lan sang các phần tử cha
                switch (fieldIndex) {
                    case 1:
                        id = result[0].day_1[0];
                        break;
                    case 2:
                        id = result[0].day_2[0];
                        break;
                    case 3:
                       id = result[0].day_3[0];
                        break;
                    case 4:
                        id = result[0].day_4[0];
                        break;
                    case 5:
                        id = result[0].day_5[0];
                        break;
                    case 6:
                        id = result[0].day_6[0];
                        break;
                    case 7:
                        id = result[0].day_7[0];
                        break;
                    case 8:
                        id = result[0].day_8[0];
                        break;
                    case 9:
                        id = result[0].day_9[0];
                        break;
                    case 10:
                        id = result[0].day_10[0];
                        break;
                    case 11:
                        id = result[0].day_11[0];
                        break;
                    case 12:
                        id = result[0].day_12[0];
                        break;
                    case 13:
                        id = result[0].day_13[0];
                        break;
                    case 14:
                        id = result[0].day_14[0];
                        break;
                    case 15:
                        id = result[0].day_15[0];
                        break;
                    case 16:
                        id = result[0].day_16[0];
                        break;
                    case 17:
                       id = result[0].day_17[0];
                        break;
                    case 18:
                        id = result[0].day_18[0];
                        break;
                    case 19:
                        id = result[0].day_19[0];
                        break;
                    case 20:
                        id = result[0].day_20[0];
                        break;
                    case 21:
                        id = result[0].day_21[0];
                        break;
                    case 22:
                        id = result[0].day_22[0];
                        break;
                    case 23:
                        id = result[0].day_23[0];
                        break;
                    case 24:
                        id = result[0].day_24[0];
                        break;
                    case 25:
                        id = result[0].day_25[0];
                        break;
                    case 26:
                        id = result[0].day_26[0];
                        break;
                    case 27:
                        id = result[0].day_27[0];
                        break;
                    case 28:
                        id = result[0].day_28[0];
                        break;
                    case 29:
                        id = result[0].day_29[0];
                        break;
                    case 30:
                        id = result[0].day_30[0];
                        break;
                    case 31:
                        id = result[0].day_31[0];
                        break;
                    default:
                        id = false;
                        break;
            }
                if(fieldIndex > 0){
                    self.do_action({
                        name: _t("Chấm công ngày " + fieldIndex + "/" + result[0].month),
                        type: 'ir.actions.act_window',
                        res_model: 'sea.hr.attendance.realtime',
                        res_id: id,
                        views: [[false, 'form']],
                        target: 'current',
                        context: {
                            default_employee_multi_id:  result[0].employee_multi_id[0],
                            default_year : result[0].year,
                            default_month : result[0].month,
                            default_day : fieldIndex,
                        }
                    });
                }
            });

        }
     },
    _onKeyDown(event){
     },
     _onSortColumn: function (event){
        return;
     },
     _onRowClicked(event){
     },
    _processColumns(columnInvisibleFields) {
        this._super.apply(this, arguments);
        var self = this;
        this.temp_columns=[...this.columns];
//        console.log('khánh đây')
        let columns=[];
        var month = this.__parentedParent.recordData.month
        var year = this.__parentedParent.recordData.year
        // Tạo đối tượng Date biểu diễn ngày cuối cùng trong tháng
        var lastDayOfMonth = new Date(year, month, 0);
        // Lấy số ngày trong tháng
        var daysInMonth = lastDayOfMonth.getDate();

        for (var i = 0; i <= daysInMonth+1; i++) {
            columns.push(this.temp_columns[i]);
        }
        this.columns=columns;
    },
    _renderHeader: function (isGrouped) {
        var self = this;
        if(this.arch.attrs.condition === 'tree') {
            const $thead = $('<thead>');
            $thead.addClass('dexuat_sau_dgns_thead');

            {
//            // Lấy External ID của một action trong Odoo mà không dựa vào action hiện tại
//            var actionXMLID = 'seatek_hr_attendance.sea_hr_attendance_action'; // Thay thế bằng External ID của action
//            var modelName = 'ir.model.data'; // Tên mô hình cho dữ liệu mô hình
//            console.log('module', '=', actionXMLID.split('.')[0], 'name', '=', actionXMLID.split('.')[1]);
//            rpc.query({
//                model: modelName,
//                method: 'search_read',
//                kwargs: {
//                    domain: [['module', '=', actionXMLID.split('.')[0]], ['name', '=', actionXMLID.split('.')[1]]],
//                    fields: ['res_id'],
//                    limit: 1,
//                },
//            }).then(function (result) {
//                if (result.length > 0) {
//                    var resID = result[0].res_id;
//                    console.log('Res ID:', resID);
//                } else {
//                    console.error('Action not found.');
//                }
//            }).fail(function (error, event) {
//                console.error('Error:', error);
//            });
}
            // Thêm ô tìm kiếm
            var text = '';
            if(this.__parentedParent.recordData.employee_id!=false && this.__parentedParent.name=="attendance_of_month_compute"){
                text= this.__parentedParent.recordData.employee_id
            }else{
                if(this.__parentedParent.recordData.employee_id_c!=false && this.__parentedParent.name=="calendar_of_month_compute"){
                    text= this.__parentedParent.recordData.employee_id_c
                }
            }
            const $searchRow = $('<tr>');
            let $searchCell = $('<th>').attr('colspan', 6);
            const $searchInput = $('<span style="text-align:left; display: flex; align-items: center;margin-bottom: 5px;" class="fa fa-search">&nbsp;Tìm theo tên nhân sự hoặc mã SeaCode</span><input>')
                .attr('type', 'text')
                .attr('placeholder', 'Tìm kiếm...')
                .attr('value', text)
                .css({
                  'width': '300px' // Thay '100px' bằng giá trị chiều rộng mong muốn
                });
                // Xử lý sự kiện 'input' trên ô tìm kiếm
            $searchInput.on('change', function (event) {
                // document.getElementById("attendance-sort_name").innerHTML  ='<span class="fa fa-filter"/>'+'&nbsp;'+$(this).context.innerText
                var changedValue = event.target.value;
//                console.log("Giá trị đã thay đổi:", changedValue);
                var fields = {};
                if(self.__parentedParent.name=="calendar_of_month_compute"){
                   fields['employee_id_c'] = changedValue;
                }else{
                    fields['employee_id'] = changedValue;
                }
                rpc.query({
                    model: 'sea.hr.attendance',
                    method: 'write',
                    args: [[parseInt(this.__parentedParent.recordData.id)], fields],
                })
                .done(function(result) {
                    console.log('done');
                    self.trigger_up('reload');
                }).fail(function(unused, event) {
                    console.log('fail');
                });

            }.bind(this));
            $searchCell.append($searchInput);
            $searchRow.append($searchCell);

            const $filterCell = $('<th>').attr('colspan', this.columns.length-6);
            {
//            let $filterCellInput = '<div style="text-align : left"><t t-name="AttendanceFilter"><span class="attendance_filter" data-qweb="AttendanceFilter"><a id="attendance-sort_name" type="button" class="btn btn-link dropdown-toggle attendance_text" data-toggle="dropdown"><span class="fa fa-filter dropdown-parent "/>';
//            if(self.__parentedParent.name=="calendar_of_month_compute"){
//                if(self.__parentedParent.recordData.department_id_c!=false){
//                    $filterCellInput = $filterCellInput + '&nbsp;' + self.__parentedParent.recordData.department_id_c.data.display_name
//                                        + '</a><div class="dropdown-menu o_filters_menu_attendance" role="button">'
//                }else{
//                    $filterCellInput = $filterCellInput + '&nbsp;Tất cả Phòng ban/Chức vụ</a><div class="dropdown-menu o_filters_menu_attendance" role="menu">'
//                }
//                $filterCellInput = $filterCellInput + '<div><button name="all" value="false" type="button" data-id="' + self.__parentedParent.recordData.id + '" data-department_id_c="null" class="btn btn-secondary o_button_attendance_filter">Tất cả Phòng ban/Chức vụ</button></div>';
//                if(self.__parentedParent.recordData.department_all!=false){
//                    JSON.parse(self.__parentedParent.recordData.department_all).forEach(function (item) {
//                        $filterCellInput = $filterCellInput + '<div><button name="'+ item['name'] +'" value="false" type="button" data-id="'
//                        + self.__parentedParent.recordData.id + '" data-department_id_c="'
//                        + item['id'] +'" class="btn btn-secondary o_button_attendance_filter">' + item['name'] + '</button></div>';
//                    });
//                }
//            }else{
//                if(self.__parentedParent.name=="attendance_of_month_compute"){
//                    if(self.__parentedParent.recordData.department_id!=false){
//                        $filterCellInput = $filterCellInput + '&nbsp;' + self.__parentedParent.recordData.department_id.data.display_name
//                                            + '</a><div class="dropdown-menu o_filters_menu_attendance" role="menu">'
//                    }else{
//                        $filterCellInput = $filterCellInput + '&nbsp;Tất cả Phòng ban/Chức vụ</a><div class="dropdown-menu o_filters_menu_attendance" role="menu">'
//                    }
//                    $filterCellInput = $filterCellInput + '<div><button name="all" value="false" type="button" data-id="' + self.__parentedParent.recordData.id + '" data-department_id="null" class="btn btn-secondary o_button_attendance_filter">Tất cả Phòng ban/Chức vụ</button></div>';
//                    if(self.__parentedParent.recordData.department_all!=false){
//                        JSON.parse(self.__parentedParent.recordData.department_all).forEach(function (item) {
//                            $filterCellInput = $filterCellInput + '<div><button name="'+ item['name'] +'" value="false" type="button" data-id="'
//                            + self.__parentedParent.recordData.id + '" data-department_id="'
//                            + item['id'] +'" class="btn btn-secondary o_button_attendance_filter">' + item['name'] + '</button></div>';
//                        });
//                    }
//                }
//            }
//            $filterCellInput =  $filterCellInput + '</div></span></t>';
//            $filterCell.append($filterCellInput);
}
            let $filterCellInput1 = `<div style="display:flex;"><span class="fa fa-filter filter_att"/><select id="attendanceSelect">`;
            if(self.__parentedParent.name=="attendance_of_month_compute" && self.__parentedParent.recordData.department_all!=false){
                $filterCellInput1 += `<option value="false" data-id="${self.__parentedParent.recordData.id}" data-department_id="0">Tất cả Phòng/Ban</option>`;
                JSON.parse(self.__parentedParent.recordData.department_all).forEach(function (item) {
                    $filterCellInput1 += `<option value="false" data-id="${self.__parentedParent.recordData.id}" data-department_id="${item['id']}"`;
                    if(self.__parentedParent.recordData.department_id!=false && item['id']===self.__parentedParent.recordData.department_id.data.id){
                        $filterCellInput1 += `selected >${self.__parentedParent.recordData.department_id.data.display_name}`;
                    }else{
                        $filterCellInput1 += `>${item['name']}`;
                    }
                    $filterCellInput1 += `</option>`;
                });
            }else{
                if(self.__parentedParent.name=="calendar_of_month_compute" && self.__parentedParent.recordData.department_all!=false){
                    $filterCellInput1 += `<option value="false" data-id="${self.__parentedParent.recordData.id}" data-department_id_c="0">Tất cả Phòng/Ban</option>`;
                    JSON.parse(self.__parentedParent.recordData.department_all).forEach(function (item) {
                        $filterCellInput1 += `<option value="false" data-id="${self.__parentedParent.recordData.id}" data-department_id_c="${item['id']}"`;
                        if(self.__parentedParent.recordData.department_id_c!=false && item['id']===self.__parentedParent.recordData.department_id_c.data.id){
                            $filterCellInput1 += `selected>${self.__parentedParent.recordData.department_id_c.data.display_name}`;
                        }else{
                            $filterCellInput1 += `>${item['name']}`;
                        }
                        $filterCellInput1 += `</option>`;
                    });
                }
            }
            $filterCellInput1 += `</select></div>`;

            $filterCell.append($filterCellInput1);
            $searchRow.append($filterCell);

            $thead.append($searchRow);
            const columns=[]
            this.columns.forEach(col=>{
                if(col.attrs['row-level']==1){
                    columns.push(col)
                }
                if(col.attrs['data-title']){
                    var new_col={
                    attrs:{
                            string:col.attrs['data-title'],
                            colspan:col.attrs['colspan']}
                    };
                    columns.push(new_col)
                }
            })
            const $tr = $('<tr>').append(_.map(columns, this._renderHeaderCell.bind(this)));
            $thead.append($tr);
            const columns_2=[]
            this.columns.forEach(col=>{
                if(col.attrs['row-level']==2){
                    col.attrs['rowspan']="1"
                    columns_2.push(col)
                }
            })
            const $tr1 = $('<tr>').append(_.map(columns_2, this._renderHeaderCell.bind(this)));
            $thead.append($tr1);
            return $thead;
        } else {
            var $tr = $('<tr>').append(_.map(this.columns, this._renderHeaderCell.bind(this)));
            if (this.hasSelectors) {
                $tr.prepend(this._renderSelector('th'));
            }

            const $thead = $('<thead>').append($tr);

            return $thead;
        }
    },
     _renderHeaderCell: function (node) {
        const $th = this._super.apply(this, arguments);
        const thClassName = node.attrs.class;
        $th.addClass(thClassName)



        const { rowspan, colspan } = node.attrs;
        if(rowspan)
        {
            $th.attr('rowspan', rowspan)
        }
        else if(colspan){
            if(node.attrs['string']) {
                $th.text(node.attrs['string'])
            }
            $th.text(node.attrs['string'])
            $th.attr('colspan', colspan)
        }
        else if(rowspan==1)
        {

            $th.attr('rowspan', rowspan)
        }



        return $th;
    },

    _renderBodyCell: function (record, node, colIndex, options) {
        var $cell = this._super.apply(this, arguments);
        if (this.state.model === "sea.hr.attendance.month") {
            {
                //            if (colIndex !== 0){
                //                 if(record.data.day_1_soon_or_late != 'false' && colIndex === 1
                //                 || record.data.day_2_soon_or_late != 'false' && colIndex === 2
                //                 || record.data.day_3_soon_or_late != 'false' && colIndex === 3
                //                 || record.data.day_4_soon_or_late != 'false' && colIndex === 4
                //                 || record.data.day_5_soon_or_late != 'false' && colIndex === 5
                //                 || record.data.day_6_soon_or_late != 'false' && colIndex === 6
                //                 || record.data.day_7_soon_or_late != 'false' && colIndex === 7
                //                 || record.data.day_8_soon_or_late != 'false' && colIndex === 8
                //                 || record.data.day_9_soon_or_late != 'false' && colIndex === 9
                //                 || record.data.day_10_soon_or_late != 'false' && colIndex === 10
                //                 || record.data.day_11_soon_or_late != 'false' && colIndex === 11
                //                 || record.data.day_12_soon_or_late != 'false' && colIndex === 12
                //                 || record.data.day_13_soon_or_late != 'false' && colIndex === 13
                //                 || record.data.day_14_soon_or_late != 'false' && colIndex === 14
                //                 || record.data.day_15_soon_or_late != 'false' && colIndex === 15
                //                 || record.data.day_16_soon_or_late != 'false' && colIndex === 16
                //                 || record.data.day_17_soon_or_late != 'false' && colIndex === 17
                //                 || record.data.day_18_soon_or_late != 'false' && colIndex === 18
                //                 || record.data.day_19_soon_or_late != 'false' && colIndex === 19
                //                 || record.data.day_21_soon_or_late != 'false' && colIndex === 21
                //                 || record.data.day_20_soon_or_late != 'false' && colIndex === 20
                //                 || record.data.day_22_soon_or_late != 'false' && colIndex === 22
                //                 || record.data.day_23_soon_or_late != 'false' && colIndex === 23
                //                 || record.data.day_24_soon_or_late != 'false' && colIndex === 24
                //                 || record.data.day_25_soon_or_late != 'false' && colIndex === 25
                //                 || record.data.day_26_soon_or_late != 'false' && colIndex === 26
                //                 || record.data.day_27_soon_or_late != 'false' && colIndex === 27
                //                 || record.data.day_28_soon_or_late != 'false' && colIndex === 28
                //                 || record.data.day_29_soon_or_late != 'false' && colIndex === 29
                //                 || record.data.day_30_soon_or_late != 'false' && colIndex === 30
                //                 || record.data.day_31_soon_or_late != 'false' && colIndex === 31){
                //                    $cell.addClass('color_red');
                //                    $cell[0].setAttribute("title", record.data.day_1_soon_or_late);
                //                    }
                //                }
            }
            switch (colIndex - 1) {
                case 1:
                    if(record.data.day_1_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_1_soon_or_late);
                    }
                    break;
                case 2:
                    if(record.data.day_2_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_2_soon_or_late);
                    }
                    break;
                case 3:
                   if(record.data.day_3_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_3_soon_or_late);
                    }
                    break;
                case 4:
                    if(record.data.day_4_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_4_soon_or_late);
                    }
                    break;
                case 5:
                    if(record.data.day_5_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_5_soon_or_late);
                    }
                    break;
                case 6:
                    if(record.data.day_6_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_6_soon_or_late);
                    }
                    break;
                case 7:
                    if(record.data.day_7_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_7_soon_or_late);
                    }
                    break;
                case 8:
                    if(record.data.day_8_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_8_soon_or_late);
                    }
                    break;
                case 9:
                    if(record.data.day_9_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_9_soon_or_late);
                    }
                    break;
                case 10:
                    if(record.data.day_10_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_10_soon_or_late);
                    }
                    break;
                case 11:
                    if(record.data.day_11_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_11_soon_or_late);
                    }
                    break;
                case 12:
                    if(record.data.day_12_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_12_soon_or_late);
                    }
                    break;
                case 13:
                    if(record.data.day_13_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_13_soon_or_late);
                    }
                    break;
                case 14:
                    if(record.data.day_14_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_14_soon_or_late);
                    }
                    break;
                case 15:
                    if(record.data.day_15_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_15_soon_or_late);
                    }
                    break;
                case 16:
                    if(record.data.day_16_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_16_soon_or_late);
                    }
                    break;
                case 17:
                   if(record.data.day_17_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_17_soon_or_late);
                    }
                    break;
                case 18:
                    if(record.data.day_18_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_18_soon_or_late);
                    }
                    break;
                case 19:
                    if(record.data.day_19_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_19_soon_or_late);
                    }
                    break;
                case 20:
                    if(record.data.day_20_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_20_soon_or_late);
                    }
                    break;
                case 21:
                    if(record.data.day_21_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_21_soon_or_late);
                    }
                    break;
                case 22:
                    if(record.data.day_22_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_22_soon_or_late);
                    }
                    break;
                case 23:
                    if(record.data.day_23_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_23_soon_or_late);
                    }
                    break;
                case 24:
                    if(record.data.day_24_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_24_soon_or_late);
                    }
                    break;
                case 25:
                    if(record.data.day_25_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_25_soon_or_late);
                    }
                    break;
                case 26:
                    if(record.data.day_26_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_26_soon_or_late);
                    }
                    break;
                case 27:
                    if(record.data.day_27_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_27_soon_or_late);
                    }
                    break;
                case 28:
                    if(record.data.day_28_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_28_soon_or_late);
                    }
                    break;
                case 29:
                    if(record.data.day_29_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_29_soon_or_late);
                    }
                    break;
                case 30:
                    if(record.data.day_30_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_30_soon_or_late);
                    }
                    break;
                case 31:
                    if(record.data.day_31_soon_or_late != 'false'){
                        $cell.addClass('color_red');
                        $cell[0].setAttribute("title", record.data.day_31_soon_or_late);
                    }
                    break;
                default:

                    break;
        }

        }
        return $cell;
    },

    _renderEmptyRow: function () {
        var $td = $('<td>&nbsp;</td>').attr('colspan', this._getNumberOfCols() * 10);
        return $('<tr>').append($td);
    },
    _renderRow: function (record, index) {
        var $row = this._super.apply(this, arguments);
        if(this.state.model === "sea.hr.calendar.employee") {
            $row.addClass('o_list_no_open');
            // add click event
            var self = this;
            $row.bind({
                click: function (ev) {
                    if((typeof(ev.target.type)=="undefined" && ev.target.tagName!="LABEL") ){
                        if(ev.target.type!="checkbox"){
                            ev.preventDefault();
                            ev.stopPropagation();
                            rpc.query({
                                     route: '/load/calendar',
                                     params: {
                                         id: record.data.id
                                     }
                                 }).then(function (data) {
                                 });
                            self.do_action({
                                name: _t("Calendar"),
                                type: 'ir.actions.act_window',
                                res_model: 'sea.hr.calendar',
                                view_mode: 'calendar, form',
                                views: [[false, 'calendar'], [false, 'form']],
                                domain: [['employee_multi_id','=', record.data.employee_multi_id.data.id], ['month', '=', record.data.month], ['year', '=', record.data.year]],
                                target: 'current',
                            });
                        }
                    }
                }
            });
        }


//        if (this.__parentedParent.recordData.department_code !== false && this.__parentedParent.recordData.department_code !== record.data.department_code) {
//            $row[0].classList.add('d-none');
////            console.log('this', this.__parentedParent.recordData.department_code)
////            console.log('record', record.data.department_code)
//        }
//        else{ $row[0].classList.remove('d-none');}

        return $row;
    },

    _renderView: function () {
        var def = this._super();

        return def;
    },
    _onAddRecord: function (ev) {
//        // we don't want the browser to navigate to a the # url
//        ev.preventDefault();
//
//        // we don't want the click to cause other effects, such as unselecting
//        // the row that we are creating, because it counts as a click on a tr
//        ev.stopPropagation();
//
//        // but we do want to unselect current row
//        var self = this;
//        this.unselectRow().then(function () {
//            var context = ev.currentTarget.dataset.context;
//            self.trigger_up('add_record', {context: context && [context]}); // TODO write a test, the deferred was not considered
//       });
        return;
    },
    _onKeyDownAddRecord: function(e) {
        switch(e.keyCode) {
            case $.ui.keyCode.ENTER:
                e.stopPropagation();
                e.preventDefault();
                //this._onAddRecord(e);
                break;
        }
    },
});
//========================================================= ---  =====================================//

var AttendanceOne2Many = FieldOne2Many.extend({

     init: function () {
//        console.log('xin chào Khánh nè')
        this._super.apply(this, arguments);
        this.creatingRecord = false;
        var month = this.record.data.month
        var year = this.record.data.year
        // Tạo đối tượng Date biểu diễn ngày cuối cùng trong tháng
        var lastDayOfMonth = new Date(year, month, 0);
        // Lấy số ngày trong tháng
        var daysInMonth = lastDayOfMonth.getDate();

        const weekdays = ['Chủ nhật', 'Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy'];
        for (var i = 1; i <= daysInMonth; i++) {
            const date = new Date(this.record.data.year + '-' + this.record.data.month + '-' + i);
            // Lấy thứ của ngày đó
            const dayOfWeek = date.getDay();
            const dayOfWeekName = weekdays[dayOfWeek];
            this.get_day(i,dayOfWeekName)
            }

    },
    get_day: function(day, thu){
        switch (day) {
            case 1:
                return this.field.views.tree.fields.day_1.string = thu;
                break;
            case 2:
                return this.field.views.tree.fields.day_2.string = thu;
                break;
            case 3:
                return this.field.views.tree.fields.day_3.string = thu;
                break;
            case 4:
                return this.field.views.tree.fields.day_4.string = thu;
                break;
            case 5:
                return this.field.views.tree.fields.day_5.string = thu;
                break;
            case 6:
                return this.field.views.tree.fields.day_6.string = thu;
                break;
            case 7:
                return this.field.views.tree.fields.day_7.string = thu;
                break;
            case 8:
                return this.field.views.tree.fields.day_8.string = thu;
                break;
            case 9:
                return this.field.views.tree.fields.day_9.string = thu;
                break;
            case 10:
                return this.field.views.tree.fields.day_10.string = thu;
                break;
            case 11:
                return this.field.views.tree.fields.day_11.string = thu;
                break;
            case 12:
                return this.field.views.tree.fields.day_12.string = thu;
                break;
            case 13:
                return this.field.views.tree.fields.day_13.string = thu;
                break;
            case 14:
                return this.field.views.tree.fields.day_14.string = thu;
                break;
            case 15:
                return this.field.views.tree.fields.day_15.string = thu;
                break;
            case 16:
                return this.field.views.tree.fields.day_16.string = thu;
                break;
            case 17:
                return this.field.views.tree.fields.day_17.string = thu;
                break;
            case 18:
                return this.field.views.tree.fields.day_18.string = thu;
                break;
            case 19:
                return this.field.views.tree.fields.day_19.string = thu;
                break;
            case 20:
                return this.field.views.tree.fields.day_20.string = thu;
                break;
            case 21:
                return this.field.views.tree.fields.day_21.string = thu;
                break;
            case 22:
                return this.field.views.tree.fields.day_22.string = thu;
                break;
            case 23:
                return this.field.views.tree.fields.day_23.string = thu;
                break;
            case 24:
                return this.field.views.tree.fields.day_24.string = thu;
                break;
            case 25:
                return this.field.views.tree.fields.day_25.string = thu;
                break;
            case 26:
                return this.field.views.tree.fields.day_26.string = thu;
                break;
            case 27:
                return this.field.views.tree.fields.day_27.string = thu;
                break;
            case 28:
                return this.field.views.tree.fields.day_28.string = thu;
                break;
            case 29:
                return this.field.views.tree.fields.day_29.string = thu;
                break;
            case 30:
                return this.field.views.tree.fields.day_30.string = thu;
                break;
            case 31:
                return this.field.views.tree.fields.day_31.string = thu;
                break;
            default:
                return false;
                break;
        }
    },
    _getRenderer: function () {
        if (this.view.arch.tag === 'tree') {
            return AttendanceRenderer;
        }
        return this._super.apply(this, arguments);
    },
    _openFormDialog: function (params) {
//            var context = this.record.getContext(_.extend({},
//                this.recordParams,
//                { additionalContext: params.context }
//            ));
//            if (this.mode!=="readonly"){
//            this.trigger_up('open_one2many_record', _.extend(params, {
//                domain: this.record.getDomain(this.recordParams),
//                context: context,
//                field: this.field,
//                fields_view: this.attrs.views && this.attrs.views.form,
//                parentID: this.value.id,
//                viewInfo: this.view,
//                deletable: this.activeActions.delete,
//            }));
//        }
        return;
    }

});
fieldRegistry.add('attendance_one2many', AttendanceOne2Many);

//========================================================= ---  =====================================//

//widget calendar
function dateToServer (date) { return date.clone().utc().locale('en').format('YYYY-MM-DD HH:mm:ss');}
var AttendanceCalendarController = AbstractController.extend({
    custom_events: _.extend({}, AbstractController.prototype.custom_events, {
        changeDate: '_onChangeDate',
        changeFilter: '_onChangeFilter',
        dropRecord: '_onDropRecord',
        next: '_onNext',
        openCreate: '_onOpenCreate',
        openEvent: '_onOpenEvent',
        prev: '_onPrev',
        quickCreate: '_onQuickCreate',
        toggleFullWidth: '_onToggleFullWidth',
        updateRecord: '_onUpdateRecord',
        viewUpdated: '_onViewUpdated',
    }),
    /**
     * @override
     * @param {Widget} parent
     * @param {AbstractModel} model
     * @param {AbstractRenderer} renderer
     * @param {Object} params
     */
    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);
        this.current_start = null;
        this.displayName = params.displayName;
        this.quickAddPop = params.quickAddPop;
        this.disableQuickCreate = params.disableQuickCreate;
        this.eventOpenPopup = params.eventOpenPopup;
        this.formViewId = params.formViewId;
        this.readonlyFormViewId = params.readonlyFormViewId;
        this.mapping = params.mapping;
        this.context = params.context;
        // The quickCreating attribute ensures that we don't do several create
        this.quickCreating = false;
    },
    /**
     * Overrides to unbind handler on the control panel mobile 'Today' button.
     *
     * @override
     */
    destroy: function () {
        this._super.apply(this, arguments);
        if (this.$todayButton) {
            this.$todayButton.off();
        }
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     * @returns {string}
     */
    getTitle: function () {
        return this.get('title');
    },
    /**
     * Render the buttons according to the CalendarView.buttons template and
     * add listeners on it. Set this.$buttons with the produced jQuery element
     *
     * @param {jQueryElement} [$node] a jQuery node where the rendered buttons
     *   should be inserted. $node may be undefined, in which case the Calendar
     *   inserts them into this.options.$buttons or into a div of its template
     */
    renderButtons: function ($node) {
        var self = this;
        this.$buttons = $(qweb.render('CalendarView.buttons', {
            isMobile: config.device.isMobile,
        }));
        this.$buttons.on('click', 'button.o_calendar_button_new', function () {
            self.trigger_up('switch_view', {view_type: 'form'});
        });

        _.each(['prev', 'today', 'next'], function (action) {
            self.$buttons.on('click', '.o_calendar_button_' + action, function () {
                self._move(action);
            });
        });
        _.each(['day', 'week', 'month'], function (scale) {
            self.$buttons.on('click', '.o_calendar_button_' + scale, function () {
                self.model.setScale(scale);
                self.reload();
            });
        });

        this.$buttons.find('.o_calendar_button_' + this.mode).addClass('active');

        if ($node) {
            this.$buttons.appendTo($node);
        } else {
            this.$('.o_calendar_buttons').replaceWith(this.$buttons);
        }
    },
    /**
     * In mobile, we want to display a special 'Today' button on the bottom
     * right corner of the control panel. This is the pager area, and as there
     * is no pager in Calendar views, we fool the system by defining a fake
     * pager (which is actually our button) such that it will be inserted in the
     * desired place.
     *
     * @todo get rid of this hack once the ControlPanel layout will be reworked
     *
     * @param {jQueryElement} $node the button should be appended to this
     *   element to be displayed in the bottom right corner of the control panel
     */
    renderPager: function ($node) {
        if (config.device.isMobile) {
            this.$todayButton = $(qweb.render('CalendarView.TodayButtonMobile'));
            this.$todayButton.on('click', this._move.bind(this, 'today'));
            $node.append(this.$todayButton);
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Move to the requested direction and reload the view
     *
     * @private
     * @param {string} to either 'prev', 'next' or 'today'
     * @returns {Deferred}
     */
    _move: function (to) {
        this.model[to]();
        return this.reload();
    },
    /**
     * @private
     * @param {Object} record
     * @param {integer} record.id
     * @returns {Deferred}
     */
    _updateRecord: function (record) {
        return this.model.updateRecord(record).always(this.reload.bind(this));
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {OdooEvent} event
     */
    _onChangeDate: function (event) {
        var modelData = this.model.get();
        if (modelData.target_date.format('YYYY-MM-DD') === event.data.date.format('YYYY-MM-DD')) {
            // When clicking on same date, toggle between the two views
            switch (modelData.scale) {
                case 'month': this.model.setScale('week'); break;
                case 'week': this.model.setScale('day'); break;
                case 'day': this.model.setScale('month'); break;

            }
        } else if (modelData.target_date.week() === event.data.date.week()) {
            // When clicking on a date in the same week, switch to day view
            this.model.setScale('day');
        } else {
            // When clicking on a random day of a random other week, switch to week view
            this.model.setScale('week');
        }
        this.model.setDate(event.data.date);
        this.reload();
    },
    /**
     * @private
     * @param {OdooEvent} event
     */
    _onChangeFilter: function (event) {
        if (this.model.changeFilter(event.data) && !event.data.no_reload) {
            this.reload();
        }
    },
    /**
     * @private
     * @param {OdooEvent} event
     */
    _onDropRecord: function (event) {
        this._updateRecord(_.extend({}, event.data, {
            'drop': true,
        }));
    },
    /**
     * @private
     * @param {OdooEvent} event
     */
    _onNext: function (event) {
        event.stopPropagation();
        this._move('next');
    },
    /**
     * @private
     * @param {OdooEvent} event
     */
    _onOpenCreate: function (event) {
        if(this.modelName === "sea.hr.calendar") {
            rpc.query({
                 route: '/load/check_add_line_calendar',
                 params: {}
                }).then(function (data) {
                if(data === true){
                    var self = this;
                    if (this.model.get().scale === "month") {
                        event.data.allDay = true;
                    }
                    var data = this.model.calendarEventToRecord(event.data);

                    var context = _.extend({}, this.context, event.options && event.options.context);
                    context.default_name = data.name || null;
                    context['default_' + this.mapping.date_start] = data[this.mapping.date_start] || null;
                    if (this.mapping.date_stop) {
                        context['default_' + this.mapping.date_stop] = data[this.mapping.date_stop] || null;
                    }
                    if (this.mapping.date_delay) {
                        context['default_' + this.mapping.date_delay] = data[this.mapping.date_delay] || null;
                    }
                    if (this.mapping.all_day) {
                        context['default_' + this.mapping.all_day] = data[this.mapping.all_day] || null;
                    }

                    for (var k in context) {
                        if (context[k] && context[k]._isAMomentObject) {
                            context[k] = dateToServer(context[k]);
                        }
                    }

                    var options = _.extend({}, this.options, event.options, {
                        context: context,
                        title: _.str.sprintf(_t('Create: %s'), (this.displayName || this.renderer.arch.attrs.string))
                    });

                    if (this.quick != null) {
                        this.quick.destroy();
                        this.quick = null;
                    }

                    if (!options.disableQuickCreate && !event.data.disableQuickCreate && this.quickAddPop) {
                        this.quick = new QuickCreate(this, true, options, data, event.data);
                        this.quick.open();
                        this.quick.opened(function () {
                            self.quick.focus();
                        });
                        return;
                    }

                    var title = _t("Create");
                    if (this.renderer.arch.attrs.string) {
                        title += ': ' + this.renderer.arch.attrs.string;
                    }
                    if (this.eventOpenPopup) {
                        new dialogs.FormViewDialog(self, {
                            res_model: this.modelName,
                            context: context,
                            title: title,
                            view_id: this.formViewId || false,
                            disable_multiple_selection: true,
                            on_saved: function () {
                                if (event.data.on_save) {
                                    event.data.on_save();
                                }
                                self.reload();
                            },
                        }).open();
                    } else {
                        this.do_action({
                            type: 'ir.actions.act_window',
                            res_model: this.modelName,
                            views: [[this.formViewId || false, 'form']],
                            target: 'current',
                            context: context,
                        });
                    }
                }
                }.bind(this));
        }
    },

    /**
     * @private
     * @param {OdooEvent} event
     */
    _onOpenEvent: function (event) {
        var self = this;
        var id = event.data._id;
        id = id && parseInt(id).toString() === id ? parseInt(id) : id;

        if (!this.eventOpenPopup) {
            this._rpc({
                model: self.modelName,
                method: 'get_formview_id',
                //The event can be called by a view that can have another context than the default one.
                args: [[id], event.context || self.context],
            }).then(function (viewId) {
                self.do_action({
                    type:'ir.actions.act_window',
                    res_id: id,
                    res_model: self.modelName,
                    views: [[viewId || false, 'form']],
                    target: 'current',
                    context: event.context || self.context,
                });
            });
            return;
        }

        var open_dialog = function (readonly) {
            var options = {
                res_model: self.modelName,
                res_id: id || null,
                context: event.context || self.context,
                readonly: readonly,
                title: _t("Open: ") + _.escape(event.data.title),
                on_saved: function () {
                    if (event.data.on_save) {
                        event.data.on_save();
                    }
                    self.reload();
                },
            };
            if (readonly) {
                if (self.readonlyFormViewId) {
                    options.view_id = parseInt(self.readonlyFormViewId);
                }
                options.buttons = [
                    {
                        text: _t("Edit"),
                        classes: 'btn-primary',
                        close: true,
                        click: function () { open_dialog(false); }
                    },
                    {
                        text: _t("Delete"),
                        click: function () {
                            Dialog.confirm(this, _t("Are you sure you want to delete this record ?"), {
                                confirm_callback: function () {
                                    self.model.deleteRecords([id], self.modelName)
                                        .then(function () {
                                            self.dialog.destroy();
                                            self.reload();
                                        });
                                }
                            });
                        },
                    },
                    {text: _t("Close"), close: true}
                ];
            } else if (self.formViewId) {
                options.view_id = parseInt(self.formViewId);
            }
            self.dialog = new dialogs.FormViewDialog(self, options).open();
        };
        open_dialog(true);
    },
    /**
     * @private
     * @param {OdooEvent} event
     */
    _onPrev: function () {
        event.stopPropagation();
        this._move('prev');
    },

    /**
     * Handles saving data coming from quick create box
     *
     * @private
     * @param {OdooEvent} event
     */
    _onQuickCreate: function (event) {
        var self = this;
        if (this.quickCreating) {
            return;
        }
        this.quickCreating = true;
        this.model.createRecord(event)
            .then(function () {
                self.quick.destroy();
                self.quick = null;
                self.reload();
            })
            .fail(function (error, errorEvent) {
                // This will occurs if there are some more fields required
                // Preventdefaulting the error event will prevent the traceback window
                errorEvent.preventDefault();
                event.data.options.disableQuickCreate = true;
                event.data.data.on_save = self.quick.destroy.bind(self.quick);
                self._onOpenCreate(event.data);
            })
            .always(function () {
                self.quickCreating = false;
            });
    },
    /**
     * Called when we want to open or close the sidebar.
     *
     * @private
     */
    _onToggleFullWidth: function () {
        this.model.toggleFullWidth();
        this.reload();
    },
    /**
     * @private
     * @param {OdooEvent} event
     */
    _onUpdateRecord: function (event) {
        this._updateRecord(event.data);
    },
    /**
     * The internal state of the calendar (mode, period displayed) has changed,
     * so update the control panel buttons and breadcrumbs accordingly.
     *
     * @private
     * @param {OdooEvent} event
     */
    _onViewUpdated: function (event) {
        this.mode = event.data.mode;
        if (this.$buttons) {
            this.$buttons.find('.active').removeClass('active');
            this.$buttons.find('.o_calendar_button_' + this.mode).addClass('active');
        }
        this.set({title: this.displayName + ' (' + event.data.title + ')'});
    },
});
var CalendarCalendarView = CalendarView.extend({
    config: _.extend({}, CalendarView.prototype.config, {
        Controller: AttendanceCalendarController,
    }),
});
viewRegistry.add('calendar_calendar', CalendarCalendarView);

//========================================================= ---  =====================================//

var FormRenderer = require('web.FormRenderer');
var FormController = require('web.FormController');
var FormView = require('web.FormView');

var CalendarFormController = FormController.extend({

    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);

        this.actionButtons = params.actionButtons;
        this.disableAutofocus = params.disableAutofocus;
        this.footerToButtons = params.footerToButtons;
        this.defaultButtons = params.defaultButtons;
        this.hasSidebar = params.hasSidebar;
        this.toolbarActions = params.toolbarActions || {};

//        console.log('tiếp tục cho view form calendar')

    },
    /**
     * Settings view should always be in edit mode, so we have to override
     * default behaviour
     *
     * @override
     */

     /**
     * Render buttons for the control panel.  The form view can be rendered in
     * a dialog, and in that case, if we have buttons defined in the footer, we
     * have to use them instead of the standard buttons.
     *
     * @override method from AbstractController
     * @param {jQueryElement} $node
     */
    renderButtons: function($node) {
        this._super.apply(this, arguments);
        var self = this
        if(this.modelName === "sea.hr.calendar") {
            rpc.query({
                 route: '/load/check_add_line_calendar',
                 params: {}
                }).then(function (data) {
                if(data === false){
                    //Tìm đến nút Edit và ẩn nó
                    this.$buttons.find('.o_form_button_edit').hide();
                }}.bind(this));}
    },
    renderSidebar: function ($node) {
        this._super.apply(this, arguments);
        if(this.modelName === "sea.hr.calendar") {
            rpc.query({
                route: '/load/check_add_line_calendar',
                params: {}
                }).then(function (data) {
                    if(data === false){
                        var sidebar = document.querySelector('.o_cp_sidebar');
                        if (sidebar) {
                            sidebar.style.display = 'none';
                        }
                    }
                }.bind(this));}
    },
});
var CalendarFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: CalendarFormController,
        Renderer: FormRenderer,
    }),
});

viewRegistry.add('calendar_calendar_form_view', CalendarFormView);

var FilterControllerMixin = {
    /**
     * @override
     */
    init: function (parent, model, renderer, params) {
        //this.importEnabled = params.importEnabled;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Adds an event listener on the import button.
     *
     * @private
     */
    _bindFilter: function () {
        var self = this;
        $(document).on('change', '#attendanceSelect', function () {
            var selectedValue = this.value;
            var selectedOption = this.options[this.selectedIndex];
            var dataId = selectedOption.getAttribute('data-department_id');
            var fields = {};
            if(selectedOption.getAttribute('data-department_id_c')!== null){
                fields['department_id_c'] = selectedOption.getAttribute('data-department_id_c')==0?null:selectedOption.getAttribute('data-department_id_c');
            }else{
                if(selectedOption.getAttribute('data-department_id')!== null){
                    fields['department_id'] = selectedOption.getAttribute('data-department_id')==0?null:selectedOption.getAttribute('data-department_id');
                }
            }
            rpc.query({
                    model: 'sea.hr.attendance',
                    method: 'write',
                    args: [[parseInt(selectedOption.getAttribute('data-id'))], fields],
                })
                .done(function(result) {
//                    console.log('done');
                    self.trigger_up('reload');
//                    self.reload();
                }).fail(function(unused, event) {
                    console.log('fail');
            });
        });
        $(document).one('click', '.o_button_attendance_filter', function (event) {
            var fields = {};
            if($(this).data('department_id_c')!== undefined){
                fields['department_id_c'] = $(this).data('department_id_c');
            }else{
                if($(this).data('department_id')!== undefined){
                    fields['department_id'] = $(this).data('department_id');
                }
            }
            rpc.query({
                    model: 'sea.hr.attendance',
                    method: 'write',
                    args: [[parseInt($(this).data('id'))], fields],
                })
                .done(function(result) {
//                    console.log('done');
                    self.trigger_up('reload');
//                    self.reload();
                }).fail(function(unused, event) {
                    console.log('fail');
            });
        });
    }
};

var AttendanceFormController = FormController.extend({

    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);
        var self = this;
    },
    renderButtons: function($node) {
    this._super.apply(this, arguments);
    var self = this
    if(this.modelName === "sea.hr.attendance" || this.modelName === "sea.hr.attendance.details") {
        rpc.query({
             route: '/load/check_group',
             params: {}
            }).then(function (data) {
            if(data === 1 || data === 0){
                //Tìm đến nút Edit và ẩn nó
                this.$buttons.find('.o_form_button_edit').hide();
            }}.bind(this));}
    },
});
var AttendanceFormViewHideEdit = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: AttendanceFormController,
    }),
});

viewRegistry.add('attendance_form_view_hide_edit', AttendanceFormViewHideEdit);



//widget view tree
var ListController = require('web.ListController');
var AttendanceDetailsViolationListController = ListController.extend({
//    events: _.extend({}, ListController.prototype.events, {
//        'click tbody td.o_data_cell': '_onRowClicked',
//        'submit .o_data_row form': '_onFormSubmit',
//    }),

    start: function () {
        var self = this;
        this._super.apply(this, arguments);
//        this.$el.on('click', '.o_data_row', function(event) {
//            console.log("this: ", self);
//            // Truy xuất giá trị data-id từ dòng được click
//            var recordID = $(self).data('id');
//
//            // In ra console để kiểm tra
//            console.log('Clicked on row with ID:', recordID);
//
//            // Thực hiện các xử lý khác với recordID ở đây
//        });
//        , this._onRowClicked.bind(this));
    },

//    _onRowClicked: function (ev) {
//        var self = this;
//        console.log('self: ', self);
//        console.log('ev: ', ev);
//        var $row = $(ev.currentTarget);
//        console.log("row: ", $row)
//        var recordID = $row.data('id');
//
//        console.log('Clicked on row with ID:', recordID);
//
//        // Thay thế nội dung của ô dữ liệu bằng một input
////        $row.find('.o_data_cell').html('<input type="text" name="your_input" class="form-control"/><button type="submit" class="btn btn-primary">Submit</button>');
//    },

//    _onFormSubmit: function (ev) {
//        ev.preventDefault();
//        var $form = $(ev.currentTarget);
//        var $row = $form.closest('.o_data_row');
//        var recordID = $row.data('id');
//        var inputValue = $form.find('input[name="your_input"]').val();
//
//        console.log('Submitted input value for row with ID:', recordID, 'Value:', inputValue);
//
//        // Thực hiện các xử lý lưu trữ dữ liệu ở đây
//    },
});
var AttendanceDetailsViolationListRenderer = ListRenderer.extend({
    events: {
        'click tbody tr': '_onRowClicked',
    },
    _onRowClicked: function (event) {
        var self = this;
        var $row = $(event.currentTarget);
        // Sử dụng phương thức index() để lấy vị trí của dòng trong danh sách
        var rowIndex = $row.index();
        var recordId = self.state.res_ids[rowIndex];
//        console.log("recordId: ", recordId, self.state.data[rowIndex].data.note);

        // Tạo id và giá trị động cho input
        var inputId = 'inputValue_' + recordId;
        if(self.state.data[rowIndex].data.note!=false){
            var vals = self.state.data[rowIndex].data.note;
        }
        // Tạo modal
        var modalContent = `
            <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title" id="myModalLabel">Nhập ghi chú ngày ${self.state.data[rowIndex].data.day}/${self.state.data[rowIndex].data.month}/${self.state.data[rowIndex].data.year}</h4>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <input type="text" id="${inputId}" class="form-control" ${vals ? `value="${vals}"` : ''} placeholder="Nhập ghi chú...">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Đóng</button>
                            <button type="button" class="btn btn-primary" id="submitBtn">Lưu</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Thêm modal vào body
        $('body').append(modalContent);

        // Hiển thị modal
        $('#myModal').modal('show');

        // Bắt sự kiện khi nút submit được click
        $('#submitBtn').on('click', function () {
//            console.log('Submitted input value for record with ID:', recordId, 'Value:', $('#' + inputId).val());

            // Thực hiện các xử lý lưu trữ dữ liệu ở đây
            var fields = {};
            if(self.state.data[rowIndex].data.note!== $('#' + inputId).val()){
                fields['note'] = $('#' + inputId).val();
                fields['explanation_approved'] = false;
                rpc.query({
                        model: 'sea.hr.attendance.details',
                        method: 'write',
                        args: [[parseInt(recordId)], fields],
                    })
                    .done(function(result) {
                        console.log('done');
                        self.trigger_up('reload');
                    }).fail(function(unused, event) {
                        console.log('fail');
                    });
            }
            // Đóng modal sau khi xử lý
            $('#myModal').modal('hide');
        });
        // Xóa modal khi nó đã được đóng
        $('#myModal').on('hidden.bs.modal', function (e) {
            $(this).remove(); // hoặc $(this).detach();
        });
        console.log('vals: ', vals);
    },
});
var AttendanceDetailsViolationListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: AttendanceDetailsViolationListController,
        Renderer: AttendanceDetailsViolationListRenderer,
    }),
});

viewRegistry.add('attendance_details_violation_view', AttendanceDetailsViolationListView);

//========================================================= ---  =====================================//


//widget view tree
var AttendanceDetailsApprovedListController = ListController.extend({
    start: function () {
        var self = this;
        this._super.apply(this, arguments);
    },
});
var AttendanceDetailsApprovedListRenderer = ListRenderer.extend({
    _renderHeader: function () {
        var $header = this._super.apply(this, arguments); // Tạo một th mới
        var $newHeader = $('<th>');

        // Thêm th vào cuối cùng trong ttr
        $header.find('tr').append($newHeader);
        return $header;
        },
    _renderFooter: function () {
        var $footer = this._super.apply(this, arguments);

        // Tạo một td mới
        var $newFooterCell = $('<td>');

        // Thêm td vào cuối cùng trong tr của tfoot
        $footer.find('tr').append($newFooterCell);

        return $footer;
    },
    _renderRow: function (record, index) {
        var $row = this._super.apply(this, arguments);
//        console.log("record: ", record);
        // Lấy id của dòng
        var recordID = record.res_id; // Sử dụng res_id hoặc cách lấy phù hợp với mô hình dữ liệu của bạn

        // Thêm data-id cho dòng
        $row.attr('data-id', recordID);
        $row.attr('data-value', record.data.explanation_approved);

        // Thêm sự kiện click vào dòng
        $row.on('click', this._onRowClicked.bind(this, recordID));
        var text = 'Approved';
        if(record.data.explanation_approved!=false){
            var text = 'UnApproved';
        }
        // Tạo nút (button) và thêm vào ô cuối cùng của dòng
        var $buttonCell = $('<td>');
        var $button = $('<button>')
            .text(text)
            .addClass('btn btn-primary o_edit_button attendance_button')
            .on('click', this._onButtonClick.bind(this, recordID, record.data.explanation_approved)); // Gắn sự kiện click cho nút

        $buttonCell.append($button);
        $row.append($buttonCell);

        return $row;
    },

    _onButtonClick: function (recordID, value) {
        var self = this;
//        console.log('Button clicked for row with ID:', recordID, value);
        var fields = {};
        if(value==false){
            fields['explanation_approved'] = true;
        }else{
            fields['explanation_approved'] = false;
        }
        rpc.query({
            model: 'sea.hr.attendance.details',
            method: 'write',
            args: [[parseInt(recordID)], fields],
        })
        .done(function(result) {
            console.log('done');
            self.trigger_up('reload');
        }).fail(function(unused, event) {
            console.log('fail');
        });
        // Thực hiện các xử lý khác với recordID ở đây
    },

});
var AttendanceDetailsApprovedListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: AttendanceDetailsApprovedListController,
        Renderer: AttendanceDetailsApprovedListRenderer,
    }),
});

viewRegistry.add('attendance_details_approved_view', AttendanceDetailsApprovedListView);

//========================================================= ---  =====================================//

});
