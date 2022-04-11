from rest_framework import serializers
from .models.user import User
from .models.category import NewCategory

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class NewCategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = NewCategory
    fields = '__all__'