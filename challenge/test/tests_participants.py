from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from challenge.models import Participant
from rest_framework import status
from django.test import TestCase
from challenge.serializer import ParticipantSerializer

##Unit Tests
class ParticipantSerializerTestCase(TestCase):
    
    def setUp(self):
        self.participant = Participant(
            first_name='Natalia', 
            last_name='Marques', 
            id_no="12260854745", 
            date_birth="1997-12-28", 
            gender="F", 
            country="Italia"
        )
        self.serializer = ParticipantSerializer(instance=self.participant)
    
    def test_verify_serialized_fields(self):
        """Test that verifies the fields that are being serialized"""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'first_name', 'last_name', 'id_no', 'date_birth', 'gender', 'country']))
    
    def test_verify_content_serializer_field(self):
        """Test that verifies the content of the serialized fields"""
        data = self.serializer.data
        self.assertEqual(data['first_name'], self.participant.first_name)
        self.assertEqual(data['last_name'], self.participant.last_name)
        self.assertEqual(data['id_no'], self.participant.id_no)
        self.assertEqual(data['date_birth'], self.participant.date_birth)
        self.assertEqual(data['gender'], self.participant.gender)
        self.assertEqual(data['country'], self.participant.country)


##Integration Tests
class ParticipantListTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('participants')
        self.participant = Participant.objects.create(
            first_name='Natalia', last_name='Marques', id_no="12260854745", date_birth="1997-12-28", gender="F", country="Italia"
        )

    def test_req_get_list_participants(self):
        """Test that verifies the GET request from the list of participants"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_req_post_create_participant(self):
        """Test that verifies the POST request of participant"""
        data = {
            'first_name':'Solange',
            'last_name':'Nunes',
            'id_no':'17997100155',
            'date_birth':'1950-08-10',
            'gender':'F',
            'country':'Brazil'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ParticipantActionsTestCase(APITestCase):

    fixtures = ['initial_participants']

    def test_req_get_one_participant(self):
        """Test that verifies the GET request of a participant"""
        response = self.client.get('/participants/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_req_put_att_participant(self):
        """Test that verifies the PUT request of a participant"""
        data = {
            "first_name": "Erikyny",
            "last_name": "Marcianin",
            "id_no": "55",
            "date_birth": "1997-03-11",
            "gender": "F",
            "country": "Italy"
        }
        response = self.client.put('/participants/1', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_req_delete_participant(self):
        """Test that verifies the DELETE request of a participant"""
        response = self.client.delete('/participants/1')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    