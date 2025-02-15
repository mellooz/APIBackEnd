from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView , TokenBlacklistView

urlpatterns = [
    # Token url (login) when go to that url u login then take the token 
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refresh token url
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # SignUp url
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    # logout url
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # update user data 
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),

    # change password
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    path('test/', views.testEndPoint, name='test'),
    path('', views.getRoutes),
]
