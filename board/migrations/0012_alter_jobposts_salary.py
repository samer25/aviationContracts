# Generated by Django 4.0.2 on 2022-02-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_alter_recruiterprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposts',
            name='salary',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
