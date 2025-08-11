from django import forms
from django.core.exceptions import ValidationError
from .models import comments, Msgs, articles, books, videos, exams, cours
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserEditForm(forms.ModelForm):
    EDUCATIONAL_LEVEL_CHOICES = [
        ('Unknown', 'لا، المقال مناسب للجميع'),
        ('الإبتدائي :', [
            ('1st Year of Primary School', 'السنة الأولى ابتدائي'),
            ('2nd Year of Primary School', 'السنة الثانية ابتدائي'),
            ('3rd Year of Primary School', 'السنة الثالثة ابتدائي'),
            ('4th Year of Primary School', 'السنة الرابعة ابتدائي'),
            ('5th Year of Primary School', 'السنة الخامسة ابتدائي'),
            ('6th Year of Primary School', 'السنة السادسة ابتدائي'),
        ]),
        ('الإعدادي :', [
            ('1st Year of Middle School', 'السنة الأولى إعدادي'),
            ('2nd Year of Middle School', 'السنة الثانية إعدادي'),
            ('3rd Year of Middle School', 'السنة الثالثة إعدادي'),
        ]),
        ('الثانوي :', [
            ('Common Core', 'المشترك العلمي'),
            ('1st Year of Baccalaureate', 'السنة الأولى من البكالوريا (تخصص علوم تجريبية)'),
            ('2nd Year of Baccalaureate', 'السنة الثانية من البكالوريا (تخصص علوم فيزيائية)'),
        ]),
        ('ما بعد الثانوي :', [
            ('Post-Baccalaureate', 'الدراسة بعد البكالوريا'),
        ])
    ]

    profile_image = forms.ImageField(
        label=_('الصورة الشخصية'),
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text=_('الصيغ المدعومة: JPG, PNG, WEBP (الحد الأقصى 2MB)')
    )
    
    educational_level = forms.ChoiceField(
        choices=EDUCATIONAL_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('المستوى التعليمي'),
        required=False
    )
    
    password = forms.CharField(
        label=_("كلمة المرور الجديدة"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text=_("اتركه فارغاً إذا لم ترد التغيير (8 أحرف على الأقل)")
    )
    
    password_confirmation = forms.CharField(
        label=_("تأكيد كلمة المرور"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['profile_image', 'educational_level', 'email', 
                 'first_name', 'last_name', 'password']
        
        labels = {
            'email': _('البريد الإلكتروني'),
            'first_name': _('الاسم الأول'),
            'last_name': _('الاسم الأخير'),
        }
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].help_text = _("اتركه فارغاً للحفاظ على كلمة المرور الحالية")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        
        if password and len(password) < 8:
            raise ValidationError(_("كلمة المرور يجب أن تكون 8 أحرف على الأقل"))
            
        if password and password != password_confirmation:
            raise ValidationError(_("كلمة المرور وتأكيدها غير متطابقين"))
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("هذا البريد الإلكتروني مسجل بالفعل"))
        return email

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError(_("حجم الصورة كبير جداً (الحد الأقصى 2MB)"))
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                raise ValidationError(_("نوع الملف غير مدعوم. يرجى رفع صورة بصيغة JPG, PNG أو WEBP"))
        return image

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


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
        model = Msgs
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
        ('Unknown', 'لا، المقال مناسب للجميع'),
        ('الإبتدائي :', [
            ('1st Year of Primary School', 'السنة الأولى ابتدائي'),
            ('2nd Year of Primary School', 'السنة الثانية ابتدائي'),
            ('3rd Year of Primary School', 'السنة الثالثة ابتدائي'),
            ('4th Year of Primary School', 'السنة الرابعة ابتدائي'),
            ('5th Year of Primary School', 'السنة الخامسة ابتدائي'),
            ('6th Year of Primary School', 'السنة السادسة ابتدائي'),
        ]),
        ('الإعدادي :', [
            ('1st Year of Middle School', 'السنة الأولى إعدادي'),
            ('2nd Year of Middle School', 'السنة الثانية إعدادي'),
            ('3rd Year of Middle School', 'السنة الثالثة إعدادي'),
        ]),
        ('الثانوي :', [
            ('Common Core', 'المشترك العلمي'),
            ('1st Year of Baccalaureate', 'السنة الأولى من البكالوريا (تخصص علوم تجريبية)'),
            ('2nd Year of Baccalaureate', 'السنة الثانية من البكالوريا (تخصص علوم فيزيائية)'),
        ]),
        ('ما بعد الثانوي :', [
            ('Post-Baccalaureate', 'الدراسة بعد البكالوريا'),
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
