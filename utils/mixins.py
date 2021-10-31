from rest_framework import serializers
from utils.helpers import get_file_representations
import os
from django.conf import settings
from django.template.defaultfilters import filesizeformat

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
            # populate field name
            field_name = (' '.join(field.split('_'))).title()
            # customize error message
            self.fields[field].error_messages['required'] = f"{field_name} field is required"
            self.fields[field].error_messages['null'] = f"{field_name} field may not be null"
            self.fields[field].error_messages['blank'] = f"{field_name} field may not be blank"
            
    def validate_files(self, attrs):
        # get model name
        MODEL = self.Meta.model
        # loop through all fields of the model
        for field in MODEL._meta.fields:
            if field.get_internal_type() in ['ImageField', 'FileField']:

                # get files and field name
                file_in_request = attrs.get(field.name, None)

                if file_in_request:
                    
                    # define field name
                    field_name = field.name
                    visible_field_name = (' '.join(field_name.split('_'))).title()

                    file = file_in_request
                    # validate file
                    if not file:
                        raise serializers.ValidationError({
                            field_name: f"{visible_field_name}: Invalid file!"
                        })

                    extension = os.path.splitext(file.name)[1]
                    # validate file extension
                    if not extension:
                        raise serializers.ValidationError({
                            field_name: f"{visible_field_name}: Invalid file extension!"
                        })
                    # get allowed file types from settings
                    ALLOWED_FILE_TYPES = settings.ALLOWED_FILE_TYPES

                    request_file_type = None
                    if extension in settings.ALLOWED_IMAGE_TYPES:
                        request_file_type = "image"
                    elif extension in settings.ALLOWED_DOCUMENT_TYPES:
                        request_file_type = "document"
                    else:
                        raise serializers.ValidationError(
                            {field_name: f"{visible_field_name}: Invalid file type received! Allowed file types are: {ALLOWED_FILE_TYPES}"}
                        )

                    if request_file_type:
                        if file.size > settings.FILE_SIZE_LIMIT_IN_BYTES:
                            raise serializers.ValidationError(
                                {field_name: f"{visible_field_name}: Please keep filesize under {filesizeformat(settings.FILE_SIZE_LIMIT_IN_BYTES)}. Current filesize {filesizeformat(file.size)}"}
                            )
                            
        return attrs
        
        
    def validate_common(self, attrs):
        instance = None

        initialObject = self.context.get("initialObject", None)
        requestObject = self.context.get("requestObject", None)
        
        # validate files
        self.validate_files(attrs=attrs)

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
