odoo.define('seatek_hr_survey.hr_survey', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var field_registry = require('web.field_registry');

var QWeb = core.qweb;

var HR_Survey = AbstractField.extend({
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
        this._setValue(this.$input[0].value);
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

field_registry.add('score_widget', HR_Survey);
return HR_Survey;
});
