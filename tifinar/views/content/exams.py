from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from tifinar.models import exams, Examitems, Results
from difflib import SequenceMatcher
import datetime

def exam_view(request, exam_slug):
    try:
        exam = exams.objects.get(slug=exam_slug)
        questions = Examitems.objects.filter(exam_number=exam.exam_id).order_by('qsts_id')
        
        context = {
            'exam': exam,
            'questions': questions,
            'title': exam.title,
            'Mydescription': exam.mydescription,
            'folder': 'exams',  # افتراضي، يمكن تعديله حسب هيكل مجلداتك
            'image': exam.myimage,
            'exam_id': exam.exam_id,
        }
        return render(request, 'tifinar/showExam.html', context)
    except exams.DoesNotExist:
        messages.error(request, "الاختبار غير موجود")
        return redirect('welcome')

def store_answer(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        exam_title = request.POST.get('exam_title')
        
        try:
            exam = exams.objects.get(exam_id=exam_id)
            questions = Examitems.objects.filter(exam_number=exam_id).order_by('qsts_id')
            
            total_marks = 0
            user_answers = []
            
            for i, question in enumerate(questions, 1):
                user_answer = request.POST.get(f'answer{i}')
                user_answer_list = request.POST.getlist(f'answer{i}[]')
                
                # معالجة الإجابة بناءً على نوع السؤال
                is_correct, mark_obtained = evaluate_answer(question, user_answer, user_answer_list)
                
                total_marks += mark_obtained
                
                user_answers.append({
                    'qst_1st_line': question.qst_1st_line,
                    'qsts': question.qsts,
                    'user_answer': user_answer or user_answer_list or 'لم تتم الإجابة عليه',
                    'correct_answer': question.correct_answer,
                    'mark': question.mark,
                    'mark_obtained': mark_obtained,
                    'dir': question.dir,
                    'the_type': question.the_type,
                    'qsts_id': question.qsts_id,
                    'is_correct': is_correct,
                    'if_choising_correct': question.if_choising_correct,
                })
            
            # حساب العلامة الكلية
            max_marks = Examitems.objects.filter(exam_number=exam_id).aggregate(
                total=Sum('mark')
            )['total'] or 0
            
            # حفظ النتيجة
            if request.user.is_authenticated:
                user_name = f"{request.user.first_name} {request.user.last_name}"
            else:
                user_name = request.POST.get('user_name', 'مستخدم مجهول')
            
            Results.objects.create(
                name=user_name,
                exam_title=exam_title,
                exam_link=request.build_absolute_uri(),
                result=total_marks,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            
            # عرض صفحة النتائج
            context = {
                'total_marks': total_marks,
                'max_marks': max_marks,
                'user_answers': user_answers,
                'exam_title': exam_title,
                'dir': questions[0].dir if questions else 'rtl'
            }
            
            return render(request, 'tifinar/result.html', context)
            
        except exams.DoesNotExist:
            messages.error(request, "الاختبار غير موجود")
            return redirect('welcome')
    
    return redirect('welcome')

def evaluate_answer(question, user_answer, user_answer_list):
    mark_obtained = 0
    is_correct = False
    
    try:
        question_mark = float(question.mark) if question.mark else 0
    except ValueError:
        question_mark = 0
    
    if question.the_type == 'radio':
        is_correct = user_answer == question.correct_answer
        if is_correct:
            mark_obtained = question_mark
    
    elif question.the_type == 'checkbox':
        # معالجة الإجابات المتعددة
        correct_answers = []
        for choice in [question.choice1, question.choice2, question.choice3, question.correct_answer]:
            if choice and 'true' in choice.lower():
                correct_answers.append(choice)
        
        user_answers_clean = [ans for ans in user_answer_list if ans]
        is_correct = set(user_answers_clean) == set(correct_answers) and len(user_answers_clean) == len(correct_answers)
        
        if is_correct:
            mark_obtained = question_mark
    
    elif question.the_type in ['text', 'textarea']:
        if user_answer and question.correct_answer:
            # حساب نسبة التشابه بين الإجابات
            similarity = SequenceMatcher(
                None, 
                user_answer.lower(), 
                question.correct_answer.lower()
            ).ratio()
            
            threshold = 0.8 if question.the_type == 'text' else 0.5
            if similarity >= threshold:
                is_correct = True
                mark_obtained = question_mark
    
    return is_correct, mark_obtained