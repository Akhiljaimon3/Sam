# Generated by Django 5.0.7 on 2024-08-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_concession_history_secretcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_history',
            name='secretcode',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
