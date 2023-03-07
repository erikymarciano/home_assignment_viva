from django.shortcuts import render
from challenge.models import Participant, Team, Instance, Competition, CompetitionLog
from challenge.serializer import CompetitionLogSerializer, ParticipantSerializer, TeamSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import status
import json


class ParticipantList(APIView):
    """ List all participants or create a new participant """    
    def get(self, request):        
        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)                
        return Response(serializer.data, 200)       
    
    def post(self, request):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParticipantActions(APIView):
    def get_object(self, id):
        try:
            return Participant.objects.get(id=id)
        except Participant.DoesNotExist:
            raise Http404

    def get(self, request, id):
        participant = self.get_object(id)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)
    
    def put(self, request, id):
        participant = self.get_object(id)
        serializer = ParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        participant = self.get_object(id)
        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamList(APIView):    
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamActions(APIView):
    def get_object(self, id):
        try:
            return Team.objects.get(id=id)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, id):
        team = self.get_object(id)
        serializer = TeamSerializer(team)
        return Response(serializer.data)    
    
    def put(self, request, id):
        team = self.get_object(id)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        team = self.get_object(id)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class TeamMembersActions(APIView):
    def get_team(self, id):
        try:
            return Team.objects.get(id=id)
        except Team.DoesNotExist:
            raise Http404
    
    def get_member(self, id):
        try:
            return Participant.objects.get(id=id)
        except Participant.DoesNotExist:
            raise Http404
        
    def put(self, request, t_id, m_id):
        team = self.get_team(t_id)
        member = self.get_member(m_id)
        if member in team.member.all():
            return Response(
                    {
                        "message": "this member is already on this team"
                    }, 400
                )
        else:
            if team.country == member.country:
                if team.member.all().count() < 3:
                    team.member.add(member)
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                    {
                        "message": "this team already has the maximum number of members"
                    }, 400
                    )
            else:
                return Response(
                    {
                        "message": "This member is not from the same country as the team"
                    }, 400
                    )
    
    def delete(self, request, t_id, m_id):
        team = self.get_team(t_id)
        member = self.get_member(m_id)
        if member in team.member.all():
            team.member.remove(member)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                    {
                        "message": "This member is not from this team"
                    }, 400
                )


class CreateCompetitionLog(APIView):
    def post(self, request):
        required_instances_map = {
            'International': 'Regional',
            'Regional': 'National',
            'National': 'Local',
            'Local': None
        }
        data = json.loads(str(request.body, encoding="utf-8"))
        try:            
            team = Team.objects.get(id=data["team_id"])
            competition = Competition.objects.get(id=data["competition_id"])
            required_instance = required_instances_map[competition.instance.name]
            if required_instance is not None:
                required_competition_log = CompetitionLog.objects.get(team=team, competition=Competition.objects.get(year=competition.year, instance=Instance.objects.get(name=required_instance)))
                if required_competition_log.score > 65:
                    CompetitionLog.create(
                        competition=competition,
                        team=team,
                        score=data["score"]
                    )
                    return Response(
                    {
                        "message": "Competition log successfully created"
                    }, 200
                    )
                else:
                    return Response(
                    {
                        "message": "This team does not have a score greater than 65 in the competition of the previous instance"
                    }, 400
                    )
        except Team.DoesNotExist:
            return Response(
                {
                    "message": "Does not exist a team with this id."
                }, 404
            )
        except Competition.DoesNotExist:
            return Response(
                {
                    "message": "Does not exist a competition with this id."
                }, 404
            )
        except CompetitionLog.DoesNotExist:
            return Response(
                {
                    "message": "Does not have a log that references the competition of the previous instance"
                }, 404
            )


class ListCompetitionLogs(generics.ListAPIView):
    def get_queryset(self):
        year = self.kwargs['year']
        queryset = CompetitionLog.objects.filter(competition__year=year).order_by('competition__instance', '-score')        
        return queryset
    serializer_class = CompetitionLogSerializer


class ListCompetitionLogsFiltered(generics.ListAPIView):
    def get_queryset(self):
        year = self.kwargs['year']
        instance = self.kwargs['instance'].capitalize()
        queryset = CompetitionLog.objects.filter(competition__year=year, competition__instance__name=instance).order_by('-score')
        return queryset
    serializer_class = CompetitionLogSerializer