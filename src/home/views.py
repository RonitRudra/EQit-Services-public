from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.
class Home(TemplateView):
    template_name = 'home/index.html'

class HomeRedirect(TemplateView):
    # redirect uses reverse() to process the argument,
    # so pass the namespace and name of the url pattern as stated in views.py
    def get(self, request, *args, **kwargs):
        return redirect('home:home')