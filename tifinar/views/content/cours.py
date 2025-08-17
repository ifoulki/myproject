from django.views import View
from tifinar.models import cours
from tifinar.forms import CoursForm

class CoursListView(View):
    # ... نفس هيكل ArticleListView مع تعديلات النموذج
    pass

class CoursCreateView(View):
    # ... نفس هيكل ArticleCreateView
    pass

class CoursEditView(View):
    # ... نفس هيكل ArticleEditView
    pass