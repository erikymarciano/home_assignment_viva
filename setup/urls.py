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
from rest_framework import routers, permissions
from rest_framework.urlpatterns import format_suffix_patterns
from challenge.views import CreateCompetitionLog, TeamActions, ParticipantList, TeamList, CompetitionList, CompetitionActions, TeamMembersActions, ParticipantActions, ListCompetitionLogs, ListCompetitionLogsFiltered
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Viva Challenge",
      default_version='v1',
      description="Take home assignment for Viva selective process",
      contact=openapi.Contact(email="erikymarciano@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# router = routers.DefaultRouter()
# router.register('participants', ParticipantList, basename='participants')
# dentro de urlpatters colocar path('', include(router.urls))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('participants', ParticipantList.as_view(), name='participants'),
    path('participants/<int:id>', ParticipantActions.as_view()),
    path('teams', TeamList.as_view(), name='teams'),
    path('teams/<int:id>', TeamActions.as_view()),
    path('teams/<int:team_id>/members/<int:participant_id>', TeamMembersActions.as_view()),
    path('competitions', CompetitionList.as_view(), name='teams'),
    path('competitions/<int:id>', CompetitionActions.as_view()),
    path('competitions/<int:competition_id>/results/<int:team_id>', CreateCompetitionLog.as_view()),
    path('results/<int:year>', ListCompetitionLogs.as_view()),
    path('results/<int:year>/<str:instance>', ListCompetitionLogsFiltered.as_view()),    
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0)),
]
