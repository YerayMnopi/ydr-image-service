from django.shortcuts import render
from rest_framework import viewsets
from images.serializers import *
from images.models import *


class ResponsiveImageViewSet(viewsets.ModelViewSet):
    queryset = ResponsiveImage.objects.all()
    serializer_class = ResponsiveImageSerializer
    lookup_field = 'slug'