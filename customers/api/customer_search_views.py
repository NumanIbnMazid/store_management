from .serializers import CustomerSearchSerializer
from customers.models import Customer
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper, get_exception_error_msg
from dateutil import parser


class CustomerSearchManagerViewSet(LoggingMixin, CustomViewSet):

    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Customer.objects.all()
    lookup_field = "slug"
    
    def get_serializer_class(self):
        if self.action in ["check_customer_between_range"]:
            self.serializer_class = CustomerSearchSerializer
        return self.serializer_class

    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]

    
    def get_customer_from_range(self, start_date, end_date):
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)

        qs = Customer.objects.get_queryset(created_at__range=[start_date, end_date])
        customer_objects = []
        if qs.exists():
            for instance in qs:
                customer_objects.append(instance)
            return True, customer_objects
        return False, customer_objects
    
    def check_customer_between_range(self, request, *args, **kwargs):
        """ *** Parent Method for checking customer between range *** """
        
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                start_date = parser.parse(request.data.get("start_date", ""))
                formatted_start_date_str = start_date.strftime("%Y-%m-%d")

                end_date = parser.parse(request.data.get("end_date", ""))
                formatted_end_date_str = end_date.strftime("%Y-%m-%d")
                
                result = {
                    "start_date": formatted_start_date_str,
                    "end_date": formatted_end_date_str,
                    "status": False,
                    "total_customer": 0,
                    "customer": []
                }
                
                def prepare_customer_data(customer_qs=None):
                    customer_list = []
                    for customer in customer_qs:
                        data = {}
                        data["slug"] = customer.slug
                        data["furigana"] = customer.furigana
                        data["name_of_person_in_charge"] = customer.name_of_person_in_charge
                        data["postal_code"] = customer.postal_code
                        data["prefecture"] = customer.prefecture
                        data["address"] = customer.address
                        data["building_name"] = customer.building_name
                        data["contact_address"] = customer.contact_address
                        data["other_contact_information"] = customer.other_contact_information
                        data["identification"] = customer.identification
                        data["created_at"] = customer.created_at
                        data["updated_at"] = customer.updated_at
                        customer_list.append(data)
                    result['customer'] = customer_list
                    result['total_customer'] = len(customer_list)
                    return result
            
                # filter customer between date range
                customer_filter_result = self.get_customer_from_range(start_date=formatted_start_date_str, end_date=formatted_end_date_str)
                
                # prepare customer response data
                if customer_filter_result[0] == True:
                    prepare_customer_data(customer_qs=customer_filter_result[1])
                    result["status"] = True
                else:
                    result["status"] = False
                        
                return ResponseWrapper(data=result, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        except Exception as E:
            return ResponseWrapper(error_msg=get_exception_error_msg(errorObj=E), msg="Failed to get the result!", error_code=400)


     
