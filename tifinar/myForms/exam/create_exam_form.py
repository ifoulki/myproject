from django import forms
from django.core.exceptions import ValidationError
from tifinar.models import exams
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import os 
import re  # أضف هذا السطر
import time

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
    DIR_CHOICES = [
        ('', 'مقدمة الاختبار مكتوبة بأي لغة؟'),
        ('rtl', 'العربية'),
        ('ltr', 'Français'),
        ('ltr', 'English')
    ]
    
    GENDER_CHOICES = [
        ('male', 'للدكور فقط'),
        ('female', 'للإناث فقط'),
        ('all', 'لل الجميع'),
    ]
     
    EDUCATIONAL_LEVEL_CHOICES = [
        ('0', 'لا، الاختبار مناسب للجميع'),
        ('الإبتدائي', [
            ('1', 'السنة الأولى ابتدائي'),
            ('2', 'السنة الثانية ابتدائي'),
            ('3', 'السنة الثالثة ابتدائي'),
            ('4', 'السنة الرابعة ابتدائي'),
            ('5', 'السنة الخامسة ابتدائي'),
            ('6', 'السنة السادسة ابتدائي'),
        ]),
        ('الإعدادي', [
            ('7', 'السنة الأولى إعدادي'),
            ('8', 'السنة الثانية إعدادي'),
            ('9', 'السنة الثالثة إعدادي'),
        ]),
        ('الثانوي', [
            ('10', 'المشترك العلمي'),
            ('11', 'السنة الأولى بكالوريا '),
            ('12', 'السنة الثانية بكالوريا '),
        ]),
        ('ما بعد الثانوي', [
            ('13', 'الدراسة بعد البكالوريا'),
        ])
    ]
    
    dir = forms.ChoiceField(
        choices=DIR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select small-input',
            'placeholder': 'اختر اللغة'
        }),
        label=' مقدمة الاختبار مكتوبة بأي لغة؟',
        required=True
    )

    educational_level = forms.ChoiceField(
        choices=EDUCATIONAL_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='المستوى الدراسي المطلوب',
        required=False
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='موجه لـ',
        initial='all',
        required=False
    )
    
    min_age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'الحد الأدنى للعمر',
            'min': '2',
            'max': '72'
        }),
        initial=2,
        required=False
    )
    
    max_age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'الحد الأقصى للعمر',
            'min': '2',
            'max': '75'
        }),
        initial=75,
        required=False
    )
        
    class Meta:
        abstract = True
        fields = [] 

    def clean_title(self):
        try:
            title = self.cleaned_data.get('title')
            if not title or len(title.strip()) < 2:
                raise forms.ValidationError('يجب أن يكون العنوان لا يقل عن 2 أحرف.')
            return title.strip()
        except Exception as e:
            print(f"خطأ في التحقق من العنوان: {str(e)}")
            raise forms.ValidationError('حدث خطأ في التحقق من العنوان. يرجى المحاولة مرة أخرى.')

    def clean_myimage(self):
        try:
            file = self.cleaned_data.get('myimage')
            
            # إذا كان الملف نصاً أو None، نرجعه كما هو
            if file is None or isinstance(file, str):
                return file
            
            # إذا كان كائن ملف، نتحقق من الامتداد
            if hasattr(file, 'name') and file.name:
                ext = os.path.splitext(file.name)[1].lower()
                valid_extensions = ['.jpeg', '.png', '.jpg', '.gif', '.svg', '.webp']
                if ext and ext not in valid_extensions:
                    raise ValidationError(f'نوع الملف غير مسموح به. المسموح: {", ".join(valid_extensions)}')
            
            return file
            
        except ValidationError:
            raise  # نعيد ValidationError للمستخدم
        except Exception as e:
            print(f"خطأ غير متوقع في تحقق صورة الاختبار: {str(e)}")
            # نعيد القيمة كما هي بدلاً من إظهار خطأ تقني
            return self.cleaned_data.get('myimage')

    
    
    def clean(self):
        try:
            cleaned_data = super().clean()
            min_age = cleaned_data.get('min_age')
            max_age = cleaned_data.get('max_age')
            
            if min_age and max_age and min_age > max_age:
                raise ValidationError('الحد الأدنى للعمر يجب أن يكون أقل من أو يساوي الحد الأقصى للعمر')
            
            return cleaned_data
            
        except Exception as e:
            print(f"خطأ غير متوقع في التحقق العام: {str(e)}")
            # نعيد البيانات مع إضافة خطأ عام بدلاً من خطأ تقني
            if not self.errors:
                raise ValidationError("حدث خطأ غير متوقع أثناء التحقق من البيانات. يرجى المحاولة مرة أخرى.")
            return self.cleaned_data
    
    def save(self, commit=True):
        try:
            instance = super().save(commit=False)
            
            if commit:
                instance.save()
            return instance
            
        except Exception as e:
            print(f"خطأ في حفظ النموذج: {str(e)}")
            if not instance.slug:
                instance.slug = f"exam-{int(time.time())}"
            if commit:
                instance.save()
            return instance


class ExamForm(BaseContentForm):
    TYPE_CHOICES = [
        ('', 'اختر صنف الاختبار'),
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
    
    EDUCATIONAL_LEVEL_CHOICES = [
        ('0', 'لا، الاختبار مناسب للجميع'),
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
            ('11', 'السنة الأولى من البكالوريا'),
            ('12', 'السنة الثانية من البكالوريا'),
        ]),
        ('ما بعد الثانوي :', [
            ('13', 'الدراسة بعد البكالوريا'),
        ])
    ]

    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='موضوع الاختبار',
        required=True
    )

    class Meta(BaseContentForm.Meta):

        model = exams
        fields = [
            'title', 'mydescription', 'keywords', 'author', 'myimage', 'gender',
            'the_type', 'educational_level', 'min_age', 'max_age', 'dir'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الاختبار ...',
                'minlength': '2',
                'required': True
            }),
       
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
           
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'name': 'mydescription',
                'placeholder': 'وصف مختصر ...',
                'maxlength': '255'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'keywords',
                'placeholder': 'الكلمات المفتاحية ...',
            }),
            'educational_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'min_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الحد الأدنى',
                'min': '2',
                'max': '75'
            }),
            'max_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الحد الأقصى',
                'min': '2',
                'max': '75'
            }),
            'myimage': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'formFile1'
            }),
        }

        labels = {
            'title': 'عنوان الاختبار',
            'author': 'اسم الكاتب',
            'mydescription': 'وصف يظهر في محركات البحث لتشجيع الناس على زيارة الصفحة ...',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'موضوع الاختبار',
            'dir': 'لغة العنوان',
            'educational_level': 'المستوى الدراسي',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الاختبار',
            'gender': 'موجه لـ',
        }
