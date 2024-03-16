from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView

)

from apps.views import RegisterCreateAPIView, ConfirmEmailAPIView, ProductChangeAPIView, ProductDeleteAPIView, \
    ProductListAPIView, CategoryListAPIView, ProductByCategoryListAPIView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/sign-up', RegisterCreateAPIView.as_view(), name='register'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/category/<str:category_name>/', ProductByCategoryListAPIView.as_view(), name='product-by-category'),
    path('confirm-email/<uuid:pk>', ConfirmEmailAPIView.as_view(), name='register'),
    path('products/<int:pk>/', ProductChangeAPIView.as_view(), name='product-change'),
    path('products/<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
]