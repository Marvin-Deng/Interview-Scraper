from rest_framework import serializers
from .models import GlassdoorQuestion

class EmptySerializer(serializers.Serializer):
    pass

class GlassdoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlassdoorQuestion
        fields = ('id', 'date_posted', 'experience', 'question')