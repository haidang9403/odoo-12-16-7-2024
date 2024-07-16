odoo.define('sea_shortname_company.shortname_company', function(require) {
"use strict";

var SwitchCompanyMenu = require('web.SwitchCompanyMenu');
var session = require('web.session');
SwitchCompanyMenu.include({
    start: function () {

        var self = this;
        this._super.apply(this, arguments);
        var companiesList = '';
        if (this.isMobile) {
            companiesList = '<li class="bg-info">' +
                _t('Tap on the list to change company') + '</li>';
        }
        else {
              this.$('.oe_topbar_name').text(session.short_name_company.current_company[1]);
              //this.$('.oe_topbar_name').text(session.user_companies.current_company[1]);
        }
        _.each(session.short_name_company.allowed_companies, function(company) {
        //_.each(session.user_companies.allowed_companies, function(company) {
           var a = '';
           var isCurrentCompany = company[0] === session.short_name_company.current_company[0];
            //var isCurrentCompany = company[0] === session.user_companies.current_company[0];
            if (isCurrentCompany) {
                a = '<i class="fa fa-check mr8"></i>';
            } else {
                a = '<span style="margin-right: 24px;"/>';
            }

            companiesList += '<a role="menuitemradio" aria-checked="' + isCurrentCompany + '" href="#" class="dropdown-item" data-menu="company" data-company-id="' +
                            company[0] + '">' + a + company[1] + '</a>';
        });
        this.$('.dropdown-menu').html(companiesList);

    },
});
})
