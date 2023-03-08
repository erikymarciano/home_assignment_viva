from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from challenge.models import Team, Participant
from rest_framework import status
from django.test import TestCase
from challenge.serializer import TeamSerializer

##Unit Tests
class TeamSerializerTestCase(TestCase):
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Outback', 
            representative_name='Scorpion Spider', 
            country="Australia"
        )
        self.serializer = TeamSerializer(instance=self.team)
    
    def test_verify_serialized_fields(self):
        """Test that verifies the fields that are being serialized"""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'representative_name', 'country', 'member']))
    
    def test_verify_content_serializer_field(self):
        """Test that verifies the content of the serialized fields"""
        data = self.serializer.data
        self.assertEqual(data['name'], self.team.name)
        self.assertEqual(data['representative_name'], self.team.representative_name)
        self.assertEqual(data['country'], self.team.country)


##Integration Tests
class TeamListTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('teams')
        self.team = Team.objects.create(
            name='Mugiwaras', representative_name='Luffy', country="Japan"
        )

    def test_req_get_list_teams(self):
        """Test that verifies the GET request from the list of teams"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_req_post_create_participant(self):
        """Test that verifies the POST request of team"""
        data = {
            'name':'Tequila Group',
            'representative_name':'Chaves',
            'country':'Mexico'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TeamActionsTestCase(APITestCase):

    fixtures = ['initial_teams']

    def test_req_get_one_team(self):
        """Test that verifies the GET request of a team"""
        response = self.client.get('/teams/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_req_put_att_team(self):
        """Test that verifies the PUT request of a team"""
        data = {
            "name": "Hola Amigos",
            "representative_name": "Ze Carioca",
            "country": "Mexico"
        }
        response = self.client.put('/teams/1', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_req_delete_team(self):
        """Test that verifies the DELETE request of a team"""
        response = self.client.delete('/teams/1')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

class TeamMembersActionsTestCase(APITestCase):

    fixtures = ['initial_teams', 'initial_participants']

    def test_exist_data(self):
        teams = Team.objects.all()
        people = Participant.objects.all()

        self.assertEqual(teams[0].country, 'Brazil')
        self.assertEqual(people[0].country, 'Brazil')
        self.assertEqual(teams[0].id, 1)
        self.assertEqual(people[0].id, 1)

    def test_req_put_add_member(self):
        """Test that verifies the POST request to add a team member"""
        response = self.client.put('/teams/1/members/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_req_delete_remove_member(self):
        """Test that verifies the DELETE request to delete a team member"""
        self.client.put('/teams/1/members/1')
        response = self.client.delete('/teams/1/members/1')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)