# Generated by Django 4.0.2 on 2022-02-22 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0041_subscription_price_gold_subscription_price_silver'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
