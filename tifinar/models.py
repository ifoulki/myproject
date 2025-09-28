# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class AdminArticles(models.Model):
    adm_art_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    mysubject = models.TextField(db_column='Mysubject', blank=True, null=True)  # Field name made lowercase.        
    myimage = models.CharField(db_column='myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=255)  # Field name made lowercase.
    mydescription = models.CharField(db_column='Mydescription', max_length=255)  # Field name made lowercase.       
    keywords = models.TextField(blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admin_articles'
    @property
    def get_title(self):
        return self.title


class articles(models.Model):
    art_id = models.AutoField(db_column='Art_id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(unique=True, max_length=255, blank=True, null=True)
    slug = models.SlugField( max_length=255, blank=True, null=True, allow_unicode=True, unique=True )
    mysubject = models.TextField(db_column='Mysubject', unique=True, blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    keywords = models.TextField(blank=True, null=True)
    keywords = models.TextField(db_column='keywords', blank=True, null=True)
    dir = models.CharField(max_length=3)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    myimage = models.CharField(db_column='myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    autre = models.CharField(max_length=255, blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(
        max_length=15,
        choices=[
            ('public', 'عام'),
            ('under_review', 'قيد المراجعة'),
            ('restricted', 'مقيد')
        ],
        default='under_review'
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    educational_level = models.CharField(max_length=26)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'ذكر'),
            ('female', 'أنثى'),
            ('all', 'جميع')
        ],
        default='all'
    )
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'articles'
    @property
    def get_title(self):
        return self.title


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, username, password, **extra_fields)

class AuthUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_('Username'), max_length=150, unique=True)
    email = models.EmailField(_('Email Address'), max_length=254, unique=True)
    first_name = models.CharField(_('First Name'), max_length=150)
    last_name = models.CharField(_('Last Name'), max_length=150)
    
    # حقول التوثيق والحالة
    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    last_login = models.DateTimeField(_('Last Login'), blank=True, null=True)
    
    # الحقول الإضافية من جدولك
    email_verified_at = models.DateTimeField(_('Email Verified At'), null=True, blank=True)
    remember_token = models.CharField(_('Remember Token'), max_length=100, null=True, blank=True)
    
    class Role(models.TextChoices):
        CONTENT_CREATOR = 'content_creator', _('Content Creator')
        ADMIN = 'admin', _('Admin')
        USER = 'user', _('User')
    
    role = models.CharField(
        _('Role'),
        max_length=15,
        choices=Role.choices,
        default=Role.USER
    )
    
    class EducationalLevel(models.TextChoices):
        UNKNOWN = '0', _('غير محدد')
        PRIMARY_1 = '1', _('السنة الأولى ابتدائي')
        PRIMARY_2 = '2', _('السنة الثانية ابتدائي')
        PRIMARY_3 = '3', _('السنة الثالثة ابتدائي')
        PRIMARY_4 = '4', _('السنة الرابعة ابتدائي')
        PRIMARY_5 = '5', _('السنة الخامسة ابتدائي')
        PRIMARY_6 = '6', _('السنة السادسة ابتدائي')
        MIDDLE_1 = '7', _('السنة الأولى إعدادي')
        MIDDLE_2 = '8', _('السنة الثانية إعدادي')
        MIDDLE_3 = '9', _('السنة الثالثة إعدادي')
        COMMON_CORE = '10', _('الجدع المشترك')
        BAC_1 = '11', _('السنة الأولى بكالوريا')
        BAC_2 = '12', _('السنة الثانية بكالوريا')
        POST_BAC = '13', _('التعليم العالي')

    educational_level = models.CharField(
        _('Educational Level'),
        max_length=20,
        choices=EducationalLevel.choices,
        default=EducationalLevel.UNKNOWN
    )
    
    images = models.TextField(_('Images'), null=True, blank=True)
    ville_d_origine = models.TextField(_('Ville D\'origine'), null=True, blank=True)
    adresse = models.TextField(_('Adresse'), null=True, blank=True)
    
    class EtatSocial(models.TextChoices):
        CELIBATAIRE = 'Celibataire', _('Celibataire')
        VEUF = 'Veu(f)ve', _('Veu(f)ve')
        ORGANISME = 'Organisme', _('Organisme')
        MARIE = 'Marie(e)', _('Marie(e)')
        DIVORCE = 'Divorce(e)', _('Divorce(e)')
    
    Etat_Social = models.CharField(
        _('Etat Social'),
        max_length=15,
        default=EtatSocial.CELIBATAIRE,
        null=True,
        blank=True
    )
    
    date_de_naissance = models.DateField(_('date_de_naissance'), null=True, blank=True)
    Ideologie = models.TextField(_('Ideologie'), null=True, blank=True)
    social_media = models.TextField(_('Social Media'), null=True, blank=True)
    
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')
        ALL = 'all', _('all')
    
    
    gender = models.CharField(
        _('Gender'),
        max_length=10,
        choices=Gender.choices,
        null=True,
        blank=True
    )
    
    tel = models.CharField(_('Tel'), max_length=20, null=True, blank=True)
    the_type = models.TextField(_('Type'), null=True, blank=True)
    societe = models.TextField(_('Societe'), null=True, blank=True)
    Commentaire = models.TextField(_('Commentaire'), null=True, blank=True)
    path = models.TextField(_('Path'), null=True, blank=True)
    keywords = models.TextField(_('Keywords'), null=True, blank=True)
    spouse = models.CharField(_('Spouse'), max_length=255, null=True, blank=True)
    children = models.TextField(_('Children'), null=True, blank=True)
    siblings = models.TextField(_('Siblings'), null=True, blank=True)
    parents = models.TextField(_('Parents'), null=True, blank=True)
    maternal_relatives = models.TextField(_('Maternal Relatives'), null=True, blank=True)
    paternal_relatives = models.TextField(_('Paternal Relatives'), null=True, blank=True)
    grandparents = models.TextField(_('Grandparents'), null=True, blank=True)
    friends = models.TextField(_('Friends'), null=True, blank=True)
    friend_requests = models.TextField(_('Friend Requests'), null=True, blank=True)
    name_in_arabic = models.CharField(_('Name in Arabic'), max_length=255, null=True, blank=True)
    cousins = models.TextField(_('Cousins'), null=True, blank=True)
    nieces_nephews = models.TextField(_('nieces_nephews'), null=True, blank=True)
    language = models.CharField(_('Language'), max_length=50, default='Ar', null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = AuthUserManager()
    
    class Meta:
        verbose_name = _('Auth User')
        verbose_name_plural = _('Auth Users')
        db_table = 'auth_user'
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.username


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class EducationalLevel(models.TextChoices):
    UNKNOWN = '0', _('غير محدد')
    PRIMARY_1 = '1', _('السنة الأولى ابتدائي')
    PRIMARY_2 = '2', _('السنة الثانية ابتدائي')
    PRIMARY_3 = '3', _('السنة الثالثة ابتدائي')
    PRIMARY_4 = '4', _('السنة الرابعة ابتدائي')
    PRIMARY_5 = '5', _('السنة الخامسة ابتدائي')
    PRIMARY_6 = '6', _('السنة السادسة ابتدائي')
    MIDDLE_1 = '7', _('السنة الأولى إعدادي')
    MIDDLE_2 = '8', _('السنة الثانية إعدادي')
    MIDDLE_3 = '9', _('السنة الثالثة إعدادي')
    COMMON_CORE = '10', _('الجدع المشترك')
    BAC_1 = '11', _('السنة الأولى بكالوريا')
    BAC_2 = '12', _('السنة الثانية بكالوريا')
    POST_BAC = '13', _('التعليم العالي')

class Gender(models.TextChoices):
    MALE = 'male', _('ذكر')
    FEMALE = 'female', _('أنثى')
    ALL = 'all', _('للجميع')

class VisibilityStatus(models.TextChoices):
    PUBLIC = 'public', _('عام')
    UNDER_REVIEW = 'under_review', _('قيد المراجعة')
    RESTRICTED = 'restricted', _('مقيد')

class Dir(models.TextChoices):
    RTL = 'rtl', _('من اليمين لليسار (العربية)')
    LTR = 'ltr', _('من اليسار لليمين (الفرنسية/الإنجليزية)')

class books(models.Model):
    books_id = models.AutoField(primary_key=True)
    myimage = models.CharField(max_length=500, db_column='Myimage', blank=True, null=True)
    title = models.TextField(unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, allow_unicode=True, unique=True)
    mysubject = models.TextField(db_column='Mysubject', unique=True, blank=True, null=True)
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    author = models.TextField(db_column='Author', blank=True, null=True)
    autre = models.CharField(max_length=255, blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    dir = models.CharField(
        max_length=3,
        choices=Dir.choices,
        default=Dir.LTR,
        blank=True,
        null=True
    )
    language = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(
        max_length=12,
        choices=VisibilityStatus.choices,
        default=VisibilityStatus.UNDER_REVIEW
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(
        max_length=6,
        choices=Gender.choices,
        default=Gender.ALL
    )
    min_age = models.IntegerField(default=2)
    max_age = models.IntegerField(default=75)
    educational_level = models.CharField(
        max_length=2,
        choices=EducationalLevel.choices,
        default=EducationalLevel.UNKNOWN
    )

    class Meta:
        managed = False
        db_table = 'books'
        verbose_name = 'كتاب'
        verbose_name_plural = 'الكتب'

    def __str__(self):
        return self.title or 'بدون عنوان'

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def get_title(self):
        return self.title or 'بدون عنوان'

    def clean(self):
        if self.min_age and self.max_age and self.min_age > self.max_age:
            raise ValidationError('الحد الأدنى للعمر يجب أن يكون أقل من الحد الأقصى')
        
        if self.min_age < 2 or self.min_age > 75:
            raise ValidationError('الحد الأدنى للعمر يجب أن يكون بين 2 و 75')
        
        if self.max_age < 2 or self.max_age > 75:
            raise ValidationError('الحد الأقصى للعمر يجب أن يكون بين 2 و 75')

    def get_educational_level_display(self):
        """عرض قيمة educational_level بشكل مقروء"""
        return dict(EducationalLevel.choices).get(self.educational_level, 'غير معروف')

    def get_gender_display(self):
        """عرض قيمة gender بشكل مقروء"""
        return dict(Gender.choices).get(self.gender, 'غير معروف')

    def get_visibility_status_display(self):
        """عرض قيمة visibility_status بشكل مقروء"""
        return dict(VisibilityStatus.choices).get(self.visibility_status, 'غير معروف')

    def get_dir_display(self):
        """عرض قيمة dir بشكل مقروء"""
        return dict(Dir.choices).get(self.dir, 'غير معروف')
    
class Cache(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expiration = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'cache'
        verbose_name = 'كاش'
        verbose_name_plural = 'الكاش'


class CartItems(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart_items'
        unique_together = (('user_id', 'product_id'),)

User = get_user_model()

class comments(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'عام'),
        ('under_review', 'قيد المراجعة'),
        ('restricted', 'مقيد'),
    ]
    
    cmt_id = models.AutoField(primary_key=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    author_name = models.CharField(max_length=255, blank=True, null=True)
    cmt_subject = models.TextField(blank=True, null=True)
    author_email = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(
        max_length=15, 
        choices=VISIBILITY_CHOICES, 
        default='under_review'
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
   
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.page_title}"

    @property
    def time_text(self):
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 365:
            years = diff.days // 365
            return f"منذ {years} سنة" if years > 1 else "منذ سنة واحدة"
        elif diff.days > 30:
            months = diff.days // 30
            return f"منذ {months} شهر" if months > 1 else "منذ شهر واحد"
        elif diff.days > 0:
            return f"منذ {diff.days} يوم" if diff.days > 1 else "منذ يوم واحد"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"منذ {hours} ساعة" if hours > 1 else "منذ ساعة واحدة"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"منذ {minutes} دقيقة" if minutes > 1 else "منذ دقيقة واحدة"
        else:
            return "الآن"

    @property
    def is_visible(self):
        return self.visibility_status == 'public'

class Contacts(models.Model):
    contacts_id = models.SmallAutoField(primary_key=True)
    nom = models.TextField(db_column='nom', blank=True, null=True)  # Field name made lowercase.
    prenom = models.TextField(db_column='prenom', blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.     
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    the_type = models.TextField(blank=True, null=True)
    societe = models.TextField(db_column='Societe', blank=True, null=True)  # Field name made lowercase.
    ville_d_origine = models.TextField(db_column='Ville_D_origine', blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Etat_Social = models.CharField(db_column='Etat_Social', max_length=11, blank=True, null=True)  # Field name made lowercase.
    date_de_naissance = models.DateField(db_column='date_de_naissance', blank=True, null=True)  # Field name made lowercase.
    ideologie = models.TextField(db_column='Ideologie', blank=True, null=True)  # Field name made lowercase.        
    commentaire = models.TextField(db_column='Commentaire', blank=True, null=True)  # Field name made lowercase.    
    social_media = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=7, blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    educational_level = models.CharField(max_length=28)
    keywords = models.TextField(blank=True, null=True)
    spouse = models.CharField(max_length=255, blank=True, null=True)
    children = models.TextField(blank=True, null=True)
    siblings = models.TextField(blank=True, null=True)
    parents = models.TextField(blank=True, null=True)
    maternal_relatives = models.TextField(blank=True, null=True)
    paternal_relatives = models.TextField(blank=True, null=True)
    grandparents = models.TextField(blank=True, null=True)
    friends = models.TextField(blank=True, null=True)
    name_in_arabic = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    cousins = models.TextField(blank=True, null=True)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contacts'
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"
    
    def get_author_contacts(self):
        """
        استرجاع جميع جهات الاتصال المرتبطة بالمستخدم بناءً على عمود author
        """
        if not self.author:
            return Contacts.objects.none()
        
        try:
            # تحويل الـ author من نص إلى قائمة IDs
            author_ids = [int(id_str.strip()) for id_str in self.author.split(',') if id_str.strip()]
            return Contacts.objects.filter(contacts_id__in=author_ids)
        except (ValueError, TypeError):
            return Contacts.objects.none()
    
    def add_author_contact(self, contacts_id):
        """
        إضافة جهة اتصال جديدة إلى عمود author
        """
        try:
            contacts_id = int(contacts_id)
            current_authors = self.get_author_ids()
            
            if contacts_id not in current_authors and contacts_id != self.contacts_id:
                current_authors.append(contacts_id)
                self.author = ','.join(map(str, current_authors))
                self.save()
                return True
        except (ValueError, TypeError):
            pass
        return False
    
    def remove_author_contact(self, contacts_id):
        """
        إزالة جهة اتصال من عمود author
        """
        try:
            contacts_id = int(contacts_id)
            current_authors = self.get_author_ids()
            
            if contacts_id in current_authors:
                current_authors.remove(contacts_id)
                self.author = ','.join(map(str, current_authors)) if current_authors else ''
                self.save()
                return True
        except (ValueError, TypeError):
            pass
        return False
    
    def get_author_ids(self):
        """
        الحصول على قائمة IDs من عمود author
        """
        if not self.author:
            return []
        
        try:
            return [int(id_str.strip()) for id_str in self.author.split(',') if id_str.strip()]
        except (ValueError, TypeError):
            return []


class cours(models.Model):
    cours_id = models.SmallAutoField(primary_key=True)
    title = models.TextField(unique=True, blank=True, null=True)
    slug = models.SlugField( max_length=255, blank=True, null=True, allow_unicode=True, unique=True )
    myimage = models.TextField(db_column='myimage', blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    keywords = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    author = models.TextField(db_column='Author', blank=True, null=True)  # Field name made lowercase.
    myfile = models.TextField(db_column='Myfile')  # Field name made lowercase.
    images = models.TextField(blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    exams_link = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(max_length=12)
    updated_at = models.DateField()
    created_at = models.DateTimeField()
    cours_contents = models.TextField(blank=True, null=True)
    the_type = models.CharField(max_length=13, blank=True, null=True)
    gender = models.CharField(max_length=6)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    educational_level = models.CharField(max_length=26)
    dir = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cours'
    @property
    def get_title(self):
        return self.title


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Examitems(models.Model):
    premary_id = models.AutoField(primary_key=True)
    qsts_id = models.IntegerField(blank=True, null=True)
    exam_number = models.IntegerField(blank=True, null=True)
    qst_1st_line = models.CharField(max_length=255, blank=True, null=True)
    qsts = models.CharField(max_length=255, blank=True, null=True)
    choice1 = models.CharField(max_length=255, blank=True, null=True)
    choice2 = models.CharField(max_length=255, blank=True, null=True)
    choice3 = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255, blank=True, null=True)
    if_choising_1 = models.TextField(blank=True, null=True)
    if_choising_2 = models.TextField(blank=True, null=True)
    if_choising_3 = models.TextField(blank=True, null=True)
    if_choising_correct = models.TextField(blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    qst_img = models.CharField(max_length=255, blank=True, null=True)
    img_if_wrong_answer = models.CharField(max_length=255, blank=True, null=True)
    img_if_right_answer = models.CharField(max_length=255, blank=True, null=True)
    if_its_wrong_answer = models.TextField(blank=True, null=True)
    dir = models.CharField(max_length=255, blank=True, null=True)
    mark = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'examitems'
        
    def get_shuffled_choices(self):
            choices = []
            if self.choice1:
                choices.append(self.choice1)
            if self.choice2:
                choices.append(self.choice2)
            if self.choice3:
                choices.append(self.choice3)
            if self.correct_answer:
                choices.append(self.correct_answer)
            
            # تصفية الخيارات الفارغة وخلطها
            choices = [choice for choice in choices if choice]
            random.shuffle(choices)
            return choices

class exams(models.Model):
    exam_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField( max_length=255, blank=True, null=True, allow_unicode=True, unique=True )
    mydescription = models.CharField(db_column='Mydescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    myimage = models.CharField(db_column='myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keywords = models.TextField(blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dir = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(max_length=12)
    educational_level = models.CharField(max_length=26)
    gender = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'exams'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Invoices(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice_number = models.CharField(unique=True, max_length=50)
    ice_number = models.CharField(max_length=25, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    shop_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    invoice_date = models.DateField()
    invoice_language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    products = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoices'


class Laws(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    article_id = models.AutoField(primary_key=True)
    mysubject = models.TextField(db_column='Mysubject', blank=True, null=True)  # Field name made lowercase.        
    myimage = models.CharField(db_column='myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    autre = models.CharField(max_length=255, blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'laws'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class msgs(models.Model):
    STATUS_CHOICES = [
        ('read', 'Read'),
        ('unread', 'Unread'),
        ('important', 'Important'),
    ]

    DIR_CHOICES = [
        ('ltr', 'ltr'),
        ('rtl', 'rtl'),
    ]
    msg_id = models.AutoField(primary_key=True)
    mysubject = models.TextField(db_column='mysubject', blank=True, null=True)  # Field name made lowercase.        
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author_id = models.PositiveIntegerField(blank=True, null=True)
    author_img = models.TextField(blank=True, null=True)
    recipient = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(
            max_length=9,
            choices=STATUS_CHOICES,
            default='unread',
            blank=False,
            null=False,
        )
    dir = models.CharField(
            max_length=3,
            choices=DIR_CHOICES,
            default='ltr',
            blank=False,
            null=False,
        )

    class Meta:
        managed = False
        db_table = 'msgs'


class myadmin(models.Model):
    adm_id = models.IntegerField(primary_key=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    mobile_logo = models.CharField(max_length=255, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    ads = models.TextField(blank=True, null=True)
    aside_ads = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'myadmin'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class Products(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_in_french = models.CharField(max_length=255)
    name_in_arabic = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price_before_discount = models.IntegerField(blank=True, null=True)
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    arabic_description = models.TextField()
    french_description = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField()
    image_filenames = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Results(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    exam_title = models.CharField(max_length=255, blank=True, null=True)
    exam_link = models.TextField(blank=True, null=True)
    result = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'results'


class SearchLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_or_ip = models.CharField(max_length=255, blank=True, null=True)
    search_term = models.CharField(max_length=255)
    results_count = models.IntegerField()
    source_page_title = models.TextField()
    user_agent = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'search_logs'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sessions'

class synonym_terms(models.Model):
    term = models.CharField(max_length=255)
    synonyms = models.TextField(blank=True, null=True)
    contact_field = models.CharField(max_length=64)  # هذا يجب أن يكون موجودًا
    target_gender = models.CharField(max_length=6, choices=[('male','male'),('female','female')], blank=True, null=True)
    ignore_terms = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'synonym_terms'

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=15)
    educational_level = models.CharField(max_length=26)
    images = models.TextField(blank=True, null=True)
    ville_d_origine = models.TextField(db_column='Ville_D_origine', blank=True, null=True)  # Field name made lowercase.
    adresse = models.TextField(db_column='Adresse', blank=True, null=True)  # Field name made lowercase.
    etat_social = models.CharField(db_column='Etat_Social', max_length=11, blank=True, null=True)  # Field name made lowercase.
    date_de_naissance = models.DateField(db_column='date_de_naissance', blank=True, null=True)  # Field name made lowercase.
    ideologie = models.TextField(db_column='Ideologie', blank=True, null=True)  # Field name made lowercase.        
    social_media = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=7, blank=True, null=True)
    nom = models.TextField(db_column='Nom', blank=True, null=True)  # Field name made lowercase.
    prenom = models.TextField(db_column='Prenom', blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.     
    the_type = models.TextField(blank=True, null=True)
    societe = models.TextField(db_column='Societe', blank=True, null=True)  # Field name made lowercase.
    commentaire = models.TextField(db_column='Commentaire', blank=True, null=True)  # Field name made lowercase.    
    path = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    spouse = models.CharField(max_length=255, blank=True, null=True)
    children = models.TextField(blank=True, null=True)
    siblings = models.TextField(blank=True, null=True)
    parents = models.TextField(blank=True, null=True)
    maternal_relatives = models.TextField(blank=True, null=True)
    paternal_relatives = models.TextField(blank=True, null=True)
    grandparents = models.TextField(blank=True, null=True)
    friends = models.TextField(blank=True, null=True)
    friend_requests = models.TextField(blank=True, null=True)
    name_in_arabic = models.CharField(max_length=255, blank=True, null=True)
    cousins = models.TextField(blank=True, null=True)
    language = models.TextField(db_column='Language')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'


class ArticleReaction(models.Model):
    REACTION_CHOICES = [
        ('love', '❤️ حب'),
        ('like', '👍 إعجاب'),
        ('dislike', '👎 عدم إعجاب'),
        ('sad', '😢 حزن'),
        ('funny', '😂 مضحك'),
        ('angry', '😤 غضب'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    ip_or_name = models.CharField(max_length=255)
    page_title = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    liked_at = models.DateTimeField(blank=True, null=True)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_likes'

    def __str__(self):
        return f"{self.ip_or_name} - {self.reaction_type}"    


class videos(models.Model):
    vd_id = models.AutoField(db_column='VD_id', primary_key=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    slug = models.SlugField( max_length=255, blank=True, null=True, allow_unicode=True, unique=True )
    mysubject = models.TextField(db_column='Mysubject', blank=True, null=True)  # Field name made lowercase.        
    myimage = models.TextField(db_column='myimage', blank=True, null=True)  # Field name made lowercase.
    keywords = models.TextField(blank=True, null=True)
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    keywords = models.TextField(blank=True, null=True)
    author = models.TextField(db_column='Author', blank=True, null=True)  # Field name made lowercase.
    autre = models.TextField(blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    dir = models.CharField(max_length=3, blank=True, null=True)
    visibility_status = models.CharField(max_length=12)
    updated_at = models.DateField()
    created_at = models.DateTimeField()
    educational_level = models.CharField(max_length=26)
    gender = models.CharField(max_length=6, blank=True, null=True)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'videos'
        db_table_comment = 'الفيديوهات'
    @property
    def get_title(self):
        return self.title


class Visitors(models.Model):
    page_link = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    previous_page_url = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    device_type = models.TextField(blank=True, null=True)
    visit_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'visitors'


class VisitorsIp(models.Model):
    ip = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    number_of_visits = models.IntegerField()
    visit_timestamp = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'visitors_ip'


class Visitorsearchrequests(models.Model):
    request_id = models.AutoField(db_column='Request_id', primary_key=True)  # Field name made lowercase.
    request = models.CharField(db_column='Request', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchqueriescount = models.IntegerField(db_column='SearchQueriesCount', blank=True, null=True)  # Field name made lowercase.
    numberofresults = models.IntegerField(db_column='numberOfResults', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visitorsearchrequests'

