from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from tifinar.models import AuthUser
from django.contrib.auth.decorators import login_required

@login_required
@transaction.atomic
def send_friend_request(request, user_id):
    """إرسال طلب صداقة"""
    if request.method == 'POST':
        try:
            target_user = get_object_or_404(AuthUser, id=user_id)
            current_user = request.user
            
            # التحقق من عدم إرسال طلب إلى النفس
            if target_user.id == current_user.id:
                messages.error(request, "لا يمكن إرسال طلب صداقة إلى نفسك")
                return redirect('users')
            
            # التحقق من وجود صداقة مسبقة
            current_friends = get_friends_list(current_user)
            if target_user.id in current_friends:
                messages.warning(request, "أنتم أصدقاء بالفعل")
                return redirect('users')
            
            # التحقق من وجود طلب مسبق
            target_requests = get_friend_requests_list(target_user)
            if current_user.id in target_requests:
                messages.warning(request, "تم إرسال طلب الصداقة مسبقاً")
                return redirect('users')
            
            # إضافة طلب الصداقة
            add_friend_request(target_user, current_user.id)
            
            messages.success(request, f"تم إرسال طلب صداقة إلى {target_user.first_name}")
            return redirect('users')
        
        except Exception as e:
            print(f"ERROR in send_friend_request: {e}")
            messages.error(request, "حدث خطأ أثناء إرسال طلب الصداقة")
            return redirect('users')
    
    # إذا لم يكن POST، ارجع للصفحة
    return redirect('users')

@login_required
@transaction.atomic
def cancel_friend_request(request, user_id):
    """إلغاء طلب صداقة"""
    if request.method == 'POST':
        try:
            target_user = get_object_or_404(AuthUser, id=user_id)
            current_user = request.user
            
            # إزالة طلب الصداقة
            remove_friend_request(target_user, current_user.id)
            
            messages.info(request, "تم إلغاء طلب الصداقة")
        
        except Exception as e:
            messages.error(request, "حدث خطأ أثناء إلغاء طلب الصداقة")
        
        return redirect('users')

@login_required
@transaction.atomic
def accept_friend_request(request, user_id):
    """قبول طلب صداقة"""
    if request.method == 'POST':
        try:
            sender_user = get_object_or_404(AuthUser, id=user_id)
            current_user = request.user
            
            # التحقق من وجود الطلب
            current_requests = get_friend_requests_list(current_user)
            if sender_user.id not in current_requests:
                messages.error(request, "طلب الصداقة غير موجود")
                return redirect('users')
            
            # إزالة من طلبات الصداقة وإضافة إلى الأصدقاء
            remove_friend_request(current_user, sender_user.id)
            add_friend(current_user, sender_user.id)
            add_friend(sender_user, current_user.id)
            
            messages.success(request, f"تم قبول طلب صداقة من {sender_user.first_name} {sender_user.last_name}")
        
        except Exception as e:
            messages.error(request, "حدث خطأ أثناء قبول طلب الصداقة")
        
        return redirect('users')

@login_required
@transaction.atomic
def reject_friend_request(request, user_id):
    """رفض طلب صداقة"""
    if request.method == 'POST':
        try:
            sender_user = get_object_or_404(AuthUser, id=user_id)
            current_user = request.user
            
            # إزالة طلب الصداقة فقط
            remove_friend_request(current_user, sender_user.id)
            
            messages.info(request, "تم رفض طلب الصداقة")
        
        except Exception as e:
            messages.error(request, "حدث خطأ أثناء رفض طلب الصداقة")
        
        return redirect('users')

@login_required
@transaction.atomic
def remove_friend(request, user_id):
    """إزالة صديق"""
    if request.method == 'POST':
        try:
            friend_user = get_object_or_404(AuthUser, id=user_id)
            current_user = request.user
            
            # إزالة من قائمة الأصدقاء لكلا الطرفين
            remove_friend_from_list(current_user, friend_user.id)
            remove_friend_from_list(friend_user, current_user.id)
            
            messages.info(request, f"تم إزالة {friend_user.first_name} {friend_user.last_name} من الأصدقاء")
        
        except Exception as e:
            messages.error(request, "حدث خطأ أثناء إزالة الصديق")
        
        return redirect('users')

# الدوال المساعدة
def get_friends_list(user):
    """الحصول على قائمة أصدقاء المستخدم"""
    if user.friends and user.friends.strip():
        return [int(id.strip()) for id in user.friends.split(',') if id.strip()]
    return []

def get_friend_requests_list(user):
    """الحصول على قائمة طلبات الصداقة"""
    if user.friend_requests and user.friend_requests.strip():
        return [int(id.strip()) for id in user.friend_requests.split(',') if id.strip()]
    return []
        
def add_friend_request(user, friend_id):
    """إضافة طلب صداقة"""
    requests_list = get_friend_requests_list(user)
    if friend_id not in requests_list:
        requests_list.append(friend_id)
        user.friend_requests = ','.join(map(str, requests_list))
        user.save(update_fields=['friend_requests'])  # تحديث الحقل فقط

def remove_friend_request(user, friend_id):
    """إزالة طلب صداقة"""
    requests_list = get_friend_requests_list(user)
    if friend_id in requests_list:
        requests_list.remove(friend_id)
        user.friend_requests = ','.join(map(str, requests_list)) if requests_list else ''
        user.save(update_fields=['friend_requests'])

def add_friend(user, friend_id):
    """إضافة صديق"""
    friends_list = get_friends_list(user)
    if friend_id not in friends_list:
        friends_list.append(friend_id)
        user.friends = ','.join(map(str, friends_list))
        user.save(update_fields=['friends'])

def remove_friend_from_list(user, friend_id):
    """إزالة صديق من القائمة"""
    friends_list = get_friends_list(user)
    if friend_id in friends_list:
        friends_list.remove(friend_id)
        user.friends = ','.join(map(str, friends_list)) if friends_list else ''
        user.save(update_fields=['friends'])

def get_friendship_status(current_user, target_user):
    """الحصول على حالة الصداقة بين مستخدمين"""
    current_friends = get_friends_list(current_user)
    current_requests = get_friend_requests_list(current_user)
    target_requests = get_friend_requests_list(target_user)
    
    if target_user.id in current_friends:
        return 'friends'
    elif current_user.id in target_requests:
        return 'request_sent'
    elif target_user.id in current_requests:
        return 'request_received'
    else:
        return 'not_friends'
    
def get_friendship_status(current_user, target_user):
    """الحصول على حالة الصداقة بين مستخدمين"""
    try:
        # تحقق من أن البيانات موجودة
        if not hasattr(current_user, 'friends') or not hasattr(target_user, 'friend_requests'):
            return 'not_friends'
        
        current_friends = get_friends_list(current_user)
        current_requests = get_friend_requests_list(current_user)
        target_requests = get_friend_requests_list(target_user)
        
        print(f"DEBUG: User {current_user.id} - Friends: {current_friends}, Requests: {current_requests}")
        print(f"DEBUG: Target {target_user.id} - Requests: {target_requests}")
        
        if target_user.id in current_friends:
            return 'friends'
        elif current_user.id in target_requests:
            return 'request_sent'
        elif target_user.id in current_requests:
            return 'request_received'
        else:
            return 'not_friends'
    except Exception as e:
        print(f"ERROR in get_friendship_status: {e}")
        return 'not_friends'