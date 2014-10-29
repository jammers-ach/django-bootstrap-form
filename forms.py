
from django import forms

class BootstrapModelForm(forms.ModelForm):
    def as_p(self):
        return "James is super cool - MODEL FORM"

class BootstrapForm(forms.Form):
    '''A form subclass that can be rendered as bootstrap form'''


    def as_p(self):
        return "James is super cool"
