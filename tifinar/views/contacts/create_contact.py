from django.shortcuts import render, redirect
from django.contrib import messages
from tifinar.myForms.contact.ContactForm import ContactForm
import os
from django.conf import settings

def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # معالجة الصور
            image_paths = []
            prenom = form.cleaned_data.get('Prenom', '')
            nom = form.cleaned_data.get('Nom', '')
            
            title_slug = f"{prenom.lower()}_{nom.lower()}".replace(' ', '_')
            
            # معالجة الملفات المتعددة - التصحيح هنا
            files = form.cleaned_data.get('path', [])
            if not isinstance(files, list):
                files = [files] if files else []
            
            for index, image in enumerate(files):
                if image:  # التأكد من وجود ملف
                    # الحصول على امتداد الملف
                    file_extension = image.name.split('.')[-1]
                    image_name = f"{title_slug}_{index + 1}.{file_extension}"
                    
                    # حفظ الملف
                    save_path = os.path.join(settings.MEDIA_ROOT, 'images/contacts', image_name)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    
                    with open(save_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    
                    image_paths.append(image_name)
            
            # حفظ مسارات الصور في البيانات
            contact = form.save(commit=False)
            if image_paths:
                contact.path = ','.join(image_paths)
            
            # هنا يتم الحفظ في نموذج Contacts
            contact.save()
            
            messages.success(request, 'تم تسجيل العضو بنجاح!')
            return redirect('contact_view', contacts_id=contact.pk)
    else:
        form = ContactForm(initial={'Author': request.user.id})
    
    return render(request, 'tifinar/auth/contacts/create_contact.html', {'form': form})