from django.http.response import Http404
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from utils.snippets import simple_random_string, random_string_generator
import uuid
from rest_framework import serializers
from utils.snippets import url_check


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
    
    try:
        
        response_parent["error"]["error_details"] = response.data

        if response is not None:
            response_parent["error"]["code"] = response.status_code
            response_parent["status_code"] = response.status_code

        response.data = response_parent

    except Exception as E:
        
        if response is not None:
            response_parent["error"]["error_details"] = str(E)
            response_parent["error"]["code"] = response.status_code
            response_parent["status_code"] = response.status_code
            response.data = response_parent

    return response

# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     # Now add the HTTP status code to the response.
#     if response is not None:

#         errors = []
#         message = response.data.get('detail')
#         if not message:
#             for field, value in response.data.items():
#                 errors.append("{} : {}".format(field, " ".join(value)))
#             response.data = {'data': [], 'message': 'Validation Error', 'errors': errors, 'status': 'failure'}
#         else:
#             response.data = {'data': [], 'message': message, 'error': [message], 'success': 'failure'}

#     return response


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


def model_cleaner(selfObj, qsFieldObjectList, initialObject):
    """[Dynamic Model Clean Method]

    Args:
        selfObj ([Model Instance]): [self]
        qsFieldObjectList ([List]): [[{'qs': Model.objects.filter(title='abc'), 'field': 'title'}, ]]

    Raises:
        ValidationError: [Raises Django Validation Error]
    """
    
    errors = {}
    
    try:
    
        for obj in qsFieldObjectList:
            # perform validation
            qs = obj.get("qs", selfObj.__class__.objects.filter(id=None))
            field = obj.get("field", "Undefined")
            if initialObject:
                qs = qs.exclude(slug__iexact=initialObject.slug)
            
            if qs.exists():
                value = getattr(selfObj, field)
                errors[field] = [f"{selfObj.__class__.__name__} with this {field} ({value}) already exists!"]
                
    except Exception as E:
        errors["non-field-errors"] = [str(E)]
    
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


def validate_many_to_many_list(value, model, fieldName, allowBlank=False):
    """[Validates ManyToMany Field id List]

    Args:
        value ([List]): [mant to mant ids]
        model ([Django Model Class]): [Django Model Class]
        fieldName ([String]): [Many to Many Field Name]
        allowBlank (bool, optional): [If allow blank]. Defaults to False.

    Raises:
        serializers.ValidationError: [description]

    Returns:
        [List]: [Validate Value List]
    """
    
    if value == None or value == "":
        raise serializers.ValidationError({fieldName: "Expected List!"})

    if not type(value) == list:
        raise serializers.ValidationError({fieldName: "Expected List!"})
    
    if allowBlank == False:
        if type(value) == list and len(value) <= 0:
            raise serializers.ValidationError({fieldName: f"`{fieldName}` list can't be empty!"})
    else:
        if type(value) == list and len(value) <= 0:
            return value

    qs = model.objects.filter(id__in=value).values_list("id", flat=True)
    
    if qs:
        if not len(qs) == len(value):
            restricted_ids = []
            for v in value:
                if v not in qs:
                    restricted_ids.append(v)
            if len(restricted_ids) >= 1:
                raise serializers.ValidationError(
                    {fieldName: f"Invalid {fieldName}: {restricted_ids}"})
    else:
        raise serializers.ValidationError({fieldName: f"`{fieldName}` ({value}) not found!"})
    
    return value


def process_image_data(data: dict, image_fields: list) -> dict:
    """[Processes image data from request]

    Args:
        data ([Dictionary]): [request data object]
        image_fields ([List]): [List of image fields in request]

    Returns:
        [Dictionary]: [Request data object with processed image data]
    """
    
    for field in image_fields:
        image = data.get(field, None)

        if url_check(image):
            data.pop(field, None)

    return data


def get_exception_error_msg(errorObj, msg=None):
    """[Populates Exception Message from Exception Object and returns Response]

    Args:
        errorObj ([Exception]): [ex: E]
        msg ([String]): [ex: "update"]

    Returns:
        [Response]
    """
    try:
        error_details = {}
        if msg:
            msg = msg
        else:
            msg = "Failed!"
        
        if isinstance(errorObj, Http404):
            return ResponseWrapper(error_msg="Object not found!", msg=msg, error_code=404)
        
        if hasattr(errorObj, 'detail'):
            error_details = errorObj.detail
        else:
            try:
                error_details["details"] = errorObj.__str__()
            except:
                error_details["details"] = str(errorObj)
                
        return ResponseWrapper(error_msg=error_details, msg=msg, error_code=400)
    
    except Exception as E:
        return ResponseWrapper(error_msg=str(E), msg=msg, error_code=400)
