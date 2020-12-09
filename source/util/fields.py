from django.db import models
from django.core import validators

class CharUpperField(models.CharField):    
        
    def _init_(self, *args, **kwargs):
        super(CharUpperField, self)._init_(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
        
    def get_prep_value(self, value):
        "Perform preliminary non-db specific value checks and conversions."
        if not value:
            return value
        else:
            return value.strip().upper()
        
class TextFieldlNullField(models.TextField):
    description = "CharField that stores NULL but returns ''"
    def to_python(self, value):
        if isinstance(value, models.TextField):
            return value 
        if value==None:
            return ""
        else:
            return value
    def get_db_prep_value(self, value, connection, prepared=False):
        if value=="":
            return None
        else:
            return value