from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from apps.models import Category, Product




@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                'fields': (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )



@admin.register(Category)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Product)
class BlogModelAdmin(ModelAdmin):
    pass
admin.site.unregister(Group)