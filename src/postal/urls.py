
"""
Definition of urls for postal app
"""
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',home.as_view(),name='home'),
    url(r'^inbox/$',Inbox.as_view(),name='inbox'),
    url(r'^sentbox/$',Sentbox.as_view(),name='sentbox'),
    url(r'^new-message/$',MessageNew.as_view(),name='new-message'),
    url(r'^message/detail/(?P<pk>[0-9]+)/$', MessageDetail.as_view(), name='detail'),
    url(r'^feed/$',GlobalFeed.as_view(),name='feed')
    ]