# Generated by Django 4.0.2 on 2022-04-08 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0044_remove_subscription_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlanModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.CharField(choices=[('N', 'NONE'), ('S', 'SILVER'), ('G', 'GOLD')], default='N', max_length=1)),
                ('available_post', models.SmallIntegerField(default=0)),
                ('plan_end_date', models.DateTimeField(blank=True, null=True)),
                ('price_silver_id', models.CharField(max_length=255)),
                ('price_gold_id', models.CharField(max_length=255)),
                ('choice_plan_price_id', models.CharField(blank=True, max_length=255, null=True)),
                ('price_silver', models.IntegerField(blank=True, null=True)),
                ('price_gold', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Applicant',
            new_name='ApplicantModel',
        ),
        migrations.RenameModel(
            old_name='JobPosts',
            new_name='JobPostsModel',
        ),
        migrations.RenameModel(
            old_name='SeekerProfile',
            new_name='SeekerProfileModel',
        ),
        migrations.RenameModel(
            old_name='RecruiterProfile',
            new_name='RecruiterProfileModel',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
        migrations.AddField(
            model_name='subscriptionplanmodel',
            name='recruiter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='board.recruiterprofilemodel'),
        ),
    ]
