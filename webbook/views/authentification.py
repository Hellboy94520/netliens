import traceback
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from webbook.serializer import TokenObtainPairSerializer

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

# ------------------------------
# TMP :
# ------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView as JwtTokenObtainPairView
class TokenObtainPairView(JwtTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
