from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from utils.snippets import simple_random_string, random_string_generator
import uuid


class ResponseWrapper(Response):

    def __init__(self, data=None, error_code=None, template_name=None, headers=None, exception=False, content_type=None,
                 error_msg=None, msg=None, response_success=True, status=None, data_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        status_by_default_for_gz = 200
        if error_code is None and status is not None:
            if status > 299 or status < 200:
                error_code = status
                response_success = False
            else:
                status_by_default_for_gz = status
        if error_code is not None:
            status_by_default_for_gz = error_code
            response_success = False
            
        # manipulate dynamic msg
        if msg is not None and not msg == "":
            if msg.lower() == "list":
                msg = "List retrieved successfully!" if response_success else "Failed to retrieve the list!"
            elif msg.lower() == "create":
                msg = "Created successfully!" if response_success else "Failed to create!"
            elif msg.lower() == "update":
                msg = "Updated successfully!" if response_success else "Failed to update!"
            elif msg.lower() == "delete":
                msg = "Deleted successfully!" if response_success else "Failed to delete!"
            elif msg.lower() == "retrieve":
                msg = "Object retrieved successfully!" if response_success else "Failed to retrieve the object!"
            else:
                pass

        output_data = {
            "error": {"code": error_code, "error_details": error_msg},
            "data": data,
            "status": response_success,
            "status_code": error_code if not error_code == "" and not error_code == None else status_by_default_for_gz,
            "message": msg if msg else str(error_msg) if error_msg else "Success" if response_success else "Failed",
        }
        if data_type is not None:
            output_data["type"] = data_type

        super().__init__(data=output_data, status=status_by_default_for_gz,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)


def custom_exception_handler(exc, context):
    """
    Override Django Rest Framework's default exception to adopt system's response object's structure
    """
    response = exception_handler(exc, context)

    try:
        response_parent = {
            "error": {
                "code": None,
                "error_details": None
            },
            "data": None,
            "status": False,
            "status_code": None,
            "message": "Failed"
        }
        response_parent["error"]["error_details"] = response.data

        if response is not None:
            response_parent["error"]["code"] = response.status_code
            response_parent["status_code"] = response.status_code

        response.data = response_parent

    except Exception as E:
        if response is not None:
            response.data['status_code'] = response.status_code

    return response


def populate_related_object_id(request, related_data_name):
    """[Populates Related Data Object ID]

    Args:
        related_data_name ([String]): [Related Data Name]

    Returns:
        [tuple]: [(Status(Boolean), ObjectID(Integer)/Message(String/None))]
    """
    
    related_data_name = related_data_name.lower()
    related_data = request.data.get(related_data_name)
    
    related_data_type = type(related_data)
    # Return False if space not given (as it is mandatory to verify user permission)
    if related_data == None or related_data == "":
        return False, f"`{related_data_name}` is required!"
    if (related_data_type == list or related_data_type == tuple) and len(related_data) <= 0:
        return False, f"At least one `{related_data_name}` is required!"
    
    realated_object_id = None
    
    # populate related object id
    if related_data_type == list or related_data_type == tuple:
        realated_object_id = related_data[0]
    elif related_data_type == str:
        splitted_data = related_data.split(",") if "," in related_data else related_data.split()
        realated_object_id = [int(i) for i in splitted_data][0]
    elif related_data_type == int:
        realated_object_id = related_data
    else:
        return False, "Invalid data type received!"
    
    return True, realated_object_id


def model_cleaner(selfObj, qsFieldObjectList):
    """[Dynamic Model Clean Method]

    Args:
        selfObj ([Model Instance]): [self]
        qsFieldObjectList ([List]): [[{'qs': Model.objects.filter(title='abc'), 'field': 'title'}, ]]

    Raises:
        ValidationError: [Raises Django Validation Error]
    """
    
    errors = {}
    
    for obj in qsFieldObjectList:
        # perform validation
        qs = obj.get("qs", selfObj.__class__.objects.filter(id=None))
        field = obj.get("field", "Undefined")
        if selfObj.pk:
            qs = qs.exclude(pk=selfObj.pk)
        if qs.exists():
            value = getattr(selfObj, field)
            errors[field] = [f"{selfObj.__class__.__name__} with this {field} ({value}) already exists!"]
            
    # raise exception
    if len(errors):
        raise ValidationError(
            errors
        )
        

def autoslugFromField(fieldname):
    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname!r}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                try:
                    slug = slugify(source)
                    Klass = instance.__class__
                    qs_exists = Klass.objects.filter(slug=slug).exists()
                    if qs_exists:
                        new_slug = "{slug}-{randstr}".format(
                            slug=slug,
                            randstr=random_string_generator(size=4)
                        )
                        instance.slug = new_slug
                    else:
                        instance.slug = slug
                except Exception as e:
                    instance.slug = simple_random_string()
        return model
    return decorator
        

def autoslugFromUUID():
    def decorator(model):
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                try:
                    instance.slug = str(uuid.uuid4())
                except Exception as e:
                    instance.slug = simple_random_string()
        return model
    return decorator
