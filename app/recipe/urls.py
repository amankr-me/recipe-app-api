"""
URL mappings for  the recpe api    
    """
    
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router=DefaultRouter()
router.register('recipe',views.RecipeViewset)
router.register('tags',views.TagsViewset)
router.register('ingredients', views.IngredientViewSet)


app_name='recipe'

urlpatterns = [
    path('',include(router.urls))
]
