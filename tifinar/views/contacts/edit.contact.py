from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from tifinar.models import Contacts
import random

@login_required
@require_http_methods(["GET", "POST"])
def edit_contact(request, contacts_id):
    """
    تعديل الملف الشخصي للمستخدم
    """
    contact = get_object_or_404(Contacts, contacts_id=contacts_id)

    
    if request.method == 'POST':
        try:
            # DEBUG: التحقق من جميع attributes الموجودة في contact
            print("=== جميع attributes في contact ===")
            for attr in dir(contact):
                if not attr.startswith('_'):  # تجاهل الـ private attributes
                    try:
                        value = getattr(contact, attr)
                        print(f"{attr}: {value} ({type(value)})")
                    except Exception as e:
                        print(f"{attr}: ERROR - {e}")
            print("================================")
            
            # DEBUG: التحقق من وجود date_de_naissance بشكل صريح
            print(f"hasattr date_de_naissance: {hasattr(contact, 'date_de_naissance')}")
            if hasattr(contact, 'date_de_naissance'):
                print(f"قيمة date_de_naissance: {contact.date_de_naissance}")
            else:
                print("date_de_naissance غير موجود!")
                # اطبع جميع الحقول الحقيقية في الموديل
                print("حقول الموديل:", [f.name for f in contact._meta.get_fields()])
            
            # تحديث الحقول الأساسية
            contact.prenom = request.POST.get('prenom', contact.prenom)
            contact.nom = request.POST.get('nom', contact.nom)
            contact.email = request.POST.get('email', contact.email)
            contact.tel = request.POST.get('tel', contact.tel)
            
            # تحديث الحقول الاختيارية
            contact.gender = request.POST.get('gender', contact.gender)
            contact.societe = request.POST.get('societe', contact.societe)
            contact.adresse = request.POST.get('adresse', contact.adresse)
            contact.ville_d_origine = request.POST.get('ville_d_origine', contact.ville_d_origine)
            etat_social = request.POST.get('Etat_Social')
            if etat_social:  # فقط إذا كانت القيمة موجودة وغير فارغة
                contact.Etat_Social = etat_social
            
            # تحديث تاريخ الميلاد - بحذر شديد
            date_value = request.POST.get('date_de_naissance')
            if date_value:
                # التحقق مرة أخرى قبل التعيين
                if hasattr(contact, 'date_de_naissance'):
                    contact.date_de_naissance = date_value
                    print(f"✓ تم تحديث تاريخ الميلاد: {date_value}")
                else:
                    print("✗ date_de_naissance غير موجود - تم تخطي التحديث")
            
            # باقي الحقول...
            contact.ideologie = request.POST.get('ideologie', contact.ideologie)
            contact.commentaire = request.POST.get('commentaire', contact.commentaire)
            contact.social_media = request.POST.get('social_media', contact.social_media)
            contact.educational_level = request.POST.get('educational_level', contact.educational_level)
            contact.name_in_arabic = request.POST.get('name_in_arabic', contact.name_in_arabic)
            
            # تحديث الحقول الإدارية
            if getattr(request.user, 'role', None) == 'admin':
                contact.children = request.POST.get('children', contact.children)
                contact.siblings = request.POST.get('siblings', contact.siblings)
                contact.cousins = request.POST.get('cousin', contact.cousins)
                contact.parents = request.POST.get('parents', contact.parents)
                contact.maternal_relatives = request.POST.get('maternal_relatives', contact.maternal_relatives)
                contact.paternal_relatives = request.POST.get('paternal_relatives', contact.paternal_relatives)
                contact.grandparents = request.POST.get('grandparents', contact.grandparents)
                contact.keywords = request.POST.get('keywords', contact.keywords)
                contact.spouse = request.POST.get('spouse', contact.spouse)
            
            # معالجة الصور المرفوعة
            if 'path' in request.FILES:
                uploaded_file = request.FILES['path']
                # حفظ الملف في المسار المناسب
            
            print("✓ تم تحديث جميع الحقول بنجاح - جاري الحفظ...")
            contact.save()
            messages.success(request, "تم تحديث الملف الشخصي بنجاح")
            return redirect('contact_view', contacts_id=contact.contacts_id)
            
        except Exception as e:
            # طباعة الخطأ الكامل للتصحيح
            import traceback
            error_traceback = traceback.format_exc()
            print(f"=== الخطأ الكامل ===")
            print(error_traceback)
            print(f"====================")
            
            messages.error(request, f"حدث خطأ أثناء التحديث: {str(e)}")
    
    return render(request, 'tifinar/auth/contacts/edit_contact.html', {
        'contact': contact,
    })