
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuthUser, books, articles, cours, videos, exams, Examitems, comments, Contacts
from django.utils.translation import gettext_lazy as _  # أضف هذا الاستيراد

class AuthUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name','email', 'is_staff', 'role')
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
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_per_page = 20
class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'tel', 'email', 'ville_d_origine')
    list_filter = ('the_type', 'educational_level')
    search_fields = ('nom', 'prenom', 'email', 'tel')
    list_per_page = 20

    
    def get_full_name(self, obj):
        return f"{obj.prenom} {obj.nom}"
    get_full_name.short_description = 'الاسم الكامل'
    
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    list_filter = ('the_type', 'educational_level')  
    list_per_page = 20
      
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    list_filter = ('the_type', 'educational_level')    
    list_per_page = 20

    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    list_filter = ('the_type', 'educational_level')    
    list_per_page = 20

    
class CoursAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    list_filter = ('the_type', 'educational_level')    
    list_per_page = 20

    
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'the_type', 'educational_level')
    list_filter = ('the_type', 'educational_level')    
    list_per_page = 20

class ExamItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information de question', {
            'fields': ('qsts_id', 'qst_1st_line', 'qsts', 'the_type', 'dir'),
            'classes': ('collapse',)
        }),
        ('Correct answer', {
            'fields': ('correct_answer', 'if_choising_correct', 'mark'),
            'classes': ('collapse',)
        }),
        ('choices', {
            'fields': ('choice1', 'if_choising_1', 'choice2', 'if_choising_2', 'choice3', 'if_choising_3'),
            'classes': ('collapse',)
        }),
    ]
    list_display = ('exam_number', 'qsts_id', 'get_short_question', 'the_type', 'mark')
    list_display_links = ('qsts_id', 'get_short_question')  # رابط مزدوج
    list_filter = ('exam_number', 'the_type')    
    list_per_page = 20
    search_fields = ('qst_1st_line', 'qsts', 'qsts_id')
    
    def get_short_question(self, obj):
        """عرض جزء من السؤال في القائمة"""
        if obj.qst_1st_line:
            return obj.qst_1st_line[:50] + "..." if len(obj.qst_1st_line) > 50 else obj.qst_1st_line
        return "بدون عنوان"
    get_short_question.short_description = 'السؤال'
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('page_title','author_name', 'cmt_subject' )
    list_filter = ('page_title', 'author_name','updated_at')
    
    
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Contacts,ContactAdmin)
admin.site.register(articles, ArticleAdmin)
admin.site.register(videos, VideoAdmin)
admin.site.register(books, BookAdmin)
admin.site.register(cours, CoursAdmin)
admin.site.register(exams, ExamAdmin)
admin.site.register(Examitems, ExamItemsAdmin)
admin.site.register(comments, CommentAdmin)
