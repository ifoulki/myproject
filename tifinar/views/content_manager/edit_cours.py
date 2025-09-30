import os
import re
import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.forms.utils import ErrorDict
from django.contrib import messages
from tifinar.myForms.cours.create_cours_form import CoursForm
from tifinar.models import cours
from tifinar.views.content_manager.create_cours import (
    advanced_transliterator, 
    simple_unique_id, 
    handle_uploaded_file
)
from django.contrib.auth.decorators import login_required
from tifinar.models import comments
from tifinar.forms import CommentForm
import unicodedata

logger = logging.getLogger(__name__)

def normalize_text(text):
    """تطبيع النص لإزالة الاختلافات غير المرئية"""
    if not text:
        return ""
    # إزالة التشكيل والتحويل إلى شكل قياسي
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    # إزالة المسافات الزائدة والأحرف الخاصة
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return text

@login_required
def edit_course_view(request, slug):
    logger.info(f"بدء عملية تعديل درس: {slug}")
    
    cour = get_object_or_404(cours, slug=slug)
    
    # تسجيل مفصل للتحقق من القيم
    logger.info(f"cour.images: {repr(cour.images)}")
    logger.info(f"نوع cour.images: {type(cour.images)}")
    
    # إنشاء images_list بشكل صحيح
    images_list = []
    if cour.images:
        if isinstance(cour.images, str):
            images_list = [img.strip() for img in cour.images.split(',') if img.strip()]
            logger.info(f"images_list بعد الإنشاء: {images_list}")
        else:
            logger.warning(f"cour.images ليس نصاً: {type(cour.images)}")
    else:
        logger.info("cour.images فارغ")
    
    # جلب التعليقات المرتبطة بالدرس
    content_comments = []
    comment_forms = []
    
    print(f"=== بدء التحقق من التعليقات ===")
    print(f"عنوان الدرس: '{cour.title}'")
    
    # جلب التعليقات التي تطابق عنوان الدرس بالضبط
    all_comments = comments.objects.filter(page_title__isnull=False)
    print(f"عدد التعليقات (غير NULL): {all_comments.count()}")
    
    for comment in all_comments:
        # المقارنة البسيطة بدون تطبيع مفرط
        title_match = comment.page_title.strip() == cour.title.strip()
        
        print(f"التعليق {comment.cmt_id}: '{comment.page_title}'")
        print(f"  تطابق مع '{cour.title}'؟ {title_match}")
        
        if title_match:
            content_comments.append(comment)
            print(f"  -> تمت الإضافة (تطابق تام)")
    
    print(f"عدد التعليقات المرتبطة: {len(content_comments)}")
    
    # إنشاء نماذج لكل تعليق
    for comment in content_comments:
        comment_forms.append(CommentForm(instance=comment))
    
    comment_count = len(content_comments)
    
    # تحويل zip إلى list لحل المشكلة - الإصلاح هنا
    comments_list = list(zip(content_comments, comment_forms))
    
    try:
        if request.method == 'POST':
            # التحقق مما إذا كان الطلب لتعديل درس أو تعليق
            if 'comment_id' in request.POST:
                comment_id = request.POST.get('comment_id')
                try:
                    comment_obj = comments.objects.get(cmt_id=comment_id)
                    
                    # تحديث الحقول يدوياً
                    comment_obj.author_name = request.POST.get('author_name')
                    comment_obj.author_email = request.POST.get('author_email')
                    comment_obj.cmt_subject = request.POST.get('cmt_subject')
                    comment_obj.visibility_status = request.POST.get('visibility_status')
                    comment_obj.updated_at = timezone.now()
                    
                    comment_obj.save()
                    messages.success(request, 'تم تحديث التعليق بنجاح')
                    return redirect('edit_cours', slug=slug)

                except comments.DoesNotExist:
                    messages.error(request, 'التعليق غير موجود')
                except Exception as e:
                    messages.error(request, f'حدث خطأ في تحديث التعليق: {str(e)}')
                    
            else:
                # هذا طلب لتعديل الدرس
                logger.info("طلب POST مستلم لتعديل الدرس")
                form = CoursForm(request.POST, request.FILES, instance=cour)
                
                if form.is_valid():
                    logger.info("النموذج صالح، بدء تحديث البيانات")
                    obj = form.save(commit=False)
                    
                    # تحديث slug إذا تغير العنوان
                    title = form.cleaned_data['title']
                    if title and title != cour.title:
                        obj.slug = advanced_transliterator(title)
                    
                    # معالجة الصورة الرئيسية الجديدة
                    if 'myimage' in request.FILES:
                        image_file = request.FILES['myimage']
                        image_name = handle_uploaded_file(image_file, "", obj.slug, is_main_image=True)
                        if image_name:
                            if cour.myimage and cour.myimage != image_name:
                                old_image_path = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'cours', cour.myimage)
                                if os.path.exists(old_image_path):
                                    os.remove(old_image_path)
                            obj.myimage = image_name
                    
                    # معالجة الصور المتعددة الجديدة
                    images_files = request.FILES.getlist('images[]')
                    image_names = request.POST.getlist('image_names[]')
                    
                    # الحصول على اسم المجلد وتنظيفه
                    folder_name = form.cleaned_data.get('myfile', 'default_folder')
                    if folder_name:
                        folder_name = re.sub(r'[^a-zA-Z0-9_-]', '', folder_name)
                        if not folder_name:
                            folder_name = 'default_folder'
                    else:
                        folder_name = 'default_folder'
                    
                    # البدء بالصور الحالية
                    saved_images = images_list.copy()
                    
                    # إضافة الصور الجديدة
                    for i, (image_file, image_name) in enumerate(zip(images_files, image_names)):
                        if image_file:
                            custom_name = image_name.strip() if image_name else f"image_{i+1}"
                            custom_name = re.sub(r'[^a-zA-Z0-9_-]', '', custom_name)
                            if not custom_name:
                                custom_name = f"image_{i+1}"
                            
                            file_name = handle_uploaded_file(image_file, folder_name, custom_name, is_main_image=False)
                            if file_name:
                                saved_images.append(file_name)
                    
                    # حفظ أسماء الصور
                    if saved_images:
                        obj.images = ", ".join(saved_images)
                    
                    # تحديث وقت التعديل
                    obj.updated_at = timezone.now()
                    
                    obj.save()
                    
                    messages.success(request, 'تم تحديث الدرس بنجاح.')
                    return redirect('edit_cours', slug=obj.slug)
                else:
                    messages.error(request, 'حدث خطأ في تحديث البيانات. يرجى تصحيح الأخطاء أدناه.')
                    context = {
                        'form': form, 
                        'cour': cour,
                        'title': cour.title,
                        'images_list': images_list,
                        'comments': comments_list,  # استخدام المتغير المحول
                        'comment_count': comment_count,
                    }

                    return render(request, 'tifinar/auth/cours/edit_cours.html', context)
        else:
            # عرض النموذج مع البيانات الحالية
            form = CoursForm(instance=cour)
            
            context = {
                'form': form, 
                'cour': cour,
                'title': cour.title,
                'images_list': images_list,
                'comments': comments_list,  # استخدام المتغير المحول
                'comment_count': comment_count,
              }
            
            return render(request, 'tifinar/auth/cours/edit_cours.html', context)
            
    except Exception as e:
        logger.error(f"حدث خطأ في تعديل الدرس: {str(e)}", exc_info=True)
        
        form = CoursForm(request.POST or None, request.FILES or None, instance=cour)
        
        error_msg = f"حدث خطأ غير متوقع في النظام: {str(e)}. يرجى المحاولة مرة أخرى."
        
        messages.error(request, error_msg)
        context = {
            'form': form, 
            'cour': cour,
            'title': cour.title,
            'images_list': images_list,
            'comments': comments_list,  # استخدام المتغير المحول
            'comment_count': comment_count,
            'error_message': error_msg
        }
        return render(request, 'tifinar/auth/cours/edit_cours.html', context)