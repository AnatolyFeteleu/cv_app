from django.contrib.auth import get_user_model
from .models import CurriculumVitae, Other, Language, Company, Education
from rest_framework import serializers, fields

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url',
                  'username',
                  'first_name',
                  'last_name',
                  'birthday',
                  )


class CVSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = (
            'person',
            'freelance',
            'on_vacation',
            'vacation_till',
            'profile',
            'address',
            'phone',
            'facebook',
            'linkedin',
            'skype',
            'twitter',
            'key_skills',
            'about_me',
        )


class OtherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Other
        fields = (
            'person',
            'citizenship',
            'permissions',
            'travel_to_work',
        )


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = (
            'person',
            'name',
            'level',
            'describe',
        )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'person',
            'company_name',
            'about',
            'url',
            'experience_from',
            'experience_to',
        )


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'person',
            'higher_education_institution',
            'status',
            'finished',
        )
