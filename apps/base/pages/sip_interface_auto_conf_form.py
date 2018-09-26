# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook
from pbx import init

class SipInterfaceAutoConf(FormPage):
    
    verbose_name = u'自动检测'
    app_label = 'base'
    hidden_menu = True
    
    def prepare_form(self):
        res = init.get_sipinterface_default_ip_list()
        _choices= [(e,e) for e in res]
        class MyForm(forms.Form):
            ips = forms.MultipleChoiceField(label='选择IP', choices=_choices)
        self.view_form = MyForm
        self.message_user(u'选择ip，点击确定则生成对应的端口配置', 'success')
            
    @filter_hook
    def save_forms(self):
        data = self.form_obj.cleaned_data
        ips = data.get('ips', [])
        if ips:
            for ip in ips:
                init.create_sipinterface_with_ip(ip)
        else:
            init.create_sipinterface_with_ip('')
    
    @filter_hook
    def post_response(self):
        return '/xadmin/base/sipinterface/'
site.register_page(SipInterfaceAutoConf)
