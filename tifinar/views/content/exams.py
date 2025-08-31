from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from tifinar.models import exams, Examitems, Results
from difflib import SequenceMatcher
from django.http import HttpResponse

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
            'folder': 'exams',
            'image': exam.myimage,
            'exam_id': exam.exam_id,
        }
        return render(request, 'tifinar/showExam.html', context)
    except exams.DoesNotExist:
        # بدلاً من redirect، نعرض خطأ في الصفحة نفسها
        return render(request, 'tifinar/showExam.html', {
            'error': 'الاختبار غير موجود',
            'error_message': f'لا يوجد اختبار بالرابط: {exam_slug}'
        })
        
def store_answer(request):
    print("=" * 80)
    print("🔥🔥🔥 store_answer CALLED! 🔥🔥🔥")
    print(f"🔥 Method: {request.method}")
    print(f"🔥 Path: {request.path}")
    print(f"🔥 POST data: {dict(request.POST)}")
    print("=" * 80)

    if request.method != 'POST':
        return HttpResponse("خطأ: يجب أن يكون الطلب POST", status=400)
    
    print("🐛 This is a POST request!")
    print("=" * 50)
    print("DEBUG: store_answer function STARTED")
    
    try:
        exam_id = request.POST.get('exam_id')
        exam_title = request.POST.get('exam_title')
        print(f"DEBUG: exam_id = {exam_id}, exam_title = {exam_title}")
        
        if not exam_id:
            return HttpResponse("خطأ: معرف الاختبار مفقود", status=400)
        
        # البحث عن الاختبار
        try:
            exam = exams.objects.get(exam_id=exam_id)
            print(f"DEBUG: Found exam: {exam.title}")
        except exams.DoesNotExist:
            return HttpResponse("خطأ: الاختبار غير موجود", status=404)
        
        # الحصول على الأسئلة
        questions = Examitems.objects.filter(exam_number=exam_id).order_by('qsts_id')
        print(f"DEBUG: Found {questions.count()} questions")
        
        if questions.count() == 0:
            return HttpResponse("خطأ: لا توجد أسئلة لهذا الاختبار", status=404)
        
        total_marks = 0
        user_answers = []
        
        # معالجة كل سؤال
        for i, question in enumerate(questions, 1):
            user_answer = request.POST.get(f'answer{i}')
            user_answer_list = request.POST.getlist(f'answer{i}[]')
            
            print(f"DEBUG: Q{i} - answer={user_answer}, answer_list={user_answer_list}")
            
            # تحديد نص الإجابة للعرض
            if question.the_type == 'radio' or question.the_type == 'text' or question.the_type == 'textarea':
                display_answer = user_answer if user_answer else '(لم تكتب أي إجابة لهذا السؤال)'
            elif question.the_type == 'checkbox':
                if user_answer_list and any(user_answer_list):
                    display_answer = ', '.join([ans for ans in user_answer_list if ans])
                else:
                    display_answer = '(لم تكتب أي إجابة لهذا السؤال)'
            else:
                display_answer = user_answer or str(user_answer_list) or '(لم تكتب أي إجابة لهذا السؤال)'
            
            # تقييم الإجابة
            is_correct, mark_obtained = evaluate_answer(question, user_answer, user_answer_list)
            total_marks += mark_obtained
            
            user_answers.append({
                'qst_1st_line': question.qst_1st_line,
                'user_answer': display_answer,  # استخدام النص المعدل
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'mark_obtained': mark_obtained,
                'mark': question.mark,
                'qsts_id': question.qsts_id,
                'dir': question.dir,
                'if_choising_correct': question.if_choising_correct,  
                'if_its_wrong_answer': question.if_its_wrong_answer,
            })
        
        print(f"DEBUG: Total marks = {total_marks}")
        
        # حساب العلامة الكلية
        max_marks = Examitems.objects.filter(exam_number=exam_id).aggregate(
            total=Sum('mark')
        )['total'] or 0
        
        # حفظ النتيجة
        user_name = "مستخدم مجهول"
        if request.user.is_authenticated:
            user_name = f"{request.user.first_name} {request.user.last_name or ''}"
        else:
            user_name = request.POST.get('user_name', 'مستخدم مجهول')
        
        # حفظ في قاعدة البيانات
        Results.objects.create(
            name=user_name,
            exam_title=exam_title,
            exam_link=request.build_absolute_uri(),
            result=total_marks,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        
        # عرض النتائج
        context = {
            'total_marks': total_marks,
            'max_marks': max_marks,
            'user_answers': user_answers,
            'exam_title': exam_title,
            'user_name': user_name,
        }
        
        print("DEBUG: Rendering result page...")
        return render(request, 'tifinar/result.html', context)
        
    except Exception as e:
        print(f"DEBUG: EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return HttpResponse(f"خطأ غير متوقع: {str(e)}", status=500)

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