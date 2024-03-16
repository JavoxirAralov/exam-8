from django.contrib.admin import action
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from apps.serializers import RegisterModelSerializer, CategoryModelSerializer, ProductListModelSerializer
from apps.utils import send_verification_email
from rest_framework import permissions
from rest_framework.response import Response

from rest_framework import generics, filters
from models import Product, Category


class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

    def get_success_headers(self, data):
        import uuid
        _uuid = uuid.uuid4()
        send_verification_email(data['email'], _uuid.__str__())
        cache.set(_uuid, data['email'])
        print('sent email!')
        return super().get_success_headers(data)


class ConfirmEmailAPIView(APIView):
    def get(self, request, pk):
        email = cache.get(pk)
        User.objects.filter(email=email).update(is_active=True)
        return Response({'message': 'User confirmed email!'})


class ProductChangeAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(owner_id=self.request.user.id)

    @action(['get'], True, 'category', queryset=Category.objects.all(),
            serializer_class=CategoryModelSerializer)
    def category(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductByCategoryListAPIView(generics.ListAPIView):
    serializer_class = ProductListModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Product.objects.filter(category__name=category_name)
