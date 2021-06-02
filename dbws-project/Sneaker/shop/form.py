from django import forms
from django.forms import widgets
class LoginForm(forms.Form):# Select login identity
    utype = {
        ('b', 'buyer'),
        ('s', 'seller')
    }
    username = forms.CharField(label = 'Username', max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label= 'Password', max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='Usertype', choices=utype,widget=widgets.RadioSelect)

class RegisterForm(forms.Form):# Select register identity
    utype={
        ('s', 'seller'),
        ('b','buyer')
    }
    username = forms.CharField(label = 'Username', max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1=forms.CharField(label='Password',max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    address=forms.CharField(label='Address',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    type=forms.ChoiceField(label='Usertype',choices=utype,widget=widgets.RadioSelect)

class PasswordForm(forms.Form):#Enter the password twice to confirm it.
    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
