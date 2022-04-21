# Generated by Django 4.0.2 on 2022-02-22 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0034_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiterprofile',
            name='available_post',
        ),
        migrations.RemoveField(
            model_name='recruiterprofile',
            name='membership',
        ),
        migrations.RemoveField(
            model_name='recruiterprofile',
            name='plan_end_data',
        ),
        migrations.AddField(
            model_name='subscription',
            name='available_post',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='membership',
            field=models.CharField(choices=[('None', 'NONE'), ('Silver', 'Silver'), ('Gold', 'GOLD')], default='None', max_length=10),
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan_end_data',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
