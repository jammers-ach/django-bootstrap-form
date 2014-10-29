from templatetags.bootstrap import bootstrap_horizontal
from django import forms

class BootstrapModelForm(forms.ModelForm):
    '''A model form that will render itself in bootstrap'''
    required_css_class = 'required'

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
