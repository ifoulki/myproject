from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from tifinar.models import videos, ArticleReaction, comments, AuthUser
from django.utils import timezone
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.utils.timezone import now
import os
import urllib.parse
from django.conf import settings

def encode_arabic_path(path):
    """
    ترميز المسارات العربية لتجنب مشاكل Unicode
    """
    try:
        if isinstance(path, str):
            parts = path.split('/')
            encoded_parts = []
            for part in parts:
                if any(ord(c) > 127 for c in part):
                    encoded_parts.append(urllib.parse.quote(part))
                else:
                    encoded_parts.append(part)
            return '/'.join(encoded_parts)
        return path
    except Exception as e:
        print(f"Error encoding path {path}: {e}")
        return path

def get_user_profile_image(email):
    """
    الحصول على صورة المستخدم من خلال البريد الإلكتروني
    """
    try:
        user = AuthUser.objects.filter(email=email).first()
        if not user:
            print(f"❌ المستخدم غير موجود للبريد: {email}")
            return None
            
        print(f"🔍 معالجة المستخدم: {user.username} ({user.email})")
        print(f"🆔 ID المستخدم: {user.id}")
        
        # 🔥 طباعة محتوى الحقول المهمة من جدول auth_user بأي ثمن
        print(f"🔥🔥🔥 محتوى حقل images: '{getattr(user, 'images', 'غير موجود')}'")
        print(f"🔥🔥🔥 محتوى حقل path: '{getattr(user, 'path', 'غير موجود')}'")
        
        # البحث في الحقول المباشرة في نموذج AuthUser
        if hasattr(user, 'images') and user.images:
            print(f"🔍 البحث في حقل images المباشر للمستخدم")
            images_list = [img.strip() for img in user.images.split(',') if img.strip()]
            if images_list:
                first_image = images_list[0]
                print(f"📸 الصورة من حقل images: '{first_image}'")
                
                # استخدام المسار من حقل path إذا كان موجوداً
                if hasattr(user, 'path') and user.path:
                    path_list = [p.strip() for p in user.path.split(',') if p.strip()]
                    print(f"🗂️ قائمة المسارات: {path_list}")
                    
                    for image_path in path_list:
                        if first_image in image_path:
                            print(f"✅ وجدت مسار مطابق: '{image_path}'")
                            return image_path
                
                # بناء المسار افتراضياً
                default_path = f"images/users/{user.id}/{first_image}"
                print(f"📁 المسار الافتراضي: '{default_path}'")
                
                # التحقق من وجود الملف فعلياً
                static_path = os.path.join(settings.STATIC_ROOT, default_path)
                media_path = os.path.join(settings.MEDIA_ROOT, default_path)
                
                if os.path.exists(static_path):
                    print(f"✅ الصورة موجودة في STATIC: {default_path}")
                    return f"/static/{default_path}"
                elif os.path.exists(media_path):
                    print(f"✅ الصورة موجودة في MEDIA: {default_path}")
                    return f"/media/{default_path}"
                else:
                    print(f"❌ الصورة غير موجودة في: {static_path} أو {media_path}")
        
        print(f"⚠️ لا توجد صور للمستخدم: {user.username}")
        return None
        
    except Exception as e:
        print(f"🚨 خطأ في get_user_profile_image: {e}")
        import traceback
        traceback.print_exc()
        return None

def force_find_arabic_image(user_id, image_name):
    """
    البحث القسري عن الصور العربية
    """
    try:
        # المسارات المباشرة للبحث
        direct_paths = [
            f"static/images/users/{user_id}/{image_name}",
            f"static/tifinar/images/users/user_{user_id}/{image_name}",
            f"images/users/{user_id}/{image_name}",
            f"tifinar/images/users/user_{user_id}/{image_name}",
            f"media/images/users/{user_id}/{image_name}",
            image_name
        ]
        
        for path in direct_paths:
            full_path = os.path.join(settings.BASE_DIR, path)
            if os.path.exists(full_path):
                print(f"🎯 وجدت الصورة العربية: {path}")
                # إرجاع المسار المناسب بناءً على الموقع
                if path.startswith('static/'):
                    return f"/{path}"
                elif path.startswith('media/'):
                    return f"/{path}"
                else:
                    return f"/static/{path}"
        
        # البحث في جميع أنحاء المشروع
        for root, dirs, files in os.walk(settings.BASE_DIR):
            for file in files:
                if file == image_name:
                    relative_path = os.path.relpath(os.path.join(root, file), settings.BASE_DIR)
                    print(f"🎯 وجدت الصورة في المشروع: {relative_path}")
                    return f"/{relative_path}".replace('\\', '/')
        
        return None
    except Exception as e:
        print(f"🚨 خطأ في force_find_arabic_image: {e}")
        return None

def debug_image_search(email):
    """
    دالة تصحيح متقدمة
    """
    try:
        user = AuthUser.objects.filter(email=email).first()
        if not user:
            print(f"❌ المستخدم غير موجود للبريد: {email}")
            return
            
        print(f"\n=== 🔍 DEBUG للبريد: {email} ===")
        print(f"👤 اسم المستخدم: {user.username}")
        print(f"🆔 ID المستخدم: {user.id}")
        
        # 🔥 طباعة مفصلة للحقول المهمة
        print(f"🔥🔥🔥 محتوى حقل images: '{getattr(user, 'images', 'غير موجود')}'")
        print(f"🔥🔥🔥 محتوى حقل path: '{getattr(user, 'path', 'غير موجود')}'")
        
        # فحص نظام الملفات
        print(f"\n📁 فحص نظام الملفات للمستخدم {user.id}:")
        
        possible_folders = [
            f"static/images/users/{user.id}",
            f"static/tifinar/images/users/{user.id}",
            f"media/images/users/{user.id}",
            f"images/users/{user.id}",
        ]
        
        for folder in possible_folders:
            folder_path = os.path.join(settings.BASE_DIR, folder)
            exists = os.path.exists(folder_path)
            print(f"   {folder}: {'✅ موجود' if exists else '❌ غير موجود'}")
            
            if exists:
                try:
                    files = os.listdir(folder_path)
                    print(f"   📂 محتويات {folder}: {files}")
                except Exception as e:
                    print(f"   ❌ خطأ في قراءة المجلد: {e}")
        
        print(f"\n📍 STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"📍 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"📍 BASE_DIR: {settings.BASE_DIR}")
        
    except Exception as e:
        print(f"🚨 خطأ في التصحيح: {e}")

def get_user_display_name(email):
    """
    الحصول على اسم العرض للمستخدم
    """
    try:
        user = AuthUser.objects.filter(email=email).first()
        if user:
            full_name = f"{user.first_name} {user.last_name}".strip()
            return full_name if full_name else user.username
    except Exception as e:
        print(f"Error getting user display name: {e}")
    
    return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_identifier(request):
    """الحصول على معرف المستخدم"""
    if request.user.is_authenticated:
        return request.user.username
    else:
        return get_client_ip(request)

def video_detail(request, slug):
    # التحقق من وجود المقال
    try:
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            article = videos.objects.get(slug=slug)
        else:
            article = videos.objects.get(slug=slug, visibility_status='public')
    except videos.DoesNotExist:
        raise Http404("المقال غير موجود أو غير منشور بعد")
    
    # معالجة التفاعلات والتعليقات
    user_identifier = get_user_identifier(request)
    
    if request.method == 'POST':
        # معالجة التفاعلات
        if 'reaction_type' in request.POST:
            reaction_type = request.POST.get('reaction_type')
            if reaction_type in ['love', 'like', 'dislike', 'sad', 'funny', 'angry']:
                existing_reaction = ArticleReaction.objects.filter(
                    ip_or_name=user_identifier,
                    page_title=article.title
                ).first()
                
                if existing_reaction:
                    if existing_reaction.reaction_type == reaction_type:
                        existing_reaction.delete()
                        messages.success(request, 'تم إلغاء تفاعلك بنجاح')
                    else:
                        existing_reaction.reaction_type = reaction_type
                        existing_reaction.liked_at = now()
                        existing_reaction.save()
                        messages.success(request, 'تم تحديث تفاعلك بنجاح')
                else:
                    ArticleReaction.objects.create(
                        ip_or_name=user_identifier,
                        page_title=article.title,
                        device_type=request.META.get('HTTP_USER_AGENT', 'Unknown')[:100],
                        reaction_type=reaction_type,
                        liked_at=now(),
                        created_at=now()
                    )
                    messages.success(request, 'شكراً على تفاعلك!')
        
        # معالجة التعليقات
        elif 'cmt_subject' in request.POST:
            cmt_subject = request.POST.get('cmt_subject', '').strip()
            author_name = request.POST.get('author_name', '').strip()
            author_email = request.POST.get('author_email', '').strip()
            
            if cmt_subject and author_name:
                if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                    visibility_status = 'public'
                else:
                    visibility_status = 'under_review'
                
                try:
                    comment = comments.objects.create(
                        page_title=article.title,
                        author_name=author_name,
                        cmt_subject=cmt_subject,
                        author_email=author_email if author_email else None,
                        visibility_status=visibility_status,
                        created_at=now(),
                        updated_at=now()
                    )
                    
                    messages.success(request, 
                        'شكراً على تعليقك! ' + 
                        ('سيظهر بعد المراجعة.' if visibility_status == 'under_review' else 'تم نشر تعليقك.')
                    )
                except Exception as e:
                    messages.error(request, f'حدث خطأ أثناء إضافة التعليق: {str(e)}')
            else:
                messages.error(request, 'يرجى ملء جميع الحقول المطلوبة')
    
    # الحصول على تفاعل المستخدم الحالي
    user_reaction = None
    if user_identifier:
        try:
            user_reaction = ArticleReaction.objects.filter(
                ip_or_name=user_identifier,
                page_title=article.title
            ).first()
        except:
            pass
    
    # حساب عدد التفاعلات
    try:
        reactions_count = ArticleReaction.objects.filter(page_title=article.title).values(
            'reaction_type'
        ).annotate(count=Count('id'))
        reactions_dict = {item['reaction_type']: item['count'] for item in reactions_count}
    except:
        reactions_dict = {}
    
    # الحصول على التعليقات وإضافة معلومات الصور
    try:
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            article_comments = comments.objects.filter(page_title=article.title).order_by('-created_at')
        else:
            article_comments = comments.objects.filter(
                page_title=article.title, 
                visibility_status='public'
            ).order_by('-created_at')
        
        print(f"📋 عدد التعليقات في قاعدة البيانات: {article_comments.count()}")
        
        comments_with_images = []
        user_auth_data = []  # ✅ إنشاء المتغير هنا
        
        for comment in article_comments:
            profile_image = None
            display_name = comment.author_name
            
            if comment.author_email:
                print(f"\n🔍 معالجة تعليق من: {comment.author_email}")
                
                user = AuthUser.objects.filter(email=comment.author_email).first()
                if user:
                    print(f"👤 وجدت المستخدم: {user.username} (ID: {user.id})")
                    
                    # ✅ جمع بيانات auth_user للعرض في القالب
                    user_auth_data.append({
                        'email': user.email,
                        'username': user.username,
                        'user_id': user.id,
                        'images': getattr(user, 'images', '❌ فارغ'),
                        'path': getattr(user, 'path', '❌ فارغ')
                    })
                    
                    # 🔥 طباعة محتوى الحقول قبل محاولة الحصول على الصورة
                    print(f"🔥🔥🔥 قبل get_user_profile_image - images: '{getattr(user, 'images', 'غير موجود')}'")
                    print(f"🔥🔥🔥 قبل get_user_profile_image - path: '{getattr(user, 'path', 'غير موجود')}'")
                    
                    # الحصول على الصورة
                    profile_image = get_user_profile_image(comment.author_email)
                    
                    # إذا لم توجد صورة، حاول البحث في الحقول المباشرة
                    if not profile_image and hasattr(user, 'images') and user.images:
                        images_list = [img.strip() for img in user.images.split(',') if img.strip()]
                        if images_list:
                            first_image = images_list[0]
                            if any(ord(c) > 127 for c in first_image):
                                print(f"🔤 الصورة تحتوي على حروف عربية: {first_image}")
                                profile_image = force_find_arabic_image(user.id, first_image)
                    
                    # الحصول على اسم العرض
                    user_display_name = get_user_display_name(comment.author_email)
                    if user_display_name:
                        display_name = user_display_name
                
                # تصحيح خاص للمستخدم حميد بعلوان
                if comment.author_email == 'hbialouan@gmail.com':
                    if not profile_image:
                        print("🎯 تفعيل التصحيح المتقدم لحميد بعلوان")
                        debug_image_search('hbialouan@gmail.com')
                        if user and hasattr(user, 'images') and user.images:
                            images_list = [img.strip() for img in user.images.split(',') if img.strip()]
                            if images_list:
                                first_image = images_list[0]
                                profile_image = force_find_arabic_image(user.id, first_image)
                    else:
                        print(f"✅ وجدت صورة لحميد بعلوان: {profile_image}")
            
            comments_with_images.append({
                'comment': comment,
                'profile_image': profile_image,
                'display_name': display_name
            })
            
        print(f"📊 عدد التعليقات بعد المعالجة: {len(comments_with_images)}")
            
    except Exception as e:
        comments_with_images = []
        user_auth_data = []  # ✅ تهيئة المتغير في حالة الخطأ
        print(f"🚨 Error fetching comments: {e}")
        import traceback
        traceback.print_exc()
    
    # الحصول على المقال التالي والمقالات ذات الصلة
    next_obj = (
        videos.objects.filter(
            vd_id__gt=article.vd_id, 
            visibility_status='public'
        ).order_by('vd_id').first() or
        videos.objects.filter(
            vd_id__lt=article.vd_id,
            visibility_status='public'
        ).order_by('-vd_id').first()
    )

    base_query = videos.objects.exclude(slug=slug).filter(visibility_status='public')
    
    if request.user.is_authenticated:
        user = request.user
        query = Q()
        
        if hasattr(user, 'educational_level') and user.educational_level:
            query |= Q(educational_level=user.educational_level)
        
        if hasattr(user, 'gender') and user.gender:
            query |= Q(gender=user.gender) | Q(gender='all')
        else:
            query |= Q(gender='all')
        
        if hasattr(user, 'Date_de_naissance') and user.Date_de_naissance:
            try:
                age = timezone.now().year - user.Date_de_naissance.year
                query |= Q(min_age__lte=age, max_age__gte=age)
            except:
                pass
        
        if query:
            related_articles = base_query.filter(query)
        else:
            related_articles = base_query.filter(
                Q(the_type__in=['أصناف أخرى', 'الثقافة العامة', 'without_board', 'عام', 'متنوع']) |
                Q(the_type__isnull=True)
            )
    else:
        related_articles = base_query.filter(
            Q(the_type__in=['أصناف أخرى', 'الثقافة العامة', 'without_board', 'عام', 'متنوع']) |
            Q(the_type__isnull=True) |
            Q(gender='all')
        ).filter(
            Q(min_age__lte=18, max_age__gte=18)
        )

    related_articles = list(related_articles.order_by('?')[:6])

    # إعداد السياق
    context = {
        'article': article,
        'title': article.title,
        'subject': article.mysubject,
        'description': article.mydescription,
        'myimage': article.myimage,
        'folder': "videos",
        'author': article.author,
        'autre': article.autre,
        'dir': article.dir,
        'next_obj': next_obj,
        'related_articles': related_articles,
        'updated_at': article.updated_at,
        'keywords': article.keywords,
        'reactions': reactions_dict,
        'reaction_type': user_reaction.reaction_type if user_reaction else None,
        'comments': article_comments,
        'comments_with_images': comments_with_images,
        'comments_count': article_comments.count(),
        'user_auth_data': user_auth_data,  # ✅ إضافة البيانات الجديدة
    }
    
    print(f"🎯 تم إعداد السياق مع {len(comments_with_images)} تعليق و {len(user_auth_data)} مستخدم")
    
    return render(request, 'tifinar/showVideo.html', context)