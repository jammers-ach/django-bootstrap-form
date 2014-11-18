from templatetags.bootstrap import bootstrap_horizontal
from django import forms
from django.utils.safestring import mark_safe

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

class BootstrapModelForm(forms.ModelForm):
    '''A model form that will render itself in bootstrap'''
    required_css_class = 'required'

    def __init__( self,  *args, **kw ):
        super( BootstrapModelForm, self ).__init__( *args, **kw )

        #see if any of our fields are date or datetime widgets
        for k,v in self.fields.iteritems():
            if( isinstance(v,forms.fields.DateTimeField)):
                self.fields[k].widget = BootstrapDateTimeWidget()
            elif( isinstance(v,forms.fields.DateField)):
                self.fields[k].widget = BootstrapDateWidget()

    def as_bootstrap(self):
        return bootstrap_horizontal(self)

    class Media:
        css = {
            'all': ('bootstrap_form/css/forms.css',)
        }


class BootstrapForm(forms.Form):
    '''A form subclass that can be rendered as bootstrap form'''

    def as_p(self):
        return "James is super cool - Ordinary form"
