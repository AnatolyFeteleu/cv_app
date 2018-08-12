from django.contrib.auth import get_user_model
from .models import CurriculumVitae
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url',
                  'username',
                  'email',
                  'birthday',
                  'address',
                  'phone',
                  'freelance',
                  'on_vacation',
                  'vacation_till',
                  'profile',
                  'facebook',
                  'linkedin',
                  'skype',
                  'twitter',
                  )


class CVSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = (
            "person",
            "freelance",
            "on_vacation",
            "vacation_till",
            "profile",
            "address",
            "phone",
            "facebook",
            "linkedin",
            "skype",
            "twitter",
            "key_skills",
            "about_me",
        )