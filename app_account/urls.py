from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'account'
urlpatterns = [
    # token urls
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/register/', views.UserRegisterView.as_view()),

    # change password url
    path('profile/change-password/', views.ChangePasswordView.as_view()),

    path('phone/send/', views.SendSmsView.as_view()),
    path('phone/verification/', views.VerificationPhoneView.as_view()),
]
