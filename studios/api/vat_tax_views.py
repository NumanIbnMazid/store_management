from .serializers import (VatTaxSerializer, VatTaxUpdateSerializer, StudioVatTaxSerializer)
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from studios.models import VatTax, Studio
from utils.helpers import ResponseWrapper
from utils.studio_getter_helper import (
    get_studio_id_from_studio
)
from django.db.models import Q

"""
    ----------------------- * Vat Tax * -----------------------
"""

class VatTaxManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = VatTax.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = VatTaxUpdateSerializer
        elif self.action in ["studio_vat_tax"]:
            self.serializer_class = StudioVatTaxSerializer
        else:
            self.serializer_class = VatTaxSerializer
        return self.serializer_class
    
    def get_permissions(self):
        if self.action in ["dynamic_list"]:
            permission_classes = [custom_permissions.IsStudioStaff]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(VatTaxManagerViewSet, self)._clean_data(data)
    
    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='success')
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)
        
    def dynamic_list(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser or request.user.is_staff:
                qs = self.get_queryset()
            elif request.user.is_studio_admin or request.user.is_store_staff:
                qs = self.get_queryset().filter(
                    Q(studio__slug__iexact=request.user.studio_user.slug) |
                    Q(studio__slug__iexact=request.user.store_moderator_user.store.all()[0].studio.slug)
                )
            else:
                qs = None
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list', status=200)
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)
    
    def get_studio_vat_tax(self, studio_id):
        qs = VatTax.objects.filter(studio=studio_id)
        if qs.exists():
            return True, qs.first()
        return False, None

    
    def studio_vat_tax(self, request, *args, **kwargs):
        """ *** Get studio Vat Tax *** """
        try:
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
                    "studio": studio_obj.name,
                    "vattax":{}
                }
                
                def prepare_vat_tax_data(vat_tax_instance=None):
                    result["vattax"]["vat"] = vat_tax_instance.vat
                    result["vattax"]["tax"] = vat_tax_instance.tax
                    result["vattax"]["other_service"] = vat_tax_instance.other_service
                    return result
        
                # get vat tax from DB
                vat_tax_filter_result = self.get_studio_vat_tax(studio_id=studio_obj.id)
                
                # preapare vat tax data
                if vat_tax_filter_result[0] == True:
                    prepare_vat_tax_data(vat_tax_instance=vat_tax_filter_result[1])
                else:
                    result["status"] = False
                        
                return ResponseWrapper(data=result, msg="retrieve", status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400, msg="retrieve")
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="retrieve", error_code=400)

   

    
    
