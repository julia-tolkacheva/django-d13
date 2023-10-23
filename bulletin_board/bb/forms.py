from django.forms import ModelForm
from .models import Post, Comment, Reply
from django import forms
from allauth.account.forms import SignupForm
from django.forms.widgets import HiddenInput
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


class AddCommentForm(ModelForm):
    """Форма добавления комментария"""
    class Meta:
        model = Comment
        fields = ('cbody',) 
    
        widgets={"cbody": forms.Textarea(attrs={
          'class': 'form-control',
          'cols': 80,
          'rows': 5,
          'placeholder': 'Здесь введите текст сообщения',
          }),
        }
        labels={'cbody': ''}
 

class MessageCreateForm (ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'cTime', 'postRate',)
        widgets = {
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
        labels = {
            'category': 'Выберите одну или несколько категорий:',
            'body': 'Напишите здесь ваш текст:',
            'title': 'Заголовок вашего сообщения',
            'mainPic': 'Выберете главную картинку(не менее 1024х768):'
        }


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('rbody',)

        widgets = {
          'rbody': forms.Textarea(attrs={
          'class': 'form-control',
          'cols': 80,
          'rows': 5,
          'placeholder': 'Здесь введите текст сообщения',
          
          }),
        }
        labels={'rbody': 'Ваш ответ:'}

