from django.urls import path
from .views import *

urlpatterns = [
    path('xls/', export_xls, name='export_xls'),
    path('api/v1/poll', PollAPIView.as_view()),
    path('api/v1/poll/<int:pk>', PollAPIViewDetail.as_view()),
    path('api/v1/poll/active', PollActiveAPIView.as_view()),
    path('api/v1/poll/finished', PollFinishedAPIView.as_view()),
    path('api/v1/add_vote', add_vote, name='add_vote'),
    path('api/v1/poll/winner/<int:pk>', get_winner, name='get_winner'),
    path('api/v1/poll/members/<int:pk>', get_members, name='get_members'),
]