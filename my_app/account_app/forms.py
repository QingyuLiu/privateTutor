from django import forms
from account_app.models import UserProfile as User
import re
from account_app.models import UserProfile

class RegistrationForm(forms.Form):
    identity_list = (
        (u'S', u'Student'),
        (u'T', u'Teacher'),
    )
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    username = forms.CharField(label='Username', )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    identity=forms.CharField(label='Identity', widget=forms.Select(choices=identity_list))



    # Use clean methods to define custom validation rules

    def clean(self):
        try:
             email = self.cleaned_data.get('email')
        except Exception as e:
            raise forms.ValidationError("enter a valid email address.")
        judge = UserProfile.objects.filter(email=email)
        if len(judge) > 0:
            raise forms.ValidationError(u"email already taken.")

        username = self.cleaned_data.get('username')


        judge1 = UserProfile.objects.filter(username=username)
        if len(judge1) > 0:
                raise forms.ValidationError("username already taken.")


        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("Password too short.")
        else:
            pattern1 = re.compile(r"\"?([A - Z]+@\w+\.\w+)\"?")
            pattern2 = re.compile(r"\"?([0 - 9] +@\w+\.\w+)\"?")

        password2 = self.cleaned_data.get('password2')
        if (password1 and password2 and password1 != password2):
            raise forms.ValidationError("Password mismatch.")


class LogForm(forms.Form):

    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean(self):
        try:
            email = self.cleaned_data.get('email')
        except Exception as e:
            raise forms.ValidationError("enter a valid email address.")

        password = self.cleaned_data.get('password')

class ModifyPassword(forms.Form):
    password3 = forms.CharField(label='oldPassword', widget=forms.PasswordInput)
    password4 = forms.CharField(label='newPassword1', widget=forms.PasswordInput)
    password5 = forms.CharField(label='newPassword2', widget=forms.PasswordInput)

    def clean(self):
        password4 = self.cleaned_data.get('newpassword1')


        if len(password4) < 6:
            raise forms.ValidationError("Password too short.")

        password5 = self.cleaned_data.get('newpassword2')
        if (password4 and password5 and password4!= password5):
            raise forms.ValidationError("Password mismatch.")

class ModifyEmail(forms.Form):

    newemail= forms.EmailField(label='newEmail', widget=forms.EmailInput)
    def clean(self):
        try:
            newemail = self.cleaned_data.get('newemail')
            print(newemail)
            judge = UserProfile.objects.filter(email=newemail)
            print(judge)
            if len(judge) > 0:
                raise forms.ValidationError(u"email already taken.")
        except Exception as e:
            raise forms.ValidationError("enter a valid email address.")







