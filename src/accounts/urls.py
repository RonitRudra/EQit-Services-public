
"""
Definition of urls for accounts app
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .views import *
# IMPORTANT: Check deprecation of function based views from django v1.9 to v1.11
# For PasswordResetView flow, the name should be as specified as password_reset looks for the exact name.
urlpatterns = [
	url(r'^login/$',LoginPre.as_view(),name='login'),
        url(r'^login/user/$',LoginUser.as_view(),name='login-user'),
	url(r'^login/provider/$',LoginProvider.as_view(),name='login-provider'),
        url(r'^sign-up/$',SignupPre.as_view(),name='signup'),
        url(r'^sign-up/user/$',SignupUser.as_view(),name='signup-user'),
        url(r'^sign-up/provider/$',SignupProvider.as_view(),name='signup-provider'),
        url(r'^logout/$',Logout.as_view(),name='logout'),
        url(r'^profile/$',Profile.as_view(),name='profile'),
	url(r'^profile/edit/$',ProfileEdit.as_view(),name='profile_edit'),
	url(r'^profile/edit/change-password/$',PasswordChange.as_view(),name='change_password'),
        url(r'^wallet/$',EthWallet.as_view(),name='wallet'),
        url(r'^wallet/edit/$',EthWalletEdit.as_view(),name='wallet-edit'),
	url(r'^reset-password/$',
	 PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
							success_url=reverse_lazy('accounts:password_reset_done'),
							email_template_name='accounts/password_reset_email.html',
							subject_template_name = 'accounts/password_reset_subject.txt'),
							name='password_reset'),
	url(r'^reset-password/done/$',
	 PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
	 name='password_reset_done'),
	url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	 PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
	 success_url=reverse_lazy('accounts:password_reset_complete')),
	 name='password_reset_confirm'),
	url(r'reset-password/complete/$',
	 PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
	 name='password_reset_complete'),
	url(r'^interests/$',InterestsEdit.as_view(),name='interests'),
    ]