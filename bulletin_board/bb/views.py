from typing import Any, Dict
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView, ModelFormMixin
from django.http import HttpResponseRedirect
from .models import Post, Category, Comment, Media, PostCategory, Reply
from .forms import MessageCreateForm, AddCommentForm, ReplyForm, MediaCreateForm
from .filters import CommentsFilter
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Min, Sum
# LoginRequiedMixin - для авторизованного доступа к странице
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# main page view
class MessageList(ListView):
    model = Post
    ordering = ['-cTime']
    template_name = 'messages/main.html'
    context_object_name = 'messages'
    paginate_by = 3
    queryset = Post.objects.all().annotate(num_comments=Count('comment', distinct=True), 
                                           num_files=Count('media', distinct=True),
                                           )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        context['recent_posts'] = Post.objects.all().order_by('-cTime')[:5]
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class MessageDetail(ModelFormMixin, DetailView):

    model = Post
    template_name = 'messages/detail.html'
    context_object_name = 'message'
    form_class = AddCommentForm

    success_url = '/messages/'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        context['post_cat'] = PostCategory.objects.filter(post=self.get_object())
        context['media'] = Media.objects.filter(toPost=self.get_object())
        comments = Comment.objects.filter(toPost=self.get_object())
        context['replies'] = Reply.objects.filter(toComment__toPost=self.get_object())
        context['comments_count'] = comments.count()
        context['comments'] = comments
        context['recent_posts'] = Post.objects.all()[:5]
        return context
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.fromUser = self.request.user
        self.object.toPost = self.get_object()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return self.form_valid(form)

        return render(request, self.template_name, {"form": form})

 
# класс представления для отображения комментариев к постам юзера
class CommentList(ListView):

    context_object_name = 'comments'
    template_name = 'messages/comments.html'

    def get_queryset(self):
        self.posts = Comment.objects.filter(toPost__author=self.request.user)
        return self.posts

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        context['replies'] = Reply.objects.filter(toComment__toPost__author=self.request.user)
        context['filter'] = CommentsFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class CommentReply(FormView):

    model = Reply
    template_name = 'messages/reply.html'
    context_object_name = 'reply'
    form_class = ReplyForm
    success_url = '/messages/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        #add author field
        comment_pk = self.request.path.split('/')[-1]
        target_comment = Comment.objects.get(pk=comment_pk)
        self.object.toComment = target_comment
        self.object.save()
        #save categories (m2m)
        # form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())
    

#класс представления для создания поста
class MessageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('bb.add_post',)
    template_name = 'messages/create.html'
    form_class = MessageCreateForm
    context_object_name = 'message'
    success_url = '/messages'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        author = self.request.user.id
        context['categories'] = Category.objects.annotate(num_posts=Count('post')) 
        context['time_now'] = timezone.localtime(timezone.now())
        return context  

    def form_valid(self, form):
        self.object = form.save(commit=False)
        #add author field
        self.object.author = self.request.user
        self.object.save()
        #save categories (m2m)
        form.save_m2m()
        return HttpResponseRedirect(self.request.path + '/' + str(self.object.pk))
    
#класс представления для создания медиа файлов
class MediaCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('bb.add_media',)
    template_name = 'messages/media.html'
    form_class = MediaCreateForm
    context_object_name = 'media'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post')) 
        context['time_now'] = timezone.localtime(timezone.now())
        return context  

    def form_valid(self, form):
        self.object = form.save(commit=False)
        #add author field
        message_pk = self.request.path.split('/')[-1]
        target_message = Post.objects.get(pk=message_pk)
        self.object.toPost = target_message
        self.object.save()
        return HttpResponseRedirect(self.request.path)
    



#класс представления для изменения поста
class MessageUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('bb.change_post',)
    template_name = 'messages/create.html'
    form_class = MessageCreateForm
    context_object_name = 'message'
    success_url = '/messages/'


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    

#класс представления для удаления поста
class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'message'
    permission_required = ('bb.delete_post',)
    template_name = 'messages/delete.html'
    queryset = Post.objects.all()
    success_url = '/messages'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        context['post_cat'] = PostCategory.objects.filter(post=self.get_object())
        context['media'] = Media.objects.filter(toPost=self.get_object())
        comments = Comment.objects.filter(toPost=self.get_object())
        context['replies'] = Reply.objects.filter(toComment__toPost=self.get_object())
        context['comments_count'] = comments.count()
        context['comments'] = comments
        return context

#класс представления для удаления комментария
class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    context_object_name = 'comment'
    permission_required = ('bb.delete_comment',)
    template_name = 'messages/delete.html'
    queryset = Comment.objects.all()
    success_url = '/messages/my_comments'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        comments = Comment.objects.filter(pk=self.get_object().pk)
        context['replies'] = Reply.objects.filter(toComment=self.get_object())
        context['comments'] = comments
        return context
