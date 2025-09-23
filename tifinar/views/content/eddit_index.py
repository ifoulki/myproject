from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tifinar.models import articles, videos, cours, books, exams, msgs
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
from django.contrib import messages
from django.http import HttpResponseForbidden

def index_eddit(request):
    # معالجة معلمات البحث والتصفية
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()
    path = request.path.strip('/')

    # تحديد نوع المحتوى بناء على المسار
    if path == "videos_edit":
        model = videos
        title = "فيديوهات"
        order_field = "-vd_id"
        description = "مجلة تيفيناغ الثقافية تضم سلسلات كثيرة ومتنوعة لفيديوهات ثقافية، تربوية وتعليمية ... إلخ، يمكتكم متابعتها والاستفادة منها مجانا"
        has_slug = True
    elif path == "cours_edit":
        model = cours
        title = "قواميس بصرية"  
        order_field = "-cours_id"
        description = "موقع تيفيناغ يقدم لكم مجموعة من القواميس البصرية لأجل مساعدة الراغبين في إغناء رصيدهم اللغوي، بطريقة سهلة ومبسطة بالصوت والصورة"
        has_slug = True
    
    elif path == "msgs_edit":
        model = msgs
        title = "الرسائل الواردة"  
        order_field = "-msg_id"
        description = "رسائلك الواردة من المستخدمين الآخرين"
        has_slug = False
        
        if request.user.is_authenticated:
            user_id = request.user.id
            
            # جلب جميع الرسائل ثم التصفية يدوياً
            all_messages = model.objects.all().order_by(order_field)
            filtered_messages = []
            
            for msg in all_messages:
                # التحقق بكل الطرق الممكنة
                if str(msg.recipient) == str(user_id):
                    filtered_messages.append(msg)
                else:
                    try:
                        if int(msg.recipient) == user_id:
                            filtered_messages.append(msg)
                    except (ValueError, TypeError):
                        continue
            
            # تحويل إلى queryset
            from django.db.models.query import QuerySet
            queryset = QuerySet(model=model)
            queryset._result_cache = filtered_messages
            queryset._prefetch_done = True
            
        else:
            queryset = model.objects.none()
            
    elif path == "articles_edit":
        model = articles
        title = "مقالات"
        order_field = "-art_id"
        description = "مجلة تيفيناغ تقترح عليكم مجموعة من المقالات في مختلف المجالات العلمية والثقافية والتربوية، ويمكن للزوار أيضا إغناء الموقع بمشاركاتهم في النشر عبر مشاركة مواضيغهم معنا"
        has_slug = True
    elif path == "exams_edit":
        model = exams
        title = "اختبارات"
        order_field = "-exam_id"
        description = "موقع مجلة تيفيناغ يعد منصة رائعة للراغبين في الإستعداد الجيد للإمتحانات، حيث يمكن من خلاله للزوار اجتياز اختبارات تجريبية online  وتظهر لهم النتيجة مباشرة بعد نهاية الاختبار، وذلك يساعدهم على تتبع مستواهم أثناء الاستعداد للإمتحانات"
        has_slug = True
    elif path == "books_edit":
        model = books
        title = "مكتبة تيفيناغ"
        order_field = "-books_id"
        description = 'في مكتبة تيفيناغ يمكن تحميل كتب متنوعة مجانا، بما فيها الكتب المدرسية ونماذج امتحانات وفروض لتدريب التلاميذ وإعدادهم للاختبارات المدرسية'
        has_slug = True
    else:
        return render(request, 'tifinar/404.html', status=404)

    # إنشاء queryset مع مراعاة وجود slug (لجميع النماذج ما عدا msgs)
    if path != "msgs_edit":  # تم معالجة msgs بشكل منفصل أعلاه
        if has_slug:
            queryset = model.objects.exclude(slug__isnull=True).exclude(slug__exact='')
        else:
            queryset = model.objects.all()

    # تطبيق عوامل التصفية (لجميع النماذج ما عدا msgs)
    if path != "msgs_edit":
        if the_type:
            queryset = queryset.filter(the_type__icontains=the_type)

        if search:
            # إنشاء شروط البحث
            search_conditions = Q()
            
            # إضافة الحقول المتاحة بناءً على النموذج
            if hasattr(model, 'title'):
                search_conditions |= Q(title__icontains=search)
            if hasattr(model, 'keywords'):
                search_conditions |= Q(keywords__icontains=search)
            if hasattr(model, 'the_type'):
                search_conditions |= Q(the_type__icontains=search)
            if hasattr(model, 'mysubject'):
                search_conditions |= Q(mysubject__icontains=search)
            if hasattr(model, 'mydescription'):
                search_conditions |= Q(mydescription__icontains=search)
            
            queryset = queryset.filter(search_conditions)

        # الترتيب حسب الحقل المناسب لكل نموذج
        queryset = queryset.order_by(order_field)

    # تطبيق البحث والتصفية لجدول msgs (بعد التصفية الأساسية)
    if path == "msgs_edit" and request.user.is_authenticated:
        if the_type:
            queryset = queryset.filter(the_type__icontains=the_type)

        if search:
            search_conditions = Q()
            search_conditions |= Q(mysubject__icontains=search)
            search_conditions |= Q(title__icontains=search)
            search_conditions |= Q(author__icontains=search)
            search_conditions |= Q(email__icontains=search)
            
            queryset = queryset.filter(search_conditions)

    # معالجة الصور للمحتوى
    for item in queryset:
        if hasattr(item, 'myimage') and item.myimage:
            item.images = item.myimage.split(',')
        else:
            item.images = []

    # إعداد قائمة أنواع المحتوى للتصفية
    types_list = [
        'الأمازيغية',
        'تربية وتعليم',
        'الثقافة العامة',
        'علوم',
        'القانون وحقوق الإنسان'
    ]

    # إضافة Pagination
    paginator = Paginator(queryset, 10)  # 10 عناصر لكل صفحة
    page = request.GET.get('page')
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    # إعداد بيانات القالب
    context = {
        'current_url': request.build_absolute_uri(),
        'description': description,
        'title': title,
        'dir': 'rtl',
        'articles': items,
        'types_list': types_list,
        'table_name': model._meta.db_table,
    }

    if model == videos:
        return render(request, "tifinar/auth/videos/index_videos.html", context)
    elif model == books:
        return render(request, "tifinar/auth/books/index_books.html", context)
    elif model == articles:
        return render(request, "tifinar/auth/articles/index_articles.html", context)
    elif model == exams:
        return render(request, "tifinar/auth/exams/index_exams.html", context)
    elif model == cours:
        return render(request, "tifinar/auth/cours/index_cours.html", context)
    elif model == msgs:
        # إضافة معلومات إضافية للرسائل
        context.update({
            'user_messages_count': queryset.count() if request.user.is_authenticated else 0,
            'is_inbox': True,  # للإشارة إلى أن هذه هي الرسائل الواردة
        })
        return render(request, "tifinar/auth/msgs/index_msgs.html", context)
    else:
        return render(request, 'tifinar/404.html', status=404)

def delete_content(request, slug):
    if request.method == 'POST':
        try:
            # تحديد النموذج بناءً على المسار
            path = request.path
            if 'articles/delete' in path:
                model = articles
                lookup_field = 'slug'
            elif 'videos/delete' in path:
                model = videos
                lookup_field = 'slug'
            elif 'cours/delete' in path:
                model = cours
                lookup_field = 'slug'
            elif 'books/delete' in path:
                model = books
                lookup_field = 'slug'
            elif 'exams/delete' in path:
                model = exams
                lookup_field = 'slug'
            elif 'msgs/delete' in path:
                model = msgs
                lookup_field = 'msg_id'
            else:
                messages.error(request, 'نوع المحتوى غير معروف.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            # استخدام get_object_or_404 مع الحقل المناسب
            if lookup_field == 'slug':
                item = get_object_or_404(model, slug=slug)
            elif lookup_field == 'msg_id':
                # تحويل slug إلى msg_id
                try:
                    msg_id = int(slug)
                    item = get_object_or_404(model, msg_id=msg_id)
                    
                    # التحقق من أن المستخدم مسموح له بحذف هذه الرسالة (يجب أن يكون مستقبلها)
                    if model == msgs:
                        user_id_str = str(request.user.id)
                        if item.recipient != user_id_str:
                            messages.error(request, 'ليس لديك صلاحية حذف هذه الرسالة.')
                            return redirect(request.META.get('HTTP_REFERER', '/'))
                            
                except (ValueError, TypeError):
                    messages.error(request, 'معرف الرسالة غير صحيح.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            
            # حذف الملفات المرتبطة بالمحتوى إذا وجدت
            if hasattr(item, 'myimage') and item.myimage:
                image_paths = item.myimage.split(',')
                for image_path in image_paths:
                    full_path = os.path.join(settings.BASE_DIR, image_path.strip())
                    if os.path.exists(full_path):
                        os.remove(full_path)
            
            if hasattr(item, 'autre') and item.autre:
                attachment_paths = item.autre.split(',')
                for attachment_path in attachment_paths:
                    full_path = os.path.join(settings.BASE_DIR, attachment_path.strip())
                    if os.path.exists(full_path):
                        os.remove(full_path)
            
            # حذف المحتوى من قاعدة البيانات
            item.delete()
            
            messages.success(request, 'تم حذف المنشور بنجاح.')
            return redirect(request.META.get('HTTP_REFERER', '/'))            
        except Http404:
            messages.error(request, 'المنشور المطلوب غير موجود.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المنشور: {str(e)}')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return HttpResponseForbidden()

def delete_msg(request, msg_id):
    """حذف رسالة باستخدام msg_id"""
    if request.method == 'POST':
        try:
            # الحصول على الرسالة باستخدام msg_id
            msg = get_object_or_404(msgs, msg_id=msg_id)
            
            # التحقق من أن المستخدم مسموح له بحذف هذه الرسالة (يجب أن يكون مستقبلها)
            user_id_str = str(request.user.id)
            if msg.recipient != user_id_str:
                messages.error(request, 'ليس لديك صلاحية حذف هذه الرسالة.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            # حذف الملفات المرتبطة إذا وجدت
            if hasattr(msg, 'myimage') and msg.myimage:
                image_paths = msg.myimage.split(',')
                for image_path in image_paths:
                    full_path = os.path.join(settings.BASE_DIR, image_path.strip())
                    if os.path.exists(full_path):
                        os.remove(full_path)
            
            if hasattr(msg, 'autre') and msg.autre:
                attachment_paths = msg.autre.split(',')
                for attachment_path in attachment_paths:
                    full_path = os.path.join(settings.BASE_DIR, attachment_path.strip())
                    if os.path.exists(full_path):
                        os.remove(full_path)
            
            # حذف الرسالة من قاعدة البيانات
            msg.delete()
            
            messages.success(request, 'تم حذف الرسالة بنجاح.')
            
        except Http404:
            messages.error(request, 'الرسالة المطلوبة غير موجودة.')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف الرسالة: {str(e)}')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))