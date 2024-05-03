from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from news import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsAPIView.as_view(), name='news-api'),
    path('<int:pk>/', views.NewsDetailAPIView.as_view(), name='news-detail-api'),
    path('rps/', views.RPSAPIView.as_view(), name='rps-api'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
