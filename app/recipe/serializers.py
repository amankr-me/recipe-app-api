"""
    Serializers for Recipe APIS
"""

from rest_framework import serializers

from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Seriaizer fo recipes"""
    
    class Meta:
        model =Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields= ['id']
        
        
class RecipeDetailsSerializer(RecipeSerializer):
    """Serializr for recipe detais view"""
    class Meta(RecipeSerializer.Meta):
        fields=RecipeSerializer.Meta.fields + ['description']
        
        
    