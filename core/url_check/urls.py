from django.urls import path, include
from url_check.views import model_form_upload, index, ResultsView

urlpatterns = [
    path('upload/', model_form_upload, name='upload'),
    path('', index, name='home'),
    path('results/', ResultsView.as_view(), name='results')
]
