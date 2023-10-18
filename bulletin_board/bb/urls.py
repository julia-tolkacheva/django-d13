from django.urls import path
from .views import MessageList, MessageDetail, MessageCreateView

urlpatterns = [
    path('', MessageList.as_view(), name='messages'),
    path('<int:pk>', MessageDetail.as_view(), name='msg_detail'),
    # path('search', NewsSearch.as_view(), name='post_search'),
    path('create', MessageCreateView.as_view(), name='msg_create'),
    # path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    # path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    # path('subscribe/<int:pk>', SubscribeView.as_view(), name='subscribe'),
    # path('upgrade', upgrade_acc, name='upgrade'),
]