# Python imports
import datetime
import random
import string
import uuid
# Django imports
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.utils.http import urlquote
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Helper attributes and functions
DEFAULT_IMAGE = 'profile_picture/default.png'
def generate(size=32):
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(size)])
DEFAULT_ADDRESS = '0x0000000000000000000000000000000000000000'
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Requires email address instead of username.
    Required Functions:
        _create_user
        create_user
        create_superuser
    """
    def _create_user(self,email,password,is_staff,is_superuser,**extra_fields):
        # save login time
        log_time = timezone.now()

        if not email:
            raise ValueError('Email not provided')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=log_time,
                          date_joined=log_time,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password=None,**extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)

    def create_superuser(self,email,password,**extra_fields):
        return self._create_user(email,password,True,True,**extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    User model supporting custom authentication backend.
    Auth field is set as email address.
    Fields:
        Username
        Email
        First Name
        Last Name
    """
    email = models.CharField(max_length=64,unique=True)
    # meta fields. Do not modify from client side.
    date_joined = models.DateTimeField(_('date joined'),default = timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.email)

    def get_absolute_url(self):
        return 'accounts/%s/'%urlquote(self.email)

    def get_full_name(self):
        full_name = '{} {}'.format(self.userprofile.first_name,self.userprofile.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.userprofile.first_name

    def email_user(self,subject,message,from_email=None):
        send_mail(subject,message,from_email,[self.email])

class UserProfile(models.Model):

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    #username = models.CharField(max_length=32,unique=True,null=True,blank=True)
    #username = models.CharField(max_length=32,default=uuid.uuid4)
    first_name = models.CharField(max_length=64,default = '')
    middle_name = models.CharField(max_length=64,default = '',blank=True)
    last_name = models.CharField(max_length=64,default = '')
    dob = models.DateField(default=datetime.date.today)
    description = models.TextField(max_length=500,default = '')
    address1 = models.CharField(max_length = 128, default = '')
    address2 = models.CharField(max_length = 128, default = '')
    city = models.CharField(max_length=32,default = '')
    zipcode = models.CharField(max_length=5,default = '')
    website = models.URLField(default='',blank=True)
    phone = models.CharField(max_length=10,default='')
    profile_picture = models.ImageField(upload_to='profile_picture',default = DEFAULT_IMAGE)
	# Media deployment different in development and production
    def __str__(self):
        if self.user.is_provider==True:
            stat = 'Provider'
        else:
            stat = 'User'
        return '{} : {} '.format(stat,str(self.user))

    #def save(self):
    #    if not self.username:
    #        self.username = generate()
    #        while UserProfile.objects.filter(username=self.username).exists():
    #            self.username = generate()
    #    super(UserProfile,self).save()

class Interests(models.Model):
	
    class Meta:
        verbose_name = _('interest')
        verbose_name_plural = _('interests')

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    science = models.BooleanField(default=False)
    technology = models.BooleanField(default=False)
    engineering =  models.BooleanField(default=False)
    arts = models.BooleanField(default=False)
    music = models.BooleanField(default=False)
    business = models.BooleanField(default=False)
    hospitality = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)
        
    def __str__(self):
        if self.user.is_provider==True:
            stat = 'Provider'
        else:
            stat = 'User'
        return '{} : {} '.format(stat,str(self.user))

class Friends(models.Model):

    class Meta:
        verbose_name = _('friend')
        verbose_name_plural = _('friends')

    PersonA = models.ForeignKey(CustomUser,related_name='PersonA')
    PersonB = models.ForeignKey(CustomUser,related_name='PersonB')
    date_added = models.DateField()

class Wallet(models.Model):
    class Meta:
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    eth_address = models.CharField(max_length=42,default=DEFAULT_ADDRESS)
    balance = models.PositiveIntegerField(default=0)

# Post Save link functions-----------------------------------------------------

def create_interests(sender,**kwargs):
	if kwargs['created']:
		interests = Interests.objects.create(user=kwargs['instance'])

# Linked UserProfile and CustomUser--------------------------------------------
# If a new entry is made in CustomUser, then code is triggered to create
## a new entry in UserProfile linked to the Primary key of the CustomUser model
def create_user_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

def create_wallet(sender,**kwargs):
	if kwargs['created']:
		interests = Wallet.objects.create(user=kwargs['instance'])


post_save.connect(create_user_profile,sender=CustomUser)
post_save.connect(create_interests,sender=CustomUser)
post_save.connect(create_wallet,sender=CustomUser)


