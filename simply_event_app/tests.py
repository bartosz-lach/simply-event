from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from simply_event_app.forms import EventForm
from simply_event_app.models import Event


class EventTests(TestCase):

    def setUp(self) -> None:
        user1 = User.objects.create_user('jack', 'jack@test.com', 'password')
        user2 = User.objects.create_user('tom', 'tom@test.com', 'password')
        Event.objects.bulk_create([
            Event(name='My Birthday',
                  description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sodales ultricies '
                              'tortor quis vestibulum. Aenean pharetra augue vitae libero commodo, a suscipit urna '
                              'mollis. Vivamus facilisis ipsum vitae eros sodales, eu facilisis nisi sagittis. '
                              'Vivamus nisl nisi, vehicula sit amet mauris at, aliquam sollicitudin sem. Cras dapibu',
                  location='Grand Hotel London',
                  start_date=datetime(day=1, month=1, year=2020, hour=10, minute=20),
                  owner=user1,
                  is_public=True),
            Event(name='Party',
                  description='ipit urna mollis. Vivamus facilisis ipsum vitae eros sodales, eu facilisis nisi '
                              'sagittis. Vivamus nisl nisi, vehicula sit amet mauris at, aliquam sollicitudin s',
                  location='Labamba bar',
                  start_date=datetime(day=10, month=5, year=2020, hour=11, minute=30),
                  end_date=datetime(day=10, month=5, year=2020, hour=14, minute=30),
                  owner=user2,
                  is_public=False)
        ])

    def test_event_list_view(self):
        url = reverse('simply_event_app:event_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Birthday')
        self.assertNotContains(response, 'Party')

    def test_event_detail_view(self):
        url = reverse('simply_event_app:event_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Birthday')

    def test_owner_event_list_view(self):
        self.client.login(username='jack', password='password')
        url = reverse('simply_event_app:owner_event_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Birthday')
        self.assertNotContains(response, 'Party')

    def test_event_create_view(self):
        self.client.login(username='jack', password='password')
        url = reverse('simply_event_app:event_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_form(self):
        data = {
            'name': 'Party',
            'description': 'ipit urna mollis. Vivamus facilisis ipsum vitae eros sodales, eu facilisis nisi '
                           'sagittis. Vivamus nisl nisi, vehicula sit amet mauris at, aliquam sollicitudin s',
            'location': 'Labamba bar',
            'start_date': '05/10/2020 11:30',
            'end_date': '05/10/2020 14:30',
            'owner': 'tom',
            'is_public': False
        }
        form = EventForm(data)
        self.assertTrue(form.is_valid())
