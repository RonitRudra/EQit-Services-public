from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from accounts.models import CustomUser
from postal.models import Feed

# Create your models here.

class Gig(models.Model):
	
    class Meta:
        verbose_name = _('gig')
        verbose_name_plural = _('gigs')

    poster = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    is_active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default=now)
    description = models.TextField(max_length = 500,default = '')
    tokenvalue = models.PositiveIntegerField(default = 0)
    number_allowed = models.PositiveSmallIntegerField(default=1)
    

    def __str__(self):
        return ''.join("ID:{} Title:{}".format(str(self.id),self.title))

class GigType(models.Model):
    class Meta:
        verbose_name = _('gig type')
        verbose_name_plural = _('gig types')

    gig = models.OneToOneField(Gig,primary_key=True, on_delete=models.CASCADE)
    science = models.BooleanField(default=False)
    technology = models.BooleanField(default=False)
    engineering =  models.BooleanField(default=False)
    arts = models.BooleanField(default=False)
    music = models.BooleanField(default=False)
    business = models.BooleanField(default=False)
    hospitality = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)

    def __str__(self):
        return str(self.gig)

class LikedGig(models.Model):
    class Meta:
        verbose_name = _('liked gig')
        verbose_name_plural = _('liked gigs')

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    gig = models.ForeignKey(Gig,on_delete=models.CASCADE)
    status = models.NullBooleanField(default=None, blank=True, null=True)
    date_liked = models.DateTimeField(default=now)


    def __str__(self):
        if self.status==True:
            stat = 'liked'
        else:
            stat = 'disliked'
        return '{} {} {}'.format(str(self.user),stat,str(self.gig.title))

class GigLocation(models.Model):
    class Meta:
        verbose_name = _('gig location')
        verbose_name_plural = _('gig locations')

	# Setting Name as primary key, hence verify similar names before adding to database
    gig = models.OneToOneField(Gig,on_delete=models.CASCADE)
    address1 = models.CharField(max_length = 128, default = '')
    address2 = models.CharField(max_length = 128, default = '')
    city = models.CharField(max_length = 64, default ='')
    zipcode = models.CharField(max_length=6, default = '')
    contact_first_name = models.CharField(max_length=32, default = '')
    contact_last_name = models.CharField(max_length=32, default = '')
    contact_phone = models.CharField(max_length=10,default = '')

    def __str__(self):
        return '{}:{}'.format(str(self.gig_id),self.address1)


class GigApproval(models.Model):
    class Meta:
        verbose_name = _('gig approval')
        verbose_name_plural = _('gig approvals')

    liked = models.OneToOneField(LikedGig, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_checkin_requested = models.BooleanField(default=False)
    is_checkin_approved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default = False)

    def __str__(self):
        return str(self.id)


def create_gigapproval(sender,**kwargs):
	if kwargs['created']:
		interests = GigApproval.objects.create(liked=kwargs['instance'])

post_save.connect(create_gigapproval,sender=LikedGig)

def create_feed(sender,**kwargs):
    if kwargs['created']:
        gig = kwargs['instance']
        poster = gig.poster
        print(gig.title)
        body = '{} posted a gig titled:{}'.format(str(poster),gig.title)
        feed = Feed.objects.create(poster=poster,body=body)

post_save.connect(create_feed,sender=Gig)