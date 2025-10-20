from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .choices import *

class CommonModelMixin:
    """Mixin يحتوي على الوظائف المشتركة بين جميع الموديلات"""
    
    def __str__(self):
        return self.title or 'بدون عنوان'

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def get_title(self):
        return self.title or 'بدون عنوان'

    def clean(self):
        if hasattr(self, 'min_age') and hasattr(self, 'max_age'):
            if self.min_age and self.max_age and self.min_age > self.max_age:
                raise ValidationError('الحد الأدنى للعمر يجب أن يكون أقل من الحد الأقصى')
            
            if self.min_age < 2 or self.min_age > 75:
                raise ValidationError('الحد الأدنى للعمر يجب أن يكون بين 2 و 75')
            
            if self.max_age < 2 or self.max_age > 75:
                raise ValidationError('الحد الأقصى للعمر يجب أن يكون بين 2 و 75')

    def get_educational_level_display(self):
        """عرض قيمة educational_level بشكل مقروء"""
        return dict(EducationalLevel.choices).get(self.educational_level, 'غير معروف')

    def get_gender_display(self):
        """عرض قيمة gender بشكل مقروء"""
        return dict(Gender.choices).get(self.gender, 'غير معروف')

    def get_visibility_status_display(self):
        """عرض قيمة visibility_status بشكل مقروء"""
        return dict(VisibilityStatus.choices).get(self.visibility_status, 'غير معروف')

    def get_dir_display(self):
        """عرض قيمة dir بشكل مقروء"""
        return dict(Dir.choices).get(self.dir, 'غير معروف')