from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Product

@receiver(m2m_changed, sender=Product.like.through)
def like_count_signals(sender, instance, **kwargs):
    instance.total_like = instance.like.count()
    instance.save()
