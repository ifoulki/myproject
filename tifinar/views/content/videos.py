from django.views import View
from tifinar.models import videos
from tifinar.forms import VideoForm

class VideoListView(View):
    # ... نفس هيكل ArticleListView مع تعديلات النموذج
    pass

class VideoCreateView(View):
    # ... نفس هيكل ArticleCreateView
    pass

class VideoEditView(View):
    # ... نفس هيكل ArticleEditView
    pass