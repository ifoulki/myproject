# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminArticles(models.Model):
    adm_art_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    mysubject = models.TextField(db_column='Mysubject', blank=True, null=True)  # Field name made lowercase.        
    myimage = models.CharField(db_column='Myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=255)  # Field name made lowercase.
    mydescription = models.CharField(db_column='Mydescription', max_length=255)  # Field name made lowercase.       
    keyword = models.CharField(db_column='Keyword', max_length=255)  # Field name made lowercase.
    the_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admin_articles'


class articles(models.Model):
    art_id = models.AutoField(db_column='Art_id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(unique=True, max_length=255, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mysubject = models.TextField(db_column='Mysubject', unique=True, blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    keywords = models.TextField(blank=True, null=True)
    dir = models.CharField(max_length=3)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    myimage = models.CharField(db_column='Myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    autre = models.CharField(max_length=255, blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(max_length=12)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    educational_level = models.CharField(max_length=26)
    gender = models.CharField(max_length=6)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'articles'


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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


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


class Books(models.Model):
    books_id = models.AutoField(primary_key=True)
    myimage = models.TextField(db_column='Myimage', unique=True, blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(unique=True, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mysubject = models.TextField(db_column='Mysubject', unique=True, blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    keywords = models.TextField(blank=True, null=True)
    author = models.TextField(db_column='Author', blank=True, null=True)  # Field name made lowercase.
    autre = models.CharField(max_length=255, blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    dir = models.CharField(max_length=3, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(max_length=12)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    educational_level = models.CharField(max_length=26)
    gender = models.CharField(max_length=6)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books'


class Cache(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expiration = models.PositiveIntegerField()
    created_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'cache'


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


class Comments(models.Model):
    cmt_id = models.AutoField(primary_key=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    author_name = models.CharField(max_length=255, blank=True, null=True)
    cmt_subject = models.TextField(blank=True, null=True)
    author_email = models.CharField(max_length=255, blank=True, null=True)
    visibility_status = models.CharField(max_length=12)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comments'


class Contacts(models.Model):
    contacts_id = models.SmallAutoField(primary_key=True)
    nom = models.TextField(db_column='Nom', blank=True, null=True)  # Field name made lowercase.
    prenom = models.TextField(db_column='Prenom', blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.     
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    the_type = models.TextField(blank=True, null=True)
    societe = models.TextField(db_column='Societe', blank=True, null=True)  # Field name made lowercase.
    ville_d_origine = models.TextField(db_column='Ville_D_origine', blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=255, blank=True, null=True)  # Field name made lowercase.
    etat_social = models.CharField(db_column='Etat_Social', max_length=11, blank=True, null=True)  # Field name made lowercase.
    date_de_naissance = models.DateField(db_column='Date_de_naissance', blank=True, null=True)  # Field name made lowercase.
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
    cousin = models.TextField(blank=True, null=True)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contacts'


class Cours(models.Model):
    cours_id = models.SmallAutoField(primary_key=True)
    title = models.TextField(unique=True, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    myimage = models.TextField(db_column='Myimage', unique=True, blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    keywords = models.TextField(blank=True, null=True)
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


class Exams(models.Model):
    exam_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mydescription = models.CharField(db_column='Mydescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    myimage = models.CharField(db_column='Myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
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
    myimage = models.CharField(db_column='Myimage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mydescription = models.TextField(db_column='Mydescription', blank=True, null=True)  # Field name made lowercase.    autre = models.CharField(max_length=255, blank=True, null=True)
    the_type = models.CharField(max_length=255, blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    keyword = models.CharField(db_column='Keyword', max_length=255, blank=True, null=True)  # Field name made lowercase.
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


class Msgs(models.Model):
    msg_id = models.AutoField(primary_key=True)
    mysubject = models.TextField(db_column='Mysubject', blank=True, null=True)  # Field name made lowercase.        
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author_id = models.PositiveIntegerField(blank=True, null=True)
    author_img = models.TextField(blank=True, null=True)
    recipient = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=9)
    dir = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'msgs'


class Myadmin(models.Model):
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


class SynonymTerms(models.Model):
    term = models.CharField(max_length=255)
    synonyms = models.TextField()
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
    date_de_naissance = models.DateField(db_column='Date_de_naissance', blank=True, null=True)  # Field name made lowercase.
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
    cousin = models.TextField(blank=True, null=True)
    language = models.TextField(db_column='Language')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'


class UsersLikes(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip_or_name = models.CharField(max_length=255)
    page_title = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    liked_at = models.DateTimeField(blank=True, null=True)
    reaction_type = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_likes'


class Videos(models.Model):
    vd_id = models.AutoField(db_column='VD_id', primary_key=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    mysubject = models.TextField(db_column='Mysubject', blank=True, null=True)  # Field name made lowercase.        
    myimage = models.TextField(db_column='Myimage', blank=True, null=True)  # Field name made lowercase.
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

