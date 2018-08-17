from django.db import models
from django.conf import settings
# Expand user model
from django.contrib.auth.models import AbstractUser
# Added support tel. numbers in fields model
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


def user_directory_path(instance, filename):
    return '{static}/profiles/user_{id}/{filename}'.format(static=settings.STATIC_PATH,
                                                           id=instance.id,
                                                           filename=filename,
                                                           )

# Create your models here.
class Creator(AbstractUser):
    # Common
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{firstname} {lastname} ({id})'.format(
            firstname=self.first_name,
            lastname=self.last_name,
            id=self.username
        )


class Education(models.Model):
    person = models.ForeignKey(Creator)
    higher_education_institution = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    finished = models.DateField()

    def __str__(self):
        return '{} ({})'.format(self.higher_education_institution, self.finished)


class Company(models.Model):
    person = models.ForeignKey(Creator)
    company_name = models.CharField(max_length=1000)
    about = models.TextField(max_length=1000)
    url = models.CharField(max_length=100, default='www.website.com')

    # Experience
    experience_from = models.DateField()
    experience_to = models.DateField()

    def __str__(self):
        return '{company}'.format(
            company=self.company_name,
        )


class Language(models.Model):
    person = models.ForeignKey(Creator)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    describe = models.TextField(blank=True)

    def __str__(self):
        return '{} ({})'.format(self.person, self.name)


class Other(models.Model):
    COUNTRIES = (
        ('Russia', ('Russia')),
        ('Ukraine', ('Ukraine')),
        ('Belarus', ('Belarus'))
    )
    TRAVEL = (
        ('Doesn\'t matter', ('Doesn\'t matter')),
        ('Up to one hour', ('Up to one hour')),
        ('Up to 90 minutes', ('Up to 90 minutes'))
    )
    person = models.ForeignKey(Creator)
    citizenship = models.CharField(max_length=20)
    permissions = MultiSelectField(choices=COUNTRIES, default='Russia')
    travel_to_work = MultiSelectField(choices=TRAVEL, default='Doesn\'t matter', max_choices=1)

    def __str__(self):
        return '{} {}'.format(self.person.first_name, self.person.last_name)


class CurriculumVitae(models.Model):
    Y, N = 'Y', 'N'
    YN_CHOICES = (
        (N, 'No'),
        (Y, 'Yes'),
    )
    person = models.ForeignKey(Creator, default='')
    freelance = models.CharField(choices=YN_CHOICES, default=N, max_length=3)
    on_vacation = models.CharField(choices=YN_CHOICES, default=N, max_length=3)
    vacation_till = models.DateField(null=True, blank=True)
    profile = models.FileField(null=True, upload_to=user_directory_path)
    address = models.CharField(null=True, max_length=1000)
    phone = PhoneNumberField()

    # Socials
    facebook = models.CharField(null=True, max_length=50)
    linkedin = models.CharField(null=True, max_length=50)
    skype = models.CharField(null=True, max_length=50)
    twitter = models.CharField(null=True, max_length=50)

    # Resume
    key_skills = models.TextField(blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return '{first_name} {last_name}'.format(
            first_name=self.person.first_name,
            last_name=self.person.last_name,
        )