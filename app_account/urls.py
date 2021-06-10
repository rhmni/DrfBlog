from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'account'
urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('articles/', views.ArticleProfileView.as_view()),
    path('articles/<int:article_id>/', views.ArticleProfileView.as_view()),
    path('articles/create/', views.ArticleCreateProfileView.as_view()),
    path('articles/delete/<int:article_id>/', views.ArticleDeleteProfileView.as_view()),
    path('articles/update/<int:article_id>/', views.ArticleUpdateProfileView.as_view()),
]
