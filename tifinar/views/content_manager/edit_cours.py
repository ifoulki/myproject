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

logger = logging.getLogger(__name__)

@login_required
def edit_course_view(request, slug):
    logger.info(f"بدء عملية تعديل درس: {slug}")
    
    # الحصول على الكائن المطلوب تعديله
    cour = get_object_or_404(cours, slug=slug)
    
    try:
        if request.method == 'POST':
            logger.info("طلب POST مستلم لتعديل الدرس")
            form = CoursForm(request.POST, request.FILES, instance=cour)
            
            if form.is_valid():
                logger.info("النموذج صالح، بدء تحديث البيانات")
                obj = form.save(commit=False)
                
                # تحديث slug إذا تغير العنوان
                title = form.cleaned_data['title']
                if title and title != cour.title:
                    obj.slug = advanced_transliterator(title)
                    logger.info(f"الـ slug الجديد: {obj.slug}")
                
                # معالجة الصورة الرئيسية الجديدة
                if 'myimage' in request.FILES:
                    logger.info("تم رفع صورة رئيسية جديدة")
                    image_file = request.FILES['myimage']
                    image_name = handle_uploaded_file(image_file, "", obj.slug, is_main_image=True)
                    if image_name:
                        # حذف الصورة القديمة إذا كانت موجودة
                        if cour.myimage and cour.myimage != image_name:
                            old_image_path = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'cours', cour.myimage)
                            if os.path.exists(old_image_path):
                                os.remove(old_image_path)
                                logger.info(f"تم حذف الصورة القديمة: {cour.myimage}")
                        
                        obj.myimage = image_name
                        logger.info(f"تم حفظ الصورة الرئيسية الجديدة: {image_name}")
                
                # معالجة الصور المتعددة الجديدة
                images_files = request.FILES.getlist('images[]')
                image_names = request.POST.getlist('image_names[]')
                
                logger.info(f"عدد الصور الجديدة المرفوعة: {len(images_files)}")
                logger.info(f"أسماء الصور الجديدة: {image_names}")
                
                # الحصول على اسم المجلد وتنظيفه
                folder_name = form.cleaned_data.get('myfile', 'default_folder')
                if folder_name:
                    folder_name = re.sub(r'[^a-zA-Z0-9_-]', '', folder_name)
                    if not folder_name:
                        folder_name = 'default_folder'
                else:
                    folder_name = 'default_folder'
                
                logger.info(f"اسم المجلد بعد التنظيف: {folder_name}")
                
                saved_images = []
                
                # إذا كان هناك صور حالية، نبدأ منها
                if obj.images:
                    saved_images = [img.strip() for img in obj.images.split(',')]
                
                # إضافة الصور الجديدة
                for i, (image_file, image_name) in enumerate(zip(images_files, image_names)):
                    if image_file:
                        # استخدام الاسم المقدم أو إنشاء اسم افتراضي
                        custom_name = image_name.strip() if image_name else f"image_{i+1}"
                        # تنظيف الاسم من الأحرف غير المسموحة
                        custom_name = re.sub(r'[^a-zA-Z0-9_-]', '', custom_name)
                        if not custom_name:
                            custom_name = f"image_{i+1}"
                        
                        file_name = handle_uploaded_file(image_file, folder_name, custom_name, is_main_image=False)
                        if file_name:
                            saved_images.append(file_name)
                            logger.info(f"تم حفظ الصورة الجديدة: {file_name}")
                        else:
                            logger.error(f"فشل في حفظ الصورة: {image_file.name}")
                
                # حفظ أسماء الصور في حقل images كسلسلة مفصولة بفواصل
                if saved_images:
                    obj.images = ", ".join(saved_images)
                    logger.info(f"أسماء الصور المحفوظة: {obj.images}")
                else:
                    logger.warning("لم يتم حفظ أي صور إضافية")
                
                # تحديث وقت التعديل
                obj.updated_at = timezone.now()
                
                logger.info("تحديث الكائن في قاعدة البيانات")
                obj.save()
                logger.info("تم تحديث الكائن بنجاح")
                
                messages.success(request, 'تم تحديث الدرس بنجاح.')
                return redirect('cours_edit')
            else:
                logger.error(f"أخطاء النموذج: {form.errors}")
                messages.error(request, 'حدث خطأ في تحديث البيانات. يرجى تصحيح الأخطاء أدناه.')
                return render(request, 'tifinar/auth/cours/edit_cours.html', {'form': form, 'cour': cour})
        else:
            # عرض النموذج مع البيانات الحالية
            form = CoursForm(instance=cour)
            logger.info("طلب GET، عرض نموذج التعديل")
            return render(request, 'tifinar/auth/cours/edit_cours.html', {'form': form, 'cour': cour})
            
    except Exception as e:
        logger.error(f"حدث خطأ في تعديل الدرس: {str(e)}", exc_info=True)
        
        form = CoursForm(request.POST or None, request.FILES or None, instance=cour)
        
        error_msg = f"حدث خطأ غير متوقع في النظام: {str(e)}. يرجى المحاولة مرة أخرى."
        messages.error(request, error_msg)
        
        return render(request, 'tifinar/auth/cours/edit_cours.html', {
            'form': form,
            'cour': cour,
            'error_message': error_msg
        })