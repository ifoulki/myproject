from django import forms
from .models import comments, Msgs, articles, books, videos, exams, cours

# الفورمات الأساسية
class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['page_title', 'author_name', 'author_email', 'cmt_subject']
        widgets = {
            'page_title': forms.HiddenInput(),
            'cmt_subject': forms.Textarea(attrs={'rows': 4, 'required': True}),
        }

class MsgForm(forms.ModelForm):
    class Meta:
        model = Msgs
        fields = ['author', 'author_id', 'email', 'title', 'author_img', 'recipient', 'mysubject']
    
    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 3:
            raise forms.ValidationError("يجب أن يكون اسم المرسل 3 أحرف على الأقل.")
        return author

# فورم أساسي للمحتوى المشتركfrom django import forms
from .models import comments, Msgs, articles, books, videos, exams, cours

# الفورمات الأساسية
class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['page_title', 'author_name', 'author_email', 'cmt_subject']
        widgets = {
            'page_title': forms.HiddenInput(),
            'cmt_subject': forms.Textarea(attrs={'rows': 4, 'required': True}),
        }

class MsgForm(forms.ModelForm):
    class Meta:
        model = Msgs
        fields = ['author', 'author_id', 'email', 'title', 'author_img', 'recipient', 'mysubject']
    
    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 3:
            raise forms.ValidationError("يجب أن يكون اسم المرسل 3 أحرف على الأقل.")
        return author

# فورم أساسي للمحتوى المشترك
class BaseContentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'mydescription': forms.Textarea(attrs={'maxlength': '255'}),
            'keywords': forms.Textarea(attrs={'maxlength': '255'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 7:
            raise forms.ValidationError('يجب أن يكون العنوان لا يقل عن 7 حروف.')
        return title
    
    def clean_myimage(self):
        myimage = self.cleaned_data.get('myimage')
        if myimage:
            valid_extensions = ['.jpeg', '.png', '.jpg', '.gif', '.svg', '.webp']
            if not any(myimage.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('يجب أن تكون الصورة بصيغة jpeg أو png أو jpg أو gif أو svg أو webp.')
        return myimage
    
    def clean_autre(self):
        autre = self.cleaned_data.get('autre')
        if autre:
            valid_extensions = ['.jpeg', '.png', '.jpg', '.gif', '.svg', '.webp']
            if not any(autre.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('يجب أن تكون الصورة بصيغة صحيحة.')
        return autre

# فورمات محددة لكل نموذج
class ArticleForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = articles
        fields = [
            'title', 'author', 'mysubject', 'the_type',
            'mydescription', 'keywords', 'educational_level',
            'myimage', 'autre'
        ]
        widgets = {
            **BaseContentForm.Meta.widgets,
            'mysubject': forms.Textarea(attrs={'minlength': '100'}),
        }
    
    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if len(mysubject) < 100:
            raise forms.ValidationError('يجب أن لا يقل الموضوع عن 100 حرف.')
        return mysubject
    
    def clean_mydescription(self):
        mydescription = self.cleaned_data.get('mydescription')
        if len(mydescription) < 20:
            raise forms.ValidationError('يجب أن يحتوي الوصف على 20 حرفًا على الأقل.')
        return mydescription

class BookForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = books
        fields = [
            'title', 'author', 'mysubject', 'the_type',
            'mydescription', 'keywords', 'educational_level',
            'myimage', 'autre'
        ]
    
    # يمكن إضافة تحققات خاصة بالكتب هنا

class VideoForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = videos
        fields = [
            'title', 'author', 'mysubject', 'the_type',
            'mydescription', 'keywords', 'educational_level',
            'myimage', 'autre'
        ]

class ExamForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = exams
        fields = [
            'title', 'author', 'the_type',
            'mydescription', 'keywords', 'educational_level',
            'myimage'
        ]

class CoursForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = cours
        fields = [
            'title', 'author', 'the_type','exams_link',
            'mydescription', 'keywords', 'educational_level',
            'myimage'
        ]