from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import HiddenField, CurrentUserDefault, CharField
from rest_framework.serializers import ModelSerializer
from apps.models import Category
from rest_framework import serializers
from .models import Product


class RegisterModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    email = EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Bu email bazada bor')
        return value

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password and confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            data['is_active'] = False
            return data
        raise ValidationError("Parol mos emas")


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
