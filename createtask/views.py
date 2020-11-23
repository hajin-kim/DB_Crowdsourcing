from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreateTask, CreateSchemaAttribute, CreateMappingInfo, CreateMappingInfoFromTo

from basicdb.models import Task, SchemaAttribute, MappingInfo, MappingInfoFromTo


def generateListString(iterable):
    """
    1. each element of iterable contains .__str__()
    2. use |linebreaks tag on template html file to display
    """
    text = ""
    for i in iterable:
        text += i.__str__()
        text += '\n'
    return text


"""
view functions for task
"""
def listTasks(request):
    """
    docstring
    """
    tasks = generateListString(Task.objects.values())
    return render(request, 'pages/task_list.html', {
        'list_of_tasks': tasks,
    })

def showTask(request, task_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    attributes = generateListString(SchemaAttribute.objects.filter(task=task))
    derived_schemas = generateListString(MappingInfo.objects.filter(task=task))
    return render(request, 'pages/task_select.html', {
        'task_name': task.name,
        'task_info': str(list(Task.objects.filter(id=task_id).values())),
        'task_attributes': attributes,
        'task_derived_schemas': derived_schemas,
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

"""
view functions for attribute
"""
def listAttributes(request, task_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    attributes = generateListString(SchemaAttribute.objects.filter(task=task))
    return render(request, 'pages/attribute_list.html', {
        'task_name': task.name,
        'list_of_attributes': attributes,
    })

def createAttribute(request, task_id):
    """
    docstring
    """
    form = None
    task = Task.objects.filter(id=task_id)[0]
    attribute = None

    if task.activation_state:
        return HttpResponse("<h2>태스크가 활성화되어 있습니다!</h3>")
    
    attributes = generateListString(SchemaAttribute.objects.filter(task=task))

    if request.method == 'POST':
        form = CreateSchemaAttribute(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            attribute = form.save(task)
            # attribute.task = task
            attribute.save()

            return redirect('create attribute', task_id=task_id)

    else:
        form = CreateSchemaAttribute()
    
    return render(request, 'pages/attribute_create.html', {
        'create_attribute_form': form,
        'list_of_attributes': attributes,
    })

"""
view functions for derived schema
"""
def listDerivedSchemas(request, task_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    derived_schemas = generateListString(MappingInfo.objects.filter(task=task))
    return render(request, 'pages/derived_schema_list.html', {
        'task_name': task.name,
        'list_of_derived_schemas': derived_schemas,
    })

def showDerivedSchema(request, task_id, schema_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    schema = MappingInfo.objects.filter(id=schema_id, task=task)[0]

    schema_info = MappingInfo.objects.filter(id=schema_id).values()[0]
    mapping_pairs = generateListString(MappingInfoFromTo.objects.filter(mapping_info=schema))
    return render(request, 'pages/derived_schema_select.html', {
        'task_name': task.name,
        'schema_name': schema.derived_schema_name,
        'schema_info': schema_info,
        'mapping_pairs': mapping_pairs,
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
            # schema.task = task
            schema.save()

            return redirect('list derived schemas', task_id=task_id)

    else:
        form = CreateMappingInfo()
    
    return render(request, 'pages/derived_schema_create.html', {
        'create_derived_schema_form': form
    })

"""
view functions for mapping pairs
"""
def listMappingPairs(request, task_id, schema_id):
    """
    docstring
    """
    task = Task.objects.filter(id=task_id)[0]
    derived_schema = MappingInfo.objects.filter(id=schema_id, task=task)[0]

    mapping_pairs = generateListString(MappingInfoFromTo.objects.filter(mapping_info=derived_schema))
    return render(request, 'pages/mapping_pair_list.html', {
        'task_name': task.name,
        'schema_name': derived_schema.derived_schema_name,
        'list_of_mapping_pairs': mapping_pairs,
    })

def createMappingPair(request, task_id, schema_id):
    """
    docstring
    """
    form = None
    task = Task.objects.filter(id=task_id)[0]
    derived_schema = MappingInfo.objects.filter(id=schema_id, task=task)[0]

    mapping_pairs = generateListString(MappingInfoFromTo.objects.filter(mapping_info=derived_schema))

    mapping_pair = None
    if request.method == 'POST':
        form = CreateMappingInfoFromTo(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            mapping_pair = form.save(derived_schema)
            # schema.task = task
            mapping_pair.save()

            return redirect('create mapping pair', task_id=task_id, schema_id=schema_id)

    else:
        form = CreateMappingInfoFromTo()
    
    return render(request, 'pages/mapping_pair_create.html', {
        'create_mapping_pair_form': form,
        'list_of_mapping_pairs': mapping_pairs,
    })

    