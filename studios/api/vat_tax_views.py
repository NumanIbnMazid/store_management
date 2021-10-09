from .serializers import (VatTaxSerializer, VatTaxUpdateSerializer, StudioVatTaxSerializer)
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from studios.models import VatTax, Studio
from utils.helpers import ResponseWrapper

"""
    ----------------------- * Vat Tax * -----------------------
"""

class VatTaxManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = VatTax.objects.all()
    lookup_field = "slug"
     
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = VatTaxUpdateSerializer
        
        elif self.action in ["studio_vat_tax"]:
            self.serializer_class = StudioVatTaxSerializer
        else:
            self.serializer_class = VatTaxSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(VatTaxManagerViewSet, self)._clean_data(data)
    
    def get_studio_vat_tax(self,studio):
        qs = VatTax.objects.filter(studio=studio)
        if qs.exists():
            return True, qs.first()
        return False, None

    
    def studio_vat_tax(self, request, *args, **kwargs):
        """ *** Get studio Vat Tax *** """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            studio = int(request.data.get("studio", None))
            studio_qs = Studio.objects.filter(id=studio)
            studio_obj = None
            
            if studio_qs.exists():
                studio_obj = studio_qs.first()
            else:
                return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Studio {studio} does not exists!", status=400)

            result = {
                "studio": studio,
                "vattax":{}
            }
            
            def prepare_vat_tax_data(vat_tax_instance=None):
                print(vat_tax_instance)
                result["vattax"]["vat"] = vat_tax_instance.vat
                result["vattax"]["tax"] = vat_tax_instance.tax
                result["vattax"]["other_service"] = vat_tax_instance.other_service
                return result
    
            # get vat tax from DB
            vat_tax_filter_result = self.get_studio_vat_tax(studio=studio)
            
            # preapare vat tax data
            if vat_tax_filter_result[0] == True:
                prepare_vat_tax_data(vat_tax_instance=vat_tax_filter_result[1])
            else:
                result["status"] = False
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)

   

    
    