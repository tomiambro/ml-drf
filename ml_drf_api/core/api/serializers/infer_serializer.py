from rest_framework import serializers


class InferSerializer(serializers.Serializer):
    input = serializers.ListField(child=serializers.FloatField())
