from django.shortcuts import render
from django.core.exceptions import ValidationError
from challenge.models import Participant, Team, Instance, Competition, CompetitionLog
from challenge.serializer import CompetitionLogSerializer, ParticipantSerializer, TeamSerializer, CompetitionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import NotFound
import json
from drf_yasg.utils import swagger_auto_schema


class ParticipantList(APIView):
    """ List all participants or create a new participant """
    def get(self, request):        
        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)                
        return Response(serializer.data, 200)       
    
    @swagger_auto_schema(request_body=ParticipantSerializer)
    def post(self, request, format=None):
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
    
    @swagger_auto_schema(request_body=ParticipantSerializer)
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
    
    @swagger_auto_schema(request_body=TeamSerializer)
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
    
    @swagger_auto_schema(request_body=TeamSerializer)
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
            raise NotFound(detail="Team not found", code=404)
    
    def get_member(self, id):
        try:
            return Participant.objects.get(id=id)
        except Participant.DoesNotExist:
            raise NotFound(detail="Participant not found", code=404)
        
    def put(self, request, team_id, participant_id):
        team = self.get_team(team_id)
        member = self.get_member(participant_id)
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
                    return Response(status=status.HTTP_200_OK)
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
    
    def delete(self, request, team_id, participant_id):
        team = self.get_team(team_id)
        member = self.get_member(participant_id)
        if member in team.member.all():
            team.member.remove(member)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                    {
                        "message": "This member is not from this team"
                    }, 400
                )


class CompetitionList(APIView):
    def get(self, request):        
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)                
        return Response(serializer.data, 200)       
    
    def post(self, request, format=None):
        data = json.loads(str(request.body, encoding="utf-8"))
        try:
            instance = Instance.objects.get(name=data["instance"].capitalize())
            if Competition.objects.filter(year=data["year"], instance=instance).exists():
                return Response(
                        {
                            "message": "There is already a competition in this instance in the year informed"
                        }, 400)
            else:
                competition = Competition(
                    instance=instance,
                    year=int(data["year"])
                )
                try:
                    competition.full_clean()
                    competition.save()
                    return Response(status=status.HTTP_201_CREATED)
                except ValidationError as e:
                    return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Instance.DoesNotExist:
            raise NotFound(detail="Instance not found", code=404)


class CompetitionActions(APIView):
    def get_object(self, id):
        try:
            return Competition.objects.get(id=id)
        except Competition.DoesNotExist:
            raise Http404

    def get(self, request, id):
        competition = self.get_object(id)
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data)
    
    def delete(self, request, id):
        competition = self.get_object(id)
        competition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCompetitionLog(APIView):
    def post(self, request, competition_id, team_id):
        required_instances_map = {
            'International': 'Regional',
            'Regional': 'National',
            'National': 'Local',
            'Local': None
        }
        data = json.loads(str(request.body, encoding="utf-8"))
        try:            
            team = Team.objects.get(id=team_id)
            competition = Competition.objects.get(id=competition_id)
            required_instance = required_instances_map[competition.instance.name]
            if required_instance is None:
                if CompetitionLog.objects.filter(team=team, competition=competition).exists():
                        return Response(
                        {
                            "message": "This team has participated of a competition in this instance this year"
                        }, 400
                        )
                else:
                    competition_log = CompetitionLog(
                        competition=competition,
                        team=team,
                        score=data["score"]
                    )
                    try:
                        competition_log.clean_fields()
                        competition_log.save()
                        return Response(status=status.HTTP_201_CREATED)
                    except ValidationError as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                required_competition_log = CompetitionLog.objects.get(team=team, competition=Competition.objects.get(year=competition.year, instance=Instance.objects.get(name=required_instance)))
                if required_competition_log.score > 65:
                    if CompetitionLog.objects.filter(team=team, competition=competition).exists():
                        return Response(
                        {
                            "message": "This team has participated of a competition in this instance this year"
                        }, 400
                        )
                    else:
                        competition_log = CompetitionLog(
                            competition=competition,
                            team=team,
                            score=data["score"]
                        )
                        try:
                            competition_log.full_clean()
                            competition_log.save()
                            return Response(status=status.HTTP_201_CREATED)
                        except ValidationError as e:
                            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
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