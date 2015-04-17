from templatetags.bootstrap import bootstrap_horizontal
from django import forms
from .widgets import *

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
            elif( isinstance(v,forms.ModelChoiceField)):
                self.fields[k].widget = BootstrapModelChoiceField(qs = v.queryset,required=v.required,empty_label=v.empty_label)

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

    def as_bootstrap(self):
        return bootstrap_horizontal(self)

    class Media:
        css = {
            'all': ('bootstrap_form/css/forms.css',)
        }


