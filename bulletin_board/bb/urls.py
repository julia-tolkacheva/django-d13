from django.urls import path
from .views import MessageList, MessageDetail, MessageCreateView, \
MessageUpdateView, MessageDeleteView, CommentList, CommentReply, CommentDeleteView

urlpatterns = [
    path('', MessageList.as_view(), name='messages'),
    path('<int:pk>', MessageDetail.as_view(), name='msg_detail'),
    # path('search', NewsSearch.as_view(), name='post_search'),
    path('my_comments', CommentList.as_view(), name='comments'),
    path('create', MessageCreateView.as_view(), name='msg_create'),
    path('update/<int:pk>', MessageUpdateView.as_view(), name='msg_update'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='msg_delete'),
    path('comdelete/<int:pk>', CommentDeleteView.as_view(), name='com_delete'),
    path('reply/<int:pk>', CommentReply.as_view(), name='reply'),
    # path('upgrade', upgrade_acc, name='upgrade'),
]