from django import forms
import re


class EmailForm(forms.Form):
    email_field = forms.EmailField(error_messages={'required': 'Please provide your email address.'},
                                   label='Enter email here',
                                   widget=forms.EmailInput(attrs={'class': 'contact_email_field form-control',
                                                                  'id': 'email'}))
    subject = forms.CharField(error_messages={'required': 'Please write subject of your letter, like:  Django Frontend Dev. at Google etc.'},
                              label='Enter subject of letter here',
                              widget=forms.TextInput(attrs={'class': 'contact_subject_field form-control'}))
    text_field = forms.CharField(error_messages={'required': 'Please provide your covering letter.'},
                                 widget=forms.Textarea(attrs={'class': 'contact_text_field form-control'}),
                                 label='Enter your message')
