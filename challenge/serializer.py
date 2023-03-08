from rest_framework import serializers
from challenge.models import Participant, Team, Competition, CompetitionLog, Instance
from challenge.validators import *

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
    def validate(self, data):
        if not valid_idno(data['id_no']):
            raise serializers.ValidationError({'id_no': "You can only use numbers in this field"})
        if not valid_country(data['country']):
            raise serializers.ValidationError({'country': "You can only use letters and spaces in this field"})
        return data


class TeamSerializer(serializers.ModelSerializer):
    member = ParticipantSerializer(read_only=True, many=True)
    class Meta:
        model = Team
        fields = '__all__'
    def validate(self, data):
        if not valid_country(data['country']):
            raise serializers.ValidationError({'country': "You can only use letters and spaces in this field"})
        return data


class CompetitionLogSerializer(serializers.ModelSerializer):
    competition = serializers.SerializerMethodField()
    team = serializers.ReadOnlyField(source='team.name')

    def get_competition(self, obj):
        return f'{obj.competition.year} - {obj.competition.instance.name}'
    
    class Meta:
        model = CompetitionLog
        fields = ['competition', 'team', 'score']
    def validate(self, data):
        if not valid_score(data['score']):
            raise serializers.ValidationError({'score': "Você precisa escolher uma pontuação entre 0 e 100"})
        return data
        

class InstanceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Instance
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):
    instance = serializers.ReadOnlyField(source='instance.name')
    
    class Meta:
        model = Competition
        fields = ['id', 'instance', 'year']
