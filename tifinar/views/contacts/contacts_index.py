from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tifinar.models import Contacts, synonym_terms
import re


class ContactSearchService:
    """خدمة متخصصة في البحث الديناميكي باستخدام جدول المرادفات"""
    
    FIELD_PRIORITIES = {
        'name_in_arabic': 17, 'nom': 16, 'prenom': 15, 'friends': 14,
        'siblings': 13, 'parents': 12, 'spouse': 12, 'children': 12,
        'cousins': 12, 'adresse': 11, 'tel': 11, 'email': 11,
        'ideologie': 10, 'societe': 9, 'gender': 8, 'the_type': 7,
        'keywords': 7, 'maternal_relatives': 6, 'paternal_relatives': 6,
        'ville_d_origine': 5, 'social_media': 5, 'educational_level': 4,
        'commentaire': 3, 'grandparents': 2, 'date_de_naissance': 2,
        'path': 1, 'author': 0,
    }
    
    SEARCHABLE_COLUMNS = list(FIELD_PRIORITIES.keys())
    
    @classmethod
    def get_synonyms_data(cls):
        """الحصول على بيانات المرادفات من قاعدة البيانات"""
        synonyms_data = {}
        all_entries = synonym_terms.objects.all()
        
        for entry in all_entries:
            synonyms_data[entry.relation_type] = cls._build_synonym_entry_data(entry)
        
        return synonyms_data
    
    @classmethod
    def _build_synonym_entry_data(cls, entry):
        """بناء بيانات مدخل المرادف"""
        return {
            'terms': cls._extract_all_terms(entry),
            'contact_field': entry.contact_field,
            'target_gender': entry.target_gender,
            'ignore_terms': cls._extract_ignore_terms(entry)
        }
    
    @classmethod
    def _extract_all_terms(cls, entry):
        """استخراج جميع مصطلحات العلاقة"""
        terms = [entry.term.strip()]
        if entry.synonyms:
            terms.extend([syn.strip() for syn in entry.synonyms.split(',') if syn.strip()])
        return terms
    
    @classmethod
    def _extract_ignore_terms(cls, entry):
        """استخراج مصطلحات التجاهل"""
        if not entry.ignore_terms:
            return []
        return [term.strip() for term in entry.ignore_terms.split(',')]
    
    @classmethod
    def extract_search_components(cls, search_term):
        """استخراج مكونات البحث: العلاقة والاسم"""
        synonyms_data = cls.get_synonyms_data()
        term_to_relation = cls._build_term_relation_mapping(synonyms_data)
        
        for term in cls._get_sorted_search_terms(term_to_relation):
            if term and term in search_term:
                relation_type = term_to_relation[term]
                if cls._is_search_valid(search_term, synonyms_data[relation_type]):
                    clean_name = cls._extract_clean_name(search_term, term, synonyms_data[relation_type])
                    if clean_name:
                        return term, relation_type, clean_name
        
        return None, None, search_term
    
    @classmethod
    def _build_term_relation_mapping(cls, synonyms_data):
        """بناء mapping بين المصطلحات وأنواع العلاقات"""
        mapping = {}
        for relation_type, data in synonyms_data.items():
            for term in data['terms']:
                mapping[term] = relation_type
        return mapping
    
    @classmethod
    def _get_sorted_search_terms(cls, term_to_relation):
        """الحصول على مصطلحات البحث مرتبة من الأطول إلى الأقصر"""
        terms = list(term_to_relation.keys())
        terms.sort(key=len, reverse=True)
        return terms
    
    @classmethod
    def _is_search_valid(cls, search_term, relation_data):
        """التحقق من صحة البحث (عدم وجود مصطلحات محظورة)"""
        ignore_terms = relation_data['ignore_terms']
        return not any(ignore_term in search_term for ignore_term in ignore_terms if ignore_term)
    
    @classmethod
    def _extract_clean_name(cls, search_term, relation_term, relation_data):
        """استخراج وتنظيف الاسم من مصطلح البحث"""
        name = search_term.replace(relation_term, '').strip()
        return cls._clean_name_from_relations(name, relation_data['terms'])
    
    @classmethod
    def _clean_name_from_relations(cls, name, relation_terms):
        """تنظيف الاسم من مصطلحات العلاقات"""
        if not name:
            return ''
        
        pattern = cls._build_cleaning_pattern(relation_terms)
        if pattern:
            return re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
        
        return name.strip()
    
    @classmethod
    def _build_cleaning_pattern(cls, relation_terms):
        """بناء نمط التنظيف من مصطلحات العلاقات"""
        pattern_terms = [re.escape(term) for term in relation_terms if term]
        
        common_terms = ['أخت', 'أخ', 'شقيقة', 'شقيق', 'والد', 'والدة', 'ابن', 'ابنة', 'زوج', 'زوجة']
        pattern_terms.extend([re.escape(term) for term in common_terms])
        
        if not pattern_terms:
            return None
        
        return r'\b(' + '|'.join(pattern_terms) + r')\b'
    
    @classmethod
    def get_relation_info(cls, relation_type):
        """الحصول على معلومات العلاقة المحددة"""
        try:
            entry = synonym_terms.objects.get(relation_type=relation_type)
            return cls._build_synonym_entry_data(entry)
        except synonym_terms.DoesNotExist:
            return None


class ContactQueryService:
    """خدمة متخصصة في استعلامات جهات الاتصال"""
    
    @classmethod
    def perform_relation_based_search(cls, relation_type, name):
        """إجراء بحث بناءً على العلاقة"""
        relation_info = ContactSearchService.get_relation_info(relation_type)
        if not relation_info:
            return Contacts.objects.none()
        
        main_contacts = cls._find_contacts_by_name(name)
        if not main_contacts.exists():
            return Contacts.objects.none()
        
        related_names = cls._get_related_names(main_contacts, relation_info)
        if not related_names:
            return Contacts.objects.none()
        
        return cls._find_contacts_by_names(related_names)
    
    @classmethod
    def _find_contacts_by_name(cls, name):
        """البحث عن جهات الاتصال بالاسم"""
        return Contacts.objects.filter(
            Q(name_in_arabic__icontains=name) |
            Q(nom__icontains=name) |
            Q(prenom__icontains=name)
        )
    
    @classmethod
    def _get_related_names(cls, contacts, relation_info):
        """الحصول على الأسماء المرتبطة"""
        related_names = set()
        contact_field = relation_info['contact_field']
        target_gender = relation_info['target_gender']
        
        for contact in contacts:
            names_from_contact = cls._extract_names_from_contact(contact, contact_field, target_gender)
            related_names.update(names_from_contact)
        
        return list(related_names)
    
    @classmethod
    def _extract_names_from_contact(cls, contact, contact_field, target_gender):
        """استخراج الأسماء من جهة اتصال محددة"""
        if not hasattr(contact, contact_field):
            return set()
        
        field_value = getattr(contact, contact_field)
        if not field_value:
            return set()
        
        names = re.split(r'[,\n;]+', str(field_value))
        valid_names = set()
        
        for name in names:
            clean_name = name.strip()
            if cls._is_valid_name(clean_name) and cls._matches_gender_filter(clean_name, target_gender):
                valid_names.add(clean_name)
        
        return valid_names
    
    @classmethod
    def _is_valid_name(cls, name):
        """التحقق من صحة الاسم"""
        return name and len(name) > 2
    
    @classmethod
    def _matches_gender_filter(cls, name, target_gender):
        """التحقق من تطابق الجنس إذا كان محدداً"""
        if not target_gender or target_gender == 'ALL':
            return True
        
        name_contact = cls._find_contacts_by_name(name).first()
        return name_contact and name_contact.gender == target_gender
    
    @classmethod
    def _find_contacts_by_names(cls, names):
        """البحث عن جهات اتصال بمجموعة أسماء"""
        if not names:
            return Contacts.objects.none()
        
        q_objects = Q()
        for name in names:
            q_objects |= Q(name_in_arabic__icontains=name)
            q_objects |= Q(nom__icontains=name)
            q_objects |= Q(prenom__icontains=name)
        
        return Contacts.objects.filter(q_objects).distinct()
    
    @classmethod
    def perform_normal_search(cls, search_term):
        """إجراء البحث العادي"""
        q_objects = cls._build_search_query(search_term)
        contacts = Contacts.objects.filter(q_objects)
        return cls._apply_search_priority(contacts, search_term)
    
    @classmethod
    def _build_search_query(cls, search_term):
        """بناء استعلام البحث"""
        q_objects = Q()
        for column in ContactSearchService.SEARCHABLE_COLUMNS:
            if hasattr(Contacts, column):
                q_objects |= Q(**{f'{column}__icontains': search_term})
        return q_objects
    
    @classmethod
    def _apply_search_priority(cls, contacts, search_term):
        """تطبيق أولوية البحث على النتائج"""
        when_conditions = []
        for column, priority in ContactSearchService.FIELD_PRIORITIES.items():
            if hasattr(Contacts, column):
                when_conditions.append(
                    When(**{f'{column}__icontains': search_term}, then=priority)
                )
        
        return contacts.annotate(
            search_priority=Case(
                *when_conditions,
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-search_priority', 'name_in_arabic', 'nom', 'prenom')
    
    @classmethod
    def get_user_contacts(cls, user_id):
        """الحصول على جهات اتصال المستخدم"""
        user_id_str = str(user_id)
        return Contacts.objects.filter(
            Q(author__icontains=user_id_str) |
            Q(author__startswith=user_id_str + ',') |
            Q(author__endswith=',' + user_id_str) |
            Q(author__icontains=',' + user_id_str + ',') |
            Q(author=user_id_str)
        ).distinct()


def _filter_results_by_gender(contacts, relation_term):
    """تصفية النتائج بناءً على الجنس المتوقع من العلاقة"""
    gender_mapping = {
        'أم': 'Female', 'والدة': 'Female', 'أخت': 'Female', 'زوجة': 'Female', 'ابنة': 'Female',
        'أب': 'Male', 'والد': 'Male', 'أخ': 'Male', 'زوج': 'Male', 'ابن': 'Male'
    }
    
    expected_gender = None
    for term, gender in gender_mapping.items():
        if term in relation_term:
            expected_gender = gender
            break
    
    if expected_gender:
        # إرجاع المطابقين للجنس + الذين جنسهم غير محدد
        return contacts.filter(Q(gender=expected_gender) | Q(gender__isnull=True) | Q(gender=''))
    
    return contacts


@login_required
def contacts_index(request):
    """عرض صفحة جهات الاتصال الرئيسية"""
    contacts = _get_initial_contacts(request)
    contacts = _apply_filters(contacts, request)
    contacts = _apply_search(contacts, request)
    
    return _render_contacts_page(request, contacts)


def _get_initial_contacts(request):
    """الحصول على مجموعة جهات الاتصال الأولية"""
    if _has_search_or_filters(request):
        return Contacts.objects.all().order_by('-contacts_id')  # الأحدث أولاً
    return ContactQueryService.get_user_contacts(request.user.id).order_by('-contacts_id')  # الأحدث أولاً


def _has_search_or_filters(request):
    """التحقق من وجود بحث أو فلاتر"""
    return request.GET.get('search') or request.GET.get('role')


def _apply_filters(contacts, request):
    """تطبيق الفلاتر على جهات الاتصال"""
    role = request.GET.get('role')
    if role and hasattr(Contacts, 'role'):
        return contacts.filter(role__icontains=role)
    return contacts


def _apply_search(contacts, request):
    """تطبيق البحث على جهات الاتصال"""
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        return contacts
    
    return _perform_contact_search(search_term, contacts)


def _perform_contact_search(search_term, contacts):
    """إجراء البحث في جهات الاتصال"""
    relation_term, relation_type, clean_name = ContactSearchService.extract_search_components(search_term)
    
    if _should_use_relation_search(relation_term, relation_type, clean_name):
        results = ContactQueryService.perform_relation_based_search(relation_type, clean_name)
        return _filter_results_by_gender(results, relation_term)
    
    return ContactQueryService.perform_normal_search(search_term)


def _should_use_relation_search(relation_term, relation_type, clean_name):
    """تحديد ما إذا كان يجب استخدام البحث بالعلاقة"""
    return relation_term and relation_type and clean_name


def _render_contacts_page(request, contacts):
    """عرض صفحة جهات الاتصال"""
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tifinar/auth/contacts/index.html', {
        'contacts': page_obj,
        'search_term': request.GET.get('search', ''),
        'role': request.GET.get('role', '')
    })