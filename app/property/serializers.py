"""
serializers for property apis
"""

from rest_framework import serializers
from core.models import Property, Review

class PropertySerializer(serializers.ModelSerializer):
    """Serializer for property"""
    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "title",
            "status",
            "city",
            "state",
            "country",
            "price",
            "area",
        ]
        read_only_fields = ['id','owner']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review"""
    class Meta:
        model = Review
        fields = ['id','user','property','rating','comment','created_at','updated_at']
        read_only_fields = ['id','user','property','created_at','updated_at']

class PropertyDetailSerializer(PropertySerializer):
    """Serializer for property detail view"""
    reviews = ReviewSerializer(many=True,read_only=True)
    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + [ "description", "address",
            "zipcode","bedrooms",
            "bathrooms",
            "parking",
            "furnishing",
            "amenities",
            "property_type",
            "property_image",
            'created_at',
            'updated_at',
            'reviews'
            ]
        read_only_fields = ['id','owner','created_at','updated_at','reviews']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id','property_image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required':'True'}}


