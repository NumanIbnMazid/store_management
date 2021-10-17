from rest_framework import viewsets
from utils.helpers import ResponseWrapper

class CustomViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'

    def list(self, request):
        try:
            qs = self.get_queryset()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg="list", status=200)
        except Exception as E:
           return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)

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
            return ResponseWrapper(error_msg=str(E), msg="create", error_code=400)

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
            return ResponseWrapper(error_msg=str(E), msg="update", error_code=400)

    def destroy(self, request, **kwargs):
        try:
            qs = self.queryset.filter(**kwargs).first()
            if qs:
                qs.delete()
                return ResponseWrapper(msg="delete", status=200)
            return ResponseWrapper(error_msg="Failed to delete!", msg="delete", error_code=400)
        except Exception as E:
            return ResponseWrapper(error_msg=str(E), msg="delete", error_code=400)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return ResponseWrapper(data=serializer.data, msg="retrieve", status=200)
        except Exception as E:
            return ResponseWrapper(error_msg=str(E), msg="retrieve", error_code=400)
    
    
