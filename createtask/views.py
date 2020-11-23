from django.shortcuts import render, redirect

from .forms import UploadTaskAndSchema, UploadDerivedSchema, CreateTask, CreateMappingInfo

from basicdb.models import Task, MappingInfo, MappingInfoFromTo

def listTasks(request):
    """
    docstring
    """
    return render(request, 'pages/task_list.html', {
        'list_of_tasks': str(list(Task.objects.values())),
    })

def showTask(request, task_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    return render(request, 'pages/task_select.html', {
        'task_name': task.name,
        'task_info': str(list(Task.objects.filter(id=task_id).values())),
    })

def createTask(request):
    """
    docstring
    """
    
    form = None
    task = None
    if request.method == 'POST':
        form = CreateTask(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            task = form.save()
            # task.activation_state = True
            task.save()

            # return render(request, 'pages/done_task.html', {})
            return redirect('list tasks')
    else:
        form = CreateTask()
    
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

    return render(request, 'pages/task_create.html', {
        'create_task_form': form
    })


def listDerivedSchemas(request, task_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    return render(request, 'pages/derived_schema_list.html', {
        'task_name': task.name,
        'list_of_derived_schemas': str(list(MappingInfo.objects.filter(task=task).values())),
    })


def showDerivedSchema(request, task_id, schema_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    schema = MappingInfo.objects.filter(id=schema_id, task=task)[0]
    return render(request, 'pages/derived_schema_select.html', {
        'task_name': task.name,
        'schema_name': schema.derived_schema_name,
        'schema_info': str(list(MappingInfo.objects.filter(id=schema_id).values())),
        'mapping_info': str(list(MappingInfoFromTo.objects.filter(mapping_info=schema).values())),
    })

def createDerivedSchema(request, task_id):
    """
    docstring
    """
    
    form = None
    task = Task.objects.filter(id=task_id)[0]
    schema = None
    if request.method == 'POST':
        form = CreateMappingInfo(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            schema = form.save(task)
            schema.task = task
            schema.save()

            return redirect('list derived schemas', task_id=task_id)

    else:
        form = CreateMappingInfo()
    
    return render(request, 'pages/derived_schema_create.html', {
        'create_derived_schema_form': form
    })

    