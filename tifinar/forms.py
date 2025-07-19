from django import forms
from .models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['page_title', 'author_name', 'author_email', 'cmt_subject']
        widgets = {
            'page_title': forms.HiddenInput(),
            'cmt_subject': forms.Textarea(attrs={'rows': 4, 'required': True}),
        }