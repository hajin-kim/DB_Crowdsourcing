from django.contrib import admin
from .models import Account, Task, Participation, ParsedFile, SchemaAttribute, MappingInfo, MappingInfoFromTo

# Register your models here.
admin.site.register(Account)
admin.site.register(Task)
admin.site.register(Participation)
admin.site.register(ParsedFile)
# admin.site.register(Schema)
admin.site.register(SchemaAttribute)
admin.site.register(MappingInfo)
admin.site.register(MappingInfoFromTo)
