from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from tifinar.models import Contacts
from django.contrib.auth.decorators import login_required

@login_required
def contacts_index(request):
    users = Contacts.objects.all()
    searchable_columns = [
        'name_in_arabic', 'social_media', 'last_name', 'first_name', 'keywords', 'address',
        'origin_city', 'gender', 'phone', 'email', 'role', 'educational_level',
        'ideology', 'society', 'comment', 'birth_date',
        'spouse', 'children', 'siblings', 'parents', 'maternal_relatives',
        'grandparents', 'friends', 'language',
    ]

    role = request.GET.get('role')
    if role:
        users = users.filter(role__icontains=role)

    search_term = request.GET.get('search')
    if search_term:
        # تعريف جميع علاقات القرابة بشكل كامل
        father = ['أب','اب', 'والد', 'father', 'père de']
        mother = ['أم','ام', 'والدة', 'mother', 'mère de']
        husband = ['زوج', 'husband','خطيب','حبيب','عشيق','l\'époux de ', 'le compagnon de','le conjoine de','le partenaire de ','le mari de']
        wife = ['زوجة', 'wife','عشيقة','خطيبة','حبيبة', 'l\'épouse de', 'la conjointe de', 'la femme de', 'la compagne de', 'la partenaire de']
        son = ['ابن', 'إبن', 'son', 'fils de', 'نجل']
        daughter = ['ابنة', 'إبنة', 'daughter', 'fille de', 'نجلة']
        brother = ['أخ','اخ', 'شقيق', 'brother', 'أخ لأم', 'أخ لأب','frère de']
        sister = ['أخت','اخت', 'شقيقة', 'sister', 'أخت لأم', 'أخت لأب','soeur de','sœur de']
        grandfather = ['جد', 'grandfather','grand-père','père de père de','père de mère de','أب أم','أب أب']
        grandmother = ['جدة', 'grandmother','grand-mère','أم أب','أم أب','mère de mère de','mère de père']
        maternal_uncle = ['خال', 'maternal uncle','أخ أم','l\'oncle','uncle']
        maternal_aunt = ['خالة', 'maternal aunt','aunt','أخت أم']
        paternal_uncle = ['عم', 'paternal uncle','uncle','l\'oncle','أخ أب']
        paternal_aunt = ['عمة', 'paternal aunt','أخت أب','aunt']
        cousin_male = ['ابن عم', 'أبناء عم', 'cousin','cousin de']
        cousin_female = ['ابنة العم','cousine','cousine de']
        niece_nephew_male = ['إبن أخ', 'إبن أخت', 'nephew de']
        niece_nephew_female = ['إبنة أخ', 'إبنة أخت', 'niece de','niéce']
        friend = ["صديق", "رفيق", "صاحب", "زميل", "خل", "رفيق درب","l\'ami de", "le camarade de", "le collègue de", "le copain de", "le pote de", "l\'allié de", "connaissance de","friend", "companion", "buddy", "pal", "mate", "ally", "acquaintance", "colleague"]
        girlfriend = ["صديقة", "رفيقة", "خلة", "زميلة", "صحبة","l\amie", "la compagne de", "la camarade de", "la collègue de", "la copine de", "l\alliée de", "connaissance de","girlfriend", "companion", "buddy", "pal", "mate", "ally", "acquaintance", "colleague"]

        relations = father + mother + husband + wife + son + daughter + brother + sister + grandfather + grandmother + maternal_uncle + maternal_aunt + paternal_uncle + paternal_aunt + cousin_male + cousin_female + niece_nephew_male + niece_nephew_female + friend + girlfriend

        relation_found = None
        for relation in relations:
            if relation in search_term:
                relation_found = relation
                break

        if relation_found:
            parts = search_term.split(relation_found)
            name_part = parts[-1].strip() if len(parts) > 1 else ''
            
            name_matches = Contacts.objects.filter(name_in_arabic__icontains=name_part)
            
            related_names = []
            for user in name_matches:
                # معالجة علاقات الأب والأم
                if relation_found in father + mother:
                    if user.parents:
                        parents = [p.strip() for p in user.parents.split(',') if p.strip()]
                        for parent in parents:
                            parent_user = Contacts.objects.filter(name_in_arabic__icontains=parent).first()
                            if parent_user:
                                if (relation_found in father and parent_user.gender == 'Male') or (relation_found in mother and parent_user.gender == 'Female'):
                                    related_names.append(parent)
                
                # معالجة علاقات الأبناء
                elif relation_found in son + daughter:
                    if user.children:
                        children = [c.strip() for c in user.children.split(',') if c.strip()]
                        for child in children:
                            child_user = Contacts.objects.filter(name_in_arabic__icontains=child).first()
                            if child_user:
                                if (relation_found in son and child_user.gender == 'Male') or (relation_found in daughter and child_user.gender == 'Female'):
                                    related_names.append(child)
                
                # معالجة علاقات الإخوة
                elif relation_found in brother + sister:
                    if user.siblings:
                        siblings = [s.strip() for s in user.siblings.split(',') if s.strip()]
                        for sibling in siblings:
                            sibling_user = Contacts.objects.filter(name_in_arabic__icontains=sibling).first()
                            if sibling_user:
                                if (relation_found in brother and sibling_user.gender == 'Male') or (relation_found in sister and sibling_user.gender == 'Female'):
                                    related_names.append(sibling)
                
                # معالجة علاقات الأزواج
                elif relation_found in husband + wife:
                    if user.spouse:
                        spouses = [s.strip() for s in user.spouse.split(',') if s.strip()]
                        for spouse in spouses:
                            spouse_user = Contacts.objects.filter(name_in_arabic__icontains=spouse).first()
                            if spouse_user:
                                if (relation_found in husband and spouse_user.gender == 'Male') or (relation_found in wife and spouse_user.gender == 'Female'):
                                    related_names.append(spouse)
                
                # معالجة علاقات الأعمام والعمات
                elif relation_found in paternal_uncle + paternal_aunt:
                    if user.paternal_relatives:
                        paternal_rels = [r.strip() for r in user.paternal_relatives.split(',') if r.strip()]
                        for rel in paternal_rels:
                            rel_user = Contacts.objects.filter(name_in_arabic__icontains=rel).first()
                            if rel_user:
                                if (relation_found in paternal_uncle and rel_user.gender == 'Male') or (relation_found in paternal_aunt and rel_user.gender == 'Female'):
                                    related_names.append(rel)
                
                # معالجة علاقات الأخوال والخالات
                elif relation_found in maternal_uncle + maternal_aunt:
                    if user.maternal_relatives:
                        maternal_rels = [r.strip() for r in user.maternal_relatives.split(',') if r.strip()]
                        for rel in maternal_rels:
                            rel_user = Contacts.objects.filter(name_in_arabic__icontains=rel).first()
                            if rel_user:
                                if (relation_found in maternal_uncle and rel_user.gender == 'Male') or (relation_found in maternal_aunt and rel_user.gender == 'Female'):
                                    related_names.append(rel)
                
                # معالجة علاقات الأجداد
                elif relation_found in grandfather + grandmother:
                    if user.grandparents:
                        grandparents = [g.strip() for g in user.grandparents.split(',') if g.strip()]
                        for grandparent in grandparents:
                            grandparent_user = Contacts.objects.filter(name_in_arabic__icontains=grandparent).first()
                            if grandparent_user:
                                if (relation_found in grandfather and grandparent_user.gender == 'Male') or (relation_found in grandmother and grandparent_user.gender == 'Female'):
                                    related_names.append(grandparent)
                
                # معالجة علاقات أبناء العم/العمة
                elif relation_found in cousin_male + cousin_female:
                    if user.cousins:
                        cousins = [c.strip() for c in user.cousins.split(',') if c.strip()]
                        for cousin in cousins:
                            cousin_user = Contacts.objects.filter(name_in_arabic__icontains=cousin).first()
                            if cousin_user:
                                if (relation_found in cousin_male and cousin_user.gender == 'Male') or (relation_found in cousin_female and cousin_user.gender == 'Female'):
                                    related_names.append(cousin)
                
                # معالجة علاقات أبناء الإخوة
                elif relation_found in niece_nephew_male + niece_nephew_female:
                    if user.nieces_nephews:
                        nieces_nephews = [n.strip() for n in user.nieces_nephews.split(',') if n.strip()]
                        for niece_nephew in nieces_nephews:
                            niece_nephew_user = Contacts.objects.filter(name_in_arabic__icontains=niece_nephew).first()
                            if niece_nephew_user:
                                if (relation_found in niece_nephew_male and niece_nephew_user.gender == 'Male') or (relation_found in niece_nephew_female and niece_nephew_user.gender == 'Female'):
                                    related_names.append(niece_nephew)
                
                # معالجة علاقات الأصدقاء
                elif relation_found in friend + girlfriend:
                    if user.friends:
                        friends = [f.strip() for f in user.friends.split(',') if f.strip()]
                        for friend_rel in friends:
                            friend_user = Contacts.objects.filter(name_in_arabic__icontains=friend_rel).first()
                            if friend_user:
                                if (relation_found in friend and friend_user.gender == 'Male') or (relation_found in girlfriend and friend_user.gender == 'Female'):
                                    related_names.append(friend_rel)

            if related_names:
                q_objects = Q()
                for name in set(related_names):  # استخدام set لإزالة التكرارات
                    q_objects |= Q(name_in_arabic__icontains=name)
                users = Contacts.objects.filter(q_objects)
            else:
                users = Contacts.objects.none()
        else:
            # البحث العادي إذا لم تكن هناك علاقة
            q_objects = Q()
            for column in searchable_columns:
                q_objects |= Q(**{f'{column}__icontains': search_term})
            users = users.filter(q_objects)
            
            # ترتيب النتائج حسب أفضل تطابق (تطبيق بسيط)
            users = sorted(users, key=lambda u: sum(
                1 for col in searchable_columns 
                if getattr(u, col) and search_term.lower() in str(getattr(u, col)).lower()
            ), reverse=True)

    # التقسيم إلى صفحات
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # إذا لم يكن هناك بحث وعرض المسؤولين لكل المستخدمين
    if not search_term and not role and request.user.role == 'admin':
        users = Contacts.objects.all()
        paginator = Paginator(users, 20)
        page_obj = paginator.get_page(page_number)
    elif not search_term and not role:
        # للمستخدمين العاديين: عرض الأصدقاء وطلبات الصداقة فقط
        current_user = request.user
        friend_ids = [int(id) for id in current_user.friends.split(',')] if current_user.friends else []
        request_ids = [int(id) for id in current_user.friend_requests.split(',')] if current_user.friend_requests else []
        
        all_ids = list(set(friend_ids + request_ids))
        users = Contacts.objects.filter(id__in=all_ids)
        paginator = Paginator(users, 20)
        page_obj = paginator.get_page(page_number)
    return render(request, 'tifinar/auth/contacts/index.html', {
        'users': page_obj,
        'search_term': search_term,
        'role': role
    })