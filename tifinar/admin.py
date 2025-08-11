
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuthUser
from django.utils.translation import gettext_lazy as _  # أضف هذا الاستيراد

class AuthUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional Info'), {'fields': (
            'role', 'educational_level', 'ville_d_origine', 'adresse', 'etat_social',
            'date_de_naissance', 'gender', 'tel'
        )}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(AuthUser, AuthUserAdmin)