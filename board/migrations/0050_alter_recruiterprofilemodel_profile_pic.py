# Generated by Django 4.0.2 on 2022-04-14 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0049_recruiterprofilemodel_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterprofilemodel',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='recruiter/profile_pic'),
            preserve_default=False,
        ),
    ]