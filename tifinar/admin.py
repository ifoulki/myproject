
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuthUser, books, articles, cours, videos, exams, Examitems, comments, Contacts
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

class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'tel', 'email', 'ville_d_origine')
    list_filter = ('ville_d_origine', 'the_type', 'educational_level')
    search_fields = ('nom', 'prenom', 'email', 'tel')
    
    def get_full_name(self, obj):
        return f"{obj.prenom} {obj.nom}"
    get_full_name.short_description = 'الاسم الكامل'
    
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    
class CoursAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    
class ExamItemsAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Contacts,ContactAdmin)
admin.site.register(articles)
admin.site.register(videos)
admin.site.register(books, BookAdmin)
admin.site.register(cours)
admin.site.register(exams)
admin.site.register(Examitems)
admin.site.register(comments)
