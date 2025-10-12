from django import forms
from django.core.exceptions import ValidationError
from tifinar.models import videos
from tifinar.choices import *
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os

User = get_user_model()

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
    
class BaseContentForm(forms.ModelForm):
    
    dir = forms.ChoiceField(
        choices=Dir.choices,
        widget=forms.Select(attrs={
            'class': 'small-input',
            'placeholder': 'اختر اللغة'
        }),
        label=' عنوان الفيديو مكتوب بأي لغة؟',
        initial='',
        required=False
    )

    educational_level = forms.ChoiceField(
        choices=EducationalLevel.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='المستوى الدراسي المطلوب',
        required=False
    )
    
    gender = forms.TypedChoiceField(
        choices=Gender.choices,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='موجه لـ',
        initial='all',
        required=False,
        empty_value='all',
        coerce=str
    )
    
    # 🔥 إزالة حقل visibility_status من الفورم نهائياً
    # سنتعامل معه يدوياً في الـ view
        
    class Meta:
        abstract = True
        fields = [] 

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 7:
            raise forms.ValidationError('يجب أن يكون العنوان لا يقل عن 7 أحرف.')
        return title

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if author and len(author.strip()) < 5:
            raise forms.ValidationError('اسم الكاتب يجب أن لا يقل عن 5 أحرف.')
        return author

    def clean_min_age(self):
        min_age = self.cleaned_data.get('min_age')
        if min_age is not None and (min_age < 2 or min_age > 75):
            raise forms.ValidationError('العمر الأدنى يجب أن يكون بين 2 و75.')
        return min_age

    def clean_max_age(self):
        max_age = self.cleaned_data.get('max_age')
        if max_age is not None and (max_age < 2 or max_age > 75):
            raise forms.ValidationError('العمر الأقصى يجب أن يكون بين 2 و75.')
        return max_age

    def clean(self):
        cleaned_data = super().clean()
        min_age = cleaned_data.get('min_age')
        max_age = cleaned_data.get('max_age')
        if min_age and max_age and min_age >= max_age:
            raise forms.ValidationError('يجب أن يكون الحد الأدنى للعمر أصغر من الحد الأقصى.')
        return cleaned_data

    def clean_myimage(self):
        return self._validate_file('myimage', ['.jpeg', '.png', '.jpg', '.gif', '.svg', '.webp'], 5)
    
    def clean_autre(self):
        return self._validate_file('autre', ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.zip', '.rar'], 10)
    
    def _validate_file(self, field_name, valid_extensions, max_size_mb):
        file = self.cleaned_data.get(field_name)
        
        # إذا كان file هو نص (تم تمريره من خلال التعديل)
        if isinstance(file, str):
            return file
        
        if file:
            # التحقق من الامتداد
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError(f'نوع الملف غير مسموح به. المسموح: {", ".join(valid_extensions)}')
            
            max_size = max_size_mb * 1024 * 1024
            if file.size > max_size:
                raise ValidationError(f'حجم الملف يجب أن لا يتجاوز {max_size_mb} ميجابايت.')
        
        return file
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not hasattr(instance, 'slug') or not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

class VideoForm(BaseContentForm):
    
    TYPE_CHOICES = [
        ('', 'اختر صنف الفيديو'),
        ('الآداب :', [
            ('أديان', 'أديان'),
            ('فلسفة', 'فلسفة'),
        ]),
        ('الغات :', [
            ('الأمازيغية', 'تعلم الأمازيغية'),
            ('العربية', 'تعلم العربية'),
            ('الفرنسية', 'تعلم الفرنسية'),
            ('الإنجليزية', 'تعلم الإنجليزية'),
        ]),
        ('العلوم :', [
            ('علوم الحاسوب', 'علوم الحاسوب'),
            ('رياضيات', 'تعلم الرياضيات'),
            ('الكيمياء', 'الكيمياء'),
            ('الفزياء', 'الفزياء'),
            ('علوم الحياة والأرض', 'علوم الحياة والأرض'),
        ]),
        ('مواضيع أخرى :', [
            ('صحة وحياة', 'صحة وحياة'),
            ('حقوق الإنسان', 'القانون وحقوق الإنسان'),
            ('الثقافة العامة', 'الثقافة العامة'),
            ('تربية وتعليم', 'تربية وتعليم'),
            ('أصناف أخرى', 'أصناف أخرى'),
        ])
    ]
    
    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        }),
        label='نوع الفيديو',
        required=False
    )
   
    class Meta(BaseContentForm.Meta):
        model = videos
        
        # 🔥 إزالة visibility_status من الحقول
        fields = [
            'title', 'mysubject', 'mydescription', 
            'keywords', 'author', 'myimage', 'autre', 'gender',
            'the_type', 'educational_level', 'min_age', 'max_age', 'dir','visibility_status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الفيديو ...',
                'minlength': '2',
                'required': True
            }),
            'mysubject': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'videoInput',
                'placeholder': 'ألصق رابط فيديو YouTube هنا'
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'أكتب وصفًا لمحتوى الفيديو ...'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'keywords',
                'placeholder': 'الكلمات المفتاحية ...'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'من هو صاحب الفيديو ؟ ...',
                'minlength': '5',
                'maxlength': '50'
            }),
            'the_type': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'educational_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'min_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الحد الأدنى',
            }),
            'max_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الحد الأقصى',
            }),
            'myimage': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'formFile1'
            }),
            'autre': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'formFile2'
            }),
        }
        labels = {
            'title': 'عنوان الفيديو',
            'author': 'اسم صاحب الفيديو',
            'mysubject': 'رابط الفيديو',
            'mydescription': 'وصف لمحتوى الفيديو',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'موضوع الفيديو',
            'gender': 'الفيديو موجه',
            'educational_level': 'المستوى الدراسي',
            'min_age': 'الحد الأدنى للعمر',
            'max_age': 'الحد الأقصى للعمر',
            'myimage': 'الصورة الرئيسية',
            'autre': 'مرفقات إضافية',
            'visibility_status': 'مرفقات إضافية',
        }