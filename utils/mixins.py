from rest_framework import serializers

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

    def validate(self, attrs):
        initialObject = self.context.get("initialObject", None)
        requestObject = self.context.get("requestObject", None)
        instance = self.Meta.model(**attrs)
        instance.clean(initialObject=initialObject, requestObject=requestObject)
        return attrs
