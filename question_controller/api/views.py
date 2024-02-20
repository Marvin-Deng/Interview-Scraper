from django.shortcuts import render
from rest_framework import generics
from .models import GlassdoorQuestion
from .serializers import GlassdoorSerializer

class GlassdoorView(generics.ListAPIView):
    queryset = GlassdoorQuestion.objects.all()
    serializer_class = GlassdoorSerializer
