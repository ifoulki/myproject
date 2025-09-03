from django import forms
from django.core.exceptions import ValidationError
from tifinar.models import Contacts
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
import os

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class ContactForm(forms.ModelForm):
    EDUCATIONAL_LEVEL_CHOICES = [
        ('', 'اختر المستوى التعليمي'),
        ('0', 'لا، المقال مناسب للجميع'),
        ('الإبتدائي :', [
            ('1', 'السنة الأولى ابتدائي'),
            ('2', 'السنة الثانية ابتدائي'),
            ('3', 'السنة الثالثة ابتدائي'),
            ('4', 'السنة الرابعة ابتدائي'),
            ('5', 'السنة الخامسة ابتدائي'),
            ('6', 'السنة السادسة ابتدائي'),
        ]),
        ('الإعدادي :', [
            ('7', 'السنة الأولى إعدادي'),
            ('8', 'السنة الثانية إعدادي'),
            ('9', 'السنة الثالثة إعدادي'),
        ]),
        ('الثانوي :', [
            ('10', 'المشترك العلمي'),
            ('11', 'السنة الأولى من البكالوريا (تخصص علوم تجريبية)'),
            ('12', 'السنة الثانية من البكالوريا (تخصص علوم فيزيائية)'),
        ]),
        ('ما بعد الثانوي :', [
            ('13', 'الدراسة بعد البكالوريا'),
        ])
    ]
    
    GENDER_CHOICES = [
        ('', 'اختر الجنس'),
        ('Female', 'أنثى'),
        ('Male', 'ذكر'),
        ('Other', 'أخرى'),
        ('Unknown', 'غير معروف')
    ]
    
    ETAT_SOCIAL_CHOICES = [
        ('', 'اختر الحالة الاجتماعية'),
        ('Single', 'أعزب'),
        ('Married', 'متزوج'),
        ('Divorced', 'مطلق'),
        ('Widowed', 'أرمل'),
        ('Unknown', 'غير معروف')
    ]
    
    path = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        help_text="يمكنك اختيار ملفات متعددة."
    )
    
    educational_level = forms.ChoiceField(
        choices=EDUCATIONAL_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('المستوى التعليمي'),
        required=False
    )
        
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('الجنس'),
        required=False
    )
    
    etat_Social = forms.ChoiceField(
        choices=ETAT_SOCIAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('الحالة الاجتماعية'),
        required=False
    )
    
    class Meta:
        model = Contacts
        fields = '__all__'
        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الشخصي'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم العائلي'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهاتف'
            }),
            'the_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نوع العضو'
            }),
            'societe': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الشركة أو المؤسسة'
            }),
            'ville_d_origine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'المدينة الأصلية'
            }),
            'social_media': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'حسابات وسائل التواصل'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'العنوان الكامل'
            }),
            'date_de_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ideologie': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'الآراء الدينية والسياسية'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'معلومات إضافية'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'الكلمات المفتاحية مفصولة بفواصل'
            }),
            'spouse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الزوج/الزوجة'
            }),
            'children': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أسماء الأبناء'
            }),
            'siblings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أسماء الإخوة والأخوات'
            }),
            'parents': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'معلومات عن الوالدين'
            }),
            'maternal_relatives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أقارب جهة الأم'
            }),
            'paternal_relatives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أقارب جهة الأب'
            }),
            'grandparents': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'معلومات عن الأجداد'
            }),
            'friends': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أسماء الأصدقاء'
            }),
            'name_in_arabic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الاسم باللغة العربية'
            }),
            'author': forms.HiddenInput(),
        }
    
    def clean_path(self):
        files = self.cleaned_data.get('path')
        if not files:
            return files
            
        if not isinstance(files, list):
            files = [files]
            
        for file in files:
            # التحقق من نوع الملف
            valid_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.svg', '.webp']
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("نوع الملف غير مدعوم. يرجى تحميل صورة بصيغة: jpeg, png, jpg, gif, svg, webp")
            
            # التحقق من حجم الملف (2MB)
            if file.size > 2 * 1024 * 1024:
                raise ValidationError("حجم الملف كبير جداً. الحد الأقصى هو 2MB")
        
        return files
