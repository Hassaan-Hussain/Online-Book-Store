from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Address

User = get_user_model()

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [AddressInline]

admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)

