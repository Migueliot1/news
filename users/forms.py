from django.forms import ModelForm, TextInput, Textarea
from django import forms
from .models import Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    '''
    Form for signing up on login/register page.
    
    Consists of username, email, password and confirm password areas.
    '''

    username = forms.CharField(widget=(forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Username'})))
    email = forms.CharField(widget=(forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Email'})))
    password1=forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'login__input', 'placeholder': 'Password'})))
    password2=forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'login__input', 'placeholder': 'Confirm Password'})))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AnswerForm(ModelForm):
    '''
    Form for saving comment's answer.

    Consists of comment body and id of answered comment.
    '''

    class Meta:
        model = Answer
        fields = ['comment_body', 'answer_to']

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        self.fields['comment_body'].widget = Textarea(attrs={
            'id': 'formInput#textarea',
            'class': 'input--textarea_answer',
            'name': 'answer',
            'placeholder': 'Write your comment here...'})
