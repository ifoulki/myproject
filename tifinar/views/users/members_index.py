from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from tifinar.models import AuthUser
from django.contrib.auth.decorators import login_required

@login_required
def members_index(request):
    members = AuthUser.objects.all()
    searchable_columns = [
        'name_in_arabic', 'social_media', 'last_name', 'first_name', 'keywords', 'address',
        'origin_city', 'gender', 'phone', 'email', 'role', 'educational_level',
        'ideology', 'society', 'comment', 'birth_date',
        'spouse', 'children', 'siblings', 'parents', 'maternal_relatives',
        'grandparents', 'friends', 'language',
    ]

    role = request.GET.get('role')
    if role:
        members = members.filter(role__icontains=role)

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
            
            name_matches = AuthUser.objects.filter(name_in_arabic__icontains=name_part)
            
            related_names = []
            for member in name_matches:
                # معالجة علاقات الأب والأم
                if relation_found in father + mother:
                    if member.parents:
                        parents = [p.strip() for p in member.parents.split(',') if p.strip()]
                        for parent in parents:
                            parent_member = AuthUser.objects.filter(name_in_arabic__icontains=parent).first()
                            if parent_member:
                                if (relation_found in father and parent_member.gender == 'Male') or (relation_found in mother and parent_member.gender == 'Female'):
                                    related_names.append(parent)
                
                # معالجة علاقات الأبناء
                elif relation_found in son + daughter:
                    if member.children:
                        children = [c.strip() for c in member.children.split(',') if c.strip()]
                        for child in children:
                            child_member = AuthUser.objects.filter(name_in_arabic__icontains=child).first()
                            if child_member:
                                if (relation_found in son and child_member.gender == 'Male') or (relation_found in daughter and child_member.gender == 'Female'):
                                    related_names.append(child)
                
                # معالجة علاقات الإخوة
                elif relation_found in brother + sister:
                    if member.siblings:
                        siblings = [s.strip() for s in member.siblings.split(',') if s.strip()]
                        for sibling in siblings:
                            sibling_member = AuthUser.objects.filter(name_in_arabic__icontains=sibling).first()
                            if sibling_member:
                                if (relation_found in brother and sibling_member.gender == 'Male') or (relation_found in sister and sibling_member.gender == 'Female'):
                                    related_names.append(sibling)
                
                # معالجة علاقات الأزواج
                elif relation_found in husband + wife:
                    if member.spouse:
                        spouses = [s.strip() for s in member.spouse.split(',') if s.strip()]
                        for spouse in spouses:
                            spouse_member = AuthUser.objects.filter(name_in_arabic__icontains=spouse).first()
                            if spouse_member:
                                if (relation_found in husband and spouse_member.gender == 'Male') or (relation_found in wife and spouse_member.gender == 'Female'):
                                    related_names.append(spouse)
                
                # معالجة علاقات الأعمام والعمات
                elif relation_found in paternal_uncle + paternal_aunt:
                    if member.paternal_relatives:
                        paternal_rels = [r.strip() for r in member.paternal_relatives.split(',') if r.strip()]
                        for rel in paternal_rels:
                            rel_member = AuthUser.objects.filter(name_in_arabic__icontains=rel).first()
                            if rel_member:
                                if (relation_found in paternal_uncle and rel_member.gender == 'Male') or (relation_found in paternal_aunt and rel_member.gender == 'Female'):
                                    related_names.append(rel)
                
                # معالجة علاقات الأخوال والخالات
                elif relation_found in maternal_uncle + maternal_aunt:
                    if member.maternal_relatives:
                        maternal_rels = [r.strip() for r in member.maternal_relatives.split(',') if r.strip()]
                        for rel in maternal_rels:
                            rel_member = AuthUser.objects.filter(name_in_arabic__icontains=rel).first()
                            if rel_member:
                                if (relation_found in maternal_uncle and rel_member.gender == 'Male') or (relation_found in maternal_aunt and rel_member.gender == 'Female'):
                                    related_names.append(rel)
                
                # معالجة علاقات الأجداد
                elif relation_found in grandfather + grandmother:
                    if member.grandparents:
                        grandparents = [g.strip() for g in member.grandparents.split(',') if g.strip()]
                        for grandparent in grandparents:
                            grandparent_member = AuthUser.objects.filter(name_in_arabic__icontains=grandparent).first()
                            if grandparent_member:
                                if (relation_found in grandfather and grandparent_member.gender == 'Male') or (relation_found in grandmother and grandparent_member.gender == 'Female'):
                                    related_names.append(grandparent)
                
                # معالجة علاقات أبناء العم/العمة
                elif relation_found in cousin_male + cousin_female:
                    if member.cousins:
                        cousins = [c.strip() for c in member.cousins.split(',') if c.strip()]
                        for cousin in cousins:
                            cousin_member = AuthUser.objects.filter(name_in_arabic__icontains=cousin).first()
                            if cousin_member:
                                if (relation_found in cousin_male and cousin_member.gender == 'Male') or (relation_found in cousin_female and cousin_member.gender == 'Female'):
                                    related_names.append(cousin)
                
                # معالجة علاقات أبناء الإخوة
                elif relation_found in niece_nephew_male + niece_nephew_female:
                    if member.nieces_nephews:
                        nieces_nephews = [n.strip() for n in member.nieces_nephews.split(',') if n.strip()]
                        for niece_nephew in nieces_nephews:
                            niece_nephew_member = AuthUser.objects.filter(name_in_arabic__icontains=niece_nephew).first()
                            if niece_nephew_member:
                                if (relation_found in niece_nephew_male and niece_nephew_member.gender == 'Male') or (relation_found in niece_nephew_female and niece_nephew_member.gender == 'Female'):
                                    related_names.append(niece_nephew)
                
                # معالجة علاقات الأصدقاء
                elif relation_found in friend + girlfriend:
                    if member.friends:
                        friends = [f.strip() for f in member.friends.split(',') if f.strip()]
                        for friend_rel in friends:
                            friend_member = AuthUser.objects.filter(name_in_arabic__icontains=friend_rel).first()
                            if friend_member:
                                if (relation_found in friend and friend_member.gender == 'Male') or (relation_found in girlfriend and friend_member.gender == 'Female'):
                                    related_names.append(friend_rel)

            if related_names:
                q_objects = Q()
                for name in set(related_names):  # استخدام set لإزالة التكرارات
                    q_objects |= Q(name_in_arabic__icontains=name)
                members = AuthUser.objects.filter(q_objects)
            else:
                members = AuthUser.objects.none()
        else:
            # البحث العادي إذا لم تكن هناك علاقة
            q_objects = Q()
            for column in searchable_columns:
                q_objects |= Q(**{f'{column}__icontains': search_term})
            members = members.filter(q_objects)
            
            # ترتيب النتائج حسب أفضل تطابق (تطبيق بسيط)
            members = sorted(members, key=lambda u: sum(
                1 for col in searchable_columns 
                if getattr(u, col) and search_term.lower() in str(getattr(u, col)).lower()
            ), reverse=True)

    # التقسيم إلى صفحات
    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # إذا لم يكن هناك بحث وعرض المسؤولين لكل المستخدمين
    if not search_term and not role and request.user.role == 'admin':
        members = AuthUser.objects.all()
        paginator = Paginator(members, 20)
        page_obj = paginator.get_page(page_number)
    elif not search_term and not role:
        # للمستخدمين العاديين: عرض الأصدقاء وطلبات الصداقة فقط
        current_member = request.user
        friend_ids = [int(id) for id in current_member.friends.split(',')] if current_member.friends else []
        request_ids = [int(id) for id in current_member.friend_requests.split(',')] if current_member.friend_requests else []
        
        all_ids = list(set(friend_ids + request_ids))
        members = AuthUser.objects.filter(id__in=all_ids)
        paginator = Paginator(members, 20)
        page_obj = paginator.get_page(page_number)
    return render(request, 'tifinar/auth/users/index.html', {
        'members': page_obj,
        'search_term': search_term,
        'role': role
    })