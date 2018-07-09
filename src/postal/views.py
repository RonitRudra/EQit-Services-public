from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .forms import NewMessageForm
from .models import Message, Feed
# Create your views here.

class home(TemplateView):
    template_name = 'postal/home.html'

class MessageNew(TemplateView):
    template_name = 'postal/new-message.html'

    def get(self, request, *args, **kwargs):
        # binds the sender to current user, throws error message in HTML so not used
        #form = NewMessageForm(request.user)
        
        # This works
        # initial is used to set initial values for fields passed as dictionaries
        form = NewMessageForm(request.user,initial={'sender':request.user})
        # form field widgets can be modified. Below sender is locked.
        form.fields['sender'].widget.attrs['readonly'] = True
        # NOTE: disabled does not post contents of form field
        #form.fields['sender'].widget.attrs['disabled'] = True
        return render(request,self.template_name,{'form':form})
        
    def post(self, request, *args, **kwargs):
        # Even if user edits html and changes sender, backend ignores changes in
        # favor of original instantiated data.
        form = NewMessageForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Message Sent')
            return redirect('postal:home')
        else:
            messages.add_message(request,messages.ERROR,'Something went wrong. Try again.')
            return redirect('postal:new-message')

class Inbox(ListView):
    template_name = 'postal/inbox.html'
    model = Message

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by('-date_sent')

class Sentbox(ListView):
    template_name = 'postal/sentbox.html'
    model = Message

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-date_sent')

class MessageDetail(DetailView):
    template_name = 'postal/message_detail.html'
    model = Message

    def get(self, request, *args, **kwargs):
        # overriding get method
        # preventing unauthorized users from viewing emails.
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        #---------------- Only this part added----------
        if request.user == context['object'].receiver or request.user == context['object'].sender:
            # standard return
            return self.render_to_response(context)

        else:
            return redirect('postal:inbox')
        #-----------------------------------------------


class GlobalFeed(ListView):
    template_name = 'postal/feed.html'
    model = Feed
    paginate_by = 100

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['now'] = timezone.now()
    #    return context