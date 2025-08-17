from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from tifinar.models import books
from django.utils import timezone

def book_detail(request, slug):
    book = get_object_or_404(books, slug=slug)
    
    # الحصول على الكتاب التالي
    next_obj = (
        books.objects.filter(books_id__gt=book.books_id).order_by('books_id').first() or
        books.objects.filter(books_id__lt=book.books_id).order_by('-books_id').first()
    )

    base_query = books.objects.exclude(slug=slug)
    
    if request.user.is_authenticated:
        user = request.user
        query = Q()
        
        if hasattr(user, 'educational_level'):
            query |= Q(educational_level=user.educational_level) | Q(educational_level='unknown')
        
        if hasattr(user, 'gender'):
            query |= Q(gender=user.gender) | Q(gender='unknown')
        
        if hasattr(user, 'Date_de_naissance') and user.Date_de_naissance:
            age = timezone.now().year - user.Date_de_naissance.year
            query |= Q(min_age__lte=age, max_age__gte=age)
        
        related_books = base_query.filter(query) if query else base_query.none()
    else:
        related_books = base_query.filter(
            Q(the_type__in=[
                'أصناف أخرى',
                'الثقافة العامة',
                'without_board',
                'عام',
                'متنوع',
                'قصص و روايات',
                'قصائد شعرية',
                'مجلات',
                'لقواميس اللغوية - Dictionaries',
                'أديان',
                'فلسفة',
                'الأمازيغية',
                'العربية',
                'الفرنسية',
                'الإنجليزية',
                'علوم الحاسوب',
                'رياضيات',
                'الكيمياء',
                'الفزياء',
                'علوم الحياة والأرض',
                'صحة وحياة',
                'حقوق الإنسان',
                'تربية وتعليم'
            ]) |
            Q(the_type__isnull=True)
        )

    related_books = list(related_books.order_by('?')[:6])

    context = {
        'book': book,  # تصحيح: إزالة المسافة قبل book
        'title': book.title,
        'subject': book.mysubject,
        'description': book.mydescription,
        'myimage': book.myimage,
        'folder': "books",
        'author': book.author,
        'autre': book.autre,
        'next_obj': next_obj,
        'related_articles': related_books,  
        'updated_at': book.updated_at,
        'dir': book.dir,
    }
    
    return render(request, 'tifinar/showContent.html', context)