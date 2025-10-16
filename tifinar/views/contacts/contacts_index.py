# tifinar/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tifinar.models import Contacts, synonym_terms
import re

class DynamicContactSearch:
    """فئة ديناميكية للبحث باستخدام جدول المرادفات"""
    
    @staticmethod
    def get_all_synonyms():
        """الحصول على جميع المرادفات من قاعدة البيانات"""
        synonyms_data = {}
        all_entries = synonym_terms.objects.all()
        
        for entry in all_entries:
            # جمع جميع المرادفات في قائمة واحدة
            all_terms = [entry.term.strip()]
            if entry.synonyms:
                all_terms.extend([syn.strip() for syn in entry.synonyms.split(',') if syn.strip()])
            
            # تخزين البيانات المهمة
            synonyms_data[entry.relation_type] = {
                'terms': all_terms,
                'contact_field': entry.contact_field,
                'target_gender': entry.target_gender,
                'ignore_terms': [term.strip() for term in entry.ignore_terms.split(',')] if entry.ignore_terms else []
            }
        
        return synonyms_data
    
    @staticmethod
    def extract_relation_and_name(search_term):
        """استخراج العلاقة والاسم من مصطلح البحث باستخدام جدول المرادفات"""
        synonyms_data = DynamicContactSearch.get_all_synonyms()
        
        # جمع جميع المصطلحات من جميع العلاقات
        all_terms = []
        term_to_relation = {}
        
        for relation_type, data in synonyms_data.items():
            for term in data['terms']:
                all_terms.append(term)
                term_to_relation[term] = relation_type
        
        # البحث عن مصطلح مطابق
        for term in all_terms:
            if term and term in search_term:
                # التحقق من عدم وجود كلمات محظورة
                relation_type = term_to_relation[term]
                ignore_terms = synonyms_data[relation_type]['ignore_terms']
                
                if not any(ignore_term in search_term for ignore_term in ignore_terms):
                    # استخراج الاسم
                    name = search_term.replace(term, '').strip()
                    # تنظيف الاسم
                    clean_name = DynamicContactSearch.clean_name(name, synonyms_data[relation_type]['terms'])
                    return term, relation_type, clean_name
        
        return None, None, search_term
    
    @staticmethod
    def clean_name(name, relation_terms):
        """تنظيف الاسم من الكلمات المتعلقة بالعلاقات"""
        # إنشاء نمط regex من جميع مصطلحات العلاقات
        pattern_terms = []
        for term in relation_terms:
            # الهروب من الأحخاص الخاصة في regex
            escaped_term = re.escape(term)
            pattern_terms.append(escaped_term)
        
        # إضافة كلمات شائعة أخرى
        common_terms = ['أخت', 'أخ', 'شقيقة', 'شقيق', 'والد', 'والدة', 'ابن', 'ابنة', 'زوج', 'زوجة', 'إلخ']
        pattern_terms.extend(common_terms)
        
        pattern = r'\b(' + '|'.join(pattern_terms) + r')\b'
        clean_name = re.sub(pattern, '', name).strip()
        return clean_name
    
    @staticmethod
    def get_relation_info(relation_type):
        """الحصول على معلومات العلاقة من جدول المرادفات"""
        try:
            entry = synonym_terms.objects.get(relation_type=relation_type)
            return {
                'contact_field': entry.contact_field,
                'target_gender': entry.target_gender,
                'ignore_terms': [term.strip() for term in entry.ignore_terms.split(',')] if entry.ignore_terms else []
            }
        except synonym_terms.DoesNotExist:
            return None

@login_required
def contacts_index(request):
    contacts = Contacts.objects.all()
    
    # تعريف أولويات الحقول للترتيب
    field_priorities = {
        'name_in_arabic': 17,
        'nom': 16,
        'prenom': 15,
        'friends': 14,
        'siblings': 13,
        'parents': 12,
        'spouse': 12,
        'children': 12,
        'cousins': 12,
        'adresse': 11,
        'tel': 11,
        'email': 11,
        'ideologie': 10,
        'societe': 9,
        'gender': 8,
        'the_type': 7,
        'keywords': 7,
        'maternal_relatives': 6,
        'paternal_relatives': 6,
        'ville_d_origine': 5,
        'social_media': 5,
        'educational_level': 4,
        'commentaire': 3,
        'grandparents': 2,
        'date_de_naissance': 2,
        'path': 1,
        'author': 0,
    }

    searchable_columns = list(field_priorities.keys())

    role = request.GET.get('role')
    if role and hasattr(Contacts, 'role'):
        contacts = contacts.filter(role__icontains=role)

    search_term = request.GET.get('search')
    if search_term:
        # استخدام المنطق الديناميكي مع جدول المرادفات
        relation_term, relation_type, name = DynamicContactSearch.extract_relation_and_name(search_term)
        
        if relation_term and relation_type and name:
            print(f"Found relation: '{relation_term}' (type: {relation_type}) for name: '{name}'")
            
            # الحصول على معلومات العلاقة
            relation_info = DynamicContactSearch.get_relation_info(relation_type)
            
            if relation_info:
                # البحث عن الأشخاص الأساسيين
                main_contacts = Contacts.objects.filter(
                    Q(name_in_arabic__icontains=name) |
                    Q(nom__icontains=name) |
                    Q(prenom__icontains=name)
                )
                
                print(f"Found {main_contacts.count()} main contacts")
                
                if main_contacts.exists():
                    # الحصول على الأسماء المرتبطة
                    related_names = get_related_names_dynamic(main_contacts, relation_info)
                    print(f"Found {len(related_names)} related names: {related_names}")
                    
                    if related_names:
                        # البحث عن الجهات المرتبطة
                        contacts = search_related_contacts(related_names)
                    else:
                        contacts = normal_search(search_term, searchable_columns, field_priorities)
                else:
                    contacts = normal_search(search_term, searchable_columns, field_priorities)
            else:
                contacts = normal_search(search_term, searchable_columns, field_priorities)
        else:
            # البحث العادي
            contacts = normal_search(search_term, searchable_columns, field_priorities)

    # باقي الكود كما هو...
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not search_term and not role:
        current_user_id = str(request.user.id)
        contacts = Contacts.objects.filter(
            Q(author__icontains=current_user_id) |
            Q(author__startswith=current_user_id + ',') |
            Q(author__endswith=',' + current_user_id) |
            Q(author__icontains=',' + current_user_id + ',') |
            Q(author=current_user_id)
        ).distinct()
        paginator = Paginator(contacts, 20)
        page_obj = paginator.get_page(page_number)

    return render(request, 'tifinar/auth/contacts/index.html', {
        'contacts': page_obj,
        'search_term': search_term or '',
        'role': role or ''
    })

def get_related_names_dynamic(contacts, relation_info):
    """الحصول على الأسماء المرتبطة باستخدام معلومات العلاقة الديناميكية"""
    related_names = []
    contact_field = relation_info['contact_field']
    target_gender = relation_info['target_gender']
    
    for contact in contacts:
        if hasattr(contact, contact_field):
            field_value = getattr(contact, contact_field)
            if field_value:
                # تقسيم الأسماء
                names_array = field_value.split(',')
                for name in names_array:
                    name = name.strip()
                    if name:
                        # التحقق من الجنس إذا كان محدداً
                        if target_gender and target_gender != 'ALL':
                            name_contact = Contacts.objects.filter(
                                Q(name_in_arabic__icontains=name) |
                                Q(nom__icontains=name) |
                                Q(prenom__icontains=name)
                            ).first()
                            
                            if name_contact and name_contact.gender == target_gender:
                                related_names.append(name)
                        else:
                            related_names.append(name)
    
    return list(set(related_names))

def search_related_contacts(related_names):
    """البحث عن الجهات المرتبطة"""
    if not related_names:
        return Contacts.objects.none()
    
    q_objects = Q()
    for name in related_names:
        if name:
            q_objects |= Q(name_in_arabic__icontains=name)
            q_objects |= Q(nom__icontains=name)
            q_objects |= Q(prenom__icontains=name)
    
    return Contacts.objects.filter(q_objects).distinct()

def normal_search(search_term, searchable_columns, field_priorities):
    """البحث العادي"""
    q_objects = Q()
    for column in searchable_columns:
        if hasattr(Contacts, column):
            q_objects |= Q(**{f'{column}__icontains': search_term})
    
    contacts = Contacts.objects.filter(q_objects)
    
    when_conditions = []
    for column, priority in field_priorities.items():
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