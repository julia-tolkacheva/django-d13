from typing import Any, Dict
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView, ModelFormMixin
from django.http import HttpResponseRedirect
from .models import Post, Category, Comment, Media, PostCategory
from .forms import MessageCreateForm, AddCommentForm
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
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        context['messages'] = Post.objects.annotate(num_comments=Count('comment'))
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

    success_url = f'/messages/'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        context['post_cat'] = PostCategory.objects.filter(post=self.get_object())
        context['media'] = Media.objects.filter(toPost=self.get_object())
        comments = Comment.objects.filter(toPost=self.get_object())
        context['comments_count'] = comments.count()
        context['comments'] = comments
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

 

#класс представления для создания поста
class MessageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('bb.add_post',)
    template_name = 'messages/create.html'
    form_class = MessageCreateForm
    context_object_name = 'message'
    success_url = ''

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        author = self.request.user.id
        context['categories'] = Category.objects.annotate(num_posts=Count('post')) 
        context['time_now'] = timezone.localtime(timezone.now())
        return context  

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    




#класс представления для изменения поста
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'newspaper/create_post.html'
    form_class = MessageCreateForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

#класс представления для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'newspaper/delete_post.html'
    queryset = Post.objects.all()
    success_url = '/news/'#reverse_lazy('newspaper:news')