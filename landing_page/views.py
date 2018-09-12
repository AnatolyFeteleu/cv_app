from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from dateutil import relativedelta
from .forms import EmailForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages

import datetime
import requests
import os


User = get_user_model()
YES_NO = dict(Y='Yes', N='No')


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


# Get image path
def get_path(abs_path, user_id):
    if abs_path:
        filename = str(abs_path).split('/')[-1]
        directory = r'profiles/user_{id}/'.format(media_root=settings.MEDIA_ROOT, id=user_id, filename=filename)
        return '{directory}{file}'.format(directory=directory, file=filename).replace('\\', '/')
    else:
        return 0


# Get information from db about User
def get_user_info(username, model):
    try:
        user = User.objects.get(username=username)
        user_info = model.objects.get(person_id=user.id)
        age = datetime.datetime.now().year - user.birthday.year
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
            firstname=user.first_name,
            lastname=user.last_name,
            phone=phone,
            legit_phone=legit_phone,
            email=user.email,
            age=age,
            address=user_info.address,
            freelance=user_info.freelance,
            on_vacation=user_info.on_vacation,
            vacation_till=user_info.vacation_till,
            profile=get_path(user_info.profile, user.id),
            pp_exists=bool(user_info.profile),
            resume=get_path(user_info.resume, user.id),
            socials=dict(
                facebook=user_info.facebook,
                twitter=user_info.twitter,
                linkedin=user_info.linkedin,
                skype=user_info.skype,
            )
        )
        return information
    except ObjectDoesNotExist:
        return 0


# Page views

def index(request):
    if get_user_info('admin', CurriculumVitae):
        return render(request, 'landing_page/index/index.html', {
            'firstname': get_user_info('admin', CurriculumVitae)['firstname'],
            'lastname': get_user_info('admin', CurriculumVitae)['lastname'],
            'phone': get_user_info('admin', CurriculumVitae)['phone'],
            'legit_phone': get_user_info('admin', CurriculumVitae)['legit_phone'],
            'email': get_user_info('admin', CurriculumVitae)['email'],
            'age': get_user_info('admin', CurriculumVitae)['age'],
            'address': get_user_info('admin', CurriculumVitae)['address'],
            'freelance': YES_NO[get_user_info('admin', CurriculumVitae)['freelance']],
            'on_vacation': YES_NO[get_user_info('admin', CurriculumVitae)['on_vacation']],
            'vacation_till': get_user_info('admin', CurriculumVitae)['vacation_till'],
            'profile_picture': get_user_info('admin', CurriculumVitae)['profile'],
            'skype': get_user_info('admin', CurriculumVitae)['socials']['skype'],
            'linkedin': get_user_info('admin', CurriculumVitae)['socials']['linkedin'],
            'twitter': get_user_info('admin', CurriculumVitae)['socials']['twitter'],
            'facebook': get_user_info('admin', CurriculumVitae)['socials']['facebook'],
            'resume': get_user_info('admin', CurriculumVitae)['resume'],
            'pp_exists': get_user_info('admin', CurriculumVitae)['pp_exists'],
        })
    else:
        return redirect('admin/login')


def resume(request):
    try:
        current_user = User.objects.get(username='admin')
    except ObjectDoesNotExist:
        return redirect('admin/login')

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
        'skype': get_user_info('admin', CurriculumVitae)['socials']['skype'],
        'linkedin': get_user_info('admin', CurriculumVitae)['socials']['linkedin'],
        'twitter': get_user_info('admin', CurriculumVitae)['socials']['twitter'],
        'facebook': get_user_info('admin', CurriculumVitae)['socials']['facebook'],
    }
                  )


def portfolio(request):
    try:
        current_user = User.objects.get(username='admin')
    except ObjectDoesNotExist:
        return redirect('admin/login')

    projects = list()
    for i in Project.objects.filter(person_id=current_user.id):
        projects.append(
            [
                i.project_name,
                i.project_status,
                i.project_description,
                i.project_url,
                i.project_image
            ],
        )

    return render(request, 'landing_page/portfolio/portfolio.html', {
        'skype': get_user_info('admin', CurriculumVitae)['socials']['skype'],
        'linkedin': get_user_info('admin', CurriculumVitae)['socials']['linkedin'],
        'twitter': get_user_info('admin', CurriculumVitae)['socials']['twitter'],
        'facebook': get_user_info('admin', CurriculumVitae)['socials']['facebook'],
        'projects': projects,
    })


def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_list = settings.DEFAULT_EMAIL
            subject = 'Django mailer - {}'.format(form.cleaned_data['subject'])
            text = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            </head>
            <body style="background-color: #f8f8f8; color: #333333; border-radius: 10px; padding: 50px">
                <h1 style="text-transform: uppercase; text-align: center; text-decoration: underline; padding: 0;">{subject}</h1>
                <p style="font-size: 16px; font-style: italic;">Message text:<br>"<span style="font-style: normal;">{text}</span>"</p>
                <br>
                <p style="font-size: 16px; font-style: italic;">Contact email:<br>
                    <a style="color: #1a7fab; text-decoration: none; font-size: 16px; font-style: normal;" href="mailto:{signature}">{signature}</a>
                </p>
                <br>
                <hr style="overflow: visible; padding: 0;border: none; border-top: medium double #333333; color: #333333; text-align: center;">
                <a style="color: #1a7fab; text-decoration: none; font-size: 16px;" href="mailto:{signature}">Click to reply</a>
            </body>
            </html>
            """
            message = text.format(
                subject=form.cleaned_data['subject'],
                text=form.cleaned_data['text_field'],
                signature=form.cleaned_data['email_field']
                )
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                mail = EmailMessage(
                           subject,
                           message,
                           form.cleaned_data['email_field'],
                           [recipient_list, ],
                           reply_to=[form.cleaned_data['email_field'], ],
                           headers={'Message-ID': 'Django offers'},
                       )
                mail.content_subtype = "html"
                mail.send()
                return redirect('thanks')
            else:
                messages.error(request, result)
    else:
        form = EmailForm()
    return render(request, 'landing_page/contact/contact.html', {
        'form': form,
        'skype': get_user_info('admin', CurriculumVitae)['socials']['skype'],
        'linkedin': get_user_info('admin', CurriculumVitae)['socials']['linkedin'],
        'twitter': get_user_info('admin', CurriculumVitae)['socials']['twitter'],
        'facebook': get_user_info('admin', CurriculumVitae)['socials']['facebook'],
    })


def thanks(request):
    return render(request, 'landing_page/contact/success/index.html')
