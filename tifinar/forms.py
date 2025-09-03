from django import forms
from django.core.exceptions import ValidationError
from .models import comments, msgs, articles, books, videos, exams, cours, Contacts
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['page_title', 'author_name', 'author_email', 'cmt_subject']
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
        }
        labels = {
            'author_name': _('الاسم'),
            'author_email': _('البريد الإلكتروني'),
            'cmt_subject': _('التعليق')
        }
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
        label=' موجز الكتاب مكتوب بأي لغة؟',
        required=True,
        initial='',  # لجعل الخيار الأول هو المحدد افتراضياً
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
    
    def _validate_file_extension(self, field_name):
        file = self.cleaned_data.get(field_name)
        if file:
            valid_extensions = ['.jpeg', '.png', '.jpg', '.gif', '.svg', '.webp']
            if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('الملف يجب أن يكون صورة بصيغة صحيحة.')
        return file
    
    def _validate_file(self, field_name, valid_extensions, max_size_mb):
        file = self.cleaned_data.get(field_name)
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

class ArticleForm(BaseContentForm):
    
    TYPE_CHOICES = [
        ('الأمازيغية', 'الأمازيغية'),
        ('تربية وتعليم', 'تربية وتعليم'),
        ('الثقافة العامة', 'الثقافة العامة'),
        ('علوم', 'علوم'),
        ('القانون وحقوق الإنسان', 'القانون وحقوق الإنسان'),
    ]
    
    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        }),
        label='نوع المنشور',
        required=False  # أو True إذا كان الحقل مطلوباً
    )
   
    class Meta(BaseContentForm.Meta):
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
                'class': 'keywords',
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
            'autre': 'مرفقات إضافية'
        }


    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if not mysubject or len(mysubject.strip()) < 100:
            raise forms.ValidationError('يجب أن لا يقل نص المقال عن 100 حرف.')
        return mysubject
class BookForm(BaseContentForm):
    
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
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='تصنيف الكتاب',
        required=True
    )

    class Meta(BaseContentForm.Meta):

        model = books
        fields = [
            'title', 'mysubject', 'mydescription', 'keywords',
            'author', 'myimage', 'autre', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir','gender'
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
                'name': 'mydescription',
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
                'name': 'myimage',
                'id': 'formFile1'
            }),
            'autre': forms.FileInput(attrs={
                'class': 'form-control',
                'name': 'autre',
                'id': 'formFile2'
            }),
        }

        labels = {
            'title': 'عنوان الكتاب',
            'author': 'اسم الكاتب',
            'mysubject': 'موجز عن الكتاب يشجع على تحميله :',
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

    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if not mysubject or len(mysubject.strip()) < 20:
            raise forms.ValidationError('يرجى إدخال موجز لا يقل عن 20 حرفًا.')
        return mysubject


class VideoForm(BaseContentForm):
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
            'myimage': 'غلاف الكتاب',
            'autre': 'تحميل الكتاب'
        }

    def clean_mysubject(self):
        mysubject = self.cleaned_data.get('mysubject')
        if not mysubject or len(mysubject.strip()) < 20:
            raise forms.ValidationError('يرجى إضافة رابط الفيديو.')
        return mysubject


class ExamForm(BaseContentForm):
    TYPE_CHOICES = [
     
        ('لقواميس اللغوية - Dictionaries', 'لقواميس اللغوية - Dictionaries'),
        ('أديان', 'التربية الإسلامية'),
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
    ]

    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='نوع الاختبار',
        required=True
    )

    class Meta(BaseContentForm.Meta):

        model = exams
        fields = [
            'title', 'mydescription', 'keywords',
            'author', 'myimage', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir','gender'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الاختبار ...',
                'minlength': '7',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
            'mydescription': forms.Textarea(attrs={
                'class': 'description',
                'placeholder': 'وصف مختصر ...',
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
            'title': 'عنوان الاختبار',
            'author': 'اسم الكاتب',
            'mydescription': 'وصف الاختبار',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'صنف الاختبار',
            'dir': 'بأي لغة ستطرح الأسئلة ؟',
            'educational_level': 'المستوى الدراسي',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الكتاب',
        }

class CoursForm(BaseContentForm):
    TYPE_CHOICES = [
        ('على شكل شاشة وأزرار', 'with a board'),
        ('صور مع أسماء', 'without a board'),
    ]

    the_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='نوع العرض',
        required=True
    )

    class Meta(BaseContentForm.Meta):

        model = cours
        fields = [
            'title', 'myfile', 'mydescription', 'keywords','cours_contents','images','exams_link',
            'author', 'myimage', 'intro', 'the_type', 'educational_level',
            'min_age', 'max_age', 'dir','gender'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان القاموس ...',
                'minlength': '7',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الكاتب ...',
                'maxlength': '50'
            }),
            'myfile': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المجلد الدي تخزن فيه صور القاموس',
                'required': True
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
            'title': 'عنوان القاموس',
            'author': 'اسم الكاتب',
            'myfile': 'إسم المجلد الدي تخزن فيه الصور',
            'mydescription': 'وصف يظهر في محركات البحث لتشجيع الناس على زيارة الصفحة ...',
            'intro': 'وصف يظهر أعلى الصفحة يشرح للزائر كيفية التعامل مع الصفحة ...',
            'keywords': 'الكلمات المفتاحية',
            'the_type': 'صنف الكتاب',
            'dir': 'لغة الموجز',
            'educational_level': 'المستوى الدراسي',
            'min_age': 'العمر الأدنى',
            'max_age': 'العمر الأقصى',
            'myimage': 'غلاف الكتاب',
        }
