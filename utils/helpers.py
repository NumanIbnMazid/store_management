from rest_framework.views import exception_handler
from rest_framework.response import Response


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
            response_success = False

        output_data = {
            "error": {"code": error_code, "error_details": error_msg},
            "data": data,
            "status": response_success,
            "status_code": error_code if not error_code == "" and not error_code == None else status_by_default_for_gz,
            "message": msg if msg else str(error_msg) if error_msg else "Success" if response_success else "Failed",
        }
        if data_type is not None:
            output_data["type"] = data_type

        # status=200
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