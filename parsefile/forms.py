from django import forms

from basicdb.models import Task, MappingInfo, OriginFile

class SchemaChoiceForm(forms.ModelForm):
    """
    docstring
    """
    task = Task
    mappingInfo = MappingInfo

class UploadForm(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = OriginFile
        # fields = {'name', 'data'}
        fields = {'derived_schema', 'file_original'}

    def save(self, commit=True):
        self.instance = OriginFile(**self.cleaned_data)
        
        if commit:
            self.instance.save()
            # self.instance.name = self.instance.file_original.name
            # self.instance.save()
        return self.instance


