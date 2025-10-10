# choices.py
from django.db import models
from django.utils.translation import gettext_lazy as _
class VisibilityStatus(models.TextChoices):
    PUBLIC = 'public', _('عام')
    UNDER_REVIEW = 'under_review', _('قيد المراجعة')
    RESTRICTED = 'restricted', _('مقيد')


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


class Dir(models.TextChoices):
    RTL = 'rtl', _('من اليمين لليسار (العربية)')
    LTR = 'ltr', _('من اليسار لليمين (الفرنسية/الإنجليزية)')


class SocialStatus(models.TextChoices):
    CELIBATAIRE = 'Celibataire', _('Celibataire')
    VEUF = 'Veu(f)ve', _('Veu(f)ve')
    ORGANISME = 'Organisme', _('Organisme')
    MARIE = 'Marie(e)', _('Marie(e)')
    DIVORCE = 'Divorce(e)', _('Divorce(e)')


class Role(models.TextChoices):
    USER = 'user', _('User')
    CONTENT_CREATOR = 'content_creator', _('Content Creator')
    ADMIN = 'admin', _('Admin')
