from selenium import webdriver
from django.contrib.auth import get_user_model
from landing_page.models import *


class ConditionResumeTestCase:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.user = get_user_model()
        self.resume = None
        self.pdf_file = '/path/to/pdf/file.pdf'
        self.person = 'admin'

    def setup(self):
        if CurriculumVitae.objects.get(person=self.user.objects.get(username=self.person)):
            self.resume = CurriculumVitae.objects.get(person=self.user.objects.get(username=self.person)).resume
        else:
            CurriculumVitae.objects.create(
                person=self.user.objects.get(username=self.person),
                address='Krasnodar',
                phone='+79928867286',
                resume=self.pdf_file
            )
            self.resume = CurriculumVitae.objects.get(person=self.user.objects.get(username=self.person)).resume

    def check(self):
        self.driver.get('http://127.0.0.1:8000/')
        try:
            find = self.driver.find_elements_by_css_selector('div button')
            assert find
            return True
        except AssertionError:
            return False
        finally:
            self.driver.close()
            CurriculumVitae.objects.get(person=self.user.objects.get(username=self.person)).delete()
