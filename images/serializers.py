from rest_framework import serializers
from blog.models import *

class ResponsiveImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ResponsiveImage
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }