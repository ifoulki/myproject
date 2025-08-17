from django.views import View
from tifinar.models import books
from tifinar.forms import BookForm

class BookListView(View):
    # ... نفس هيكل ArticleListView مع تعديلات النموذج
    pass

class BookCreateView(View):
    # ... نفس هيكل ArticleCreateView
    pass

class BookEditView(View):
    # ... نفس هيكل ArticleEditView
    pass