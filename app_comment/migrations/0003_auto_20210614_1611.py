# Generated by Django 3.2.4 on 2021-06-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_comment', '0002_auto_20210614_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='delete_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]