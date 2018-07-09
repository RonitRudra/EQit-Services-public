import re
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
# All middleware require a class based definition
# required functions: __init__, __call__ which are to be defined exactly as docs
# The init function takes get_response as optional due to changes in middleware definitions
# from 1.9 to 1.10+
EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings,'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [re.compile(x) for x in settings.LOGIN_EXEMPT_URLS]


class Middleware_LoginRequired(object):
	"""
	1. If user is not authenticated, only allow access to exempt pages
	2. If authenticated user tries to access login and signup pages, redirect to profile
	3.
	"""

	def __init__(self,get_response=None):
		self.get_response = get_response

	def __call__(self,request):
		response = self.get_response(request)
		return response

	def process_view(self,request,view_func,view_args,view_kwargs):
		#assert hasattr(request,user)
		path = request.path_info.lstrip('/')
		url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
		if path == reverse('accounts:logout').lstrip('/'):
			logout(request)
		#if request.user.is_authenticated() and url_is_exempt:
		#	return redirect(settings.LOGIN_REDIRECT_URL)
		#elif request.user.is_authenticated() or url_is_exempt:
		#	return None
		#else:
		#	return redirect(settings.LOGIN_URL)
		if not request.user.is_authenticated() and not url_is_exempt:
			return redirect(settings.LOGIN_URL)
		if request.user.is_authenticated() and url_is_exempt:
			return redirect('accounts:profile')
