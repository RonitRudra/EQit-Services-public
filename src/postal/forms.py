from django import forms
from django.utils.timezone import now

from .models import Message
from accounts.models import CustomUser

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender','receiver','body',)
   
    ## the logged in user is passed as argument to init which filters the queryset
    ## You wouldn't want the user to send messages to themselves
    ## For good measure, sender field is filtered to contain only current user
    def __init__(self, user, *args, **kwargs):
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields['receiver'].queryset = CustomUser.objects.exclude(email=user)
        self.fields['sender'].queryset = CustomUser.objects.filter(email=user)
    ## Ensures user cannot tamper with sender field
    ## Clean methods for each field are clean_<fieldname>  
    def clean_sender(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.sender
        else:
            return self.cleaned_data['sender']

