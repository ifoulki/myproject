from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
   
class ContactEditForm(forms.ModelForm):
    EDUCATIONAL_LEVEL_CHOICES = [
        ('0', 'ما هو مستواك الدراسي؟'),
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
            
        # تعيين القيمة الافتراضية بناءً على البيانات الحالية
        if self.instance and self.instance.educational_level:
            self.fields['educational_level'].initial = self.instance.educational_level

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


  