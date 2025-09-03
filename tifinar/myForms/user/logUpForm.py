from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from tifinar.models import AuthUser


class AuthUserCreationForm(UserCreationForm):
    """نموذج إنشاء مستخدم مخصص مع المستوى التعليمي"""
    
    EDUCATIONAL_LEVEL_CHOICES = [
        ('0', 'غير محدد'),
        ('1', 'السنة الأولى ابتدائي'),
        ('2', 'السنة الثانية ابتدائي'),
        ('3', 'السنة الثالثة ابتدائي'),
        ('4', 'السنة الرابعة ابتدائي'),
        ('5', 'السنة الخامسة ابتدائي'),
        ('6', 'السنة السادسة ابتدائي'),
        ('7', 'السنة الأولى إعدادي'),
        ('8', 'السنة الثانية إعدادي'),
        ('9', 'السنة الثالثة إعدادي'),
        ('10', 'الجدع المشترك'),
        ('11', 'السنة الأولى بكالوريا'),
        ('12', 'السنة الثانية بكالورية'),
        ('13', 'التعليم العالي')
    ]
    
    educational_level = forms.ChoiceField(
        choices=EDUCATIONAL_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('المستوى التعليمي'),
        required=False,
        initial='0'
    )
    
    class Meta:
        model = AuthUser
        fields = ('username', 'first_name', 'last_name', 'email', 'educational_level', 'gender', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تحسين مظهر الحقول بشكل موحد
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class MultipleFileInput(forms.ClearableFileInput):
    """وسيلة إدخال لملفات متعددة"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """حقل ملفات متعددة"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """تنظيف البيانات للملفات المتعددة"""
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result