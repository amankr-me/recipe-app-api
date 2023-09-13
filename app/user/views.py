"""
view for the user api
"""

from rest_framework import generics
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the syatem"""
    serializer_class = UserSerializer
