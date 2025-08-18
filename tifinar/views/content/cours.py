from django.shortcuts import render, get_object_or_404
from tifinar.models import cours
import random

def show_cours(request, slug):
    cour = get_object_or_404(cours, slug=slug)
    
    contents = cour.cours_contents.split(',') if cour.cours_contents else []
    images = cour.images.split(',') if cour.images else []
    
    content_image_pairs = [
        {'content': c.strip(), 'image': i.strip()} 
        for c, i in zip(contents, images) 
        if c.strip() and i.strip()
    ]
    
    # 👇 هنا الخلط
    random.shuffle(content_image_pairs)
    
    context = {
        'title': cour.title,
        'articles': cour.title,
        'updated_at': cour.updated_at,
        'the_type': cour.the_type,
        'intro': cour.intro,
        'folder_child': cour.myfile,
        'image': cour.myimage,
        'dir': cour.dir or 'rtl',
        'content_image_pairs': content_image_pairs,
        'cours_contents': contents,
        'images': images,
    }
    
    return render(request, 'tifinar/showCours.html', context)
