from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Case
from datetime import date
class CaseModelTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username='a', password='p')
    def test_create_case(self):
        c = Case.objects.create(reporter=self.u, crime_type='Phishing', location='X', date_of_crime=date.today(), victim_name='V', description='D')
        self.assertTrue(c.tracking_id.startswith('CCMS-'))
