import os
from datetime import datetime
import pandas as pd

from django.shortcuts import render, redirect
from django.conf import settings

from .models import OriginFile
from .forms import UploadForm

from basicdb.models import Account, Task, ParsedFile, MappingInfo

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
        'files': str(list(OriginFile.objects.values())),
        'files_parsed': str(list(ParsedFile.objects.values())),
    })

def uploadFile(request):
    """
    docstring
    """
    form = None
    saved_original_file = None
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            saved_original_file = form.save()
    else:
        form = UploadForm()

    if saved_original_file:
        # TODO: 이 부분 구현해야 합니다:
        task_name = "test_task"
        schema_name = "test_schema"
        submitter_id = "test_id"
        grader_id = "test_id"

        # print(saved_original_file.get_absolute_path(), "###")
        df = pd.read_csv(saved_original_file.get_absolute_path())

        # { 파싱전: 파싱후 }
        mapping_info = { i.original_column_name: i.parsing_column_name for i in MappingInfo.objects.filter(
            task=Task.objects.filter(name=task_name)[0], 
            original_schema_name=schema_name
            ) }
        for key in df.columns:
            if key in mapping_info.keys():
                df.rename(columns = {key: mapping_info[key]}, inplace = True)
            else:
                df.drop([key], axis='columns', inplace=True)

        parsed_file_path = os.path.join(settings.MEDIA_ROOT, str(saved_original_file).replace('data_original/', 'data_parsed/'))
        # print(df)
        df.to_csv(parsed_file_path, index=False)
        # print(df)

        # print(df.isnull().sum()/(len(df)*len(df.columns)), "###")
        parsed_file = ParsedFile(
            task=Task.objects.filter(name=task_name)[0],
            submitter=Account.objects.filter(acc_id=submitter_id)[0],
            grader=Account.objects.filter(acc_id=grader_id)[0],
            submit_count=1,
            start_date=datetime.now(),
            end_date=datetime.now(),
            total_tuple=len(df),
            duplicated_tuple=len(df)-len(df.drop_duplicates()),
            null_ratio=df.isnull().sum().sum()/(len(df)*len(df.columns)),
            grading_score=3,
            pass_state=True,
            grading_end_date=datetime.now(),
        )
        # print(df)
        parsed_file.file_original = str(saved_original_file)
        parsed_file.file_parsed = str(saved_original_file).replace('data_original/', 'data_parsed/')
        parsed_file.save()
        # TODO: data too long error
        # select @@global.sql_mode;  # SQL 설정 보기
        # remove: "STRICT_TRANS_TABLES"
        # set @@global.sql_mode="ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION";
        return redirect('fileList')





    return render(request, 'pages/upload.html', {
        'form': form
    })