from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
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
        # للمستخدمين العاديين: عرض الأشخاص الذين كتبهم المستخدم فقط
        current_user_id = str(request.user.id)
        
        # البحث في عمود Author الذي يحتوي على IDs مفصولة بفواصل
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

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contacts, contacts_id=contact_id)
    current_user_id = str(request.user.id)
    
    try:
        if request.user.is_superuser:
            # Superadmin - حذف كامل من قاعدة البيانات
            contact_name = f"{contact.prenom} {contact.nom}"
            contact.delete()
            messages.success(request, f'تم حذف الجهة "{contact_name}" بشكل نهائي من قاعدة البيانات')
            
        else:
            # مستخدم عادي - إزالة ID المستخدم من عمود Author فقط
            if contact.author:
                author_ids = [id.strip() for id in str(contact.author).split(',') if id.strip()]
                
                if current_user_id in author_ids:
                    # إزالة ID المستخدم من القائمة
                    author_ids.remove(current_user_id)
                    
                    if author_ids:
                        # تحديث العمود بالقائمة الجديدة
                        contact.author = ','.join(author_ids)
                    else:
                        # إذا لم يتبقى أي authors، يمكن حذف الجهة أو تركها
                        contact.author = ''
                    
                    contact.save()
                    messages.success(request, f'تم إزالة صلاحيتك عن الجهة "{contact.prenom} {contact.nom}"')
                else:
                    messages.error(request, 'ليس لديك صلاحية لهذه الجهة')
            else:
                messages.error(request, 'هذه الجهة لا تملك معلومات authors')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'تمت العملية بنجاح'})
            
        return redirect('contacts')
        
    except Exception as e:
        error_message = f'حدث خطأ أثناء المعالجة: {str(e)}'
        messages.error(request, error_message)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': error_message})
            
        return redirect('contacts')