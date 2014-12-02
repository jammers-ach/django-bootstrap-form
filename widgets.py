'''
widgets.py - Bootstrap widgets for bootstrap form
'''
from django import forms
from django.utils.safestring import mark_safe

class BootstrapModelChoiceField(forms.widgets.Select):

    def __init__(self,*args,**kwargs):
        qs = kwargs.pop('qs')
        choices = [(o.pk,o) for o in qs]

        self.has_add_url = hasattr(choices[0][1],'get_edit_url')
        self.has_search_url = hasattr(choices[0][1],'get_search_url')

        if(self.has_add_url):
            self.add_url = choices[0][1].get_edit_url()
        if(self.has_search_url):
            self.search_url = choices[0][1].get_search_url()

        blank_choice = kwargs.pop('empty_label','---------')

        if(kwargs.get('required',False)):
            kwargs['choices'] = [(None,blank_choice)] + choices
        else:
            kwargs['choices'] = choices

        super(BootstrapModelChoiceField,self).__init__(*args,**kwargs)

    def render(self, name, value, attrs=None):
        us = super(BootstrapModelChoiceField,self).render(name,value,attrs)

        html = """<div class='input-group model-picker'>
        %s

        """ % us
        if(self.has_add_url or self.has_search_url):
            html += "<span class='input-group-btn'>"

        if(self.has_search_url):
            html+= """<button class="btn btn-default search_obj_button" type="button" data-url="%s">
                <span class="glyphicon glyphicon-search"></span>
            </button>""" % self.search_url
        if(self.has_add_url):
            html += """<button class="btn btn-default add_obj_button" type="button" data-url="%s">
                <span class="glyphicon glyphicon-plus"></span>
            </button>""" % self.add_url

        if(self.has_add_url or self.has_search_url):
            html += "</span>"
        html += "</div>"



        return mark_safe(html)

    class Media:
        #css = {
               #'all':('bootstrap_form/css/bootstrap-datetimepicker.min.css',)
        #}
        js = ['bootstrap_form/js/bootstrap_form_modelpicker.js']

class BootstrapDateWidget(forms.widgets.Input):

    _widget_class = 'datepicker'
    _date_format = 'YYYY-MM-DD'



    class Media:
        css = {
               'all':('bootstrap_form/css/bootstrap-datetimepicker.min.css',)
        }
        js = ['bootstrap_form/js/moment.min.js','bootstrap_form/js/bootstrap_form_datepicker.js','bootstrap_form/js/bootstrap-datetimepicker.min.js']

    def render(self, name, value, attrs=None):
        html = """<div class='input-group %s' id='datetimepicker1'>
                    <input name='%s' type='text' class="form-control" data-date-format='%s' value='%s'/>
                    <span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span>
                    </span>
                </div>""" % (self._widget_class,name,self._date_format,value if value else '')
                #TODO find out how to do classess well here
        return mark_safe(html)


class BootstrapDateTimeWidget(BootstrapDateWidget):
    _widget_class = 'datetimepicker'
    _date_format = 'YYYY-MM-DD HH:mm:SS'


