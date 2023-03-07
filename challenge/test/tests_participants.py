from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from challenge.models import Participant
from rest_framework import status

class ParticipantsListTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('participants')
        self.participant_1 = Participant.objects.create(
            first_name='Natalia', last_name='Marques', id_no="12260854745", date_birth="1997-12-28", gender="F", country="Italia"
        )
        self.participant_2 = Participant.objects.create(
            first_name='Cristiane', last_name='Nunes', id_no="02334507776", date_birth="1973-06-11", gender="F", country="Italia"
        )

    def test_req_get_list_participants(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_req_post_create_participant(self):
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
    
    def test_req_put_att_participant(self):
        data = {
            'first_name':'Rebeca',
            'last_name':'Marciano',
            'id_no':'17997100155',
            'date_birth':'2010-16-11',
            'gender':'F',
            'country':'Brazil'
        }
        response = self.client.put('/participants/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_req_delete_participant(self):
        response = self.client.delete('/participants/1/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    