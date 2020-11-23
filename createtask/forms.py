from django import forms

from basicdb.models import Task, MappingInfo


class CreateTask(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = Task
        # fields = {'name', 'data'}
        fields = {
            'name', 
            'minimal_upload_frequency', 
            'activation_state', 
            'description', 
            'original_data_description', 
        }

    def save(self, commit=True):
        self.instance = Task(**self.cleaned_data)
        
        if commit:
            self.instance.save()
            # self.instance.name = self.instance.file_original.name
            # self.instance.save()
        return self.instance
    
    
class CreateMappingInfo(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = MappingInfo
        # fields = {'name', 'data'}
        fields = {
            'derived_schema_name', 
        }

    def save(self, task, commit=True):
        self.instance = MappingInfo(**self.cleaned_data)
        self.instance.task = task
        
        if commit:
            self.instance.save()
            # self.instance.name = self.instance.file_original.name
            # self.instance.save()
        return self.instance



class UploadTaskAndSchema(forms.ModelForm):
    """
    docstring
    """
    name = Task.name.field
    minimal_upload_frequency = Task.minimal_upload_frequency.field
    activation_state = Task.activation_state.field
    description = Task.description.field
    original_data_description = Task.original_data_description.field

    

    # class Meta:
    #     model = Task
    #     # fields = {'name', 'data'}
    #     fields = {'name', 'minimal_upload_frequency', 'description', 'original_data_description'}

    # def save(self, commit=True):
    #     self.instance = OriginFile(**self.cleaned_data)
        
    #     if commit:
    #         self.instance.save()
    #         # self.instance.name = self.instance.file_original.name
    #         # self.instance.save()
    #     return self.instance


class UploadDerivedSchema(forms.ModelForm):
    """
    docstring
    """
    task = Task.name

    # from: 제출자가 제출할 파일의 컬럼 레이블
    # to: 실제 태스크가 받는 컬럼 레이블
    mapping_from_1 = forms.CharField()
    mapping_to_1 = forms.CharField()
    mapping_from_2 = forms.CharField()
    mapping_to_2 = forms.CharField()
    mapping_from_3 = forms.CharField()
    mapping_to_3 = forms.CharField()
    mapping_from_4 = forms.CharField()
    mapping_to_4 = forms.CharField()
    mapping_from_5 = forms.CharField()
    mapping_to_5 = forms.CharField()
    mapping_from_6 = forms.CharField()
    mapping_to_6 = forms.CharField()
    mapping_from_7 = forms.CharField()
    mapping_to_7 = forms.CharField()
    mapping_from_8 = forms.CharField()
    mapping_to_8 = forms.CharField()
    mapping_from_9 = forms.CharField()
    mapping_to_9 = forms.CharField()
    mapping_from_10 = forms.CharField()
    mapping_to_10 = forms.CharField()
