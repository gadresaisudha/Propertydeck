"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models
from unittest.mock import patch

def create_user():
    return get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

def create_property(user):
    return models.Property.objects.create(
            owner = user,
            title="Modern Apartment in Downtown",
            description="A 3BHK apartment with a modern design and stunning views.",
            property_type="Residential",
            status="Available",
            city="San Francisco",
            state="California",
            country="USA",
            address="456 Market Street",
            zipcode="94103",
            price=750000,
            area=1500,
            bedrooms=3,
            bathrooms=2,
            parking=True,
            furnishing="Semi-Furnished",
            amenities=["Gym", "Swimming Pool", "Power Backup"],
        )

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test for creating a user with email"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]
        for email,expected in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_withoout_email_raises_error(self):
        """Test that create a user without email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        """Test create a superuser"""
        user = get_user_model().objects.create_superuser('test@example.com','test123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_property(self):
        """Test create a property is successful"""
        user = create_user()
        property =create_property(user)

        # Assertions to verify the property was created successfully
        self.assertEqual(property.owner, user)
        self.assertEqual(property.title, "Modern Apartment in Downtown")
        self.assertEqual(property.price, 750000)
        self.assertEqual(property.bedrooms, 3)
        self.assertTrue(property.parking)
        self.assertIn("Gym", property.amenities)
        self.assertTrue(models.Property.objects.filter(title="Modern Apartment in Downtown").exists())

    def test_create_review(self):
        user = create_user()
        property = create_property(user)
        review = models.Review.objects.create(user = user,property=property,rating = 4)
        self.assertEqual(review.user,user)
        self.assertEqual(review.property,property)

    @patch('core.models.uuid.uuid4')
    def test_property_file_name_uuid(self,mock_uuid):
        """Test generating image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.property_image_file_path(None,'example.jpg')
        self.assertEqual(file_path,f'uploads/property/{uuid}.jpg')
