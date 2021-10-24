from rest_framework import serializers
from utils.helpers import get_file_representations

# Class Custom Model Admin Mixing
class CustomModelAdminMixin(object):
    '''
    DOCSTRING for CustomModelAdminMixin:
    This model mixing automatically displays all fields of a model in admin panel 
    following the criteria.
    code: @ Numan Ibn Mazid
    '''

    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.get_internal_type() != 'TextField'
        ]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


class DynamicMixinModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DynamicMixinModelSerializer, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].error_messages['required'] = f"`{(''.join(field.split('_'))).title()}` field is required"
            self.fields[field].error_messages['null'] = f"`{(''.join(field.split('_'))).title()}` field may not be null"
            self.fields[field].error_messages['blank'] = f"`{(''.join(field.split('_'))).title()}` field may not be blank"
        
    def validate_common(self, attrs):
        instance = None

        initialObject = self.context.get("initialObject", None)
        requestObject = self.context.get("requestObject", None)

        if len(self.Meta.model._meta.many_to_many) >= 1:
            attrsCopy = attrs.copy()
            # modelAllFields = self.Meta.model._meta.fields + self.Meta.model._meta.many_to_many
            for field in self.Meta.model._meta.many_to_many:
                # remove many to many field from attrs
                many_field_name = attrs.pop(field.name)
            instance = self.Meta.model(**attrs)
            # return back the original attrs
            attrs = attrsCopy
        else:
            instance = self.Meta.model(**attrs)

        # call the models clean method if exists
        models_clean = getattr(instance, "clean", None)
        if callable(models_clean):
            instance.clean(initialObject=initialObject, requestObject=requestObject)

        return attrs
        
    def validate_initials(self, attrs):
        return self.validate_common(attrs=attrs)
        
    def validate(self, attrs):
        return self.validate_common(attrs=attrs)
    
    
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(DynamicMixinModelSerializer, self).to_representation(instance)
        representation = get_file_representations(representation=representation, instance=instance)
        return representation
