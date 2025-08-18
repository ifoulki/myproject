from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from tifinar.models import AuthUser
import random

@login_required
def user_profile_view(request, user_id):
    """
    عرض الملف الشخصي الكامل للمستخدم مع كل التفاصيل
    """
    user = get_object_or_404(AuthUser, id=user_id)
    
    # معالجة الصور
    images = []
    if user.path:
        images = [img.strip() for img in user.path.split(',') if img.strip()]
        random.shuffle(images)  # خلط الصور لعرض عشوائي
    
    # معالجة وسائل التواصل الاجتماعي
    social_media = {}
    if user.social_media:
        for item in user.social_media.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                social_media[key.strip()] = value.strip()
    
    # معالجة العلاقات العائلية
    family_data = {
        'parents': user.parents.split(',') if user.parents else [],
        'children': user.children.split(',') if user.children else [],
        'siblings': user.siblings.split(',') if user.siblings else [],
        'spouse': user.spouse.split(',') if user.spouse else [],
        'grandparents': user.grandparents.split(',') if user.grandparents else [],
        'maternal_relatives': user.maternal_relatives.split(',') if user.maternal_relatives else [],
        'paternal_relatives': user.paternal_relatives.split(',') if user.paternal_relatives else [],
        'friends': user.friends.split(',') if user.friends else [],
        'cousins': user.cousin.split(',') if user.cousin else [],
    }

    # التحقق من الصلاحيات
    is_owner = request.user.id == user.id
    is_admin = request.user.role == AuthUser.Role.ADMIN
    
    context = {
        'user': user,
        'images': images,
        'social_media': social_media,
        'family_data': family_data,
        'is_owner': is_owner,
        'is_admin': is_admin,
        'languages': user.language.split(',') if user.language else [],
    }
    
    return render(request, 'tifinar/auth/users/show_user.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def edit_user_profile(request, user_id):
    """
    تعديل الملف الشخصي للمستخدم بدون استخدام Forms
    """
    user = get_object_or_404(AuthUser, id=user_id)
    
    if not (request.user.id == user.id or request.user.role == AuthUser.Role.ADMIN):
        messages.error(request, "ليس لديك صلاحية لتعديل هذا الملف الشخصي")
        return redirect('user_profile', user_id=user.id)
    
    if request.method == 'POST':
        try:
            # تحديث الحقول الأساسية
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.phone = request.POST.get('phone', user.phone)
            
            # تحديث الحقول الاختيارية
            user.gender = request.POST.get('gender', user.gender)
            user.role = request.POST.get('role', user.role)
            user.societe = request.POST.get('societe', user.societe)
            user.address = request.POST.get('address', user.address)
            user.origin_city = request.POST.get('origin_city', user.origin_city)
            user.social_status = request.POST.get('social_status', user.social_status)
            user.birth_date = request.POST.get('birth_date', user.birth_date)
            user.ideology = request.POST.get('ideology', user.ideology)
            user.comment = request.POST.get('comment', user.comment)
            user.social_media = request.POST.get('social_media', user.social_media)
            
            # معالجة الصور المرفوعة
            if 'new_images' in request.FILES:
                new_images = request.FILES.getlist('new_images')
                image_paths = [img.name for img in new_images]
                if user.path:
                    user.path += ',' + ','.join(image_paths)
                else:
                    user.path = ','.join(image_paths)
            
            user.save()
            messages.success(request, "تم تحديث الملف الشخصي بنجاح")
            return redirect('user_profile', user_id=user.id)
            
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء التحديث: {str(e)}")
    
    # عرض صفحة التعديل
    return render(request, 'tifinar/auth/users/edit_profile.html', {
        'user': user,
        'role_choices': AuthUser.Role.choices,
        'gender_choices': AuthUser.Gender.choices,
        'social_status_choices': AuthUser.EtatSocial.choices,
    })

@login_required
@require_http_methods(["POST"])
def delete_user_profile(request, user_id):
    """
    حذف الملف الشخصي (للمسؤولين فقط)
    """
    if request.user.role != AuthUser.Role.ADMIN:
        messages.error(request, "ليس لديك صلاحية لحذف المستخدمين")
        return redirect('home')
    
    user = get_object_or_404(AuthUser, id=user_id)
    try:
        full_name = user.get_full_name()
        user.delete()
        messages.success(request, f"تم حذف المستخدم {full_name} بنجاح")
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء الحذف: {str(e)}")
    
    return redirect('users_list')

@login_required
def manage_user_relations(request, user_id):
    """
    إدارة علاقات المستخدم (أصدقاء، عائلة، إلخ)
    """
    user = get_object_or_404(AuthUser, id=user_id)
    
    if request.method == 'POST':
        relation_type = request.POST.get('relation_type')
        target_id = request.POST.get('target_id')
        action = request.POST.get('action')
        
        try:
            target_user = AuthUser.objects.get(id=target_id)
            
            if relation_type == 'friend':
                friends = user.friends.split(',') if user.friends else []
                if action == 'add' and str(target_id) not in friends:
                    friends.append(str(target_id))
                    user.friends = ','.join(friends)
                elif action == 'remove' and str(target_id) in friends:
                    friends.remove(str(target_id))
                    user.friends = ','.join(friends)
            
            elif relation_type == 'family':
                # يمكنك إضافة المزيد من أنواع العلاقات هنا
                pass
                
            user.save()
            messages.success(request, "تم تحديث العلاقة بنجاح")
        except AuthUser.DoesNotExist:
            messages.error(request, "المستخدم المطلوب غير موجود")
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")
    
    return redirect('user_profile', user_id=user.id)

@login_required
def update_profile_image(request, user_id):
    """
    تحديث الصورة الرئيسية للملف الشخصي
    """
    user = get_object_or_404(AuthUser, id=user_id)
    
    if not (request.user.id == user.id or request.user.role == AuthUser.Role.ADMIN):
        messages.error(request, "ليس لديك صلاحية لتعديل هذا الملف الشخصي")
        return redirect('user_profile', user_id=user.id)
    
    if request.method == 'POST' and 'profile_image' in request.FILES:
        try:
            new_image = request.FILES['profile_image']
            if user.path:
                user.path = f"{new_image.name},{user.path}"
            else:
                user.path = new_image.name
            user.save()
            messages.success(request, "تم تحديث صورة الملف الشخصي بنجاح")
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء تحديث الصورة: {str(e)}")
    
    return redirect('user_profile', user_id=user.id)