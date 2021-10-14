from rest_framework import viewsets
from utils.helpers import ResponseWrapper

class CustomViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'

    def list(self, request):
        try:
            qs = self.get_queryset()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='List retrieved successfully!', status=200)
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="Failed to retrieve the list!", error_code=400)

    def create(self, request):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                qs = serializer.save()
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, msg='Created successfully!', status=200)
            return ResponseWrapper(error_msg=serializer.errors, msg="Failed to create!", error_code=400)
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="Failed to create!", error_code=400)

    def update(self, request, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, msg="Updated successfully!", status=200)
            return ResponseWrapper(error_msg=serializer.errors, msg="Failed to update!", error_code=400)
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="Failed to update!", error_code=400)

    def destroy(self, request, **kwargs):
        try:
            qs = self.queryset.filter(**kwargs).first()
            if qs:
                qs.delete()
                return ResponseWrapper(msg='Deleted successfully!', status=200)
            return ResponseWrapper(error_msg="Failed To Delete", msg="Failed to delete!", error_code=400)
        except Exception as E:
            return ResponseWrapper(error_msg=str(E), msg="Failed to delete!", error_code=400)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return ResponseWrapper(data=serializer.data, msg='Object retrieved successfully!', status=200)
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg=f"Failed to retrieve the object!", error_code=400)
    
    
