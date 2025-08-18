from django.shortcuts import render, get_object_or_404, redirect
from tifinar.models import AuthUser
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tifinar.forms import UserEditForm

@login_required
def show_user(request, user_id=None):
    if user_id:
        user = get_object_or_404(AuthUser, pk=user_id)
    else:
        user = request.user
    
    context = {
        'user': user,
        'user_full_name': user.get_full_name(),
        'user_role': user.get_role_display(),
        'educational_level': user.get_educational_level_display(),
    }
    return render(request, 'tifinar/auth/show_user.html', context)

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if 'clear_image' in request.POST:
                request.user.profile_image.delete()
            form.save()
            messages.success(request, 'تم تحديث البيانات بنجاح')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'tifinar/auth/edit_user.html', {'form': form})