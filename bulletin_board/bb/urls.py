from django.urls import path
from .views import MessageList

urlpatterns = [
    path('', MessageList.as_view(), name='messages'),
    # path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    # path('search', NewsSearch.as_view(), name='post_search'),
    # path('create', PostCreateView.as_view(), name='post_create'),
    # path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    # path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    # path('subscribe/<int:pk>', SubscribeView.as_view(), name='subscribe'),
    # path('upgrade', upgrade_acc, name='upgrade'),
]