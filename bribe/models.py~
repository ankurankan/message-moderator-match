from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Tag(models.Model):
    tagname = models.CharField(max_length=50)
    def __unicode__(self):
        return self.tagname


class Report(models.Model):
    slug = models.CharField(max_length=20, null=True, blank=True)
    body = models.TextField(max_length=1000, default="Please enter your report here")
    tag = models.ManyToManyField(Tag)
    review_status = models.BooleanField(default=False)

    def __unicode__(self):
        return self.slug


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    preferences = models.CharField(verbose_name="Preferences", max_length=50)
    
    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


    
