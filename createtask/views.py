from django.shortcuts import render

from .forms import UploadTask

from basicdb.models import Task

# Create your views here.
def createTask(request):
    """
    docstring
    """
    
    form = None
    task = None
    if request.method == 'POST':
        form = UploadTask(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            task = form.save()
            task.activation_state = True
            task.save()

            return render(request, 'pages/done.html', {})
    else:
        form = UploadTask()
    
    # name = "test_task"
    # minimal_upload_frequency = 0
    # description = "test_desc"
    # original_data_description = "what is this?"

    # task = Task(
    #     name=name,
    #     minimal_upload_frequency=minimal_upload_frequency,
    #     activation_state=True,
    #     description=description,
    #     original_data_description=original_data_description
    # )

    return render(request, 'pages/create.html', {
        'create_form': form
    })