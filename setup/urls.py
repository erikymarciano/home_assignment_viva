"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from challenge.views import CreateCompetitionLog, TeamActions, ParticipantList, TeamList, TeamMembersActions, ParticipantActions, ListCompetitionLogs, ListCompetitionLogsFiltered

urlpatterns = [
    path('admin/', admin.site.urls),
    path('participants/', ParticipantList.as_view(), name='participants'),
    path('participants/<int:id>/', ParticipantActions.as_view()),
    path('teams/', TeamList.as_view()),
    path('teams/<int:id>/', TeamActions.as_view()),
    path('teams/<int:t_id>/members/<int:m_id>/', TeamMembersActions.as_view()),
    path('results/<int:year>/', ListCompetitionLogs.as_view()),
    path('results/<int:year>/<str:instance>/', ListCompetitionLogsFiltered.as_view()),
    path('results/', CreateCompetitionLog.as_view()),
]
