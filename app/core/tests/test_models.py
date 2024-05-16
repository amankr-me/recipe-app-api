"""
Test for models
"""

from decimal import Decimal 

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com',password='testpass123'):
    """Creat and rturn a new user"""
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email is normalized for new user."""

        sample_emails=[
            ['Test1@Example.com', 'Test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],

        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Test new user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')


    def test_create_superuser(self):
        """Test create super user."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_create_recipe(self):
        """Test creating recipe successfully"""
        user =get_user_model().objects.create_user(
            "test@example.com",
            "testpass123"
        )
        recipe= models.Recipe.objects.create(
            user=user,
            title="Sample Recipe Name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample Recipe Description"
        )
        print("tag")
        
        self.assertEqual(str(recipe),recipe.title)


    def tag_create_test(self):
        """Test reating a tag is successful"""
        print("tag2")
        user=create_user()
        tag=models.Tag.objects.create(user=user, name='Tag1')
        print("tag")
        self.assertEqual(str(tag),tag.name)


