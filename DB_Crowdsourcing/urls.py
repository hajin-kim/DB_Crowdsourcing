"""DB_Crowdsourcing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings

from basicdb import views as basicdbViews
from parsefile import views as fileuploadViews
from createtask import views as createtaskViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', basicdbViews.printAccount),

    path('', fileuploadViews.index, name='index'),
    path('upload/', fileuploadViews.uploadFile, name='uploadFile'),
    path('list/', fileuploadViews.fileList, name='fileList'),
    path('create_task/', createtaskViews.createTask, name='createTask'),

]

# if settings.DEBUG:
#     urlpatterns.append(
#         static(
#             settings.MEDIA_URL,
#             settings.MEDIA_ROOT
#         )
#     )


