
from django.conf import settings
from django.conf.urls import url
from .views import *

urlpatterns = [url(r'^$',Home.as_view(),name='home'),
               url(r'^browse/$',GigBrowse.as_view(),name='browse'),
               url(r'^new-gig/$',GigNew.as_view(),name='new-gig'),
               url(r'^detail/(?P<pk>[0-9]+)/$', GigDetail.as_view(), name='detail'),
               url(r'^activity/$',ViewActivity.as_view(),name='view-activity'),
               url(r'^activity/manage/(?P<pk>[0-9]+)/$', GigManage.as_view(), name='manage'),
               url(r'^activity/manage/(?P<pk>[0-9]+)/approval/$', GigManageApproval.as_view(), name='manage-approval'),
               url(r'^activity/manage/(?P<pk>[0-9]+)/checkin/$', GigManageCheckin.as_view(), name='manage-checkin'),
               url(r'^activity/manage/(?P<pk>[0-9]+)/payment/$', GigManagePayment.as_view(), name='manage-payment'),
               url(r'^activity/go/(?P<pk>[0-9]+)/$',GigGo.as_view(),name='go'),
			   ]