from django.shortcuts import render, redirect

from .models import File
from .forms import UploadForm

# Create your views here.
def index(request):
    """
    docstring
    """
    return render(request, 'pages/index.html', {})

def fileList(request):
    """
    docstring
    """
    return render(request, 'pages/list.html', {
        'files': str(list(File.objects.values()))
    })

def uploadFile(request):
    """
    docstring
    """
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            form.save()
            return redirect('fileList')
    else:
        form = UploadForm()
    return render(request, 'pages/upload.html', {
        'form': form
    })