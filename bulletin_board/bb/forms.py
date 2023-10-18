from django.forms import ModelForm
from .models import Post
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models  import Group
from django.contrib.auth.models import User


class BasicSignupForm(SignupForm):
  def save(self, request):
    user = super(BasicSignupForm, self).save(request)
    basic_group = Group.objects.get_or_create(name='Common')[0]
    basic_group.user_set.add(user)
    return user

class SubscribeForm(forms.Form):
    email = forms.EmailField(initial="example@mail.ru")

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        print ("send email!")
        pass


class MessageCreateForm (ModelForm):
    
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'body', 'mainPic']
        widgets = {
          'author' : forms.Select(attrs={
            'class': 'form-control', 
          }),

          'category' : forms.SelectMultiple(attrs={
            'class': 'form-control', 
          }),

          'body' : forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Здесь введите текст сообщения'
          }),

          'title' : forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введите заголовок'
          }),
        }