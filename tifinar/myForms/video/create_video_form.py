from django import forms
from django.core.exceptions import ValidationError
from tifinar.models import videos
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify  # أضف هذا
import os  # أضف هذا

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
        ('rtl', 'العربية'),
        ('ltr', 'Français'),
        ('ltr', 'English'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'للدكور فقط'),
        ('female', 'للإناث فقط'),
        ('all', 'للجميع'),
    ]
     
    EDUCATIONAL_LEVEL_CHOICES = [
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
    
    dir = forms.ChoiceField(
        choices=DIR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'small-input',
            'placeholder': 'اختر اللغة'
        }),
        label=' عنوان الفيديو مكتوب بأي لغة؟',
        initial='',
        required=False

    )

    educational_level = forms.ChoiceField(
        choices=EDUCATIONAL_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='المستوى الدراسي المطلوب',
        required=False
    )
    
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='موجه لـ',
        initial='all',
        required=False,
        empty_value='all',
        coerce=str
    )
        
    class Meta:
        abstract = True
        fields = [] 

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 7:
            raise forms.ValidationError('يجب أن يكون العنوان لا يقل عن 7 أحرف.')
        return title

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
        ('', 'اختر صنف الكتاب'),
        ('الآداب :', [
            ('قصص و روايات', 'قصص و روايات'),
            ('قصائد شعرية', 'قصائد شعرية'),
            ('مجلات', 'مجلات'),
            ('لقواميس اللغوية - Dictionaries', 'لقواميس اللغوية - Dictionaries'),
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
        
        fields = [
            'title', 'slug', 'mysubject', 'mydescription', 
            'keywords', 'author', 'myimage', 'autre', 'gender',
            'the_type', 'educational_level', 'min_age', 'max_age', 'dir'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الفيديو ...',
                'minlength': '2',
                'required': True
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'أكتب وصفًا لمحتوى الفيديو ...'
            }),
            'mydescription': forms.TextInput(attrs={
                'class': 'form-control',
                'id':'videoInput',
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
            'autre': 'مرفقات إضافية'
        }
