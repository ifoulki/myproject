from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from tifinar.models import AuthUser
import random
import os 
@login_required
def member_profile_view(request, user_id):
    """
    عرض الملف الشخصي الكامل للمستخدم مع كل التفاصيل
    """
    member = get_object_or_404(AuthUser, id=user_id)
    
    # معالجة الصور
    images = []
    if member.path:
        images = [img.strip() for img in member.path.split(',') if img.strip()]
        random.shuffle(images)  # خلط الصور لعرض عشوائي
    
    # معالجة وسائل التواصل الاجتماعي
    social_media = {}
    if member.social_media:
        for item in member.social_media.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                social_media[key.strip()] = value.strip()
    
    # معالجة العلاقات العائلية
    family_data = {}
    if hasattr(member, 'parents'):
        family_data['parents'] = {
            'parents': member.parents.split(',') if member.parents else [],
            'children': member.children.split(',') if member.children else [],
            'siblings': member.siblings.split(',') if member.siblings else [],
            'spouse': member.spouse.split(',') if member.spouse else [],
            'grandparents': member.grandparents.split(',') if member.grandparents else [],
            'maternal_relatives': member.maternal_relatives.split(',') if member.maternal_relatives else [],
            'paternal_relatives': member.paternal_relatives.split(',') if member.paternal_relatives else [],
            'friends': member.friends.split(',') if member.friends else [],
            'cousins': member.cousins.split(',') if member.cousins else [],
        }

    # التحقق من الصلاحيات
    is_owner = request.user.id == member.id
    is_admin = request.user.role == AuthUser.role.admin
    
    context = {
        'member': member,
        'images': images,
        'social_media': social_media,
        'family_data': family_data,
        'is_owner': is_owner,
        'is_admin': is_admin,
        'languages': member.language.split(',') if member.language else [],
    }
    
    return render(request, 'tifinar/auth/members/show_member.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def edit_member_profile(request, user_id):
    """
    تعديل الملف الشخصي للمستخدم بدون استخدام Forms
    """
    member = get_object_or_404(AuthUser, id=user_id)
    
    if request.method == 'POST':
        try:
            # تحديث الحقول الأساسية
            member.first_name = request.POST.get('first_name', member.first_name)
            member.last_name = request.POST.get('last_name', member.last_name)
            member.email = request.POST.get('email', member.email)
            member.tel = request.POST.get('tel', member.tel)
            
            # تحديث الحقول الاختيارية
            member.gender = request.POST.get('gender', member.gender)
            member.role = request.POST.get('role', member.role)
            member.societe = request.POST.get('societe', member.societe)
            member.adresse = request.POST.get('adresse', member.adresse)
            member.ville_d_origine = request.POST.get('ville_d_origine', member.ville_d_origine)
            member.Etat_Social = request.POST.get('Etat_Social', member.Etat_Social)
            member.date_de_naissance = request.POST.get('date_de_naissance', member.date_de_naissance)
            member.Ideologie = request.POST.get('Ideologie', member.Ideologie)
            member.Commentaire = request.POST.get('Commentaire', member.Commentaire)
            member.social_media = request.POST.get('social_media', member.social_media)
            
            # معالجة الصور المرفوعة
            
            # معالجة الصور المرفوعة (محسنة)
            if 'new_images' in request.FILES:
                new_images = request.FILES.getlist('new_images')
                image_names = []
                
                for image in new_images:
                    # حفظ الملف فعلياً (يجب تكوين إعدادات MEDIA أولاً)
                    file_name = f"{member.id}_{image.name}"
                    file_path = os.path.join(settings.MEDIA_ROOT, 'profiles', file_name)
                    
                    with open(file_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    
                    image_names.append(file_name)
                
                if member.path:
                    member.path += ',' + ','.join(image_names)
                else:
                    member.path = ','.join(image_names)
            
            member.save()
            messages.success(request, "تم تحديث الملف الشخصي بنجاح")
            return redirect('edit_member_profile', user_id=member.id)
            
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء التحديث: {str(e)}")
    
    # عرض صفحة التعديل
    return render(request, 'tifinar/auth/members/edit_profile.html', {
        'member': member,
        'role_choices': AuthUser.role.choices,
        'gender_choices': AuthUser.Gender.choices,
    })

@login_required
@require_http_methods(["POST"])
def delete_member_profile(request, user_id):
    """
    حذف الملف الشخصي (للمسؤولين فقط)
    """
    member = get_object_or_404(AuthUser, id=user_id)
    try:
        full_name = member.get_full_name()
        member.delete()
        messages.success(request, f"تم حذف المستخدم {full_name} بنجاح")
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء الحذف: {str(e)}")
    
    return redirect('users_list')

@login_required
def manage_member_relations(request, user_id):
    """
    إدارة علاقات المستخدم (أصدقاء، عائلة، إلخ)
    """
    member = get_object_or_404(AuthUser, id=user_id)
    
    if request.method == 'POST':
        relation_type = request.POST.get('relation_type')
        target_id = request.POST.get('target_id')
        action = request.POST.get('action')
        
        try:
            target_member = AuthUser.objects.get(id=target_id)
            
            if relation_type == 'friend':
                friends = member.friends.split(',') if member.friends else []
                if action == 'add' and str(target_id) not in friends:
                    friends.append(str(target_id))
                    member.friends = ','.join(friends)
                elif action == 'remove' and str(target_id) in friends:
                    friends.remove(str(target_id))
                    member.friends = ','.join(friends)
            
            elif relation_type == 'family':
                # يمكنك إضافة المزيد من أنواع العلاقات هنا
                pass
                
            member.save()
            messages.success(request, "تم تحديث العلاقة بنجاح")
        except AuthUser.DoesNotExist:
            messages.error(request, "المستخدم المطلوب غير موجود")
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")
    
    return redirect('edit_member_profile', user_id=member.id)

@login_required
def update_profile_image(request, user_id):
    """
    تحديث الصورة الرئيسية للملف الشخصي
    """
    member = get_object_or_404(AuthUser, id=user_id)
    
    if request.method == 'POST' and 'profile_image' in request.FILES:
        try:
            new_image = request.FILES['profile_image']
            if member.path:
                member.path = f"{new_image.name},{member.path}"
            else:
                member.path = new_image.name
            member.save()
            messages.success(request, "تم تحديث صورة الملف الشخصي بنجاح")
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء تحديث الصورة: {str(e)}")
    
    return redirect('edit_member_profile', user_id=member.id)