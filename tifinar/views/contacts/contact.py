from django.shortcuts import render, get_object_or_404, redirect
from tifinar.models import Contacts
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tifinar.myForms.contact.ContactEditForm import ContactEditForm

@login_required
def delete_contact(request, contacts_id):
    contact = get_object_or_404(Contacts, pk=contacts_id)
    
    # التحقق من الصلاحيات (فقط المدير يمكنه الحذف)
    if request.user.role != "admin":
        messages.error(request, 'ليس لديك صلاحية حذف الأعضاء')
        return redirect('contact_view', contacts_id=contacts_id)
    
    if request.method == 'POST':
        try:
            # حذف الصور إذا وجدت
            if contact.path:
                from django.conf import settings
                import os
                images = contact.path.split(',')
                for image in images:
                    image_path = os.path.join(settings.MEDIA_ROOT, 'images/contacts', image)
                    if os.path.exists(image_path):
                        os.remove(image_path)
            
            # حذف العضو
            contact.delete()
            messages.success(request, 'تم حذف العضو بنجاح')
            return redirect('contacts')  # التوجيه إلى صفحة الأعضاء الرئيسية
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء الحذف: {str(e)}')
            return redirect('contact_view', contacts_id=contacts_id)
    
    # إذا لم يكن method POST
    messages.error(request, 'طريقة غير مسموحة')
    return redirect('contact_view', contacts_id=contacts_id)

@login_required
def show_contact(request, contact_id=None):
    if contact_id:
        user = get_object_or_404(Contacts, pk=contact_id)
    else:
        user = request.user
    
    context = {
        'user': user,
        'user_full_name': user.get_full_name(),
        'user_role': user.get_role_display(),
        'educational_level': user.get_educational_level_display(),
    }
    return render(request, 'tifinar/auth/show_contact.html', context)

@login_required
def edit_contact(request):
    if request.method == 'POST':
        form = ContactEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if 'clear_image' in request.POST:
                request.user.profile_image.delete()
            form.save()
            messages.success(request, 'تم تحديث البيانات بنجاح')
            return redirect('contact_view', contacts_id=request.user.pk)
    else:
        form = ContactEditForm(instance=request.user)
    
    return render(request, 'tifinar/auth/edit_contact.html', {'form': form})