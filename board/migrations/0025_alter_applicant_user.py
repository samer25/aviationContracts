# Generated by Django 4.0.2 on 2022-02-17 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0024_applicant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seeker', to=settings.AUTH_USER_MODEL),
        ),
    ]
