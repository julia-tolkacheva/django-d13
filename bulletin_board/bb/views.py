from typing import Any, Dict
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from .models import Post, Category, Comment, Media
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator


# main page view
class MessageList(ListView):
    model = Post
    #queryset = Post.objects.order_by("-postDateTime")
    ordering = ['-cTime']
    template_name = 'messages/main.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        # context['time_now'] = timezone.localtime(timezone.now())
        # context['empty'] = None
        # context['filter'] = NewsFilter(self.request.GET,
        #                                queryset=self.get_queryset())
        # context['choices'] = Post.postChoice
        # context['form'] = NewsForm()
        # context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
