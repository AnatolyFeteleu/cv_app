from django import forms


class EmailForm(forms.Form):
    email_field = forms.EmailField(label='Enter email here')
    text_field = forms.CharField(widget=forms.Textarea, label='Enter your message')



