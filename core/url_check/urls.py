from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from url_check.views import model_form_upload, index, ResultsView, download
from django.conf.urls.static import static
import core.settings as settings


urlpatterns = [
    path('upload/', model_form_upload, name='upload'),
    path('', index, name='home'),
    path('results/', ResultsView.as_view(), name='results'),
    url(r'^media/(?P<path>.*)$', download, name='download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
