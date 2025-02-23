"""
views for the property APIS
"""
from rest_framework import (viewsets,mixins,status)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.models import Property, Review
from property import serializers
from property.permissions import IsReviewOwnerOrReadOnly

class PropertyViewSet(viewsets.ModelViewSet):
    """View for manage property APIS"""
    serializer_class = serializers.PropertyDetailSerializer
    queryset = Property.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.PropertySerializer
        elif self.action == 'upload_image':
            return serializers.PropertyImageSerializer
        return self.serializer_class

    def perform_create(self,serializer):
        """Create a new property"""
        serializer.save(owner = self.request.user)

    @action(methods=['POST'],detail=True,url_path='upload-image')
    def upload_image(self,request,pk=None):
        """upload an image to property"""
        property = self.get_object()
        serializer = self.get_serializer(property,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """view for manage reviews APIS"""
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsReviewOwnerOrReadOnly]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')

        # If 'property_id' is provided, filter reviews by the property
        if property_id:
            return self.queryset.filter(property__id=property_id).order_by('-created_at')

    def perform_create(self,serializer):
        property_id = self.kwargs.get('property_id')
        property_instance = get_object_or_404(Property, id=property_id)
        serializer.save(user=self.request.user, property=property_instance)
