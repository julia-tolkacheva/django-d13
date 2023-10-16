from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)
   
    def __str__(self):
        return f'{self.categoryName}'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    cTime = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255, default = 'Заголовок')
    body = models.TextField(default = 'Здесь должен быть текст')
    mainPic = models.ImageField(upload_to='user_images')
    postRate = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.postTitle}-({self.pk})' 

    def like(self):
        self.postRate += 1
        self.save()
    
    def dislike(self):
        self.postRate -= 1
        self.save()
    
    def preview(self, count=124):
        if (len(self.postBody) <= count):
            return self.postBody
        else:
            return self.postBody[:count-3]+'...'

    def get_absolute_url(self):
        return f'/post/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)   


class Comment(models.Model):
    toPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    fromUser = models.ForeignKey(User, on_delete = models.CASCADE)
    cTime = models.DateTimeField(auto_now_add = True)
    body = models.TextField(default = 'Комментарий')
    status = models.IntegerField(default = 0)

    def approve(self):
        self.status = 1
        self.save()
    
    def disapprove(self):
        self.status = 0
        self.save()

    def preview(self, count=124):
        if (len(self.commentBody) <= count):
            return self.commentBody
        else:
            return self.commentBody[:count-3]+'...'

    def __str__(self):
        return self.preview(40)
    

class Media(models.Model):
    picture = 'P'
    video   = 'V'
    file    = 'F'
    tChoice = [
        (picture, 'Картинка'),
        (video,   'Видео'),
        (file,    'Файл')
    ]
    toPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    type = models.CharField(max_length = 1, choices = tChoice, default = picture)
    media = models.FileField(upload_to= 'user_files')