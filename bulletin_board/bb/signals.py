from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail, mail_managers
from .models import Post, Comment, Reply
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

#функция обработки сигнала записи в базу данных
@receiver(sender=Comment, signal=post_save )
def notify_author_about_new_comment(sender, instance, **kwargs):
    '''уведомление автора поста о новом комментарии '''
    post = instance.toPost
    author = post.author

    print(author, author.email)
    html_content = render_to_string(
        'messages/notification.html',
        {
            'post': post,
            'comment': instance,
            'username': author,
            'domain': Site.objects.get_current().domain,
            'relative_url': post.get_absolute_url()+'#comments'
        } 
    )
    msg = EmailMultiAlternatives(
        subject=f'Новый комментарий к посту:{post.title}',
        body=instance.cbody,
        from_email='julia.tolkacheva.666@yandex.ru',
        to=[author.email,]
    )
    msg.attach_alternative(html_content,"text/html")
    msg.send()
 

@receiver(sender=Reply, signal=post_save )
def notify_user_about_new_reply(sender, instance, **kwargs):
    '''уведомление пользователя о том, что автор ответил на его комментарий '''
    comment = instance.toComment
    post = comment.toPost
    author = comment.fromUser

    print(author, author.email)
    html_content = render_to_string(
        'messages/notification.html',
        {
            'title': comment.preview(50),
            'body': instance.rbody,
            'username': author,
            'domain': Site.objects.get_current().domain,
            'relative_url': post.get_absolute_url()+'#comments'
        } 
    )
    msg = EmailMultiAlternatives(
        subject=f'Новый комментарий к сообщению',
        body=instance.rbody,
        from_email='julia.tolkacheva.666@yandex.ru',
        to=[author.email,]
    )
    msg.attach_alternative(html_content,"text/html")
    msg.send()

 