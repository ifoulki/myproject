from django import forms
from tifinar.models import comments, msgs, videos, exams
from tifinar.choices import *
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()
import os

TYPE_CHOICES = [
        ('التربية الإسلامية', 'التربية الإسلامية'),
        ('فلسفة', 'فلسفة'),
        ('الأمازيغية', 'تعلم الأمازيغية'),
        ('الفرنسية', 'تعلم الفرنسية'),
        ('الإنجليزية', 'تعلم الإنجليزية'),
        ('رياضيات', 'تعلم الرياضيات'),
        ('الكيمياء', 'الكيمياء'),
        ('الفزياء', 'الفزياء'),
        ('علوم الحياة والأرض', 'علوم الحياة والأرض'),
        ('صحة وحياة', 'صحة وحياة'),
        ('علوم الحاسوب', 'علوم الحاسوب'),
        ('حقوق الإنسان', 'القانون وحقوق الإنسان'),
        ('الثقافة العامة', 'الثقافة العامة'),
        ('تربية وتعليم', 'تربية وتعليم'),
        ('أصناف أخرى', 'أصناف أخرى'),
    ]

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['page_title', 'author_name', 'author_email', 'cmt_subject','visibility_status']
        widgets = {
            'page_title': forms.HiddenInput(),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('اسمك ...'),
                'minlength': '3',
                'required': True
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('بريدك الإلكتروني ...'),
                'required': True
            }),
            'cmt_subject': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': _('اكتب تعليقك هنا ...'),
                'required': True
            }),
            'visibility_status': forms.RadioSelect(
                choices=VisibilityStatus.choices,
            ),
        }
        labels = {
            'author_name': _('الاسم'),
            'author_email': _('البريد الإلكتروني'),
            'cmt_subject': _('التعليق')
        }

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # تحديث وقت التعديل
        instance.updated_at = timezone.now()
        if commit:
            instance.save()
        return instance
        
class MsgForm(forms.ModelForm):
    class Meta:
        model = msgs
        fields = ['author', 'author_id', 'email', 'title', 'author_img', 'recipient', 'mysubject']

        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المرسل ...',
                'minlength': '3'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'بريد المرسل ...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الرسالة ...'
            }),
            'mysubject': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نص الرسالة ...',
                'rows': 4
            }),
        }
    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 3:
            raise forms.ValidationError("يجب أن يكون اسم المرسل 3 أحرف على الأقل.")
        return author

class BaseContentForm(forms.ModelForm):
    
    dir = forms.ChoiceField(
        choices=Dir.choices,
        widget=forms.Select(attrs={
            'class': 'small-input',
            'placeholder': 'اختر اللغة'
        }),
        label=' موجز الكتاب مكتوب بأي لغة؟',
        required=True,
        initial='',  # لجعل الخيار الأول هو المحدد افتراضياً
    )

    educational_level = forms.ChoiceField(
        choices=EducationalLevel.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='المستوى الدراسي المطلوب',
        required=False
    )
    
    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='موجه لـ',
        initial='all',
        required=False
    )
    
    visibility_status = forms.ChoiceField(
        choices=VisibilityStatus.choices,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='حالة الظهور',
        required=True
    )
    
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

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not hasattr(instance, 'slug') or not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class VideoForm(BaseContentForm):

    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='تصنيف الفيديو',
        required=True
    )

    class Meta(BaseContentForm.Meta):

        model = videos
        fields = [
            'title', 'mysubject', 'mydescription', 'keywords',
            'author', 'myimage', 'autre', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir','gender'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الفيديو ...',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'author',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
            'mysubject': forms.Textarea(attrs={
                'class': 'mysubject',
                'placeholder': 'ألصق رابط الفيديو هنا ..',
                'required': True
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'وصف الفيديو ...',
            }),
            
            'keywords': forms.Textarea(attrs={
                'class': 'keywords',
                'placeholder': 'الكلمات المفتاحية ...',
                'value': ''  # إضافة هذه السطر
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
            'autre': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'formFile2'
            }),
        }

        labels = {
            'title': 'عنوان الفيديو',
            'author': 'صاحب الفيديو',
            'mysubject': 'رابط الفيديو',
            'mydescription': 'وصف الفيديو',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'صنف الفيديو',
            'dir': 'العنوان مكتوب بأي لغة؟',
            'educational_level': 'هل يجب أن يكون للمشاهد مستوى دراسي معين؟',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الفيديو',
            'autre': 'تحميل الفيديو'
        }

    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if not mysubject or len(mysubject.strip()) < 20:
            raise forms.ValidationError('يرجى إضافة رابط الفيديو.')
        return mysubject

class BookForm(BaseContentForm):

    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='تصنيف الكتاب',
        required=True
    )

    class Meta(BaseContentForm.Meta):

        model = videos
        fields = [
            'title', 'mysubject', 'mydescription', 'keywords',
            'author', 'myimage', 'autre', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir','gender'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الاختبار ...',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'author',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
           
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'وصف الكتاب ...',
            }),
            
            'keywords': forms.Textarea(attrs={
                'class': 'keywords',
                'placeholder': 'الكلمات المفتاحية ...',
                'value': ''  # إضافة هذه السطر
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
            'title': 'عنوان الكتاب',
            'author': 'صاحب الكتاب',
            'mydescription': 'وصف الكتاب',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'صنف الكتاب',
            'dir': 'العنوان مكتوب بأي لغة؟',
            'educational_level': 'هل يجب أن يكون للمشاهد مستوى دراسي معين؟',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الكتاب',
        }

    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if not mysubject or len(mysubject.strip()) < 20:
            raise forms.ValidationError('يرجى إضافة رابط الكتاب.')
        return mysubject


class ExamForm(BaseContentForm):

    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='تصنيف الاختبار',
        required=True
    )

    visibility_status = forms.ChoiceField(
        choices=VisibilityStatus.choices,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='حالة الظهور',
        required=True
    )

    class Meta:
        model = exams
        fields = [
            'title', 'mydescription', 'keywords',
            'author', 'myimage', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir', 'gender', 'visibility_status'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الاختبار ...',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'author',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'وصف الاختبار ...',
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
            'author': 'صاحب الاختبار', 
            'mydescription': 'وصف الاختبار',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'صنف الاختبار',
            'dir': 'العنوان مكتوب بأي لغة؟',
            'educational_level': 'هل يجب أن يكون للمستخدم مستوى دراسي معين؟',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الاختبار',
            'visibility_status': 'حالة الظهور',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'visibility_status' not in self.fields:
            self.fields['visibility_status'] = forms.ChoiceField(
                choices=VisibilityStatus.choices,
                widget=forms.Select(attrs={'class': 'form-control form-select'}),
                label='حالة الظهور',
                required=True
            )

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not hasattr(instance, 'slug') or not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance