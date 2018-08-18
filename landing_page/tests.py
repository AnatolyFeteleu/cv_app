from django.test import TestCase
from .models import Education, Creator
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

# Create your tests here.
class EducationestCase (TestCase):
    def setUp(self):
        Creator.objects.create(username="anatoly", email="anatoly@gmail.com", password="qwerty12345")
        Education.objects.create(person=User.objects.get(username="anatoly"), higher_education_institution="VKIEM", status="Get profile education", finished="2016-07-01")

    def test_finished_education(self):
        queryset = User.objects.get(username="anatoly")
        education = Education.objects.get(higher_education_institution="VKIEM", person=queryset)
        self.assertEqual(education.finished, datetime.date(2016, 7, 1))
        self.assertEqual(education.person.username, 'anatoly')
