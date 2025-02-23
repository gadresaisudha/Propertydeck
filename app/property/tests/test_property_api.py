from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Property
from property.serializers import PropertySerializer, PropertyDetailSerializer
import tempfile
import os
from PIL import Image

PROPERTY_URL = reverse('property:property-list')



def detail_url(property_id):
    return reverse('property:property-detail',args=[property_id])

def image_upload_url(property_id):
    """Create and return a property detail url"""
    return reverse('property:property-upload-image',args=[property_id])

def create_property(user, **params):
    """Create and return a simple property"""
    defaults = {
        'title':"Modern Apartment in Downtown",
        'description':"A 3BHK apartment with a modern design and stunning views.",
        'property_type':"Residential",
        'status':"Available",
        'city':"San Francisco",
        'state':"California",
        'country':"USA",
        'address':"456 Market Street",
        'zipcode':"94103",
        'price':750000,
        'area':1500,
        'bedrooms':3,
        'bathrooms':2,
        'parking':True,
        'furnishing':"Semi-Furnished",
        'amenities':["Gym", "Swimming Pool", "Power Backup"],
    }
    defaults.update(params)
    property = Property.objects.create(owner=user,**defaults)
    return property

class PublicPropertyAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(PROPERTY_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivatePropertyAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)


    def test_retrieve_properties(self):
        """Test retrieving list of property"""
        create_property(user=self.user)
        create_property(user=self.user)

        res = self.client.get(PROPERTY_URL)

        properties =  Property.objects.all().order_by('-id')
        serializer = PropertySerializer(properties,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_get_property_detail(self):
        """Test get property detail"""
        property = create_property(user=self.user)
        url = detail_url(property.id)
        res = self.client.get(url)
        serializer = PropertyDetailSerializer(property)
        self.assertEqual(res.data,serializer.data)


    def test_create_property(self):
        """Test create property"""
        payload = {
            'title':"Modern Apartment in Downtown",
            'city':"San Francisco",
            'state':"California",
            'country':"USA",
            'price':750000,
            'area':1500,
        }
        res = self.client.post(PROPERTY_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        property = Property.objects.get(id=res.data['id'])
        for k,v in payload.items():
            self.assertEqual(getattr(property,k),v)
        self.assertEqual(property.owner,self.user)

class ImageUploadTests(TestCase):
    """Tests for the image upload API"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user@example.com','pass123')
        self.client.force_authenticate(self.user)
        self.property = create_property(user=self.user)

    def tearDown(self):
        return self.property.property_image.delete()


    def test_upload_image(self):
        """Test uploading an image to a recipe"""
        url = image_upload_url(self.property.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img  = Image.new('RGB',(10,10))
            img.save(image_file,format='JPEG')
            image_file.seek(0)
            payload = {'property_image':image_file}
            res = self.client.post(url,payload,format='multipart')
        self.property.refresh_from_db()
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('property_image',res.data)
        self.assertTrue(os.path.exists(self.property.property_image.path))

