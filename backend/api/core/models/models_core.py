from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class ModelCore(models.Model):
    """
    Base model class for all models in the core application.
    Provides common functionality and fields.
    """
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_value_for_field(self, field_name):
        """
        Returns the value of the specified field.
        """
        if hasattr(self, field_name):
            return getattr(self, field_name)
        raise ValidationError(f"Field '{field_name}' does not exist on {self.__class__.__name__}")
    
    
    def set_value_for_field(self, field_name, value):
        """
        Sets the value of the specified field.
        """
        if hasattr(self, field_name):
            setattr(self, field_name, value)
            self.save(update_fields=[field_name])
        else:
            raise ValidationError(f"Field '{field_name}' does not exist on {self.__class__.__name__}")
    
    
    def get_attr(self, key_path:str, default:any=None):
        """
        Retrieves a value from the model's fields or related objects.
        If the value is not found, it returns the provided default value.
        """
        try:
            if not key_path:
                return default
            
            keys = key_path.split('.')
            first_key = keys.pop(0)
            
            value =  getattr(self, first_key, None)
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
           
        except ValidationError:
            return default
        
    def set_attr(self, key_path:str, value:any=None, save:bool=False):
        """
        Retrieves a value from the model's fields or related objects.
        If the value is not found, it returns the provided default value.
        If save is True, it saves the model after setting the value.
        """
        try:
            
            if not key_path:
                return
            
            keys = key_path.split('.')
            field_name = keys.pop(0)
            
            data = getattr(self, field_name, None)
            if not isinstance(data, dict):
                data = {}
            
            current = data
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            
            current[keys[-1]] = value
            setattr(self, field_name, data)
            
            if save:
                self.save(update_fields=[field_name])
            
        except ValidationError:
            return value