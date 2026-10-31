from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def comment_created_notification(sender, instance, created, **kwargs):
    if created:
        print(f'New comment awaiting approval for post: {instance.post.title}')
