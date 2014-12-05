'''
Fields.py - new fields for models
'''

from django.db.models import Field,SubfieldBase
from .widgets import BootstrapChoiceOtherField
#import os
#from django.conf import settings

class ChoicedOtherField(Field):
    '''a field that is restricted to the model+field in question'''

    description = 'A field that is restricted to the model in question'

    __metaclass__ = SubfieldBase

    def __init__(self, *args, **kwargs):
        #self.widget = MultipleFileWidget()
        self.obj_mod = kwargs.pop('obj_mod',None)
        self.obj_classname = kwargs.pop('obj',None)
        field = kwargs.pop('field','')
        if(isinstance(field,str)):
            self.fields = [field]
        else:
            self.fields = field

        self.default_choices  = kwargs.pop('default_choices','')

        super(ChoicedOtherField,self).__init__(*args,**kwargs)


    def formfield(self, **kwargs):
        #defaults = {'widget': self.widget}
        mod = __import__(self.obj_mod)
        klass = getattr(mod.models, self.obj_classname)
        required = not self.blank


        defaults = {'widget':BootstrapChoiceOtherField(klass=klass,fields=self.fields,default_choices=self.default_choices,required=required),
                    }
        defaults.update(kwargs)
        return super(ChoicedOtherField, self).formfield(**defaults)

    def get_internal_type(self):
        return "TextField"



