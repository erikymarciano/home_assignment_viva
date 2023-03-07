from django.contrib import admin
from challenge.models import Participant, Team, Instance, Competition, CompetitionLog

class Participants(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'id_no', 'date_birth', 'gender', 'country')
    list_display_links = ('id', 'first_name', 'id_no')
    search_fields = ('first_name', 'last_name', 'id_no')
    list_per_page = 20

admin.site.register(Participant, Participants)


class Teams(admin.ModelAdmin):
    list_display = ('id', 'name', 'representative_name', 'country')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'representative_name', 'country', 'member')
    list_per_page = 20

admin.site.register(Team, Teams)


class Instances(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Instance, Instances)


class Competitions(admin.ModelAdmin):
    list_display = ('id', 'instance', 'year')
    list_display_links = ('id',)
    search_fields = ('instance', 'year')

admin.site.register(Competition, Competitions)


class CompetitionLogs(admin.ModelAdmin):
    list_display = ('id', 'competition', 'team', 'score')
    list_display_links = ('id',)
    search_fields = ('competition', 'team')

admin.site.register(CompetitionLog, CompetitionLogs)