from django.shortcuts import render, redirect
from django.contrib import messages  # استيراد نظام الرسائل من Django
from tifinar.models import msgs  # استيراد نموذج الرسائل
from tifinar.forms import MsgForm  # استيراد نموذج الرسائل

def send_message(request):
    if request.method == 'POST':
        form = MsgForm(request.POST)
        if form.is_valid():
            try:
                msg = form.save(commit=False)
                
                # تعيين القيم الافتراضية إذا كانت فارغة
                msg.author_id = msg.author_id or '0'
                msg.recipient = msg.recipient or '1'
                msg.author_img = msg.author_img or ''
                msg.mysubject = msg.mysubject or ''
                msg.title = msg.title or ''
                msg.email = msg.email or ''
                
                msg.save()
                
                # استخدام نظام رسائل Django بدلاً من msgs.success
                messages.success(request, 'تم إرسال رسالتك بنجاح!')
                return redirect(request.META.get('HTTP_REFERER', '/'))
                
            except Exception as e:
                # تسجيل الخطأ في السجلات
                print(f"Error saving message: {str(e)}")
                messages.error(request, 'حدث خطأ أثناء حفظ الرسالة. الرجاء المحاولة لاحقاً.')
        else:
            # عرض أخطاء التحقق من الصحة
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    else:
        form = MsgForm()
    
    return render(request, 'tifinar/send_message.html', {'form': form})