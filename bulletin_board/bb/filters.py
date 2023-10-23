from django_filters import FilterSet, CharFilter
from .models import Post, Comment
from django import forms


class CommentsFilter(FilterSet):
        
    #postAuthor__userModel__username = CharFilter(lookup_expr='icontains') 
    

    class Meta:
        model=Comment

        fields = {
            'toPost' : ['exact'],
            'fromUser' : ['exact'],
        }

    def __init__(self, *args, **kwargs):
       super(CommentsFilter, self).__init__(*args, **kwargs)
       self.filters['toPost'].label="Пост"
       self.filters['fromUser'].label="От пользователя"



