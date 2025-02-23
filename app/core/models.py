from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.conf import settings
from django.core.validators import RegexValidator
import uuid
import os


def property_image_file_path(instance,filename):
    """generate file path for new property image"""
    ext  = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads','property',filename)

# Create your models here.
class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self,email,password=None, **extra_fields):
        """create save and return a new user"""
        if not email:
            raise ValueError('user must have a email address')
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        """create save and return a new superuser"""
        if not email:
            raise ValueError('user must have a email address')
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    contact =  models.CharField(max_length=15, null=True)
    objects = UserManager()
    #email field used for authentication instead of default username
    USERNAME_FIELD = 'email'

class Property(models.Model):
    STATUS_CHOICES = [
        ('Available for Rent','for_rent'),
        ('Available for Purchase','for_sale'),
        ('Rented Out', 'rented_out'),
        ('Sold','sold'),
    ]
    """Property model"""

    """property description"""
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True,null=True)
    property_type = models.CharField(
        max_length=50,
        choices=[('Residential', 'Residential'), ('Commercial', 'Commercial')],
        blank= True,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='for_sale'
    )

    """Location details"""
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255,blank=True,null=True)
    zipcode = models.CharField(max_length=10, blank=True,null=True)

    """price and size details"""
    price = models.DecimalField(max_digits=15, decimal_places=2)
    area = models.FloatField()
    bedrooms = models.IntegerField(null=True)
    bathrooms = models.IntegerField(null=True)
    parking = models.BooleanField(null=True)
    furnishing = models.CharField(
        max_length=50,
        choices=[('Furnished', 'Furnished'), ('Semi-Furnished', 'Semi-Furnished'), ('Unfurnished', 'Unfurnished')],
        blank= True,
        null= True
    )

    """owner and user_review details"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


    """Additional info"""
    amenities = models.JSONField(default=list, blank=True,null=True)
    property_image = models.ImageField(upload_to=property_image_file_path,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='reviews')
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    comment =  models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','property')

    def __str__(self):
        return f'{self.user.name}-{self.property.title}-{self.rating}'
