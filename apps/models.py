from django.contrib.auth.models import User
from django.db.models import Model, CharField, BooleanField, TextField, ForeignKey, CASCADE, ImageField
from django_ckeditor_5.fields import CKEditor5Field


class Category(Model):
    name = CharField(max_length=255)
    description = CKEditor5Field(config_name='extends', null=True, blank=True)
    users = ForeignKey(User, CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Catigories'


class Product(Model):
    title = CharField(max_length=55)
    description = CKEditor5Field(config_name='extends', null=True, blank=True)
    collor = CharField(max_length=55)
    price = CharField(max_length=55)
    image = ImageField(upload_to='image/categories')
    users = ForeignKey(User, CASCADE)

    category = ForeignKey('apps.Category', CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
