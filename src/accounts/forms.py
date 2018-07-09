from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile, Interests, Wallet
from django.utils.timezone import now

class CreationForm_User(UserCreationForm):
    """
	Purpose: Register a new user
	Model Linked: CustomUser
    """
    def __init__(self,*args, **kwargs):
        super(CreationForm_User,self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self,commit=True):
        user = super(CreationForm_User,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.date_joined = now()
        user.is_provider = False
        user.is_active = True

        if commit:
            user.save()
        return user

class CreationForm_Provider(UserCreationForm):
    """
	Purpose: Register a new user
	Model Linked: CustomUser
    """
    def __init__(self,*args, **kwargs):
        super(CreationForm_Provider,self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self,commit=True):
        user = super(CreationForm_Provider,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.date_joined = now()
        user.is_provider = True
        user.is_active = False

        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    """
    Purpose: Facilitate login
	Model Linked: None
	Authentication backend handles appropriate model.
    """
    email = forms.EmailField(max_length=64,label="Email Address")
    password = forms.CharField(max_length=None,widget=forms.widgets.PasswordInput)

class UserProfileChangeForm(forms.ModelForm):
    """
    Purpose: Change/Edit User Profiles
    Model Linked: UserProfile
    the user field is excluded as it is obtained from the foreign key.

    """
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(UserProfileChangeForm,self).__init__(*args,**kwargs)
        f = self.fields.get('user_permissions',None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class InterestsForm(forms.ModelForm):
    class Meta:
        model = Interests
        fields = "__all__"
        exclude = ('user',)

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('eth_address',)
        exclude= ('user','balance',)

