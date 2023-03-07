from rest_framework import serializers
from challenge.models import Participant, Team, CompetitionLog
from challenge.validators import *

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
    def validate(self, data):
        if not only_letters(data['first_name']):
            raise serializers.ValidationError({'first_name': "You cant use numbers in this field"})
        if not only_letters(data['last_name']):
            raise serializers.ValidationError({'last_name': "You cant use numbers in this field"})
        if not only_numbers(data['id_no']):
            raise serializers.ValidationError({'id_no': "You cant use letters in this field"})
        if not valid_gender(data['gender']):
            raise serializers.ValidationError({'gender': "You need to choose M or F in this field"})
        # if not only_letters(data['country']):
        #     raise serializers.ValidationError({'country': "You cant use numbers in this field"})
        return data


class TeamSerializer(serializers.ModelSerializer):
    member = ParticipantSerializer(read_only=True, many=True)
    class Meta:
        model = Team
        fields = '__all__'
    def validate(self, data):
        # if not only_letters(data['representative_name']):
        #     raise serializers.ValidationError({'representative_name': "You cant use numbers in this field"})
        # if not only_letters(data['country']):
        #     raise serializers.ValidationError({'country': "You cant use numbers in this field"})
        return data
        

class CompetitionLogSerializer(serializers.ModelSerializer):
    competition = serializers.SerializerMethodField()
    team = serializers.ReadOnlyField(source='team.name')

    def get_competition(self, obj):
        return f'{obj.competition.year} - {obj.competition.instance.name}'
    
    class Meta:
        model = CompetitionLog
        fields = ['competition', 'team', 'score']
