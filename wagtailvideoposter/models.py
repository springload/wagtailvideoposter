from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class EmbedVideoPosterImage(models.Model):
    """
    Represents a relationship among an Embed object (of type Video) and an Image
    """
    image = models.ForeignKey(
        related_name='+',
        blank=True,
        to='wagtailimages.Image',
        null=True
    )
    embed = models.ForeignKey(
        related_name='poster_image',
        blank=False,
        to='wagtailembeds.Embed',
        null=False
    )

    class Meta:  # Add unique constraint to avoid duplicates
        unique_together = ('image', 'embed',)


#  Pre Save signals to remove existing instance of the same embed
@receiver(pre_save, sender=EmbedVideoPosterImage)
def pre_embedvideoposterimage_save(sender, instance, **kwargs):
    try:
        existing_object = EmbedVideoPosterImage.objects.get(embed=instance.embed)
        existing_object.delete()
    except ObjectDoesNotExist:
        return
