# Generated by Django 5.0.7 on 2024-08-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_alter_passwordreset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='concession_history',
            name='secretcode',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
