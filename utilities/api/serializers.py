from rest_framework import serializers


class DjangoFakerSerializer(serializers.Serializer):
    is_faked = serializers.BooleanField(default=True)
    insertedPks = serializers.ListField(read_only=True)
