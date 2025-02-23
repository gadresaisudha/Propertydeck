from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Review, Property
from property.serializers import ReviewSerializer


def review_detail_url(property_id,review_id):
    return reverse('property:property-reviews-detail',kwargs={'property_id':property_id,'pk':review_id})

def property_review_list_url(property_id):
    return reverse('property:property-reviews-list',kwargs={'property_id':property_id})

def create_user():
    return get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

class PublicReviewApiTest(TestCase):
    """Test unauthorized API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving reviews"""

        res = self.client.get(property_review_list_url(1))
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateReviewApiTest(TestCase):
    """Test authorized API request"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@example.com','testpass123')
        self.client.force_authenticate(self.user)
        self.property = Property.objects.create(
            title="Luxury Apartment",
            price=100500.00,
            owner=self.user,
            area = 1500,
            city = 'hnk',
            state = 'Telangana',
            country = 'India')
        self.review1 = Review.objects.create(
            user=self.user,
            property=self.property,
            rating=4.5,
            comment="Great place, very clean!"
        )

        self.client1 = APIClient()
        self.user1 = get_user_model().objects.create_user(email="reviewer2@example.com", password="testpass")
        self.client1.force_authenticate(self.user1)
        self.review2 = Review.objects.create(
            user=self.user1,
            property=self.property,
            rating=5.0,
            comment="Amazing experience!"
        )

        self.client2 = APIClient()
        self.user2 = get_user_model().objects.create_user(email="reviewer3@example.com", password="testpass3")
        self.client2.force_authenticate(self.user2)

    def test_retrieve_reviews(self):
        url = property_review_list_url(self.property.id)
        res = self.client1.get(url)
        reviews = Review.objects.filter(property__id=self.property.id).order_by('-created_at')
        serializer = ReviewSerializer(reviews,many= True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_retrieve_review_detail(self):
        url = review_detail_url(self.property.id,self.review1.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_update_review(self):
        url = review_detail_url(self.property.id,self.review1.id)
        payload = {'rating':'3.5'}
        res = self.client.patch(url,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['rating'],payload['rating'])

    def test_create_review(self):
        url = property_review_list_url(self.property.id)
        payload = {'rating': '4.5','comment':'Amazing experience!'}
        res = self.client2.post(url,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(res.data['rating'],payload['rating'])

