from django import forms
from tifinar.models import msgs
from tifinar.choices import *
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify

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

