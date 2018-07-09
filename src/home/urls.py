
"""
Definition of urls for home app
"""
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',HomeRedirect.as_view()),
    url(r'^home/$',Home.as_view(),name='home')
    ]