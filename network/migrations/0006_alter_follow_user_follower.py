# Generated by Django 5.0.4 on 2025-04-16 18:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_follow_user_follower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='user_follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
