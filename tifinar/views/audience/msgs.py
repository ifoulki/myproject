from django.shortcuts import render, redirect
from django.contrib import messages
from tifinar.models import msgs, AuthUser  # استيراد النموذج المخصص
from tifinar.myForms.msgs.msgs_forms import *

def send_message(request):
    recipient_id = request.GET.get('user_id')
    recipient_user = None
    conversation_messages = []
    message_count = 0
    
    # جلب بيانات المستخدم المرسل إليه إذا كان user_id موجوداً
    if recipient_id:
        try:
            recipient_user = AuthUser.objects.get(id=recipient_id)
            
            # جلب جميع الرسائل المتبادلة بين المستخدمين
            if request.user.is_authenticated:
                # تحويل recipient_id إلى string للمقارنة الصحيحة
                recipient_id_str = str(recipient_id)
                current_user_id_str = str(request.user.id)
                
                # الرسائل المرسلة من المستخدم الحالي إلى المستلم
                sent_messages = msgs.objects.filter(
                    author_id=request.user.id, 
                    recipient=recipient_id_str
                )
                
                # الرسائل المستلمة من المستلم إلى المستخدم الحالي
                received_messages = msgs.objects.filter(
                    author_id=recipient_id, 
                    recipient=current_user_id_str
                )
                
                print(f"Sent messages count: {sent_messages.count()}")
                print(f"Received messages count: {received_messages.count()}")
                
                # دمج الرسائل وترتيبها حسب التاريخ
                conversation_messages = list(sent_messages) + list(received_messages)
                conversation_messages.sort(key=lambda x: x.created_at)
                
                message_count = len(conversation_messages)
                print(f"Total messages: {message_count}")
                
        except AuthUser.DoesNotExist:
            messages.error(request, 'المستخدم المطلوب غير موجود')
        except ValueError:
            messages.error(request, 'معرف المستخدم غير صحيح')
        except Exception as e:
            print(f"Error: {str(e)}")
            messages.error(request, f'حدث خطأ: {str(e)}')
    
    if request.method == 'POST':
        form = MsgForm(request.POST)
        if form.is_valid():
            try:
                msg = form.save(commit=False)
                
                if recipient_id:
                    msg.recipient = recipient_id
                
                # تعيين القيم الافتراضية
                if request.user.is_authenticated:
                    msg.author_id = request.user.id
                    msg.author = f"{request.user.first_name} {request.user.last_name}"
                    msg.email = request.user.email
                else:
                    msg.author_id = 0  # للمستخدمين غير المسجلين
                
                msg.author_img = msg.author_img or ''
                msg.mysubject = msg.mysubject or ''
                msg.title = msg.title or 'standard'
                msg.email = msg.email or ''
                
                msg.save()
                messages.success(request, 'تم إرسال رسالتك بنجاح!')
                return redirect(f'{request.path}?user_id={recipient_id}')
                
            except Exception as e:
                print(f"Error saving message: {str(e)}")
                messages.error(request, 'حدث خطأ أثناء حفظ الرسالة.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    else:
        form = MsgForm(initial={'recipient': recipient_id} if recipient_id else {})
    
    return render(request, 'tifinar/send_message.html', {
        'form': form,
        'recipient_id': recipient_id,
        'recipient_user': recipient_user,
        'conversation_messages': conversation_messages,
        'message_count': message_count
    })