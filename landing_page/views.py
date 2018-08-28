from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import *
from .models import CurriculumVitae, Company, Education, Language, Other
from django.db.models.base import ObjectDoesNotExist
from dateutil import relativedelta
from rest_framework.response import Response
import datetime

User = get_user_model()
YES_NO = dict(Y='Yes', N='No')


# Get image path
def get_profile_pic_path(abs_path, user_id):
    profile_picture_dir = 'profiles/user_{user_id}'.format(user_id=user_id)
    profile_picture = str(abs_path).split('/')[-1]
    return '{dir}/{picture}'.format(dir=profile_picture_dir, picture=profile_picture)


# REST viewsets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CVViewSet(viewsets.ModelViewSet):
    queryset = CurriculumVitae.objects.all()
    serializer_class = CVSerializer


class OtherViewSet(viewsets.ModelViewSet):
    queryset = Other.objects.all()
    serializer_class = OtherSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

# REST viewsets


# Create your views here.
def index(request):
    current_user = User.objects.get(username='admin')
    try:
        user_info = CurriculumVitae.objects.get(person_id=current_user.id)
        serializer = CVSerializer(user_info, many=True)
    except ObjectDoesNotExist:
        return redirect('admin/login')

    age = datetime.datetime.now().year - current_user.birthday.year
    legit_phone = '7{}{}{}{}'.format(str(user_info.phone)[2:5],
                                     str(user_info.phone)[5:8],
                                     str(user_info.phone)[8:10],
                                     str(user_info.phone)[10:12]
                                     )
    phone = '+7 {} {} {} {}'.format(str(user_info.phone)[2:5],
                                    str(user_info.phone)[5:8],
                                    str(user_info.phone)[8:10],
                                    str(user_info.phone)[10:12]
                                    )
    information = dict(
        firstname=current_user.first_name,
        lastname=current_user.last_name,
        phone=phone,
        legit_phone=legit_phone,
        email=current_user.email,
        age=age,
        address=user_info.address,
        freelance=user_info.freelance,
        on_vacation=user_info.on_vacation,
        vacation_till=user_info.vacation_till,
        profile=get_profile_pic_path(user_info.profile, current_user.id),
        socials=dict(
            facebook=user_info.facebook,
            twitter=user_info.twitter,
            linkedin=user_info.linkedin,
            skype=user_info.skype,
        )
    )
    return render(request, 'landing_page/index/index.html', {
        'firstname': information['firstname'],
        'lastname': information['lastname'],
        'phone': information['phone'],
        'legit_phone': information['legit_phone'],
        'email': information['email'],
        'age': information['age'],
        'address': information['address'],
        'freelance': YES_NO[information['freelance']],
        'on_vacation': YES_NO[information['on_vacation']],
        'vacation_till': information['vacation_till'],
        'profile_picture': information['profile'],
        'skype': information['socials']['skype'],
        'linkedin': information['socials']['linkedin'],
        'twitter': information['socials']['twitter'],
        'facebook': information['socials']['facebook'],
    })


def resume(request):
    current_user = User.objects.get(username='admin')
    exp_list = list()
    cv = CurriculumVitae.objects.get(person_id=current_user.id)
    for i in Company.objects.filter(person_id=current_user.id):
        exp_list.append([i.company_name,
                         i.position,
                         abs(relativedelta.relativedelta(i.experience_from, i.experience_to).years),
                         abs(relativedelta.relativedelta(i.experience_from, i.experience_to).months),
                         'http://{}'.format(i.url),
                         i.about,
                         i.experience_from,
                         i.experience_to
                         ])
    edu_list = list()
    for i in Education.objects.filter(person_id=current_user.id):
        edu_list.append(
            [
                i.higher_education_institution,
                i.status,
                i.finished,
            ]
        )
    lang_list = list()
    for i in Language.objects.filter(person_id=current_user.id):
        lang_list.append(
            [
                i.name,
                i.level,
                i.describe,
            ]
        )
    other_list = list()
    for i in Other.objects.filter(person_id=current_user.id):
        other_list.append(
            [
                i.citizenship,
                i.permissions,
                i.travel_to_work,
            ]
        )
    # other_list = list(zip(*other_list))
    return render(request, 'landing_page/resume/resume.html', {
        'experience': exp_list,
        'key_skills': cv.key_skills,
        'about_me': cv.about_me,
        'edu_list': edu_list,
        'lang_list': lang_list,
        'other': other_list,
    }
                  )


def portfolio(request):
    return render(request, 'landing_page/portfolio/portfolio.html')


def contact(request):
    return render (request, 'landing_page/contact/contact.html')