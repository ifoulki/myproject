from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from tifinar.models import Contacts
import random
from django.http import JsonResponse

@login_required
def contact_view(request, contacts_id):
    """
    عرض الملف الشخصي الكامل للمستخدم مع كل التفاصيل
    """
    contact = get_object_or_404(Contacts, contacts_id=contacts_id)
    
    # معالجة الصور
    images = []
    if contact.path:
        images = [img.strip() for img in contact.path.split(',') if img.strip()]
        random.shuffle(images)  # خلط الصور لعرض عشوائي
    
    # معالجة وسائل التواصل الاجتماعي
    social_media = {}
    if contact.social_media:
        for item in contact.social_media.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                social_media[key.strip()] = value.strip()
    
    # معالجة العلاقات العائلية
    family_data = {
        'parents': contact.parents.split(',') if contact.parents else [],
        'children': contact.children.split(',') if contact.children else [],
        'siblings': contact.siblings.split(',') if contact.siblings else [],
        'spouse': contact.spouse.split(',') if contact.spouse else [],
        'grandparents': contact.grandparents.split(',') if contact.grandparents else [],
        'maternal_relatives': contact.maternal_relatives.split(',') if contact.maternal_relatives else [],
        'paternal_relatives': contact.paternal_relatives.split(',') if contact.paternal_relatives else [],
        'friends': contact.friends.split(',') if contact.friends else [],
        'cousins': contact.cousins.split(',') if contact.cousins else [],
    }

    # التحقق من الصلاحيات
    is_owner = request.user.id == contact.contacts_id
    
    context = {
        'contact': contact,
        'images': images,
        'social_media': social_media,
        'family_data': family_data,
        'is_owner': is_owner,
    }
    
    return render(request, 'tifinar/auth/contacts/show_contact.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def edit_contact(request, contacts_id):
    """
    تعديل الملف الشخصي للمستخدم بدون استخدام Forms
    """
    contact = get_object_or_404(Contacts, contacts_id=contacts_id)
    
    if not (request.user.id == contact.contacts_id or request.user.role == "admin"):
        messages.error(request, "ليس لديك صلاحية لتعديل هذا الملف الشخصي")
        return redirect('contact_view', contacts_id=contact.contacts_id)
    
    if request.method == 'POST':
        try:
            # تحديث الحقول الأساسية
            contact.prenom = request.POST.get('prenom', contact.prenom)
            contact.nom = request.POST.get('last_name', contact.nom)
            contact.name_in_arabic = request.POST.get('name_in_arabic', contact.name_in_arabic)
            contact.email = request.POST.get('email', contact.email)
            contact.tel = request.POST.get('phone', contact.tel)
            
            # تحديث الحقول الاختيارية
            contact.gender = request.POST.get('gender', contact.gender)
            contact.societe = request.POST.get('societe', contact.societe)
            contact.adresse = request.POST.get('adresse', contact.adresse)
            contact.ville_d_origine = request.POST.get('ville_d_origine', contact.ville_d_origine)
            contact.Etat_Social = request.POST.get('Etat_Social', contact.Etat_Social)
            contact.date_de_naissance = request.POST.get('date_de_naissance', contact.date_de_naissance)
            contact.ideologie = request.POST.get('ideologie', contact.ideologie)
            contact.commentaire = request.POST.get('commentaire', contact.commentaire)
            contact.social_media = request.POST.get('social_media', contact.social_media)
            
            # معالجة الصور المرفوعة
            if 'new_images' in request.FILES:
                new_images = request.FILES.getlist('new_images')
                image_paths = [img.name for img in new_images]
                if contact.path:
                    contact.path += ',' + ','.join(image_paths)
                else:
                    contact.path = ','.join(image_paths)
            
            contact.save()
            messages.success(request, "تم تحديث الملف الشخصي بنجاح")
            return redirect('contact_view', contacts_id=contact.contacts_id)
            
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء التحديث: {str(e)}")
    
    # عرض صفحة التعديل
    return render(request, 'tifinar/auth/contacts/edit_contact.html', {
        'contact': contact,
        'gender_choices': Contacts.gender,
        'social_status_choices': Contacts.Etat_Social,
    })

@login_required
@require_http_methods(["POST"])

@login_required
def delete_contact(request, contacts_id):
    contact = get_object_or_404(Contacts, contacts_id=contacts_id)
    current_user_id = str(request.user.id)
    
    try:
        if request.user.is_superuser:
            # Superadmin - حذف كامل من قاعدة البيانات
            contact_name = f"{contact.prenom} {contact.nom}"
            contact.delete()
            messages.success(request, f'تم حذف الجهة "{contact_name}" بشكل نهائي من قاعدة البيانات')
            
        else:
            # مستخدم عادي - إزالة ID المستخدم من عمود Author فقط
            if contact.author:
                author_ids = [id.strip() for id in str(contact.author).split(',') if id.strip()]
                
                if current_user_id in author_ids:
                    # إزالة ID المستخدم من القائمة
                    author_ids.remove(current_user_id)
                    
                    if author_ids:
                        # تحديث العمود بالقائمة الجديدة
                        contact.author = ','.join(author_ids)
                    else:
                        # إذا لم يتبقى أي authors، يمكن حذف الجهة أو تركها
                        contact.author = ''
                    
                    contact.save()
                    messages.success(request, f'تم إزالة صلاحيتك عن الجهة "{contact.prenom} {contact.nom}"')
                else:
                    messages.error(request, 'ليس لديك صلاحية لهذه الجهة')
            else:
                messages.error(request, 'هذه الجهة لا تملك معلومات authors')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'تمت العملية بنجاح'})
            
        return redirect('contacts')
        
    except Exception as e:
        error_message = f'حدث خطأ أثناء المعالجة: {str(e)}'
        messages.error(request, error_message)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': error_message})
            
        return redirect('contacts')

@login_required
def manage_contact_relations(request, contacts_id):
    """
    إدارة علاقات المستخدم (أصدقاء، عائلة، إلخ)
    """
    contact = get_object_or_404(Contacts, contacts_id=contacts_id)
    
    if request.method == 'POST':
        relation_type = request.POST.get('relation_type')
        target_id = request.POST.get('target_id')
        action = request.POST.get('action')
        
        try:
            target_contact = Contacts.objects.get(id=target_id)
            
            if relation_type == 'friend':
                friends = contact.friends.split(',') if contact.friends else []
                if action == 'add' and str(target_id) not in friends:
                    friends.append(str(target_id))
                    contact.friends = ','.join(friends)
                elif action == 'remove' and str(target_id) in friends:
                    friends.remove(str(target_id))
                    contact.friends = ','.join(friends)
            
            elif relation_type == 'family':
                # يمكنك إضافة المزيد من أنواع العلاقات هنا
                pass
                
            contact.save()
            messages.success(request, "تم تحديث العلاقة بنجاح")
        except Contacts.DoesNotExist:
            messages.error(request, "المستخدم المطلوب غير موجود")
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")
    
    return redirect('contact_view', contacts_id=contact.contacts_id)

@login_required
def update_contact_image(request, contacts_id):
    """
    تحديث الصورة الرئيسية للملف الشخصي
    """
    contact = get_object_or_404(Contacts, contacts_id=contacts_id)
    
    if not (request.user.contacts_id == contact.contacts_id or request.user.role == "admin"):
        messages.error(request, "ليس لديك صلاحية لتعديل هذا الملف الشخصي")
        return redirect('contact_view', contacts_id=contact.contacts_id)
    
    if request.method == 'POST' and 'profile_image' in request.FILES:
        try:
            new_image = request.FILES['profile_image']
            if contact.path:
                contact.path = f"{new_image.name},{contact.path}"
            else:
                contact.path = new_image.name
            contact.save()
            messages.success(request, "تم تحديث صورة الملف الشخصي بنجاح")
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء تحديث الصورة: {str(e)}")
    
    return redirect('contact_view', contacts_id=contact.contacts_id)