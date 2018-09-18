from django.test import TestCase, Client, LiveServerTestCase
from .models import Education, Creator, CurriculumVitae
from django.contrib.auth import get_user_model
from selenium import webdriver

import datetime

User = get_user_model()


# Create your tests here.
class EducationTestCase(TestCase):
    def setUp(self):
        Creator.objects.create(
            username="anatoly",
            email="anatoly@gmail.com",
            password="qwerty12345"
        )
        Education.objects.create(
            person=User.objects.get(username="anatoly"),
            higher_education_institution="VKIEM",
            status="Get profile education",
            finished="2016-07-01"
        )

    def test_finished_education(self):
        user = User.objects.get(username="anatoly")
        education = Education.objects.get(person=user, higher_education_institution="VKIEM")
        self.assertEqual(education.finished, datetime.date(2016, 7, 1))
        self.assertEqual(education.person.username, 'anatoly')


class ConnectionTestCase(TestCase):
    def setUp(self):
        Creator.objects.create(username="anatoly", email="anatoly@gmail.com", password="qwerty12345")

    def test_scenario(self):
        client = Client()
        get = client.get('/admin/login/')
        post = client.post('/admin/login/', {'username': 'anatoly', 'password': 'qwerty12345'})
        self.assertEqual(str(get).split(' ')[1][:-1], 'status_code=200')
        self.assertEqual(str(post).split(' ')[1][:-1], 'status_code=200')


class ConditionTestCase(TestCase):
    def __init__(self):
        self.pdf_file = '/path/to/pdf/file.pdf'

    def setUp(self):
        Creator.objects.create(username="anatoly", email="anatoly@gmail.com", password="qwerty12345")
        CurriculumVitae.objects.create(
            person=User.objects.get(username='anatoly'),
            address='Krasnodar',
            phone='+79928867286',
            resume=self.pdf_file
        )

    def check(self):
        self.assertEqual(
            CurriculumVitae.objects.get(person=User.objects.get(username='anatoly')).resume,
            self.pdf_file)


class ConditionResumeTestCase(LiveServerTestCase):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.user = get_user_model()
        self.resume = None
        self.pdf_file = '/path/to/pdf/file.pdf'
        self.person = 'anatoly'

    def setUp(self):
        Creator.objects.create(username=self.person, email="anatoly@gmail.com", password="qwerty12345")
        CurriculumVitae.objects.create(
            person=User.objects.get(username=self.person),
            address='Krasnodar',
            phone='+79928867286',
            resume=self.pdf_file
        )
        self.resume = CurriculumVitae.objects.get(person=self.user.objects.get(username=self.person)).resume
        super(ConditionResumeTestCase, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ConditionResumeTestCase, self).tearDown()

    def check(self):
        self.driver.get('http://127.0.0.1:8000/')
        find = self.driver.find_elements_by_css_selector('div button')
        self.assertEqual(find, 'test')
