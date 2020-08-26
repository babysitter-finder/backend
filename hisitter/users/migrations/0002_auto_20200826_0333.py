# Generated by Django 3.0.9 on 2020-08-26 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babysitter',
            name='user_bbs',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userbbs', to=settings.AUTH_USER_MODEL, verbose_name='Babysitter'),
        ),
    ]
