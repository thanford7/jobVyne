from django.db import models


__all__ = ('SocialPlatform',)


class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
