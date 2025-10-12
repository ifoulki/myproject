from django import forms
from tifinar.models import comments
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
        