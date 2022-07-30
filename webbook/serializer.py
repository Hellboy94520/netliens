from rest_framework import serializers
from .models.user import User



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

# class NewCategorySerializer(serializers.ModelSerializer):
#   class Meta:
#     model = NewCategory
#     fields = '__all__'