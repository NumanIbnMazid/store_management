from rest_framework import viewsets
from utils.helpers import ResponseWrapper

class CustomViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'

    def list(self, request):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, msg='success')

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, msg='created')
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def destroy(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        return ResponseWrapper(error_msg="failed to delete", error_code=400)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseWrapper(serializer.data)
    
    
