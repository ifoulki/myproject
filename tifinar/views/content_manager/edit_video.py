from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from tifinar.models import videos, comments
from tifinar.forms import VideoForm, CommentForm
from django.contrib import messages
import os
from django.conf import settings
import logging
import re
from django.db.models import Q
logger = logging.getLogger(__name__)
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib as mpl
from django.utils import timezone
import unicodedata

plt.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

def reshape_arabic(text):
    """دالة لإعادة تشكيل النصوص العربية"""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def generate_chart_image(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100, transparent=True)
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

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

CONTENT_TYPES = {
    'videos': {
        'model': videos,
        'id_field': 'vd_id',
        'subject_field': 'mysubject',
        'template': 'edit_video.html',
        'redirect_name': 'show_video',
        'form_class': VideoForm,
        'types': ['أدب', 'علوم', 'تاريخ', 'فلسفة']
    },
}
    
def edit_video(request, slug):
    # تحديد نوع المحتوى مباشرة داخل الدالة
    content_type = 'videos'
    config = CONTENT_TYPES.get(content_type)
    
    if not config:
        return HttpResponseNotFound("نوع المحتوى غير موجود")

    ModelClass = config['model']
    content = get_object_or_404(ModelClass, slug=slug)

    # جلب التعليقات المرتبطة بالكتاب
    content_comments = []
    comment_forms = []

    if content_type == 'videos':
        print(f"=== بدء التحقق من التعليقات ===")
        print(f"عنوان الكتاب: '{content.title}'")
        print(f"slug الكتاب: '{slug}'")
        
        # تطبيع العناوين للمقارنة
        normalized_video_title = normalize_text(content.title)
        print(f"العنوان بعد التطبيع: '{normalized_video_title}'")
        
        # جلب جميع التعليقات غير NULL
        all_comments = comments.objects.filter(page_title__isnull=False)
        print(f"عدد التعليقات (غير NULL): {all_comments.count()}")
        
        # البحث بالتطابق الكامل فقط
        for comment in all_comments:
            normalized_comment_title = normalize_text(comment.page_title)
            
            # التطابق الكامل فقط - تم إزالة التطابق الجزئي
            exact_match = normalized_comment_title == normalized_video_title
            
            print(f"التعليق {comment.cmt_id}: '{comment.page_title}'")
            print(f"  تطبيع: '{normalized_comment_title}'")
            print(f"  تطابق تام؟ {exact_match}")
            
            if exact_match:
                content_comments.append(comment)
                print(f"  -> تمت الإضافة (تطابق كامل)")
            else:
                print(f"  -> لم تتم الإضافة (لا يوجد تطابق كامل)")
            print(f"  ---")
        
        print(f"عدد التعليقات المرتبطة: {len(content_comments)}")
        
        # إنشاء نماذج لكل تعليق
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))
            print(f"تم إنشاء نموذج للتعليق {comment.cmt_id}")

    if request.method == 'POST':
        # التحقق مما إذا كان الطلب لتعديل كتاب أو تعليق
        if 'comment_id' in request.POST:
            # هذا طلب لتعديل تعليق
            comment_id = request.POST.get('comment_id')
            try:
                comment_obj = comments.objects.get(cmt_id=comment_id)
                
                # تحديث الحقول يدوياً لتجنب مشاكل النموذج
                comment_obj.author_name = request.POST.get('author_name')
                comment_obj.author_email = request.POST.get('author_email')
                comment_obj.cmt_subject = request.POST.get('cmt_subject')
                comment_obj.visibility_status = request.POST.get('visibility_status')
                comment_obj.updated_at = timezone.now()
                
                comment_obj.save()
                messages.success(request, 'تم تحديث التعليق بنجاح')
                print(f"تم تحديث التعليق {comment_id} بنجاح")
                return redirect(request.path)

            except comments.DoesNotExist:
                error_msg = 'التعليق غير موجود'
                messages.error(request, error_msg)
                print(error_msg)
            except Exception as e:
                error_msg = f'حدث خطأ في تحديث التعليق: {str(e)}'
                messages.error(request, error_msg)
                print(error_msg)
                
        else:
            # هذا طلب لتعديل الكتاب
            form = config['form_class'](request.POST, request.FILES, instance=content)
            if form.is_valid():
                try:
                    content = form.save(commit=False)
                    image_fields = ['myimage', 'autre']
                    original_images = {field: getattr(content, field, '') for field in image_fields}

                    for field in image_fields:
                        if field in request.FILES and request.FILES[field]:
                            new_files = request.FILES.getlist(field)
                            processed_value = handle_uploaded_images(
                                new_files, original_images[field], content.slug, field.split('_')[-1]
                            )
                            setattr(content, field, processed_value)
                        else:
                            setattr(content, field, original_images[field])

                    content.save()

                    if hasattr(form, 'save_m2m'):
                        form.save_m2m()

                    messages.success(request, 'تم تحديث الكتاب بنجاح')
                    print(f"تم تحديث الكتاب {content.title} بنجاح")
                    return redirect(request.path)
                    
                except Exception as e:
                    error_msg = f'حدث خطأ في تحديث الكتاب: {str(e)}'
                    messages.error(request, error_msg)
                    print(error_msg)
            else:
                error_msg = 'بيانات النموذج غير صالحة'
                messages.error(request, error_msg)
                print(error_msg)
                for field, errors in form.errors.items():
                    for error in errors:
                        error_detail = f"{field}: {error}"
                        messages.error(request, error_detail)
                        print(error_detail)

    else:
        form = config['form_class'](instance=content)

    # إذا لم تكن هناك نماذج تعليقات، أنشئها
    if not comment_forms and content_type == 'videos':
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))

    context = {
        'video': content,
        'title': content.title,
        'description': content.mydescription,
        'form': form,
        'content_types': config['types'],
        'comments': zip(content_comments, comment_forms) if content_type == 'videos' else [],
        'comment_count': len(content_comments) if content_type == 'videos' else 0
    }

    print(f"تم تحضير context مع {len(content_comments)} تعليقات")
    return render(request, f'tifinar/auth/videos/edit_video.html', context)

def handle_uploaded_images(new_images, existing_images, slug, image_type):
    image_names = []
    if existing_images and isinstance(existing_images, str):
        image_names = existing_images.split(',')

    for i, image in enumerate(new_images, start=1):
        ext = os.path.splitext(image.name)[1]
        new_name = f"{slug}_{image_type}_{i}{ext}"
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', new_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        image_names.append(new_name)

    return ','.join(image_names)