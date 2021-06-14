from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from app_blog.models import Article


class Comment(models.Model):
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    article = models.ForeignKey(
        Article,
        limit_choices_to={
            'can_comment': True,
            'status': 'P',
        },
        on_delete=models.CASCADE,
        related_name='comments',
    )

    sub_comment = models.ForeignKey(
        'self',
        limit_choices_to={
            'is_sub': False,
        },
        on_delete=models.CASCADE,
        related_name='subcomments',
        null=True,
        blank=True,
    )

    is_sub = models.BooleanField(default=False)
    body = models.TextField()
    register_date = models.DateTimeField()
    is_delete = models.BooleanField(default=False)
    delete_date = models.DateTimeField(null=True, blank=True)
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.body[:20]

    def save(self, *args, **kwargs):

        if self.sub_comment:
            self.is_sub = True

        if self.is_delete and not self.delete_date:
            self.delete_date = datetime.now()

        if not self.is_delete:
            self.delete_date = None

        super(Comment, self).save(*args, **kwargs)

    def clean(self):
        if self.is_sub and not self.sub_comment:
            raise ValidationError({
                'sub_comment': ValidationError('this field with is_sub=True can not be empty.', code='empty'),
            })
