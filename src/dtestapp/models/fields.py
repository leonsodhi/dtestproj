from django.db import models

class IntegerListField(models.CommaSeparatedIntegerField):
    description = "Comma-separated integers represented as a list"
    
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs): 
        kwargs['max_length'] = 255
        super(IntegerListField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        if isinstance(value, list):
            return value
        l = []
        if(len(value) > 0):
            l = [int(n) for n in value.split(",")]
        return l
                
    def get_prep_value(self, value):        
        return str(value).strip('[').strip(']')
    