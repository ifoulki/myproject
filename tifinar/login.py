from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("welcome")  # استبدل بـ الصفحة التي تريد
        else:
            messages.error(request, "البريد الإلكتروني أو كلمة المرور غير صحيحة")
    return render(request, "tifinar/login.html")
