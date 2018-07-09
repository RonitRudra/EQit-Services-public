from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import CustomUser
# Create your models here.

class Message(models.Model):
    class Meta:
        verbose_name = _('message')
        verbose_name_plural  = _('messages')

    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='receiver')
    body = models.TextField(max_length=500)
    date_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}->{}'.format(str(self.sender),str(self.receiver))

class Feed(models.Model):
    class Meta:
        verbose_name = _('feed')
        verbose_name_plural  = _('feeds')

    poster = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return '{} on {}'.format(str(self.sender),str(self.date_posted))