"""
Definition of urls for EQit_Services.
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
import django.contrib.auth.views
from django.contrib import admin
admin.autodiscover()
urlpatterns = [

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('home.urls',namespace='home')),
    url(r'^account/',include('accounts.urls',namespace="accounts")),
    url(r'^gig/',include('gigs.urls',namespace='gigs')),
    url(r'^postal/',include('postal.urls',namespace='postal'))

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
