from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from core.celery import handle_uploaded_file
from .forms import DocumentForm


def index(request):
    return render(request, 'url_check/index.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['document'])
            form.save()
            # print(type(request.FILES['document'].chunks()))
            handle_uploaded_file.delay(request.FILES['document'].name)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'url_check/model_form_upload.html', {
        'form': form
    })

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
