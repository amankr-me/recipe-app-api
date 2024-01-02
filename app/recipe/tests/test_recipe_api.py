"""
Test for Recipe Api
"""
    
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer
    )

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create and Return recipe detail url"""
    return reverse('recipe:recipe-details',args=[recipe_id])


def create_recipe(user,**params):
    """Create and return a simpl Recipe"""
    defaults={
        'title':'Simple Recipe Name',
        'time_minutes':22,
        'price':Decimal('5.50'),
        'description':'Sample Decription',
        'link':'http://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe=Recipe.objects.create(user=user,**defaults)
    return recipe

class PublicRecipeApiTests(TestCase):
    """Test unauthenticated API Request"""
    def setUp(self):
        self.client= APIClient()
    
    def test_auth_required(self):
        """Test auth is required for API calls"""
        res=self.client.get(RECIPES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateRecipeApiTest(TestCase):
    """Test authenticated api request"""
    def setUp(self):
        self.client=APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)
        
    def test_retrive_recipe(self):
        """Test reciving list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipe = Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipe,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK) 
        self.assertEqual(res.data, serializer.data)
        
    def test_recipe_list_limited_to_user(self):
        """Test list of recipe is limited to authentiated user"""
        other_user=get_user_model().objects.create_user(
            'other@example.com'
            'password123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipe = Recipe.objects.filter(user=self.user)
        serializer=RecipeSerializer(recipe,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK) 
        self.assertEqual(res.data, serializer.data)     
        
        
    def test_get_recipe_detais(self):
        """Test gett recipe detais"""
        
        recipe=create_recipe(user=self.user)
        url= detail_url(recipe.id)
        res=self.client.get(url)
        
        serializer=RecipeDetailsSerializer(recipe)
        
        self.assertEqual(res.data,serializer.data)