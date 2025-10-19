from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from tifinar.models import AuthUser, synonym_terms
from django.contrib.auth.decorators import login_required
from tifinar.views.members.friends_views import get_friendship_status
import re


@login_required
def members_index(request):
    members = _get_initial_members_queryset(request.user)
    members = _apply_role_filter(members, request)
    members = _apply_search_filter(members, request)
    members = _add_friendship_status_to_members(members, request.user)
    
    return _render_members_page(request, members)


def _get_initial_members_queryset(user):
    if _is_admin_user(user):
        return AuthUser.objects.all()
    return _get_limited_members_for_regular_user(user)


def _is_admin_user(user):
    return user.role == 'admin'


def _get_limited_members_for_regular_user(user):
    friend_ids = _extract_ids_from_field(user.friends)
    request_ids = _extract_ids_from_field(user.friend_requests)
    all_ids = list(set(friend_ids + request_ids))
    return AuthUser.objects.filter(id__in=all_ids)


def _extract_ids_from_field(field_value):
    if not field_value:
        return []
    return [int(id) for id in field_value.split(',')]


def _apply_role_filter(members, request):
    role = request.GET.get('role')
    if role:
        return members.filter(role__icontains=role)
    return members


def _apply_search_filter(members, request):
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        return members
    
    return _perform_advanced_search(search_term, members)


def _perform_advanced_search(search_term, members):
    synonym_results = advanced_search_with_synonyms(search_term, members)
    if synonym_results.exists():
        return synonym_results
    return smart_search(search_term, members)


def _add_friendship_status_to_members(members, current_user):
    for member in members:
        member.friendship_status = get_friendship_status(current_user, member)
    return members


def _render_members_page(request, members):
    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tifinar/auth/members/index.html', {
        'members': page_obj,
        'search_term': request.GET.get('search', ''),
        'role': request.GET.get('role')
    })


def advanced_search_with_synonyms(search_term, queryset):
    synonyms_data = get_all_synonyms_data()
    relation_term, relation_type, clean_name = extract_relation_and_name(search_term, synonyms_data)
    
    if not _has_valid_relation_data(relation_term, relation_type, clean_name):
        return queryset.none()
    
    return _find_members_using_relation(relation_type, clean_name, synonyms_data, queryset)


def _has_valid_relation_data(relation_term, relation_type, clean_name):
    return relation_term and relation_type and clean_name


def _find_members_using_relation(relation_type, clean_name, synonyms_data, queryset):
    relation_info = synonyms_data.get(relation_type)
    if not relation_info:
        return queryset.none()
    
    main_members = _find_members_by_name(clean_name, queryset)
    if not main_members.exists():
        return queryset.none()
    
    related_names = get_related_names_from_members(main_members, relation_info)
    if not related_names:
        return queryset.none()
    
    return search_related_members(related_names, relation_info, queryset)


def _find_members_by_name(name, queryset):
    return queryset.filter(
        Q(name_in_arabic__icontains=name) |
        Q(first_name__icontains=name) |
        Q(last_name__icontains=name)
    )


def get_all_synonyms_data():
    synonyms_data = {}
    all_entries = synonym_terms.objects.all()
    
    for entry in all_entries:
        synonyms_data[entry.relation_type] = _build_relation_data(entry)
    
    return synonyms_data


def _build_relation_data(entry):
    return {
        'terms': _get_all_relation_terms(entry),
        'contact_field': entry.contact_field,
        'target_gender': entry.target_gender,
        'ignore_terms': _get_ignore_terms(entry)
    }


def _get_all_relation_terms(entry):
    terms = [entry.term.strip()]
    if entry.synonyms:
        terms.extend([syn.strip() for syn in entry.synonyms.split(',') if syn.strip()])
    return terms


def _get_ignore_terms(entry):
    if not entry.ignore_terms:
        return []
    return [term.strip() for term in entry.ignore_terms.split(',')]


def extract_relation_and_name(search_term, synonyms_data):
    term_to_relation = _build_term_to_relation_mapping(synonyms_data)
    all_terms = _get_sorted_search_terms(term_to_relation)
    
    for term in all_terms:
        relation_type = term_to_relation[term]
        if _is_term_in_search_and_not_ignored(term, search_term, synonyms_data[relation_type]):
            clean_name = _extract_and_clean_name(search_term, term, synonyms_data[relation_type])
            if clean_name:
                return term, relation_type, clean_name
    
    return None, None, search_term


def _build_term_to_relation_mapping(synonyms_data):
    mapping = {}
    for relation_type, data in synonyms_data.items():
        for term in data['terms']:
            if term:
                mapping[term] = relation_type
    return mapping


def _get_sorted_search_terms(term_to_relation):
    terms = list(term_to_relation.keys())
    terms.sort(key=len, reverse=True)
    return terms


def _is_term_in_search_and_not_ignored(term, search_term, relation_data):
    if term not in search_term:
        return False
    
    ignore_terms = relation_data['ignore_terms']
    return not any(ignore_term in search_term for ignore_term in ignore_terms if ignore_term)


def _extract_and_clean_name(search_term, relation_term, relation_data):
    name = search_term.replace(relation_term, '').strip()
    return clean_extracted_name(name, relation_data['terms'])


def clean_extracted_name(name, relation_terms):
    if not name:
        return ''
    
    pattern = _build_cleaning_pattern(relation_terms)
    if pattern:
        return re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
    
    return name.strip()


def _build_cleaning_pattern(relation_terms):
    pattern_terms = [re.escape(term) for term in relation_terms if term]
    
    common_terms = ['أخت', 'أخ', 'شقيقة', 'شقيق', 'والد', 'والدة', 'ابن', 'ابنة', 'زوج', 'زوجة']
    pattern_terms.extend([re.escape(term) for term in common_terms])
    
    if not pattern_terms:
        return None
    
    return r'\b(' + '|'.join(pattern_terms) + r')\b'


def get_related_names_from_members(members, relation_info):
    related_names = set()
    contact_field = relation_info['contact_field']
    
    for member in members:
        names_from_member = _extract_names_from_member(member, contact_field, relation_info)
        related_names.update(names_from_member)
    
    return list(related_names)


def _extract_names_from_member(member, contact_field, relation_info):
    if not hasattr(member, contact_field):
        return set()
    
    field_value = getattr(member, contact_field)
    if not field_value:
        return set()
    
    names = re.split(r'[,\n;]+', str(field_value))
    valid_names = set()
    
    for name in names:
        clean_name = name.strip()
        if _is_valid_name(clean_name) and _matches_gender_filter(clean_name, relation_info):
            valid_names.add(clean_name)
    
    return valid_names


def _is_valid_name(name):
    return name and len(name) > 2


def _matches_gender_filter(name, relation_info):
    target_gender = relation_info.get('target_gender')
    if not target_gender or target_gender == 'ALL':
        return True
    
    name_member = _find_member_by_name(name)
    return name_member and name_member.gender == target_gender


def _find_member_by_name(name):
    return AuthUser.objects.filter(
        Q(name_in_arabic__icontains=name) |
        Q(first_name__icontains=name) |
        Q(last_name__icontains=name)
    ).first()


def search_related_members(related_names, relation_info, queryset):
    if not related_names:
        return queryset.none()
    
    results = _find_members_by_names(related_names, queryset)
    return _filter_by_gender_if_needed(results, relation_info.get('target_gender'))


def _find_members_by_names(names, queryset):
    q_objects = Q()
    for name in names:
        q_objects |= Q(name_in_arabic__icontains=name)
        q_objects |= Q(first_name__icontains=name)
        q_objects |= Q(last_name__icontains=name)
    
    return queryset.filter(q_objects).distinct()


def _filter_by_gender_if_needed(queryset, target_gender):
    if target_gender and target_gender != 'ALL':
        return queryset.filter(gender=target_gender)
    return queryset


# الحفاظ على الوظائف الأصلية كما هي (دون تغيير)
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
