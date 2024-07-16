
odoo.define('seatek_hr_appraisal.appraisal_user', function (require) {
// The goal of this file is to contain JS hacks related to allowing
// section and note on sale order and invoice.

// [UPDATED] now also allows configuring products on sale order.

"use strict";
var pyUtils = require('web.py_utils');
var core = require('web.core');
var _t = core._t;
var FieldChar = require('web.basic_fields').FieldChar;
var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
var FieldMany2One = require('web.relational_fields').FieldMany2One;

var AbstractField = require('web.AbstractField');
var fieldRegistry = require('web.field_registry');
var FieldText = require('web.basic_fields').FieldText;
var ListRenderer = require('web.ListRenderer');
var session = require('web.session');
var field_utils = require('web.field_utils');
var dom = require('web.dom');

var FIELD_CLASSES = {
    float: 'o_list_number',
    integer: 'o_list_number',
    monetary: 'o_list_number',
    text: 'o_list_text',
};

var new_columns=[];
var AppraisalUsers = ListRenderer.extend({
    events: _.extend({}, ListRenderer.prototype.events, {
        'click tbody td.o_data_cell': '_onCellClick',
        'keydown .o_field_x2many_list_row_add a': '_onKeyDownAddRecord',
        'click .o_field_x2many_list_row_add a': '_onAddRecord',
    }),
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        var self=this;
        if(this.state.model=='hr.survey.user.input' || this.state.model=='hr.appraisal'){
            this.addCreateLine = true;
        }
        if(this.state.model=='hr.survey.user.input.line'){
            this.addCreateLine = false;
        }

    },
    _onKeyDown(event){
     },
     _onSortColumn: function (event){
        return;
     },
    _processColumns(columnInvisibleFields) {
        this._super.apply(this, arguments);
        var self = this;
        this.temp_columns=[...this.columns];
        let column=0
        let current_user=session.uid;

        if(this.state.model=='hr.survey.user.input.line'){
            if(this.temp_columns){
            }
            let columns=[];
            if (this.arch.attrs?.pages=='kpis'){
                columns.push(this.columns[column]);
                column=1;
            }
            else if (this.arch.attrs?.pages=='seacorp'){
                columns.push(this.columns[column]);
                column=1;
            }
            //If manager , manager user can edit title
            let modifiers={readonly:true};
            if((this.__parentedParent.recordData.manager_user_id_compute ==current_user || this.__parentedParent.recordData.user_id_compute ==current_user  )&& this.state.data[0].data?.enable_edit_percentage){
                modifiers={readonly:false};
            }
            this.temp_columns[column].attrs.modifiers=modifiers;
            columns.push(this.columns[column]);
            if(this.state.data){
                if (this.columns[column+1].attrs.name=="percentage"){
                    if(this.state.data){
                        if(this.state.data.length>0){
                            //If manager , manager user can edit percentage
                            if (this.state.data[0].data?.enable_edit_percentage){
                                let modifiers={readonly:true};
                                    if(this.__parentedParent.recordData.manager_user_id_compute  ==current_user || this.__parentedParent.recordData.user_id_compute ==current_user  ){
                                        modifiers={readonly:false};
                                    }
                                this.temp_columns[column+1].attrs.modifiers=modifiers;
                                columns.push(this.temp_columns[column+1]);
                            }
                        }
                        if (this.arch.attrs?.pages=='kpis'){
                            column=2;
                        }else if (this.arch.attrs?.pages=='seacorp'){
                            column=2;
                        }
                        else{
                            column=1;
                        }
                    }
                }

                this.hasSelectors=false;
//                if(this.__parentedParent.recordData.manager_user_id_compute == this.__parentedParent.recordData.smanager_user_id_compute ==current_user){
//                    columns.push(this.temp_columns[column+1]);
//                    columns.push(this.temp_columns[column+2]);
//                    columns.push(this.temp_columns[column+3]);
//                    columns.push(this.temp_columns[column+4]);
//                    columns.push(this.temp_columns[column+5]);
//                    columns.push(this.temp_columns[column+6]);
//                }
                if(this.__parentedParent.recordData?.smanager_user_id_compute ==current_user){
                    if(this.arch.attrs.general!="True")
                    {
                        columns.push(this.temp_columns[column+5]);
                        columns.push(this.temp_columns[column+6]);
                        columns.push(this.temp_columns[column+1]);
                    }
                    else{
                        columns.push(this.temp_columns[column+6]);
                    }



                    columns.push(this.temp_columns[column+2]);
                    //columns.push(this.temp_columns[column+3]);
                    columns.push(this.temp_columns[column+4]);
                    columns.push(this.temp_columns[column+13]);

                }
                else if(this.__parentedParent.recordData?.manager_user_id_compute==current_user){
                    if(this.arch.attrs.general!="True")
                    {
                        columns.push(this.temp_columns[column+3]);
                        columns.push(this.temp_columns[column+4]);
                        columns.push(this.temp_columns[column+1]);
                        columns.push(this.temp_columns[column+2]);
                    }
                    else{
                        columns.push(this.temp_columns[column+2]);
                        columns.push(this.temp_columns[column+4]);
                    }

                    //columns.push(this.temp_columns[column+5]);
                    columns.push(this.temp_columns[column+6]);
                    columns.push(this.temp_columns[column+13]);
                }
                else if(this.__parentedParent.recordData?.colleague_user_id_compute ==current_user){

                    if(this.arch.attrs.general!="True")
                    {
                        columns.push(this.temp_columns[column+7]);
                    }
                    columns.push(this.temp_columns[column+8]);
                }
                else if(this.__parentedParent.recordData?.colleague2_user_id_compute ==current_user){
                        if(this.arch.attrs.general!="True")
                        {
                            columns.push(this.temp_columns[column+9]);
                        }
                        columns.push(this.temp_columns[column+10]);
                }
                else if(this.__parentedParent.recordData?.colleague3_user_id_compute ==current_user){
                        if(this.arch.attrs.general!="True")
                        {
                            columns.push(this.temp_columns[column+11]);
                        }
                        columns.push(this.temp_columns[column+12]);
                }
                else if(this.__parentedParent.recordData.user_id_compute){

                    if(this.__parentedParent.recordData.user_id_compute==current_user){
                        if(this.arch.attrs.general!="True")
                        {
                            columns.push(this.temp_columns[column+1]);
                            columns.push(this.temp_columns[column+2]);
                            columns.push(this.temp_columns[column+3]);
                        }
                        else
                        {
                            columns.push(this.temp_columns[column+2]);
                        }


                        columns.push(this.temp_columns[column+4]);
                        columns.push(this.temp_columns[column+5]);
                        columns.push(this.temp_columns[column+6]);
                    }
                }
                else if(this.__parentedParent.attrs.options.HDDG==true){
                    if(this.arch.attrs.general!="True")
                    {
                       columns.push(this.temp_columns[column+1]);
                       columns.push(this.temp_columns[column+2]);
                    }
                    else
                    {
                        columns.push(this.temp_columns[column+1]);
                    }
                    columns.push(this.temp_columns[column+3]);
                    columns.push(this.temp_columns[column+4]);
                    columns.push(this.temp_columns[column+5]);
//                    columns.push(this.temp_columns[column+6]);
//                    if(this.temp_columns[column+7]){
//                    columns.push(this.temp_columns[column+7]);
//                    }

//                    columns.push(this.temp_columns[column+8]);
//                    columns.push(this.temp_columns[column+8]);
//                    columns.push(this.temp_columns[column+9]);
//                    if (this.temp_columns[column+6]){
//
//                        if(this.temp_columns[column+6].attrs.name!="summary_level")
//                        {
//                            columns.push(this.temp_columns[column+6]);
//                        }
//                    }
                    if (this.temp_columns[column+6]){

                        if(this.temp_columns[column+6].attrs.name!="summary_level")
                        {
                            columns.push(this.temp_columns[column+6]);
                        }
                    }
//                    if(this.temp_columns[column+7]){
//                        columns.push(this.temp_columns[column+7]);
//                    }
                    if (this.temp_columns[column+7]){
                        if(this.temp_columns[column+7].attrs.name!="summary_level")
                        {
                            columns.push(this.temp_columns[column+7]);
                        }
                    }
                    if (this.temp_columns[column+8]){
                        if(this.temp_columns[column+8].attrs.name!="summary_level")
                        {
                            columns.push(this.temp_columns[column+8]);
                        }
                    }
                    if (this.temp_columns[column+9]){
                        if(this.temp_columns[column+9].attrs.name!="summary_level")
                        {
                            columns.push(this.temp_columns[column+9]);
                        }
                    }

                }
            }
            this.columns=columns;
        }
//        else if (this.state.model=='hr.survey.user.input')
//        {
//
//            let columns=[];
//
//            this.temp_columns.forEach(index=>{
//                if (index.tag!='p'){
//                    columns.push(index);
//                }
//            })
//
//            this.columns=columns;
//        }

    },
    _renderHeader: function (isGrouped) {
        if(this.arch.attrs.condition === 'tree') {
            const $thead = $('<thead>');
            $thead.addClass('dexuat_sau_dgns_thead');
//            for(let index = 1; index <= 2; index++) {
//                const filteredColumns = _.filter(this.columns, column => +column.attrs['row-level'] === index)
//                const $tr = $('<tr>').append(_.map(filteredColumns, this._renderHeaderCell.bind(this)));
//                $thead.append($tr);
//            }
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

        //if(node.attrs['data-title'] === 'th-title' ) return;
        let summary_level = 0;
        summary_level=record.data.summary_level;
        const isFieldNumber = node.attrs.class === 'o_field_value_number';
        const editClass = record.data.enable_edit_title ? ' edit' : '';
        var tdClassName = colIndex ? 'o_data_cell' : `o_data_cell level-${summary_level} ${editClass}`;
        if (node.tag === 'button') {
            tdClassName += ' o_list_button';
        } else if (node.tag === 'field') {
            var typeClass = FIELD_CLASSES[this.state.fields[node.attrs.name].type];
            if (typeClass) {
                tdClassName += (' ' + typeClass);
            }
            if (node.attrs.widget) {
                tdClassName += (' o_' + node.attrs.widget + '_cell');
            }
        }
        var $td = $('<td>', { class: tdClassName });

        // We register modifiers on the <td> element so that it gets the correct
        // modifiers classes (for styling)
        var modifiers = this._registerModifiers(node, record, $td, _.pick(options, 'mode'));
        // If the invisible modifiers is true, the <td> element is left empty.
        // Indeed, if the modifiers was to change the whole cell would be
        // rerendered anyway.
        if (modifiers.invisible && !(options && options.renderInvisible)) {
            return $td;
        }

        if (node.tag === 'button') {
            return $td.append(this._renderButton(record, node));
        } else if (node.tag === 'widget') {
            return $td.append(this._renderWidget(record, node));
        }
        if (node.attrs.widget || (options && options.renderWidgets)) {
            var $el = this._renderFieldWidget(node, record, _.pick(options, 'mode'));
            this._handleAttributes($el, node);
            return $td.append($el);
        }
        var name = node.attrs.name;
        var field = this.state.fields[name];
        var value = record.data[name];
        var formattedValue = field_utils.format[field.type](value, field, {
            data: record.data,
            escape: true,
            isPassword: 'password' in node.attrs,
            digits: node.attrs.digits ? JSON.parse(node.attrs.digits) : undefined,
        });
        this._handleAttributes($td, node);
        return !colIndex || isFieldNumber ? $td.html(`<span>${formattedValue}</span>`) : $td.html(formattedValue);
        //return colIndex ? $td.html(formattedValue) : $td.html(`<span>${formattedValue}</span>`);
    },

    _renderEmptyRow: function () {
        var $td = $('<td>&nbsp;</td>').attr('colspan', this._getNumberOfCols() * 10);
        return $('<tr>').append($td);
    },
    _renderRow: function (record, index) {
        var $row = this._super.apply(this, arguments);
        const summary_level = record.data.summary_level;
        $row.addClass(`level-${summary_level}`);
        const rowHeader = $('thead tr');
        if (this.addTrashIcon) {
            if((this.state.model !== 'hr.survey.user.input.line' && this.state.model !== 'hr.survey.user.input') ) {
                const $editIcon = $('<button>', {class: 'fa fa-pencil', name: 'edit', 'aria-label': _t('Edit row ') + (index+1)});
                const $editTd = $('<td>', {class: 'o_list_record_edit'}).append($editIcon);
                $row[0].lastChild.before($editTd[0]);
                while(rowHeader[0].children.length < $row[0].children.length) {
                    rowHeader[0].append($('<th>')[0]);
                }
            }
        }
        if(this.state.model === 'hr.survey.user.input.line') {
            $row.find('.o_list_record_remove').remove();
        }
        return $row;
    },

    _renderView: function () {
        var def = this._super();

        return def;
    },
    _onAddRecord: function (ev) {
        // we don't want the browser to navigate to a the # url
        ev.preventDefault();

        // we don't want the click to cause other effects, such as unselecting
        // the row that we are creating, because it counts as a click on a tr
        ev.stopPropagation();

        // but we do want to unselect current row
        var self = this;
        this.unselectRow().then(function () {
            var context = ev.currentTarget.dataset.context;
            self.trigger_up('add_record', {context: context && [context]}); // TODO write a test, the deferred was not considered
       });
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

// We create a custom widget because this is the cleanest way to do it:
// to be sure this custom code will only impact selected fields having the widget
// and not applied to any other existing ListRenderer.
var AppraisalUsersOne2Many = FieldOne2Many.extend({
    events: _.extend({}, ListRenderer.prototype.events, {
        'click tr .o_list_record_edit': '_onEditIconClick',
        'click .o_field_x2many_list_row_add a': '_onAddRecord',
        'click tbody td.o_data_cell': '_onCellClick',
        'click tbody tr': '_onRowClicked',
        'keydown': '_onKeyDown',
    }),
    _onAddRecord(ev) {
    return;
    },
    _onEditIconClick(event) {
        event.preventDefault();
        event.stopPropagation();
        var $row = $(event.target).closest('tr');
        var id = $row.data('id');
        var self = this;
        this._openFormDialog({            id,
            context: $row[0],
            on_saved: function (record) {
                self._setValue({ operation: 'UPDATE', id: record.id });
            },
        });
     },
     _onCellClick(event){

     },
     _onRowClicked(event){
     },
     _onKeyDown(event){
     },
     _onEmptyRowClick(event){
     },
     _onKeyDownAddRecord(event){
        event.preventDefault();
        event.stopPropagation();
        return;
     },
     _onSortColumn: function (event){
        event.preventDefault();
        event.stopPropagation();
     },
     _onDoAction(event){

     },
     _onFooterClick(event){
     },
    /**
     * We want to use our custom renderer for the list.
     *
     * @override
     */

     init: function () {
        this._super.apply(this, arguments);
        this.creatingRecord = false;
    },
    _getRenderer: function () {
        if (this.view.arch.tag === 'tree') {
            return AppraisalUsers;
        }
        return this._super.apply(this, arguments);
    },
    _openFormDialog: function (params) {
            var context = this.record.getContext(_.extend({},
                this.recordParams,
                { additionalContext: params.context }
            ));
            if (this.mode!=="readonly"){
            this.trigger_up('open_one2many_record', _.extend(params, {
                domain: this.record.getDomain(this.recordParams),
                context: context,
                field: this.field,
                fields_view: this.attrs.views && this.attrs.views.form,
                parentID: this.value.id,
                viewInfo: this.view,
                deletable: this.activeActions.delete,
            }));
        }
    }
});
var AppraisalUsersOne2ManySurvey = FieldOne2Many.extend({
    events: _.extend({}, ListRenderer.prototype.events, {
        'click tr .o_list_record_edit': '_onEditIconClick',
        'click tbody td.o_data_cell': '_onCellClick',
        'click tbody tr': '_onRowClicked',
        'keydown': '_onKeyDown',
    }),

    _onEditIconClick(event) {
        event.preventDefault();
        event.stopPropagation();
        var $row = $(event.target).closest('tr');
        var id = $row.data('id');
        var self = this;
        this._openFormDialog({
            id,
            context: $row[0],
            on_saved: function (record) {
                self._setValue({ operation: 'UPDATE', id: record.id });
            },
        });
     },
     _onCellClick(event){

     },
     _onRowClicked(event){
     },
     _onKeyDown(event){
     },
     _onEmptyRowClick(event){
     },
     _onKeyDownAddRecord(event){
        event.preventDefault();
        event.stopPropagation();
        return;
     },
     _onSortColumn: function (event){
        event.preventDefault();
        event.stopPropagation();
     },
     _onDoAction(event){

     },
     _onFooterClick(event){
     },
    /**
     * We want to use our custom renderer for the list.
     *
     * @override
     */

     init: function () {
        this._super.apply(this, arguments);
        this.creatingRecord = false;
    },
    _getRenderer: function () {
        if (this.view.arch.tag === 'tree') {
            return AppraisalUsers;
        }
        return this._super.apply(this, arguments);
    },
    _openFormDialog: function (params) {
            var context = this.record.getContext(_.extend({},
                this.recordParams,
                { additionalContext: params.context }
            ));
            if (this.mode!=="readonly"){
            this.trigger_up('open_one2many_record', _.extend(params, {
                domain: this.record.getDomain(this.recordParams),
                context: context,
                field: this.field,
                fields_view: this.attrs.views && this.attrs.views.form,
                parentID: this.value.id,
                viewInfo: this.view,
                deletable: this.activeActions.delete,
            }));
        }
    }
});
var AppraisalUserMany2One =FieldMany2One.extend({

    init: function () {
        this._super.apply(this, arguments);
    },
    _onFieldChanged: function (event) {
        this.__parentedParent.__parentedChildren.forEach(children=>{
            if(children.name=='survey_user_ids')
            {
                children._getRenderer();
            }
        });
        this.lastChangeEvent = event;
    },
});

var Appraisal_Field = AbstractField.extend({
    custom_events: _.extend({}, AbstractField.prototype.custom_events, {
        field_changed: '_onFieldChanged'
    }),
    events: _.extend({
        'keydown': '_onKeydown',
        'input': '_onInput',
        'change': '_onChange',
    }, AbstractField.prototype.events),
    supportedFieldTypes: ['char'],
    /**
     * @override
     */
    init: function (parent) {
        this._super.apply(this, arguments);
         if (this.mode === 'edit') {
                this.tagName = 'input';
         }

    },
    _renderEdit: function (){
        this._super.apply(this, arguments);
        this._prepareInput(this.$el);
    },
     _renderReadonly: function () {
        this.$el.text(this.value);
    },
    _onKeydown : function(e){
        if(e.keyCode === $.ui.keyCode.SPACE){
            e.preventDefault();
        }
    },
    _onInput : function(event){

    },
    _onChange : function(event){
        console.log('onchange')
    },
    _onFieldChanged: function(event){

    },
    _prepareInput: function ($input) {
        this.$input = $input || $("<input/>");
        this.$input.addClass('o_input');

        var inputAttrs = { placeholder: this.attrs.placeholder || "" };
        var inputVal;
        inputAttrs = _.extend(inputAttrs, { type: 'text', autocomplete: this.attrs.autocomplete });
        inputVal = this.value;
        this.$input.attr(inputAttrs);
        this.$input.val(inputVal);

        return this.$input;
    },
    commitChanges: function () {
        if (this._isDirty && this.mode === 'edit') {
            return this._doAction();
        }
    },
    _doAction: function () {
        // as _doAction may be debounced, it may happen that it is called after
        // the widget has been destroyed, and in this case, we don't want it to
        // do anything (commitChanges ensures that if it has local changes, they
        // are triggered up before the widget is destroyed, if necessary).
        if (!this.isDestroyed()) {
            return this._setValue(this._getValue());
        }
    },
});
var FieldBoolean = AbstractField.extend({
    className: 'o_field_boolean',
    events: _.extend({}, AbstractField.prototype.events, {
        change: '_onChange',
    }),
    supportedFieldTypes: ['boolean'],

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Toggle the checkbox if it is activated due to a click on itself.
     *
     * @override
     */
    activate: function (options) {
        var activated = this._super.apply(this, arguments);
        // The formatValue of boolean fields renders HTML elements similar to
        // the one rendered by the widget itself. Even though the event might
        // have been fired on the non-widget version of this field, we can still
        // test the presence of its custom class.
        if (activated && options && options.event && $(options.event.target).closest('.custom-control.custom-checkbox').length) {
            this._setValue(!this.value);  // Toggle the checkbox
        }
        return activated;
    },

    /**
     * @override
     * @returns {jQuery} the focusable checkbox input
     */
    getFocusableElement: function () {
        return this.mode === 'readonly' ? $() : this.$input;
    },
    /**
     * A boolean field is always set since false is a valid value.
     *
     * @override
     */
    isSet: function () {
        return true;
    },
    /**
     * When the checkbox is rerendered, we need to check if it was the actual
     * origin of the reset. If it is, we need to activate it back so it looks
     * like it was not rerendered but is still the same input.
     *
     * @override
     */
    reset: function (record, event) {
        var rendered = this._super.apply(this, arguments);
        if (event && event.target.name === this.name) {
            this.activate();
        }
        return rendered;
    },
    /**
     * Associates the 'for' attribute of the internal label.
     *
     * @override
     */
    setIDForLabel: function (id) {
        this._super.apply(this, arguments);
        this.$('.custom-control-label').attr('for', id);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * The actual checkbox is designed in css to have full control over its
     * appearance, as opposed to letting the browser and the os decide how
     * a checkbox should look. The actual input is disabled and hidden. In
     * readonly mode, the checkbox is disabled.
     *
     * @override
     * @private
     */
    _render: function () {
        var $checkbox = this._formatValue(this.value);
        this.$input = $checkbox.find('input');
        this.$input.prop('disabled', this.mode === 'readonly');
        this.$el.addClass($checkbox.attr('class'));
        this.$el.empty().append($checkbox.contents());
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Properly update the value when the checkbox is (un)ticked to trigger
     * possible onchanges.
     *
     * @private
     */
    _onChange: function () {
        this._setValue(this.$input[0].checked);
    },
    /**
     * Implement keyboard movements.  Mostly useful for its environment, such
     * as a list view.
     *
     * @override
     * @private
     * @param {KeyEvent} ev
     */
    _onKeydown: function (ev) {
        switch (ev.which) {
            case $.ui.keyCode.ENTER:
                this.$input.prop('checked', !this.value);
                this._setValue(!this.value);
                return;
            case $.ui.keyCode.UP:
            case $.ui.keyCode.RIGHT:
            case $.ui.keyCode.DOWN:
            case $.ui.keyCode.LEFT:
                ev.preventDefault();
        }
        this._super.apply(this, arguments);
    },
});
var AppraisalFieldBooleanButton = AbstractField.extend({
    className: 'o_stat_info',
    supportedFieldTypes: ['boolean'],

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * A boolean field is always set since false is a valid value.
     *
     * @override
     */
    isSet: function () {
        return true;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * This widget is supposed to be used inside a stat button and, as such, is
     * rendered the same way in edit and readonly mode.
     *
     * @override
     * @private
     */
    _render: function () {
        this.$el.empty();
        var text, hover;
        switch (this.nodeOptions.terminology) {
            case "active":
                text = this.value ? _t("ĐÁNH GIÁ") : _t("KHÔNG ĐÁNH GIÁ");
                hover = this.value ? _t("KHÔNG ĐÁNH GIÁ") : _t("ĐÁNH GIÁ");
                break;
            case "archive":
                text = this.value ? _t("Active") : _t("Archived");
                hover = this.value ? _t("Archive") : _t("Restore");
                break;
            case "close":
                text = this.value ? _t("Active") : _t("Closed");
                hover = this.value ? _t("Close") : _t("Open");
                break;
            default:
                var opt_terms = this.nodeOptions.terminology || {};
                if (typeof opt_terms === 'string') {
                    opt_terms = {}; //unsupported terminology
                }
                text = this.value ? _t(opt_terms.string_true) || _t("On")
                                  : _t(opt_terms.string_false) || _t("Off");
                hover = this.value ? _t(opt_terms.hover_true) || _t("Switch Off")
                                   : _t(opt_terms.hover_false) || _t("Switch On");
        }
        var val_color = this.value ? 'text-success' : 'text-danger';
        var hover_color = this.value ? 'text-danger' : 'text-success';
        var $val = $('<span>').addClass('o_stat_text o_not_hover ' + val_color).text(text);
        var $hover = $('<span>').addClass('o_stat_text o_hover ' + hover_color).text(hover);
        this.$el.append($val).append($hover);
    },
});
fieldRegistry.add('khongdanhgia_button', AppraisalFieldBooleanButton);
fieldRegistry.add('checkbox_field', FieldBoolean);
fieldRegistry.add('appraisal_field', Appraisal_Field);
fieldRegistry.add('appraisalUser_one2many', AppraisalUsersOne2Many);
fieldRegistry.add('survey_one2many', AppraisalUsersOne2ManySurvey);
fieldRegistry.add('appraisalUser_many2one', AppraisalUserMany2One);

});
