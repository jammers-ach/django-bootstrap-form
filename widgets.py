'''
widgets.py - Bootstrap widgets for bootstrap form
'''
from django import forms
from django.utils.safestring import mark_safe

class BootstrapChoiceOtherField(forms.widgets.Select):


    def __init__(self,*args,**kwargs):
        kwargs['attrs'] = {'class':'otherchoice'}

        self.klass = kwargs.pop('klass')
        self.fields = kwargs.pop('fields')
        self.default_choices = kwargs.pop('default_choices')
        self.required=kwargs.pop('required')

        kwargs['choices'] = ()


        super(BootstrapChoiceOtherField,self).__init__(*args,**kwargs)

    class Media:
        #css = {
               #'all':('bootstrap_form/css/bootstrap-datetimepicker.min.css',)
        #}
        js = ['bootstrap_form/js/bootstrap_form_other_choice.js'] #TODO move all the boostrapform js into one

    def render(self, name, value, attrs=None,choices=()):
        print choices
        us = super(BootstrapChoiceOtherField,self).render(name,value,attrs)
        input2 = '<input class="other_option form-control"  name="__%s" type="text">' % name

        html = """<div>
        %s
        %s
        """ % (us,input2)
        html += "</div>"
        return mark_safe(html)


    def render_options(self, choices, selected_choices):
        choices = self.make_choices()
        return super(BootstrapChoiceOtherField,self).render_options(choices,selected_choices)



    def make_choices(self):
        vals = self.klass.objects.all().order_by(*self.fields).values_list(*self.fields,flat=True).distinct()

        choices =  list(self.default_choices)
        choices.extend([i for i in vals if i not in self.default_choices])
        choices = sorted([ (i,i) for i in choices])


        if(not self.required):
            choices = [('','----')] + choices

        choices += [('_-_','....other')]

        return choices



class BootstrapIntegratedModelField(forms.widgets.Input):
    pass

class BootstrapModelChoiceField(forms.widgets.Select):

    def __init__(self,*args,**kwargs):
        qs = kwargs.pop('qs')
        choices = [(o.pk,o) for o in qs]

        if(len(choices) > 0):
            self.has_add_url = hasattr(choices[0][1],'get_edit_url')
            self.has_search_url = hasattr(choices[0][1],'get_search_url')
        else:
            self.has_add_url = False
            self.has_search_url = False

        if(self.has_add_url):
            self.add_url = choices[0][1].get_edit_url()
        if(self.has_search_url):
            self.search_url = choices[0][1].get_search_url()

        blank_choice = kwargs.pop('empty_label','---------')

        if(kwargs.pop('required',False)):
            kwargs['choices'] = [(None,blank_choice)] + choices
        else:
            kwargs['choices'] = choices

        super(BootstrapModelChoiceField,self).__init__(*args,**kwargs)

    def render(self, name, value, attrs=None):
        us = super(BootstrapModelChoiceField,self).render(name,value,attrs)

        html = """<div class='%s model-picker'>
        %s

        """ % ('input-group' if self.has_add_url or self.has_search_url else '',us)
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


