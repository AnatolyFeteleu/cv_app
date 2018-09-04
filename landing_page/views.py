from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import *
from .models import CurriculumVitae, Company, Education, Language, Other
from django.db.models.base import ObjectDoesNotExist
from dateutil import relativedelta
from .forms import EmailForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages

import datetime
import requests


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
    directory = 'profiles/user_{user_id}'.format(user_id=user_id)
    file = str(abs_path).split('/')[-1]
    return '{directory}/{file}'.format(directory=directory, file=file)


# Page views

def index(request):
    try:
        current_user = User.objects.get(username='admin')
        user_info = CurriculumVitae.objects.get(person_id=current_user.id)
    except:
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
        profile=get_path(user_info.profile, current_user.id),
        pp_exists=bool(user_info.profile),
        resume=get_path(user_info.resume, current_user.id),
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
        'resume': information['resume']
    })


def resume(request):
    try:
        current_user = User.objects.get(username='admin')
    except:
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
    }
                  )


def portfolio(request):
    return render(request, 'landing_page/portfolio/portfolio.html')


def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = 'Django mailer - {}'.format(form.cleaned_data['subject'])
            text = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Django mailer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            </head>
            <body style="background-color: #f8f8f8; color: #333333; border-radius: 10px; padding: 50px">
                <div>
                    <h2 style='text-transform: uppercase; text-align: center;>{subject}</h2>
                    <p style="font-size: 16px">Message text:<br>"{text}"</p>
                    <br>
                    <p style="font-size: 16px">Contact email:<br>
                        <a style="color: #1a7fab; text-decoration: none;" href="mailto:{signature}">{signature}</a>
                    </p>
                    <br>
                    <hr style="overflow: visible; padding: 0;border: none; border-top: medium double #333333; color: #333333; text-align: center;">
                    <a style="color: #1a7fab; text-decoration: none; font-size: 16px" href="mailto:{signature}">Click to reply</a>
                </div>
            </body>
            </html>
            """
            message = text.format(
                subject=form.cleaned_data['subject'],
                text=form.cleaned_data['text_field'],
                signature=form.cleaned_data['email_field']
                )
            recipient_list = settings.DEFAULT_EMAIL

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
    return render(request, 'landing_page/contact/contact.html', {'form': form})


def thanks(request):
    return render(request, 'landing_page/contact/success/index.html')