from django.views import View
from tifinar.models import exams
from tifinar.forms import ExamForm

class ExamListView(View):
    # ... نفس هيكل ArticleListView مع تعديلات النموذج
    pass

class ExamCreateView(View):
    # ... نفس هيكل ArticleCreateView
    pass

class ExamEditView(View):
    # ... نفس هيكل ArticleEditView
    pass