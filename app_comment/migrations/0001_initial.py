# Generated by Django 3.2.4 on 2021-06-14 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_blog', '0003_article_can_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sub', models.BooleanField(default=False)),
                ('body', models.TextField()),
                ('register_date', models.DateTimeField()),
                ('is_confirm', models.BooleanField(default=False)),
                ('article', models.ForeignKey(limit_choices_to={'can_comment': True}, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_blog.article')),
                ('sub_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcomments', to='app_comment.comment')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
