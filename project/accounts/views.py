from django.shortcuts import render
from .models import User , Profile
from .serializers import UserSerializer , MyTokenObtainPairSerializer , RegisterSerializer , ChangePasswordSerializer

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
# for access and refresh token 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView

# Create your views here.





@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token/',
        'token/refresh/',
        'token/blacklist/',
        'register/',
        'test/',
    ]
    return Response(routes)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    # to get jwt after signup
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data['email'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response





class UserProfileView(RetrieveUpdateAPIView):
    """ show user data """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """ get current user data """
        return self.request.user





class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update_password(request.user)
            return Response({"message": "password updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)