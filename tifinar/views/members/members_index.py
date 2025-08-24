from django.shortcuts import render
from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat, Coalesce
from django.core.paginator import Paginator
from tifinar.models import AuthUser, synonym_terms
from django.contrib.auth.decorators import login_required
import re

@login_required
def members_index(request):
    # البدء بجميع الأعضاء للمسؤولين، أو محدود للعاديين
    if request.user.role == 'admin':
        members = AuthUser.objects.all()
    else:
        # للمستخدمين العاديين: الأصدقاء وطلبات الصداقة فقط
        current_member = request.user
        friend_ids = [int(id) for id in current_member.friends.split(',')] if current_member.friends else []
        request_ids = [int(id) for id in current_member.friend_requests.split(',')] if current_member.friend_requests else []
        all_ids = list(set(friend_ids + request_ids))
        members = AuthUser.objects.filter(id__in=all_ids)
    
    # معالجة تصفية الدور
    role = request.GET.get('role')
    if role:
        members = members.filter(role__icontains=role)

    search_term = request.GET.get('search', '').strip()
    
    if search_term:
        # 1. البحث في المرادفات أولاً
        synonym_results = search_with_synonyms(search_term, members)
        if synonym_results is not None:
            members = synonym_results
        else:
            # 2. البحث الذكي إذا لم توجد مرادفات
            members = smart_search(search_term, members)
    
    # التقسيم إلى صفحات
    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tifinar/auth/members/index.html', {
        'members': page_obj,
        'search_term': search_term,
        'role': role
    })

def search_with_synonyms(search_term, queryset):
    """
    البحث باستخدام جدول المرادفات
    """
    synonym_entries = synonym_terms.objects.all()
    
    for entry in synonym_entries:
        terms_to_check = [entry.term.strip()] 
        if entry.synonyms:
            terms_to_check.extend([s.strip() for s in entry.synonyms.split(',')])
        
        ignore_terms = [i.strip() for i in entry.ignore_terms.split(',')] if entry.ignore_terms else []
        
        # التحقق من وجود أي مصطلح في البحث
        for term in terms_to_check:
            if term and term in search_term:
                # التحقق من عدم وجود كلمات محظورة
                if any(ignore in search_term for ignore in ignore_terms if ignore):
                    continue
                
                # استخراج الاسم بعد المصطلح
                name_part = extract_name_after_term(search_term, term)
                
                if name_part:
                    return find_related_members(entry, name_part, queryset)
    
    return None

def extract_name_after_term(search_term, term):
    """
    استخراج الاسم من البحث بعد المصطلح
    """
    # استخدام regex لأفضل استخراج
    pattern = r'(?:^|\s)' + re.escape(term) + r'\s+([^\s].*?)(?:\s|$)'
    match = re.search(pattern, search_term, re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # إذا لم يعثر، حاول تقسيم بسيط
    parts = search_term.split(term)
    if len(parts) > 1:
        return parts[-1].strip()
    
    return ''

def find_related_members(synonym_entry, name_part, queryset):
    """
    إيجاد الأعضاء المرتبطين بناءً على المرادف
    """
    target_field = synonym_entry.contact_field
    target_gender = synonym_entry.target_gender
    
    if not target_field:
        return None
    
    # البحث عن الأعضاء الذين يتطابق اسمهم مع name_part
    name_matches = queryset.filter(
        Q(name_in_arabic__icontains=name_part) |
        Q(first_name__icontains=name_part) |
        Q(last_name__icontains=name_part)
    )
    
    if not name_matches:
        return queryset.none()
    
    # جمع الأسماء المرتبطة
    related_names = set()
    
    for member in name_matches:
        if hasattr(member, target_field):
            field_value = getattr(member, target_field)
            if field_value:
                # تقسيم القيم (دعم تنسيقات متعددة)
                names = re.split(r'[,\n;]+', str(field_value))
                for name in names:
                    clean_name = name.strip()
                    if clean_name and len(clean_name) > 2:  # تجنب الأسماء القصيرة
                        related_names.add(clean_name)
    
    if not related_names:
        return queryset.none()
    
    # البحث عن الأعضاء المرتبطين
    q_objects = Q()
    for name in related_names:
        q_objects |= Q(name_in_arabic__icontains=name)
        q_objects |= Q(first_name__icontains=name)
        q_objects |= Q(last_name__icontains=name)
    
    results = queryset.filter(q_objects)
    
    # تصفية حسب الجنس إذا محدد
    if target_gender:
        results = results.filter(gender=target_gender)
    
    return results

def smart_search(search_term, queryset):
    """
    بحث ذكي مع ترجيح النتائج
    """
    # تقسيم كلمات البحث
    search_words = re.findall(r'\w+', search_term.lower())
    
    if not search_words:
        return queryset.none()
    
    # تعريف أوزان الحقول
    field_weights = {
        'name_in_arabic': 17,  # الأعلى أولوية
        'last_name': 16,
        'first_name': 15,
        'friends': 14,
        'siblings': 13,
        'parents': 12,
        'spouse': 12,
        'children': 12,
        'cousins': 12,
        'adresse': 11,
        'tel': 11,
        'email': 11,
        'Ideologie': 10,
        'societe': 9,
        'gender': 8,
        'the_type': 7,
        'keywords': 7,
        'maternal_relatives': 6,
        'paternal_relatives': 6,
        'ville_d_origine': 5,
        'social_media': 5,
        'educational_level': 4,
        'Commentaire': 3,
        'grandparents': 2,
        'date_de_naissance': 2,
        'path': 1,
    }
    
    # إنشاء استعلام ديناميكي
    q_objects = Q()
    for field, weight in field_weights.items():
        for word in search_words:
            if len(word) > 2:  # تجاهل الكلمات القصيرة
                q_objects |= Q(**{f'{field}__icontains': word})
    
    # البحث الأولي
    results = queryset.filter(q_objects)
    
    if not results:
        return queryset.none()
    
    # ترجيح النتائج
    weighted_results = []
    for member in results:
        score = 0
        
        for field, weight in field_weights.items():
            field_value = getattr(member, field, '')
            if field_value:
                field_value_lower = str(field_value).lower()
                for word in search_words:
                    if word in field_value_lower:
                        # زيادة الوزن إذا كانت المطابقة كاملة
                        if word == field_value_lower:
                            score += weight * 2
                        else:
                            score += weight
        
        # زيادة الوزن إذا كان الاسم الكامل مطابق
        full_name = f"{member.first_name or ''} {member.last_name or ''}".strip().lower()
        if search_term.lower() in full_name:
            score += 15
        
        if score > 0:
            weighted_results.append((member, score))
    
    # ترتيب حسب الوزن
    weighted_results.sort(key=lambda x: x[1], reverse=True)
    
    return [result[0] for result in weighted_results]

# وظيفة مساعدة للبحث المتقدم (اختياري)
def advanced_search_filters(queryset, request):
    """
    تطبيق فلاتر البحث المتقدم
    """
    filters = Q()
    
    # فلترة حسب الجنس
    gender = request.GET.get('gender')
    if gender:
        filters &= Q(gender=gender)
    
    # فلترة حسب المدينة
    city = request.GET.get('city')
    if city:
        filters &= Q(ville_d_origine__icontains=city)
    
    # فلترة حسب المستوى التعليمي
    education = request.GET.get('education')
    if education:
        filters &= Q(educational_level=education)
    
    # فلترة حسب الحالة الاجتماعية
    marital_status = request.GET.get('marital_status')
    if marital_status:
        filters &= Q(etat_social=marital_status)
    
    return queryset.filter(filters)