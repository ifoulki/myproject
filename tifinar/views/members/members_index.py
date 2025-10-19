from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from tifinar.models import AuthUser, synonym_terms
from django.contrib.auth.decorators import login_required
from tifinar.views.members.friends_views import get_friendship_status  # تصحيح المسار
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
        # 1. البحث باستخدام المرادفات أولاً (التحسين الجديد)
        synonym_results = advanced_search_with_synonyms(search_term, members)
        if synonym_results.exists():
            members = synonym_results
        else:
            # 2. البحث الذكي إذا لم توجد نتائج من المرادفات
            members = smart_search(search_term, members)
    
    # إضافة حالة الصداقة لكل عضو
    for member in members:
        member.friendship_status = get_friendship_status(request.user, member)
    
    # التقسيم إلى صفحات
    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tifinar/auth/members/index.html', {
        'members': page_obj,
        'search_term': search_term,
        'role': role
    })

def advanced_search_with_synonyms(search_term, queryset):
    """
    بحث متقدم باستخدام جدول المرادفات - النسخة المطورة
    """
    # الحصول على جميع بيانات المرادفات
    synonyms_data = get_all_synonyms_data()
    
    # استخراج العلاقة والاسم من البحث
    relation_term, relation_type, clean_name = extract_relation_and_name(search_term, synonyms_data)
    
    if relation_term and relation_type and clean_name:
        # الحصول على معلومات العلاقة
        relation_info = synonyms_data.get(relation_type)
        
        if relation_info and clean_name:
            # البحث عن الأعضاء الأساسيين بالاسم
            main_members = queryset.filter(
                Q(name_in_arabic__icontains=clean_name) |
                Q(first_name__icontains=clean_name) |
                Q(last_name__icontains=clean_name)
            )
            
            if main_members.exists():
                # الحصول على الأسماء المرتبطة من حقل العلاقة
                related_names = get_related_names_from_members(main_members, relation_info)
                
                if related_names:
                    # البحث عن الأعضاء المرتبطين
                    return search_related_members(related_names, relation_info, queryset)
    
    # إذا لم توجد نتائج، إرجاع queryset فارغ للانتقال للبحث الذكي
    return queryset.none()

def get_all_synonyms_data():
    """
    الحصول على جميع بيانات المرادفات من قاعدة البيانات
    """
    synonyms_data = {}
    all_entries = synonym_terms.objects.all()
    
    for entry in all_entries:
        # جمع جميع مصطلحات العلاقة
        all_terms = [entry.term.strip()]
        if entry.synonyms:
            all_terms.extend([syn.strip() for syn in entry.synonyms.split(',') if syn.strip()])
        
        # تخزين بيانات العلاقة
        synonyms_data[entry.relation_type] = {
            'terms': all_terms,
            'contact_field': entry.contact_field,
            'target_gender': entry.target_gender,
            'ignore_terms': [term.strip() for term in entry.ignore_terms.split(',')] if entry.ignore_terms else []
        }
    
    return synonyms_data

def extract_relation_and_name(search_term, synonyms_data):
    """
    استخراج العلاقة والاسم من مصطلح البحث
    """
    # جمع جميع المصطلحات من جميع العلاقات
    all_terms = []
    term_to_relation = {}
    
    for relation_type, data in synonyms_data.items():
        for term in data['terms']:
            if term:  # التأكد من أن المصطلح ليس فارغاً
                all_terms.append(term)
                term_to_relation[term] = relation_type
    
    # ترتيب المصطلحات من الأطول إلى الأقصر لتجنب المطالبات الجزئية
    all_terms.sort(key=len, reverse=True)
    
    # البحث عن مصطلح مطابق
    for term in all_terms:
        if term and term in search_term:
            relation_type = term_to_relation[term]
            ignore_terms = synonyms_data[relation_type]['ignore_terms']
            
            # التحقق من عدم وجود كلمات محظورة
            if not any(ignore_term in search_term for ignore_term in ignore_terms if ignore_term):
                # استخراج الاسم وتنظيفه
                name = search_term.replace(term, '').strip()
                clean_name = clean_extracted_name(name, synonyms_data[relation_type]['terms'])
                if clean_name:
                    return term, relation_type, clean_name
    
    return None, None, search_term

def clean_extracted_name(name, relation_terms):
    """
    تنظيف الاسم المستخرج من مصطلحات العلاقات
    """
    if not name:
        return ''
    
    # إنشاء نمط regex من مصطلحات العلاقات
    pattern_terms = []
    for term in relation_terms:
        if term:
            escaped_term = re.escape(term)
            pattern_terms.append(escaped_term)
    
    # إضافة كلمات علاقات شائعة أخرى
    common_terms = ['أخت', 'أخ', 'شقيقة', 'شقيق', 'والد', 'والدة', 'ابن', 'ابنة', 'زوج', 'زوجة']
    pattern_terms.extend([re.escape(term) for term in common_terms])
    
    if pattern_terms:
        pattern = r'\b(' + '|'.join(pattern_terms) + r')\b'
        clean_name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
    else:
        clean_name = name.strip()
    
    return clean_name

def get_related_names_from_members(members, relation_info):
    """
    الحصول على الأسماء المرتبطة من الأعضاء باستخدام معلومات العلاقة
    """
    related_names = set()
    contact_field = relation_info['contact_field']
    target_gender = relation_info['target_gender']
    
    for member in members:
        if hasattr(member, contact_field):
            field_value = getattr(member, contact_field)
            if field_value:
                # تقسيم القيم (دعم تنسيقات متعددة)
                names = re.split(r'[,\n;]+', str(field_value))
                for name in names:
                    clean_name = name.strip()
                    if clean_name and len(clean_name) > 2:  # تجنب الأسماء القصيرة
                        # التحقق من الجنس إذا كان محدداً
                        if target_gender and target_gender != 'ALL':
                            # البحث عن العضو بالاسم للتحقق من الجنس
                            name_member = AuthUser.objects.filter(
                                Q(name_in_arabic__icontains=clean_name) |
                                Q(first_name__icontains=clean_name) |
                                Q(last_name__icontains=clean_name)
                            ).first()
                            
                            if name_member and name_member.gender == target_gender:
                                related_names.add(clean_name)
                        else:
                            related_names.add(clean_name)
    
    return list(related_names)

def search_related_members(related_names, relation_info, queryset):
    """
    البحث عن الأعضاء المرتبطين بالأسماء
    """
    if not related_names:
        return queryset.none()
    
    # بناء استعلام البحث
    q_objects = Q()
    for name in related_names:
        q_objects |= Q(name_in_arabic__icontains=name)
        q_objects |= Q(first_name__icontains=name)
        q_objects |= Q(last_name__icontains=name)
    
    results = queryset.filter(q_objects).distinct()
    
    # تصفية حسب الجنس إذا محدد
    target_gender = relation_info.get('target_gender')
    if target_gender and target_gender != 'ALL':
        results = results.filter(gender=target_gender)
    
    return results

# الحفاظ على جميع الوظائف الأصلية كما هي دون تغيير
def search_with_synonyms(search_term, queryset):
    """
    البحث باستخدام جدول المرادفات - النسخة الأصلية محفوظة
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
    استخراج الاسم من البحث بعد المصطلح - محفوظة كما هي
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
    إيجاد الأعضاء المرتبطين بناءً على المرادف - محفوظة كما هي
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
    بحث ذكي مع ترجيح النتائج - محفوظة كما هي
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

# وظيفة مساعدة للبحث المتقدم (اختياري) - محفوظة كما هي
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