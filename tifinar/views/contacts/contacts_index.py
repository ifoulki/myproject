from django.shortcuts import render
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tifinar.models import Contacts, synonym_terms

@login_required
def contacts_index(request):
    contacts = Contacts.objects.all()
    
    # تعريف أولويات الحقول للترتيب
    field_priorities = {
        'name_in_arabic': 17,  # الأعلى أولوية
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
        # البحث في جدول المرادفات
        synonym_entries = synonym_terms.objects.all()
        matched_entry = None
        
        for entry in synonym_entries:
            terms_to_check = [entry.term.strip()] 
            if entry.synonyms:
                terms_to_check.extend([syn.strip() for syn in entry.synonyms.split(',') if syn.strip()])
            
            ignore_terms = []
            if entry.ignore_terms:
                ignore_terms = [ignore.strip() for ignore in entry.ignore_terms.split(',') if ignore.strip()]
            
            # البحث عن أي مصطلح مطابق
            for t in terms_to_check:
                if t and t in search_term:
                    # التحقق من عدم وجود كلمات محظورة
                    if not any(ignore in search_term for ignore in ignore_terms):
                        matched_entry = entry
                        break
            if matched_entry:
                break

        if matched_entry:
            print(f"Matched synonym: {matched_entry.term}, field: {matched_entry.contact_field}")
            
            # استخراج الاسم بعد المصطلح
            name_part = search_term
            for term in [matched_entry.term] + (matched_entry.synonyms.split(',') if matched_entry.synonyms else []):
                if term.strip() in search_term:
                    parts = search_term.split(term.strip())
                    name_part = parts[-1].strip() if parts[-1].strip() else (parts[0].strip() if parts[0].strip() else search_term)
                    break

            print(f"Name part extracted: '{name_part}'")
            
            # البحث عن الأسماء المطابقة للجزء المستخرج
            name_matches = Contacts.objects.filter(
                Q(name_in_arabic__icontains=name_part) |
                Q(nom__icontains=name_part) |
                Q(prenom__icontains=name_part)
            )

            related_names = []
            target_field = matched_entry.contact_field
            target_gender = matched_entry.target_gender

            print(f"Found {name_matches.count()} name matches")
            
            for contact in name_matches:
                if target_field and hasattr(contact, target_field):
                    field_value = getattr(contact, target_field, '')
                    if field_value:
                        print(f"Field {target_field} value: {field_value}")
                        # تقسيم الأسماء بفواصل
                        names_list = []
                        if isinstance(field_value, str):
                            if ',' in field_value:
                                names_list = [name.strip() for name in field_value.split(',') if name.strip()]
                            else:
                                names_list = [field_value.strip()]
                        
                        for rel_name in names_list:
                            if rel_name:
                                # البحث عن الأسماء المرتبطة
                                rel_contacts = Contacts.objects.filter(
                                    Q(name_in_arabic__icontains=rel_name) |
                                    Q(nom__icontains=rel_name) |
                                    Q(prenom__icontains=rel_name)
                                )
                                
                                for rel_contact in rel_contacts:
                                    # التحقق من الجنس إذا محدد
                                    gender_match = True
                                    if target_gender and rel_contact.gender:
                                        gender_match = (rel_contact.gender.lower() == target_gender.lower())
                                    
                                    if gender_match:
                                        related_names.append(rel_contact.name_in_arabic or f"{rel_contact.nom} {rel_contact.prenom}")

            print(f"Related names found: {related_names}")
            
            if related_names:
                # البحث عن جميع الأسماء المرتبطة
                q_objects = Q()
                for name in set(related_names):
                    if name:
                        q_objects |= Q(name_in_arabic__icontains=name)
                        q_objects |= Q(nom__icontains=name)
                        q_objects |= Q(prenom__icontains=name)
                
                contacts = Contacts.objects.filter(q_objects).distinct()
            else:
                contacts = Contacts.objects.none()
                
        else:
            # البحث العادي مع ترتيب الأولويات
            q_objects = Q()
            for column in searchable_columns:
                if hasattr(Contacts, column):
                    q_objects |= Q(**{f'{column}__icontains': search_term})
            
            contacts = contacts.filter(q_objects)
            
            # إضافة ترتيب الأولويات للنتائج
            when_conditions = []
            for column, priority in field_priorities.items():
                if hasattr(Contacts, column):
                    when_conditions.append(
                        When(**{f'{column}__icontains': search_term}, then=priority)
                    )
            
            # ترتيب النتائج حسب الأولوية ثم حسب الاسم
            contacts = contacts.annotate(
                search_priority=Case(
                    *when_conditions,
                    default=0,
                    output_field=IntegerField()
                )
            ).order_by('-search_priority', 'name_in_arabic', 'nom', 'prenom')

    # التقسيم إلى صفحات
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # إذا لم يكن هناك بحث
    if not search_term and not role:
        # للمستخدمين العاديين: عرض الأصدقاء فقط
        current_contact = request.user
        
        friend_ids = []
        if hasattr(current_contact, 'friends') and current_contact.friends:
            try:
                friend_ids = [int(id.strip()) for id in str(current_contact.friends).split(',') if id.strip().isdigit()]
            except (ValueError, AttributeError):
                friend_ids = []
        
        if friend_ids:
            contacts = Contacts.objects.filter(contacts_id__in=friend_ids)
        else:
            contacts = Contacts.objects.none()
        
        paginator = Paginator(contacts, 20)
        page_obj = paginator.get_page(page_number)

    return render(request, 'tifinar/auth/contacts/index.html', {
        'contacts': page_obj,
        'search_term': search_term or '',
        'role': role or ''
    })