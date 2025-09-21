from django.shortcuts import render, redirect
from django.contrib import messages
from tifinar.models import msgs, AuthUser  # استيراد النموذج المخصص
from tifinar.forms import MsgForm

def send_message(request):
    recipient_id = request.GET.get('user_id')
    recipient_user = None
    
    # جلب بيانات المستخدم المرسل إليه إذا كان user_id موجوداً
    if recipient_id:
        try:
            recipient_user = AuthUser.objects.get(id=recipient_id)
        except AuthUser.DoesNotExist:
            messages.error(request, 'المستخدم المطلوب غير موجود')
        except ValueError:
            messages.error(request, 'معرف المستخدم غير صحيح')
    
    if request.method == 'POST':
        form = MsgForm(request.POST)
        if form.is_valid():
            try:
                msg = form.save(commit=False)
                
                if recipient_id:
                    msg.recipient = recipient_id
                
                msg.author_id = msg.author_id or '0'
                msg.recipient = msg.recipient or '1'
                msg.author_img = msg.author_img or ''
                msg.mysubject = msg.mysubject or ''
                msg.title = msg.title or ''
                msg.email = msg.email or ''
                
                msg.save()
                messages.success(request, 'تم إرسال رسالتك بنجاح!')
                return redirect(request.META.get('HTTP_REFERER', '/'))
                
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
        'recipient_user': recipient_user  # تمرير بيانات المستخدم إلى القالب
    })