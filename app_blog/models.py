from datetime import datetime
from django.conf import settings
from django.db import models
from tinymce.models import HTMLField


class Article(models.Model):
    SHARING_STATUS = (
        ('C', 'confirming'),
        ('D', 'draft'),
        ('P', 'published'),
        ('U', 'unconfirmed'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=250)
    slug = models.SlugField(allow_unicode=True)
    body = HTMLField()
    poster = models.ImageField()
    is_delete = models.BooleanField(default=False)
    delete_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=150, choices=SHARING_STATUS, default='D')
    last_update = models.DateTimeField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_delete and not self.delete_date:
            self.delete_date = datetime.now()
        super(Article, self).save(*args, **kwargs)
