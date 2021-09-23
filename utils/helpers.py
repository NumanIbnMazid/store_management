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
            "status_code": status_by_default_for_gz,
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
        # print(f"Failed to customize exception. Exception: {str(E)}")

    return response
