import os
from datetime import datetime
import pandas as pd

from django.shortcuts import render, redirect
from django.conf import settings

from .forms import SchemaChoiceForm, UploadForm

from basicdb.models import Account, Task, Participation, ParsedFile, SchemaAttribute, MappingInfo, MappingPair, OriginFile

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


# def getTaskAndSchema(request):
#     """
#     docstring
#     """
#     form = None
#     saved_original_file = None
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # form = form.save(commit=False) # 중복 DB save를 방지
#             saved_original_file = form.save()
#     else:
#         form = UploadForm()

#     if saved_original_file:
#         pass


def uploadFile(request):
    """
    docstring
    """
    form = None
    # schema_choice_form = None
    saved_original_file = None
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        # schema_choice_form = SchemaChoiceForm(request.POST, request.FILES)
        if form.is_valid():
            # form = form.save(commit=False) # 중복 DB save를 방지
            saved_original_file = form.save()
        # elif schema_choice_form.is_valid():

    else:
        form = UploadForm()
        # schema_choice_form = SchemaChoiceForm()


    if saved_original_file:
        # TODO: 이 부분 구현해야 합니다!
        # 각 릴레이션의 튜풀을 받아야 합니다.
        # 이런 식으로요:
        # task = Task.objects.filter(***)[0]
        # 아마 key 등을 이 함수의 파라미터를 통해 받아오는 방법 등을 택할 것 같네요.
        task_name = "test_task"
        submitter_pk = "test_id"
        grader_pk = "test_id"

        task = Task.objects.filter(name=task_name)[0]
        submitter = Account.objects.filter(id=submitter_pk)[0]
        grader = Account.objects.filter(id=grader_pk)[0]

        derived_schema = saved_original_file.derived_schema

        # print(saved_original_file.get_absolute_path(), "###")
        # load csv file from the server
        df = pd.read_csv(saved_original_file.get_absolute_path())

        # get DB tuples
        mapping_info = MappingInfo.objects.filter(
            task=task, 
            derived_schema_name=derived_schema
        )[0]

        # get parsing information into a dictionary
        # { 파싱전: 파싱후 }
        mapping_from_to = {
            i.parsing_column_name: i.schema_attribute.attr \
            for i in MappingPair.objects.filter(
                mapping_info=mapping_info
            )
        }

        # parse
        for key in df.columns:
            if key in mapping_from_to.keys():
                df.rename(columns = {key: mapping_from_to[key]}, inplace = True)
            else:
                df.drop([key], axis='columns', inplace=True)

        # save the parsed file
        parsed_file_path = os.path.join(settings.MEDIA_ROOT, str(saved_original_file).replace('data_original/', 'data_parsed/'))
        df.to_csv(parsed_file_path, index=False)

        # increment submit count of Participation tuple by 1
        participation = Participation.objects.filter(account=submitter, task=task)[0]
        participation.submit_count += 1
        participation.save()

        # make statistic
        # print(df.isnull().sum()/(len(df)*len(df.columns)), "###")
        parsed_file = ParsedFile(
            task=task,
            submitter=submitter,
            grader=grader,
            submit_count=participation.submit_count,
            start_date=datetime.now(),
            end_date=datetime.now(),
            total_tuple=len(df),
            duplicated_tuple=len(df)-len(df.drop_duplicates()),
            null_ratio=df.isnull().sum().sum()/(len(df)*len(df.columns)),
            grading_score=3,
            pass_state=True,
            grading_end_date=datetime.now(),
        )

        # save the parsed file
        # print(df)
        parsed_file.file_original = str(saved_original_file)
        parsed_file.file_parsed = str(saved_original_file).replace('data_original/', 'data_parsed/')
        parsed_file.save()

        # TODO: data too long error
        # select @@global.sql_mode;  # SQL 설정 보기
        # remove: "STRICT_TRANS_TABLES"
        # set @@global.sql_mode="ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION";

        return redirect('list files')

    return render(request, 'pages/upload.html', {
        'file_upload_form': form
    })