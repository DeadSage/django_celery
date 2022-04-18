from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from core.celery import handle_uploaded_file
from .forms import DocumentForm
from .models import Document
import os
import core.settings as settings


def index(request):
    return render(request, 'url_check/index.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            handle_uploaded_file.delay()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'url_check/model_form_upload.html', {
        'form': form
    })


class ResultsView(generic.ListView):
    template_name = 'url_check/results.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Document.objects.all()


# class FileFieldFormView(FormView):
#     form_class = DocumentForm
#     template_name = 'url_check/model_form_upload.html'  # Replace with your template.
#     success_url = reverse_lazy('home')  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES
#         if form.is_valid():
#             print(files)
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
