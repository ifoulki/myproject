from django.shortcuts import render, redirect
from django.contrib.auth import login
from tifinar.forms import AuthUserCreationForm

def custom_logup(request):
    if request.method == 'POST':
        form = AuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        return render(request, "tifinar/logup.html")
