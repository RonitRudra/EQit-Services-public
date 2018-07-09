
# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


# Local imports
from .forms import CreationForm_User, CreationForm_Provider, UserLoginForm, UserProfileChangeForm, InterestsForm, WalletForm
from .models import CustomUser, UserProfile, Interests, Wallet, DEFAULT_ADDRESS
# Create your views here.
# Views take a request and return a response,
# Return a template response through render

class LoginPre(TemplateView):
	template_name = 'accounts/login.html'

class LoginUser(TemplateView):
    template_name = 'accounts/login_user.html'
    
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                username = CustomUser.objects.get(email=form.cleaned_data['email'])
                if username.is_provider == True:
                    messages.add_message(request,messages.ERROR,'You were using the wrong login page. Login Here')
                    return redirect('accounts:login-provider')
                password = form.cleaned_data['password']
                user = authenticate(username=username,password=password)
                if user is None:
                    raise ValidationError(message='Validation Failed')
            except (ObjectDoesNotExist,ValidationError):
                messages.add_message(request, messages.ERROR, 'Username or Password Does not Match')
                return redirect('accounts:login-user')
            if user.is_active:
                login(request,user)
                messages.add_message(request,messages.SUCCESS,'You are now logged in.')
                return redirect('home:home')
            else:
                messages.add_message(request,messages.ERROR,'Your account is not active. Please contact our staff.')
                return redirect('accounts:login-user')
        else:
            messages.add_message(request, messages.ERROR, 'There were invalid entries in the form.')
            return redirect('accounts:login-user')


class LoginProvider(TemplateView):
    template_name = 'accounts/login_provider.html'

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                username = CustomUser.objects.get(email=form.cleaned_data['email'])
                if username.is_provider == False:
                    messages.add_message(request,messages.ERROR,'You were using the wrong login page. Login Here')
                    return redirect('accounts:login-user')
                password = form.cleaned_data['password']
                user = authenticate(username=username,password=password)
                if user is None:
                    raise ValidationError(message='Validation Failed')
            except (ObjectDoesNotExist,ValidationError):
                messages.add_message(request, messages.ERROR, 'Username or Password Does not Match')
                return redirect('accounts:login-provider')

            if user.is_active:
                login(request,user)
                messages.add_message(request,messages.SUCCESS,'You are now logged in.')
                return redirect('home:home')
            else:
                messages.add_message(request,messages.ERROR,'Your account is not active. Please contact our staff.')
                return redirect('accounts:login-provider')
        else:
            messages.add_message(request, messages.ERROR, 'There were invalid entries in the form.')
            return redirect('accounts:login-provider')


class SignupPre(TemplateView):
    template_name = 'accounts/signup.html'

class SignupUser(TemplateView):
    template_name = 'accounts/signup_user.html'

    def get(self, request, *args, **kwargs):
        form = CreationForm_User()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = CreationForm_User(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Your account has been created. Please proceed to log in.')
            return redirect('accounts:login-user')
        else:
            for error_code,error_desc in form.error_messages.items():
                messages.add_message(request,messages.ERROR,error_desc)
            return redirect('accounts:signup-user')


class SignupProvider(TemplateView):
    template_name = 'accounts/signup_provider.html'

    def get(self, request, *args, **kwargs):
        form = CreationForm_Provider()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = CreationForm_Provider(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Your account has been created but not activated. Please await an email from our staff.')
            return redirect('accounts:login-provider')
        else:
            for error_code,error_desc in form.error_messages.items():
                messages.add_message(request,messages.ERROR,error_desc)
            return redirect('accounts:signup-provider')

class Logout(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request,messages.SUCCESS,'You have been logged out.')
        return redirect('accounts:login')

class Profile(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'user':request.user})

class ProfileEdit(TemplateView):
    """
    Prefixes are used to differentiate forms.
    PKs of form1 user is required by the second form as it's a one-one relationship
    For editing forms, pass an instance to pre-populate form for GET request, or
    retain request params for POST request so correct entry is edited.
    """
    template_name = 'accounts/profile_edit.html'

    def get(self, request, *args, **kwargs):
        google_api_key = settings.GOOGLE_PLACES_API_KEY
        form = UserProfileChangeForm(instance=UserProfile.objects.get(user=request.user))
        return render(request,self.template_name,{'form':form,'google_api_key':google_api_key})
    
    def post(self, request, *args, **kwargs):
        form=UserProfileChangeForm(request.POST,request.FILES,instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Your Changes Have Been Saved')
            return redirect('accounts:profile')
        else:
            messages.add_message(request,messages.ERROR,'There were invalid entries in the form.')
            return redirect('accounts:profile_edit')


class PasswordChange(TemplateView):
    template_name = 'accounts/change_password.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            # prevent session invalidation and logout
            update_session_auth_hash(request,user)
            messages.add_message(request,messages.SUCCESS, 'Password Succesfully Updated!')
            return redirect('accounts:profile')
        else:
            messages.add_message(request,messages.ERROR, 'There were invalid entries in the form.')
            redirect(request,'accounts:change_password')


class InterestsEdit(TemplateView):
    template_name = 'accounts/interests.html'

    def get(self, request, *args, **kwargs):
        form = InterestsForm(instance=Interests.objects.get(user=request.user))
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = InterestsForm(request.POST,instance=Interests.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, 'Your Changes Have Been Saved')
            return redirect('accounts:profile')
        else:
            messages.add_message(request,messages.ERROR, 'There were invalid entries in the form.')
            redirect(request,'accounts:interests')

class EthWallet(TemplateView):
    template_name = 'accounts/wallet.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        wallet = user.wallet
        return render(request,self.template_name,{'wallet':wallet})

class EthWalletEdit(TemplateView):
    template_name = 'accounts/wallet_edit.html'

    def get(self, request, *args, **kwargs):
        form = WalletForm(instance=Wallet.objects.get(user=request.user))
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = WalletForm(request.POST,instance=Wallet.objects.get(user=request.user))
        if form.is_valid():
            if form.cleaned_data['eth_address'] == DEFAULT_ADDRESS:
                messages.add_message(request,messages.ERROR, 'You cannot use that address')
                return redirect('accounts:wallet-edit')
            num = len(Wallet.objects.filter(eth_address=form.cleaned_data['eth_address']))
            if num !=0:
                messages.add_message(request,messages.ERROR, 'The address already exists')
                return redirect('accounts:wallet-edit')
            form.save()
            messages.add_message(request,messages.SUCCESS, 'Your Changes Have Been Saved')
            return redirect('accounts:wallet')
        else:
            messages.add_message(request,messages.ERROR, 'There were invalid entries in the form.')
            redirect(request,'accounts:wallet')
