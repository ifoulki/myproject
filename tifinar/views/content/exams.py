from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from difflib import SequenceMatcher
from django.http import HttpResponse

import datetime

from django.db.models import Count, Sum
from tifinar.models import exams, Examitems, Results, ArticleReaction, comments, AuthUser
from django.utils.timezone import now
def encode_arabic_path(path):
    """
    ترميز المسارات العربية لتجنب مشاكل Unicode
    """
    try:
        if isinstance(path, str):
            parts = path.split('/')
            encoded_parts = []
            for part in parts:
                if any(ord(c) > 127 for c in part):
                    encoded_parts.append(urllib.parse.quote(part))
                else:
                    encoded_parts.append(part)
            return '/'.join(encoded_parts)
        return path
    except Exception as e:
        print(f"Error encoding path {path}: {e}")
        return path

def get_user_profile_image(email):
    """
    الحصول على صورة المستخدم من خلال البريد الإلكتروني
    """
    try:
        user = AuthUser.objects.filter(email=email).first()
        if not user:
            return None
            
        # البحث في الحقول المباشرة في نموذج AuthUser
        if hasattr(user, 'images') and user.images:
            images_list = [img.strip() for img in user.images.split(',') if img.strip()]
            if images_list:
                first_image = images_list[0]
                
                # استخدام المسار من حقل path إذا كان موجوداً
                if hasattr(user, 'path') and user.path:
                    path_list = [p.strip() for p in user.path.split(',') if p.strip()]
                    for image_path in path_list:
                        if first_image in image_path:
                            return image_path
                
                # بناء المسار افتراضياً
                default_path = f"images/users/{user.id}/{first_image}"
                
                # التحقق من وجود الملف فعلياً
                static_path = os.path.join(settings.STATIC_ROOT, default_path)
                media_path = os.path.join(settings.MEDIA_ROOT, default_path)
                
                if os.path.exists(static_path):
                    return f"/static/{default_path}"
                elif os.path.exists(media_path):
                    return f"/media/{default_path}"
        
        return None
        
    except Exception as e:
        print(f"Error in get_user_profile_image: {e}")
        return None

def get_user_display_name(email):
    """
    الحصول على اسم العرض للمستخدم
    """
    try:
        user = AuthUser.objects.filter(email=email).first()
        if user:
            full_name = f"{user.first_name} {user.last_name}".strip()
            return full_name if full_name else user.username
    except Exception:
        pass
    
    return None

def get_user_identifier(request):
    """الحصول على معرف المستخدم"""
    if request.user.is_authenticated:
        return request.user.username
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

def exam_view(request, exam_slug):
    try:
        exam = exams.objects.get(slug=exam_slug)
        questions = Examitems.objects.filter(exam_number=exam.exam_id).order_by('qsts_id')
        
        # الحصول على معرف المستخدم
        user_identifier = get_user_identifier(request)
        
        # معالجة طلبات POST (التفاعلات والتعليقات)
        if request.method == 'POST':
            # معالجة التفاعلات
            if 'reaction_type' in request.POST:
                reaction_type = request.POST.get('reaction_type')
                if reaction_type in ['love', 'like', 'dislike', 'sad', 'funny', 'angry']:
                    existing_reaction = ArticleReaction.objects.filter(
                        ip_or_name=user_identifier,
                        page_title=exam.title
                    ).first()
                    
                    if existing_reaction:
                        if existing_reaction.reaction_type == reaction_type:
                            existing_reaction.delete()
                            messages.success(request, 'تم إلغاء تفاعلك بنجاح')
                        else:
                            existing_reaction.reaction_type = reaction_type
                            existing_reaction.liked_at = now()
                            existing_reaction.save()
                            messages.success(request, 'تم تحديث تفاعلك بنجاح')
                    else:
                        ArticleReaction.objects.create(
                            ip_or_name=user_identifier,
                            page_title=exam.title,
                            device_type=request.META.get('HTTP_USER_AGENT', 'Unknown')[:100],
                            reaction_type=reaction_type,
                            liked_at=now(),
                            created_at=now()
                        )
                        messages.success(request, 'شكراً على تفاعلك!')
            
            # معالجة التعليقات
            elif 'cmt_subject' in request.POST:
                cmt_subject = request.POST.get('cmt_subject', '').strip()
                author_name = request.POST.get('author_name', '').strip()
                author_email = request.POST.get('author_email', '').strip()
                
                if cmt_subject and author_name:
                    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                        visibility_status = 'public'
                    else:
                        visibility_status = 'under_review'
                    
                    try:
                        comment = comments.objects.create(
                            page_title=exam.title,
                            author_name=author_name,
                            cmt_subject=cmt_subject,
                            author_email=author_email if author_email else None,
                            visibility_status=visibility_status,
                            created_at=now(),
                            updated_at=now()
                        )
                        
                        messages.success(request, 
                            'شكراً على تعليقك! ' + 
                            ('سيظهر بعد المراجعة.' if visibility_status == 'under_review' else 'تم نشر تعليقك.')
                        )
                    except Exception as e:
                        messages.error(request, f'حدث خطأ أثناء إضافة التعليق: {str(e)}')
                else:
                    messages.error(request, 'يرجى ملء جميع الحقول المطلوبة')
        
        # الحصول على تفاعل المستخدم الحالي
        user_reaction = None
        if user_identifier:
            try:
                user_reaction = ArticleReaction.objects.filter(
                    ip_or_name=user_identifier,
                    page_title=exam.title
                ).first()
            except:
                pass
        
        # حساب عدد التفاعلات
        try:
            reactions_count = ArticleReaction.objects.filter(page_title=exam.title).values(
                'reaction_type'
            ).annotate(count=Count('id'))
            reactions_dict = {item['reaction_type']: item['count'] for item in reactions_count}
        except:
            reactions_dict = {}
        
        # الحصول على التعليقات وإضافة معلومات الصور
        try:
            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                exam_comments = comments.objects.filter(page_title=exam.title).order_by('-created_at')
            else:
                exam_comments = comments.objects.filter(
                    page_title=exam.title, 
                    visibility_status='public'
                ).order_by('-created_at')
            
            comments_with_images = []
            user_auth_data = []
            
            for comment in exam_comments:
                profile_image = None
                display_name = comment.author_name
                
                if comment.author_email:
                    user = AuthUser.objects.filter(email=comment.author_email).first()
                    if user:
                        # جمع بيانات auth_user للعرض في القالب
                        user_auth_data.append({
                            'email': user.email,
                            'username': user.username,
                            'user_id': user.id,
                            'images': getattr(user, 'images', '❌ فارغ'),
                            'path': getattr(user, 'path', '❌ فارغ')
                        })
                        
                        # الحصول على الصورة
                        profile_image = get_user_profile_image(comment.author_email)
                        
                        # الحصول على اسم العرض
                        user_display_name = get_user_display_name(comment.author_email)
                        if user_display_name:
                            display_name = user_display_name
                
                comments_with_images.append({
                    'comment': comment,
                    'profile_image': profile_image,
                    'display_name': display_name
                })
                
        except Exception as e:
            comments_with_images = []
            user_auth_data = []
            print(f"Error fetching comments: {e}")
        
        # إعداد السياق مع إضافة متغيرات التعليقات والتفاعلات
        context = {
            'exam': exam,
            'questions': questions,
            'title': exam.title,
            'Mydescription': exam.mydescription,
            'folder': 'exams',
            'image': exam.myimage,
            'exam_id': exam.exam_id,
            # إضافة متغيرات التعليقات والتفاعلات
            'reactions': reactions_dict,
            'reaction_type': user_reaction.reaction_type if user_reaction else None,
            'comments': exam_comments,
            'comments_with_images': comments_with_images,
            'comments_count': exam_comments.count() if 'exam_comments' in locals() else 0,
            'user_auth_data': user_auth_data,
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