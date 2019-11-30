from rest_framework import serializers

class LilicSerializer(serializers.Serializer):
    music_name = serializers.CharField(max_length=20)
    artist_name = serializers.CharField(max_length=20)
