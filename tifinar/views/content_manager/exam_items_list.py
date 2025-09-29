from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from tifinar.models import Examitems, exams
from tifinar.myForms.exam_items.exam_items_form import ExamItemForm
from django.db.models import Max
from django.http import JsonResponse

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
    # الحصول على آخر exam (الأكبر exam_id)
    last_exam = exams.objects.order_by('-exam_id').first()
    max_exam_id = last_exam.exam_id if last_exam else 1
    
    # حساب next_qsts_id للاختبار الأخير - استخدم exam_number بدلاً من exam_id
    max_qsts_id = Examitems.objects.filter(exam_number=max_exam_id).aggregate(
        max_id=Max('qsts_id')
    )['max_id']
    next_qsts_id = (max_qsts_id or 0) + 1
    
    if request.method == 'POST':
        form = ExamItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                exam_item = form.save(commit=False)
                
                if exam_item.the_type in ['radio', 'checkbox']:
                    exam_item.choices = {
                        'choice1': {
                            'text': form.cleaned_data.get('choice1', ''),
                            'correct': form.cleaned_data.get('choice1_correct') == 'true'
                        },
                        'choice2': {
                            'text': form.cleaned_data.get('choice2', ''),
                            'correct': form.cleaned_data.get('choice2_correct') == 'true'
                        },
                        'choice3': {
                            'text': form.cleaned_data.get('choice3', ''),
                            'correct': form.cleaned_data.get('choice3_correct') == 'true'
                        }
                    }
                
                exam_item.save()
                messages.success(request, 'تم إضافة السؤال بنجاح')
                return redirect('exam_items_list')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء حفظ السؤال: {str(e)}')
    else:
        # استخدم exam_number بدلاً من exam_id في initial
        form = ExamItemForm(initial={'exam_number': max_exam_id})
    
    context = {
        'form': form,
        'next_qsts_id': next_qsts_id,
        'max_exam_id': max_exam_id,
    }
    return render(request, 'tifinar/auth/examsQsts/exam_items_create.html', context)

def exam_items_edit(request, item_id):
    item = get_object_or_404(Examitems, premary_id=item_id)
    
    if request.method == 'POST':
        form = ExamItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            try:
                exam_item = form.save(commit=False)
                
                # معالجة الخيارات إذا كان السؤال من نوع اختيار
                if exam_item.the_type in ['radio', 'checkbox']:
                    # حفظ الخيارات مباشرة في الحقول الموجودة في المودل
                    exam_item.choice1 = form.cleaned_data.get('choice1', '')
                    exam_item.choice2 = form.cleaned_data.get('choice2', '')
                    exam_item.choice3 = form.cleaned_data.get('choice3', '')
                
                exam_item.save()
                messages.success(request, 'تم تعديل السؤال بنجاح')
                return redirect('exam_items_list')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تعديل السؤال: {str(e)}')
    else:
        # تحميل البيانات الحالية مباشرة من الحقول في المودل
        initial_data = {
            'choice1': item.choice1 if item.choice1 else '',
            'choice2': item.choice2 if item.choice2 else '',
            'choice3': item.choice3 if item.choice3 else '',
        }
        
        form = ExamItemForm(instance=item, initial=initial_data)
    
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'tifinar/auth/examsQsts/exam_items_edit.html', context)

def exam_items_delete(request, item_id):
    item = get_object_or_404(Examitems, premary_id=item_id)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'تم حذف السؤال بنجاح')
    
    return redirect('exam_items_list')

def get_next_qsts_id(request):
    exam_id = request.GET.get('exam_id')
    
    try:
        if exam_id and exam_id.isdigit():
            # استخدم exam_number بدلاً من exam_id
            max_qsts_id = Examitems.objects.filter(exam_number=int(exam_id)).aggregate(
                max_id=Max('qsts_id')
            )['max_id']
            next_qsts_id = (max_qsts_id or 0) + 1

        else:
            last_exam = exams.objects.order_by('-exam_id').first()
            if last_exam:
                # استخدم exam_number بدلاً من exam_id
                max_qsts_id = Examitems.objects.filter(exam_number=last_exam.exam_id).aggregate(
                    max_id=Max('qsts_id')
                )['max_id']
                next_qsts_id = (max_qsts_id or 0) + 1
            else:
                next_qsts_id = 1
        
        return JsonResponse({
            'success': True,
            'next_qsts_id': next_qsts_id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })