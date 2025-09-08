from rest_framework import status, permissions
from rest_framework.views import APIView 
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .serializers import CustomUserSerializer



class UserCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "User Created", "user": serializer.data}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get("username")
        if username is None:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        password = request.data.get("password")
        if password is None:
            return Response({"message": "password is required"}, status=status.HTTP_400_BAD_REQUEST)


        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            serializer = CustomUserSerializer(user)
            return Response({"message": "Authorization is done", "user": serializer.data, "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            }, status=status.HTTP_200_OK )
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)