from django import forms
from .models import comments, Msgs, articles, books, videos, exams, cours
from django.utils.text import slugify

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
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class BaseContentForm(forms.ModelForm):
    class Meta:
        abstract = True  # إن كنت تستعمله في مشروع كبير

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
        return self._validate_file_extension('myimage')

    def clean_autre(self):
        return self._validate_file_extension('autre')

    def _validate_file_extension(self, field_name):
        file = self.cleaned_data.get(field_name)
        if file:
            valid_extensions = ['.jpeg', '.png', '.jpg', '.gif', '.svg', '.webp']
            if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('الملف يجب أن يكون صورة بصيغة صحيحة.')
        return file

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not hasattr(instance, 'slug') or not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

class ArticleForm(forms.ModelForm):
      # 1. أضف هذا الجزء قبل class Meta ↓
    TYPE_CHOICES = [
        ('الأمازيغية', 'الأمازيغية'),
        ('تربية وتعليم', 'تربية وتعليم'),
        ('الثقافة العامة', 'الثقافة العامة'),
        ('علوم', 'علوم'),
        ('القانون وحقوق الإنسان', 'القانون وحقوق الإنسان'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'للدكور فقط'),
        ('female', 'للإناث فقط'),
        ('all', 'للجميع'),
    ]
    
    # 2. أعد تعريف حقل the_type لاستخدام الخيارات
    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        }),
        label='نوع المنشور',
        required=False  # أو True إذا كان الحقل مطلوباً
    )
   
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        }),
        label='هدا المقال موجه',
        required=False  # أو True إذا كان الحقل مطلوباً
    )


    class Meta:
        model = articles
        fields = [
            'title', 'slug', 'mysubject', 'mydescription', 
            'keywords', 'author', 'myimage', 'autre', 'gender',
            'the_type', 'educational_level', 'min_age', 'max_age'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان المنشور ...',
                'minlength': '7',
                'required': True
            }),
            'mysubject': forms.Textarea(attrs={
                'class': 'mysubject',
                'minlength': '100',
                'required': True
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'أكتب وصفًا لمنشورك ...'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'Keyword',
                'placeholder': 'الكلمات المفتاحية ...'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الكاتب ...',
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
            'title': 'عنوان المقال',
            'author': 'اسم الكاتب',
            'mysubject': 'نص المقال',
            'mydescription': 'وصف المنشور',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'نوع المنشور',
            'gender': 'المقال موجه',
            'educational_level': 'المستوى الدراسي',
            'min_age': 'الحد الأدنى للعمر',
            'max_age': 'الحد الأقصى للعمر',
            'myimage': 'الصورة الرئيسية',
            'autre': 'صورة إضافية'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 7:
            raise forms.ValidationError('يجب أن يكون العنوان لا يقل عن 7 أحرف.')
        return title

    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if len(mysubject) < 100:
            raise forms.ValidationError('يجب أن لا يقل نص المقال عن 100 حرف.')
        return mysubject

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 5:
            raise forms.ValidationError('يجب أن لا يقل اسم الكاتب عن 5 أحرف.')
        return author

    def clean_min_age(self):
        min_age = self.cleaned_data.get('min_age')
        if min_age and (min_age < 2 or min_age > 75):
            raise forms.ValidationError('يجب أن يكون العمر بين 2 و75 سنة.')
        return min_age

    def clean_max_age(self):
        max_age = self.cleaned_data.get('max_age')
        if max_age and (max_age < 2 or max_age > 75):
            raise forms.ValidationError('يجب أن يكون العمر بين 2 و75 سنة.')
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
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

from django import forms
from django.utils.text import slugify
from .models import books  # تأكد أن الاسم مطابق
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('قصص و روايات', 'قصص و روايات'),
        ('قصائد شعرية', 'قصائد شعرية'),
        ('مجلات', 'مجلات'),
        ('لقواميس اللغوية - Dictionaries', 'لقواميس اللغوية - Dictionaries'),
        ('أديان', 'أديان'),
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

    DIR_CHOICES = [
        ('rtl', 'العربية'),
        ('ltr', 'Français'),
        ('ltr', 'English'),
    ]

    the_type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control form-select'
    }), required=True)

    dir = forms.ChoiceField(choices=DIR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control form-select small-input'
    }), required=True)

    class Meta:
        model = books
        fields = [
            'title', 'mysubject', 'mydescription', 'keywords',
            'author', 'myimage', 'autre', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الكتاب ...',
                'minlength': '7',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
            'mysubject': forms.Textarea(attrs={
                'class': 'mysubject',
                'placeholder': 'عن ماذا يتحدث الكتاب؟',
                'required': True
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'وصف مختصر ...',
                'maxlength': '255'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'keywords',
                'placeholder': 'الكلمات المفتاحية ...',
                'maxlength': '255'
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
            'title': 'عنوان الكتاب',
            'author': 'اسم الكاتب',
            'mysubject': 'موجز عن الكتاب',
            'mydescription': 'وصف المحتوى',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'صنف الكتاب',
            'dir': 'لغة الموجز',
            'educational_level': 'المستوى الدراسي',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الكتاب',
            'autre': 'تحميل الكتاب'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 7:
            raise forms.ValidationError('يجب أن يكون العنوان لا يقل عن 7 أحرف.')
        return title

    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if not mysubject or len(mysubject.strip()) < 20:
            raise forms.ValidationError('يرجى إدخال موجز لا يقل عن 20 حرفًا.')
        return mysubject

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 5:
            raise forms.ValidationError('اسم الكاتب يجب أن لا يقل عن 5 أحرف.')
        return author

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

    
    # يمكن إضافة تحققات خاصة بالكتب هنا

class VideoForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = videos
        fields = [
            'title', 'author', 'mysubject', 'the_type', 'gender',
            'mydescription', 'keywords', 'educational_level',
            'myimage', 'autre'
        ]

class ExamForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = exams
        fields = [
            'title', 'author', 'the_type','gender',
            'mydescription', 'keywords', 'educational_level',
            'myimage'
        ]

class CoursForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = cours
        fields = [
            'title', 'author', 'the_type','exams_link','gender',
            'mydescription', 'keywords', 'educational_level',
            'myimage'
        ]