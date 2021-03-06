# Generated by Django 4.0.2 on 2022-02-15 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0022_alter_jobposts_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiterprofile',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='recruiter/profile_pic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seekerprofile',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='seeker/profile_pic'),
            preserve_default=False,
        ),
    ]
