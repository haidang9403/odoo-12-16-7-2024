odoo.define('seatek_hr_appraisal.Appraisal', function (require) {
"use strict";

var Context = require('web.Context');
var core = require('web.core');
var dataManager = require('web.data_manager');
var Dialog = require('web.Dialog');
var Domain = require('web.Domain');
var FormController = require('web.FormController');
var FormRenderer = require('web.FormRenderer');
var FormView = require('web.FormView');
var pyUtils = require('web.py_utils');
var session  = require('web.session');
var viewRegistry = require('web.view_registry');
var rpc = require('web.rpc');

var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;

var AppraisalController = FormController.extend({
    custom_events: _.extend({}, FormController.prototype.custom_events, {
        change_layout: '_onChangeLayout',
        enable_dashboard: '_onEnableDashboard',
        save_dashboard: '_saveDashboard',
        switch_view: '_onSwitchView',
    }),

    /**
     * @override
     */

    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);
        var self=this;

    },

    start: function () {
        return this._super.apply(this, arguments);

    },
    update: function (params, options) {
        var self = this;
        this.mode = params.mode || this.mode;
        return this._super(params, options).then(function () {
        });
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */


});

var AppraisalRenderer = FormRenderer.extend({
    custom_events: _.extend({}, FormRenderer.prototype.custom_events, {
        do_action: '_onDoAction',
        env_updated: '_onEnvUpdated',
        update_filters: '_onUpdateFilters',
        switch_view: '_onSwitchView',
    }),
    events: _.extend({}, FormRenderer.prototype.events, {
        'click .oe_dashboard_column .oe_fold': '_onFoldClick',
        'click .oe_dashboard_link_change_layout': '_onChangeLayout',
        'click .oe_dashboard_column .oe_close': '_onCloseAction',
    }),

    /**
     * @override
     */

    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        var self=this
        console.log('form renderer',this);


        let currentUser=session.uid;
//        if(this.state.data.is_manager){
//            this.temp_node=this.arch.children[3].children[0];
//            this.test_node=this.arch.children[3].children[0];
//        }
        if (this.arch.attrs.class){

            if(this.arch.attrs.class=='o_user_input' || this.arch.attrs.class=='o_user_input_dialog'){
                this.arch.children.forEach(group=>{
                    if(group.tag=='group'){
                        let children=[];
                        this.selectUserOpinionElement(group, children, currentUser);
                        let childrenDeXuat=[];
                        this.selectDeXuatHDDGElement(group, childrenDeXuat, currentUser);
                    }
                });
            }
//            if(this.arch.attrs.class=='o_user_input_dialog'){
//                var $modal = this.$('.modal');
//                console.log('modal',$modal);
//                if ($modal.is('.modal-dialog')) {}
//            }
        }



    },
    selectUserOpinionElement(root = {}, children = [], currentUser) {
        if(root.children){
        root.children.forEach(item => {
            if(item.attrs?.class == "user_opinion") {
                if(this.state.data.smanager_user_id_compute==currentUser){
                    children.push(item.children[4]);
                    children.push(item.children[5]);
                }
                else if(this.state.data.manager_user_id_compute==currentUser){
                    children.push(item.children[2]);
                    children.push(item.children[3]);
                }
                else if(this.state.data.user_id_compute==currentUser){
                    children.push(item.children[0]);
                    children.push(item.children[1]);
                }
                item.children=children;
            } else {
                this.selectUserOpinionElement(item, [], currentUser);
            }
        });
        }
    },
     _updatePages: function(survey){
        var self=this;

    },
    selectDeXuatHDDGElement(root = {}, children = [], currentUser) {

        if (root.children){
        root.children.forEach(item => {
            if(item.attrs?.class == "de_xuat_hddg") {
                if(this.state.data.smanager_user_id_compute==currentUser){
                    let modifiers={readonly:true};
                    children.push(item.children[0]);
                    children.push(item.children[1]);
                    children.push(item.children[2]);
                    children.push(item.children[3]);
                    children.push(item.children[4]);
                    children.push(item.children[5]);
                    children.push(item.children[6]);
                    children.push(item.children[7]);
                    children.push(item.children[8]);
                    children.push(item.children[9]);
                    children.push(item.children[10]);
                    children.push(item.children[11]);
                    children.push(item.children[12]);
                    children[0].attrs.modifiers=modifiers;
                    children[1].attrs.modifiers=modifiers;
                    children[2].attrs.modifiers=modifiers;
                    children[3].attrs.modifiers=modifiers;
                    children[4].attrs.modifiers=modifiers;
                    children[5].attrs.modifiers=modifiers;
                    children[6].attrs.modifiers=modifiers;
                    children[7].attrs.modifiers=modifiers;
                }
                if(this.state.data.manager_user_id_compute==currentUser){
                    let modifiers={readonly:true};
                    children.push(item.children[0]);
                    children.push(item.children[1]);
                    children.push(item.children[2]);
                    children.push(item.children[3]);
                    children.push(item.children[4]);
                    children.push(item.children[5]);
                    children.push(item.children[6]);
                    children.push(item.children[7]);
                    children.push(item.children[8]);
                    children[0].attrs.modifiers=modifiers;
                    children[1].attrs.modifiers=modifiers;
                    children[2].attrs.modifiers=modifiers;
                    children[3].attrs.modifiers=modifiers;
                }
                if(this.state.data.user_id_compute==currentUser){
                    children.push(item.children[0]);
                    children.push(item.children[1]);
                    children.push(item.children[2]);
                    children.push(item.children[3]);
                }
            item.children=children;
            } else {
                this.selectDeXuatHDDGElement(item, [], currentUser);
            }
        });
        }
    },
     _updatePages: function(survey){
        var self=this;

    },
    _onDoAction(event){
    },
    _renderTagNotebook: function (node) {
        var self=this;
        let new_node=[];
        let number_of_node=0;
            if(this.state.data.question_general){
                if(this.state.data.question_general.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='question_general'){
                                index.attrs.string=this.state.data.question_general.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_1){
                if(this.state.data.questions_1.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_1'){
                                index.attrs.string=this.state.data.questions_1.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_2){
                if(this.state.data.questions_2.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_2'){
                                index.attrs.string=this.state.data.questions_2.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_3){
                if(this.state.data.questions_3.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_3'){
                                index.attrs.string=this.state.data.questions_3.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_4){
                if(this.state.data.questions_4.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_4'){
                                index.attrs.string=this.state.data.questions_4.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
                if(this.state.data.questions_5){
                    if(this.state.data.questions_5.count>0){
                        node.children.forEach(index=>{
                            index.children.forEach(page=>{
                                if(page.attrs.name=='questions_5'){
                                    let modifiers={readonly:true};
                                    if(this.state.data.is_manager || this.arch.attrs.HDDG){
                                        modifiers={invisible:false};
                                    }
                                    else{
                                        modifiers={invisible:true};
                                    }

                                    index.attrs.modifiers=modifiers;
                                    index.attrs.string=this.state.data.questions_5.data[0].data.page_name
                                    new_node.push(index);
                                }
                            })
                        });
                    }
                }
            if(this.state.data.questions_6){
                if(this.state.data.questions_6.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_6'){
                                index.attrs.string=this.state.data.questions_6.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_7){
                if(this.state.data.questions_7.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_7'){
                                index.attrs.string=this.state.data.questions_7.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_8){
                if(this.state.data.questions_8.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_8'){
                                index.attrs.string=this.state.data.questions_8.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_9){
                if(this.state.data.questions_9.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_9'){
                                index.attrs.string=this.state.data.questions_9.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }
            if(this.state.data.questions_10){
                if(this.state.data.questions_10.count>0){
                    node.children.forEach(index=>{
                        index.children.forEach(page=>{
                            if(page.attrs.name=='questions_10'){
                                index.attrs.string=this.state.data.questions_10.data[0].data.page_name
                                new_node.push(index);
                            }
                        })
                    });
                }
            }



        node.children=new_node;
        var self = this;
        var $headers = $('<ul class="nav nav-tabs">');
        var $pages = $('<div class="tab-content">');
        var autofocusTab = -1;
        // renderedTabs is used to aggregate the generated $headers and $pages
        // alongside their node, so that their modifiers can be registered once
        // all tabs have been rendered, to ensure that the first visible tab
        // is correctly activated
        var renderedTabs = _.map(node.children, function (child, index) {
            var pageID = _.uniqueId('notebook_page_');
            var $header = self._renderTabHeader(child, pageID);
            var $page = self._renderTabPage(child, pageID);
            if (autofocusTab === -1 && child.attrs.autofocus === 'autofocus') {
                autofocusTab = index;
            }
            self._handleAttributes($header, child);
            $headers.append($header);
            $pages.append($page);
            return {
                $header: $header,
                $page: $page,
                node: child,
            };
        });
        if (renderedTabs.length) {
            var tabToFocus = renderedTabs[Math.max(0, autofocusTab)];
            tabToFocus.$header.find('.nav-link').addClass('active');
            tabToFocus.$page.addClass('active');
        }
        // register the modifiers for each tab
        _.each(renderedTabs, function (tab) {
            self._registerModifiers(tab.node, self.state, tab.$header, {
                callback: function (element, modifiers) {
                    // if the active tab is invisible, activate the first visible tab instead
                    var $link = element.$el.find('.nav-link');
                    var $firstVisibleTab = $headers.find('li:not(.o_invisible_modifier):first() > a');
                    if (modifiers.invisible && $link.hasClass('active')) {
                        $link.removeClass('active');
                        tab.$page.removeClass('active');
                        $firstVisibleTab.addClass('active');
                        $pages.find($firstVisibleTab.attr('href')).addClass('active');
                    }
                    if (!modifiers.invisible) {
                        // make first page active if there is only one page to display
                        var $visibleTabs = $headers.find('li:not(.o_invisible_modifier)');
                        if ($visibleTabs.length === 1) {
                            $firstVisibleTab.addClass('active');
                            $pages.find($firstVisibleTab.attr('href')).addClass('active');
                        }
                    }
                },
            });
        });

        var $notebook = $('<div class="o_notebook">')
                .data('name', node.attrs.name || '_default_')
                .append($headers, $pages);

        this._registerModifiers(node, this.state, $notebook);
        this._handleAttributes($notebook, node);

        return $notebook;
    },
});

var AppraisalView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {

        Controller: AppraisalController,
        Renderer: AppraisalRenderer,
    }),

    /**
     * @override
     */
    init: function (viewInfo) {
        this._super.apply(this, arguments);
        this.controllerParams.customViewID = viewInfo.custom_view_id;
    },
});

return AppraisalView;

});


odoo.define('seatek_hr_appraisal.viewRegistry', function (require) {
"use strict";

var AppraisalView = require('seatek_hr_appraisal.Appraisal');

var viewRegistry = require('web.view_registry');

viewRegistry.add('form_appraisal', AppraisalView);

});
