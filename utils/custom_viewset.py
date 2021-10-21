from rest_framework import viewsets
from utils.helpers import ResponseWrapper, get_exception_error_msg
from django.db.models import Q

class CustomViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'

    def list(self, request):
        try:
            qs = self.get_queryset()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg="list", status=200)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")
       
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
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")

    def create(self, request):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                qs = serializer.save()
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, msg="create", status=200)
            return ResponseWrapper(error_msg=serializer.errors, msg="create", error_code=400)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="create")

    def update(self, request, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True, context={
                "initialObject": self.get_object(), "requestObject": request
            })
            if serializer.is_valid():
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, msg="update", status=200)
            return ResponseWrapper(error_msg=serializer.errors, msg="update", error_code=400)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="update")

    def destroy(self, request, **kwargs):
        try:
            qs = self.queryset.filter(**kwargs).first()
            if qs:
                qs.delete()
                return ResponseWrapper(msg="delete", status=200)
            return ResponseWrapper(error_msg="Failed to delete!", msg="delete", error_code=400)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="delete")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return ResponseWrapper(data=serializer.data, msg="retrieve", status=200)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="retrieve")
    
    
