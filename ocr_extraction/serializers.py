from rest_framework import serializers

class DataSerializer(serializers.Serializer):
    image = serializers.ImageField(write_only = True)

class ExtractionSerializer(serializers.Serializer):
    screenshot_image = serializers.ListField(child = DataSerializer())