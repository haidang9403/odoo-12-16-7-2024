odoo.define('sea_asset_base.sea_asset_controllers', function (require) {
// The goal of this file is to contain JS hacks related to allowing
// section and note on sale order and invoice.

// [UPDATED] now also allows configuring products on sale order.

"use strict";
var pyUtils = require('web.py_utils');
var core = require('web.core');
var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
var fieldRegistry = require('web.field_registry');
var ListRenderer = require('web.ListRenderer');
var field_utils = require('web.field_utils');

var SeaAssetListController = ListController.extend({
    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);
        this.hasSidebar = params.hasSidebar;
        this.toolbarActions = params.toolbarActions || {};
        this.editable = params.editable;
        this.noLeaf = params.noLeaf;
        this.selectedRecords = params.selectedRecords || [];
        console.log('List controller');

    },
    // Override the ListView to handle the custom events 'open_record' (triggered when clicking on a
    // row of the list) such that it triggers up 'select_record' with its res_id.
    custom_events: _.extend({}, ListController.prototype.custom_events, {
//        open_record: function (event) {
//            var selectedRecord = this.model.get(event.data.id);
//            this.trigger_up('select_record', {
//                id: selectedRecord.res_id,
//                display_name: selectedRecord.data.display_name,
//            });
//        },
    }),
});
var SeaAssetListRenderer = ListRenderer.extend({

    _renderBodyCell: function (record, node, index, options) {
        var $cell = this._super.apply(this, arguments);
        return $cell;
    },

    _renderRow: function (record, index) {

        var $row = this._super.apply(this, arguments);
        var self=this;
        return this._super.apply(this, arguments);
    },

    _renderView: function () {
        var def = this._super();
        return def;
    },


});

var SeaAssetOne2Many = FieldOne2Many.extend({
    events: _.extend({}, SeaAssetListRenderer.prototype.events, {
        'click tr .o_list_record_edit': '_onEditIconClick',
        'click tbody td.o_data_cell': '_onCellClick',
        'click tbody tr': '_onRowClicked',
        'keydown': '_onKeyDown',
    }),
    config: _.extend({}, FieldOne2Many.prototype.config, {

        Controller: SeaAssetListController,
        Renderer: ListRenderer,
    }),
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
        console.log('one2many')
    },
    _getRenderer: function () {
        if (this.view.arch.tag === 'tree') {
            return SeatekSignListRenderer;
        }
        return this._super.apply(this, arguments);
    },

});

fieldRegistry.add('sea_asset_one2many', SeaAssetOne2Many);

});
