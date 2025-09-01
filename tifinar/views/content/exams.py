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

def clean_choice_text(choice):
    """تنظيف نص الخيار من البادئات correct:/wrong:"""
    if not choice:
        return choice
    
    choice_str = str(choice).strip()
    
    # إذا كانت البادئة موجودة، نزيلها
    if choice_str.lower().startswith('correct:'):
        return choice_str.split(':', 1)[1].strip()
    elif choice_str.lower().startswith('wrong:'):
        return choice_str.split(':', 1)[1].strip()
    elif choice_str.lower().startswith('correct='):
        return choice_str.split('=', 1)[1].strip()
    elif choice_str.lower().startswith('wrong='):
        return choice_str.split('=', 1)[1].strip()
    
    return choice_str

def get_correct_answers(question):
    """استخراج جميع الإجابات الصحيحة من سؤال من نوع checkbox"""
    correct_answers = []
    
    if question.the_type != 'checkbox':
        return [clean_choice_text(question.correct_answer)] if question.correct_answer else []
    
    # جمع جميع الخيارات المتاحة
    choices_data = [
        question.choice1, 
        question.choice2, 
        question.choice3, 
        question.correct_answer
    ]
    
    for choice in choices_data:
        if choice:
            choice_str = str(choice).lower()
            if 'correct:' in choice_str or 'correct=' in choice_str:
                cleaned_choice = clean_choice_text(choice)
                correct_answers.append(cleaned_choice)
    
    return correct_answers


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
        title = request.POST.get('title')
        print(f"DEBUG: exam_id = {exam_id}, exam_title = {title}")
        
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
            if question.the_type == 'radio':
                display_answer = clean_choice_text(user_answer) if user_answer else 0
            
            elif question.the_type == 'checkbox':
                if user_answer_list:
                    # تنظيف جميع الإجابات من البادئات
                    cleaned_answers = []
                    for ans in user_answer_list:
                        if ans and ans.strip():  # تجاهل الإجابات الفارغة
                            cleaned = clean_choice_text(ans)
                            cleaned_answers.append(cleaned)
                    
                    if cleaned_answers:
                        display_answer = '، '.join(cleaned_answers)
                    else:
                        display_answer = 0
                else:
                    display_answer = 0
            
            elif question.the_type in ['text', 'textarea']:
                display_answer = clean_choice_text(user_answer) if user_answer else 0
            
            else:
                display_answer = clean_choice_text(user_answer) if user_answer else 0
            
            # الحصول على الإجابات الصحيحة (للعرض والتقييم)
            if question.the_type == 'checkbox':
                correct_display = '، '.join(get_correct_answers(question))
            else:
                correct_display = clean_choice_text(question.correct_answer) if question.correct_answer else ''
            
            # تقييم الإجابة
            is_correct, mark_obtained = evaluate_answer(question, user_answer, user_answer_list)
            total_marks += mark_obtained
            
            user_answers.append({
                'qst_1st_line': question.qst_1st_line,
                'user_answer': display_answer,
                'correct_answer': correct_display,
                'is_correct': is_correct,
                'mark_obtained': mark_obtained,
                'mark': question.mark,
                'qsts_id': question.qsts_id,
                'dir': question.dir,
                'if_choising_correct': clean_choice_text(question.if_choising_correct) if question.if_choising_correct else None,
                'if_its_wrong_answer': clean_choice_text(question.if_its_wrong_answer) if question.if_its_wrong_answer else None,
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
            exam_title=title,
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
            'title': title,
            'user_name': user_name,
            'dir': questions[0].dir if questions else 'rtl'
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
        # تنظيف الإجابات للمقارنة
        cleaned_user_answer = clean_choice_text(user_answer) if user_answer else ""
        cleaned_correct_answer = clean_choice_text(question.correct_answer) if question.correct_answer else ""
        
        is_correct = cleaned_user_answer == cleaned_correct_answer
        if is_correct:
            mark_obtained = question_mark
    
    elif question.the_type == 'checkbox':
        # الحصول على جميع الإجابات الصحيحة والخاطئة
        correct_choices = []
        wrong_choices = []
        
        # جمع جميع الخيارات المتاحة
        choices_data = [
            question.choice1, 
            question.choice2, 
            question.choice3, 
            question.correct_answer
        ]
        
        for choice in choices_data:
            if choice:
                cleaned_choice = clean_choice_text(choice)
                choice_str = str(choice).lower()
                
                if 'correct:' in choice_str or 'correct=' in choice_str:
                    correct_choices.append(cleaned_choice)
                elif 'wrong:' in choice_str or 'wrong=' in choice_str:
                    wrong_choices.append(cleaned_choice)
                else:
                    # إذا لم تكن هناك بادئة، نعتبرها خيارًا صحيحًا
                    correct_choices.append(cleaned_choice)
        
        # تنظيف إجابات المستخدم
        user_answers_clean = []
        if user_answer_list:
            user_answers_clean = [clean_choice_text(ans) for ans in user_answer_list if ans]
        elif user_answer:
            user_answers_clean = [clean_choice_text(user_answer)]
        
        # التحقق من أن المستخدم اختار جميع الإجابات الصحيحة ولم يختار أي إجابة خاطئة
        user_has_all_correct = all(choice in user_answers_clean for choice in correct_choices)
        user_has_no_wrong = not any(choice in user_answers_clean for choice in wrong_choices)
        
        is_correct = user_has_all_correct and user_has_no_wrong
        
        if is_correct:
            mark_obtained = question_mark
    
    elif question.the_type in ['text', 'textarea']:
        if user_answer and question.correct_answer:
            # تنظيف الإجابات قبل المقارنة
            cleaned_user_answer = clean_choice_text(user_answer).lower().strip()
            cleaned_correct_answer = clean_choice_text(question.correct_answer).lower().strip()
            
            similarity = SequenceMatcher(
                None, 
                cleaned_user_answer, 
                cleaned_correct_answer
            ).ratio()
            
            threshold = 0.8 if question.the_type == 'text' else 0.5
            if similarity >= threshold:
                is_correct = True
                mark_obtained = question_mark
    
    return is_correct, mark_obtained