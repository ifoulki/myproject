from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from tifinar.models import Examitems, exams
from tifinar.myForms.exam_items.exam_items_form import ExamItemForm



def exam_items_list(request):
    exam_number = request.GET.get('exam_number')
    
    items = Examitems.objects.all()
    if exam_number:
        items = items.filter(exam_number=exam_number)
    
    exam = exams.objects.all()
    
    context = {
        'items': items,
        'exams': exam,
    }
    return render(request, 'tifinar/auth/examsQsts/index.html', context)


def exam_items_create(request):
    if request.method == 'POST':
        form = ExamItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة السؤال بنجاح')
            return redirect('exam_items_list')
    else:
        form = ExamItemForm()
    
    return render(request, 'tifinar/auth/examsQstss/index.html', {'form': form})

def exam_items_edit(request, item_id):
    item = get_object_or_404(Examitems, premary_id=item_id)
    
    if request.method == 'POST':
        form = ExamItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل السؤال بنجاح')
            return redirect('exam_items_list')
    else:
        form = ExamItemForm(instance=item)
    
    return render(request, 'tifinar/auth/examsQstss/index.html', {'form': form})

def exam_items_delete(request, item_id):
    item = get_object_or_404(Examitems, premary_id=item_id)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'تم حذف السؤال بنجاح')
    
    return redirect('exam_items_list')