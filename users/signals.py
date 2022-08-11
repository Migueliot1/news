from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    '''Creates User Profile when User is created.'''

    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email
        )


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    '''Deletes User when Profile is deleted.'''

    user = instance.user
    user.delete()
    