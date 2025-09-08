from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from tifinar.models import cours, ArticleReaction, comments, AuthUser
from django.conf import settings
from django.contrib import messages
from django.utils.timezone import now
import os
import urllib.parse
import random

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
            return None
            
        # البحث في الحقول المباشرة في نموذج AuthUser
        if hasattr(user, 'images') and user.images:
            images_list = [img.strip() for img in user.images.split(',') if img.strip()]
            if images_list:
                first_image = images_list[0]
                
                # استخدام المسار من حقل path إذا كان موجوداً
                if hasattr(user, 'path') and user.path:
                    path_list = [p.strip() for p in user.path.split(',') if p.strip()]
                    for image_path in path_list:
                        if first_image in image_path:
                            return image_path
                
                # بناء المسار افتراضياً
                default_path = f"images/users/{user.id}/{first_image}"
                
                # التحقق من وجود الملف فعلياً
                static_path = os.path.join(settings.STATIC_ROOT, default_path)
                media_path = os.path.join(settings.MEDIA_ROOT, default_path)
                
                if os.path.exists(static_path):
                    return f"/static/{default_path}"
                elif os.path.exists(media_path):
                    return f"/media/{default_path}"
        
        return None
        
    except Exception as e:
        print(f"Error in get_user_profile_image: {e}")
        return None

def get_user_display_name(email):
    """
    الحصول على اسم العرض للمستخدم
    """
    try:
        user = AuthUser.objects.filter(email=email).first()
        if user:
            full_name = f"{user.first_name} {user.last_name}".strip()
            return full_name if full_name else user.username
    except Exception:
        pass
    
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
def show_cours(request, slug):
    # الحصول على الكورس أو إظهار 404
    cour = get_object_or_404(cours, slug=slug)
    
    # معالجة محتويات الكورس والصور
    contents = cour.cours_contents.split(',') if cour.cours_contents else []
    images = cour.images.split(',') if cour.images else []
    
    # إقران المحتوى مع الصور
    content_image_pairs = [
        {'content': c.strip(), 'image': i.strip()} 
        for c, i in zip(contents, images) 
        if c.strip() and i.strip()
    ]
    
    # خلط المحتوى عشوائياً
    random.shuffle(content_image_pairs)
    
    # الحصول على معرف المستخدم
    user_identifier = get_user_identifier(request)
    
    # معالجة طلبات POST (التفاعلات والتعليقات)
    if request.method == 'POST':
        # معالجة التفاعلات
        if 'reaction_type' in request.POST:
            reaction_type = request.POST.get('reaction_type')
            if reaction_type in ['love', 'like', 'dislike', 'sad', 'funny', 'angry']:
                existing_reaction = ArticleReaction.objects.filter(
                    ip_or_name=user_identifier,
                    page_title=cour.title
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
                        page_title=cour.title,
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
                        page_title=cour.title,
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
                page_title=cour.title
            ).first()
        except:
            pass
    
    # حساب عدد التفاعلات
    try:
        reactions_count = ArticleReaction.objects.filter(page_title=cour.title).values(
            'reaction_type'
        ).annotate(count=Count('id'))
        reactions_dict = {item['reaction_type']: item['count'] for item in reactions_count}
    except:
        reactions_dict = {}
    
    # الحصول على التعليقات وإضافة معلومات الصور
    try:
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            article_comments = comments.objects.filter(page_title=cour.title).order_by('-created_at')
        else:
            article_comments = comments.objects.filter(
                page_title=cour.title, 
                visibility_status='public'
            ).order_by('-created_at')
        
        comments_with_images = []
        user_auth_data = []
        
        for comment in article_comments:
            profile_image = None
            display_name = comment.author_name
            
            if comment.author_email:
                user = AuthUser.objects.filter(email=comment.author_email).first()
                if user:
                    # جمع بيانات auth_user للعرض في القالب
                    user_auth_data.append({
                        'email': user.email,
                        'username': user.username,
                        'user_id': user.id,
                        'images': getattr(user, 'images', '❌ فارغ'),
                        'path': getattr(user, 'path', '❌ فارغ')
                    })
                    
                    # الحصول على الصورة
                    profile_image = get_user_profile_image(comment.author_email)
                    
                    # الحصول على اسم العرض
                    user_display_name = get_user_display_name(comment.author_email)
                    if user_display_name:
                        display_name = user_display_name
            
            comments_with_images.append({
                'comment': comment,
                'profile_image': profile_image,
                'display_name': display_name
            })
            
    except Exception as e:
        comments_with_images = []
        user_auth_data = []
        print(f"Error fetching comments: {e}")
    
    # ⭐⭐ إضافة الجزء الخاص بـ sidebar ⭐⭐
    # الحصول على المقال التالي
    next_obj = (
        cours.objects.filter(
            cours_id__gt=cour.cours_id, 
            visibility_status='public'
        ).order_by('cours_id').first() or
        cours.objects.filter(
            cours_id__lt=cour.cours_id,
            visibility_status='public'
        ).order_by('-cours_id').first()
    )

    # الحصول على المقالات ذات الصلة
    base_query = cours.objects.exclude(slug=slug).filter(visibility_status='public')
    
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
        'title': cour.title,
        'articles': cour.title,
        'updated_at': cour.updated_at,
        'the_type': cour.the_type,
        'intro': cour.intro,
        'folder_child': cour.myfile,
        'image': cour.myimage,
        'dir': cour.dir or 'rtl',
        'content_image_pairs': content_image_pairs,
        'cours_contents': contents,
        'images': images,
        # إضافة متغيرات التعليقات والتفاعلات
        'reactions': reactions_dict,
        'reaction_type': user_reaction.reaction_type if user_reaction else None,
        'comments': article_comments,
        'comments_with_images': comments_with_images,
        'comments_count': article_comments.count() if 'article_comments' in locals() else 0,
        'user_auth_data': user_auth_data,
        # ⭐⭐ إضافة المتغيرات الجديدة للـ sidebar ⭐⭐
        'next_obj': next_obj,
        'related_articles': related_articles,
        'folder': 'cours',  # هذا مهم ليظهر المحتوى بشكل صحيح
    }
    
    return render(request, 'tifinar/showCours.html', context)